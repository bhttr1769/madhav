
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
from brain.agents.remote_execution_reconciliation_coordinator import (
    RemoteExecutionReconciliationCoordinator,
)


def make_record(dispatch_id, status):
    return RemoteExecutionRecord(
        dispatch_id=dispatch_id,
        request_fingerprint=f"fingerprint-{dispatch_id}",
        owner_node_id="node-b",
        status=status,
    )


def test_reconciles_only_incomplete_dispatches(tmp_path):
    persistence = JsonRemoteExecutionPersistence(tmp_path)

    claimed = make_record(
        "dispatch-claimed",
        RemoteExecutionStatus.CLAIMED,
    )
    running = make_record(
        "dispatch-running",
        RemoteExecutionStatus.CLAIMED,
    )
    completed = make_record(
        "dispatch-completed",
        RemoteExecutionStatus.CLAIMED,
    )

    assert persistence.claim(claimed)
    assert persistence.claim(running)
    assert persistence.claim(completed)

    persistence.save(
        make_record("dispatch-running", RemoteExecutionStatus.RUNNING)
    )
    persistence.save(
        make_record("dispatch-completed", RemoteExecutionStatus.RUNNING)
    )

    response = AgentMessage(
        id="response-1",
        sender_agent_id="agent-b",
        recipient_agent_id="agent-a",
        message_type=AgentMessageType.RESPONSE,
        payload={"kind": "remote_task_result", "status": "completed"},
        correlation_id="dispatch-completed",
    )

    persistence.save(
        RemoteExecutionRecord(
            dispatch_id="dispatch-completed",
            request_fingerprint="fingerprint-dispatch-completed",
            owner_node_id="node-b",
            status=RemoteExecutionStatus.COMPLETED,
            response=response,
        )
    )

    coordinator = RemoteExecutionReconciliationCoordinator(persistence)
    reconciled = coordinator.reconcile_incomplete()

    assert {record.dispatch_id for record in reconciled} == {
        "dispatch-claimed",
        "dispatch-running",
    }
    assert all(
        record.status is RemoteExecutionStatus.UNCERTAIN
        for record in reconciled
    )
    assert (
        persistence.load("dispatch-completed").status
        is RemoteExecutionStatus.COMPLETED
    )


def test_reconciliation_is_idempotent(tmp_path):
    persistence = JsonRemoteExecutionPersistence(tmp_path)
    persistence.claim(
        make_record("dispatch-1", RemoteExecutionStatus.CLAIMED)
    )

    coordinator = RemoteExecutionReconciliationCoordinator(persistence)

    first = coordinator.reconcile_incomplete()
    second = coordinator.reconcile_incomplete()

    assert len(first) == 1
    assert first[0].status is RemoteExecutionStatus.UNCERTAIN
    assert second == ()
