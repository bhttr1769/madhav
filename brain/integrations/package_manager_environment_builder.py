from brain.package_managers.models.package_manager_environment import (
    PackageManagerEnvironment,
)

from brain.package_managers.services.package_manager_service import (
    PackageManagerService,
)

from brain.workspace.models.repository import (
    Repository,
)


class PackageManagerEnvironmentBuilder:
    """
    Connects repository knowledge with
    package-manager intelligence.
    """

    def __init__(
        self,
        service: PackageManagerService,
    ):

        self._service = service

    def build(
        self,
        repository: Repository,
    ) -> PackageManagerEnvironment:

        return self._service.analyze(
            repository.signatures,
        )