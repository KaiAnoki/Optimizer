from app import AresOptimizer
from app.schemas import UserRequest


def test_pipeline_returns_route_and_trace():
    response = AresOptimizer().handle(UserRequest(message="Explain the ARES optimizer architecture"))
    assert response.answer
    assert response.trace_id
    assert response.agent_trace
    assert response.route.route.value in {"fast_model", "reasoning_model", "coding_model", "tool_agent", "vision_model"}


def test_coding_routes_to_coding_model():
    response = AresOptimizer().handle(UserRequest(message="Write Python code for a router"))
    assert response.task.label.value == "coding"
    assert response.route.route.value == "coding_model"
