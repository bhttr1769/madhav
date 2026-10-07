from brain.agents.context_source import ContextSource
from brain.agents.context_source_coordinator import ContextSourceCoordinator
from brain.agents.context_source_status import ContextSourceStatus
from brain.agents.models.context_source_result import ContextSourceResult


class FakeProvider:
    def __init__(self, source, value):
        self.source = source
        self.value = value

    def provide(self):
        return ContextSourceResult(
            source=self.source,
            status=ContextSourceStatus.AVAILABLE,
            value=self.value,
        )


class FailingProvider:
    def __init__(self, source):
        self.source = source

    def provide(self):
        raise RuntimeError("source failure")


def test_coordinator_returns_available_source():
    coordinator = ContextSourceCoordinator()

    project = object()

    results = coordinator.coordinate(
        providers=(
            FakeProvider(ContextSource.PROJECT, project),
        ),
        requested_sources=frozenset({
            ContextSource.PROJECT,
        }),
    )

    result = results[ContextSource.PROJECT]

    assert result.status == ContextSourceStatus.AVAILABLE
    assert result.value is project


def test_unrequested_source_is_marked_not_requested():
    coordinator = ContextSourceCoordinator()

    results = coordinator.coordinate(
        providers=(),
        requested_sources=frozenset(),
    )

    assert (
        results[ContextSource.PROJECT].status
        == ContextSourceStatus.NOT_REQUESTED
    )


def test_requested_source_without_provider_is_unavailable():
    coordinator = ContextSourceCoordinator()

    results = coordinator.coordinate(
        providers=(),
        requested_sources=frozenset({
            ContextSource.PROJECT,
        }),
    )

    assert (
        results[ContextSource.PROJECT].status
        == ContextSourceStatus.UNAVAILABLE
    )


def test_provider_failure_is_recorded():
    coordinator = ContextSourceCoordinator()

    results = coordinator.coordinate(
        providers=(
            FailingProvider(ContextSource.MEMORY),
        ),
        requested_sources=frozenset({
            ContextSource.MEMORY,
        }),
    )

    result = results[ContextSource.MEMORY]

    assert result.status == ContextSourceStatus.FAILED
    assert isinstance(result.error, RuntimeError)


def test_multiple_sources_are_coordinated():
    coordinator = ContextSourceCoordinator()

    project = object()
    environment = object()

    results = coordinator.coordinate(
        providers=(
            FakeProvider(ContextSource.PROJECT, project),
            FakeProvider(ContextSource.ENVIRONMENT, environment),
        ),
        requested_sources=frozenset({
            ContextSource.PROJECT,
            ContextSource.ENVIRONMENT,
        }),
    )

    assert results[ContextSource.PROJECT].value is project
    assert results[ContextSource.ENVIRONMENT].value is environment

    assert (
        results[ContextSource.MEMORY].status
        == ContextSourceStatus.NOT_REQUESTED
    )


def test_coordinator_does_not_modify_provider_values():
    coordinator = ContextSourceCoordinator()

    project = object()
    provider = FakeProvider(ContextSource.PROJECT, project)

    results = coordinator.coordinate(
        providers=(provider,),
        requested_sources=frozenset({
            ContextSource.PROJECT,
        }),
    )

    assert provider.value is project
    assert results[ContextSource.PROJECT].value is project