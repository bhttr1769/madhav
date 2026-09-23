import pytest

from brain.evolution.evolution_dependency_planner import (
    EvolutionDependencyPlanner,
)

from brain.evolution.models.evolution_dependency_assessment import (
    EvolutionDependencyAssessment,
)

from brain.evolution.models.evolution_dependency_plan import (
    EvolutionDependencyPlan,
)

from brain.evolution.models.evolution_dependency_plan_operation import (
    EvolutionDependencyPlanOperation,
)

from brain.evolution.models.evolution_dependency_resolution import (
    EvolutionDependencyResolution,
)

from brain.evolution.models.evolution_dependency_resolution_status import (
    EvolutionDependencyResolutionStatus,
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


def dependency():
    return Dependency(
        name="pytest",
        version="8.0.0",
        source="pyproject.toml",
    )


def requirement():
    return EvolutionDependencyRequirement(
        dependency=dependency(),
        reason="Required by the evolution",
    )


def assessment(
    status,
):
    return EvolutionDependencyAssessment(
        dependency=dependency(),
        status=status,
        reason="test assessment",
    )


def resolution(
    assessment_status,
    resolution_status,
    package_manager=None,
):
    return EvolutionDependencyResolution(
        assessment=assessment(
            assessment_status,
        ),
        status=resolution_status,
        package_manager=package_manager,
        reason="test resolution",
    )


def test_available_dependency_requires_no_action():

    planner = EvolutionDependencyPlanner()

    result = planner.plan(
        requirement(),
        resolution(
            EvolutionDependencyStatus.AVAILABLE,
            EvolutionDependencyResolutionStatus
            .NOT_REQUIRED,
        ),
    )

    assert isinstance(
        result,
        EvolutionDependencyPlan,
    )

    assert (
        result.operation
        == EvolutionDependencyPlanOperation
        .NO_ACTION
    )

    assert result.package_manager is None


def test_missing_dependency_produces_add_plan():

    planner = EvolutionDependencyPlanner()

    result = planner.plan(
        requirement(),
        resolution(
            EvolutionDependencyStatus.MISSING,
            EvolutionDependencyResolutionStatus
            .RESOLVABLE,
            package_manager="pip",
        ),
    )

    assert (
        result.operation
        == EvolutionDependencyPlanOperation.ADD
    )

    assert result.package_manager == "pip"

    assert "pytest" in result.reason
    assert "8.0.0" in result.reason
    assert "pip" in result.reason


def test_version_mismatch_produces_update_plan():

    planner = EvolutionDependencyPlanner()

    result = planner.plan(
        requirement(),
        resolution(
            EvolutionDependencyStatus.VERSION_MISMATCH,
            EvolutionDependencyResolutionStatus
            .RESOLVABLE,
            package_manager="pip",
        ),
    )

    assert (
        result.operation
        == EvolutionDependencyPlanOperation.UPDATE
    )

    assert result.package_manager == "pip"

    assert "pytest" in result.reason
    assert "8.0.0" in result.reason


def test_not_resolvable_dependency_is_blocked():

    planner = EvolutionDependencyPlanner()

    result = planner.plan(
        requirement(),
        resolution(
            EvolutionDependencyStatus.MISSING,
            EvolutionDependencyResolutionStatus
            .NOT_RESOLVABLE,
        ),
    )

    assert (
        result.operation
        == EvolutionDependencyPlanOperation
        .BLOCKED
    )

    assert result.package_manager is None


def test_unresolved_dependency_is_blocked():

    planner = EvolutionDependencyPlanner()

    result = planner.plan(
        requirement(),
        resolution(
            EvolutionDependencyStatus.UNRESOLVED,
            EvolutionDependencyResolutionStatus
            .UNRESOLVED,
        ),
    )

    assert (
        result.operation
        == EvolutionDependencyPlanOperation
        .BLOCKED
    )

    assert result.package_manager is None


def test_resolvable_dependency_requires_package_manager():

    planner = EvolutionDependencyPlanner()

    with pytest.raises(
        ValueError,
        match="resolvable dependency must have "
        "a package manager",
    ):
        planner.plan(
            requirement(),
            resolution(
                EvolutionDependencyStatus.MISSING,
                EvolutionDependencyResolutionStatus
                .RESOLVABLE,
            ),
        )


def test_resolution_dependency_must_match_requirement():

    planner = EvolutionDependencyPlanner()

    other_dependency = Dependency(
        name="requests",
        version="2.32.0",
        source="pyproject.toml",
    )

    other_assessment = (
        EvolutionDependencyAssessment(
            dependency=other_dependency,
            status=EvolutionDependencyStatus.MISSING,
            reason="test assessment",
        )
    )

    other_resolution = (
        EvolutionDependencyResolution(
            assessment=other_assessment,
            status=(
                EvolutionDependencyResolutionStatus
                .RESOLVABLE
            ),
            package_manager="pip",
            reason="test resolution",
        )
    )

    with pytest.raises(
        ValueError,
        match="resolution assessment dependency",
    ):
        planner.plan(
            requirement(),
            other_resolution,
        )


def test_plan_preserves_requirement_and_resolution():

    planner = EvolutionDependencyPlanner()

    requested = requirement()

    resolved = resolution(
        EvolutionDependencyStatus.MISSING,
        EvolutionDependencyResolutionStatus
        .RESOLVABLE,
        package_manager="pip",
    )

    result = planner.plan(
        requested,
        resolved,
    )

    assert result.requirement is requested
    assert result.resolution is resolved