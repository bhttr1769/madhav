from brain.perception.models.cross_modal_context import (
    CrossModalContext,
)

from brain.perception.models.observation import (
    Observation,
)

from brain.reasoning.context_builder import (
    ContextBuilder,
)


def test_context_builder_converts_observations():

    observation = Observation(
        source="workspace",
        category="technology",
        subject="project",
        value="Python",
    )

    perception = CrossModalContext(
        observations=frozenset({
            observation,
        }),
        relationships=frozenset(),
    )

    context = ContextBuilder().build(
        perception,
    )

    assert context.observations == frozenset({
        "workspace:technology:project:Python",
    })


def test_context_builder_preserves_facts():

    perception = CrossModalContext(
        observations=frozenset(),
        relationships=frozenset(),
    )

    context = ContextBuilder().build(
        perception,
        facts=frozenset({
            "project uses Python",
        }),
    )

    assert context.facts == frozenset({
        "project uses Python",
    })


def test_context_builder_preserves_constraints():

    perception = CrossModalContext(
        observations=frozenset(),
        relationships=frozenset(),
    )

    context = ContextBuilder().build(
        perception,
        constraints=frozenset({
            "Windows environment",
        }),
    )

    assert context.constraints == frozenset({
        "Windows environment",
    })


def test_context_builder_preserves_goals():

    perception = CrossModalContext(
        observations=frozenset(),
        relationships=frozenset(),
    )

    context = ContextBuilder().build(
        perception,
        goals=frozenset({
            "understand project",
        }),
    )

    assert context.goals == frozenset({
        "understand project",
    })


def test_context_builder_handles_empty_perception():

    perception = CrossModalContext(
        observations=frozenset(),
        relationships=frozenset(),
    )

    context = ContextBuilder().build(
        perception,
    )

    assert context.observations == frozenset()
    assert context.facts == frozenset()
    assert context.constraints == frozenset()
    assert context.goals == frozenset()