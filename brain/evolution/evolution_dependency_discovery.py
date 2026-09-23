
from brain.package_managers.models.package_manager_environment import (
    PackageManagerEnvironment,
)


class EvolutionDependencyDiscovery:
    """
    Discovers the dependency environment of a project
    using the existing package-manager service.
    """

    def __init__(
        self,
        package_manager_service,
    ):
        if not callable(
            getattr(
                package_manager_service,
                "analyze",
                None,
            )
        ):
            raise TypeError(
                "package_manager_service must expose "
                "a callable analyze method"
            )

        self._package_manager_service = (
            package_manager_service
        )

    def discover(
        self,
        signatures,
    ) -> PackageManagerEnvironment:
        if signatures is None:
            raise TypeError(
                "signatures must not be None"
            )

        environment = (
            self._package_manager_service.analyze(
                signatures
            )
        )

        if not isinstance(
            environment,
            PackageManagerEnvironment,
        ):
            raise TypeError(
                "package_manager_service.analyze must "
                "return a PackageManagerEnvironment"
            )

        return environment