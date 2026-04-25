from __future__ import annotations

import uuid

from .classifier import PublicTaskClassifier
from .model_router import ModelRouter
from .reranker import PublicReranker
from .responder import PublicResponder
from .retrieval_controller import RetrievalController
from .retriever import PublicRetriever
from .schemas import AgentStep, ChatResponse, UserRequest


class AresOptimizer:
    def __init__(self) -> None:
        self.classifier = PublicTaskClassifier()
        self.retrieval_controller = RetrievalController()
        self.retriever = PublicRetriever()
        self.reranker = PublicReranker()
        self.router = ModelRouter()
        self.responder = PublicResponder()

    def handle(self, request: UserRequest) -> ChatResponse:
        trace_id = request.metadata.get("trace_id") or str(uuid.uuid4())
        trace: list[AgentStep] = []

        task = self.classifier.classify(request.message)
        trace.append(AgentStep(name="classifier", status="ok", detail=task.label.value))

        retrieval_plan = self.retrieval_controller.plan(request.message, task)
        trace.append(AgentStep(name="retrieval_controller", status="ok", detail=retrieval_plan.source))

        context = self.retriever.retrieve(request.message, retrieval_plan)
        if retrieval_plan.rerank:
            context = self.reranker.rerank(context)
        trace.append(AgentStep(name="retrieval", status="ok", detail=f"{len(context)} chunks"))

        route = self.router.choose(request.message, task, context)
        trace.append(AgentStep(name="model_router", status="ok", detail=route.route.value))

        answer = self.responder.generate(request.message, task, route, context)
        trace.append(AgentStep(name="responder", status="ok", detail="public demo response generated"))

        return ChatResponse(
            answer=answer,
            task=task,
            retrieval=retrieval_plan,
            route=route,
            context_used=context,
            trace_id=trace_id,
            agent_trace=trace,
        )
