from datetime import datetime

from brain.safety.logging.models.action_log import (
    ActionLog,
)

from brain.safety.logging.models.action_log_event import (
    ActionLogEvent,
)

from brain.safety.logging.models.action_log_status import (
    ActionLogStatus,
)

from brain.safety.models.action import (
    Action,
)


def test_action_log_creation():

    action = Action(
        name="execute",
        category="command",
        target="echo hello",
    )

    timestamp = datetime.now()

    log = ActionLog(
        id="test-1",
        action=action,
        timestamp=timestamp,
        event=ActionLogEvent.REQUESTED,
        status=ActionLogStatus.PENDING,
        metadata={},
    )

    assert (
        log.id
        == "test-1"
    )

    assert (
        log.action
        == action
    )

    assert (
        log.timestamp
        == timestamp
    )

    assert (
        log.event
        == ActionLogEvent.REQUESTED
    )

    assert (
        log.status
        == ActionLogStatus.PENDING
    )

    assert (
        log.metadata
        == {}
    )


def test_action_log_is_immutable():

    action = Action(
        name="execute",
        category="command",
        target="echo hello",
    )

    log = ActionLog(
        id="test-1",
        action=action,
        timestamp=datetime.now(),
        event=ActionLogEvent.REQUESTED,
        status=ActionLogStatus.PENDING,
        metadata={},
    )

    try:

        log.status = (
            ActionLogStatus.COMPLETED
        )

        assert False

    except (
        AttributeError
    ):

        pass