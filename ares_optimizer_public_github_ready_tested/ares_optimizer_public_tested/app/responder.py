from __future__ import annotations

from .schemas import RetrievedChunk, RouteDecision, TaskPrediction


class PublicResponder:
    def generate(self, message: str, task: TaskPrediction, route: RouteDecision, context: list[RetrievedChunk]) -> str:
        if context:
            bullets = "\n".join(f"- {c.text}" for c in context[:3])
            return (
                f"ARES Optimizer routed this request to `{route.route.value}`.\n\n"
                f"Relevant context selected:\n{bullets}\n\n"
                "In production, this payload is forwarded to the configured A.R.E.S backend or local LLM."
            )
        return (
            f"ARES Optimizer classified this as `{task.label.value}` and routed it to `{route.route.value}`. "
            "This public build demonstrates the orchestration layer while preserving private optimizer internals."
        )
