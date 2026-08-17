from brain.environment.models.command_result import (
    CommandResult,
)


class FakeTerminal:

    def execute(
        self,
        command,
    ):

        return CommandResult(
            return_code=0,
            stdout=(
                "123|postgres:16|"
                "postgres|Up 2 hours"
            ),
            stderr="",
        )