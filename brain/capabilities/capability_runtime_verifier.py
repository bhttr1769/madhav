from brain.capabilities.models.capability_execution_result import (
    CapabilityExecutionResult,
)
from brain.capabilities.models.capability_verification import (
    CapabilityVerification,
)


class CapabilityRuntimeVerifier:
    def verify(
        self,
        execution_result: CapabilityExecutionResult,
    ) -> CapabilityVerification:
        if not isinstance(
            execution_result,
            CapabilityExecutionResult,
        ):
            raise TypeError(
                "execution_result must be a CapabilityExecutionResult"
            )

        if execution_result.status == "success":
            return CapabilityVerification(
                capability_id=execution_result.capability_id,
                passed=True,
                status="verified",
                evidence=execution_result.output,
                rationale="Capability execution completed successfully.",
            )

        return CapabilityVerification(
            capability_id=execution_result.capability_id,
            passed=False,
            status="failed",
            evidence=execution_result.error,
            rationale="Capability execution failed.",
        )