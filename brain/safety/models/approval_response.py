from enum import Enum


class ApprovalResponse(Enum):
    """
    Represents the user's response to an approval request.
    """

    APPROVE = "approve"

    REJECT = "reject"