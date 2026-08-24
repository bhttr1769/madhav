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


def create_action():

    return Action(
        name="execute",
        category="command",
        target="echo hello",
    )


def test_logging_service_creates_log():

    store = ActionLogStore()

    service = LoggingService(
        store,
    )

    action = create_action()

    log = service.log(
        action=action,
        event=ActionLogEvent.REQUESTED,
        status=ActionLogStatus.PENDING,
    )

    assert (
        log.action
        == action
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


def test_logging_service_stores_log():

    store = ActionLogStore()

    service = LoggingService(
        store,
    )

    log = service.log(
        action=create_action(),
        event=ActionLogEvent.EVALUATED,
        status=ActionLogStatus.ALLOWED,
    )

    assert (
        store.count()
        == 1
    )

    assert (
        store.get(log.id)
        == log
    )


def test_logging_service_generates_unique_ids():

    store = ActionLogStore()

    service = LoggingService(
        store,
    )

    first = service.log(
        action=create_action(),
        event=ActionLogEvent.REQUESTED,
        status=ActionLogStatus.PENDING,
    )

    second = service.log(
        action=create_action(),
        event=ActionLogEvent.REQUESTED,
        status=ActionLogStatus.PENDING,
    )

    assert (
        first.id
        != second.id
    )


def test_logging_service_records_metadata():

    store = ActionLogStore()

    service = LoggingService(
        store,
    )

    metadata = {
        "source": "safety",
        "reason": "policy matched",
    }

    log = service.log(
        action=create_action(),
        event=ActionLogEvent.EVALUATED,
        status=ActionLogStatus.ALLOWED,
        metadata=metadata,
    )

    assert (
        log.metadata
        == metadata
    )


def test_logging_service_copies_metadata():

    store = ActionLogStore()

    service = LoggingService(
        store,
    )

    metadata = {
        "source": "safety",
    }

    log = service.log(
        action=create_action(),
        event=ActionLogEvent.EVALUATED,
        status=ActionLogStatus.ALLOWED,
        metadata=metadata,
    )

    metadata["source"] = "changed"

    assert (
        log.metadata["source"]
        == "safety"
    )


def test_logging_service_records_multiple_events():

    store = ActionLogStore()

    service = LoggingService(
        store,
    )

    action = create_action()

    first = service.log(
        action=action,
        event=ActionLogEvent.REQUESTED,
        status=ActionLogStatus.PENDING,
    )

    second = service.log(
        action=action,
        event=ActionLogEvent.EVALUATED,
        status=ActionLogStatus.ALLOWED,
    )

    third = service.log(
        action=action,
        event=ActionLogEvent.EXECUTION_STARTED,
        status=ActionLogStatus.RUNNING,
    )

    assert (
        store.all()
        == [
            first,
            second,
            third,
        ]
    )

def test_logging_service_sanitizes_metadata():

    store = ActionLogStore()

    service = LoggingService(
        store,
    )

    log = service.log(
        action=create_action(),
        event=ActionLogEvent.REQUESTED,
        status=ActionLogStatus.PENDING,
        metadata={
            "password": "secret123",
            "source": "test",
        },
    )

    assert (
        log.metadata["password"]
        == "[REDACTED]"
    )

    assert (
        log.metadata["source"]
        == "test"
    )


def test_logging_service_sanitizes_action():

    store = ActionLogStore()

    service = LoggingService(
        store,
    )

    action = Action(
        name="execute",
        category="command",
        target=(
            "connect password=secret123"
        ),
    )

    log = service.log(
        action=action,
        event=ActionLogEvent.REQUESTED,
        status=ActionLogStatus.PENDING,
    )

    assert (
        "secret123"
        not in log.action.target
    )