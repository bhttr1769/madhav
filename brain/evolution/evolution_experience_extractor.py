from brain.evolution.models.evolution_experience import (
    EvolutionExperience,
)
from brain.evolution.models.evolution_result import (
    EvolutionResult,
)


class EvolutionExperienceExtractor:
    def extract(
        self,
        evolution_id: str,
        result: EvolutionResult,
    ) -> tuple[EvolutionExperience, ...]:
        if not isinstance(evolution_id, str):
            raise TypeError(
                "evolution_id must be a string"
            )

        if not evolution_id.strip():
            raise ValueError(
                "evolution_id must not be empty"
            )

        if not isinstance(result, EvolutionResult):
            raise TypeError(
                "result must be an EvolutionResult"
            )

        experiences = []

        for task_result in result.task_results:
            passed = task_result.engineering_result.passed

            if passed:
                outcome = "success"
                lesson = (
                    f"Task completed successfully: "
                    f"{task_result.task_description}"
                )
            else:
                outcome = "failure"
                lesson = (
                    f"Task failed during engineering execution: "
                    f"{task_result.task_description}"
                )

            experiences.append(
                EvolutionExperience(
                    evolution_id=evolution_id,
                    requested_capability=result.requested_capability,
                    task_id=task_result.task_id,
                    task_description=task_result.task_description,
                    outcome=outcome,
                    lesson=lesson,
                    reusable=True,
                )
            )

        return tuple(experiences)