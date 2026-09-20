from datetime import datetime

from brain.evolution.models.evolution_history import (
    EvolutionHistory,
)
from brain.evolution.models.evolution_result import (
    EvolutionResult,
)


class EvolutionHistoryBuilder:
    def build(
        self,
        evolution_id: str,
        request,
        result: EvolutionResult,
        started_at: datetime,
        completed_at: datetime,
        status: str,
    ) -> EvolutionHistory:
        if not isinstance(
            evolution_id,
            str,
        ):
            raise TypeError(
                "evolution_id must be a string"
            )

        if not isinstance(
            result,
            EvolutionResult,
        ):
            raise TypeError(
                "result must be an EvolutionResult"
            )

        if not isinstance(
            started_at,
            datetime,
        ):
            raise TypeError(
                "started_at must be a datetime"
            )

        if not isinstance(
            completed_at,
            datetime,
        ):
            raise TypeError(
                "completed_at must be a datetime"
            )

        task_count = len(
            result.task_decomposition.tasks
        )

        completed_task_count = len(
            result.task_results
        )

        termination_reason = (
            result.task_results[-1]
            .engineering_result
            .termination_reason
            if result.task_results
            else "no_tasks_executed"
        )

        return EvolutionHistory(
            evolution_id=evolution_id,
            requested_capability=(
                result.requested_capability
            ),
            objective=request.objective,
            mode=request.mode,
            status=status,
            started_at=started_at,
            completed_at=completed_at,
            task_count=task_count,
            completed_task_count=(
                completed_task_count
            ),
            passed=result.passed,
            termination_reason=(
                termination_reason
            ),
        )