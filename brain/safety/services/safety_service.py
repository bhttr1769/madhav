from brain.safety.models.action import (
    Action,
)

from brain.safety.models.approval_response import (
    ApprovalResponse,
)

from brain.safety.models.permission_decision import (
    PermissionDecision,
)

from brain.safety.models.risk import (
    Risk,
)

from brain.safety.logging.models.action_log_event import (
    ActionLogEvent,
)

from brain.safety.logging.models.action_log_status import (
    ActionLogStatus,
)

from brain.safety.logging.services.logging_service import (
    LoggingService,
)

from brain.safety.logging.stores.action_log_store import (
    ActionLogStore,
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
    execution authorization, and
    safety action logging.
    """

    def __init__(
        self,
        risk_registry: RiskClassifierRegistry,
        policy_registry: PolicyRegistry,
        logging_service: LoggingService | None = None,
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

        self._logging_service = (
            logging_service
            if logging_service is not None
            else LoggingService(
                ActionLogStore(),
            )
        )

    def _evaluate(
        self,
        action: Action,
    ) -> tuple[
        PermissionDecision,
        Risk,
    ]:

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

        return (
            decision,
            risk,
        )

    def evaluate(
        self,
        action: Action,
    ) -> PermissionDecision:

        self._logging_service.log(
            action=action,
            event=ActionLogEvent.REQUESTED,
            status=ActionLogStatus.PENDING,
        )

        decision, risk = (
            self._evaluate(
                action,
            )
        )

        if (
            decision
            == PermissionDecision.ALLOW
        ):

            status = (
                ActionLogStatus.ALLOWED
            )

        elif (
            decision
            == PermissionDecision.DENY
        ):

            status = (
                ActionLogStatus.DENIED
            )

        else:

            status = (
                ActionLogStatus.WAITING_APPROVAL
            )

        self._logging_service.log(
            action=action,
            event=ActionLogEvent.EVALUATED,
            status=status,
            metadata={
                "risk": risk.value,
                "decision": decision.value,
            },
        )

        return decision

    def authorize(
        self,
        action: Action,
        approval: ApprovalResponse | None = None,
    ) -> None:

        decision, risk = (
            self._evaluate(
                action,
            )
        )

        if (
            decision
            == PermissionDecision.ALLOW
        ):

            self._logging_service.log(
                action=action,
                event=ActionLogEvent.ALLOWED,
                status=ActionLogStatus.ALLOWED,
                metadata={
                    "risk": risk.value,
                },
            )

        elif (
            decision
            == PermissionDecision.DENY
        ):

            self._logging_service.log(
                action=action,
                event=ActionLogEvent.DENIED,
                status=ActionLogStatus.DENIED,
                metadata={
                    "risk": risk.value,
                },
            )

        elif (
            decision
            == PermissionDecision.ASK
        ):

            if (
                approval
                == ApprovalResponse.APPROVE
            ):

                self._logging_service.log(
                    action=action,
                    event=(
                        ActionLogEvent
                        .APPROVAL_GRANTED
                    ),
                    status=(
                        ActionLogStatus.ALLOWED
                    ),
                    metadata={
                        "risk": risk.value,
                    },
                )

            elif (
                approval
                == ApprovalResponse.REJECT
            ):

                self._logging_service.log(
                    action=action,
                    event=(
                        ActionLogEvent
                        .APPROVAL_REJECTED
                    ),
                    status=(
                        ActionLogStatus.DENIED
                    ),
                    metadata={
                        "risk": risk.value,
                    },
                )

                self._logging_service.log(
                    action=action,
                    event=ActionLogEvent.CANCELLED,
                    status=ActionLogStatus.FAILED,
                    metadata={
                        "reason": (
                            "User rejected approval."
                        ),
                    },
                )

        self._execution_guard.authorize(
            action,
            decision,
            approval,
        )