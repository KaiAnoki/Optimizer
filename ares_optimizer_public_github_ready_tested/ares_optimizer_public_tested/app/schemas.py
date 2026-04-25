from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class TaskType(str, Enum):
    chat = "chat"
    retrieval = "retrieval"
    reasoning = "reasoning"
    coding = "coding"
    memory = "memory"
    tool_use = "tool_use"
    vision = "vision"


class RouteType(str, Enum):
    fast_model = "fast_model"
    reasoning_model = "reasoning_model"
    coding_model = "coding_model"
    tool_agent = "tool_agent"
    vision_model = "vision_model"


class UserRequest(BaseModel):
    message: str = Field(..., min_length=1)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class TaskPrediction(BaseModel):
    label: TaskType
    confidence: float = Field(ge=0.0, le=1.0)
    public_reason: str


class RetrievalPlan(BaseModel):
    enabled: bool
    source: str = "none"
    top_k: int = 0
    query_rewrite: bool = False
    rerank: bool = False


class RetrievedChunk(BaseModel):
    text: str
    source: str
    score: float
    metadata: Dict[str, Any] = Field(default_factory=dict)


class RouteDecision(BaseModel):
    route: RouteType
    confidence: float = Field(ge=0.0, le=1.0)
    public_reason: str


class AgentStep(BaseModel):
    name: str
    status: str
    detail: str


class ChatResponse(BaseModel):
    answer: str
    task: TaskPrediction
    retrieval: RetrievalPlan
    route: RouteDecision
    context_used: List[RetrievedChunk] = Field(default_factory=list)
    trace_id: str
    agent_trace: List[AgentStep] = Field(default_factory=list)
    public_note: str = "Public showcase build: proprietary ranking and optimization internals are intentionally abstracted."
