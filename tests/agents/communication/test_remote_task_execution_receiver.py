
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
from brain.agents.communication.remote_task_execution_handler import (
    RemoteTaskExecutionHandler,
)
from brain.agents.communication.remote_task_execution_receiver import (
    RemoteTaskExecutionReceiver,
)
from brain.agents.execution_node_registry import ExecutionNodeRegistry
from brain.agents.models.agent_message import (
    AgentMessage,
    AgentMessageType,
)
from brain.agents.models.execution_node_identity import ExecutionNodeIdentity
from brain.agents.models.execution_node_registration import (
    ExecutionNodeRegistration,
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


SECRET = b"x" * 32


class RecordingTransport(RemoteMessageTransport):
    def __init__(self):
        self.sent = []

    def send(self, endpoint: str, wire_bytes: bytes) -> None:
        self.sent.append((endpoint, wire_bytes))


def make_receiver():
    receiver_auth = RemoteMessageAuthenticator(
        local_node_id="node-b",
        peer_secrets={"node-a": SECRET},
        clock=lambda: 1_000,
    )

    sender_auth = RemoteMessageAuthenticator(
        local_node_id="node-a",
        peer_secrets={"node-b": SECRET},
        clock=lambda: 1_000,
    )

    transport = RecordingTransport()
    node_registry = ExecutionNodeRegistry(
        (
            ExecutionNodeRegistration(
                identity=ExecutionNodeIdentity("node-a"),
                endpoint="https://node-a.example",
            ),
        )
    )

    gateway = AuthenticatedRemoteMessageGateway(
        node_registry=node_registry,
        authenticator=receiver_auth,
        transport=transport,
    )

    # The router needs only to confirm that the recipient agent exists.
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
    runtime.execute_capability = Mock(return_value={"answer": 42})

    runtime_registry = object.__new__(AgentRuntimeRegistry)
    runtime_registry._runtimes = {"runtime-b": runtime}

    runtime._organization_id = "org-1"

    organization_state = OrganizationPersistenceState(
        organization=Organization(
            id="org-1",
            name="Test Organization",
        ),
        units=(),
        agents=(),
        roles=(),
        memberships=(
            OrganizationMembership(
                id="membership-a",
                organization_id="org-1",
                agent_id="agent-a",
                organizational_unit_id="unit-1",
                role_id="role-1",
                status=MembershipStatus.ACTIVE,
            ),
        ),
        reporting_relationships=(),
        delegations=(),
    )

    organization_persistence = SimpleNamespace(
        load=lambda organization_id: organization_state
        if organization_id == "org-1"
        else (_ for _ in ()).throw(KeyError(organization_id))
    )

    authority_evaluation_service = AuthorityEvaluationService(
        trusted_authorities={"org-1": "agent-a"},
    )

    handler = RemoteTaskExecutionHandler()
    receiver = RemoteTaskExecutionReceiver(
        gateway=gateway,
        router=router,
        runtime_registry=runtime_registry,
        execution_handler=handler,
        organization_persistence=organization_persistence,
        authority_evaluation_service=authority_evaluation_service,
        node_agent_bindings={
            "node-a": {"agent-a"},
        },
    )

    return receiver, sender_auth, transport, router, runtime


def make_request():
    return AgentMessage(
        id="message-1",
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


def test_authenticated_request_executes_and_returns_remote_result():
    receiver, sender_auth, transport, router, runtime = make_receiver()
    request = make_request()
    wire_bytes = sender_auth.seal(request, "node-b")

    response = receiver.receive(wire_bytes)

    runtime.execute_capability.assert_called_once_with(
        "capability.calculate",
        {"number": 21},
        authority_agent_id="agent-a",
    )
    assert router.messages_for("agent-b") == (request,)
    assert response is not None
    assert response.message_type == AgentMessageType.RESPONSE
    assert response.correlation_id == "dispatch-1"
    assert response.payload["kind"] == "remote_task_result"
    assert response.payload["workflow_step_id"] == "step-1"
    assert response.payload["status"] == "completed"

    assert len(transport.sent) == 1
    endpoint, response_wire = transport.sent[0]
    assert endpoint == "https://node-a.example"
    assert sender_auth.open(response_wire) == response



def test_duplicate_request_does_not_execute_capability_twice():
    receiver, sender_auth, transport, _, runtime = make_receiver()
    request = make_request()

    # Each delivery gets a fresh authentication nonce, but the logical
    # dispatch ID remains unchanged so execution idempotency can apply.
    first_wire = sender_auth.seal(request, "node-b")
    second_wire = sender_auth.seal(request, "node-b")

    first = receiver.receive(first_wire)
    second = receiver.receive(second_wire)

    runtime.execute_capability.assert_called_once()
    assert first is not None
    assert second is not None
    assert second.payload == first.payload
    assert len(transport.sent) == 2


def test_ambiguous_runtime_selection_is_rejected():
    receiver, sender_auth, _, _, runtime = make_receiver()

    second_runtime = object.__new__(AgentRuntime)
    second_runtime._state = SimpleNamespace(
        runtime_id="runtime-b-2",
        agent_id="agent-b",
    )
    second_runtime.execute_capability = Mock()

    receiver._runtime_registry._runtimes["runtime-b-2"] = second_runtime
    wire_bytes = sender_auth.seal(make_request(), "node-b")

    try:
        receiver.receive(wire_bytes)
    except ValueError as exc:
        assert "multiple runtimes" in str(exc)
    else:
        raise AssertionError("ambiguous runtime selection was accepted")

    runtime.execute_capability.assert_not_called()
    second_runtime.execute_capability.assert_not_called()


def test_unbound_sender_node_is_denied():
    receiver, sender_auth, _, _, runtime = make_receiver()
    receiver._node_agent_bindings = {
        "node-a": frozenset({"different-agent"}),
    }

    wire_bytes = sender_auth.seal(make_request(), "node-b")

    try:
        receiver.receive(wire_bytes)
    except PermissionError:
        pass
    else:
        raise AssertionError("Unbound sender was accepted")

    runtime.execute_capability.assert_not_called()


def test_missing_organization_state_is_denied():
    receiver, sender_auth, _, _, runtime = make_receiver()

    def missing_organization(_organization_id):
        raise KeyError("org-1")

    receiver._organization_persistence.load = missing_organization
    wire_bytes = sender_auth.seal(make_request(), "node-b")

    try:
        receiver.receive(wire_bytes)
    except PermissionError:
        pass
    else:
        raise AssertionError("Missing organization state was accepted")

    runtime.execute_capability.assert_not_called()


def test_agent_without_active_membership_is_denied():
    receiver, sender_auth, _, _, runtime = make_receiver()
    receiver._node_agent_bindings = {
        "node-a": frozenset({"agent-c"}),
    }

    request = make_request()
    unauthorized_request = AgentMessage(
        id=request.id,
        sender_agent_id="agent-c",
        recipient_agent_id=request.recipient_agent_id,
        message_type=request.message_type,
        correlation_id=request.correlation_id,
        payload=request.payload,
    )

    wire_bytes = sender_auth.seal(unauthorized_request, "node-b")

    try:
        receiver.receive(wire_bytes)
    except PermissionError:
        pass
    else:
        raise AssertionError("Agent without active membership was accepted")

    runtime.execute_capability.assert_not_called()

