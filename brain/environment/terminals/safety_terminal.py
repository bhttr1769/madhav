from brain.environment.models.command import (
    Command,
)

from brain.environment.models.command_result import (
    CommandResult,
)

from brain.environment.terminals.base_terminal import (
    BaseTerminal,
)

from brain.environment.terminals.local_terminal import (
    LocalTerminal,
)

from brain.safety.models.approval_response import (
    ApprovalResponse,
)

from brain.safety.services.safety_service import (
    SafetyService,
)


class SafetyTerminal(
    BaseTerminal,
):

    def __init__(
        self,
        safety_service: SafetyService,
        terminal: BaseTerminal | None = None,
    ):

        self._safety_service = (
            safety_service
        )

        self._terminal = (
            terminal
            if terminal is not None
            else LocalTerminal()
        )

    def execute(
        self,
        command: Command,
        approval: ApprovalResponse | None = None,
    ) -> CommandResult:

        action = (
            command.to_action()
        )

        self._safety_service.authorize(
            action,
            approval,
        )

        return self._terminal.execute(
            command,
        )