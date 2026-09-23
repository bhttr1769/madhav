import pytest

from brain.evolution.evolution_improvement_planner import (
    EvolutionImprovementPlanner,
)

from brain.evolution.evolution_improvement_proposer import (
    EvolutionImprovementProposer,
)

from brain.evolution.evolution_improvement_request_builder import (
    EvolutionImprovementRequestBuilder,
)

from brain.evolution.models.evolution_improvement_category import (
    EvolutionImprovementCategory,
)

from brain.evolution.models.evolution_improvement_observation import (
    EvolutionImprovementObservation,
)

from brain.evolution.models.evolution_improvement_proposal import (
    EvolutionImprovementProposal,
)

from brain.evolution.models.evolution_improvement_plan import (
    EvolutionImprovementPlan,
)

from brain.evolution.models.evolution_result import (
    EvolutionResult,
)

from tests.evolution.test_evolution_executor import (
    _executor,
)


def _observation():
    return EvolutionImprovementObservation(
        category=(
            EvolutionImprovementCategory.VERIFICATION
        ),
        description=(
            "Repeated unsuccessful "
            "verification experiences."
        ),
        evolution_ids=(
            "evo-001",
            "evo-002",
        ),
        occurrence_count=2,
    )


def _proposal():
    return EvolutionImprovementProposal(
        category=(
            EvolutionImprovementCategory.VERIFICATION
        ),
        problem=(
            "Repeated unsuccessful verification "
            "experiences were observed."
        ),
        proposed_improvement=(
            "Review and improve the verification process."
        ),
        evidence=(
            _observation(),
        ),
        target_component="evolution_validator",
        expected_effect=(
            "Reduce repeated unsuccessful "
            "verification outcomes."
        ),
    )


def _plan():
    planner = EvolutionImprovementPlanner()

    return planner.plan(
        _proposal()
    )


def test_improvement_plan_executes_through_existing_executor():
    plan = _plan()

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

    expected_request = (
        EvolutionImprovementRequestBuilder().build(
            plan
        )
    )

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

    assert result.engineering_result.passed is True

    assert len(result.task_results) == 1

    assert result.task_results[0].task_id == (
        task.id
    )

    assert requirement_service.calls == [
        expected_request.objective
    ]

    assert task_decomposer.calls == [
        requirement
    ]

    assert system_designer.calls == [
        decomposition
    ]

    assert planner.calls == [
        decomposition
    ]

    assert len(engineering_loop.calls) == 1


def test_improvement_execution_uses_supervised_mode_by_default():
    plan = _plan()

    (
        executor,
        _,
        _,
        _,
        _,
        _,
        _,
        _,
        _,
    ) = _executor()

    result = executor.execute_improvement(
        improvement_plan=plan,
    )

    assert result.passed is True


def test_improvement_execution_preserves_improvement_target():
    plan = _plan()

    assert plan.target_component == (
        "evolution_validator"
    )

    assert plan.proposal.category is (
        EvolutionImprovementCategory.VERIFICATION
    )


def test_improvement_plan_is_created_from_observation():
    observation = _observation()

    proposer = EvolutionImprovementProposer()

    proposal = proposer.propose(
        observation
    )

    planner = EvolutionImprovementPlanner()

    plan = planner.plan(
        proposal
    )

    assert isinstance(
        plan,
        EvolutionImprovementPlan,
    )

    assert plan.proposal == proposal

    assert plan.proposal.evidence == (
        observation,
    )


def test_improvement_execution_rejects_invalid_plan():
    (
        executor,
        _,
        _,
        _,
        _,
        _,
        _,
        _,
        _,
    ) = _executor()

    with pytest.raises(
        TypeError,
        match=(
            "plan must be an "
            "EvolutionImprovementPlan"
        ),
    ):
        executor.execute_improvement(
            improvement_plan=None,
        )