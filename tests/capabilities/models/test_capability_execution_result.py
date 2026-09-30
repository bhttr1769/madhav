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


def test_execution_result_is_immutable():
    result = CapabilityExecutionResult(
        capability_id="test.capability",
        output="processed",
    )

    with pytest.raises(FrozenInstanceError):
        result.output = "changed"