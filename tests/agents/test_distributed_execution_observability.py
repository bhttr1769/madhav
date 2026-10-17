from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from brain.agents.agent_runtime import AgentRuntime
from brain.agents.communication.authenticated_remote_message_gateway import (
    AuthenticatedRemoteMessageGateway,
)
from brain.agents.communication.remote_task_dispatcher import (
    RemoteTaskDispatcher,
)
from brain.agents.communication.remote_task_execution_handler import (
    RemoteTaskExecutionHandler,
)
from brain.agents.models.agent_message import (
    AgentMessage,
    AgentMessageType,
)
from brain.agents.models.agent_operation import (
    AgentOperation,
    AgentOperationStatus,
)
from brain.agents.models.agent_task import AgentTask
from brain.agents.models.agent_task_status import AgentTaskStatus
from brain.agents.models.goal import Goal
from brain.agents.models.goal_status import GoalStatus
from brain.agents.models.remote_execution_record import (
    RemoteExecutionRecord,
    RemoteExecutionStatus,
)
from brain.agents.models.remote_task_dispatch import RemoteTaskDispatch
from brain.agents.models.workflow import Workflow, WorkflowStatus
from brain.agents.models.workflow_step import (
    WorkflowStep,
    WorkflowStepStatus,
)
from brain.agents.persistence.json_remote_execution_persistence import (
    JsonRemoteExecutionPersistence,
)
from brain.agents.remote_execution_reconciliation_coordinator import (
    RemoteExecutionReconciliationCoordinator,
)
from brain.safety.logging.models.action_log_event import ActionLogEvent
from brain.safety.logging.models.action_log_status import ActionLogStatus
from brain.safety.logging.services.logging_service import LoggingService
from brain.safety.logging.stores.action_log_store import ActionLogStore


def make_logging_service():
    store = ActionLogStore()
    return LoggingService(store), store


class RecordingGateway(AuthenticatedRemoteMessageGateway):
    def __init__(self, error=None):
        self.error = error
        self.sent = []

    def send_to_node(self, message, recipient_node_id):
        if self.error is not None:
            raise self.error
        self.sent.append((message, recipient_node_id))


def make_dispatch():
    goal = Goal(
        id="goal-1",
        agent_id="agent-a",
        description="Complete assigned work",
        status=GoalStatus.ACTIVE,
    )
    task = AgentTask(
        id="task-1",
        goal_id=goal.id,
        description="Calculate a result",
        status=AgentTaskStatus.ACTIVE,
    )
    workflow = Workflow(
        id="workflow-1",
        goal_id=goal.id,
        step_ids=("step-1",),
        status=WorkflowStatus.RUNNING,
    )
    step = WorkflowStep(
        id="step-1",
        task_id=task.id,
        status=WorkflowStepStatus.RUNNING,
    )
    operation = AgentOperation(
        id="operation-1",
        goal_id=goal.id,
        workflow_id=workflow.id,
        status=AgentOperationStatus.RUNNING,
    )

    return RemoteTaskDispatch(
        dispatch_id="dispatch-1",
        sender_agent_id="agent-a",
        recipient_agent_id="agent-b",
        recipient_node_id="node-b",
        capability_id="capability.calculate",
        operation=operation,
        goal=goal,
        workflow=workflow,
        step=step,
        task=task,
        input_payload={"number": 21},
    )


def make_runtime():
    runtime = object.__new__(AgentRuntime)
    runtime._state = SimpleNamespace(agent_id="agent-b")
    runtime.execute_capability = Mock(return_value={"answer": 42})
    return runtime


def make_message():
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
            "input_payload": {"number": 21},
        },
    )


def test_dispatch_logs_attempt_and_successful_send():
    logging_service, store = make_logging_service()
    gateway = RecordingGateway()
    dispatcher = RemoteTaskDispatcher(gateway, logging_service)

    message = dispatcher.dispatch(make_dispatch())

    assert len(gateway.sent) == 1
    assert gateway.sent[0][0] == message
    assert [log.event for log in store.all()] == [
        ActionLogEvent.REQUESTED,
        ActionLogEvent.REQUESTED,
    ]
    assert [log.metadata["phase"] for log in store.all()] == [
        "dispatch_attempted",
        "dispatch_sent",
    ]
    assert all(
        log.metadata["dispatch_id"] == "dispatch-1"
        for log in store.all()
    )


