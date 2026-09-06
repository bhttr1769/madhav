import pytest

from brain.engineering.verification.models.verification_assessment import (
    VerificationAssessment,
)
from brain.engineering.verification.models.verification_result import (
    VerificationResult,
)
from brain.engineering.verification.verification_interpreter import (
    VerificationInterpreter,
)


def test_interpreter_returns_passed_assessment():
    result = VerificationResult(
        passed=True,
        return_code=0,
        stdout="5 passed",
        stderr="",
    )

    assessment = VerificationInterpreter.interpret(
        result
    )

    assert isinstance(
        assessment,
        VerificationAssessment,
    )
    assert assessment.passed is True
    assert assessment.status == "passed"
    assert assessment.summary == (
        "Verification completed successfully."
    )
    assert assessment.failure_output == ""


def test_interpreter_returns_failed_assessment():
    result = VerificationResult(
        passed=False,
        return_code=1,
        stdout="1 failed",
        stderr="AssertionError",
    )

    assessment = VerificationInterpreter.interpret(
        result
    )

    assert isinstance(
        assessment,
        VerificationAssessment,
    )
    assert assessment.passed is False
    assert assessment.status == "failed"
    assert assessment.summary == (
        "Verification failed with a "
        "non-zero return code (1)."
    )
    assert assessment.failure_output == (
        "1 failed\nAssertionError"
    )


def test_interpreter_preserves_stdout_when_stderr_empty():
    result = VerificationResult(
        passed=False,
        return_code=1,
        stdout="test failure",
        stderr="",
    )

    assessment = VerificationInterpreter.interpret(
        result
    )

    assert assessment.failure_output == (
        "test failure"
    )


def test_interpreter_preserves_stderr_when_stdout_empty():
    result = VerificationResult(
        passed=False,
        return_code=1,
        stdout="",
        stderr="command failed",
    )

    assessment = VerificationInterpreter.interpret(
        result
    )

    assert assessment.failure_output == (
        "command failed"
    )


def test_interpreter_returns_empty_failure_output_when_both_are_empty():
    result = VerificationResult(
        passed=False,
        return_code=1,
        stdout="",
        stderr="",
    )

    assessment = VerificationInterpreter.interpret(
        result
    )

    assert assessment.failure_output == ""


def test_interpreter_rejects_invalid_result():
    with pytest.raises(TypeError):
        VerificationInterpreter.interpret(None)


def test_interpreter_does_not_modify_result():
    result = VerificationResult(
        passed=False,
        return_code=2,
        stdout="stdout",
        stderr="stderr",
    )

    VerificationInterpreter.interpret(result)

    assert result.passed is False
    assert result.return_code == 2
    assert result.stdout == "stdout"
    assert result.stderr == "stderr"