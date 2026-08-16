from brain.environment.registries.terminal_registry import (
    TerminalRegistry,
)

from brain.environment.terminals.local_terminal import (
    LocalTerminal,
)


def test_terminal_registry():

    registry = (
        TerminalRegistry()
    )

    terminal = (
        LocalTerminal()
    )

    registry.register(
        terminal,
    )

    assert (
        len(
            registry.all(),
        )
        == 1
    )

    assert (
        registry.all()[0]
        == terminal
    )