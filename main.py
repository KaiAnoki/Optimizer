from __future__ import annotations

from fastapi import FastAPI

from app import AresOptimizer
from app.schemas import ChatResponse, UserRequest


app = FastAPI(
    title="ARES Optimizer",
    description="Deterministic task classification, retrieval, and model-routing API.",
    version="1.1.0",
)
optimizer = AresOptimizer()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "ares-optimizer"}


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return health()


@app.post("/route")
def route(request: UserRequest) -> dict:
    result = optimizer.handle(request)
    return {
        "trace_id": result.trace_id,
        "task": result.task.model_dump(),
        "retrieval": result.retrieval.model_dump(),
        "route": result.route.model_dump(),
        "agent_trace": [step.model_dump() for step in result.agent_trace],
    }


@app.post("/chat", response_model=ChatResponse)
def chat(request: UserRequest) -> ChatResponse:
    return optimizer.handle(request)
