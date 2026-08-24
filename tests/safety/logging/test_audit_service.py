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

from brain.safety.logging.services.audit_service import (
    AuditService,
)

from brain.safety.logging.stores.action_log_store import (
    ActionLogStore,
)

from brain.safety.models.action import (
    Action,
)


def create_log(
    log_id,
    category,
    event,
    status,
    timestamp=None,
):

    return ActionLog(
        id=log_id,
        action=Action(
            name="execute",
            category=category,
            target="echo hello",
        ),
        timestamp=(
            timestamp
            if timestamp is not None
            else datetime.now()
        ),
        event=event,
        status=status,
        metadata={},
    )


def create_service():

    store = ActionLogStore()

    service = AuditService(
        store,
    )

    return service, store


def test_all():

    service, store = (
        create_service()
    )

    first = create_log(
        "1",
        "command",
        ActionLogEvent.REQUESTED,
        ActionLogStatus.PENDING,
    )

    second = create_log(
        "2",
        "package",
        ActionLogEvent.EXECUTION_STARTED,
        ActionLogStatus.RUNNING,
    )

    store.append(first)
    store.append(second)

    assert (
        service.all()
        == [
            first,
            second,
        ]
    )


def test_get():

    service, store = (
        create_service()
    )

    log = create_log(
        "test-id",
        "command",
        ActionLogEvent.REQUESTED,
        ActionLogStatus.PENDING,
    )

    store.append(log)

    assert (
        service.get("test-id")
        == log
    )


def test_get_missing():

    service, _ = (
        create_service()
    )

    assert (
        service.get("missing")
        is None
    )


def test_by_event():

    service, store = (
        create_service()
    )

    requested = create_log(
        "1",
        "command",
        ActionLogEvent.REQUESTED,
        ActionLogStatus.PENDING,
    )

    completed = create_log(
        "2",
        "command",
        ActionLogEvent.EXECUTION_COMPLETED,
        ActionLogStatus.COMPLETED,
    )

    store.append(requested)
    store.append(completed)

    assert (
        service.by_event(
            ActionLogEvent.REQUESTED,
        )
        == [
            requested,
        ]
    )


def test_by_status():

    service, store = (
        create_service()
    )

    pending = create_log(
        "1",
        "command",
        ActionLogEvent.REQUESTED,
        ActionLogStatus.PENDING,
    )

    failed = create_log(
        "2",
        "command",
        ActionLogEvent.EXECUTION_FAILED,
        ActionLogStatus.FAILED,
    )

    store.append(pending)
    store.append(failed)

    assert (
        service.by_status(
            ActionLogStatus.FAILED,
        )
        == [
            failed,
        ]
    )


def test_by_category():

    service, store = (
        create_service()
    )

    command = create_log(
        "1",
        "command",
        ActionLogEvent.REQUESTED,
        ActionLogStatus.PENDING,
    )

    package = create_log(
        "2",
        "package",
        ActionLogEvent.REQUESTED,
        ActionLogStatus.PENDING,
    )

    store.append(command)
    store.append(package)

    assert (
        service.by_category(
            "command",
        )
        == [
            command,
        ]
    )


def test_between():

    service, store = (
        create_service()
    )

    now = datetime.now()

    old = create_log(
        "1",
        "command",
        ActionLogEvent.REQUESTED,
        ActionLogStatus.PENDING,
        now - timedelta(
            minutes=10,
        ),
    )

    current = create_log(
        "2",
        "command",
        ActionLogEvent.REQUESTED,
        ActionLogStatus.PENDING,
        now,
    )

    future = create_log(
        "3",
        "command",
        ActionLogEvent.REQUESTED,
        ActionLogStatus.PENDING,
        now + timedelta(
            minutes=10,
        ),
    )

    store.append(old)
    store.append(current)
    store.append(future)

    results = service.between(
        now - timedelta(
            minutes=1,
        ),
        now + timedelta(
            minutes=1,
        ),
    )

    assert (
        results
        == [
            current,
        ]
    )


def test_count():

    service, store = (
        create_service()
    )

    assert (
        service.count()
        == 0
    )

    store.append(
        create_log(
            "1",
            "command",
            ActionLogEvent.REQUESTED,
            ActionLogStatus.PENDING,
        )
    )

    assert (
        service.count()
        == 1
    )