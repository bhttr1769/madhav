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

from brain.package_managers.models.package_manager_environment import (
    PackageManagerEnvironment,
)


class EvolutionDependencyResolutionService:
    """
    Determines whether an evolution dependency can be
    resolved using the discovered package-manager
    environment.

    This service does not install dependencies,
    modify manifests, or execute package-manager commands.
    """

    def resolve(
        self,
        assessment: EvolutionDependencyAssessment,
        environment: PackageManagerEnvironment,
    ) -> EvolutionDependencyResolution:

        if not isinstance(
            assessment,
            EvolutionDependencyAssessment,
        ):
            raise TypeError(
                "assessment must be an "
                "EvolutionDependencyAssessment"
            )

        if not isinstance(
            environment,
            PackageManagerEnvironment,
        ):
            raise TypeError(
                "environment must be a "
                "PackageManagerEnvironment"
            )

        status = assessment.status

        if (
            status
            == EvolutionDependencyStatus.AVAILABLE
        ):
            return EvolutionDependencyResolution(
                assessment=assessment,
                status=(
                    EvolutionDependencyResolutionStatus
                    .NOT_REQUIRED
                ),
                package_manager=None,
                reason=(
                    "dependency is already available; "
                    "resolution is not required"
                ),
            )

        if (
            status
            == EvolutionDependencyStatus.UNRESOLVED
        ):
            return EvolutionDependencyResolution(
                assessment=assessment,
                status=(
                    EvolutionDependencyResolutionStatus
                    .UNRESOLVED
                ),
                package_manager=None,
                reason=(
                    "dependency availability could not "
                    "be determined; resolution cannot "
                    "be determined safely"
                ),
            )

        if not environment.managers:
            return EvolutionDependencyResolution(
                assessment=assessment,
                status=(
                    EvolutionDependencyResolutionStatus
                    .NOT_RESOLVABLE
                ),
                package_manager=None,
                reason=(
                    "no package manager is available "
                    "in the discovered environment"
                ),
            )

        package_managers = tuple(
            sorted(
                manager.name
                for manager in environment.managers
                if manager.name
            )
        )

        if not package_managers:
            return EvolutionDependencyResolution(
                assessment=assessment,
                status=(
                    EvolutionDependencyResolutionStatus
                    .UNRESOLVED
                ),
                package_manager=None,
                reason=(
                    "package managers were discovered "
                    "but none has a valid name"
                ),
            )

        package_manager = package_managers[0]

        if (
            status
            == EvolutionDependencyStatus.MISSING
        ):
            return EvolutionDependencyResolution(
                assessment=assessment,
                status=(
                    EvolutionDependencyResolutionStatus
                    .RESOLVABLE
                ),
                package_manager=package_manager,
                reason=(
                    f"dependency is missing and the "
                    f"discovered package manager "
                    f"'{package_manager}' may resolve it"
                ),
            )

        if (
            status
            == EvolutionDependencyStatus.VERSION_MISMATCH
        ):
            return EvolutionDependencyResolution(
                assessment=assessment,
                status=(
                    EvolutionDependencyResolutionStatus
                    .RESOLVABLE
                ),
                package_manager=package_manager,
                reason=(
                    f"dependency version does not match "
                    f"and the discovered package manager "
                    f"'{package_manager}' may resolve it"
                ),
            )

        return EvolutionDependencyResolution(
            assessment=assessment,
            status=(
                EvolutionDependencyResolutionStatus
                .UNRESOLVED
            ),
            package_manager=None,
            reason=(
                "dependency resolution could not be "
                "determined safely"
            ),
        )