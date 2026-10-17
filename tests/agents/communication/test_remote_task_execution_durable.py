
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from brain.agents.agent_runtime import AgentRuntime
from brain.agents.communication.remote_task_execution_handler import (
    RemoteExecutionUncertainError,
    RemoteTaskExecutionHandler,
)
from brain.agents.models.agent_message import (
    AgentMessage,
    AgentMessageType,
)
from brain.agents.models.remote_execution_record import (
    RemoteExecutionRecord,
    RemoteExecutionStatus,
)
from brain.agents.persistence.json_remote_execution_persistence import (
    JsonRemoteExecutionPersistence,
)
from brain.agents.communication.remote_task_execution_handler import (
    RemoteTaskExecutionHandler,
)
from brain.agents.persistence.json_remote_execution_persistence import (
    JsonRemoteExecutionPersistence,
)

execution_persistence = JsonRemoteExecutionPersistence(
    "data/remote_execution"
)

execution_handler = RemoteTaskExecutionHandler(
    persistence=execution_persistence,
    owner_node_id="node-b",  # Replace with this node's configured ID.
)

def make_runtime():
    runtime = object.__new__(AgentRuntime)
    runtime._state = SimpleNamespace(agent_id="agent-b")
    runtime.execute_capability = Mock(return_value={"answer": 42})
    return runtime


def make_message(input_payload=None):
    return AgentMessage(
        id="request-1",
        sender_agent_id="agent-a",
        recipient_agent_id="agent-b",
        message_type=AgentMessageType.REQUEST,
        correlation_id="dispatch-1",
        payload={
            "kind": "remote_task_dispatch",
            "dispatch_id": "dispatch-1",
            "capability_id": "capability.calculate",
            "operation_id": "operation-1",
            "goal_id": "goal-1",
            "workflow_id": "workflow-1",
            "step_id": "step-1",
            "task_id": "task-1",
            "input_payload": (
                {"number": 21}
                if input_payload is None
                else input_payload
            ),
        },
    )


def test_completed_result_is_reused_after_handler_restart(tmp_path):
    persistence = JsonRemoteExecutionPersistence(tmp_path)
    first_runtime = make_runtime()

    first_handler = RemoteTaskExecutionHandler(
        persistence=persistence,
        owner_node_id="node-b",
    )
    first_response = first_handler.handle(make_message(), first_runtime)

    second_runtime = make_runtime()
    second_handler = RemoteTaskExecutionHandler(
        persistence=JsonRemoteExecutionPersistence(tmp_path),
        owner_node_id="node-b",
    )
    second_response = second_handler.handle(make_message(), second_runtime)

    first_runtime.execute_capability.assert_called_once()
    second_runtime.execute_capability.assert_not_called()
    assert second_response == first_response


def test_existing_running_dispatch_is_not_reexecuted(tmp_path):
    persistence = JsonRemoteExecutionPersistence(tmp_path)
    message = make_message()

    fingerprint = RemoteTaskExecutionHandler._fingerprint(message)
    persistence.claim(
        RemoteExecutionRecord(
            dispatch_id="dispatch-1",
            request_fingerprint=fingerprint,
            owner_node_id="node-b",
            status=RemoteExecutionStatus.CLAIMED,
        )
    )
    persistence.save(
        RemoteExecutionRecord(
            dispatch_id="dispatch-1",
            request_fingerprint=fingerprint,
            owner_node_id="node-b",
            status=RemoteExecutionStatus.RUNNING,
        )
    )

    runtime = make_runtime()
    handler = RemoteTaskExecutionHandler(
        persistence=persistence,
        owner_node_id="node-b",
    )

    with pytest.raises(RemoteExecutionUncertainError):
        handler.handle(message, runtime)

    runtime.execute_capability.assert_not_called()


def test_completed_dispatch_rejects_conflicting_payload(tmp_path):
    persistence = JsonRemoteExecutionPersistence(tmp_path)
    runtime = make_runtime()
    handler = RemoteTaskExecutionHandler(
        persistence=persistence,
        owner_node_id="node-b",
    )

    handler.handle(make_message(), runtime)

    conflicting = make_message({"number": 999})
    with pytest.raises(ValueError, match="different request"):
        RemoteTaskExecutionHandler(
            persistence=JsonRemoteExecutionPersistence(tmp_path),
            owner_node_id="node-b",
        ).handle(conflicting, make_runtime())

    runtime.execute_capability.assert_called_once()
