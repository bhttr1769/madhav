from brain.agents.agent_context_selector import AgentContextSelector
from brain.agents.context_source import ContextSource
from brain.agents.models.agent_context import AgentContext


def test_selector_selects_requested_sources():
    selector = AgentContextSelector()

    user = object()
    project = object()
    environment = object()
    memory = object()
    knowledge = object()
    perception = object()
    runtime = object()

    context = AgentContext(
        runtime_id="runtime-1",
        agent_id="agent-1",
        user=user,
        project=project,
        environment=environment,
        memory=memory,
        knowledge=knowledge,
        perception=perception,
        runtime=runtime,
    )

    result = selector.select(
        context,
        frozenset({
            ContextSource.PROJECT,
            ContextSource.ENVIRONMENT,
            ContextSource.RUNTIME,
        }),
    )

    assert result.project is project
    assert result.environment is environment
    assert result.runtime is runtime

    assert result.user is None
    assert result.memory is None
    assert result.knowledge is None
    assert result.perception is None


def test_selector_can_select_all_sources():
    selector = AgentContextSelector()

    values = {
        "user": object(),
        "project": object(),
        "environment": object(),
        "memory": object(),
        "knowledge": object(),
        "perception": object(),
        "runtime": object(),
    }

    context = AgentContext(
        runtime_id="runtime-1",
        agent_id="agent-1",
        **values,
    )

    result = selector.select(
        context,
        frozenset(ContextSource),
    )

    assert result.user is values["user"]
    assert result.project is values["project"]
    assert result.environment is values["environment"]
    assert result.memory is values["memory"]
    assert result.knowledge is values["knowledge"]
    assert result.perception is values["perception"]
    assert result.runtime is values["runtime"]


def test_selector_with_empty_sources_returns_identity_only():
    selector = AgentContextSelector()

    context = AgentContext(
        runtime_id="runtime-1",
        agent_id="agent-1",
        project=object(),
        memory=object(),
    )

    result = selector.select(
        context,
        frozenset(),
    )

    assert result.runtime_id == "runtime-1"
    assert result.agent_id == "agent-1"
    assert result.project is None
    assert result.memory is None


def test_selector_does_not_modify_original_context():
    selector = AgentContextSelector()

    project = object()
    memory = object()

    context = AgentContext(
        runtime_id="runtime-1",
        agent_id="agent-1",
        project=project,
        memory=memory,
    )

    selector.select(
        context,
        frozenset({ContextSource.PROJECT}),
    )

    assert context.project is project
    assert context.memory is memory


def test_selector_creates_new_context():
    selector = AgentContextSelector()

    context = AgentContext(
        runtime_id="runtime-1",
        agent_id="agent-1",
        project=object(),
    )

    result = selector.select(
        context,
        frozenset({ContextSource.PROJECT}),
    )

    assert result is not context


def test_selector_rejects_invalid_context():
    selector = AgentContextSelector()

    try:
        selector.select(
            object(),
            frozenset(),
        )
        assert False
    except TypeError as exc:
        assert "context" in str(exc)


def test_selector_rejects_invalid_sources_container():
    selector = AgentContextSelector()

    context = AgentContext(
        runtime_id="runtime-1",
        agent_id="agent-1",
    )

    try:
        selector.select(context, set())
        assert False
    except TypeError as exc:
        assert "frozenset" in str(exc)


def test_selector_rejects_invalid_source_values():
    selector = AgentContextSelector()

    context = AgentContext(
        runtime_id="runtime-1",
        agent_id="agent-1",
    )

    try:
        selector.select(
            context,
            frozenset({"project"}),
        )
        assert False
    except TypeError as exc:
        assert "ContextSource" in str(exc)