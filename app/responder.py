from __future__ import annotations

from .schemas import RetrievedChunk, RouteDecision, TaskPrediction


class Responder:
    """Format the routing decision for inspection by an API or CLI client."""

    def generate(
        self,
        message: str,
        task: TaskPrediction,
        route: RouteDecision,
        context: list[RetrievedChunk],
    ) -> str:
        if context:
            sources = ", ".join(dict.fromkeys(chunk.source for chunk in context[:3]))
            return (
                f"Classified as {task.label.value} and selected {route.route.value}. "
                f"Retrieved {len(context)} context chunks from {sources}."
            )
        return f"Classified as {task.label.value} and selected {route.route.value}."
