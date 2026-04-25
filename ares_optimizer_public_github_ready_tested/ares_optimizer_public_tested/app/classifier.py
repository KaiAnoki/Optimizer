from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable

from .schemas import TaskPrediction, TaskType


@dataclass(frozen=True)
class SignalRule:
    terms: Iterable[str]
    task: TaskType
    weight: float


# Public-safe routing signals. Production deployments can replace this with the
# private policy/scoring layer without changing the external API.
RULES = [
    SignalRule(("python", "code", "debug", "function", "script", "api"), TaskType.coding, 1.4),
    SignalRule(("remember", "memory", "saved", "what did i say", "my project"), TaskType.memory, 1.2),
    SignalRule(("search", "retrieve", "lookup", "find", "document", "docs"), TaskType.retrieval, 1.1),
    SignalRule(("plan", "strategy", "compare", "why", "how should", "architecture"), TaskType.reasoning, 1.0),
    SignalRule(("send", "schedule", "open", "create task", "delete", "run"), TaskType.tool_use, 1.3),
    SignalRule(("image", "photo", "picture", "screenshot", "vision"), TaskType.vision, 1.5),
]


class PublicTaskClassifier:
    """Public classifier interface for the A.R.E.S decision layer.

    This implementation is intentionally transparent but conservative. The
    closed/private implementation can use stronger learned policies while
    keeping this same contract.
    """

    def classify(self, text: str) -> TaskPrediction:
        lowered = text.lower()
        scores: Dict[TaskType, float] = {task: 0.05 for task in TaskType}

        for rule in RULES:
            for term in rule.terms:
                if term in lowered:
                    scores[rule.task] += rule.weight

        if len(text) > 180:
            scores[TaskType.reasoning] += 0.45
        if "?" in text and len(text.split()) > 8:
            scores[TaskType.reasoning] += 0.25

        best = max(scores, key=scores.get)
        total = sum(scores.values()) or 1.0
        confidence = min(0.97, max(0.51, scores[best] / total + 0.35))
        reason = f"Detected public-safe routing signals for {best.value}."
        return TaskPrediction(label=best, confidence=round(confidence, 3), public_reason=reason)
