from __future__ import annotations

from .schemas import RetrievedChunk, RouteDecision, RouteType, TaskPrediction, TaskType


class ModelRouter:
    def choose(self, message: str, task: TaskPrediction, context: list[RetrievedChunk]) -> RouteDecision:
        complexity = min(1.0, len(message.split()) / 80)
        if task.label == TaskType.coding:
            return RouteDecision(route=RouteType.coding_model, confidence=0.91, public_reason="Code-oriented request.")
        if task.label == TaskType.tool_use:
            return RouteDecision(route=RouteType.tool_agent, confidence=0.88, public_reason="Action-oriented request.")
        if task.label == TaskType.vision:
            return RouteDecision(route=RouteType.vision_model, confidence=0.9, public_reason="Image/vision request.")
        if context or task.label in {TaskType.reasoning, TaskType.retrieval, TaskType.memory} or complexity > 0.55:
            return RouteDecision(route=RouteType.reasoning_model, confidence=0.86, public_reason="Context synthesis or multi-step reasoning required.")
        return RouteDecision(route=RouteType.fast_model, confidence=0.8, public_reason="Simple low-latency response path.")
