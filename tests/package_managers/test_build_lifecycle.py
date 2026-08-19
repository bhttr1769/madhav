from brain.package_managers.models.build_lifecycle import (
    BuildLifecycle,
)

from brain.package_managers.models.project_commands import (
    ProjectCommand,
)


def test_build_lifecycle():

    lifecycle = BuildLifecycle(
        commands=frozenset(
            {
                ProjectCommand(
                    name="install",
                    command="npm install",
                ),
            }
        ),
    )

    assert (
        len(
            lifecycle.commands,
        )
        == 1
    )