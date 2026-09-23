import pytest

from brain.evolution.models.evolution_dependency_assessment import (
    EvolutionDependencyAssessment,
)

from brain.evolution.models.evolution_dependency_requirement import (
    EvolutionDependencyRequirement,
)

from brain.evolution.models.evolution_dependency_status import (
    EvolutionDependencyStatus,
)

from brain.package_managers.models.dependency import (
    Dependency,
)


def create_dependency():
    return Dependency(
        name="pytest",
        version="8.0.0",
        source="pyproject.toml",
    )


def test_dependency_status_contains_expected_values():

    assert (
        EvolutionDependencyStatus.AVAILABLE.value
        == "available"
    )

    assert (
        EvolutionDependencyStatus.MISSING.value
        == "missing"
    )

    assert (
        EvolutionDependencyStatus.VERSION_MISMATCH.value
        == "version_mismatch"
    )

    assert (
        EvolutionDependencyStatus.UNRESOLVED.value
        == "unresolved"
    )


def test_requirement_accepts_dependency():

    dependency = create_dependency()

    requirement = (
        EvolutionDependencyRequirement(
            dependency=dependency,
            reason="Required by generated code",
        )
    )

    assert (
        requirement.dependency
        == dependency
    )

    assert (
        requirement.reason
        == "Required by generated code"
    )


def test_requirement_rejects_invalid_dependency():

    with pytest.raises(
        TypeError,
        match="dependency must be a Dependency",
    ):
        EvolutionDependencyRequirement(
            dependency="pytest",
            reason="Required by generated code",
        )


def test_requirement_rejects_invalid_reason_type():

    with pytest.raises(
        TypeError,
        match="reason must be a string",
    ):
        EvolutionDependencyRequirement(
            dependency=create_dependency(),
            reason=123,
        )


def test_requirement_rejects_empty_reason():

    with pytest.raises(
        ValueError,
        match="reason must not be empty",
    ):
        EvolutionDependencyRequirement(
            dependency=create_dependency(),
            reason="",
        )


def test_requirement_is_immutable():

    requirement = (
        EvolutionDependencyRequirement(
            dependency=create_dependency(),
            reason="Required by generated code",
        )
    )

    with pytest.raises(
        AttributeError,
    ):
        requirement.reason = "changed"


def test_assessment_accepts_available_dependency():

    dependency = create_dependency()

    assessment = (
        EvolutionDependencyAssessment(
            dependency=dependency,
            status=EvolutionDependencyStatus.AVAILABLE,
            reason="Dependency is already available",
        )
    )

    assert (
        assessment.dependency
        == dependency
    )

    assert (
        assessment.status
        == EvolutionDependencyStatus.AVAILABLE
    )

    assert (
        assessment.reason
        == "Dependency is already available"
    )


def test_assessment_accepts_missing_dependency():

    assessment = (
        EvolutionDependencyAssessment(
            dependency=create_dependency(),
            status=EvolutionDependencyStatus.MISSING,
            reason="Dependency is not installed",
        )
    )

    assert (
        assessment.status
        == EvolutionDependencyStatus.MISSING
    )


def test_assessment_accepts_version_mismatch():

    assessment = (
        EvolutionDependencyAssessment(
            dependency=create_dependency(),
            status=(
                EvolutionDependencyStatus.VERSION_MISMATCH
            ),
            reason="Installed version does not satisfy requirement",
        )
    )

    assert (
        assessment.status
        == EvolutionDependencyStatus.VERSION_MISMATCH
    )


def test_assessment_accepts_unresolved_dependency():

    assessment = (
        EvolutionDependencyAssessment(
            dependency=create_dependency(),
            status=EvolutionDependencyStatus.UNRESOLVED,
            reason="Dependency state could not be determined",
        )
    )

    assert (
        assessment.status
        == EvolutionDependencyStatus.UNRESOLVED
    )


def test_assessment_rejects_invalid_dependency():

    with pytest.raises(
        TypeError,
        match="dependency must be a Dependency",
    ):
        EvolutionDependencyAssessment(
            dependency="pytest",
            status=EvolutionDependencyStatus.AVAILABLE,
            reason="Available",
        )


def test_assessment_rejects_invalid_status():

    with pytest.raises(
        TypeError,
        match="status must be an EvolutionDependencyStatus",
    ):
        EvolutionDependencyAssessment(
            dependency=create_dependency(),
            status="available",
            reason="Available",
        )


def test_assessment_rejects_invalid_reason_type():

    with pytest.raises(
        TypeError,
        match="reason must be a string",
    ):
        EvolutionDependencyAssessment(
            dependency=create_dependency(),
            status=EvolutionDependencyStatus.AVAILABLE,
            reason=123,
        )


def test_assessment_rejects_empty_reason():

    with pytest.raises(
        ValueError,
        match="reason must not be empty",
    ):
        EvolutionDependencyAssessment(
            dependency=create_dependency(),
            status=EvolutionDependencyStatus.AVAILABLE,
            reason="",
        )


def test_assessment_is_immutable():

    assessment = (
        EvolutionDependencyAssessment(
            dependency=create_dependency(),
            status=EvolutionDependencyStatus.AVAILABLE,
            reason="Available",
        )
    )

    with pytest.raises(
        AttributeError,
    ):
        assessment.status = (
            EvolutionDependencyStatus.MISSING
        )