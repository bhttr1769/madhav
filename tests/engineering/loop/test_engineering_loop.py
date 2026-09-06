import pytest

from brain.code.models.code_structure import CodeStructure
from brain.engineering.design.models.system_design import SystemDesign
from brain.engineering.generation.models.code_change import CodeChange
from brain.engineering.loop.engineering_loop import EngineeringLoop
from brain.engineering.loop.models.engineering_loop_request import (
    EngineeringLoopRequest,
)
from brain.engineering.loop.models.engineering_loop_result import (
    EngineeringLoopResult,
)
from brain.engineering.planning.models.plan import EngineeringPlan
from brain.engineering.requirements.models.requirement import Requirement
from brain.engineering.tasks.models.task import Task
from brain.engineering.verification.models.verification_assessment import (
    VerificationAssessment,
)
from brain.engineering.verification.models.verification_result import (
    VerificationResult,
)
from brain.engineering.loop.local_change_applier import (
    LocalChangeApplier,
)


class FakeVerifier:
    def __init__(self, results):
        self.results = list(results)
        self.calls = []

    def verify(self, request):
        self.calls.append(request)
        return self.results.pop(0)


class FakeDebugger:
    def __init__(self, changes):
        self.changes = changes
        self.calls = []

    def debug(self, request):
        self.calls.append(request)

        class Result:
            def __init__(self, changes):
                self.changes = changes

        return Result(self.changes)


class FakeRefactorer:
    def __init__(self, changes):
        self.changes = changes
        self.calls = []

    def refactor(self, request):
        self.calls.append(request)

        class Result:
            def __init__(self, changes):
                self.changes = changes

        return Result(self.changes)


class FakeImprover:
    def __init__(self, changes):
        self.changes = changes
        self.calls = []

    def improve(self, request):
        self.calls.append(request)

        class Result:
            def __init__(self, changes):
                self.changes = changes

        return Result(self.changes)


class FakeChangeApplier:
    def __init__(self):
        self.calls = []

    def apply(self, changes):
        self.calls.append(changes)


class FakeInterpreter:
    @staticmethod
    def interpret(result):
        if result.passed:
            return VerificationAssessment(
                passed=True,
                status="passed",
                summary="Verification passed.",
                failure_output="",
            )

        return VerificationAssessment(
            passed=False,
            status="failed",
            summary="Verification failed.",
            failure_output="failure output",
        )


