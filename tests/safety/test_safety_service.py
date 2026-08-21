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

from brain.safety.models.policy import (
    Policy,
)

from brain.safety.models.risk import (
    Risk,
)

from brain.safety.registries.policy_registry import (
    PolicyRegistry,
)

from brain.safety.registries.risk_classifier_registry import (
    RiskClassifierRegistry,
)

from brain.safety.services.safety_service import (
    SafetyService,
)


class FakeRiskClassifier:

    def classify(
        self,
        action,
    ):

        return Risk.LOW


def test_safety_service_allows():

    risk_registry = (
        RiskClassifierRegistry()
    )

    risk_registry.register(
        FakeRiskClassifier(),
    )

    policy_registry = (
        PolicyRegistry()
    )

    policy_registry.register(
        Policy(
            category="command",
            maximum_risk=Risk.LOW,
            decision=PermissionDecision.ALLOW,
        )
    )

    service = SafetyService(
        risk_registry,
        policy_registry,
    )

    decision = service.evaluate(
        Action(
            name="execute",
            category="command",
            target="echo hello",
        )
    )

    assert (
        decision
        == PermissionDecision.ALLOW
    )


def test_safety_service_denies():

    risk_registry = (
        RiskClassifierRegistry()
    )

    risk_registry.register(
        FakeRiskClassifier(),
    )

    policy_registry = (
        PolicyRegistry()
    )

    service = SafetyService(
        risk_registry,
        policy_registry,
    )

    decision = service.evaluate(
        Action(
            name="execute",
            category="unknown",
            target="test",
        )
    )

    assert (
        decision
        == PermissionDecision.DENY
    )


def test_safety_service_requires_approval():

    risk_registry = (
        RiskClassifierRegistry()
    )

    risk_registry.register(
        FakeRiskClassifier(),
    )

    policy_registry = (
        PolicyRegistry()
    )

    policy_registry.register(
        Policy(
            category="command",
            maximum_risk=Risk.LOW,
            decision=PermissionDecision.ASK,
        )
    )

    service = SafetyService(
        risk_registry,
        policy_registry,
    )

    action = Action(
        name="execute",
        category="command",
        target="test",
    )

    decision = service.evaluate(
        action,
    )

    assert (
        decision
        == PermissionDecision.ASK
    )

    service.authorize(
        action,
        ApprovalResponse.APPROVE,
    )

def test_safety_service_rejects_without_approval():

    risk_registry = (
        RiskClassifierRegistry()
    )

    risk_registry.register(
        FakeRiskClassifier(),
    )

    policy_registry = (
        PolicyRegistry()
    )

    policy_registry.register(
        Policy(
            category="command",
            maximum_risk=Risk.LOW,
            decision=PermissionDecision.ASK,
        )
    )

    service = SafetyService(
        risk_registry,
        policy_registry,
    )

    action = Action(
        name="execute",
        category="command",
        target="test",
    )

    with pytest.raises(
        PermissionError,
    ):

        service.authorize(
            action,
        )

def test_safety_service_rejects_explicit_rejection():

    risk_registry = (
        RiskClassifierRegistry()
    )

    risk_registry.register(
        FakeRiskClassifier(),
    )

    policy_registry = (
        PolicyRegistry()
    )

    policy_registry.register(
        Policy(
            category="command",
            maximum_risk=Risk.LOW,
            decision=PermissionDecision.ASK,
        )
    )

    service = SafetyService(
        risk_registry,
        policy_registry,
    )

    action = Action(
        name="execute",
        category="command",
        target="test",
    )

    with pytest.raises(
        PermissionError,
    ):

        service.authorize(
            action,
            ApprovalResponse.REJECT,
        )

class HighRiskClassifier:

    def classify(
        self,
        action,
    ):

        return Risk.HIGH

def test_safety_service_denies_excessive_risk():

    risk_registry = (
        RiskClassifierRegistry()
    )

    risk_registry.register(
        HighRiskClassifier(),
    )

    policy_registry = (
        PolicyRegistry()
    )

    policy_registry.register(
        Policy(
            category="command",
            maximum_risk=Risk.MEDIUM,
            decision=PermissionDecision.ALLOW,
        )
    )

    service = SafetyService(
        risk_registry,
        policy_registry,
    )

    action = Action(
        name="execute",
        category="command",
        target="test",
    )

    decision = service.evaluate(
        action,
    )

    assert (
        decision
        == PermissionDecision.DENY
    )

    with pytest.raises(
        PermissionError,
    ):

        service.authorize(
            action,
        )