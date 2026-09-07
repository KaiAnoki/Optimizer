from __future__ import annotations

from .schemas import RetrievalPlan, TaskPrediction, TaskType


class RetrievalController:
    def plan(self, message: str, task: TaskPrediction) -> RetrievalPlan:
        lowered = message.lower()
        if task.label == TaskType.memory:
            return RetrievalPlan(enabled=True, source="memory", top_k=4, query_rewrite=True, rerank=True)
        if task.label == TaskType.retrieval:
            source = "hybrid" if any(x in lowered for x in ("project", "ares", "optimizer")) else "docs"
            return RetrievalPlan(enabled=True, source=source, top_k=5, query_rewrite=True, rerank=True)
        if task.label in (TaskType.reasoning, TaskType.coding) and any(x in lowered for x in ("ares", "optimizer", "architecture")):
            return RetrievalPlan(enabled=True, source="hybrid", top_k=3, query_rewrite=False, rerank=True)
        return RetrievalPlan(enabled=False)
