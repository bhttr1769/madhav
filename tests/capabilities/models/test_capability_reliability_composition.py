from dataclasses import FrozenInstanceError

import pytest

from brain.capabilities.models.capability_reliability_composition import (
    CapabilityReliabilityComposition,
)


def test_reliability_composition_stores_data():
    composition = object()
    assessments = ()

    result = CapabilityReliabilityComposition(
        composition=composition,
        assessments=assessments,
    )

    assert result.composition is composition
    assert result.assessments == assessments


def test_reliability_composition_is_immutable():
    result = CapabilityReliabilityComposition(
        composition=object(),
        assessments=(),
    )

    with pytest.raises(FrozenInstanceError):
        result.assessments = ()