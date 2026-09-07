from __future__ import annotations

from .schemas import RetrievedChunk


class Reranker:
    """Remove duplicate chunks and preserve descending retrieval score."""

    def rerank(self, chunks: list[RetrievedChunk]) -> list[RetrievedChunk]:
        deduplicated: dict[str, RetrievedChunk] = {}
        for chunk in chunks:
            key = " ".join(chunk.text.lower().split())
            if key not in deduplicated or chunk.score > deduplicated[key].score:
                deduplicated[key] = chunk
        return sorted(deduplicated.values(), key=lambda chunk: chunk.score, reverse=True)
