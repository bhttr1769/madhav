from brain.evolution.evolution_improvement_analyzer import (
    EvolutionImprovementAnalyzer,
)

from brain.evolution.evolution_improvement_planner import (
    EvolutionImprovementPlanner,
)

from brain.evolution.evolution_improvement_proposer import (
    EvolutionImprovementProposer,
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

from brain.evolution.models.evolution_improvement_plan import (
    EvolutionImprovementPlan,
)

from brain.evolution.models.evolution_improvement_proposal import (
    EvolutionImprovementProposal,
)

from brain.evolution.models.evolution_result import (
    EvolutionResult,
)

from tests.evolution.test_evolution_executor import (
    _executor,
)
from brain.evolution.evolution_improvement_request_builder import (
    EvolutionImprovementRequestBuilder,
)


def _history(evolution_id):
    from datetime import datetime, timedelta

    started_at = datetime(
        2026,
        9,
        20,
        10,
        0,
    )

    return EvolutionHistory(
        evolution_id=evolution_id,
        requested_capability="web_research",
        objective="Add web research capability.",
        mode="supervised",
        status="failed",
        started_at=started_at,
        completed_at=(
            started_at + timedelta(minutes=5)
        ),
        task_count=1,
        completed_task_count=0,
        passed=False,
        termination_reason="verification_failed",
    )


def _experience(evolution_id):
    return EvolutionExperience(
        evolution_id=evolution_id,
        requested_capability="web_research",
        task_id=f"task-{evolution_id}",
        task_description=(
            "verification: verify generated tests"
        ),
        outcome="failure",
        lesson="Verification failed.",
        reusable=True,
    )


def test_improvement_pipeline_runs_end_to_end():
    histories = (
        _history("evo-001"),
        _history("evo-002"),
    )

    experiences = (
        _experience("evo-001"),
        _experience("evo-002"),
    )

    analyzer = EvolutionImprovementAnalyzer()

    observations = analyzer.analyze(
        histories=histories,
        experiences=experiences,
    )

    assert len(observations) == 1

    observation = observations[0]

    assert isinstance(
        observation,
        EvolutionImprovementObservation,
    )

    assert observation.category is (
        EvolutionImprovementCategory.VERIFICATION
    )

    proposer = EvolutionImprovementProposer()

    proposal = proposer.propose(
        observation
    )

    assert isinstance(
        proposal,
        EvolutionImprovementProposal,
    )

    assert proposal.category is (
        EvolutionImprovementCategory.VERIFICATION
    )

    planner = EvolutionImprovementPlanner()

    plan = planner.plan(
        proposal
    )

    assert isinstance(
        plan,
        EvolutionImprovementPlan,
    )

    assert plan.target_component == (
        "evolution_validator"
    )

    (
        executor,
        requirement_service,
        task_decomposer,
        system_designer,
        planner,
        _,
        _,
        engineering_loop,
        context,
    ) = _executor()

    expected_request = (
        EvolutionImprovementRequestBuilder().build(
        plan
        )
    )

    result = executor.execute_improvement(
        improvement_plan=plan,
    )

    (
        requirement,
        task,
        decomposition,
        design,
        engineering_plan,
        _,
        _,
        _,
        _,
    ) = context

    assert isinstance(
        result,
        EvolutionResult,
    )

    assert result.passed is True

    assert result.requirement == requirement

    assert result.task_decomposition == (
        decomposition
    )

    assert result.design == design

    assert result.plan == engineering_plan

    assert len(result.task_results) == 1

    assert result.task_results[0].task_id == (
        task.id
    )

    assert requirement_service.calls

    assert len(
        requirement_service.calls
    ) == 1

    assert requirement_service.calls == [
        expected_request.objective
    ]

    assert task_decomposer.calls == [
        requirement
    ]

    assert system_designer.calls == [
        decomposition
    ]

    assert engineering_loop.calls

    assert planner.calls == [
        decomposition
    ]