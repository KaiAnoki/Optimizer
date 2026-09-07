from __future__ import annotations

import json
import re
from collections.abc import Iterable
from pathlib import Path

from .schemas import RetrievedChunk, RetrievalPlan


TOKEN_RE = re.compile(r"[a-zA-Z0-9_]+")
DEFAULT_DATA_DIR = Path(__file__).resolve().parents[1] / "data"


def tokens(text: str) -> set[str]:
    return set(TOKEN_RE.findall(text.lower()))


class Retriever:
    def __init__(self, data_dir: str | Path = DEFAULT_DATA_DIR) -> None:
        self.data_dir = Path(data_dir)

    def retrieve(self, query: str, plan: RetrievalPlan) -> list[RetrievedChunk]:
        if not plan.enabled:
            return []
        chunks = list(self._load_sources(plan.source))
        query_tokens = tokens(query)
        scored: list[RetrievedChunk] = []
        for chunk in chunks:
            chunk_tokens = tokens(chunk.text)
            if not chunk_tokens:
                continue
            overlap = len(query_tokens & chunk_tokens) / max(len(query_tokens), 1)
            configured_weight = chunk.metadata.get("weight", chunk.metadata.get("public_weight", 0.0))
            score = overlap + float(configured_weight)
            if score > 0:
                scored.append(chunk.model_copy(update={"score": round(score, 4)}))
        scored.sort(key=lambda chunk: chunk.score, reverse=True)
        return scored[:plan.top_k]

    def _load_sources(self, source: str) -> Iterable[RetrievedChunk]:
        names = ["knowledge_base.json"]
        if source in {"memory", "hybrid"}:
            names.append("memory_store.json")
        if source == "hybrid":
            names.append("web_cache.json")

        for name in names:
            path = self.data_dir / name
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
            except (FileNotFoundError, OSError, json.JSONDecodeError):
                continue
            if not isinstance(payload, list):
                continue
            for item in payload:
                if not isinstance(item, dict) or not isinstance(item.get("text"), str):
                    continue
                yield RetrievedChunk(
                    text=item["text"],
                    source=str(item.get("source", name)),
                    score=0.0,
                    metadata=item.get("metadata", {}) if isinstance(item.get("metadata", {}), dict) else {},
                )
