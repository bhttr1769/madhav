from brain.environment.models.command import (
    Command,
)

from brain.environment.terminals.local_terminal import (
    LocalTerminal,
)


def test_local_terminal():

    terminal = (
        LocalTerminal()
    )

    result = terminal.execute(
        Command(
            "echo hello",
        )
    )

    assert (
        result.return_code
        == 0
    )

    assert (
        "hello"
        in result.stdout.lower()
    )  