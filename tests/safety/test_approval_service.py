from brain.safety.models.action import (
    Action,
)

from brain.safety.models.approval_response import (
    ApprovalResponse,
)

from brain.safety.models.risk import (
    Risk,
)

from brain.safety.services.approval_service import (
    ApprovalService,
)


def test_create_approval_request():

    service = (
        ApprovalService()
    )

    action = Action(
        name="install",
        category="package",
        target="pytest",
    )

    request = service.create_request(
        action,
        Risk.HIGH,
    )

    assert (
        request.action
        == action
    )

    assert (
        request.risk
        == Risk.HIGH
    )


def test_approve():

    service = (
        ApprovalService()
    )

    assert (
        service.resolve(
            ApprovalResponse.APPROVE,
        )
        is True
    )


def test_reject():

    service = (
        ApprovalService()
    )

    assert (
        service.resolve(
            ApprovalResponse.REJECT,
        )
        is False
    )