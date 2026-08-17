from brain.environment.exceptions.unsafe_command_error import (
    UnsafeCommandError,
)

from brain.environment.models.command import (
    Command,
)

from brain.environment.policies.command_policy import (
    CommandPolicy,
)


class CommandValidator:

    def validate(
        self,
        command: Command,
    ) -> None:

        executable = (
            command.value
            .strip()
            .split()[0]
            .lower()
        )

        if (
            executable
            in CommandPolicy.BLOCKED_COMMANDS
        ):

            raise UnsafeCommandError(
                f"Blocked command: {executable}"
            )