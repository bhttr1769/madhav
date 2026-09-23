from brain.evolution.models.evolution_dependency_assessment import (
    EvolutionDependencyAssessment,
)

from brain.evolution.models.evolution_dependency_requirement import (
    EvolutionDependencyRequirement,
)

from brain.evolution.models.evolution_dependency_status import (
    EvolutionDependencyStatus,
)

from brain.package_managers.models.package_manager_environment import (
    PackageManagerEnvironment,
)


class EvolutionDependencyAvailability:
    """
    Assesses whether an evolution dependency requirement
    is satisfied by the discovered project environment.
    """

    def assess(
        self,
        requirement: EvolutionDependencyRequirement,
        environment: PackageManagerEnvironment,
    ) -> EvolutionDependencyAssessment:

        if not isinstance(
            requirement,
            EvolutionDependencyRequirement,
        ):
            raise TypeError(
                "requirement must be an "
                "EvolutionDependencyRequirement"
            )

        if not isinstance(
            environment,
            PackageManagerEnvironment,
        ):
            raise TypeError(
                "environment must be a "
                "PackageManagerEnvironment"
            )

        required_dependency = (
            requirement.dependency
        )

        if not required_dependency.name:
            return EvolutionDependencyAssessment(
                dependency=required_dependency,
                status=(
                    EvolutionDependencyStatus.UNRESOLVED
                ),
                reason=(
                    "dependency name is empty"
                ),
            )

        if not required_dependency.version:
            return EvolutionDependencyAssessment(
                dependency=required_dependency,
                status=(
                    EvolutionDependencyStatus.UNRESOLVED
                ),
                reason=(
                    "dependency version is empty"
                ),
            )

        matching_dependencies = tuple(
            dependency
            for dependency in environment.dependencies
            if dependency.name
            == required_dependency.name
        )

        if not matching_dependencies:
            return EvolutionDependencyAssessment(
                dependency=required_dependency,
                status=(
                    EvolutionDependencyStatus.MISSING
                ),
                reason=(
                    f"dependency '{required_dependency.name}' "
                    "is not present in the environment"
                ),
            )

        for dependency in matching_dependencies:

            if (
                dependency.version
                == required_dependency.version
            ):
                return EvolutionDependencyAssessment(
                    dependency=required_dependency,
                    status=(
                        EvolutionDependencyStatus.AVAILABLE
                    ),
                    reason=(
                        f"dependency '{required_dependency.name}' "
                        f"version '{required_dependency.version}' "
                        "is available"
                    ),
                )

        available_versions = sorted(
            {
                dependency.version
                for dependency in matching_dependencies
            }
        )

        return EvolutionDependencyAssessment(
            dependency=required_dependency,
            status=(
                EvolutionDependencyStatus.VERSION_MISMATCH
            ),
            reason=(
                f"dependency '{required_dependency.name}' "
                f"requires version "
                f"'{required_dependency.version}', "
                f"available versions: "
                f"{available_versions}"
            ),
        )