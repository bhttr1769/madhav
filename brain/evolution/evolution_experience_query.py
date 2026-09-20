from brain.evolution.models.evolution_experience import (
    EvolutionExperience,
)


class EvolutionExperienceQuery:
    def __init__(self, store):
        self._store = store

    def all(
        self,
    ) -> tuple[EvolutionExperience, ...]:
        return self._store.all()

    def by_capability(
        self,
        requested_capability: str,
    ) -> tuple[EvolutionExperience, ...]:
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
            experience
            for experience in self._store.all()
            if experience.requested_capability
            == requested_capability
        )

    def by_evolution(
        self,
        evolution_id: str,
    ) -> tuple[EvolutionExperience, ...]:
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

        return tuple(
            experience
            for experience in self._store.all()
            if experience.evolution_id == evolution_id
        )

    def reusable(
        self,
    ) -> tuple[EvolutionExperience, ...]:
        return tuple(
            experience
            for experience in self._store.all()
            if experience.reusable
        )

    def successful(
        self,
    ) -> tuple[EvolutionExperience, ...]:
        return tuple(
            experience
            for experience in self._store.all()
            if experience.outcome == "success"
        )

    def failed(
        self,
    ) -> tuple[EvolutionExperience, ...]:
        return tuple(
            experience
            for experience in self._store.all()
            if experience.outcome == "failure"
        )