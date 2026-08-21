import pytest

from brain.environment.models.command import (
    Command,
)

from brain.environment.terminals.safety_terminal import (
    SafetyTerminal,
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


class FakeTerminal:

    def __init__(
        self,
    ):

        self.executed = False

    def execute(
        self,
        command,
    ):

        self.executed = True

        return None


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

    return SafetyService(
        risk_registry,
        policy_registry,
    )


def test_safety_terminal_allows():

    terminal = FakeTerminal()

    safety_terminal = SafetyTerminal(
        create_safety_service(
            PermissionDecision.ALLOW,
        ),
        terminal,
    )

    safety_terminal.execute(
        Command(
            "echo hello",
        )
    )

    assert (
        terminal.executed
        is True
    )


def test_safety_terminal_blocks():

    terminal = FakeTerminal()

    safety_terminal = SafetyTerminal(
        create_safety_service(
            PermissionDecision.DENY,
        ),
        terminal,
    )

    with pytest.raises(
        PermissionError,
    ):

        safety_terminal.execute(
            Command(
                "echo hello",
            )
        )

    assert (
        terminal.executed
        is False
    )


def test_safety_terminal_requires_approval():

    terminal = FakeTerminal()

    safety_terminal = SafetyTerminal(
        create_safety_service(
            PermissionDecision.ASK,
        ),
        terminal,
    )

    with pytest.raises(
        PermissionError,
    ):

        safety_terminal.execute(
            Command(
                "echo hello",
            )
        )

    assert (
        terminal.executed
        is False
    )


def test_safety_terminal_approved():

    terminal = FakeTerminal()

    safety_terminal = SafetyTerminal(
        create_safety_service(
            PermissionDecision.ASK,
        ),
        terminal,
    )

    safety_terminal.execute(
        Command(
            "echo hello",
        ),
        ApprovalResponse.APPROVE,
    )

    assert (
        terminal.executed
        is True
    )

def test_safety_terminal_executes_real_terminal():

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

    safety_service = SafetyService(
        risk_registry,
        policy_registry,
    )

    terminal = SafetyTerminal(
        safety_service,
    )

    result = terminal.execute(
        Command(
            "echo hello",
        )
    )

    assert (
        result.return_code
        == 0
    )

    assert (
        "hello"
        in result.stdout.lower()
    )