from brain.environment.terminals.base_terminal import (
    BaseTerminal,
)


class TerminalRegistry:

    def __init__(
        self,
    ):

        self._terminals: list[
            BaseTerminal
        ] = []

    def register(
        self,
        terminal: BaseTerminal,
    ):

        if terminal not in self._terminals:

            self._terminals.append(
                terminal,
            )

    def all(
        self,
    ) -> list[BaseTerminal]:

        return self._terminals