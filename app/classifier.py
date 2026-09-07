from __future__ import annotations

import re
from dataclasses import dataclass

from .schemas import TaskPrediction, TaskType


TOKEN_RE = re.compile(r"[a-z0-9_+#.-]+")


@dataclass(frozen=True, slots=True)
class SignalRule:
    terms: tuple[str, ...]
    task: TaskType
    weight: float


RULES = (
    SignalRule(("python", "code", "debug", "function", "script", "api"), TaskType.coding, 1.4),
    SignalRule(("remember", "memory", "saved", "what did i say", "my project"), TaskType.memory, 1.2),
    SignalRule(("search", "retrieve", "lookup", "find", "document", "docs"), TaskType.retrieval, 1.1),
    SignalRule(("plan", "strategy", "compare", "why", "how should", "architecture"), TaskType.reasoning, 1.0),
    SignalRule(("send", "schedule", "open", "create task", "delete", "run"), TaskType.tool_use, 1.3),
    SignalRule(("image", "photo", "picture", "screenshot", "vision"), TaskType.vision, 1.5),
)


class TaskClassifier:
    """Classify requests with a transparent, deterministic rule set."""

    def classify(self, text: str) -> TaskPrediction:
        normalized = " ".join(text.lower().split())
        tokens = set(TOKEN_RE.findall(normalized))
        scores: dict[TaskType, float] = {task: 0.05 for task in TaskType}

        for rule in RULES:
            matches = sum(
                1
                for term in rule.terms
                if (term in normalized if " " in term else term in tokens)
            )
            scores[rule.task] += matches * rule.weight

        if len(text) > 180:
            scores[TaskType.reasoning] += 0.45
        if "?" in text and len(text.split()) > 8:
            scores[TaskType.reasoning] += 0.25

        best = max(scores, key=scores.get)
        total = sum(scores.values()) or 1.0
        confidence = min(0.97, max(0.51, scores[best] / total + 0.35))
        return TaskPrediction(
            label=best,
            confidence=round(confidence, 3),
            reason=f"Matched deterministic routing signals for {best.value}.",
        )
