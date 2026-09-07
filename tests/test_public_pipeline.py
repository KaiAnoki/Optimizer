import json

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from app import AresOptimizer
from app.classifier import TaskClassifier
from app.retriever import Retriever
from app.schemas import RetrievalPlan, UserRequest
from main import app


def test_pipeline_returns_route_and_trace() -> None:
    response = AresOptimizer().handle(UserRequest(message="Explain the ARES optimizer architecture"))
    assert response.answer
    assert response.trace_id
    assert [step.name for step in response.agent_trace] == [
        "classifier", "retrieval_controller", "retrieval", "model_router", "responder"
    ]


def test_coding_routes_to_coding_model() -> None:
    response = AresOptimizer().handle(UserRequest(message="Write Python code for a router"))
    assert response.task.label.value == "coding"
    assert response.route.route.value == "coding_model"


def test_classifier_does_not_match_substrings() -> None:
    prediction = TaskClassifier().classify("List the capital cities")
    assert prediction.label.value == "chat"


def test_whitespace_message_is_rejected() -> None:
    with pytest.raises(ValidationError, match="message must contain text"):
        UserRequest(message="   ")


def test_retriever_uses_project_data_outside_repository_cwd(monkeypatch, tmp_path) -> None:
    monkeypatch.chdir(tmp_path)
    chunks = Retriever().retrieve(
        "optimizer architecture",
        RetrievalPlan(enabled=True, source="docs", top_k=3),
    )
    assert chunks


def test_retriever_skips_malformed_json(tmp_path) -> None:
    (tmp_path / "knowledge_base.json").write_text("not-json", encoding="utf-8")
    chunks = Retriever(tmp_path).retrieve(
        "anything",
        RetrievalPlan(enabled=True, source="docs", top_k=3),
    )
    assert chunks == []


def test_api_health_and_route() -> None:
    client = TestClient(app)
    assert client.get("/health").json() == {"status": "ok", "service": "ares-optimizer"}
    response = client.post("/route", json={"message": "Debug a Python API"})
    assert response.status_code == 200
    assert response.json()["route"]["route"] == "coding_model"


def test_cli_response_is_json_serializable() -> None:
    response = AresOptimizer().handle(UserRequest(message="Hello"))
    json.dumps(response.model_dump(mode="json"))
