from brain.engineering.requirements.models.requirement import (
    Requirement,
)


def test_requirement_model():

    requirement = Requirement(
        original_request="Add authentication.",
        objective="Add authentication to the application.",
        functional_requirements=frozenset({
            "Authenticate users.",
        }),
        non_functional_requirements=frozenset(),
        constraints=frozenset(),
        acceptance_criteria=frozenset({
            "Unauthenticated users are rejected.",
        }),
        assumptions=frozenset(),
        ambiguities=frozenset({
            "Authentication mechanism is unspecified.",
        }),
        affected_areas=frozenset({
            "authentication",
        }),
        confidence=0.8,
    )

    assert requirement.original_request == "Add authentication."

    assert (
        "Authenticate users."
        in requirement.functional_requirements
    )

    assert (
        "Authentication mechanism is unspecified."
        in requirement.ambiguities
    )

    assert requirement.confidence == 0.8