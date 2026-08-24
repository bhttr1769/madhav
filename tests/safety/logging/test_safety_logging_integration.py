import pytest

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


def create_safety_service(
    decision,
):

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
            decision=decision,
        )
    )

    store = ActionLogStore()

    logging_service = (
        LoggingService(
            store,
        )
    )

    service = SafetyService(
        risk_registry,
        policy_registry,
        logging_service,
    )

    return (
        service,
        store,
    )


def create_action():

    return Action(
        name="execute",
        category="command",
        target="echo hello",
    )


def test_allow_is_logged():

    service, store = (
        create_safety_service(
            PermissionDecision.ALLOW,
        )
    )

    action = create_action()

    decision = service.evaluate(
        action,
    )

    assert (
        decision
        == PermissionDecision.ALLOW
    )

    logs = store.all()

    assert [
        log.event
        for log in logs
    ] == [
        ActionLogEvent.REQUESTED,
        ActionLogEvent.EVALUATED,
    ]

    assert (
        logs[0].status
        == ActionLogStatus.PENDING
    )

    assert (
        logs[1].status
        == ActionLogStatus.ALLOWED
    )


def test_deny_is_logged():

    service, store = (
        create_safety_service(
            PermissionDecision.DENY,
        )
    )

    action = create_action()

    decision = service.evaluate(
        action,
    )

    assert (
        decision
        == PermissionDecision.DENY
    )

    logs = store.all()

    assert [
        log.event
        for log in logs
    ] == [
        ActionLogEvent.REQUESTED,
        ActionLogEvent.EVALUATED,
    ]

    assert (
        logs[1].status
        == ActionLogStatus.DENIED
    )


def test_approval_granted_is_logged():

    service, store = (
        create_safety_service(
            PermissionDecision.ASK,
        )
    )

    action = create_action()

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

    logs = store.all()

    assert [
        log.event
        for log in logs
    ] == [
        ActionLogEvent.REQUESTED,
        ActionLogEvent.EVALUATED,
        ActionLogEvent.APPROVAL_GRANTED,
    ]


def test_approval_rejection_is_logged():

    service, store = (
        create_safety_service(
            PermissionDecision.ASK,
        )
    )

    action = create_action()

    service.evaluate(
        action,
    )

    with pytest.raises(
        PermissionError,
    ):

        service.authorize(
            action,
            ApprovalResponse.REJECT,
        )

    logs = store.all()

    assert [
        log.event
        for log in logs
    ] == [
        ActionLogEvent.REQUESTED,
        ActionLogEvent.EVALUATED,
        ActionLogEvent.APPROVAL_REJECTED,
        ActionLogEvent.CANCELLED,
    ]


def test_authorize_allow_is_logged():

    service, store = (
        create_safety_service(
            PermissionDecision.ALLOW,
        )
    )

    action = create_action()

    service.authorize(
        action,
    )

    logs = store.all()

    assert [
        log.event
        for log in logs
    ] == [
        ActionLogEvent.ALLOWED,
    ]