from brain.engineering.verification.models.verification_result import (
    VerificationResult,
)


def test_verification_result_can_be_constructed():
    result = VerificationResult(
        passed=True,
        return_code=0,
        stdout="1 passed",
        stderr="",
    )

    assert result.passed is True
    assert result.return_code == 0
    assert result.stdout == "1 passed"
    assert result.stderr == ""