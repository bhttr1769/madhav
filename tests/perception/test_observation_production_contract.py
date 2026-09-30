from dataclasses import fields

from brain.perception.models.observation import (
    Observation,
)


def test_observation_contract():
    observation = Observation(
        source="workspace",
        category="technology",
        subject="project",
        value="Python",
    )

    assert observation.source == "workspace"
    assert observation.category == "technology"
    assert observation.subject == "project"
    assert observation.value == "Python"
    assert observation.confidence == 1.0


def test_observation_contract_has_exact_fields():
    assert [
        field.name
        for field in fields(Observation)
    ] == [
        "source",
        "category",
        "subject",
        "value",
        "confidence",
    ]


def test_observation_is_immutable():
    observation = Observation(
        source="workspace",
        category="technology",
        subject="project",
        value="Python",
    )

    try:
        observation.value = "Java"
    except AttributeError:
        pass
    else:
        raise AssertionError(
            "Observation must be immutable"
        )


def test_observation_equality_and_hashability():
    first = Observation(
        source="workspace",
        category="technology",
        subject="project",
        value="Python",
        confidence=0.95,
    )

    second = Observation(
        source="workspace",
        category="technology",
        subject="project",
        value="Python",
        confidence=0.95,
    )

    assert first == second
    assert hash(first) == hash(second)