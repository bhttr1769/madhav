from dataclasses import FrozenInstanceError

import pytest

from brain.evolution.models.evolution_request import (
    EvolutionRequest,
)


def test_evolution_request_stores_complete_context():
    request = EvolutionRequest(
        requested_capability="web_research",
        objective="Add web research.",
        constraints=frozenset(
            {"reuse existing architecture"}
        ),
        mode="supervised",
    )

    assert request.requested_capability == (
        "web_research"
    )

    assert request.objective == (
        "Add web research."
    )

    assert request.constraints == frozenset(
        {"reuse existing architecture"}
    )

    assert request.mode == "supervised"


def test_evolution_request_is_immutable():
    request = EvolutionRequest(
        requested_capability="web_research",
        objective="Add web research.",
        constraints=frozenset(),
        mode="proposal",
    )

    with pytest.raises(
        FrozenInstanceError
    ):
        request.mode = "autonomous"


def test_constraints_are_immutable():
    request = EvolutionRequest(
        requested_capability="memory",
        objective="Improve memory.",
        constraints=frozenset(
            {"preserve compatibility"}
        ),
        mode="proposal",
    )

    assert isinstance(
        request.constraints,
        frozenset,
    )