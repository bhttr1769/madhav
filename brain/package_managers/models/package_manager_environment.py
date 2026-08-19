from dataclasses import dataclass

from brain.package_managers.models.dependency import (
    Dependency,
)

from brain.package_managers.models.dependency_file import (
    DependencyFile,
)

from brain.package_managers.models.package_manager import (
    PackageManager,
)

from brain.package_managers.models.build_lifecycle import (
    BuildLifecycle,
)



@dataclass(
    frozen=True,
)
class PackageManagerEnvironment:
    """
    Complete package-manager knowledge.
    """

    managers: set[PackageManager]

    dependency_files: set[DependencyFile]

    dependencies: set[Dependency]

    lifecycles: set[BuildLifecycle]