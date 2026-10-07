from brain.agents.agent_context_validator import AgentContextValidator
from brain.agents.context_source import ContextSource
from brain.agents.context_source_status import ContextSourceStatus
from brain.agents.models.agent_context import AgentContext
from brain.agents.models.context_integration_result import (
    ContextIntegrationResult,
)
from brain.agents.models.context_source_result import (
    ContextSourceResult,
)
from brain.agents.agent_runtime import AgentRuntime
from brain.agents.models.agent_definition import AgentDefinition
from brain.agents.models.agent_identity import AgentIdentity
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


def create_runtime(
    runtime_id="runtime-1",
    agent_id="agent-1",
):
    definition = AgentDefinition(
        identity=AgentIdentity(
            id=agent_id,
            name="Test Agent",
        ),
        description="Test agent definition",
        version="1.0.0",
        capabilities=frozenset(),
    )

    return AgentRuntime(
        definition,
        FakeCapabilityRuntime(),
        runtime_id=runtime_id,
    )

def test_validator_accepts_matching_runtime():
    validator = AgentContextValidator()

    runtime = create_runtime()

    context = AgentContext(
        runtime_id="runtime-1",
        agent_id="agent-1",
        runtime=runtime,
    )

    result = validator.validate(context)

    assert result.valid is True
    assert result.errors == ()


def test_validator_rejects_non_runtime_object():
    validator = AgentContextValidator()

    context = AgentContext(
        runtime_id="runtime-1",
        agent_id="agent-1",
        runtime=object(),
    )

    result = validator.validate(context)

    assert result.valid is False
    assert any(
        "AgentRuntime" in error
        for error in result.errors
    )


def test_validator_rejects_runtime_id_mismatch():
    validator = AgentContextValidator()

    runtime = create_runtime(
        runtime_id="runtime-2",
        agent_id="agent-1",
    )

    context = AgentContext(
        runtime_id="runtime-1",
        agent_id="agent-1",
        runtime=runtime,
    )

    result = validator.validate(context)

    assert result.valid is False
    assert any(
        "runtime.runtime_id" in error
        for error in result.errors
    )


def test_validator_rejects_agent_id_mismatch():
    validator = AgentContextValidator()

    runtime = create_runtime(
        runtime_id="runtime-1",
        agent_id="agent-2",
    )

    context = AgentContext(
        runtime_id="runtime-1",
        agent_id="agent-1",
        runtime=runtime,
    )

    result = validator.validate(context)

    assert result.valid is False
    assert any(
        "runtime.agent_id" in error
        for error in result.errors
    )


def test_validator_rejects_integration_with_runtime_mismatch():
    validator = AgentContextValidator()

    runtime = create_runtime(
        runtime_id="runtime-2",
        agent_id="agent-1",
    )

    context = AgentContext(
        runtime_id="runtime-1",
        agent_id="agent-1",
        runtime=runtime,
    )

    source_results = {
        source: ContextSourceResult(
            source=source,
            status=ContextSourceStatus.NOT_REQUESTED,
        )
        for source in ContextSource
    }

    result = ContextIntegrationResult(
        context=context,
        source_results=source_results,
    )

    validation = validator.validate_integration(result)

    assert validation.valid is False
    assert any(
        "runtime.runtime_id" in error
        for error in validation.errors
    )

def test_valid_agent_context():
    validator = AgentContextValidator()

    context = AgentContext(
        runtime_id="runtime-1",
        agent_id="agent-1",
    )

    result = validator.validate(context)

    assert result.valid is True
    assert result.errors == ()


def test_invalid_agent_context_type():
    validator = AgentContextValidator()

    try:
        validator.validate(object())
        assert False
    except TypeError:
        pass


def test_valid_integration_result():
    validator = AgentContextValidator()

    project = object()

    context = AgentContext(
        runtime_id="runtime-1",
        agent_id="agent-1",
        project=project,
    )

    source_results = {
        source: ContextSourceResult(
            source=source,
            status=ContextSourceStatus.NOT_REQUESTED,
        )
        for source in ContextSource
    }

    source_results[ContextSource.PROJECT] = ContextSourceResult(
        source=ContextSource.PROJECT,
        status=ContextSourceStatus.AVAILABLE,
        value=project,
    )

    result = ContextIntegrationResult(
        context=context,
        source_results=source_results,
    )

    validation = validator.validate_integration(result)

    assert validation.valid is True
    assert validation.errors == ()


def test_available_source_must_have_context_value():
    validator = AgentContextValidator()

    context = AgentContext(
        runtime_id="runtime-1",
        agent_id="agent-1",
    )

    source_results = {
        source: ContextSourceResult(
            source=source,
            status=ContextSourceStatus.NOT_REQUESTED,
        )
        for source in ContextSource
    }

    source_results[ContextSource.PROJECT] = ContextSourceResult(
        source=ContextSource.PROJECT,
        status=ContextSourceStatus.AVAILABLE,
        value=object(),
    )

    result = ContextIntegrationResult(
        context=context,
        source_results=source_results,
    )

    validation = validator.validate_integration(result)

    assert validation.valid is False
    assert any(
        "project" in error
        for error in validation.errors
    )


def test_unavailable_source_must_not_exist_in_context():
    validator = AgentContextValidator()

    context = AgentContext(
        runtime_id="runtime-1",
        agent_id="agent-1",
        project=object(),
    )

    source_results = {
        source: ContextSourceResult(
            source=source,
            status=ContextSourceStatus.NOT_REQUESTED,
        )
        for source in ContextSource
    }

    source_results[ContextSource.PROJECT] = ContextSourceResult(
        source=ContextSource.PROJECT,
        status=ContextSourceStatus.UNAVAILABLE,
    )

    result = ContextIntegrationResult(
        context=context,
        source_results=source_results,
    )

    validation = validator.validate_integration(result)

    assert validation.valid is False


def test_context_value_must_match_available_source_result():
    validator = AgentContextValidator()

    context = AgentContext(
        runtime_id="runtime-1",
        agent_id="agent-1",
        project=object(),
    )

    source_results = {
        source: ContextSourceResult(
            source=source,
            status=ContextSourceStatus.NOT_REQUESTED,
        )
        for source in ContextSource
    }

    source_results[ContextSource.PROJECT] = ContextSourceResult(
        source=ContextSource.PROJECT,
        status=ContextSourceStatus.AVAILABLE,
        value=object(),
    )

    result = ContextIntegrationResult(
        context=context,
        source_results=source_results,
    )

    validation = validator.validate_integration(result)

    assert validation.valid is False


def test_missing_source_result_is_invalid():
    validator = AgentContextValidator()

    context = AgentContext(
        runtime_id="runtime-1",
        agent_id="agent-1",
    )

    result = ContextIntegrationResult(
        context=context,
        source_results={},
    )

    validation = validator.validate_integration(result)

    assert validation.valid is False
    assert len(validation.errors) == len(ContextSource)