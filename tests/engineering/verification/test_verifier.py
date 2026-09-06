from brain.code.models.code_structure import CodeStructure
from brain.engineering.generation.models.code_change import CodeChange
from brain.engineering.planning.models.plan import EngineeringPlan
from brain.engineering.tasks.models.task import Task
from brain.engineering.verification.models.verification_request import (
    VerificationRequest,
)
from brain.engineering.verification.models.verification_result import (
    VerificationResult,
)
from brain.engineering.verification.verifier import Verifier


class FakeTerminal:
    def __init__(self, result):
        self.result = result
        self.last_command = None

    def execute(self, command):
        self.last_command = command
        return self.result


class FakeCommandResult:
    def __init__(
        self,
        return_code,
        stdout,
        stderr,
    ):
        self.return_code = return_code
        self.stdout = stdout
        self.stderr = stderr


def make_request(
    command="pytest tests/example.py -q",
):
    task = Task(
        id="task-1",
        description="Verify implementation",
        category="verification",
        dependencies=frozenset(),
        affected_areas=frozenset({"module"}),
        acceptance_criteria=frozenset(
            {"verification passes"}
        ),
    )

    plan = EngineeringPlan(
        task_order=("task-1",),
        strategy=("verify implementation",),
        milestones=("verification",),
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

    proposed_changes = (
        CodeChange(
            path="brain/example.py",
            operation="modify",
            content="return value",
        ),
    )

    return VerificationRequest(
        task=task,
        plan=plan,
        existing_code=existing_code,
        proposed_changes=proposed_changes,
        command=command,
    )


def test_verifier_returns_passed_result():
    terminal = FakeTerminal(
        FakeCommandResult(
            return_code=0,
            stdout="1 passed",
            stderr="",
        )
    )

    verifier = Verifier(terminal)

    result = verifier.verify(
        make_request()
    )

    assert isinstance(result, VerificationResult)
    assert result.passed is True
    assert result.return_code == 0
    assert result.stdout == "1 passed"
    assert result.stderr == ""


def test_verifier_returns_failed_result():
    terminal = FakeTerminal(
        FakeCommandResult(
            return_code=1,
            stdout="",
            stderr="1 failed",
        )
    )

    verifier = Verifier(terminal)

    result = verifier.verify(
        make_request()
    )

    assert isinstance(result, VerificationResult)
    assert result.passed is False
    assert result.return_code == 1
    assert result.stdout == ""
    assert result.stderr == "1 failed"


def test_verifier_builds_command_from_request():
    terminal = FakeTerminal(
        FakeCommandResult(
            return_code=0,
            stdout="success",
            stderr="",
        )
    )

    verifier = Verifier(terminal)

    verifier.verify(
        make_request("pytest tests/unit -q")
    )

    assert terminal.last_command.value == (
        "pytest tests/unit -q"
    )


def test_verifier_rejects_invalid_request():
    verifier = Verifier(
        FakeTerminal(
            FakeCommandResult(
                return_code=0,
                stdout="",
                stderr="",
            )
        )
    )

    try:
        verifier.verify(None)
    except TypeError:
        pass
    else:
        raise AssertionError(
            "Verifier should reject invalid request"
        )


def test_verifier_preserves_stdout_and_stderr():
    terminal = FakeTerminal(
        FakeCommandResult(
            return_code=2,
            stdout="partial output",
            stderr="unexpected failure",
        )
    )

    verifier = Verifier(terminal)

    result = verifier.verify(
        make_request()
    )

    assert result.stdout == "partial output"
    assert result.stderr == (
        "unexpected failure"
    )

def test_verifier_and_interpreter_form_complete_success_path():
    from brain.engineering.verification.verification_interpreter import (
        VerificationInterpreter,
    )

    terminal = FakeTerminal(
        FakeCommandResult(
            return_code=0,
            stdout="3 passed",
            stderr="",
        )
    )

    verifier = Verifier(terminal)

    result = verifier.verify(
        make_request()
    )

    assessment = VerificationInterpreter.interpret(
        result
    )

    assert assessment.passed is True
    assert assessment.status == "passed"
    assert assessment.failure_output == ""


def test_verifier_and_interpreter_form_complete_failure_path():
    from brain.engineering.verification.verification_interpreter import (
        VerificationInterpreter,
    )

    terminal = FakeTerminal(
        FakeCommandResult(
            return_code=1,
            stdout="1 failed",
            stderr="AssertionError: expected 5",
        )
    )

    verifier = Verifier(terminal)

    result = verifier.verify(
        make_request()
    )

    assessment = VerificationInterpreter.interpret(
        result
    )

    assert assessment.passed is False
    assert assessment.status == "failed"
    assert assessment.failure_output == (
        "1 failed\nAssertionError: expected 5"
    )


def test_verification_preserves_command_execution_boundary():
    terminal = FakeTerminal(
        FakeCommandResult(
            return_code=0,
            stdout="success",
            stderr="",
        )
    )

    verifier = Verifier(terminal)

    result = verifier.verify(
        make_request("python -m pytest tests/example.py -q")
    )

    assert terminal.last_command.value == (
        "python -m pytest tests/example.py -q"
    )
    assert result.passed is True


def test_verification_does_not_modify_proposed_changes():
    request = make_request()

    original_changes = request.proposed_changes

    terminal = FakeTerminal(
        FakeCommandResult(
            return_code=0,
            stdout="success",
            stderr="",
        )
    )

    verifier = Verifier(terminal)

    verifier.verify(request)

    assert request.proposed_changes == original_changes