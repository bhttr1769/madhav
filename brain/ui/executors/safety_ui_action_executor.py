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

from brain.ui.executors.ui_action_executor import (
    UIActionExecutor,
)

from brain.ui.executors.windows_ui_action_executor import (
    WindowsUIActionExecutor,
)

from brain.ui.models.ui_action import (
    UIAction,
)


class SafetyUIActionExecutor:
    """
    Executes UI actions through the existing safety boundary.
    """

    def __init__(
        self,
        safety_service: SafetyService,
        executor: UIActionExecutor | None = None,
        logging_service: LoggingService | None = None,
    ):
        if not isinstance(
            safety_service,
            SafetyService,
        ):
            raise TypeError(
                "safety_service must be a SafetyService"
            )

        if executor is not None and not isinstance(
            executor,
            UIActionExecutor,
        ):
            raise TypeError(
                "executor must be a UIActionExecutor"
            )

        if logging_service is not None and not isinstance(
            logging_service,
            LoggingService,
        ):
            raise TypeError(
                "logging_service must be a LoggingService"
            )

        self._safety_service = safety_service

        self._executor = (
            executor
            if executor is not None
            else WindowsUIActionExecutor()
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
        action: UIAction,
        approval: ApprovalResponse | None = None,
    ) -> None:

        if not isinstance(
            action,
            UIAction,
        ):
            raise TypeError(
                "action must be a UIAction"
            )

        safety_action = action.to_action()

        self._safety_service.authorize(
            safety_action,
            approval,
        )

        self._logging_service.log(
            action=safety_action,
            event=ActionLogEvent.EXECUTION_STARTED,
            status=ActionLogStatus.RUNNING,
        )

        try:

            self._executor.execute(
                action,
            )

            self._logging_service.log(
                action=safety_action,
                event=ActionLogEvent.EXECUTION_COMPLETED,
                status=ActionLogStatus.COMPLETED,
            )

        except Exception as error:

            self._logging_service.log(
                action=safety_action,
                event=ActionLogEvent.EXECUTION_FAILED,
                status=ActionLogStatus.FAILED,
                metadata={
                    "error": str(error),
                },
            )

            raise