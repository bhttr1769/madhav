from brain.environment.terminals.base_terminal import (
    BaseTerminal,
)


class TerminalRegistry:
    """
    Stores terminal implementations.
    """

    def __init__(
        self,
    ):

        self._terminals = []

    def register(
        self,
        terminal: BaseTerminal,
    ):

        self._terminals.append(
            terminal,
        )

    def all(
        self,
    ):

        return self._terminals