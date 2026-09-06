from brain.code.models.code_structure import CodeStructure
from brain.engineering.design.models.system_design import SystemDesign
from brain.engineering.generation.models.code_change import CodeChange
from brain.engineering.improvement.models.engineering_improvement_request import (
    EngineeringImprovementRequest,
)
from brain.engineering.planning.models.plan import EngineeringPlan
from brain.engineering.requirements.models.requirement import Requirement
from brain.engineering.tasks.models.task import Task


def test_engineering_improvement_request_can_be_constructed():
    requirement = Requirement(
        original_request="Improve the implementation.",
        objective="Improve the implementation safely.",
        functional_requirements=frozenset(
            {"existing behavior must be preserved"}
        ),
        non_functional_requirements=frozenset(
            {"improve engineering quality"}
        ),
        constraints=frozenset(),
        acceptance_criteria=frozenset(
            {"existing behavior remains correct"}
        ),
        assumptions=frozenset(),
        ambiguities=frozenset(),
        affected_areas=frozenset({"brain/example.py"}),
        confidence=1.0,
    )

    task = Task(
        id="task-1",
        description="Improve implementation",
        category="improvement",
        dependencies=frozenset(),
        affected_areas=frozenset({"brain/example.py"}),
        acceptance_criteria=frozenset(
            {"implementation quality is improved"}
        ),
    )

    design = SystemDesign(
        requirement=requirement,
        tasks=(task,),
        components=(),
        interfaces=(),
        dependencies=(),
        data_flows=(),
        constraints=frozenset(),
        decisions=frozenset(),
        acceptance_criteria=frozenset(
            {"existing behavior remains correct"}
        ),
    )

    plan = EngineeringPlan(
        task_order=("task-1",),
        strategy=("improve implementation safely",),
        milestones=("improvement",),
        required_capabilities=frozenset(
            {"testing", "review", "refactoring"}
        ),
        risks=frozenset(),
        assumptions=frozenset(),
        validation_strategy=("run tests",),
        confidence=1.0,
    )

    existing_code = CodeStructure(
        modules=frozenset(),
        classes=frozenset(),
        functions=frozenset(),
        imports=frozenset(),
        calls=frozenset(),
    )

    proposed_changes = (
        CodeChange(
            path="brain/example.py",
            operation="modify",
            content="return value",
        ),
    )

    request = EngineeringImprovementRequest(
        task=task,
        design=design,
        plan=plan,
        existing_code=existing_code,
        proposed_changes=proposed_changes,
    )

    assert request.task is task
    assert request.design is design
    assert request.plan is plan
    assert request.existing_code is existing_code
    assert request.proposed_changes == proposed_changes