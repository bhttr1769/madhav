from brain.safety.models.action import (
    Action,
)

from brain.safety.models.approval_request import (
    ApprovalRequest,
)

from brain.safety.models.approval_response import (
    ApprovalResponse,
)

from brain.safety.models.risk import (
    Risk,
)


class ApprovalService:
    """
    Manages actions that require user approval.
    """

    def create_request(
        self,
        action: Action,
        risk: Risk,
    ) -> ApprovalRequest:

        return ApprovalRequest(
            action=action,
            risk=risk,
        )

    def resolve(
        self,
        response: ApprovalResponse,
    ) -> bool:

        return (
            response
            == ApprovalResponse.APPROVE
        )