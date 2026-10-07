from brain.agents.context_source import ContextSource
from brain.agents.models.context_restoration_state import (
    ContextRestorationState,
)


def test_restoration_state_can_be_created():
    state = ContextRestorationState(
        runtime_id="runtime-1",
        agent_id="agent-1",
        requested_sources=frozenset({
            ContextSource.PROJECT,
            ContextSource.MEMORY,
        }),
    )

    assert state.runtime_id == "runtime-1"
    assert state.agent_id == "agent-1"

    assert state.requested_sources == frozenset({
        ContextSource.PROJECT,
        ContextSource.MEMORY,
    })


def test_empty_requested_sources_are_allowed():
    state = ContextRestorationState(
        runtime_id="runtime-1",
        agent_id="agent-1",
        requested_sources=frozenset(),
    )

    assert state.requested_sources == frozenset()


def test_restoration_state_is_immutable():
    state = ContextRestorationState(
        runtime_id="runtime-1",
        agent_id="agent-1",
        requested_sources=frozenset(),
    )

    try:
        state.runtime_id = "runtime-2"
        assert False
    except AttributeError:
        pass


def test_invalid_runtime_id_is_rejected():
    try:
        ContextRestorationState(
            runtime_id="",
            agent_id="agent-1",
            requested_sources=frozenset(),
        )
        assert False
    except ValueError:
        pass


def test_invalid_source_is_rejected():
    try:
        ContextRestorationState(
            runtime_id="runtime-1",
            agent_id="agent-1",
            requested_sources=frozenset({"project"}),
        )
        assert False
    except TypeError:
        pass