from brain.safety.models.action import (
    Action,
)

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

from brain.safety.services.permission_evaluator import (
    PermissionEvaluator,
)


def test_permission_evaluator():

    registry = (
        PolicyRegistry()
    )

    registry.register(
        Policy(
            category="command",
            maximum_risk=Risk.MEDIUM,
            decision=PermissionDecision.ASK,
        )
    )

    evaluator = (
        PermissionEvaluator(
            registry,
        )
    )

    decision = evaluator.evaluate(
        Action(
            name="execute",
            category="command",
            target="test",
        ),
        Risk.MEDIUM,
    )

    assert (
        decision
        == PermissionDecision.ASK
    )


def test_permission_evaluator_denies_excessive_risk():

    registry = (
        PolicyRegistry()
    )

    registry.register(
        Policy(
            category="command",
            maximum_risk=Risk.MEDIUM,
            decision=PermissionDecision.ALLOW,
        )
    )

    evaluator = (
        PermissionEvaluator(
            registry,
        )
    )

    decision = evaluator.evaluate(
        Action(
            name="execute",
            category="command",
            target="test",
        ),
        Risk.HIGH,
    )

    assert (
        decision
        == PermissionDecision.DENY
    )


def test_permission_evaluator_denies_unknown_category():

    registry = (
        PolicyRegistry()
    )

    evaluator = (
        PermissionEvaluator(
            registry,
        )
    )

    decision = evaluator.evaluate(
        Action(
            name="execute",
            category="unknown",
            target="test",
        ),
        Risk.SAFE,
    )

    assert (
        decision
        == PermissionDecision.DENY
    )