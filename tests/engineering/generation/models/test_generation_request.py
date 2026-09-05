from brain.code.models.code_structure import CodeStructure

from brain.engineering.design.models.system_design import (
    SystemDesign,
)
from brain.engineering.generation.models.engineering_decision import (
    EngineeringDecision,
)
from brain.engineering.generation.models.generation_request import (
    GenerationRequest,
)
from brain.engineering.planning.models.plan import (
    EngineeringPlan,
)
from brain.engineering.requirements.models.requirement import (
    Requirement,
)
from brain.engineering.tasks.models.task import (
    Task,
)


def _create_requirement() -> Requirement:
    return Requirement(
        original_request="Implement a user authentication feature.",
        objective="Allow users to authenticate securely.",
        functional_requirements=frozenset(
            {"Users can log in."}
        ),
        non_functional_requirements=frozenset(
            {"Authentication must be secure."}
        ),
        constraints=frozenset(),
        acceptance_criteria=frozenset(
            {"Valid users can authenticate."}
        ),
        assumptions=frozenset(),
        ambiguities=frozenset(),
        affected_areas=frozenset(
            {"authentication"}
        ),
        confidence=1.0,
    )


def _create_task() -> Task:
    return Task(
        id="task-1",
        description="Implement authentication.",
        category="implementation",
        dependencies=frozenset(),
        affected_areas=frozenset(
            {"authentication"}
        ),
        acceptance_criteria=frozenset(
            {"Valid users can authenticate."}
        ),
    )


def _create_plan() -> EngineeringPlan:
    return EngineeringPlan(
        task_order=("task-1",),
        strategy=(
            "Implement authentication according to the system design.",
        ),
        milestones=(
            "Authentication implementation complete.",
        ),
        required_capabilities=frozenset(),
        risks=frozenset(),
        assumptions=frozenset(),
        validation_strategy=(
            "Run the relevant tests.",
        ),
        confidence=1.0,
    )


def _create_design(
    requirement: Requirement,
    task: Task,
) -> SystemDesign:
    return SystemDesign(
        requirement=requirement,
        tasks=(task,),
        components=(),
        interfaces=(),
        dependencies=(),
        data_flows=(),
        constraints=frozenset(),
        decisions=frozenset(),
        acceptance_criteria=(
            requirement.acceptance_criteria,
        ),
    )


def _create_existing_code() -> CodeStructure:
    return CodeStructure(
        modules=frozenset(),
        classes=frozenset(),
        functions=frozenset(),
        imports=frozenset(),
        calls=frozenset(),
    )


def _create_engineering_decision() -> EngineeringDecision:
    return EngineeringDecision(
        implementation_required=True,
        necessity="Implementation is required.",
        reuse_existing=True,
        use_standard_library=True,
        use_existing_dependency=False,
        new_dependency_required=False,
        abstraction_justified=False,
        optimization_justified=False,
        rationale=(
            "The task requires a new implementation.",
        ),
    )


def test_generation_request_preserves_values():
    requirement = _create_requirement()
    task = _create_task()
    plan = _create_plan()
    design = _create_design(
        requirement,
        task,
    )
    existing_code_value = _create_existing_code()
    engineering_decision_value = _create_engineering_decision()

    request = GenerationRequest(
        task=task,
        design=design,
        plan=plan,
        existing_code=existing_code_value,
        engineering_decision=engineering_decision_value,
    )

    assert request.task == task
    assert request.design == design
    assert request.plan == plan
    assert request.existing_code is existing_code_value
    assert request.engineering_decision is engineering_decision_value


def test_generation_request_is_immutable():
    requirement = _create_requirement()
    task = _create_task()
    plan = _create_plan()
    design = _create_design(
        requirement,
        task,
    )
    existing_code_value = _create_existing_code()
    engineering_decision_value = _create_engineering_decision()

    request = GenerationRequest(
        task=task,
        design=design,
        plan=plan,
        existing_code=existing_code_value,
        engineering_decision=engineering_decision_value,
    )

    try:
        request.task = task
    except Exception:
        pass
    else:
        raise AssertionError(
            "GenerationRequest must be immutable"
        )


def test_generation_request_is_dataclass():
    requirement = _create_requirement()
    task = _create_task()
    plan = _create_plan()
    design = _create_design(
        requirement,
        task,
    )
    existing_code_value = _create_existing_code()
    engineering_decision_value = _create_engineering_decision()

    request = GenerationRequest(
        task=task,
        design=design,
        plan=plan,
        existing_code=existing_code_value,
        engineering_decision=engineering_decision_value,
    )

    assert request.__dataclass_fields__