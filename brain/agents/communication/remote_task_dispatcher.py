from brain.agents.communication.authenticated_remote_message_gateway import (
    AuthenticatedRemoteMessageGateway,
)
from brain.agents.models.agent_message import AgentMessage
from brain.agents.models.remote_task_dispatch import RemoteTaskDispatch
from brain.agents.models.remote_task_result import RemoteTaskResult
from brain.safety.logging.models.action_log_event import ActionLogEvent
from brain.safety.logging.models.action_log_status import ActionLogStatus
from brain.safety.logging.services.logging_service import LoggingService
from brain.safety.models.action import Action


class RemoteTaskDispatcher:
    """Dispatch tasks through authenticated remote messaging."""

    def __init__(
        self,
        gateway: AuthenticatedRemoteMessageGateway,
        logging_service: LoggingService | None = None,
    ) -> None:
        if not isinstance(gateway, AuthenticatedRemoteMessageGateway):
            raise TypeError(
                "gateway must be an AuthenticatedRemoteMessageGateway"
            )

        if logging_service is not None and not isinstance(
            logging_service,
            LoggingService,
        ):
            raise TypeError(
                "logging_service must be a LoggingService or None"
            )

        self._gateway = gateway
        self._logging_service = logging_service

    def dispatch(self, request: RemoteTaskDispatch) -> AgentMessage:
        """Send a task request and return its correlation-bearing message."""

        if not isinstance(request, RemoteTaskDispatch):
            raise TypeError("request must be a RemoteTaskDispatch")

        message = request.to_message()

        self._log(
            request,
            ActionLogEvent.REQUESTED,
            ActionLogStatus.PENDING,
            phase="dispatch_attempted",
            outcome="pending",
        )

        try:
            self._gateway.send_to_node(
                message,
                request.recipient_node_id,
            )
        except Exception as exc:
            self._log(
                request,
                ActionLogEvent.EXECUTION_FAILED,
                ActionLogStatus.FAILED,
                phase="dispatch_delivery",
                outcome="failed",
                error_type=type(exc).__name__,
            )
            raise

        self._log(
            request,
            ActionLogEvent.REQUESTED,
            ActionLogStatus.PENDING,
            phase="dispatch_sent",
            outcome="sent",
        )

        return message

    @staticmethod
    def correlate_result(
        request: RemoteTaskDispatch,
        response: AgentMessage,
    ) -> RemoteTaskResult:
        """Validate a response against the exact dispatch that created it."""

        return RemoteTaskResult.from_message(response, request)

    def _log(
        self,
        request: RemoteTaskDispatch,
        event: ActionLogEvent,
        status: ActionLogStatus,
        *,
        phase: str,
        outcome: str,
        error_type: str | None = None,
    ) -> None:
        """Record safe dispatch metadata without affecting delivery."""

        if self._logging_service is None:
            return

        metadata = {
            "phase": phase,
            "outcome": outcome,
            "dispatch_id": request.dispatch_id,
            "task_id": request.task.id,
            "goal_id": request.goal.id,
            "workflow_id": request.workflow.id,
            "workflow_step_id": request.step.id,
            "operation_id": request.operation.id,
            "sender_agent_id": request.sender_agent_id,
            "recipient_agent_id": request.recipient_agent_id,
            "recipient_node_id": request.recipient_node_id,
            "error_type": error_type,
        }

        try:
            self._logging_service.log(
                action=Action(
                    name="remote_task_dispatch",
                    category="distributed_execution",
                    target=request.dispatch_id,
                ),
                event=event,
                status=status,
                metadata=metadata,
            )
        except Exception:
            # Observability must not change dispatch behavior.
            pass