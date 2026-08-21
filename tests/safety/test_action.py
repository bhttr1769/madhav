from brain.safety.models.action import (
    Action,
)


def test_action():

    action = Action(
        name="execute",
        category="command",
        target="echo hello",
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