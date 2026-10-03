from dataclasses import FrozenInstanceError

import pytest

from brain.capabilities.models.capability_execution_result import (
    CapabilityExecutionResult,
)


def test_execution_result_stores_data():
    result = CapabilityExecutionResult(
        capability_id="test.capability",
        output="processed",
    )

    assert result.capability_id == "test.capability"
    assert result.output == "processed"
    assert result.status == "success"
    assert result.error is None


def test_execution_result_accepts_arbitrary_output():
    output = {
        "value": 42,
        "status": "complete",
    }

    result = CapabilityExecutionResult(
        capability_id="test.capability",
        output=output,
    )

    assert result.output is output


def test_failed_execution_result_stores_error():
    error = RuntimeError("execution failed")

    result = CapabilityExecutionResult(
        capability_id="test.capability",
        output=None,
        status="failed",
        error=error,
    )

    assert result.status == "failed"
    assert result.error is error


def test_execution_result_is_immutable():
    result = CapabilityExecutionResult(
        capability_id="test.capability",
        output="processed",
    )

    with pytest.raises(FrozenInstanceError):
        result.output = "changed"


@pytest.mark.parametrize(
    "capability_id",
    ["", "   ", None, 42],
)
def test_invalid_capability_id(capability_id):
    with pytest.raises((TypeError, ValueError)):
        CapabilityExecutionResult(
            capability_id=capability_id,
            output="processed",
        )


@pytest.mark.parametrize(
    "status",
    ["invalid", "", None, 42],
)
def test_invalid_status(status):
    with pytest.raises((TypeError, ValueError)):
        CapabilityExecutionResult(
            capability_id="test.capability",
            output="processed",
            status=status,
        )


def test_success_cannot_contain_error():
    with pytest.raises(ValueError):
        CapabilityExecutionResult(
            capability_id="test.capability",
            output="processed",
            status="success",
            error=RuntimeError("unexpected error"),
        )


def test_failed_execution_requires_error():
    with pytest.raises(ValueError):
        CapabilityExecutionResult(
            capability_id="test.capability",
            output=None,
            status="failed",
        )