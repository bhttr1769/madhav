import pytest

from brain.agents.agent_context_builder import AgentContextBuilder
from brain.agents.agent_context_integrator import AgentContextIntegrator
from brain.agents.agent_runtime import AgentRuntime
from brain.agents.context_source import ContextSource
from brain.agents.context_source_coordinator import ContextSourceCoordinator
from brain.agents.context_source_status import ContextSourceStatus
from brain.agents.models.agent_definition import AgentDefinition
from brain.agents.models.agent_identity import AgentIdentity
from brain.agents.models.context_source_result import ContextSourceResult
from brain.capabilities.capability_runtime import CapabilityRuntime
from brain.capabilities.models.capability_execution_request import (
    CapabilityExecutionRequest,
)
from brain.capabilities.models.capability_execution_result import (
    CapabilityExecutionResult,
)


class FakeCapabilityRuntime(CapabilityRuntime):
    def __init__(self):
        self.requests = []

    def execute(
        self,
        request: CapabilityExecutionRequest,
    ) -> CapabilityExecutionResult:
        self.requests.append(request)

        return CapabilityExecutionResult(
            capability_id=request.capability_id,
            output=request.input_data,
        )


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


def create_runtime():
    definition = AgentDefinition(
        identity=AgentIdentity(
            id="agent-1",
            name="Test Agent",
        ),
        description="Test agent definition",
        version="1.0.0",
        capabilities=frozenset(),
    )

    return AgentRuntime(
        definition,
        FakeCapabilityRuntime(),
        runtime_id="runtime-1",
    )


def create_integrator():
    return AgentContextIntegrator(
        coordinator=ContextSourceCoordinator(),
        builder=AgentContextBuilder(),
    )


def test_integrator_builds_context_from_available_sources():
    integrator = create_integrator()
    runtime = create_runtime()

    project = object()
    environment = object()

    result = integrator.integrate(
        runtime=runtime,
        providers=(
            FakeProvider(ContextSource.PROJECT, project),
            FakeProvider(ContextSource.ENVIRONMENT, environment),
        ),
        requested_sources=frozenset({
            ContextSource.PROJECT,
            ContextSource.ENVIRONMENT,
        }),
    )

    assert result.context.project is project
    assert result.context.environment is environment


def test_integrator_attaches_actual_runtime():
    integrator = create_integrator()
    runtime = create_runtime()

    result = integrator.integrate(
        runtime=runtime,
        providers=(),
        requested_sources=frozenset(),
    )

    assert result.context.runtime is runtime


def test_integrator_derives_identity_from_runtime():
    integrator = create_integrator()
    runtime = create_runtime()

    result = integrator.integrate(
        runtime=runtime,
        providers=(),
        requested_sources=frozenset(),
    )

    assert result.context.runtime_id == runtime.runtime_id
    assert result.context.agent_id == runtime.agent_id


def test_integrator_does_not_mutate_runtime():
    integrator = create_integrator()
    runtime = create_runtime()

    original_state = runtime.state

    integrator.integrate(
        runtime=runtime,
        providers=(),
        requested_sources=frozenset(),
    )

    assert runtime.state is original_state
    assert runtime.runtime_id == "runtime-1"
    assert runtime.agent_id == "agent-1"


def test_integrator_rejects_invalid_runtime():
    integrator = create_integrator()

    with pytest.raises(TypeError):
        integrator.integrate(
            runtime=object(),
            providers=(),
            requested_sources=frozenset(),
        )


def test_integrator_preserves_source_results():
    integrator = create_integrator()
    runtime = create_runtime()

    project = object()

    result = integrator.integrate(
        runtime=runtime,
        providers=(
            FakeProvider(ContextSource.PROJECT, project),
        ),
        requested_sources=frozenset({
            ContextSource.PROJECT,
        }),
    )

    source_result = result.source_results[ContextSource.PROJECT]

    assert source_result.status == ContextSourceStatus.AVAILABLE
    assert source_result.value is project


def test_unavailable_source_is_not_inserted_into_context():
    integrator = create_integrator()
    runtime = create_runtime()

    result = integrator.integrate(
        runtime=runtime,
        providers=(),
        requested_sources=frozenset({
            ContextSource.PROJECT,
        }),
    )

    assert result.context.project is None

    assert (
        result.source_results[ContextSource.PROJECT].status
        == ContextSourceStatus.UNAVAILABLE
    )


def test_failed_source_is_not_inserted_into_context():
    integrator = create_integrator()
    runtime = create_runtime()

    result = integrator.integrate(
        runtime=runtime,
        providers=(
            FailingProvider(ContextSource.MEMORY),
        ),
        requested_sources=frozenset({
            ContextSource.MEMORY,
        }),
    )

    assert result.context.memory is None

    assert (
        result.source_results[ContextSource.MEMORY].status
        == ContextSourceStatus.FAILED
    )


def test_unrequested_source_is_not_inserted_into_context():
    integrator = create_integrator()
    runtime = create_runtime()

    project = object()

    result = integrator.integrate(
        runtime=runtime,
        providers=(
            FakeProvider(ContextSource.PROJECT, project),
        ),
        requested_sources=frozenset(),
    )

    assert result.context.project is None

    assert (
        result.source_results[ContextSource.PROJECT].status
        == ContextSourceStatus.NOT_REQUESTED
    )


def test_partial_context_is_allowed():
    integrator = create_integrator()
    runtime = create_runtime()

    project = object()

    result = integrator.integrate(
        runtime=runtime,
        providers=(
            FakeProvider(ContextSource.PROJECT, project),
        ),
        requested_sources=frozenset({
            ContextSource.PROJECT,
            ContextSource.MEMORY,
        }),
    )

    assert result.context.project is project
    assert result.context.memory is None

    assert (
        result.source_results[ContextSource.PROJECT].status
        == ContextSourceStatus.AVAILABLE
    )

    assert (
        result.source_results[ContextSource.MEMORY].status
        == ContextSourceStatus.UNAVAILABLE
    )