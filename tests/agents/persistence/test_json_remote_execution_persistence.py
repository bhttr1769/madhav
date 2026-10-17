
import pytest

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


def make_record(
    status=RemoteExecutionStatus.CLAIMED,
    response=None,
    fingerprint="fingerprint-1",
    owner="node-b",
):
    return RemoteExecutionRecord(
        dispatch_id="dispatch-1",
        request_fingerprint=fingerprint,
        owner_node_id=owner,
        status=status,
        response=response,
    )


def make_response():
    return AgentMessage(
        id="response-1",
        sender_agent_id="agent-b",
        recipient_agent_id="agent-a",
        message_type=AgentMessageType.RESPONSE,
        payload={
            "kind": "remote_task_result",
            "dispatch_id": "dispatch-1",
            "status": "completed",
            "output": {"answer": 42},
            "error": None,
        },
        correlation_id="dispatch-1",
    )


def test_claim_is_created_only_once(tmp_path):
    persistence = JsonRemoteExecutionPersistence(tmp_path)
    record = make_record()

    assert persistence.claim(record) is True
    assert persistence.claim(record) is False
    assert persistence.load("dispatch-1") == record


def test_completed_response_survives_reload(tmp_path):
    persistence = JsonRemoteExecutionPersistence(tmp_path)
    persistence.claim(make_record())

    running = make_record(status=RemoteExecutionStatus.RUNNING)
    persistence.save(running)

    completed = make_record(
        status=RemoteExecutionStatus.COMPLETED,
        response=make_response(),
    )
    persistence.save(completed)

    restored = JsonRemoteExecutionPersistence(tmp_path).load("dispatch-1")
    assert restored == completed
    assert restored.response is not None
    assert restored.response.payload["output"] == {"answer": 42}


def test_dispatch_fingerprint_cannot_change(tmp_path):
    persistence = JsonRemoteExecutionPersistence(tmp_path)
    persistence.claim(make_record())

    with pytest.raises(ValueError, match="fingerprint"):
        persistence.save(
            make_record(
                status=RemoteExecutionStatus.RUNNING,
                fingerprint="different-fingerprint",
            )
        )


def test_owner_cannot_change_implicitly(tmp_path):
    persistence = JsonRemoteExecutionPersistence(tmp_path)
    persistence.claim(make_record())

    with pytest.raises(ValueError, match="owner cannot change"):
        persistence.save(
            make_record(
                status=RemoteExecutionStatus.RUNNING,
                owner="node-c",
            )
        )


def test_terminal_record_cannot_be_reopened(tmp_path):
    persistence = JsonRemoteExecutionPersistence(tmp_path)
    persistence.claim(make_record())
    persistence.save(make_record(status=RemoteExecutionStatus.RUNNING))
    persistence.save(
        make_record(
            status=RemoteExecutionStatus.COMPLETED,
            response=make_response(),
        )
    )

    with pytest.raises(ValueError, match="invalid remote execution transition"):
        persistence.save(
            make_record(status=RemoteExecutionStatus.RUNNING)
        )


def test_missing_record_raises_key_error(tmp_path):
    persistence = JsonRemoteExecutionPersistence(tmp_path)

    with pytest.raises(KeyError):
        persistence.load("missing-dispatch")
