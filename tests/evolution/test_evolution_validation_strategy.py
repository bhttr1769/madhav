import pytest

from brain.evolution.evolution_validation_strategy import (
    EvolutionValidationStrategy,
)


def test_creates_validation_strategy_for_tasks():
    strategy = EvolutionValidationStrategy()

    result = strategy.create(
        (
            "implement capability: repository_analysis",
        )
    )

    assert result == (
        "run generated tests",
        "run existing engineering tests",
        "verify capability integration",
    )


def test_creates_validation_strategy_for_multiple_tasks():
    strategy = EvolutionValidationStrategy()

    result = strategy.create(
        (
            "implement capability: project_graph",
            "implement capability: repository_analysis",
        )
    )

    assert result == (
        "run generated tests",
        "run existing engineering tests",
        "verify capability integration",
    )


def test_returns_existing_capability_validation_for_no_tasks():
    strategy = EvolutionValidationStrategy()

    result = strategy.create(())

    assert result == (
        "verify existing capabilities",
    )


def test_rejects_non_tuple_tasks():
    strategy = EvolutionValidationStrategy()

    with pytest.raises(
        TypeError,
        match="tasks must be a tuple",
    ):
        strategy.create(
            [
                "implement capability: repository_analysis",
            ]
        )


def test_rejects_invalid_task():
    strategy = EvolutionValidationStrategy()

    with pytest.raises(
        TypeError,
        match="tasks must contain only strings",
    ):
        strategy.create(
            (
                "valid task",
                123,
            )
        )