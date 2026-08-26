from brain.reasoning.models.decision import (
    Decision,
)


def test_decision():

    decision = Decision(
        action="inspect project architecture",
        rationale="Architecture information is incomplete.",
        confidence=0.9,
        alternatives=frozenset({
            "inspect dependencies",
            "inspect source files",
        }),
    )

    assert decision.action == (
        "inspect project architecture"
    )

    assert decision.rationale == (
        "Architecture information is incomplete."
    )

    assert decision.confidence == 0.9

    assert decision.alternatives == frozenset({
        "inspect dependencies",
        "inspect source files",
    })


def test_decision_supports_no_alternatives():

    decision = Decision(
        action="continue",
        rationale="No additional action is required.",
        confidence=1.0,
        alternatives=frozenset(),
    )

    assert decision.alternatives == frozenset()
