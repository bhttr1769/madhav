from brain.evolution.models.evolution_history import (
    EvolutionHistory,
)


class EvolutionHistoryRecorder:
    def __init__(self):
        self._history = []

    def record(
        self,
        history: EvolutionHistory,
    ) -> None:
        if not isinstance(
            history,
            EvolutionHistory,
        ):
            raise TypeError(
                "history must be an EvolutionHistory"
            )

        self._history.append(
            history
        )

    def all(
        self,
    ) -> tuple[EvolutionHistory, ...]:
        return tuple(
            self._history
        )

    def get(
        self,
        evolution_id: str,
    ) -> EvolutionHistory:
        if not isinstance(
            evolution_id,
            str,
        ):
            raise TypeError(
                "evolution_id must be a string"
            )

        if not evolution_id.strip():
            raise ValueError(
                "evolution_id must not be empty"
            )

        for history in self._history:
            if history.evolution_id == evolution_id:
                return history

        raise KeyError(
            f"evolution history not found: "
            f"{evolution_id}"
        )