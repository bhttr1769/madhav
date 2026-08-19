from brain.package_managers.models.build_lifecycle import (
    BuildLifecycle,
)

from brain.package_managers.models.project_commands import (
    ProjectCommand,
)


class FakeBuildLifecycleDetector:

    def detect(
        self,
        package_managers,
    ):

        return {
            BuildLifecycle(
                commands=frozenset(
                    {
                        ProjectCommand(
                            name="install",
                            command="fake install",
                        ),
                        ProjectCommand(
                            name="build",
                            command="fake build",
                        ),
                    }
                )
            )
        }