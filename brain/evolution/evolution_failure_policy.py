from brain.evolution.models.evolution_task_result import (
    EvolutionTaskResult,
)


class EvolutionFailurePolicy:
    def should_stop(
        self,
        task_result: EvolutionTaskResult,
    ) -> bool:
        if not isinstance(
            task_result,
            EvolutionTaskResult,
        ):
            raise TypeError(
                "task_result must be an EvolutionTaskResult"
            )

        return not task_result.engineering_result.passed