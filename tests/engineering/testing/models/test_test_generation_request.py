from brain.code.models.code_structure import CodeStructure

from brain.engineering.design.models.system_design import (
    SystemDesign,
)

from brain.engineering.generation.models.code_change import (
    CodeChange,
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

from brain.engineering.testing.models.test_generation_request import (
    TestGenerationRequest as GenerationRequest,
)


def task() -> Task:
    return Task(
        id="task-1",
        description="Add a health endpoint.",
        category="backend",
        dependencies=frozenset(),
        affected_areas=frozenset({"api"}),
        acceptance_criteria=frozenset(
            {
                "Health endpoint returns HTTP 200.",
                "Health endpoint reports service status.",
            }
        ),
    )


def requirement() -> Requirement:
    return Requirement(
        original_request="Add a health endpoint.",
        objective="Expose the service health status through an API endpoint.",
        functional_requirements=frozenset(
            {
                "Provide a health endpoint.",
            }
        ),
        non_functional_requirements=frozenset(),
        constraints=frozenset(),
        acceptance_criteria=frozenset(
            {
                "Health endpoint returns HTTP 200.",
            }
        ),
        assumptions=frozenset(),
        ambiguities=frozenset(),
        affected_areas=frozenset({"api"}),
        confidence=0.9,
    )


def design() -> SystemDesign:
    return SystemDesign(
        requirement=requirement(),
        tasks=(task(),),
        components=(),
        interfaces=(),
        dependencies=(),
        data_flows=(),
        constraints=frozenset(),
        decisions=frozenset(),
        acceptance_criteria=frozenset(
            {
                "Health endpoint returns HTTP 200.",
            }
        ),
    )


def plan() -> EngineeringPlan:
    return EngineeringPlan(
        task_order=("task-1",),
        strategy=("Implement the health endpoint.",),
        milestones=("Health endpoint implemented.",),
        required_capabilities=frozenset({"backend"}),
        risks=frozenset(),
        assumptions=frozenset(),
        validation_strategy=("Verify the endpoint returns HTTP 200.",),
        confidence=0.9,
    )


def existing_code() -> CodeStructure:
    return CodeStructure(
        modules=frozenset(),
        classes=frozenset(),
        functions=frozenset(),
        imports=frozenset(),
        calls=frozenset(),
    )


def proposed_changes() -> tuple[CodeChange, ...]:
    return (
        CodeChange(
            path="app/health.py",
            operation="create",
            content="def health():\n    return {'status': 'ok'}\n",
        ),
    )


def test_test_generation_request_is_constructed_with_complete_context():

    request = GenerationRequest(
        task=task(),
        design=design(),
        plan=plan(),
        existing_code=existing_code(),
        proposed_changes=proposed_changes(),
    )

    assert request.task == task()
    assert request.design == design()
    assert request.plan == plan()
    assert request.existing_code == existing_code()
    assert request.proposed_changes == proposed_changes()