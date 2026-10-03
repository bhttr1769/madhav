import pytest

from brain.capabilities.capability_reliability_assessor import (
    CapabilityReliabilityAssessor,
)
from brain.capabilities.models.capability_execution_result import (
    CapabilityExecutionResult,
)
from brain.capabilities.models.capability_verification import (
    CapabilityVerification,
)


def test_successful_verified_execution_is_reliable():
    assessor = CapabilityReliabilityAssessor()

    execution = CapabilityExecutionResult(
        capability_id="test.capability",
        output="complete",
    )

    verification = CapabilityVerification(
        capability_id="test.capability",
        passed=True,
        status="verified",
        evidence="complete",
        rationale="Execution completed successfully.",
    )

    assessment = assessor.assess(
        execution,
        verification,
    )

    assert assessment.capability_id == "test.capability"
    assert assessment.status == "reliable"


def test_failed_execution_is_unreliable():
    assessor = CapabilityReliabilityAssessor()

    execution = CapabilityExecutionResult(
        capability_id="test.capability",
        output=None,
        status="failed",
        error=RuntimeError("failed"),
    )

    verification = CapabilityVerification(
        capability_id="test.capability",
        passed=False,
        status="failed",
        evidence="failed",
        rationale="Execution failed.",
    )

    assessment = assessor.assess(
        execution,
        verification,
    )

    assert assessment.status == "unreliable"


def test_unknown_verification_is_unknown():
    assessor = CapabilityReliabilityAssessor()

    execution = CapabilityExecutionResult(
        capability_id="test.capability",
        output="result",
    )

    verification = CapabilityVerification(
        capability_id="test.capability",
        passed=False,
        status="unknown",
        evidence=None,
        rationale="Insufficient evidence.",
    )

    assessment = assessor.assess(
        execution,
        verification,
    )

    assert assessment.status == "unknown"


def test_mismatched_capability_ids_are_rejected():
    assessor = CapabilityReliabilityAssessor()

    execution = CapabilityExecutionResult(
        capability_id="test.capability.one",
        output="result",
    )

    verification = CapabilityVerification(
        capability_id="test.capability.two",
        passed=True,
        status="verified",
        evidence="result",
        rationale="Execution verified.",
    )

    with pytest.raises(ValueError):
        assessor.assess(
            execution,
            verification,
        )


def test_invalid_execution_result_is_rejected():
    assessor = CapabilityReliabilityAssessor()

    verification = CapabilityVerification(
        capability_id="test.capability",
        passed=True,
        status="verified",
        evidence="result",
        rationale="Execution verified.",
    )

    with pytest.raises(TypeError):
        assessor.assess(
            "invalid",
            verification,
        )


def test_invalid_verification_is_rejected():
    assessor = CapabilityReliabilityAssessor()

    execution = CapabilityExecutionResult(
        capability_id="test.capability",
        output="result",
    )

    with pytest.raises(TypeError):
        assessor.assess(
            execution,
            "invalid",
        )