from datetime import datetime
from datetime import timedelta

from brain.safety.logging.stores.action_log_store import (
    ActionLogStore,
)


class RetentionService:
    """
    Removes action logs older than the configured
    retention period.
    """

    def __init__(
        self,
        store: ActionLogStore,
        retention_days: int,
    ):

        if retention_days < 0:

            raise ValueError(
                "retention_days cannot be negative."
            )

        self._store = store

        self._retention_days = (
            retention_days
        )

    def purge(
        self,
        now: datetime | None = None,
    ) -> int:

        current_time = (
            now
            if now is not None
            else datetime.now()
        )

        cutoff = (
            current_time
            - timedelta(
                days=self._retention_days,
            )
        )

        logs = self._store.all()

        retained = [
            log
            for log in logs
            if log.timestamp >= cutoff
        ]

        removed = (
            len(logs)
            - len(retained)
        )

        self._store.clear()

        for log in retained:

            self._store.append(
                log,
            )

        return removed