import pytest

from brain.evolution.evolution_dependency_safety_policy import (
    EvolutionDependencySafetyPolicy,
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
from brain.evolution.models.evolution_dependency_requirement import (
    EvolutionDependencyRequirement,
)
from brain.evolution.models.evolution_dependency_resolution import (
    EvolutionDependencyResolution,
)
from brain.evolution.models.evolution_dependency_resolution_status import (
    EvolutionDependencyResolutionStatus,
)
from brain.evolution.models.evolution_dependency_safety_result import (
    EvolutionDependencySafetyResult,
)
from brain.evolution.models.evolution_dependency_safety_status import (
    EvolutionDependencySafetyStatus,
)
from brain.evolution.models.evolution_dependency_status import (
    EvolutionDependencyStatus,
)
from brain.package_managers.models.dependency import (
    Dependency,
)


def _dependency():
    return Dependency(
        name="requests",
        version="2.31.0",
        source="requirements.txt",
    )


def _requirement():
    return EvolutionDependencyRequirement(
        dependency=_dependency(),
        reason="Required by the evolution.",
    )


def _assessment(
    status=EvolutionDependencyStatus.AVAILABLE,
):
    return EvolutionDependencyAssessment(
        dependency=_dependency(),
        status=status,
        reason="Test dependency assessment.",
    )


def _resolution(
    status=EvolutionDependencyResolutionStatus.NOT_REQUIRED,
    assessment_status=EvolutionDependencyStatus.AVAILABLE,
):
    package_manager = None

    if (
        status
        is EvolutionDependencyResolutionStatus.RESOLVABLE
    ):
        package_manager = "pip"

    return EvolutionDependencyResolution(
        assessment=_assessment(
            assessment_status,
        ),
        status=status,
        package_manager=package_manager,
        reason="Test dependency resolution.",
    )


def _plan(
    operation,
    assessment_status=EvolutionDependencyStatus.AVAILABLE,
    resolution_status=(
        EvolutionDependencyResolutionStatus.NOT_REQUIRED
    ),
    reason="Test dependency plan.",
):
    resolution = _resolution(
        status=resolution_status,
        assessment_status=assessment_status,
    )

    return EvolutionDependencyPlan(
        requirement=_requirement(),
        resolution=resolution,
        operation=operation,
        package_manager=(
            resolution.package_manager
        ),
        reason=reason,
    )


def test_no_plans_are_allowed():
    policy = EvolutionDependencySafetyPolicy()

    result = policy.evaluate(())

    assert isinstance(
        result,
        EvolutionDependencySafetyResult,
    )

    assert result.status is (
        EvolutionDependencySafetyStatus.ALLOWED
    )

    assert result.allowed is True

    assert result.reason == (
        "no dependency changes are required"
    )


def test_no_action_plan_is_allowed():
    policy = EvolutionDependencySafetyPolicy()

    result = policy.evaluate(
        (
            _plan(
                EvolutionDependencyPlanOperation.NO_ACTION,
            ),
        )
    )

    assert result.status is (
        EvolutionDependencySafetyStatus.ALLOWED
    )

    assert result.allowed is True

    assert result.reason == (
        "all dependency plans require no "
        "environment mutation"
    )


def test_add_plan_is_blocked():
    policy = EvolutionDependencySafetyPolicy()

    result = policy.evaluate(
        (
            _plan(
                EvolutionDependencyPlanOperation.ADD,
                assessment_status=(
                    EvolutionDependencyStatus.MISSING
                ),
                resolution_status=(
                    EvolutionDependencyResolutionStatus.RESOLVABLE
                ),
            ),
        )
    )

    assert result.status is (
        EvolutionDependencySafetyStatus.BLOCKED
    )

    assert result.allowed is False

    assert result.reason == (
        "dependency addition requires explicit "
        "dependency mutation authorization"
    )


def test_update_plan_is_blocked():
    policy = EvolutionDependencySafetyPolicy()

    result = policy.evaluate(
        (
            _plan(
                EvolutionDependencyPlanOperation.UPDATE,
                assessment_status=(
                    EvolutionDependencyStatus.VERSION_MISMATCH
                ),
                resolution_status=(
                    EvolutionDependencyResolutionStatus.RESOLVABLE
                ),
            ),
        )
    )

    assert result.status is (
        EvolutionDependencySafetyStatus.BLOCKED
    )

    assert result.allowed is False

    assert result.reason == (
        "dependency update requires explicit "
        "dependency mutation authorization"
    )


def test_blocked_plan_is_blocked():
    policy = EvolutionDependencySafetyPolicy()

    result = policy.evaluate(
        (
            _plan(
                EvolutionDependencyPlanOperation.BLOCKED,
                resolution_status=(
                    EvolutionDependencyResolutionStatus.NOT_RESOLVABLE
                ),
                reason="No package manager available.",
            ),
        )
    )

    assert result.status is (
        EvolutionDependencySafetyStatus.BLOCKED
    )

    assert result.allowed is False

    assert result.reason == (
        "dependency plan is blocked: "
        "No package manager available."
    )


def test_mixed_no_action_and_add_is_blocked():
    policy = EvolutionDependencySafetyPolicy()

    result = policy.evaluate(
        (
            _plan(
                EvolutionDependencyPlanOperation.NO_ACTION,
            ),
            _plan(
                EvolutionDependencyPlanOperation.ADD,
                assessment_status=(
                    EvolutionDependencyStatus.MISSING
                ),
                resolution_status=(
                    EvolutionDependencyResolutionStatus.RESOLVABLE
                ),
            ),
        )
    )

    assert result.status is (
        EvolutionDependencySafetyStatus.BLOCKED
    )

    assert result.allowed is False


def test_mixed_no_action_and_update_is_blocked():
    policy = EvolutionDependencySafetyPolicy()

    result = policy.evaluate(
        (
            _plan(
                EvolutionDependencyPlanOperation.NO_ACTION,
            ),
            _plan(
                EvolutionDependencyPlanOperation.UPDATE,
                assessment_status=(
                    EvolutionDependencyStatus.VERSION_MISMATCH
                ),
                resolution_status=(
                    EvolutionDependencyResolutionStatus.RESOLVABLE
                ),
            ),
        )
    )

    assert result.status is (
        EvolutionDependencySafetyStatus.BLOCKED
    )

    assert result.allowed is False


def test_plans_must_be_tuple():
    policy = EvolutionDependencySafetyPolicy()

    with pytest.raises(
        TypeError,
        match="plans must be a tuple",
    ):
        policy.evaluate([])


def test_plans_must_contain_dependency_plans():
    policy = EvolutionDependencySafetyPolicy()

    with pytest.raises(
        TypeError,
        match=(
            "plans must contain only "
            "EvolutionDependencyPlan instances"
        ),
    ):
        policy.evaluate(
            (object(),)
        )


def test_safety_result_requires_valid_status():
    with pytest.raises(
        TypeError,
        match=(
            "status must be an "
            "EvolutionDependencySafetyStatus"
        ),
    ):
        EvolutionDependencySafetyResult(
            status="allowed",
            reason="test",
        )


def test_safety_result_requires_string_reason():
    with pytest.raises(
        TypeError,
        match="reason must be a string",
    ):
        EvolutionDependencySafetyResult(
            status=(
                EvolutionDependencySafetyStatus.ALLOWED
            ),
            reason=None,
        )


def test_safety_result_requires_non_empty_reason():
    with pytest.raises(
        ValueError,
        match="reason must not be empty",
    ):
        EvolutionDependencySafetyResult(
            status=(
                EvolutionDependencySafetyStatus.ALLOWED
            ),
            reason="",
        )


def test_safety_result_allowed_property():
    allowed = EvolutionDependencySafetyResult(
        status=(
            EvolutionDependencySafetyStatus.ALLOWED
        ),
        reason="Safe.",
    )

    blocked = EvolutionDependencySafetyResult(
        status=(
            EvolutionDependencySafetyStatus.BLOCKED
        ),
        reason="Blocked.",
    )

    assert allowed.allowed is True
    assert blocked.allowed is False