from brain.engineering.generation.models.engineering_generation_request import (
    EngineeringGenerationRequest,
)
from brain.engineering.loop.models.engineering_loop_request import (
    EngineeringLoopRequest,
)
from brain.engineering.testing.models.test_generation_request import (
    TestGenerationRequest,
)
from brain.evolution.models.evolution_task_result import (
    EvolutionTaskResult,
)


class EvolutionTaskExecutor:
    def __init__(
        self,
        engineering_generation,
        test_generator,
        engineering_loop,
        existing_code,
        verification_command,
        max_iterations=3,
    ):
        self._engineering_generation = (
            engineering_generation
        )
        self._test_generator = test_generator
        self._engineering_loop = engineering_loop
        self._existing_code = existing_code
        self._verification_command = (
            verification_command
        )
        self._max_iterations = max_iterations

    def execute(
        self,
        task,
        design,
        plan,
        task_id,
    ) -> EvolutionTaskResult:
        generation_result = (
            self._engineering_generation.generate(
                EngineeringGenerationRequest(
                    task=task,
                    design=design,
                    plan=plan,
                    existing_code=self._existing_code,
                )
            )
        )

        implementation_changes = (
            generation_result.changes
        )

        test_result = self._test_generator.generate(
            TestGenerationRequest(
                task=task,
                design=design,
                plan=plan,
                existing_code=self._existing_code,
                proposed_changes=(
                    implementation_changes
                ),
            )
        )

        proposed_changes = (
            implementation_changes
            + test_result.changes
        )

        engineering_result = (
            self._engineering_loop.execute(
                EngineeringLoopRequest(
                    task=task,
                    design=design,
                    plan=plan,
                    existing_code=self._existing_code,
                    proposed_changes=proposed_changes,
                    verification_command=(
                        self._verification_command
                    ),
                    max_iterations=self._max_iterations,
                )
            )
        )

        return EvolutionTaskResult(
            task_id=task_id,
            task_description=task.description,
            proposed_changes=proposed_changes,
            engineering_result=engineering_result,
        )