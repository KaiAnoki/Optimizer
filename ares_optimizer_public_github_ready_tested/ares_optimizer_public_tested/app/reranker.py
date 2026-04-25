from __future__ import annotations

from typing import List

from .schemas import RetrievedChunk


class PublicReranker:
    """Public-safe reranker.

    The production reranking strategy is abstracted. This demonstrator keeps the
    behavior deterministic and easy to inspect for reviewers.
    """

    def rerank(self, chunks: List[RetrievedChunk]) -> List[RetrievedChunk]:
        deduped: dict[str, RetrievedChunk] = {}
        for chunk in chunks:
            key = chunk.text.strip().lower()[:120]
            if key not in deduped or chunk.score > deduped[key].score:
                deduped[key] = chunk
        return sorted(deduped.values(), key=lambda c: c.score, reverse=True)
