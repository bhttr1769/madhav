from brain.safety.models.action import (
    Action,
)

from brain.safety.models.approval_response import (
    ApprovalResponse,
)

from brain.safety.models.permission_decision import (
    PermissionDecision,
)


class ExecutionGuard:
    """
    Controls whether an action may cross
    the safety boundary.
    """

    def authorize(
        self,
        action: Action,
        decision: PermissionDecision,
        approval: ApprovalResponse | None = None,
    ) -> None:

        if (
            decision
            == PermissionDecision.ALLOW
        ):

            return

        if (
            decision
            == PermissionDecision.ASK
            and approval
            == ApprovalResponse.APPROVE
        ):

            return

        raise PermissionError(
            "Action is not authorized."
        )