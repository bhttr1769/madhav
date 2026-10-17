from brain.agents.models.remote_execution_record import (
    RemoteExecutionRecord,
    RemoteExecutionStatus,
)
from brain.agents.persistence.remote_execution_persistence import (
    RemoteExecutionPersistence,
)
from brain.safety.logging.models.action_log_event import ActionLogEvent
from brain.safety.logging.models.action_log_status import ActionLogStatus
from brain.safety.logging.services.logging_service import LoggingService
from brain.safety.models.action import Action


class RemoteExecutionReconciliationCoordinator:
    """Reconcile incomplete remote dispatches without replaying them."""

    def __init__(
        self,
        persistence: RemoteExecutionPersistence,
        logging_service: LoggingService | None = None,
    ) -> None:
        if not isinstance(persistence, RemoteExecutionPersistence):
            raise TypeError(
                "persistence must be a RemoteExecutionPersistence"
            )

        if logging_service is not None and not isinstance(
            logging_service,
            LoggingService,
        ):
            raise TypeError(
                "logging_service must be a LoggingService or None"
            )

        self._persistence = persistence
        self._logging_service = logging_service

    def reconcile_incomplete(
        self,
    ) -> tuple[RemoteExecutionRecord, ...]:
        """
        Mark persisted CLAIMED/RUNNING records uncertain.

        The caller must first establish that the previous execution
        process has stopped. This method never re-executes work.
        """
        reconciled = []

        for record in self._persistence.all():
            if record.status not in {
                RemoteExecutionStatus.CLAIMED,
                RemoteExecutionStatus.RUNNING,
            }:
                continue

            updated = RemoteExecutionRecord(
                dispatch_id=record.dispatch_id,
                request_fingerprint=record.request_fingerprint,
                owner_node_id=record.owner_node_id,
                status=RemoteExecutionStatus.UNCERTAIN,
            )
            self._persistence.save(updated)
            reconciled.append(updated)

            self._log_uncertain(updated)

        return tuple(reconciled)

    def _log_uncertain(
        self,
        record: RemoteExecutionRecord,
    ) -> None:
        if self._logging_service is None:
            return

        try:
            self._logging_service.log(
                action=Action(
                    name="reconcile_remote_execution",
                    category="distributed_execution",
                    target=record.dispatch_id,
                ),
                event=ActionLogEvent.EXECUTION_FAILED,
                status=ActionLogStatus.FAILED,
                metadata={
                    "phase": "reconciliation",
                    "outcome": "uncertain",
                    "dispatch_id": record.dispatch_id,
                    "owner_node_id": record.owner_node_id,
                    "previous_status": "incomplete",
                    "current_status": record.status.value,
                },
            )
        except Exception:
            # The durable reconciliation result must remain authoritative.
            pass