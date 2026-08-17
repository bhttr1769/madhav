import subprocess

from brain.environment.models.command import (
    Command,
)

from brain.environment.models.command_result import (
    CommandResult,
)

from brain.environment.terminals.base_terminal import (
    BaseTerminal,
)


class LocalTerminal(
    BaseTerminal,
):

    def execute(
        self,
        command: Command,
    ) -> CommandResult:

        result = subprocess.run(
            command.value,
            capture_output=True,
            text=True,
            shell=True,
        )

        return CommandResult(
            return_code=result.returncode,
            stdout=result.stdout,
            stderr=result.stderr,
        )