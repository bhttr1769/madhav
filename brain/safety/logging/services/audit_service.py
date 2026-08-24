from datetime import datetime

from brain.safety.logging.models.action_log import (
    ActionLog,
)

from brain.safety.logging.models.action_log_event import (
    ActionLogEvent,
)

from brain.safety.logging.models.action_log_status import (
    ActionLogStatus,
)

from brain.safety.logging.stores.action_log_store import (
    ActionLogStore,
)


class AuditService:
    """
    Provides querying and audit capabilities
    over action log records.
    """

    def __init__(
        self,
        store: ActionLogStore,
    ):

        self._store = store

    def all(
        self,
    ) -> list[ActionLog]:

        return self._store.all()

    def get(
        self,
        log_id: str,
    ) -> ActionLog | None:

        return self._store.get(
            log_id,
        )

    def by_event(
        self,
        event: ActionLogEvent,
    ) -> list[ActionLog]:

        return [
            log
            for log in self._store.all()
            if log.event == event
        ]

    def by_status(
        self,
        status: ActionLogStatus,
    ) -> list[ActionLog]:

        return [
            log
            for log in self._store.all()
            if log.status == status
        ]

    def by_category(
        self,
        category: str,
    ) -> list[ActionLog]:

        return [
            log
            for log in self._store.all()
            if log.action.category
            == category
        ]

    def between(
        self,
        start: datetime,
        end: datetime,
    ) -> list[ActionLog]:

        return [
            log
            for log in self._store.all()
            if start
            <= log.timestamp
            <= end
        ]

    def count(
        self,
    ) -> int:

        return self._store.count()