from brain.package_managers.models.build_lifecycle import (
    BuildLifecycle,
)

from brain.package_managers.models.dependency import (
    Dependency,
)

from brain.package_managers.models.dependency_file import (
    DependencyFile,
)

from brain.package_managers.models.package_manager import (
    PackageManager,
)

from brain.package_managers.models.package_manager_environment import (
    PackageManagerEnvironment,
)

from brain.package_managers.models.project_commands import (
    ProjectCommand,
)


def test_package_manager_environment():

    environment = (
        PackageManagerEnvironment(
            managers={
                PackageManager(
                    name="npm",
                    manifest="package.json",
                ),
            },
            dependency_files={
                DependencyFile(
                    name="package.json",
                    path="package.json",
                    type="manifest",
                ),
            },
            dependencies={
                Dependency(
                    name="express",
                    version="1.0.0",
                    source="package.json",
                ),
            },
            lifecycles={
                BuildLifecycle(
                    commands=frozenset(
                        {
                            ProjectCommand(
                                name="install",
                                command="npm install",
                            ),
                            ProjectCommand(
                                name="build",
                                command="npm run build",
                            ),
                        }
                    ),
                ),
            },
        )
    )

    assert len(
        environment.managers
    ) == 1

    assert len(
        environment.dependency_files
    ) == 1

    assert len(
        environment.dependencies
    ) == 1

    assert len(
        environment.lifecycles
    ) == 1