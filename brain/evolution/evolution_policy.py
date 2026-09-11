from brain.evolution.models.evolution_mode import (
    EvolutionMode,
)

from brain.evolution.models.evolution_mode import (
    EvolutionMode,
)

class EvolutionPolicy:
    def allows_implementation(
        self,
        mode: EvolutionMode,
    ) -> bool:
        if not isinstance(mode, EvolutionMode):
            raise TypeError(
                "mode must be an EvolutionMode"
            )

        return mode in {
            EvolutionMode.SUPERVISED,
            EvolutionMode.AUTONOMOUS,
        }

    def allows_verification(
        self,
        mode: EvolutionMode,
    ) -> bool:
        if not isinstance(mode, EvolutionMode):
            raise TypeError(
                "mode must be an EvolutionMode"
            )

        return mode in {
            EvolutionMode.SUPERVISED,
            EvolutionMode.AUTONOMOUS,
        }

    def allows_integration(
        self,
        mode: EvolutionMode,
    ) -> bool:
        if not isinstance(mode, EvolutionMode):
            raise TypeError(
                "mode must be an EvolutionMode"
            )

        return mode is EvolutionMode.AUTONOMOUS

def __post_init__(self):
    if not isinstance(
        self.requested_capability,
        str,
    ):
        raise TypeError(
            "requested_capability must be a string"
        )

    if not self.requested_capability.strip():
        raise ValueError(
            "requested_capability must not be empty"
        )

    if not isinstance(
        self.objective,
        str,
    ):
        raise TypeError(
            "objective must be a string"
        )

    if not self.objective.strip():
        raise ValueError(
            "objective must not be empty"
        )

    try:
        EvolutionMode(self.mode)
    except (ValueError, TypeError) as exc:
        raise ValueError(
            f"invalid evolution mode: {self.mode}"
        ) from exc