@pytest.fixture
def loop_request():
    requirement = Requirement(
        original_request="Implement requested behavior.",
        objective="Implement requested behavior correctly.",
        functional_requirements=frozenset(
            {"requested behavior must work"}
        ),
        non_functional_requirements=frozenset(),
        constraints=frozenset(),
        acceptance_criteria=frozenset(
            {"verification passes"}
        ),
        assumptions=frozenset(),
        ambiguities=frozenset(),
        affected_areas=frozenset(
            {"brain/example.py"}
        ),
        confidence=1.0,
    )

    task = Task(
        id="task-1",
        description="Implement requested behavior",
        category="implementation",
        dependencies=frozenset(),
        affected_areas=frozenset(
            {"brain/example.py"}
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
        strategy=("implement behavior",),
        milestones=("implementation",),
        required_capabilities=frozenset(
            {"verification"}
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

    initial_change = CodeChange(
        path="brain/example.py",
        operation="modify",
        content="return value",
    )

    return EngineeringLoopRequest(
        task=task,
        design=design,
        plan=plan,
        existing_code=existing_code,
        proposed_changes=(initial_change,),
        verification_command="pytest tests/example.py -q",
        max_iterations=2,
    )


def test_loop_stops_immediately_when_verification_passes(
    loop_request,
):
    verifier = FakeVerifier(
        [
            VerificationResult(
                passed=True,
                return_code=0,
                stdout="1 passed",
                stderr="",
            )
        ]
    )

    debugger = FakeDebugger(())
    refactorer = FakeRefactorer(())
    improver = FakeImprover(())
    applier = FakeChangeApplier()

    loop = EngineeringLoop(
        verifier=verifier,
        debugger=debugger,
        refactorer=refactorer,
        improver=improver,
        change_applier=applier,
        interpreter=FakeInterpreter,
    )

    result = loop.execute(loop_request)

    assert isinstance(
        result,
        EngineeringLoopResult,
    )
    assert result.passed is True
    assert result.termination_reason == (
        "verification_passed"
    )
    assert len(result.iterations) == 1

    assert debugger.calls == []
    assert refactorer.calls == []
    assert improver.calls == []
    assert applier.calls == []


def test_loop_runs_improvement_pipeline_after_failure(
    loop_request,
):
    debug_change = CodeChange(
        path="brain/debug.py",
        operation="modify",
        content="debug fix",
    )

    refactor_change = CodeChange(
        path="brain/refactor.py",
        operation="modify",
        content="refactor",
    )

    improvement_change = CodeChange(
        path="brain/improve.py",
        operation="modify",
        content="improvement",
    )

    verifier = FakeVerifier(
        [
            VerificationResult(
                passed=False,
                return_code=1,
                stdout="",
                stderr="failure",
            ),
            VerificationResult(
                passed=True,
                return_code=0,
                stdout="2 passed",
                stderr="",
            ),
        ]
    )

    debugger = FakeDebugger(
        (debug_change,)
    )
    refactorer = FakeRefactorer(
        (refactor_change,)
    )
    improver = FakeImprover(
        (improvement_change,)
    )
    applier = FakeChangeApplier()

    loop = EngineeringLoop(
        verifier=verifier,
        debugger=debugger,
        refactorer=refactorer,
        improver=improver,
        change_applier=applier,
        interpreter=FakeInterpreter,
    )

    result = loop.execute(loop_request)

    assert result.passed is True
    assert result.termination_reason == (
        "verification_passed"
    )

    assert result.changes == (
        loop_request.proposed_changes[0],
        debug_change,
        refactor_change,
        improvement_change,
    )

    assert len(debugger.calls) == 1
    assert len(refactorer.calls) == 1
    assert len(improver.calls) == 1

    assert applier.calls == [
        (debug_change,),
        (refactor_change,),
        (improvement_change,),
    ]


def test_loop_passes_accumulated_changes_to_next_verification(
    loop_request,
):
    debug_change = CodeChange(
        path="brain/debug.py",
        operation="modify",
        content="debug fix",
    )

    verifier = FakeVerifier(
        [
            VerificationResult(
                passed=False,
                return_code=1,
                stdout="",
                stderr="failure",
            ),
            VerificationResult(
                passed=True,
                return_code=0,
                stdout="success",
                stderr="",
            ),
        ]
    )

    loop = EngineeringLoop(
        verifier=verifier,
        debugger=FakeDebugger(
            (debug_change,)
        ),
        refactorer=FakeRefactorer(()),
        improver=FakeImprover(()),
        change_applier=FakeChangeApplier(),
        interpreter=FakeInterpreter,
    )

    loop.execute(loop_request)

    assert verifier.calls[0].proposed_changes == (
        loop_request.proposed_changes[0],
    )

    assert verifier.calls[1].proposed_changes == (
        loop_request.proposed_changes[0],
        debug_change,
    )


def test_loop_passes_failure_context_to_debugger(
    loop_request,
):
    verifier = FakeVerifier(
        [
            VerificationResult(
                passed=False,
                return_code=1,
                stdout="stdout failure",
                stderr="stderr failure",
            ),
            VerificationResult(
                passed=True,
                return_code=0,
                stdout="success",
                stderr="",
            ),
        ]
    )

    debugger = FakeDebugger(())

    loop = EngineeringLoop(
        verifier=verifier,
        debugger=debugger,
        refactorer=FakeRefactorer(()),
        improver=FakeImprover(()),
        change_applier=FakeChangeApplier(),
        interpreter=FakeInterpreter,
    )

    loop.execute(loop_request)

    debug_request = debugger.calls[0]

    assert debug_request.error_message == (
        "Verification failed."
    )
    assert debug_request.traceback == (
        "failure output"
    )


def test_loop_stops_after_max_iterations(
    loop_request,
):
    verifier = FakeVerifier(
        [
            VerificationResult(
                passed=False,
                return_code=1,
                stdout="failure 1",
                stderr="",
            ),
            VerificationResult(
                passed=False,
                return_code=1,
                stdout="failure 2",
                stderr="",
            ),
        ]
    )

    loop = EngineeringLoop(
        verifier=verifier,
        debugger=FakeDebugger(()),
        refactorer=FakeRefactorer(()),
        improver=FakeImprover(()),
        change_applier=FakeChangeApplier(),
        interpreter=FakeInterpreter,
    )

    result = loop.execute(loop_request)

    assert result.passed is False
    assert result.termination_reason == (
        "max_iterations_reached"
    )
    assert len(result.iterations) == 2


def test_loop_rejects_invalid_request():
    loop = EngineeringLoop(
        verifier=FakeVerifier([]),
        debugger=FakeDebugger(()),
        refactorer=FakeRefactorer(()),
        improver=FakeImprover(()),
        change_applier=FakeChangeApplier(),
    )

    with pytest.raises(TypeError):
        loop.execute(None)


def test_loop_rejects_invalid_iteration_limit(
    loop_request,
):
    invalid_request = EngineeringLoopRequest(
        task=loop_request.task,
        design=loop_request.design,
        plan=loop_request.plan,
        existing_code=loop_request.existing_code,
        proposed_changes=loop_request.proposed_changes,
        verification_command=loop_request.verification_command,
        max_iterations=0,
    )

    loop = EngineeringLoop(
        verifier=FakeVerifier([]),
        debugger=FakeDebugger(()),
        refactorer=FakeRefactorer(()),
        improver=FakeImprover(()),
        change_applier=FakeChangeApplier(),
    )

    with pytest.raises(ValueError):
        loop.execute(invalid_request)


def test_loop_does_not_apply_empty_change_sets(
    loop_request,
):
    verifier = FakeVerifier(
        [
            VerificationResult(
                passed=False,
                return_code=1,
                stdout="failure",
                stderr="",
            ),
            VerificationResult(
                passed=True,
                return_code=0,
                stdout="success",
                stderr="",
            ),
        ]
    )

    applier = FakeChangeApplier()

    loop = EngineeringLoop(
        verifier=verifier,
        debugger=FakeDebugger(()),
        refactorer=FakeRefactorer(()),
        improver=FakeImprover(()),
        change_applier=applier,
        interpreter=FakeInterpreter,
    )

    result = loop.execute(loop_request)

    assert result.passed is True
    assert applier.calls == []

def test_loop_uses_local_change_applier_by_default():
    loop = EngineeringLoop(
        verifier=object(),
        debugger=object(),
        refactorer=object(),
        improver=object(),
    )

    assert isinstance(
        loop._change_applier,
        LocalChangeApplier,
    )