def test_dispatch_logs_delivery_failure_and_propagates():
    logging_service, store = make_logging_service()
    dispatcher = RemoteTaskDispatcher(
        RecordingGateway(RuntimeError("transport unavailable")),
        logging_service,
    )

    with pytest.raises(RuntimeError, match="transport unavailable"):
        dispatcher.dispatch(make_dispatch())

    logs = store.all()
    assert [log.event for log in logs] == [
        ActionLogEvent.REQUESTED,
        ActionLogEvent.EXECUTION_FAILED,
    ]
    assert logs[-1].status is ActionLogStatus.FAILED
    assert logs[-1].metadata["error_type"] == "RuntimeError"
    assert "transport unavailable" not in str(logs[-1].metadata)


def test_execution_logs_start_and_completion_without_payloads():
    logging_service, store = make_logging_service()
    handler = RemoteTaskExecutionHandler(
        logging_service=logging_service,
    )

    response = handler.handle(make_message(), make_runtime())

    assert response.payload["status"] == "completed"
    logs = store.all()

    assert [log.event for log in logs] == [
        ActionLogEvent.EXECUTION_STARTED,
        ActionLogEvent.EXECUTION_COMPLETED,
    ]
    assert logs[0].status is ActionLogStatus.RUNNING
    assert logs[1].status is ActionLogStatus.COMPLETED

    for log in logs:
        assert log.metadata["dispatch_id"] == "dispatch-1"
        assert log.metadata["task_id"] == "task-1"
        assert "input_payload" not in log.metadata
        assert "output" not in log.metadata


def test_execution_logs_failure_without_exception_message():
    logging_service, store = make_logging_service()
    runtime = make_runtime()
    runtime.execute_capability.side_effect = RuntimeError(
        "sensitive failure detail"
    )
    handler = RemoteTaskExecutionHandler(
        logging_service=logging_service,
    )

    response = handler.handle(make_message(), runtime)

    assert response.payload["status"] == "failed"
    logs = store.all()

    assert [log.event for log in logs] == [
        ActionLogEvent.EXECUTION_STARTED,
        ActionLogEvent.EXECUTION_FAILED,
    ]
    assert logs[-1].metadata["outcome"] == "failed"
    assert logs[-1].metadata["error_type"] == "RuntimeError"
    assert "sensitive failure detail" not in str(logs[-1].metadata)


def test_duplicate_dispatch_logs_cached_result_reuse():
    logging_service, store = make_logging_service()
    runtime = make_runtime()
    handler = RemoteTaskExecutionHandler(
        logging_service=logging_service,
    )
    message = make_message()

    first = handler.handle(message, runtime)
    second = handler.handle(message, runtime)

    runtime.execute_capability.assert_called_once()
    assert first == second

    logs = store.all()
    assert len(logs) == 3
    assert logs[-1].metadata["phase"] == "result_reuse"
    assert logs[-1].metadata["outcome"] == "cached_result_reused"


def test_reconciliation_logs_uncertain_transition(tmp_path):
    logging_service, store = make_logging_service()
    persistence = JsonRemoteExecutionPersistence(tmp_path)

    record = RemoteExecutionRecord(
        dispatch_id="dispatch-1",
        request_fingerprint="fingerprint-1",
        owner_node_id="node-b",
        status=RemoteExecutionStatus.CLAIMED,
    )
    assert persistence.claim(record)

    coordinator = RemoteExecutionReconciliationCoordinator(
        persistence,
        logging_service,
    )

    reconciled = coordinator.reconcile_incomplete()

    assert len(reconciled) == 1
    assert reconciled[0].status is RemoteExecutionStatus.UNCERTAIN

    logs = store.all()
    assert len(logs) == 1
    assert logs[0].event is ActionLogEvent.EXECUTION_FAILED
    assert logs[0].metadata["phase"] == "reconciliation"
    assert logs[0].metadata["outcome"] == "uncertain"
    assert logs[0].metadata["dispatch_id"] == "dispatch-1"