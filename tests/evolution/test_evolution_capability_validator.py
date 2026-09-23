import pytest

from brain.capabilities.models.capability_descriptor import (
    CapabilityDescriptor,
)
from brain.evolution.evolution_capability_validator import (
    EvolutionCapabilityValidator,
)
from brain.evolution.models.evolution_validation_check import (
    EvolutionValidationCheck,
)


def _capability(
    capability_id="web_research",
):
    return CapabilityDescriptor(
        id=capability_id,
        name="Web Research",
        description="Performs web research.",
        version="1.0.0",
        entry_point=(
            "brain.research.WebResearchCapability"
        ),
        dependencies=frozenset(),
    )


def test_validator_accepts_matching_capability():
    validator = EvolutionCapabilityValidator()

    result = validator.validate(
        capabilities=(
            _capability(),
        ),
        requested_capability="web_research",
    )

    assert isinstance(
        result,
        EvolutionValidationCheck,
    )

    assert result.name == (
        "capability_validation"
    )

    assert result.passed is True


def test_validator_rejects_no_capability():
    validator = EvolutionCapabilityValidator()

    result = validator.validate(
        capabilities=(),
        requested_capability="web_research",
    )

    assert result.passed is False

    assert result.reason == (
        "no capability descriptor was discovered"
    )


def test_validator_rejects_multiple_capabilities():
    validator = EvolutionCapabilityValidator()

    result = validator.validate(
        capabilities=(
            _capability("web_research"),
            _capability("another_capability"),
        ),
        requested_capability="web_research",
    )

    assert result.passed is False

    assert result.reason == (
        "exactly one capability descriptor "
        "must be discovered"
    )


def test_validator_rejects_non_descriptor():
    validator = EvolutionCapabilityValidator()

    with pytest.raises(
        TypeError,
        match="CapabilityDescriptor instances",
    ):
        validator.validate(
            capabilities=(object(),),
            requested_capability="web_research",
        )


def test_validator_rejects_empty_capability_id():
    validator = EvolutionCapabilityValidator()

    capability = _capability()

    invalid = CapabilityDescriptor(
        id="",
        name=capability.name,
        description=capability.description,
        version=capability.version,
        entry_point=capability.entry_point,
        dependencies=capability.dependencies,
    )

    result = validator.validate(
        capabilities=(invalid,),
        requested_capability="web_research",
    )

    assert result.passed is False

    assert result.reason == (
        "capability descriptor must have "
        "a valid id"
    )


def test_validator_rejects_empty_capability_name():
    validator = EvolutionCapabilityValidator()

    capability = _capability()

    invalid = CapabilityDescriptor(
        id=capability.id,
        name="",
        description=capability.description,
        version=capability.version,
        entry_point=capability.entry_point,
        dependencies=capability.dependencies,
    )

    result = validator.validate(
        capabilities=(invalid,),
        requested_capability="web_research",
    )

    assert result.passed is False

    assert result.reason == (
        "capability descriptor must have "
        "a valid name"
    )


def test_validator_rejects_empty_entry_point():
    validator = EvolutionCapabilityValidator()

    capability = _capability()

    invalid = CapabilityDescriptor(
        id=capability.id,
        name=capability.name,
        description=capability.description,
        version=capability.version,
        entry_point="",
        dependencies=capability.dependencies,
    )

    result = validator.validate(
        capabilities=(invalid,),
        requested_capability="web_research",
    )

    assert result.passed is False

    assert result.reason == (
        "capability descriptor must have "
        "a valid entry point"
    )


def test_validator_rejects_mismatched_capability():
    validator = EvolutionCapabilityValidator()

    result = validator.validate(
        capabilities=(
            _capability("different_capability"),
        ),
        requested_capability="web_research",
    )

    assert result.passed is False

    assert result.reason == (
        "discovered capability does not "
        "match the requested capability"
    )


def test_validator_rejects_non_tuple_capabilities():
    validator = EvolutionCapabilityValidator()

    with pytest.raises(
        TypeError,
        match="capabilities must be a tuple",
    ):
        validator.validate(
            capabilities=[],
            requested_capability="web_research",
        )


def test_validator_rejects_non_string_requested_capability():
    validator = EvolutionCapabilityValidator()

    with pytest.raises(
        TypeError,
        match="requested_capability must be a string",
    ):
        validator.validate(
            capabilities=(
                _capability(),
            ),
            requested_capability=123,
        )


def test_validator_rejects_empty_requested_capability():
    validator = EvolutionCapabilityValidator()

    with pytest.raises(
        ValueError,
        match="requested_capability must not be empty",
    ):
        validator.validate(
            capabilities=(
                _capability(),
            ),
            requested_capability="   ",
        )