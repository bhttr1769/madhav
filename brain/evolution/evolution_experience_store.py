from brain.evolution.models.evolution_experience import (
    EvolutionExperience,
)


class EvolutionExperienceStore:
    def __init__(self):
        self._experiences = []

    def add(
        self,
        experience: EvolutionExperience,
    ) -> None:
        if not isinstance(
            experience,
            EvolutionExperience,
        ):
            raise TypeError(
                "experience must be an EvolutionExperience"
            )

        self._experiences.append(experience)

    def add_all(
        self,
        experiences: tuple[EvolutionExperience, ...],
    ) -> None:
        if not isinstance(experiences, tuple):
            raise TypeError(
                "experiences must be a tuple"
            )

        for experience in experiences:
            self.add(experience)

    def all(
        self,
    ) -> tuple[EvolutionExperience, ...]:
        return tuple(self._experiences)