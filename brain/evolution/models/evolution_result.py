from dataclasses import dataclass

from brain.engineering.design.models.system_design import (
    SystemDesign,
)
from brain.engineering.generation.models.code_change import (
    CodeChange,
)
from brain.engineering.loop.models.engineering_loop_result import (
    EngineeringLoopResult,
)
from brain.engineering.planning.models.plan import (
    EngineeringPlan,
)
from brain.engineering.requirements.models.requirement import (
    Requirement,
)
from brain.engineering.tasks.models.task_decomposition import (
    TaskDecomposition,
)
from brain.evolution.models.evolution_task_result import (
    EvolutionTaskResult,
)


@dataclass(frozen=True)
class EvolutionResult:
    requested_capability: str
    requirement: Requirement
    task_decomposition: TaskDecomposition
    design: SystemDesign
    plan: EngineeringPlan

    proposed_changes: tuple[CodeChange, ...] = ()
    engineering_result: EngineeringLoopResult | None = None
    task_results: tuple[EvolutionTaskResult, ...] = ()

    @property
    def all_proposed_changes(
        self,
    ) -> tuple[CodeChange, ...]:
        if self.task_results:
            changes = []

            for task_result in self.task_results:
                changes.extend(
                    task_result.proposed_changes
                )

            return tuple(changes)

        return self.proposed_changes

    @property
    def passed(self) -> bool:
        if self.task_results:
            return all(
                task_result.engineering_result.passed
                for task_result in self.task_results
            )

        if self.engineering_result is None:
            return True

        return self.engineering_result.passed