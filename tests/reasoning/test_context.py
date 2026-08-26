from brain.reasoning.models.context import (
    Context,
)


def test_context():

    context = Context(
        observations=frozenset({
            "Python project detected",
        }),
        facts=frozenset({
            "project uses Python",
        }),
        constraints=frozenset({
            "Windows environment",
        }),
        goals=frozenset({
            "understand project architecture",
        }),
    )

    assert context.observations == frozenset({
        "Python project detected",
    })

    assert context.facts == frozenset({
        "project uses Python",
    })

    assert context.constraints == frozenset({
        "Windows environment",
    })

    assert context.goals == frozenset({
        "understand project architecture",
    })


def test_context_supports_empty_sections():

    context = Context(
        observations=frozenset(),
        facts=frozenset(),
        constraints=frozenset(),
        goals=frozenset(),
    )

    assert context.observations == frozenset()
    assert context.facts == frozenset()
    assert context.constraints == frozenset()
    assert context.goals == frozenset()