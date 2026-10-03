from dataclasses import FrozenInstanceError

import pytest

from brain.capabilities.models.capability_reliability_assessment import (
    CapabilityReliabilityAssessment,
)


@pytest.mark.parametrize(
    "status",
    [
        "reliable",
        "unreliable",
        "unknown",
    ],
)
def test_supported_reliability_status(status):
    assessment = CapabilityReliabilityAssessment(
        capability_id="test.capability",
        status=status,
        evidence="evidence",
        rationale="Assessment was established.",
    )

    assert assessment.status == status


@pytest.mark.parametrize(
    "status",
    ["", "invalid", None, 42],
)
def test_invalid_reliability_status(status):
    with pytest.raises((TypeError, ValueError)):
        CapabilityReliabilityAssessment(
            capability_id="test.capability",
            status=status,
            evidence="evidence",
            rationale="Assessment was established.",
        )


@pytest.mark.parametrize(
    "capability_id",
    ["", "   ", None, 42],
)
def test_invalid_capability_id(capability_id):
    with pytest.raises((TypeError, ValueError)):
        CapabilityReliabilityAssessment(
            capability_id=capability_id,
            status="reliable",
            evidence="evidence",
            rationale="Assessment was established.",
        )


def test_rationale_must_not_be_empty():
    with pytest.raises(ValueError):
        CapabilityReliabilityAssessment(
            capability_id="test.capability",
            status="reliable",
            evidence="evidence",
            rationale="   ",
        )


def test_assessment_is_immutable():
    assessment = CapabilityReliabilityAssessment(
        capability_id="test.capability",
        status="reliable",
        evidence="evidence",
        rationale="Assessment was established.",
    )

    with pytest.raises(FrozenInstanceError):
        assessment.status = "unknown"