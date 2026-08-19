from brain.package_managers.models.package_manager_environment import (
    PackageManagerEnvironment,
)


class PackageManagerService:
    """
    Orchestrates package-manager intelligence.
    """

    def __init__(
        self,
        dependency_file_detector,
        package_manager_detector,
        dependency_detector,
        build_lifecycle_detector,
    ):

        self._dependency_file_detector = (
            dependency_file_detector
        )

        self._package_manager_detector = (
            package_manager_detector
        )

        self._dependency_detector = (
            dependency_detector
        )

        self._build_lifecycle_detector = (
            build_lifecycle_detector
        )

    def analyze(
        self,
        signatures,
    ) -> PackageManagerEnvironment:

        dependency_files = (
            self._dependency_file_detector.detect(
                signatures,
            )
        )

        package_managers = (
            self._package_manager_detector.detect(
                dependency_files,
            )
        )

        dependencies = (
            self._dependency_detector.detect(
                dependency_files,
            )
        )

        lifecycles = (
            self._build_lifecycle_detector.detect(
                package_managers,
            )
        )

        return PackageManagerEnvironment(
            managers=package_managers,
            dependency_files=dependency_files,
            dependencies=dependencies,
            lifecycles=lifecycles,
        )