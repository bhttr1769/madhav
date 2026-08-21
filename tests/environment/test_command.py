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

def test_command_to_action():

    command = Command(
        value="echo hello",
    )

    action = (
        command.to_action()
    )

    assert (
        action.name
        == "execute"
    )

    assert (
        action.category
        == "command"
    )

    assert (
        action.target
        == "echo hello"
    )