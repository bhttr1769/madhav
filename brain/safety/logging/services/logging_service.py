from datetime import datetime
from uuid import uuid4
from typing import Any

from brain.safety.logging.models.action_log import (
    ActionLog,
)

from brain.safety.logging.models.action_log_event import (
    ActionLogEvent,
)

from brain.safety.logging.models.action_log_status import (
    ActionLogStatus,
)

from brain.safety.logging.services.privacy_service import (
    PrivacyService,
)

from brain.safety.logging.stores.action_log_store import (
    ActionLogStore,
)

from brain.safety.models.action import (
    Action,
)


class LoggingService:
    """
    Creates, sanitizes, and stores action log records.
    """

    def __init__(
        self,
        store: ActionLogStore,
        privacy_service: PrivacyService | None = None,
    ):

        self._store = store

        self._privacy_service = (
            privacy_service
            if privacy_service is not None
            else PrivacyService()
        )

    def log(
        self,
        action: Action,
        event: ActionLogEvent,
        status: ActionLogStatus,
        metadata: dict[str, Any] | None = None,
    ) -> ActionLog:

        safe_action = (
            self._privacy_service
            .sanitize_action(
                action,
            )
        )

        safe_metadata = (
            self._privacy_service
            .sanitize_metadata(
                dict(metadata)
                if metadata is not None
                else {}
            )
        )

        log = ActionLog(
            id=str(uuid4()),
            action=safe_action,
            timestamp=datetime.now(),
            event=event,
            status=status,
            metadata=safe_metadata,
        )

        self._store.append(
            log,
        )

        return log