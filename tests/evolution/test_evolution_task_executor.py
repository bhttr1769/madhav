import pytest

from brain.engineering.generation.models.code_change import (
    CodeChange,
)
from brain.engineering.generation.models.engineering_generation_result import (
    EngineeringGenerationResult,
)
from brain.engineering.loop.models.engineering_loop_result import (
    EngineeringLoopResult,
)
from brain.engineering.testing.models.test_generation_result import (
    TestGenerationResult as GenerationTestResult,
)
from brain.evolution.evolution_task_executor import (
    EvolutionTaskExecutor,
)


class FakeEngineeringGeneration:
    def __init__(self, result):
        self.result = result
        self.calls = []

    def generate(self, request):
        self.calls.append(request)
        return self.result


class FakeTestGenerator:
    def __init__(self, result):
        self.result = result
        self.calls = []

    def generate(self, request):
        self.calls.append(request)
        return self.result


class FakeEngineeringLoop:
    def __init__(self, result):
        self.result = result
        self.calls = []

    def execute(self, request):
        self.calls.append(request)
        return self.result


class FakeTask:
    description = "Implement repository analysis."


class FakeDesign:
    pass


class FakePlan:
    pass


def create_code_change(
    path: str,
) -> CodeChange:
    return CodeChange(
        path=path,
        operation="create",
        content="test content",
    )


def create_generation_result(
    changes,
):
    return EngineeringGenerationResult(
        changes=changes,
        engineering_decision=None,
        quality_assessment=None,
        optimization_decision=None,
    )


def create_test_result(
    changes,
):
    return GenerationTestResult(
        changes=changes,
    )


def create_engineering_result():
    return EngineeringLoopResult(
        changes=(),
        passed=True,
        iterations=(),
        termination_reason="verification_passed",
    )


def create_executor(
    engineering_generation,
    test_generator,
    engineering_loop,
):
    return EvolutionTaskExecutor(
        engineering_generation=engineering_generation,
        test_generator=test_generator,
        engineering_loop=engineering_loop,
        existing_code="existing-code",
        verification_command="pytest",
        max_iterations=5,
    )


def test_executes_engineering_generation():
    implementation_change = create_code_change(
        "implementation.py",
    )

    generation_result = create_generation_result(
        (implementation_change,),
    )

    engineering_generation = FakeEngineeringGeneration(
        generation_result,
    )

    test_generator = FakeTestGenerator(
        create_test_result(()),
    )

    engineering_loop = FakeEngineeringLoop(
        create_engineering_result(),
    )

    executor = create_executor(
        engineering_generation,
        test_generator,
        engineering_loop,
    )

    task = FakeTask()
    design = FakeDesign()
    plan = FakePlan()

    executor.execute(
        task=task,
        design=design,
        plan=plan,
        task_id="task-1",
    )

    assert len(
        engineering_generation.calls
    ) == 1

    request = engineering_generation.calls[0]

    assert request.task is task
    assert request.design is design
    assert request.plan is plan
    assert request.existing_code == "existing-code"


def test_passes_implementation_changes_to_test_generator():
    implementation_change = create_code_change(
        "implementation.py",
    )

    generation_result = create_generation_result(
        (implementation_change,),
    )

    engineering_generation = FakeEngineeringGeneration(
        generation_result,
    )

    test_generator = FakeTestGenerator(
        create_test_result(()),
    )

    engineering_loop = FakeEngineeringLoop(
        create_engineering_result(),
    )

    executor = create_executor(
        engineering_generation,
        test_generator,
        engineering_loop,
    )

    task = FakeTask()
    design = FakeDesign()
    plan = FakePlan()

    executor.execute(
        task=task,
        design=design,
        plan=plan,
        task_id="task-1",
    )

    assert len(
        test_generator.calls
    ) == 1

    request = test_generator.calls[0]

    assert request.task is task
    assert request.design is design
    assert request.plan is plan
    assert request.existing_code == "existing-code"
    assert request.proposed_changes == (
        implementation_change,
    )


def test_passes_combined_changes_to_engineering_loop():
    implementation_change = create_code_change(
        "implementation.py",
    )

    test_change = create_code_change(
        "test_implementation.py",
    )

    engineering_generation = FakeEngineeringGeneration(
        create_generation_result(
            (implementation_change,),
        ),
    )

    test_generator = FakeTestGenerator(
        create_test_result(
            (test_change,),
        ),
    )

    engineering_loop = FakeEngineeringLoop(
        create_engineering_result(),
    )

    executor = create_executor(
        engineering_generation,
        test_generator,
        engineering_loop,
    )

    task = FakeTask()
    design = FakeDesign()
    plan = FakePlan()

    executor.execute(
        task=task,
        design=design,
        plan=plan,
        task_id="task-1",
    )

    assert len(
        engineering_loop.calls
    ) == 1

    request = engineering_loop.calls[0]

    assert request.task is task
    assert request.design is design
    assert request.plan is plan
    assert request.existing_code == "existing-code"
    assert request.proposed_changes == (
        implementation_change,
        test_change,
    )


def test_forwards_verification_configuration():
    engineering_generation = FakeEngineeringGeneration(
        create_generation_result(()),
    )

    test_generator = FakeTestGenerator(
        create_test_result(()),
    )

    engineering_loop = FakeEngineeringLoop(
        create_engineering_result(),
    )

    executor = create_executor(
        engineering_generation,
        test_generator,
        engineering_loop,
    )

    executor.execute(
        task=FakeTask(),
        design=FakeDesign(),
        plan=FakePlan(),
        task_id="task-1",
    )

    request = engineering_loop.calls[0]

    assert request.verification_command == "pytest"
    assert request.max_iterations == 5


def test_returns_evolution_task_result():
    implementation_change = create_code_change(
        "implementation.py",
    )

    test_change = create_code_change(
        "test_implementation.py",
    )

    engineering_result = create_engineering_result()

    engineering_generation = FakeEngineeringGeneration(
        create_generation_result(
            (implementation_change,),
        ),
    )

    test_generator = FakeTestGenerator(
        create_test_result(
            (test_change,),
        ),
    )

    engineering_loop = FakeEngineeringLoop(
        engineering_result,
    )

    executor = create_executor(
        engineering_generation,
        test_generator,
        engineering_loop,
    )

    result = executor.execute(
        task=FakeTask(),
        design=FakeDesign(),
        plan=FakePlan(),
        task_id="task-1",
    )

    assert result.task_id == "task-1"

    assert result.task_description == (
        "Implement repository analysis."
    )

    assert result.proposed_changes == (
        implementation_change,
        test_change,
    )

    assert result.engineering_result == (
        engineering_result
    )


def test_preserves_failed_engineering_result():
    failed_result = EngineeringLoopResult(
        changes=(),
        passed=False,
        iterations=(),
        termination_reason="max_iterations_reached",
    )

    engineering_generation = FakeEngineeringGeneration(
        create_generation_result(()),
    )

    test_generator = FakeTestGenerator(
        create_test_result(()),
    )

    engineering_loop = FakeEngineeringLoop(
        failed_result,
    )

    executor = create_executor(
        engineering_generation,
        test_generator,
        engineering_loop,
    )

    result = executor.execute(
        task=FakeTask(),
        design=FakeDesign(),
        plan=FakePlan(),
        task_id="task-1",
    )

    assert result.engineering_result == failed_result
    assert result.engineering_result.passed is False