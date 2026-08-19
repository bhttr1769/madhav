from brain.package_managers.models.project_commands import (
    ProjectCommand,
)


def test_project_command():

    command = ProjectCommand(
        name="install",
        command="npm install",
    )

    assert (
        command.name
        == "install"
    )

    assert (
        command.command
        == "npm install"
    )