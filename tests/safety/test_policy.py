from brain.safety.models.permission_decision import (
    PermissionDecision,
)

from brain.safety.models.policy import (
    Policy,
)

from brain.safety.models.risk import (
    Risk,
)


def test_policy():

    policy = Policy(
        category="command",
        maximum_risk=Risk.MEDIUM,
        decision=PermissionDecision.ASK,
    )

    assert (
        policy.category
        == "command"
    )

    assert (
        policy.maximum_risk
        == Risk.MEDIUM
    )

    assert (
        policy.decision
        == PermissionDecision.ASK
    )