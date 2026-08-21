from brain.safety.models.action import (
    Action,
)

from brain.safety.models.approval_response import (
    ApprovalResponse,
)

from brain.safety.models.permission_decision import (
    PermissionDecision,
)

from brain.safety.registries.policy_registry import (
    PolicyRegistry,
)

from brain.safety.registries.risk_classifier_registry import (
    RiskClassifierRegistry,
)

from brain.safety.services.approval_service import (
    ApprovalService,
)

from brain.safety.services.execution_guard import (
    ExecutionGuard,
)

from brain.safety.services.permission_evaluator import (
    PermissionEvaluator,
)

from brain.safety.services.risk_classifier import (
    RiskClassifier,
)


class SafetyService:
    """
    Coordinates risk classification,
    permission evaluation, approval,
    and execution authorization.
    """

    def __init__(
        self,
        risk_registry: RiskClassifierRegistry,
        policy_registry: PolicyRegistry,
    ):

        self._risk_classifier = (
            RiskClassifier(
                risk_registry,
            )
        )

        self._permission_evaluator = (
            PermissionEvaluator(
                policy_registry,
            )
        )

        self._approval_service = (
            ApprovalService()
        )

        self._execution_guard = (
            ExecutionGuard()
        )

    def evaluate(
        self,
        action: Action,
    ) -> PermissionDecision:

        risk = (
            self._risk_classifier.classify(
                action,
            )
        )

        return (
            self._permission_evaluator.evaluate(
                action,
                risk,
            )
        )

    def authorize(
        self,
        action: Action,
        approval: ApprovalResponse | None = None,
    ) -> None:

        risk = (
            self._risk_classifier.classify(
                action,
            )
        )

        decision = (
            self._permission_evaluator.evaluate(
                action,
                risk,
            )
        )

        self._execution_guard.authorize(
            action,
            decision,
            approval,
        )