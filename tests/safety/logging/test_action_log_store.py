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

from brain.safety.logging.stores.action_log_store import (
    ActionLogStore,
)

from brain.safety.models.action import (
    Action,
)


def create_log(
    log_id,
):

    return ActionLog(
        id=log_id,
        action=Action(
            name="execute",
            category="command",
            target="echo hello",
        ),
        timestamp=datetime.now(),
        event=ActionLogEvent.REQUESTED,
        status=ActionLogStatus.PENDING,
        metadata={},
    )


def test_append_and_get():

    store = ActionLogStore()

    log = create_log(
        "test-1",
    )

    store.append(
        log,
    )

    assert (
        store.get("test-1")
        == log
    )


def test_all_preserves_order():

    store = ActionLogStore()

    first = create_log(
        "test-1",
    )

    second = create_log(
        "test-2",
    )

    store.append(first)
    store.append(second)

    assert (
        store.all()
        == [
            first,
            second,
        ]
    )


def test_count():

    store = ActionLogStore()

    assert (
        store.count()
        == 0
    )

    store.append(
        create_log("test-1"),
    )

    store.append(
        create_log("test-2"),
    )

    assert (
        store.count()
        == 2
    )


def test_missing_log_returns_none():

    store = ActionLogStore()

    assert (
        store.get("missing")
        is None
    )


def test_clear():

    store = ActionLogStore()

    store.append(
        create_log("test-1"),
    )

    store.append(
        create_log("test-2"),
    )

    store.clear()

    assert (
        store.count()
        == 0
    )

    assert (
        store.all()
        == []
    )


def test_all_returns_copy():

    store = ActionLogStore()

    log = create_log(
        "test-1",
    )

    store.append(log)

    logs = store.all()

    logs.clear()

    assert (
        store.count()
        == 1
    )