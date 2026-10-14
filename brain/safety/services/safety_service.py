from datetime import datetime, timezone
from typing import Protocol

from brain.organization.authority_evaluation_service import (
    AuthorityEvaluationService,
)
from brain.organization.authority_execution_context import (
    get_authority_execution_context,
)
from brain.organization.models.authority_decision import AuthorityDecision
from brain.organization.models.organization_persistence_state import (
    OrganizationPersistenceState,
)
from brain.safety.logging.models.action_log_event import ActionLogEvent
from brain.safety.logging.models.action_log_status import ActionLogStatus
from brain.safety.logging.services.logging_service import LoggingService
from brain.safety.logging.stores.action_log_store import ActionLogStore
from brain.safety.models.action import Action
from brain.safety.models.approval_response import ApprovalResponse
from brain.safety.models.permission_decision import PermissionDecision
from brain.safety.models.risk import Risk
from brain.safety.registries.policy_registry import PolicyRegistry
from brain.safety.registries.risk_classifier_registry import (
    RiskClassifierRegistry,
)
from brain.safety.services.approval_service import ApprovalService
from brain.safety.services.execution_guard import ExecutionGuard
from brain.safety.services.permission_evaluator import PermissionEvaluator
from brain.safety.services.risk_classifier import RiskClassifier


class OrganizationPersistence(Protocol):
    """Interface required by organizational authority enforcement."""

    def load(
        self,
        organization_id: str,
    ) -> OrganizationPersistenceState:
        ...


