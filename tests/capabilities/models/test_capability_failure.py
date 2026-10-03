from dataclasses import FrozenInstanceError

import pytest

from brain.capabilities.models.capability_failure import (
    CapabilityFailure,
)


def test_execution_failure():
    error = RuntimeError("execution failed")

    failure = CapabilityFailure(
        capability_id="test.capability",
        category="execution",
        evidence=error,
        rationale="The capability implementation raised an exception.",
    )

    assert failure.capability_id == "test.capability"
    assert failure.category == "execution"
    assert failure.evidence is error
    assert (
        failure.rationale
        == "The capability implementation raised an exception."
    )


@pytest.mark.parametrize(
    "category",
    [
        "execution",
        "validation",
        "dependency",
        "timeout",
        "unknown",
    ],
)
def test_supported_failure_categories(category):
    failure = CapabilityFailure(
        capability_id="test.capability",
        category=category,
        evidence="evidence",
        rationale="Failure was classified.",
    )

    assert failure.category == category


@pytest.mark.parametrize(
    "category",
    ["", "invalid", None, 42],
)
def test_invalid_failure_category(category):
    with pytest.raises((TypeError, ValueError)):
        CapabilityFailure(
            capability_id="test.capability",
            category=category,
            evidence="evidence",
            rationale="Failure was classified.",
        )


@pytest.mark.parametrize(
    "capability_id",
    ["", "   ", None, 42],
)
def test_invalid_capability_id(capability_id):
    with pytest.raises((TypeError, ValueError)):
        CapabilityFailure(
            capability_id=capability_id,
            category="execution",
            evidence="evidence",
            rationale="Failure was classified.",
        )


def test_rationale_must_not_be_empty():
    with pytest.raises(ValueError):
        CapabilityFailure(
            capability_id="test.capability",
            category="execution",
            evidence="evidence",
            rationale="   ",
        )


def test_failure_is_immutable():
    failure = CapabilityFailure(
        capability_id="test.capability",
        category="execution",
        evidence="error",
        rationale="Execution failed.",
    )

    with pytest.raises(FrozenInstanceError):
        failure.category = "timeout"