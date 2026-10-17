
from types import SimpleNamespace
from unittest.mock import Mock

from brain.agents.agent_runtime import AgentRuntime
from brain.agents.agent_runtime_registry import AgentRuntimeRegistry
from brain.agents.communication.agent_message_router import AgentMessageRouter
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
from brain.agents.communication.remote_task_execution_handler import (
    RemoteTaskExecutionHandler,
)
from brain.agents.communication.remote_task_execution_receiver import (
    RemoteTaskExecutionReceiver,
)
from brain.agents.execution_node_registry import ExecutionNodeRegistry
from brain.agents.models.agent_identity import AgentIdentity
from brain.agents.models.agent_message import AgentMessage
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
from brain.organization.authority_evaluation_service import (
    AuthorityEvaluationService,
)
from brain.organization.models.membership_status import MembershipStatus
from brain.organization.models.organization import Organization
from brain.organization.models.organization_membership import (
    OrganizationMembership,
)
from brain.organization.models.organization_persistence_state import (
    OrganizationPersistenceState,
)
from brain.organization.models.organizational_role import OrganizationalRole
from brain.organization.models.organizational_unit import OrganizationalUnit


SECRET = b"x" * 32
ENDPOINT_A = "https://node-a.example"
ENDPOINT_B = "https://node-b.example"


class InProcessTransport(RemoteMessageTransport):
    """Route authenticated wire messages between in-process nodes."""

    def __init__(self):
        self.handlers = {}
        self.sent = []

    def register(self, endpoint, handler):
        self.handlers[endpoint] = handler

    def send(self, endpoint: str, wire_bytes: bytes) -> None:
        self.sent.append((endpoint, wire_bytes))

        handler = self.handlers.get(endpoint)
        if handler is None:
            raise ConnectionError(
                f"No receiver registered for endpoint: {endpoint}"
            )

        handler(wire_bytes)


class InMemoryOrganizationPersistence:
    """Provide an organization snapshot to the receiver's authority checks."""

    def __init__(self, state):
        self.state = state

    def load(self, organization_id: str) -> OrganizationPersistenceState:
        if organization_id != self.state.organization.id:
            raise KeyError(organization_id)
        return self.state


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
        operation=operation,
        goal=goal,
        workflow=workflow,
        step=step,
        task=task,
        capability_id="capability.calculate",
        input_payload={"number": 21},
    )


def make_organization_persistence():
    organization = Organization("org-1", "Integration Test Organization")
    unit = OrganizationalUnit("unit-1", "org-1", "Engineering")
    role = OrganizationalRole("role-1", "org-1", "Administrator")

    agent_a = AgentIdentity("agent-a", "Agent A")
    agent_b = AgentIdentity("agent-b", "Agent B")

    state = OrganizationPersistenceState(
        organization=organization,
        units=(unit,),
        agents=(agent_a, agent_b),
        roles=(role,),
        memberships=(
            OrganizationMembership(
                "membership-a",
                "org-1",
                "agent-a",
                "unit-1",
                "role-1",
                MembershipStatus.ACTIVE,
            ),
            OrganizationMembership(
                "membership-b",
                "org-1",
                "agent-b",
                "unit-1",
                "role-1",
                MembershipStatus.ACTIVE,
            ),
        ),
        reporting_relationships=(),
    )

    return InMemoryOrganizationPersistence(state)


def make_system():
    transport = InProcessTransport()

    sender_auth = RemoteMessageAuthenticator(
        local_node_id="node-a",
        peer_secrets={"node-b": SECRET},
        clock=lambda: 1_000,
    )

    receiver_auth = RemoteMessageAuthenticator(
        local_node_id="node-b",
        peer_secrets={"node-a": SECRET},
        clock=lambda: 1_000,
    )

    sender_registry = ExecutionNodeRegistry(
        (
            ExecutionNodeRegistration(
                identity=ExecutionNodeIdentity("node-b"),
                endpoint=ENDPOINT_B,
            ),
        )
    )

    receiver_registry = ExecutionNodeRegistry(
        (
            ExecutionNodeRegistration(
                identity=ExecutionNodeIdentity("node-a"),
                endpoint=ENDPOINT_A,
            ),
        )
    )

    sender_gateway = AuthenticatedRemoteMessageGateway(
        node_registry=sender_registry,
        authenticator=sender_auth,
        transport=transport,
    )

    receiver_gateway = AuthenticatedRemoteMessageGateway(
        node_registry=receiver_registry,
        authenticator=receiver_auth,
        transport=transport,
    )

    router = object.__new__(AgentMessageRouter)
    router._registry = SimpleNamespace(
        has=lambda agent_id: agent_id == "agent-b"
    )
    router._messages = {}

    runtime = object.__new__(AgentRuntime)
    runtime._state = SimpleNamespace(
        runtime_id="runtime-b",
        agent_id="agent-b",
    )
    runtime._organization_id = "org-1"
    runtime.execute_capability = Mock(return_value={"answer": 42})

    runtime_registry = object.__new__(AgentRuntimeRegistry)
    runtime_registry._runtimes = {"runtime-b": runtime}

    handler = RemoteTaskExecutionHandler()

    receiver = RemoteTaskExecutionReceiver(
        gateway=receiver_gateway,
        router=router,
        runtime_registry=runtime_registry,
        execution_handler=handler,
        organization_persistence=make_organization_persistence(),
        authority_evaluation_service=AuthorityEvaluationService(
            trusted_authorities={"org-1": "agent-a"}
        ),
        node_agent_bindings={"node-a": {"agent-a"}},
    )

    responses = []

    def receive_response(wire_bytes):
        responses.append(sender_auth.open(wire_bytes))

    transport.register(ENDPOINT_B, receiver.receive)
    transport.register(ENDPOINT_A, receive_response)

    dispatcher = RemoteTaskDispatcher(sender_gateway)

    return dispatcher, transport, responses, runtime, router


def test_dispatch_executes_remotely_and_correlates_result():
    dispatcher, transport, responses, runtime, router = make_system()
    request = make_dispatch()

    dispatched_message = dispatcher.dispatch(request)

    runtime.execute_capability.assert_called_once_with(
        "capability.calculate",
        {"number": 21},
        authority_agent_id="agent-a",
    )

    assert dispatched_message.correlation_id == request.dispatch_id
    assert len(responses) == 1

    result = RemoteTaskResult.from_message(responses[0], request)

    assert result.dispatch_id == request.dispatch_id
    assert result.task_id == request.task.id
    assert result.status == "completed"
    assert result.output == {"answer": 42}

    assert router.messages_for("agent-b") == (dispatched_message,)
    assert [endpoint for endpoint, _ in transport.sent] == [
        ENDPOINT_B,
        ENDPOINT_A,
    ]


def test_duplicate_dispatch_does_not_execute_capability_twice():
    dispatcher, _, responses, runtime, _ = make_system()
    request = make_dispatch()

    dispatcher.dispatch(request)
    dispatcher.dispatch(request)

    runtime.execute_capability.assert_called_once()
    assert len(responses) == 2

    first_result = RemoteTaskResult.from_message(responses[0], request)
    second_result = RemoteTaskResult.from_message(responses[1], request)

    assert first_result == second_result
    assert first_result.status == "completed"
    assert first_result.output == {"answer": 42}
