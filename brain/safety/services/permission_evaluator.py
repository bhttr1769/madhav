from brain.safety.models.action import (
    Action,
)

from brain.safety.models.permission_decision import (
    PermissionDecision,
)

from brain.safety.models.risk import (
    Risk,
)

from brain.safety.registries.policy_registry import (
    PolicyRegistry,
)


class PermissionEvaluator:
    """
    Evaluates whether an action is permitted
    according to registered safety policies.
    """

    def __init__(
        self,
        registry: PolicyRegistry,
    ):

        self._registry = registry

    def evaluate(
        self,
        action: Action,
        risk: Risk,
    ) -> PermissionDecision:

        policy = (
            self._registry.find(
                action.category,
            )
        )

        if policy is None:

            return (
                PermissionDecision.DENY
            )

        if (
            risk.value
            > policy.maximum_risk.value
        ):

            return (
                PermissionDecision.DENY
            )

        return policy.decision