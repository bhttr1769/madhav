import pytest

from brain.evolution.evolution_dependency_availability import (
    EvolutionDependencyAvailability,
)

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

from brain.package_managers.models.package_manager_environment import (
    PackageManagerEnvironment,
)


def dependency(
    name="pytest",
    version="8.0.0",
):
    return Dependency(
        name=name,
        version=version,
        source="pyproject.toml",
    )


def environment(
    *dependencies,
):
    return PackageManagerEnvironment(
        managers=set(),
        dependency_files=set(),
        dependencies=set(dependencies),
        lifecycles=set(),
    )


def requirement(
    name="pytest",
    version="8.0.0",
):
    return EvolutionDependencyRequirement(
        dependency=dependency(
            name=name,
            version=version,
        ),
        reason="Required by the evolution",
    )


def test_available_dependency():

    service = EvolutionDependencyAvailability()

    result = service.assess(
        requirement(),
        environment(
            dependency(),
        ),
    )

    assert isinstance(
        result,
        EvolutionDependencyAssessment,
    )

    assert (
        result.status
        == EvolutionDependencyStatus.AVAILABLE
    )


def test_missing_dependency():

    service = EvolutionDependencyAvailability()

    result = service.assess(
        requirement(
            name="requests",
            version="2.32.0",
        ),
        environment(
            dependency(
                name="pytest",
                version="8.0.0",
            ),
        ),
    )

    assert (
        result.status
        == EvolutionDependencyStatus.MISSING
    )


def test_version_mismatch():

    service = EvolutionDependencyAvailability()

    result = service.assess(
        requirement(
            name="pytest",
            version="8.1.0",
        ),
        environment(
            dependency(
                name="pytest",
                version="8.0.0",
            ),
        ),
    )

    assert (
        result.status
        == EvolutionDependencyStatus.VERSION_MISMATCH
    )


def test_same_name_and_version_is_available():

    service = EvolutionDependencyAvailability()

    result = service.assess(
        requirement(
            name="pytest",
            version="8.0.0",
        ),
        environment(
            dependency(
                name="pytest",
                version="8.0.0",
            ),
            dependency(
                name="requests",
                version="2.32.0",
            ),
        ),
    )

    assert (
        result.status
        == EvolutionDependencyStatus.AVAILABLE
    )


def test_multiple_versions_are_available_when_one_matches():

    service = EvolutionDependencyAvailability()

    result = service.assess(
        requirement(
            name="pytest",
            version="8.0.0",
        ),
        environment(
            dependency(
                name="pytest",
                version="7.4.0",
            ),
            dependency(
                name="pytest",
                version="8.0.0",
            ),
        ),
    )

    assert (
        result.status
        == EvolutionDependencyStatus.AVAILABLE
    )


def test_multiple_versions_without_match_are_mismatch():

    service = EvolutionDependencyAvailability()

    result = service.assess(
        requirement(
            name="pytest",
            version="9.0.0",
        ),
        environment(
            dependency(
                name="pytest",
                version="7.4.0",
            ),
            dependency(
                name="pytest",
                version="8.0.0",
            ),
        ),
    )

    assert (
        result.status
        == EvolutionDependencyStatus.VERSION_MISMATCH
    )

    assert "7.4.0" in result.reason
    assert "8.0.0" in result.reason


def test_empty_dependency_name_is_unresolved():

    service = EvolutionDependencyAvailability()

    result = service.assess(
        requirement(
            name="",
            version="8.0.0",
        ),
        environment(),
    )

    assert (
        result.status
        == EvolutionDependencyStatus.UNRESOLVED
    )


def test_empty_dependency_version_is_unresolved():

    service = EvolutionDependencyAvailability()

    result = service.assess(
        requirement(
            name="pytest",
            version="",
        ),
        environment(),
    )

    assert (
        result.status
        == EvolutionDependencyStatus.UNRESOLVED
    )


def test_rejects_invalid_requirement():

    service = EvolutionDependencyAvailability()

    with pytest.raises(
        TypeError,
        match="requirement must be an "
        "EvolutionDependencyRequirement",
    ):
        service.assess(
            object(),
            environment(),
        )


def test_rejects_invalid_environment():

    service = EvolutionDependencyAvailability()

    with pytest.raises(
        TypeError,
        match="environment must be a "
        "PackageManagerEnvironment",
    ):
        service.assess(
            requirement(),
            object(),
        )


def test_assessment_preserves_required_dependency():

    service = EvolutionDependencyAvailability()

    requested = requirement(
        name="pytest",
        version="8.0.0",
    )

    result = service.assess(
        requested,
        environment(
            dependency(),
        ),
    )

    assert (
        result.dependency
        == requested.dependency
    )