import pytest

from brain.environment.models.command import (
    Command,
)

from brain.environment.models.command_result import (
    CommandResult,
)

from brain.environment.terminals.safety_terminal import (
    SafetyTerminal,
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
        result=None,
        error=None,
    ):

        self.result = result
        self.error = error
        self.executed = False

    def execute(
        self,
        command,
    ):

        self.executed = True

        if self.error is not None:

            raise self.error

        return self.result


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


def create_logging():

    store = ActionLogStore()

    service = LoggingService(
        store,
    )

    return service, store


def test_execution_success_is_logged():

    terminal = FakeTerminal(
        result=CommandResult(
            return_code=0,
            stdout="hello",
            stderr="",
        ),
    )

    logging_service, store = (
        create_logging()
    )

    safety_terminal = SafetyTerminal(
        create_safety_service(
            PermissionDecision.ALLOW,
        ),
        terminal,
        logging_service,
    )

    result = safety_terminal.execute(
        Command(
            "echo hello",
        )
    )

    assert (
        result.return_code
        == 0
    )

    logs = store.all()

    assert [
        log.event
        for log in logs
    ] == [
        ActionLogEvent.EXECUTION_STARTED,
        ActionLogEvent.EXECUTION_COMPLETED,
    ]

    assert (
        logs[0].status
        == ActionLogStatus.RUNNING
    )

    assert (
        logs[1].status
        == ActionLogStatus.COMPLETED
    )


def test_execution_failure_result_is_logged():

    terminal = FakeTerminal(
        result=CommandResult(
            return_code=1,
            stdout="",
            stderr="command failed",
        ),
    )

    logging_service, store = (
        create_logging()
    )

    safety_terminal = SafetyTerminal(
        create_safety_service(
            PermissionDecision.ALLOW,
        ),
        terminal,
        logging_service,
    )

    result = safety_terminal.execute(
        Command(
            "bad command",
        )
    )

    assert (
        result.return_code
        == 1
    )

    logs = store.all()

    assert [
        log.event
        for log in logs
    ] == [
        ActionLogEvent.EXECUTION_STARTED,
        ActionLogEvent.EXECUTION_FAILED,
    ]

    assert (
        logs[1].status
        == ActionLogStatus.FAILED
    )

    assert (
        logs[1].metadata[
            "return_code"
        ]
        == 1
    )


def test_execution_exception_is_logged():

    terminal = FakeTerminal(
        error=RuntimeError(
            "terminal failure",
        ),
    )

    logging_service, store = (
        create_logging()
    )

    safety_terminal = SafetyTerminal(
        create_safety_service(
            PermissionDecision.ALLOW,
        ),
        terminal,
        logging_service,
    )

    with pytest.raises(
        RuntimeError,
    ):

        safety_terminal.execute(
            Command(
                "echo hello",
            )
        )

    logs = store.all()

    assert [
        log.event
        for log in logs
    ] == [
        ActionLogEvent.EXECUTION_STARTED,
        ActionLogEvent.EXECUTION_FAILED,
    ]

    assert (
        logs[1].metadata[
            "error"
        ]
        == "terminal failure"
    )


def test_denied_action_does_not_start_execution():

    terminal = FakeTerminal(
        result=CommandResult(
            return_code=0,
            stdout="hello",
            stderr="",
        ),
    )

    logging_service, store = (
        create_logging()
    )

    safety_terminal = SafetyTerminal(
        create_safety_service(
            PermissionDecision.DENY,
        ),
        terminal,
        logging_service,
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

    assert (
        all(
            log.event
            != ActionLogEvent.EXECUTION_STARTED
            for log in store.all()
        )
    )