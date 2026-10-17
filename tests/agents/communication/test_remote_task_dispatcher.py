import pytest

from brain.agents.communication.authenticated_remote_message_gateway import (
    AuthenticatedRemoteMessageGateway,
)
from brain.agents.communication.remote_message_authenticator import (
    RemoteMessageAuthenticator,
)
from brain.agents.communication.remote_message_transport import (
    RemoteMessageTransport,
)
from brain.agents.communication.remote_task_dispatcher import (
    RemoteTaskDispatcher,
)
from brain.agents.execution_node_registry import ExecutionNodeRegistry
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
from brain.agents.models.execution_node_identity import ExecutionNodeIdentity
from brain.agents.models.execution_node_registration import (
    ExecutionNodeRegistration,
)
from brain.agents.models.goal import Goal
from brain.agents.models.goal_status import GoalStatus
from brain.agents.models.remote_task_dispatch import RemoteTaskDispatch
from brain.agents.models.remote_task_result import RemoteTaskResult
from brain.agents.models.workflow import Workflow, WorkflowStatus
from brain.agents.models.workflow_step import (
    WorkflowStep,
    WorkflowStepStatus,
)


SECRET = b"x" * 32


class RecordingTransport(RemoteMessageTransport):
    def __init__(self) -> None:
        self.sent: list[tuple[str, bytes]] = []

    def send(self, endpoint: str, wire_bytes: bytes) -> None:
        self.sent.append((endpoint, wire_bytes))


def make_dispatch() -> RemoteTaskDispatch:
    goal = Goal(
        id="goal-1",
        agent_id="agent-a",
        description="Complete the assigned work",
        status=GoalStatus.ACTIVE,
    )

    task = AgentTask(
        id="task-1",
        goal_id=goal.id,
        description="Calculate the requested result",
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


def make_dispatcher():
    registry = ExecutionNodeRegistry(
        (
            ExecutionNodeRegistration(
                identity=ExecutionNodeIdentity("node-b"),
                endpoint="https://node-b.example",
            ),
        )
    )

    sender_authenticator = RemoteMessageAuthenticator(
        local_node_id="node-a",
        peer_secrets={"node-b": SECRET},
        clock=lambda: 1_000,
    )

    transport = RecordingTransport()

    gateway = AuthenticatedRemoteMessageGateway(
        node_registry=registry,
        authenticator=sender_authenticator,
        transport=transport,
    )

    return RemoteTaskDispatcher(gateway), transport


def make_result_message(
    dispatch: RemoteTaskDispatch,
) -> AgentMessage:
    return RemoteTaskResult(
        dispatch_id=dispatch.dispatch_id,
        task_id=dispatch.task.id,
        goal_id=dispatch.goal.id,
        workflow_id=dispatch.workflow.id,
        workflow_step_id=dispatch.step.id,
        operation_id=dispatch.operation.id,
        sender_agent_id=dispatch.recipient_agent_id,
        recipient_agent_id=dispatch.sender_agent_id,
        status="completed",
        output={"answer": 42},
    ).to_message()


def test_dispatch_sends_authenticated_request_to_registered_node() -> None:
    dispatcher, transport = make_dispatcher()
    request = make_dispatch()

    message = dispatcher.dispatch(request)

    assert message.message_type is AgentMessageType.REQUEST
    assert message.correlation_id == request.dispatch_id
    assert message.payload["kind"] == "remote_task_dispatch"
    assert message.payload["task_id"] == request.task.id
    assert message.payload["operation_id"] == request.operation.id
    assert message.payload["capability_id"] == request.capability_id

    assert len(transport.sent) == 1
    endpoint, wire_bytes = transport.sent[0]
    assert endpoint == "https://node-b.example"

    receiver = RemoteMessageAuthenticator(
        local_node_id="node-b",
        peer_secrets={"node-a": SECRET},
        clock=lambda: 1_000,
    )
    assert receiver.open(wire_bytes) == message


def test_dispatch_rejects_wrong_request_type() -> None:
    dispatcher, _ = make_dispatcher()

    with pytest.raises(TypeError, match="RemoteTaskDispatch"):
        dispatcher.dispatch("invalid")


def test_dispatch_rejects_task_that_is_not_active() -> None:
    request = make_dispatch()

    inactive_task = AgentTask(
        id=request.task.id,
        goal_id=request.goal.id,
        description=request.task.description,
        status=AgentTaskStatus.CREATED,
    )

    with pytest.raises(ValueError, match="task must be ACTIVE"):
        RemoteTaskDispatch(
            dispatch_id="dispatch-2",
            sender_agent_id="agent-a",
            recipient_agent_id="agent-b",
            recipient_node_id="node-b",
            capability_id="capability.calculate",
            operation=request.operation,
            goal=request.goal,
            workflow=request.workflow,
            step=request.step,
            task=inactive_task,
            input_payload={"number": 21},
        )


def test_correlates_matching_response() -> None:
    request = make_dispatch()
    response = make_result_message(request)

    result = RemoteTaskDispatcher.correlate_result(request, response)

    assert result.dispatch_id == request.dispatch_id
    assert result.task_id == request.task.id
    assert result.status == "completed"
    assert result.output == {"answer": 42}


def test_rejects_wrong_correlation_id() -> None:
    request = make_dispatch()
    original = make_result_message(request)

    response = AgentMessage(
        id=original.id,
        sender_agent_id=original.sender_agent_id,
        recipient_agent_id=original.recipient_agent_id,
        message_type=original.message_type,
        payload=original.payload,
        correlation_id="another-dispatch",
    )

    with pytest.raises(ValueError, match="correlation ID"):
        RemoteTaskDispatcher.correlate_result(request, response)


def test_rejects_response_from_wrong_agent() -> None:
    request = make_dispatch()
    original = make_result_message(request)

    response = AgentMessage(
        id=original.id,
        sender_agent_id="unexpected-agent",
        recipient_agent_id=original.recipient_agent_id,
        message_type=original.message_type,
        payload=original.payload,
        correlation_id=original.correlation_id,
    )

    with pytest.raises(ValueError, match="sender"):
        RemoteTaskDispatcher.correlate_result(request, response)


def test_rejects_result_for_another_task() -> None:
    request = make_dispatch()
    original = make_result_message(request)
    payload = dict(original.payload)
    payload["task_id"] = "another-task"

    response = AgentMessage(
        id=original.id,
        sender_agent_id=original.sender_agent_id,
        recipient_agent_id=original.recipient_agent_id,
        message_type=AgentMessageType.RESPONSE,
        payload=payload,
        correlation_id=original.correlation_id,
    )

    with pytest.raises(ValueError, match="task_id"):
        RemoteTaskDispatcher.correlate_result(request, response)


def test_rejects_non_response_message() -> None:
    request = make_dispatch()
    response = make_result_message(request)

    information = AgentMessage(
        id=response.id,
        sender_agent_id=response.sender_agent_id,
        recipient_agent_id=response.recipient_agent_id,
        message_type=AgentMessageType.INFORMATION,
        payload=response.payload,
        correlation_id=response.correlation_id,
    )

    with pytest.raises(ValueError, match="RESPONSE"):
        RemoteTaskDispatcher.correlate_result(request, information)


def test_rejects_failed_result_without_error() -> None:
    with pytest.raises(ValueError, match="non-empty error"):
        RemoteTaskResult(
            dispatch_id="dispatch-1",
            task_id="task-1",
            goal_id="goal-1",
            workflow_id="workflow-1",
            workflow_step_id="step-1",
            operation_id="operation-1",
            sender_agent_id="agent-b",
            recipient_agent_id="agent-a",
            status="failed",
        )