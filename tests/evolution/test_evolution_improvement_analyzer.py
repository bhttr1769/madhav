from datetime import datetime, timedelta

import pytest

from brain.evolution.evolution_improvement_analyzer import (
    EvolutionImprovementAnalyzer,
)

from brain.evolution.models.evolution_experience import (
    EvolutionExperience,
)

from brain.evolution.models.evolution_history import (
    EvolutionHistory,
)

from brain.evolution.models.evolution_improvement_category import (
    EvolutionImprovementCategory,
)

from brain.evolution.models.evolution_improvement_observation import (
    EvolutionImprovementObservation,
)


def _history(
    evolution_id,
    passed=False,
):
    started_at = datetime(
        2026,
        9,
        20,
        10,
        0,
    )

    completed_at = (
        started_at + timedelta(
            minutes=5
        )
        if passed or not passed
        else None
    )

    return EvolutionHistory(
        evolution_id=evolution_id,
        requested_capability="web_research",
        objective="Add web research capability.",
        mode="supervised",
        status=(
            "completed"
            if passed
            else "failed"
        ),
        started_at=started_at,
        completed_at=completed_at,
        task_count=1,
        completed_task_count=(
            1
            if passed
            else 0
        ),
        passed=passed,
        termination_reason=(
            "completed"
            if passed
            else "verification_failed"
        ),
    )


def _experience(
    evolution_id,
    task_description,
    outcome="failure",
    lesson="Previous attempt failed.",
):
    return EvolutionExperience(
        evolution_id=evolution_id,
        requested_capability="web_research",
        task_id=f"task-{evolution_id}",
        task_description=task_description,
        outcome=outcome,
        lesson=lesson,
        reusable=True,
    )


def test_analyzer_requires_tuple_histories():
    analyzer = EvolutionImprovementAnalyzer()

    with pytest.raises(TypeError):
        analyzer.analyze(
            histories=[],
            experiences=(),
        )


def test_analyzer_requires_tuple_experiences():
    analyzer = EvolutionImprovementAnalyzer()

    with pytest.raises(TypeError):
        analyzer.analyze(
            histories=(),
            experiences=[],
        )


def test_analyzer_rejects_invalid_history():
    analyzer = EvolutionImprovementAnalyzer()

    with pytest.raises(TypeError):
        analyzer.analyze(
            histories=(None,),
            experiences=(),
        )


def test_analyzer_rejects_invalid_experience():
    analyzer = EvolutionImprovementAnalyzer()

    with pytest.raises(TypeError):
        analyzer.analyze(
            histories=(),
            experiences=(None,),
        )


def test_analyzer_returns_no_observations_without_experience():
    analyzer = EvolutionImprovementAnalyzer()

    result = analyzer.analyze(
        histories=(),
        experiences=(),
    )

    assert result == ()


def test_successful_experience_does_not_create_observation():
    analyzer = EvolutionImprovementAnalyzer()

    histories = (
        _history(
            "evo-001",
            passed=True,
        ),
        _history(
            "evo-002",
            passed=True,
        ),
    )

    experiences = (
        _experience(
            "evo-001",
            "verification: verify generated tests",
            outcome="success",
        ),
        _experience(
            "evo-002",
            "verification: verify generated tests",
            outcome="success",
        ),
    )

    result = analyzer.analyze(
        histories=histories,
        experiences=experiences,
    )

    assert result == ()


def test_single_failure_does_not_create_observation():
    analyzer = EvolutionImprovementAnalyzer()

    histories = (
        _history(
            "evo-001",
        ),
    )

    experiences = (
        _experience(
            "evo-001",
            "verification: verify generated tests",
        ),
    )

    result = analyzer.analyze(
        histories=histories,
        experiences=experiences,
    )

    assert result == ()


