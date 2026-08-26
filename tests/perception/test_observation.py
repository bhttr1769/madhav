from brain.perception.models.observation import (
    Observation,
)


def test_observation():

    observation = Observation(
        source="workspace",
        category="technology",
        subject="project",
        value="Python",
        confidence=0.95,
    )

    assert observation.source == "workspace"
    assert observation.category == "technology"
    assert observation.subject == "project"
    assert observation.value == "Python"
    assert observation.confidence == 0.95


def test_observation_defaults_confidence():

    observation = Observation(
        source="ui",
        category="element",
        subject="button",
        value="Submit",
    )

    assert observation.confidence == 1.0