import pytest

from brain.capabilities.capability_runtime_verifier import (
    CapabilityRuntimeVerifier,
)
from brain.capabilities.models.capability_execution_result import (
    CapabilityExecutionResult,
)


def test_successful_execution_is_verified():
    verifier = CapabilityRuntimeVerifier()

    result = CapabilityExecutionResult(
        capability_id="test.capability",
        output={"value": 42},
    )

    verification = verifier.verify(result)

    assert verification.capability_id == "test.capability"
    assert verification.passed is True
    assert verification.status == "verified"
    assert verification.evidence == {"value": 42}


def test_failed_execution_is_failed():
    verifier = CapabilityRuntimeVerifier()

    error = RuntimeError("execution failed")

    result = CapabilityExecutionResult(
        capability_id="test.capability",
        output=None,
        status="failed",
        error=error,
    )

    verification = verifier.verify(result)

    assert verification.capability_id == "test.capability"
    assert verification.passed is False
    assert verification.status == "failed"
    assert verification.evidence is error


def test_invalid_execution_result_is_rejected():
    verifier = CapabilityRuntimeVerifier()

    with pytest.raises(TypeError):
        verifier.verify("invalid")