def test_repeated_failure_creates_observation():
    analyzer = EvolutionImprovementAnalyzer()

    histories = (
        _history(
            "evo-001",
        ),
        _history(
            "evo-002",
        ),
    )

    experiences = (
        _experience(
            "evo-001",
            "verification: verify generated tests",
            lesson="Verification failed.",
        ),
        _experience(
            "evo-002",
            "verification: verify generated tests",
            lesson="Verification failed.",
        ),
    )

    result = analyzer.analyze(
        histories=histories,
        experiences=experiences,
    )

    assert len(result) == 1

    observation = result[0]

    assert isinstance(
        observation,
        EvolutionImprovementObservation,
    )

    assert observation.category is (
        EvolutionImprovementCategory.VERIFICATION
    )

    assert observation.occurrence_count == 2

    assert observation.evolution_ids == (
        "evo-001",
        "evo-002",
    )


def test_analyzer_ignores_unclassifiable_task_description():
    analyzer = EvolutionImprovementAnalyzer()

    histories = (
        _history("evo-001"),
        _history("evo-002"),
    )

    experiences = (
        _experience(
            "evo-001",
            "Improve the implementation",
        ),
        _experience(
            "evo-002",
            "Improve the implementation",
        ),
    )

    result = analyzer.analyze(
        histories=histories,
        experiences=experiences,
    )

    assert result == ()


def test_analyzer_requires_matching_history_for_evidence():
    analyzer = EvolutionImprovementAnalyzer()

    histories = (
        _history("evo-001"),
    )

    experiences = (
        _experience(
            "evo-001",
            "verification: verify generated tests",
        ),
        _experience(
            "evo-002",
            "verification: verify generated tests",
        ),
    )

    result = analyzer.analyze(
        histories=histories,
        experiences=experiences,
    )

    assert result == ()


def test_analyzer_uses_explicit_category_marker():
    analyzer = EvolutionImprovementAnalyzer()

    histories = (
        _history("evo-001"),
        _history("evo-002"),
    )

    experiences = (
        _experience(
            "evo-001",
            "test generation: generated tests were incomplete",
        ),
        _experience(
            "evo-002",
            "test generation: generated tests were incomplete",
        ),
    )

    result = analyzer.analyze(
        histories=histories,
        experiences=experiences,
    )

    assert len(result) == 1

    assert result[0].category is (
        EvolutionImprovementCategory.TEST_GENERATION
    )


def test_analyzer_deduplicates_evolution_ids():
    analyzer = EvolutionImprovementAnalyzer()

    histories = (
        _history("evo-001"),
        _history("evo-002"),
    )

    experiences = (
        _experience(
            "evo-001",
            "verification: verify generated tests",
        ),
        _experience(
            "evo-001",
            "verification: verify generated tests",
        ),
        _experience(
            "evo-002",
            "verification: verify generated tests",
        ),
    )

    result = analyzer.analyze(
        histories=histories,
        experiences=experiences,
    )

    assert len(result) == 1

    observation = result[0]

    assert observation.evolution_ids == (
        "evo-001",
        "evo-002",
    )

    assert observation.occurrence_count == 2


def test_analyzer_supports_custom_minimum_occurrences():
    analyzer = EvolutionImprovementAnalyzer(
        minimum_occurrences=3,
    )

    histories = (
        _history("evo-001"),
        _history("evo-002"),
    )

    experiences = (
        _experience(
            "evo-001",
            "verification: verify generated tests",
        ),
        _experience(
            "evo-002",
            "verification: verify generated tests",
        ),
    )

    result = analyzer.analyze(
        histories=histories,
        experiences=experiences,
    )

    assert result == ()


def test_analyzer_rejects_invalid_minimum_occurrences():
    with pytest.raises(ValueError):
        EvolutionImprovementAnalyzer(
            minimum_occurrences=1,
        )


def test_analyzer_rejects_non_integer_minimum_occurrences():
    with pytest.raises(TypeError):
        EvolutionImprovementAnalyzer(
            minimum_occurrences="2",
        )