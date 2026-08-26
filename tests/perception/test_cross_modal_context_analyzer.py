from brain.perception.cross_modal_context_analyzer import (
    CrossModalContextAnalyzer,
)

from brain.perception.models.observation import (
    Observation,
)


def test_analyzer_preserves_observations():

    observations = frozenset({
        Observation(
            source="workspace",
            category="technology",
            subject="project",
            value="Python",
        ),
    })

    context = (
        CrossModalContextAnalyzer().analyze(
            observations,
        )
    )

    assert context.observations == observations


def test_analyzer_detects_same_technology():

    workspace = Observation(
        source="workspace",
        category="technology",
        subject="project",
        value="Python",
    )

    code = Observation(
        source="code",
        category="technology",
        subject="module",
        value="Python",
    )

    context = (
        CrossModalContextAnalyzer().analyze(
            frozenset({
                workspace,
                code,
            }),
        )
    )

    assert (
        (
            "code:technology:module:Python",
            "same_technology",
            "workspace:technology:project:Python",
        )
        in context.relationships
    )


def test_analyzer_does_not_relate_same_source():

    first = Observation(
        source="workspace",
        category="technology",
        subject="project",
        value="Python",
    )

    second = Observation(
        source="workspace",
        category="technology",
        subject="module",
        value="Python",
    )

    context = (
        CrossModalContextAnalyzer().analyze(
            frozenset({
                first,
                second,
            }),
        )
    )

    assert context.relationships == frozenset()


def test_analyzer_does_not_invent_relationships():

    first = Observation(
        source="workspace",
        category="technology",
        subject="project",
        value="Python",
    )

    second = Observation(
        source="ui",
        category="element",
        subject="button",
        value="Submit",
    )

    context = (
        CrossModalContextAnalyzer().analyze(
            frozenset({
                first,
                second,
            }),
        )
    )

    assert context.relationships == frozenset()