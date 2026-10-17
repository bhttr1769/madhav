
from collections.abc import Iterable, Mapping
from datetime import datetime, timezone

from brain.agents.agent_runtime_registry import AgentRuntimeRegistry
from brain.agents.communication.agent_message_router import AgentMessageRouter
from brain.agents.communication.authenticated_remote_message_gateway import (
    AuthenticatedRemoteMessageGateway,
)
from brain.agents.communication.remote_task_execution_handler import (
    RemoteTaskExecutionHandler,
)
from brain.agents.models.agent_message import (
    AgentMessage,
    AgentMessageType,
)
from brain.agents.models.authenticated_remote_message import (
    AuthenticatedRemoteMessage,
)
from brain.organization.authority_evaluation_service import (
    AuthorityEvaluationService,
)
from brain.organization.models.organization_persistence_state import (
    OrganizationPersistenceState,
)


class RemoteTaskExecutionReceiver:
    """
    Receive authenticated remote task requests.

    Node authentication, node-to-agent binding, and organizational authority
    are checked before a remote capability is executed.
    """

    def __init__(
        self,
        gateway: AuthenticatedRemoteMessageGateway,
        router: AgentMessageRouter,
        runtime_registry: AgentRuntimeRegistry,
        execution_handler: RemoteTaskExecutionHandler,
        *,
        organization_persistence: object | None = None,
        authority_evaluation_service: AuthorityEvaluationService | None = None,
        node_agent_bindings: Mapping[str, Iterable[str]] | None = None,
    ) -> None:
        if not isinstance(gateway, AuthenticatedRemoteMessageGateway):
            raise TypeError(
                "gateway must be an AuthenticatedRemoteMessageGateway"
            )
        if not isinstance(router, AgentMessageRouter):
            raise TypeError("router must be an AgentMessageRouter")
        if not isinstance(runtime_registry, AgentRuntimeRegistry):
            raise TypeError(
                "runtime_registry must be an AgentRuntimeRegistry"
            )
        if not isinstance(execution_handler, RemoteTaskExecutionHandler):
            raise TypeError(
                "execution_handler must be a RemoteTaskExecutionHandler"
            )

        if (organization_persistence is None) != (
            authority_evaluation_service is None
        ):
            raise ValueError(
                "organization_persistence and "
                "authority_evaluation_service must be configured together"
            )

        if authority_evaluation_service is not None and not isinstance(
            authority_evaluation_service,
            AuthorityEvaluationService,
        ):
            raise TypeError(
                "authority_evaluation_service must be an "
                "AuthorityEvaluationService or None"
            )

        if organization_persistence is not None and not callable(
            getattr(organization_persistence, "load", None)
        ):
            raise TypeError(
                "organization_persistence must provide a callable load method"
            )

        normalized_bindings: dict[str, frozenset[str]] = {}

        if node_agent_bindings is not None:
            if not isinstance(node_agent_bindings, Mapping):
                raise TypeError("node_agent_bindings must be a mapping")

            for node_id, agent_ids in node_agent_bindings.items():
                if not isinstance(node_id, str) or not node_id.strip():
                    raise ValueError(
                        "node binding IDs must be non-empty strings"
                    )

                if isinstance(agent_ids, (str, bytes)):
                    raise TypeError(
                        "each node binding must contain an iterable of agent IDs"
                    )

                try:
                    normalized_ids = frozenset(agent_ids)
                except TypeError as exc:
                    raise TypeError(
                        "each node binding must contain an iterable of agent IDs"
                    ) from exc

                if not normalized_ids:
                    raise ValueError(
                        f"node {node_id!r} must have at least one bound agent"
                    )

                if any(
                    not isinstance(agent_id, str) or not agent_id.strip()
                    for agent_id in normalized_ids
                ):
                    raise ValueError(
                        "bound agent IDs must be non-empty strings"
                    )

                normalized_bindings[node_id] = normalized_ids

        self._gateway = gateway
        self._router = router
        self._runtime_registry = runtime_registry
        self._execution_handler = execution_handler
        self._organization_persistence = organization_persistence
        self._authority_evaluation_service = authority_evaluation_service
        self._node_agent_bindings = normalized_bindings

    def receive(self, wire_bytes: bytes) -> AgentMessage | None:
        """
        Authenticate and route a message; execute authorized remote tasks.

        Non-task messages are routed normally and return None.
        """
        if not isinstance(wire_bytes, bytes):
            raise TypeError("wire_bytes must be bytes")

        # Do not trust the sender node ID until gateway authentication succeeds.
        envelope = AuthenticatedRemoteMessage.from_wire_bytes(wire_bytes)

        message = self._gateway.receive_message(
            wire_bytes,
            self._router,
        )

        if message.message_type != AgentMessageType.REQUEST:
            return None

        if message.payload.get("kind") != "remote_task_dispatch":
            return None

        runtime = self._resolve_runtime(message.recipient_agent_id)

        self._authorize_remote_execution(
            message=message,
            authenticated_sender_node_id=envelope.sender_node_id,
            runtime=runtime,
        )

        response = self._execution_handler.handle(
            message,
            runtime,
            authority_agent_id=message.sender_agent_id,
        )

        self._gateway.send_to_node(
            response,
            envelope.sender_node_id,
        )

        return response

    def _authorize_remote_execution(
        self,
        message: AgentMessage,
        authenticated_sender_node_id: str,
        runtime: object,
    ) -> None:
        """
        Fail closed unless node identity, organization state, and authority
        all authorize this capability request.
        """
        if (
            self._organization_persistence is None
            or self._authority_evaluation_service is None
        ):
            raise PermissionError(
                "Remote execution denied: organizational authorization "
                "is not configured."
            )

        allowed_agents = self._node_agent_bindings.get(
            authenticated_sender_node_id
        )

        if (
            allowed_agents is None
            or message.sender_agent_id not in allowed_agents
        ):
            raise PermissionError(
                "Remote execution denied: authenticated node is not "
                "authorized to act as the requesting agent."
            )

        if message.recipient_agent_id != runtime.agent_id:
            raise PermissionError(
                "Remote execution denied: recipient runtime identity mismatch."
            )

        organization_id = runtime.organization_id
        if not isinstance(organization_id, str) or not organization_id.strip():
            raise PermissionError(
                "Remote execution denied: recipient has no organization."
            )

        capability_id = message.payload.get("capability_id")
        if not isinstance(capability_id, str) or not capability_id.strip():
            raise PermissionError(
                "Remote execution denied: capability ID is missing or invalid."
            )

        try:
            state = self._organization_persistence.load(organization_id)
        except Exception as exc:
            raise PermissionError(
                "Remote execution denied: organization state could not be loaded."
            ) from exc

        if not isinstance(state, OrganizationPersistenceState):
            raise PermissionError(
                "Remote execution denied: organization state is invalid."
            )

        if state.organization.id != organization_id:
            raise PermissionError(
                "Remote execution denied: organization identity mismatch."
            )

        decision = self._authority_evaluation_service.evaluate(
            organization=state.organization,
            memberships=state.memberships,
            delegations=state.delegations,
            requesting_agent_id=message.sender_agent_id,
            action="execute_capability",
            target=capability_id,
            at=datetime.now(timezone.utc),
        )

        if not decision.allowed:
            raise PermissionError(
                "Remote execution denied by organizational authority: "
                f"{decision.reason}"
            )

    def _resolve_runtime(self, agent_id: str):
        matches = tuple(
            runtime
            for runtime in self._runtime_registry.all()
            if runtime.agent_id == agent_id
        )

        if not matches:
            raise LookupError(
                f"no runtime registered for recipient agent: {agent_id}"
            )

        if len(matches) > 1:
            raise ValueError(
                f"multiple runtimes registered for recipient agent: {agent_id}"
            )

        return matches[0]
