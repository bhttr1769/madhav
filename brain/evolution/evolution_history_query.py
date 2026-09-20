from brain.evolution.models.evolution_history import (
    EvolutionHistory,
)


class EvolutionHistoryQuery:
    def __init__(
        self,
        recorder,
    ):
        self._recorder = recorder

    def all(
        self,
    ) -> tuple[EvolutionHistory, ...]:
        return self._recorder.all()

    def by_capability(
        self,
        requested_capability: str,
    ) -> tuple[EvolutionHistory, ...]:
        if not isinstance(
            requested_capability,
            str,
        ):
            raise TypeError(
                "requested_capability must be a string"
            )

        if not requested_capability.strip():
            raise ValueError(
                "requested_capability must not be empty"
            )

        return tuple(
            history
            for history in self._recorder.all()
            if history.requested_capability
            == requested_capability
        )

    def by_status(
        self,
        status: str,
    ) -> tuple[EvolutionHistory, ...]:
        if not isinstance(
            status,
            str,
        ):
            raise TypeError(
                "status must be a string"
            )

        if not status.strip():
            raise ValueError(
                "status must not be empty"
            )

        return tuple(
            history
            for history in self._recorder.all()
            if history.status == status
        )

    def passed(
        self,
    ) -> tuple[EvolutionHistory, ...]:
        return tuple(
            history
            for history in self._recorder.all()
            if history.passed
        )

    def failed(
        self,
    ) -> tuple[EvolutionHistory, ...]:
        return tuple(
            history
            for history in self._recorder.all()
            if not history.passed
        )