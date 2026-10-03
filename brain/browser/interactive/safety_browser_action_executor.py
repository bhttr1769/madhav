from brain.browser.interactive.browser_executor import BrowserExecutor
from brain.browser.interactive.models.browser_action import BrowserAction
from brain.safety.models.approval_response import ApprovalResponse
from brain.safety.services.safety_service import SafetyService


class SafetyBrowserActionExecutor:
    """
    Authorizes browser actions before delegating execution.
    """

    def __init__(
        self,
        safety_service: SafetyService,
        executor: BrowserExecutor,
    ):
        self._safety_service = safety_service
        self._executor = executor

    def execute(
        self,
        action: BrowserAction,
        approval: ApprovalResponse | None = None,
    ) -> None:
        if not isinstance(action, BrowserAction):
            raise TypeError(
                "action must be a BrowserAction"
            )

        safety_action = action.to_action()

        self._safety_service.authorize(
            safety_action,
            approval,
        )

        self._executor.execute(action)