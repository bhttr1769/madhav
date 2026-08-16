from brain.environment.models.command import (
    Command,
)


def test_command():

    command = Command(
        value="echo hello",
    )

    assert (
        command.value
        == "echo hello"
    )