from __future__ import annotations

from fastapi import FastAPI

from app import AresOptimizer
from app.schemas import UserRequest

app = FastAPI(
    title="ARES Optimizer Public Showcase",
    description="Public-safe AI routing and retrieval optimizer for A.R.E.S.",
    version="1.0.0-public",
)
optimizer = AresOptimizer()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "ares-optimizer-public"}


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return health()


@app.post("/route")
def route(request: UserRequest):
    result = optimizer.handle(request)
    return {
        "trace_id": result.trace_id,
        "task": result.task.model_dump(),
        "retrieval": result.retrieval.model_dump(),
        "route": result.route.model_dump(),
        "agent_trace": [step.model_dump() for step in result.agent_trace],
    }


@app.post("/chat")
def chat(request: UserRequest):
    return optimizer.handle(request).model_dump()
