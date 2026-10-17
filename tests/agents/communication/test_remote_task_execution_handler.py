
from threading import Event, Thread
from types import SimpleNamespace
from unittest.mock import Mock
from uuid import uuid4

import pytest

from brain.agents.agent_runtime import AgentRuntime
from brain.agents.communication.remote_task_execution_handler import (
    RemoteTaskExecutionHandler,
)
from brain.agents.models.agent_message import (
    AgentMessage,
    AgentMessageType,
)


def make_runtime():
    runtime = object.__new__(AgentRuntime)
    runtime._state = SimpleNamespace(agent_id="agent-b")
    runtime.execute_capability = Mock(return_value={"answer": 42})
    return runtime


def make_message(input_payload=None, dispatch_id="dispatch-1"):
    return AgentMessage(
        id=str(uuid4()),
        sender_agent_id="agent-a",
        recipient_agent_id="agent-b",
        message_type=AgentMessageType.REQUEST,
        correlation_id=dispatch_id,
        payload={
            "kind": "remote_task_dispatch",
            "dispatch_id": dispatch_id,
            "capability_id": "capability.calculate",
            "operation_id": "operation-1",
            "goal_id": "goal-1",
            "workflow_id": "workflow-1",
            "step_id": "step-1",
            "task_id": "task-1",
            "input_payload": input_payload or {"value": 6},
        },
    )


def test_executes_capability_and_returns_correlated_result():
    handler = RemoteTaskExecutionHandler()
    runtime = make_runtime()
    request = make_message()

    response = handler.handle(request, runtime)

    runtime.execute_capability.assert_called_once_with(
        "capability.calculate",
        {"value": 6},
    )
    assert response.message_type == AgentMessageType.RESPONSE
    assert response.correlation_id == request.correlation_id
    assert response.sender_agent_id == "agent-b"
    assert response.recipient_agent_id == "agent-a"
    assert response.payload["kind"] == "remote_task_result"
    assert response.payload["status"] == "completed"
    assert response.payload["output"] == {"answer": 42}


def test_duplicate_dispatch_reuses_cached_result():
    handler = RemoteTaskExecutionHandler()
    runtime = make_runtime()
    request = make_message()

    first = handler.handle(request, runtime)
    second = handler.handle(request, runtime)

    runtime.execute_capability.assert_called_once()
    assert second == first


def test_reusing_dispatch_id_with_different_payload_is_rejected():
    handler = RemoteTaskExecutionHandler()
    runtime = make_runtime()

    handler.handle(make_message({"value": 6}), runtime)

    with pytest.raises(ValueError, match="different request"):
        handler.handle(make_message({"value": 99}), runtime)

    runtime.execute_capability.assert_called_once()


def test_capability_failure_is_cached():
    handler = RemoteTaskExecutionHandler()
    runtime = make_runtime()
    runtime.execute_capability.side_effect = RuntimeError("capability failed")
    request = make_message()

    first = handler.handle(request, runtime)
    second = handler.handle(request, runtime)

    runtime.execute_capability.assert_called_once()
    assert first == second
    assert first.payload["status"] == "failed"
    assert "capability failed" in first.payload["error"]


def test_rejects_wrong_recipient():
    handler = RemoteTaskExecutionHandler()
    runtime = make_runtime()
    request = make_message()

    request = AgentMessage(
        id=request.id,
        sender_agent_id=request.sender_agent_id,
        recipient_agent_id="agent-other",
        message_type=request.message_type,
        payload=request.payload,
        correlation_id=request.correlation_id,
    )

    with pytest.raises(ValueError, match="recipient"):
        handler.handle(request, runtime)

    runtime.execute_capability.assert_not_called()


def test_concurrent_duplicate_executes_only_once():
    handler = RemoteTaskExecutionHandler()
    runtime = make_runtime()
    request = make_message()
    execution_started = Event()
    allow_execution_to_finish = Event()

    def slow_execution(capability_id, input_data):
        execution_started.set()
        assert allow_execution_to_finish.wait(timeout=5)
        return {"answer": 42}

    runtime.execute_capability.side_effect = slow_execution
    responses = []
    errors = []

    def run():
        try:
            responses.append(handler.handle(request, runtime))
        except Exception as exc:
            errors.append(exc)

    first_thread = Thread(target=run)
    second_thread = Thread(target=run)

    first_thread.start()
    assert execution_started.wait(timeout=5)
    second_thread.start()
    allow_execution_to_finish.set()

    first_thread.join(timeout=5)
    second_thread.join(timeout=5)

    assert not first_thread.is_alive()
    assert not second_thread.is_alive()
    assert not errors
    assert len(responses) == 2
    assert responses[0] == responses[1]
    runtime.execute_capability.assert_called_once()
