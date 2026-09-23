import pytest

from brain.evolution.evolution_dependency_resolution import (
    EvolutionDependencyResolutionService,
)

from brain.evolution.models.evolution_dependency_assessment import (
    EvolutionDependencyAssessment,
)

from brain.evolution.models.evolution_dependency_resolution import (
    EvolutionDependencyResolution,
)

from brain.evolution.models.evolution_dependency_resolution_status import (
    EvolutionDependencyResolutionStatus,
)

from brain.evolution.models.evolution_dependency_status import (
    EvolutionDependencyStatus,
)

from brain.evolution.models.evolution_dependency_requirement import (
    EvolutionDependencyRequirement,
)

from brain.package_managers.models.dependency import (
    Dependency,
)

from brain.package_managers.models.package_manager import (
    PackageManager,
)

from brain.package_managers.models.package_manager_environment import (
    PackageManagerEnvironment,
)


def dependency():
    return Dependency(
        name="pytest",
        version="8.0.0",
        source="pyproject.toml",
    )


def assessment(
    status,
):
    return EvolutionDependencyAssessment(
        dependency=dependency(),
        status=status,
        reason="test assessment",
    )


def environment(
    managers=None,
):
    if managers is None:
        managers = set()

    return PackageManagerEnvironment(
        managers=managers,
        dependency_files=set(),
        dependencies=set(),
        lifecycles=set(),
    )


def test_available_dependency_does_not_require_resolution():

    service = EvolutionDependencyResolutionService()

    result = service.resolve(
        assessment(
            EvolutionDependencyStatus.AVAILABLE,
        ),
        environment(),
    )

    assert isinstance(
        result,
        EvolutionDependencyResolution,
    )

    assert (
        result.status
        == EvolutionDependencyResolutionStatus
        .NOT_REQUIRED
    )

    assert result.package_manager is None


def test_unresolved_dependency_remains_unresolved():

    service = EvolutionDependencyResolutionService()

    result = service.resolve(
        assessment(
            EvolutionDependencyStatus.UNRESOLVED,
        ),
        environment(
            {
                PackageManager(
                    name="pip",
                    manifest="pyproject.toml",
                )
            }
        ),
    )

    assert (
        result.status
        == EvolutionDependencyResolutionStatus
        .UNRESOLVED
    )

    assert result.package_manager is None


def test_missing_dependency_is_resolvable_when_manager_exists():

    service = EvolutionDependencyResolutionService()

    result = service.resolve(
        assessment(
            EvolutionDependencyStatus.MISSING,
        ),
        environment(
            {
                PackageManager(
                    name="pip",
                    manifest="pyproject.toml",
                )
            }
        ),
    )

    assert (
        result.status
        == EvolutionDependencyResolutionStatus
        .RESOLVABLE
    )

    assert result.package_manager == "pip"


def test_version_mismatch_is_resolvable_when_manager_exists():

    service = EvolutionDependencyResolutionService()

    result = service.resolve(
        assessment(
            EvolutionDependencyStatus.VERSION_MISMATCH,
        ),
        environment(
            {
                PackageManager(
                    name="pip",
                    manifest="pyproject.toml",
                )
            }
        ),
    )

    assert (
        result.status
        == EvolutionDependencyResolutionStatus
        .RESOLVABLE
    )

    assert result.package_manager == "pip"


def test_missing_dependency_is_not_resolvable_without_manager():

    service = EvolutionDependencyResolutionService()

    result = service.resolve(
        assessment(
            EvolutionDependencyStatus.MISSING,
        ),
        environment(),
    )

    assert (
        result.status
        == EvolutionDependencyResolutionStatus
        .NOT_RESOLVABLE
    )

    assert result.package_manager is None


def test_version_mismatch_is_not_resolvable_without_manager():

    service = EvolutionDependencyResolutionService()

    result = service.resolve(
        assessment(
            EvolutionDependencyStatus.VERSION_MISMATCH,
        ),
        environment(),
    )

    assert (
        result.status
        == EvolutionDependencyResolutionStatus
        .NOT_RESOLVABLE
    )

    assert result.package_manager is None


def test_uses_deterministic_package_manager_when_multiple_exist():

    service = EvolutionDependencyResolutionService()

    result = service.resolve(
        assessment(
            EvolutionDependencyStatus.MISSING,
        ),
        environment(
            {
                PackageManager(
                    name="npm",
                    manifest="package.json",
                ),
                PackageManager(
                    name="pip",
                    manifest="pyproject.toml",
                ),
            }
        ),
    )

    assert (
        result.package_manager
        == "npm"
    )


def test_rejects_invalid_assessment():

    service = EvolutionDependencyResolutionService()

    with pytest.raises(
        TypeError,
        match="assessment must be an "
        "EvolutionDependencyAssessment",
    ):
        service.resolve(
            object(),
            environment(),
        )


def test_rejects_invalid_environment():

    service = EvolutionDependencyResolutionService()

    with pytest.raises(
        TypeError,
        match="environment must be a "
        "PackageManagerEnvironment",
    ):
        service.resolve(
            assessment(
                EvolutionDependencyStatus.MISSING,
            ),
            object(),
        )


def test_result_preserves_assessment():

    service = EvolutionDependencyResolutionService()

    original = assessment(
        EvolutionDependencyStatus.MISSING,
    )

    result = service.resolve(
        original,
        environment(
            {
                PackageManager(
                    name="pip",
                    manifest="pyproject.toml",
                )
            }
        ),
    )

    assert result.assessment is original