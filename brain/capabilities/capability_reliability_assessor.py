from brain.capabilities.models.capability_execution_result import (
    CapabilityExecutionResult,
)
from brain.capabilities.models.capability_verification import (
    CapabilityVerification,
)
from brain.capabilities.models.capability_reliability_assessment import (
    CapabilityReliabilityAssessment,
)


class CapabilityReliabilityAssessor:
    def assess(
        self,
        execution_result: CapabilityExecutionResult,
        verification: CapabilityVerification,
    ) -> CapabilityReliabilityAssessment:
        if not isinstance(
            execution_result,
            CapabilityExecutionResult,
        ):
            raise TypeError(
                "execution_result must be a CapabilityExecutionResult"
            )

        if not isinstance(
            verification,
            CapabilityVerification,
        ):
            raise TypeError(
                "verification must be a CapabilityVerification"
            )

        if (
            execution_result.capability_id
            != verification.capability_id
        ):
            raise ValueError(
                "execution result and verification "
                "must reference the same capability"
            )

        if (
            execution_result.status == "success"
            and verification.status == "verified"
        ):
            return CapabilityReliabilityAssessment(
                capability_id=execution_result.capability_id,
                status="reliable",
                evidence={
                    "execution": execution_result,
                    "verification": verification,
                },
                rationale=(
                    "Capability execution succeeded "
                    "and was verified."
                ),
            )

        if (
            execution_result.status == "failed"
            or verification.status == "failed"
        ):
            return CapabilityReliabilityAssessment(
                capability_id=execution_result.capability_id,
                status="unreliable",
                evidence={
                    "execution": execution_result,
                    "verification": verification,
                },
                rationale=(
                    "Capability execution or verification failed."
                ),
            )

        return CapabilityReliabilityAssessment(
            capability_id=execution_result.capability_id,
            status="unknown",
            evidence={
                "execution": execution_result,
                "verification": verification,
            },
            rationale=(
                "Available evidence is insufficient "
                "to establish capability reliability."
            ),
        )