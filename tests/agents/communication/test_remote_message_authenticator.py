
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
from brain.agents.execution_node_registry import ExecutionNodeRegistry
from brain.agents.models.agent_message import AgentMessage, AgentMessageType
from brain.agents.models.execution_node_identity import ExecutionNodeIdentity
from brain.agents.models.execution_node_registration import (
    ExecutionNodeRegistration,
)


SECRET = b"x" * 32


def make_message() -> AgentMessage:
    return AgentMessage(
        id="message-1",
        sender_agent_id="agent-a",
        recipient_agent_id="agent-b",
        message_type=AgentMessageType.INFORMATION,
        payload={"value": "original"},
        correlation_id="correlation-1",
    )


def make_authenticator(
    local_node_id: str,
    peer_node_id: str,
    clock=lambda: 1_000,
) -> RemoteMessageAuthenticator:
    return RemoteMessageAuthenticator(
        local_node_id=local_node_id,
        peer_secrets={peer_node_id: SECRET},
        clock=clock,
    )


def test_authenticated_message_round_trip() -> None:
    sender = make_authenticator("node-a", "node-b")
    receiver = make_authenticator("node-b", "node-a")

    wire_bytes = sender.seal(make_message(), "node-b")

    assert receiver.open(wire_bytes) == make_message()


def test_replayed_message_is_rejected() -> None:
    sender = make_authenticator("node-a", "node-b")
    receiver = make_authenticator("node-b", "node-a")
    wire_bytes = sender.seal(make_message(), "node-b")

    receiver.open(wire_bytes)

    with pytest.raises(ValueError, match="replayed"):
        receiver.open(wire_bytes)


def test_modified_payload_fails_authentication() -> None:
    sender = make_authenticator("node-a", "node-b")
    receiver = make_authenticator("node-b", "node-a")
    wire_bytes = sender.seal(make_message(), "node-b")

    tampered = wire_bytes.replace(
        b'"value":"original"',
        b'"value":"modified"',
    )
    assert tampered != wire_bytes

    with pytest.raises(ValueError, match="authentication failed"):
        receiver.open(tampered)


def test_message_for_another_node_is_rejected() -> None:
    sender = make_authenticator("node-a", "node-b")
    receiver = make_authenticator("node-c", "node-a")
    wire_bytes = sender.seal(make_message(), "node-b")

    with pytest.raises(ValueError, match="different node"):
        receiver.open(wire_bytes)


def test_expired_message_is_rejected() -> None:
    sender = make_authenticator("node-a", "node-b", clock=lambda: 1_000)
    receiver = make_authenticator("node-b", "node-a", clock=lambda: 2_000)
    wire_bytes = sender.seal(make_message(), "node-b")

    with pytest.raises(ValueError, match="expired"):
        receiver.open(wire_bytes)


def test_unknown_peer_cannot_be_used_for_signing() -> None:
    sender = make_authenticator("node-a", "node-b")

    with pytest.raises(ValueError, match="no shared secret"):
        sender.seal(make_message(), "node-c")


def test_short_shared_secret_is_rejected() -> None:
    with pytest.raises(ValueError, match="at least 32 bytes"):
        RemoteMessageAuthenticator(
            local_node_id="node-a",
            peer_secrets={"node-b": b"short"},
        )


def test_non_json_payload_is_rejected() -> None:
    sender = make_authenticator("node-a", "node-b")
    message = AgentMessage(
        id="message-2",
        sender_agent_id="agent-a",
        recipient_agent_id="agent-b",
        message_type=AgentMessageType.INFORMATION,
        payload={"not_json": object()},
    )

    with pytest.raises(ValueError, match="JSON-compatible"):
        sender.seal(message, "node-b")


class RecordingTransport(RemoteMessageTransport):
    def __init__(self) -> None:
        self.sent: list[tuple[str, bytes]] = []

    def send(self, endpoint: str, wire_bytes: bytes) -> None:
        self.sent.append((endpoint, wire_bytes))


def test_gateway_sends_signed_envelope_to_registered_endpoint() -> None:
    registry = ExecutionNodeRegistry(
        (
            ExecutionNodeRegistration(
                identity=ExecutionNodeIdentity(node_id="node-b"),
                endpoint="https://node-b.example",
            ),
        )
    )
    authenticator = make_authenticator("node-a", "node-b")
    transport = RecordingTransport()
    gateway = AuthenticatedRemoteMessageGateway(
        node_registry=registry,
        authenticator=authenticator,
        transport=transport,
    )

    gateway.send_to_node(make_message(), "node-b")

    assert len(transport.sent) == 1
    endpoint, wire_bytes = transport.sent[0]
    assert endpoint == "https://node-b.example"

    receiver = make_authenticator("node-b", "node-a")
    assert receiver.open(wire_bytes) == make_message()


def test_gateway_rejects_unregistered_destination() -> None:
    gateway = AuthenticatedRemoteMessageGateway(
        node_registry=ExecutionNodeRegistry(),
        authenticator=make_authenticator("node-a", "node-b"),
        transport=RecordingTransport(),
    )

    with pytest.raises(KeyError, match="execution node not found"):
        gateway.send_to_node(make_message(), "node-b")
