from brain.safety.models.permission_decision import (
    PermissionDecision,
)


def test_permission_decision():

    assert (
        PermissionDecision.ALLOW.value
        == "allow"
    )

    assert (
        PermissionDecision.DENY.value
        == "deny"
    )

    assert (
        PermissionDecision.ASK.value
        == "ask"
    )