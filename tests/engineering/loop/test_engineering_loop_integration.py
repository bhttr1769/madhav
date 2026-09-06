from pathlib import Path

from brain.code.models.code_structure import CodeStructure
from brain.engineering.debugging.models.debugging_result import (
    DebuggingResult,
)
from brain.engineering.design.models.system_design import SystemDesign
from brain.engineering.generation.models.code_change import CodeChange
from brain.engineering.improvement.models.engineering_improvement_result import (
    EngineeringImprovementResult,
)
from brain.engineering.loop.engineering_loop import EngineeringLoop
from brain.engineering.loop.local_change_applier import (
    LocalChangeApplier,
)
from brain.engineering.loop.models.engineering_loop_request import (
    EngineeringLoopRequest,
)
from brain.engineering.planning.models.plan import EngineeringPlan
from brain.engineering.refactoring.models.refactoring_result import (
    RefactoringResult,
)
from brain.engineering.requirements.models.requirement import Requirement
from brain.engineering.tasks.models.task import Task
from brain.engineering.verification.verifier import Verifier


class FakeDebugger:
    def __init__(self, changes):
        self.changes = changes
        self.calls = []

    def debug(self, request):
        self.calls.append(request)

        return DebuggingResult(
            changes=self.changes,
            diagnosis="Fixed failing implementation.",
        )


class FakeRefactorer:
    def __init__(self, changes=()):
        self.changes = changes
        self.calls = []

    def refactor(self, request):
        self.calls.append(request)

        return RefactoringResult(
            changes=self.changes,
            rationale="No additional refactoring required.",
        )


class FakeImprover:
    def __init__(self, changes=()):
        self.changes = changes
        self.calls = []

    def improve(self, request):
        self.calls.append(request)

        return EngineeringImprovementResult(
            changes=self.changes,
            rationale=(
                "No additional improvement required.",
            ),
        )


def test_engineering_loop_applies_real_changes_and_verifies(
    tmp_path: Path,
):
    target = tmp_path / "target.txt"

    target.write_text(
        "fail",
        encoding="utf-8",
    )

    debug_change = CodeChange(
        path="target.txt",
        operation="modify",
        content="pass",
    )

    request = _build_request(
        target=target,
        proposed_changes=(
            CodeChange(
                path="target.txt",
                operation="modify",
                content="pass",
            ),
        ),
    )

    debugger = FakeDebugger(
        (debug_change,),
    )

    refactorer = FakeRefactorer()
    improver = FakeImprover()

    loop = EngineeringLoop(
        verifier=Verifier(),
        debugger=debugger,
        refactorer=refactorer,
        improver=improver,
        change_applier=LocalChangeApplier(
            tmp_path,
        ),
    )

    result = loop.execute(request)

    assert result.passed is True
    assert result.termination_reason == (
        "verification_passed"
    )

    assert len(result.iterations) == 2

    assert result.iterations[0].passed is False
    assert result.iterations[1].passed is True

    assert result.changes == (
        request.proposed_changes[0],
        debug_change,
    )

    assert len(debugger.calls) == 1
    assert len(refactorer.calls) == 1
    assert len(improver.calls) == 1

    assert target.read_text(
        encoding="utf-8",
    ) == "pass"


def _build_request(
    target: Path,
    proposed_changes: tuple[CodeChange, ...],
) -> EngineeringLoopRequest:
    requirement = Requirement(
        original_request="Fix the failing implementation.",
        objective="Make the implementation pass verification.",
        functional_requirements=frozenset(
            {"implementation must pass verification"}
        ),
        non_functional_requirements=frozenset(),
        constraints=frozenset(),
        acceptance_criteria=frozenset(
            {"verification passes"}
        ),
        assumptions=frozenset(),
        ambiguities=frozenset(),
        affected_areas=frozenset(
            {"target.txt"}
        ),
        confidence=1.0,
    )

    task = Task(
        id="task-1",
        description="Fix the failing implementation.",
        category="bugfix",
        dependencies=frozenset(),
        affected_areas=frozenset(
            {"target.txt"}
        ),
        acceptance_criteria=frozenset(
            {"verification passes"}
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
            {"verification passes"}
        ),
    )

    plan = EngineeringPlan(
        task_order=("task-1",),
        strategy=("fix failing implementation",),
        milestones=("implementation",),
        required_capabilities=frozenset(
            {"verification"}
        ),
        risks=frozenset(),
        assumptions=frozenset(),
        validation_strategy=("run verification",),
        confidence=1.0,
    )

    existing_code = CodeStructure(
        modules=frozenset(),
        classes=frozenset(),
        functions=frozenset(),
        imports=frozenset(),
        calls=frozenset(),
    )

    verification_command = (
        "python -c "
        "\"from pathlib import Path; "
        f"assert Path(r'{target}').read_text(encoding='utf-8') == 'pass'\""
    )

    return EngineeringLoopRequest(
        task=task,
        design=design,
        plan=plan,
        existing_code=existing_code,
        proposed_changes=proposed_changes,
        verification_command=verification_command,
        max_iterations=2,
    )