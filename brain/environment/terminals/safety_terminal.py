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

from brain.safety.logging.models.action_log_event import (
    ActionLogEvent,
)

from brain.safety.logging.models.action_log_status import (
    ActionLogStatus,
)

from brain.safety.logging.services.logging_service import (
    LoggingService,
)

from brain.safety.logging.stores.action_log_store import (
    ActionLogStore,
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
        logging_service: LoggingService | None = None,
    ):

        self._safety_service = (
            safety_service
        )

        self._terminal = (
            terminal
            if terminal is not None
            else LocalTerminal()
        )

        self._logging_service = (
            logging_service
            if logging_service is not None
            else LoggingService(
                ActionLogStore(),
            )
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

        self._logging_service.log(
            action=action,
            event=ActionLogEvent.EXECUTION_STARTED,
            status=ActionLogStatus.RUNNING,
        )

        try:

            result = (
                self._terminal.execute(
                    command,
                )
            )

            if result is None:

                self._logging_service.log(
                    action=action,
                    event=(
                        ActionLogEvent
                        .EXECUTION_COMPLETED
                    ),
                    status=(
                        ActionLogStatus.COMPLETED
                    ),
                )

                return result

            if (
                result.return_code
                == 0
            ):

                self._logging_service.log(
                    action=action,
                    event=(
                        ActionLogEvent
                        .EXECUTION_COMPLETED
                    ),
                    status=(
                        ActionLogStatus.COMPLETED
                    ),
                    metadata={
                        "return_code": (
                            result.return_code
                        ),
                    },
                )

            else:

                self._logging_service.log(
                    action=action,
                    event=(
                        ActionLogEvent
                        .EXECUTION_FAILED
                    ),
                    status=(
                        ActionLogStatus.FAILED
                    ),
                    metadata={
                        "return_code": (
                            result.return_code
                        ),
                        "stderr": result.stderr,
                    },
                )

            return result

        except Exception as error:

            self._logging_service.log(
                action=action,
                event=(
                    ActionLogEvent
                    .EXECUTION_FAILED
                ),
                status=(
                    ActionLogStatus.FAILED
                ),
                metadata={
                    "error": str(error),
                },
            )

            raise