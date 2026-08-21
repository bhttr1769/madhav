from brain.safety.models.permission_decision import (
    PermissionDecision,
)

from brain.safety.models.policy import (
    Policy,
)

from brain.safety.models.risk import (
    Risk,
)

from brain.safety.registries.policy_registry import (
    PolicyRegistry,
)


def test_policy_registry():

    registry = (
        PolicyRegistry()
    )

    policy = Policy(
        category="command",
        maximum_risk=Risk.MEDIUM,
        decision=PermissionDecision.ASK,
    )

    registry.register(
        policy,
    )

    assert (
        registry.count()
        == 1
    )

    assert (
        len(
            registry.all(),
        )
        == 1
    )

    assert (
        registry.all()[0]
        == policy
    )

def test_policy_registry_find():

    registry = (
        PolicyRegistry()
    )

    policy = Policy(
        category="command",
        maximum_risk=Risk.MEDIUM,
        decision=PermissionDecision.ASK,
    )

    registry.register(
        policy,
    )

    assert (
        registry.find(
            "command",
        )
        == policy
    )

    assert (
        registry.find(
            "unknown",
        )
        is None
    )