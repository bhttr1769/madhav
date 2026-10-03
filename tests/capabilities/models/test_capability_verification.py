from dataclasses import FrozenInstanceError

import pytest

from brain.capabilities.models.capability_verification import (
    CapabilityVerification,
)


def test_verified_capability_verification():
    verification = CapabilityVerification(
        capability_id="test.capability",
        passed=True,
        status="verified",
        evidence={"output": "complete"},
        rationale="Expected execution evidence was observed.",
    )

    assert verification.capability_id == "test.capability"
    assert verification.passed is True
    assert verification.status == "verified"
    assert verification.evidence == {"output": "complete"}
    assert (
        verification.rationale
        == "Expected execution evidence was observed."
    )


def test_failed_capability_verification():
    verification = CapabilityVerification(
        capability_id="test.capability",
        passed=False,
        status="failed",
        evidence={"error": "execution failed"},
        rationale="Execution evidence indicates failure.",
    )

    assert verification.passed is False
    assert verification.status == "failed"


def test_unknown_capability_verification():
    verification = CapabilityVerification(
        capability_id="test.capability",
        passed=False,
        status="unknown",
        evidence=None,
        rationale="Insufficient evidence to verify execution.",
    )

    assert verification.passed is False
    assert verification.status == "unknown"


def test_capability_verification_is_immutable():
    verification = CapabilityVerification(
        capability_id="test.capability",
        passed=True,
        status="verified",
        evidence="complete",
        rationale="Execution verified.",
    )

    with pytest.raises(FrozenInstanceError):
        verification.passed = False


@pytest.mark.parametrize(
    "capability_id",
    ["", "   ", None, 42],
)
def test_invalid_capability_id(capability_id):
    with pytest.raises((TypeError, ValueError)):
        CapabilityVerification(
            capability_id=capability_id,
            passed=True,
            status="verified",
            evidence="complete",
            rationale="Execution verified.",
        )


@pytest.mark.parametrize(
    "status",
    ["invalid", "", None, 42],
)
def test_invalid_status(status):
    with pytest.raises((TypeError, ValueError)):
        CapabilityVerification(
            capability_id="test.capability",
            passed=True,
            status=status,
            evidence="complete",
            rationale="Execution verified.",
        )


def test_verified_requires_passed():
    with pytest.raises(ValueError):
        CapabilityVerification(
            capability_id="test.capability",
            passed=False,
            status="verified",
            evidence="complete",
            rationale="Execution verified.",
        )


def test_failed_requires_not_passed():
    with pytest.raises(ValueError):
        CapabilityVerification(
            capability_id="test.capability",
            passed=True,
            status="failed",
            evidence="failure",
            rationale="Execution failed.",
        )


def test_unknown_requires_not_passed():
    with pytest.raises(ValueError):
        CapabilityVerification(
            capability_id="test.capability",
            passed=True,
            status="unknown",
            evidence=None,
            rationale="Evidence is insufficient.",
        )


def test_rationale_must_not_be_empty():
    with pytest.raises(ValueError):
        CapabilityVerification(
            capability_id="test.capability",
            passed=True,
            status="verified",
            evidence="complete",
            rationale="   ",
        )