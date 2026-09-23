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


class EvolutionDependencyPlanner:
    """
    Creates a dependency change plan from an evolution
    dependency requirement and its resolution decision.

    This service does not execute dependency changes.
    """

    def plan(
        self,
        requirement: EvolutionDependencyRequirement,
        resolution: EvolutionDependencyResolution,
    ) -> EvolutionDependencyPlan:

        if not isinstance(
            requirement,
            EvolutionDependencyRequirement,
        ):
            raise TypeError(
                "requirement must be an "
                "EvolutionDependencyRequirement"
            )

        if not isinstance(
            resolution,
            EvolutionDependencyResolution,
        ):
            raise TypeError(
                "resolution must be an "
                "EvolutionDependencyResolution"
            )

        if (
            resolution.assessment.dependency
            != requirement.dependency
        ):
            raise ValueError(
                "resolution assessment dependency "
                "must match requirement dependency"
            )

        status = resolution.status

        if (
            status
            == EvolutionDependencyResolutionStatus
            .NOT_REQUIRED
        ):
            return EvolutionDependencyPlan(
                requirement=requirement,
                resolution=resolution,
                operation=(
                    EvolutionDependencyPlanOperation
                    .NO_ACTION
                ),
                package_manager=None,
                reason=(
                    "dependency is already available; "
                    "no dependency change is required"
                ),
            )

        if (
            status
            == EvolutionDependencyResolutionStatus
            .RESOLVABLE
        ):
            assessment_status = (
                resolution.assessment.status
            )

            if resolution.package_manager is None:
                raise ValueError(
                    "resolvable dependency must have "
                    "a package manager"
                )

            if (
                assessment_status.value
                == "missing"
            ):
                return EvolutionDependencyPlan(
                    requirement=requirement,
                    resolution=resolution,
                    operation=(
                        EvolutionDependencyPlanOperation
                        .ADD
                    ),
                    package_manager=(
                        resolution.package_manager
                    ),
                    reason=(
                        f"add dependency "
                        f"'{requirement.dependency.name}' "
                        f"version "
                        f"'{requirement.dependency.version}' "
                        f"using "
                        f"'{resolution.package_manager}'"
                    ),
                )

            if (
                assessment_status.value
                == "version_mismatch"
            ):
                return EvolutionDependencyPlan(
                    requirement=requirement,
                    resolution=resolution,
                    operation=(
                        EvolutionDependencyPlanOperation
                        .UPDATE
                    ),
                    package_manager=(
                        resolution.package_manager
                    ),
                    reason=(
                        f"update dependency "
                        f"'{requirement.dependency.name}' "
                        f"to version "
                        f"'{requirement.dependency.version}' "
                        f"using "
                        f"'{resolution.package_manager}'"
                    ),
                )

            raise ValueError(
                "resolvable dependency has an "
                "unsupported assessment status"
            )

        if (
            status
            in (
                EvolutionDependencyResolutionStatus
                .NOT_RESOLVABLE,
                EvolutionDependencyResolutionStatus
                .UNRESOLVED,
            )
        ):
            return EvolutionDependencyPlan(
                requirement=requirement,
                resolution=resolution,
                operation=(
                    EvolutionDependencyPlanOperation
                    .BLOCKED
                ),
                package_manager=None,
                reason=(
                    "dependency change cannot be "
                    "planned safely: "
                    f"{resolution.reason}"
                ),
            )

        raise ValueError(
            "unsupported dependency resolution status"
        )