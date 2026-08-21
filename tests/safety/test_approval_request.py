from brain.safety.models.action import (
    Action,
)

from brain.safety.models.approval_request import (
    ApprovalRequest,
)

from brain.safety.models.risk import (
    Risk,
)


def test_approval_request():

    action = Action(
        name="execute",
        category="command",
        target="npm install",
    )

    request = ApprovalRequest(
        action=action,
        risk=Risk.HIGH,
    )

    assert (
        request.action
        == action
    )

    assert (
        request.risk
        == Risk.HIGH
    )