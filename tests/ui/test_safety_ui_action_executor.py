import pytest

from brain.safety.models.approval_response import (
    ApprovalResponse,
)

from brain.safety.models.action import (
    Action,
)

from brain.ui.executors.safety_ui_action_executor import (
    SafetyUIActionExecutor,
)

from brain.ui.executors.ui_action_executor import (
    UIActionExecutor,
)

from brain.ui.models.ui_action import (
    UIAction,
)


class FakeSafetyService:

    def __init__(self):
        self.calls = []

    def authorize(
        self,
        action,
        approval=None,
    ):
        self.calls.append(
            (action, approval)
        )


class FakeUIActionExecutor(
    UIActionExecutor,
):

    def __init__(self):
        self.calls = []

    def execute(
        self,
        action,
    ):
        self.calls.append(action)


class FakeLoggingService:

    def __init__(self):
        self.calls = []

    def log(
        self,
        **kwargs,
    ):
        self.calls.append(kwargs)


def create_executor():

    safety_service = FakeSafetyService()
    executor = FakeUIActionExecutor()
    logging_service = FakeLoggingService()

    wrapper = object.__new__(
        SafetyUIActionExecutor
    )

    wrapper._safety_service = safety_service
    wrapper._executor = executor
    wrapper._logging_service = logging_service

    return (
        wrapper,
        safety_service,
        executor,
        logging_service,
    )


def test_ui_action_is_authorized_before_execution():

    (
        wrapper,
        safety_service,
        executor,
        _,
    ) = create_executor()

    action = UIAction(
        action_type="click",
        x=100,
        y=200,
    )

    wrapper.execute(action)

    assert len(safety_service.calls) == 1
    assert len(executor.calls) == 1

    assert safety_service.calls[0][0] == (
        Action(
            name="click",
            category="ui",
            target="x=100;y=200",
        )
    )


def test_approval_is_forwarded():

    (
        wrapper,
        safety_service,
        _,
        _,
    ) = create_executor()

    action = UIAction(
        action_type="click",
        x=100,
        y=200,
    )

    wrapper.execute(
        action,
        ApprovalResponse.APPROVE,
    )

    assert safety_service.calls[0][1] == (
        ApprovalResponse.APPROVE
    )


def test_execution_does_not_happen_when_authorization_fails():

    class RejectingSafetyService:

        def authorize(
            self,
            action,
            approval=None,
        ):
            raise PermissionError(
                "Action is not authorized."
            )

    executor = FakeUIActionExecutor()

    wrapper = object.__new__(
        SafetyUIActionExecutor
    )

    wrapper._safety_service = (
        RejectingSafetyService()
    )

    wrapper._executor = executor

    wrapper._logging_service = (
        FakeLoggingService()
    )

    action = UIAction(
        action_type="click",
        x=100,
        y=200,
    )

    with pytest.raises(
        PermissionError,
    ):
        wrapper.execute(action)

    assert executor.calls == []


def test_executor_receives_original_ui_action():

    (
        wrapper,
        _,
        executor,
        _,
    ) = create_executor()

    action = UIAction(
        action_type="type",
        text="hello",
    )

    wrapper.execute(action)

    assert executor.calls == [
        action
    ]


def test_success_is_logged():

    (
        wrapper,
        _,
        _,
        logging_service,
    ) = create_executor()

    action = UIAction(
        action_type="press",
        key="ENTER",
    )

    wrapper.execute(action)

    assert len(logging_service.calls) == 2

    started = logging_service.calls[0]
    completed = logging_service.calls[1]

    assert (
        started["event"].value
        == "execution_started"
    )

    assert (
        completed["event"].value
        == "execution_completed"
    )

    assert completed["action"] == Action(
        name="press",
        category="ui",
        target="key=ENTER",
    )


def test_execution_failure_is_logged_and_raised():

    class FailingExecutor(
        UIActionExecutor,
    ):

        def execute(
            self,
            action,
        ):
            raise RuntimeError(
                "input failed"
            )

    safety_service = FakeSafetyService()
    logging_service = FakeLoggingService()

    wrapper = object.__new__(
        SafetyUIActionExecutor
    )

    wrapper._safety_service = safety_service
    wrapper._executor = FailingExecutor()
    wrapper._logging_service = logging_service

    action = UIAction(
        action_type="click",
        x=100,
        y=200,
    )

    with pytest.raises(
        RuntimeError,
        match="input failed",
    ):
        wrapper.execute(action)

    assert len(logging_service.calls) == 2

    started = logging_service.calls[0]
    failed = logging_service.calls[1]

    assert (
        started["event"].value
        == "execution_started"
    )

    assert (
        failed["event"].value
        == "execution_failed"
    )

    assert (
        failed["status"].value
        == "failed"
    )