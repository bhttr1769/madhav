from brain.safety.logging.models.action_log import (
    ActionLog,
)


class ActionLogStore:
    """
    Stores immutable action log records.
    """

    def __init__(
        self,
    ):

        self._logs = []

    def append(
        self,
        log: ActionLog,
    ) -> None:

        self._logs.append(
            log,
        )

    def all(
        self,
    ) -> list[ActionLog]:

        return list(
            self._logs,
        )

    def get(
        self,
        log_id: str,
    ) -> ActionLog | None:

        for log in self._logs:

            if log.id == log_id:

                return log

        return None

    def count(
        self,
    ) -> int:

        return len(
            self._logs,
        )

    def clear(
        self,
    ) -> None:

        self._logs.clear()