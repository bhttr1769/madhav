from brain.engineering.verification.models.verification_assessment import (
    VerificationAssessment,
)
from brain.engineering.verification.models.verification_result import (
    VerificationResult,
)


class VerificationInterpreter:
    _PASSED_STATUS = "passed"
    _FAILED_STATUS = "failed"

    @classmethod
    def interpret(
        cls,
        result: VerificationResult,
    ) -> VerificationAssessment:
        if not isinstance(result, VerificationResult):
            raise TypeError(
                "result must be a VerificationResult"
            )

        if result.passed:
            return VerificationAssessment(
                passed=True,
                status=cls._PASSED_STATUS,
                summary=(
                    "Verification completed successfully."
                ),
                failure_output="",
            )

        failure_output = cls._build_failure_output(
            result
        )

        return VerificationAssessment(
            passed=False,
            status=cls._FAILED_STATUS,
            summary=(
                "Verification failed with a "
                f"non-zero return code ({result.return_code})."
            ),
            failure_output=failure_output,
        )

    @staticmethod
    def _build_failure_output(
        result: VerificationResult,
    ) -> str:
        parts = []

        if result.stdout.strip():
            parts.append(result.stdout.strip())

        if result.stderr.strip():
            parts.append(result.stderr.strip())

        return "\n".join(parts)