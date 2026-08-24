from datetime import datetime
from datetime import timedelta

from brain.safety.logging.models.action_log import (
    ActionLog,
)

from brain.safety.logging.models.action_log_event import (
    ActionLogEvent,
)

from brain.safety.logging.models.action_log_status import (
    ActionLogStatus,
)

from brain.safety.logging.services.retention_service import (
    RetentionService,
)

from brain.safety.logging.stores.action_log_store import (
    ActionLogStore,
)

from brain.safety.models.action import (
    Action,
)


def create_log(
    log_id,
    timestamp,
):

    return ActionLog(
        id=log_id,
        action=Action(
            name="execute",
            category="command",
            target="echo hello",
        ),
        timestamp=timestamp,
        event=ActionLogEvent.REQUESTED,
        status=ActionLogStatus.PENDING,
        metadata={},
    )


def test_purge_removes_old_logs():

    store = ActionLogStore()

    now = datetime.now()

    old_log = create_log(
        "old",
        now - timedelta(
            days=31,
        ),
    )

    new_log = create_log(
        "new",
        now - timedelta(
            days=5,
        ),
    )

    store.append(old_log)
    store.append(new_log)

    retention = RetentionService(
        store,
        retention_days=30,
    )

    removed = retention.purge(
        now=now,
    )

    assert (
        removed
        == 1
    )

    assert (
        store.all()
        == [
            new_log,
        ]
    )


def test_purge_keeps_recent_logs():

    store = ActionLogStore()

    now = datetime.now()

    log = create_log(
        "recent",
        now - timedelta(
            days=5,
        ),
    )

    store.append(log)

    retention = RetentionService(
        store,
        retention_days=30,
    )

    removed = retention.purge(
        now=now,
    )

    assert (
        removed
        == 0
    )

    assert (
        store.all()
        == [
            log,
        ]
    )


def test_negative_retention_is_rejected():

    store = ActionLogStore()

    try:

        RetentionService(
            store,
            retention_days=-1,
        )

        assert False

    except ValueError:

        pass