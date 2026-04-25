from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Iterable, List

from .schemas import RetrievedChunk, RetrievalPlan

TOKEN_RE = re.compile(r"[a-zA-Z0-9_]+")


def tokens(text: str) -> set[str]:
    return set(TOKEN_RE.findall(text.lower()))


class PublicRetriever:
    def __init__(self, data_dir: str | Path = "data") -> None:
        self.data_dir = Path(data_dir)

    def retrieve(self, query: str, plan: RetrievalPlan) -> List[RetrievedChunk]:
        if not plan.enabled:
            return []
        chunks = list(self._load_sources(plan.source))
        q = tokens(query)
        scored: list[RetrievedChunk] = []
        for chunk in chunks:
            c_tokens = tokens(chunk.text)
            if not c_tokens:
                continue
            overlap = len(q & c_tokens) / max(len(q), 1)
            score = overlap + float(chunk.metadata.get("public_weight", 0.0))
            if score > 0:
                scored.append(chunk.model_copy(update={"score": round(score, 4)}))
        scored.sort(key=lambda c: c.score, reverse=True)
        return scored[: plan.top_k]

    def _load_sources(self, source: str) -> Iterable[RetrievedChunk]:
        names = ["knowledge_base.json"]
        if source in {"memory", "hybrid"}:
            names.append("memory_store.json")
        if source == "hybrid":
            names.append("web_cache.json")
        for name in names:
            path = self.data_dir / name
            if not path.exists():
                continue
            payload = json.loads(path.read_text(encoding="utf-8"))
            for item in payload:
                yield RetrievedChunk(
                    text=item.get("text", ""),
                    source=item.get("source", name),
                    score=0.0,
                    metadata=item.get("metadata", {}),
                )
