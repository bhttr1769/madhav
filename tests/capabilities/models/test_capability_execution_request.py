from dataclasses import FrozenInstanceError

import pytest

from brain.capabilities.models.capability_execution_request import (
    CapabilityExecutionRequest,
)


def test_execution_request_stores_data():
    request = CapabilityExecutionRequest(
        capability_id="test.capability",
        input_data="hello",
    )

    assert request.capability_id == "test.capability"
    assert request.input_data == "hello"


def test_execution_request_accepts_arbitrary_input():
    input_data = {
        "query": "hello",
        "limit": 5,
    }

    request = CapabilityExecutionRequest(
        capability_id="test.capability",
        input_data=input_data,
    )

    assert request.input_data is input_data


def test_execution_request_is_immutable():
    request = CapabilityExecutionRequest(
        capability_id="test.capability",
        input_data="hello",
    )

    with pytest.raises(FrozenInstanceError):
        request.capability_id = "changed"