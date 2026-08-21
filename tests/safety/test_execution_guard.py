import pytest

from brain.safety.models.action import (
    Action,
)

from brain.safety.models.approval_response import (
    ApprovalResponse,
)

from brain.safety.models.permission_decision import (
    PermissionDecision,
)

from brain.safety.services.execution_guard import (
    ExecutionGuard,
)

def test_approved_action():

    guard = (
        ExecutionGuard()
    )

    guard.authorize(
        Action(
            name="install",
            category="package",
            target="pytest",
        ),
        PermissionDecision.ASK,
        ApprovalResponse.APPROVE,
    )


def test_rejected_action():

    guard = (
        ExecutionGuard()
    )

    with pytest.raises(
        PermissionError,
    ):

        guard.authorize(
            Action(
                name="install",
                category="package",
                target="pytest",
            ),
            PermissionDecision.ASK,
            ApprovalResponse.REJECT,
        )

def test_allowed_action():

    guard = (
        ExecutionGuard()
    )

    guard.authorize(
        Action(
            name="execute",
            category="command",
            target="echo hello",
        ),
        PermissionDecision.ALLOW,
    )


def test_denied_action():

    guard = (
        ExecutionGuard()
    )

    with pytest.raises(
        PermissionError,
    ):

        guard.authorize(
            Action(
                name="execute",
                category="command",
                target="dangerous",
            ),
            PermissionDecision.DENY,
        )


def test_pending_action():

    guard = (
        ExecutionGuard()
    )

    with pytest.raises(
        PermissionError,
    ):

        guard.authorize(
            Action(
                name="execute",
                category="command",
                target="requires approval",
            ),
            PermissionDecision.ASK,
        )