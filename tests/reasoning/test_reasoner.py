from brain.reasoning.fake_reasoner import (
    FakeReasoner,
)

from brain.reasoning.models.context import (
    Context,
)

from brain.reasoning.reasoner import (
    Reasoner,
)


def test_reasoner_is_interface():

    assert Reasoner.__abstractmethods__ == {
        "reason",
    }


def test_fake_reasoner_returns_result():

    context = Context(
        observations=frozenset({
            "workspace:technology:project:Python",
        }),
        facts=frozenset(),
        constraints=frozenset(),
        goals=frozenset({
            "understand project",
        }),
    )

    reasoner = FakeReasoner(
        result="project uses Python",
    )

    result = reasoner.reason(
        context,
    )

    assert result == (
        "project uses Python"
    )