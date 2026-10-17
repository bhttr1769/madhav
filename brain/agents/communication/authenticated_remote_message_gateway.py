
from brain.agents.communication.agent_message_router import AgentMessageRouter
from brain.agents.communication.remote_message_authenticator import (
    RemoteMessageAuthenticator,
)
from brain.agents.communication.remote_message_transport import (
    RemoteMessageTransport,
)
from brain.agents.execution_node_registry import ExecutionNodeRegistry
from brain.agents.models.agent_message import AgentMessage


class AuthenticatedRemoteMessageGateway:
    """Sends authenticated remote messages and validates incoming envelopes."""

    def __init__(
        self,
        node_registry: ExecutionNodeRegistry,
        authenticator: RemoteMessageAuthenticator,
        transport: RemoteMessageTransport,
    ) -> None:
        if not isinstance(node_registry, ExecutionNodeRegistry):
            raise TypeError(
                "node_registry must be an ExecutionNodeRegistry"
            )

        if not isinstance(authenticator, RemoteMessageAuthenticator):
            raise TypeError(
                "authenticator must be a RemoteMessageAuthenticator"
            )

        if not isinstance(transport, RemoteMessageTransport):
            raise TypeError(
                "transport must be a RemoteMessageTransport"
            )

        self._node_registry = node_registry
        self._authenticator = authenticator
        self._transport = transport

    def send_to_node(
        self,
        message: AgentMessage,
        recipient_node_id: str,
    ) -> None:
        if not isinstance(message, AgentMessage):
            raise TypeError("message must be an AgentMessage")

        registration = self._node_registry.get(recipient_node_id)
        wire_bytes = self._authenticator.seal(
            message,
            recipient_node_id,
        )
        self._transport.send(registration.endpoint, wire_bytes)

    def receive(
        self,
        wire_bytes: bytes,
        local_router: AgentMessageRouter,
    ) -> None:
        """Authenticate an incoming message and deliver it locally."""
        self.receive_message(wire_bytes, local_router)

    def receive_message(
        self,
        wire_bytes: bytes,
        local_router: AgentMessageRouter,
    ) -> AgentMessage:
        """
        Authenticate, validate, route, and return an incoming message.

        The router remains responsible only for message delivery.
        """
        if not isinstance(wire_bytes, bytes):
            raise TypeError("wire_bytes must be bytes")

        if not isinstance(local_router, AgentMessageRouter):
            raise TypeError(
                "local_router must be an AgentMessageRouter"
            )

        message = self._authenticator.open(wire_bytes)
        local_router.send(message)
        return message