class SafetyService:
    """
    Coordinate safety policy, risk evaluation, approval, and execution.

    When organizational authority is configured, it is evaluated independently
    and must allow the action before safety approval can authorize execution.
    """

    def __init__(
        self,
        risk_registry: RiskClassifierRegistry,
        policy_registry: PolicyRegistry,
        logging_service: LoggingService | None = None,
        *,
        organization_persistence: OrganizationPersistence | None = None,
        authority_evaluation_service: (
            AuthorityEvaluationService | None
        ) = None,
    ) -> None:
        if (
            organization_persistence is None
        ) != (
            authority_evaluation_service is None
        ):
            raise ValueError(
                "organization_persistence and "
                "authority_evaluation_service must be configured together"
            )

        if authority_evaluation_service is not None and not isinstance(
            authority_evaluation_service,
            AuthorityEvaluationService,
        ):
            raise TypeError(
                "authority_evaluation_service must be an "
                "AuthorityEvaluationService or None"
            )

        if organization_persistence is not None and not callable(
            getattr(organization_persistence, "load", None)
        ):
            raise TypeError(
                "organization_persistence must provide a callable load method"
            )

        self._risk_classifier = RiskClassifier(risk_registry)
        self._permission_evaluator = PermissionEvaluator(policy_registry)
        self._approval_service = ApprovalService()
        self._execution_guard = ExecutionGuard()
        self._organization_persistence = organization_persistence
        self._authority_evaluation_service = authority_evaluation_service
        self._logging_service = (
            logging_service
            if logging_service is not None
            else LoggingService(ActionLogStore())
        )

    def _evaluate(self, action: Action) -> tuple[PermissionDecision, Risk]:
        risk = self._risk_classifier.classify(action)
        decision = self._permission_evaluator.evaluate(action, risk)
        return decision, risk

    def _organizational_authority(
        self,
        action: Action,
    ) -> AuthorityDecision | None:
        """
        Return None when organizational enforcement is not configured.

        When configured, missing or invalid execution context and persistence
        failures produce a denial instead of bypassing organizational checks.
        """
        if self._organization_persistence is None:
            return None

        authority_service = self._authority_evaluation_service
        if authority_service is None:
            # Defensive fail-closed behavior if the configuration is corrupted.
            return AuthorityDecision(
                allowed=False,
                reason="Organizational authority evaluation is not configured.",
            )

        context = get_authority_execution_context()

        if context is None:
            return AuthorityDecision(
                allowed=False,
                reason="No trusted execution context is available.",
            )

        if context.organization_id is None:
            return AuthorityDecision(
                allowed=False,
                reason="Execution context has no organization ID.",
            )

        try:
            # Reload every time so revocations and membership changes take effect.
            state = self._organization_persistence.load(
                context.organization_id
            )
        except Exception:
            # Do not allow execution when the authoritative snapshot is
            # unavailable or cannot be read.
            return AuthorityDecision(
                allowed=False,
                reason="Organization snapshot could not be loaded.",
            )

        if not isinstance(state, OrganizationPersistenceState):
            return AuthorityDecision(
                allowed=False,
                reason="Organization persistence returned an invalid snapshot.",
            )

        if state.organization.id != context.organization_id:
            return AuthorityDecision(
                allowed=False,
                reason="Organization snapshot does not match the execution context.",
            )

        return authority_service.evaluate(
            organization=state.organization,
            memberships=state.memberships,
            delegations=state.delegations,
            requesting_agent_id=context.agent_id,
            action=action.name,
            target=action.target,
            at=datetime.now(timezone.utc),
        )

    def evaluate(self, action: Action) -> PermissionDecision:
        self._logging_service.log(
            action=action,
            event=ActionLogEvent.REQUESTED,
            status=ActionLogStatus.PENDING,
        )

        authority_decision = self._organizational_authority(action)

        if (
            authority_decision is not None
            and not authority_decision.allowed
        ):
            self._logging_service.log(
                action=action,
                event=ActionLogEvent.EVALUATED,
                status=ActionLogStatus.DENIED,
                metadata={
                    "decision": PermissionDecision.DENY.value,
                    "organizational_authority": authority_decision.reason,
                },
            )
            return PermissionDecision.DENY

        decision, risk = self._evaluate(action)

        if decision == PermissionDecision.ALLOW:
            status = ActionLogStatus.ALLOWED
        elif decision == PermissionDecision.DENY:
            status = ActionLogStatus.DENIED
        else:
            status = ActionLogStatus.WAITING_APPROVAL

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
        # Organizational authority is a prerequisite, not an approvable
        # safety-policy decision. User approval cannot override its denial.
        authority_decision = self._organizational_authority(action)

        if (
            authority_decision is not None
            and not authority_decision.allowed
        ):
            self._logging_service.log(
                action=action,
                event=ActionLogEvent.DENIED,
                status=ActionLogStatus.DENIED,
                metadata={
                    "organizational_authority": authority_decision.reason,
                },
            )
            raise PermissionError(
                "Organizational authority denied the action: "
                f"{authority_decision.reason}"
            )

        decision, risk = self._evaluate(action)

        if decision == PermissionDecision.ALLOW:
            self._logging_service.log(
                action=action,
                event=ActionLogEvent.ALLOWED,
                status=ActionLogStatus.ALLOWED,
                metadata={"risk": risk.value},
            )

        elif decision == PermissionDecision.DENY:
            self._logging_service.log(
                action=action,
                event=ActionLogEvent.DENIED,
                status=ActionLogStatus.DENIED,
                metadata={"risk": risk.value},
            )

        elif decision == PermissionDecision.ASK:
            if approval == ApprovalResponse.APPROVE:
                self._logging_service.log(
                    action=action,
                    event=ActionLogEvent.APPROVAL_GRANTED,
                    status=ActionLogStatus.ALLOWED,
                    metadata={"risk": risk.value},
                )

            elif approval == ApprovalResponse.REJECT:
                self._logging_service.log(
                    action=action,
                    event=ActionLogEvent.APPROVAL_REJECTED,
                    status=ActionLogStatus.DENIED,
                    metadata={"risk": risk.value},
                )
                self._logging_service.log(
                    action=action,
                    event=ActionLogEvent.CANCELLED,
                    status=ActionLogStatus.FAILED,
                    metadata={"reason": "User rejected approval."},
                )

        self._execution_guard.authorize(action, decision, approval)