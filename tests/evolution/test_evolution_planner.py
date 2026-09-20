import pytest

from brain.capabilities.models.capability_assessment import (
    CapabilityAssessment,
)
from brain.evolution.evolution_planner import (
    EvolutionPlanner,
)
from brain.evolution.models.evolution_plan import (
    EvolutionPlan,
)
from brain.evolution.models.evolution_request import (
    EvolutionRequest,
)
from brain.capabilities.models.capability_descriptor import (
    CapabilityDescriptor,
)
from brain.evolution.models.evolution_experience import (
    EvolutionExperience,
)


def _request(
    capability="web_research",
):
    return EvolutionRequest(
        requested_capability=capability,
        objective="Add the requested capability.",
        constraints=frozenset(),
        mode="supervised",
    )


def _missing_assessment(
    capability="web_research",
):
    return CapabilityAssessment(
        requested_capability=capability,
        available=False,
        status="unavailable",
        matched_capabilities=frozenset(),
        missing_capabilities=frozenset(
            {capability}
        ),
        rationale="Capability is not registered.",
    )


def _available_assessment(
    capability="web_research",
):
    return CapabilityAssessment(
        requested_capability=capability,
        available=True,
        status="available",
        matched_capabilities=frozenset(
            {capability}
        ),
        missing_capabilities=frozenset(),
        rationale="Capability is registered.",
    )


def test_planner_creates_plan_for_missing_capability():
    request = _request()
    assessment = _missing_assessment()

    plan = EvolutionPlanner().plan(
        request,
        assessment,
    )

    assert isinstance(
        plan,
        EvolutionPlan,
    )

    assert plan.requested_capability == (
        "web_research"
    )

    assert plan.current_status == "missing"

    assert plan.required_capabilities == (
        frozenset({"web_research"})
    )

    assert plan.tasks == (
        "implement capability: web_research",
    )


def test_planner_includes_validation_strategy():
    plan = EvolutionPlanner().plan(
        _request(),
        _missing_assessment(),
    )

    assert plan.validation_strategy == (
        "run generated tests",
        "run existing engineering tests",
        "verify capability integration",
    )


def test_planner_includes_risks():
    plan = EvolutionPlanner().plan(
        _request(),
        _missing_assessment(),
    )

    assert plan.risks == frozenset(
        {"implementation may fail verification"}
    )


def test_planner_handles_existing_capability():
    plan = EvolutionPlanner().plan(
        _request(),
        _available_assessment(),
    )

    assert plan.current_status == (
        "already_available"
    )

    assert plan.reusable_capabilities == (
        frozenset({"web_research"})
    )

    assert plan.required_capabilities == frozenset()
    assert plan.tasks == ()
    assert plan.risks == frozenset()


def test_planner_rejects_invalid_request():
    with pytest.raises(TypeError):
        EvolutionPlanner().plan(
            None,
            _missing_assessment(),
        )


def test_planner_rejects_invalid_assessment():
    with pytest.raises(TypeError):
        EvolutionPlanner().plan(
            _request(),
            None,
        )


def test_planner_rejects_mismatched_capability():
    with pytest.raises(ValueError):
        EvolutionPlanner().plan(
            _request("web_research"),
            _missing_assessment("memory"),
        )

def test_plan_uses_available_capabilities():
    planner = EvolutionPlanner()

    request = EvolutionRequest(
        requested_capability="repository_analysis",
        objective="Analyze a repository.",
        constraints=frozenset(),
        mode="proposal",
    )

    assessment = CapabilityAssessment(
        requested_capability="repository_analysis",
        available=False,
        status="unavailable",
        matched_capabilities=frozenset(),
        missing_capabilities=frozenset(
            {"repository_analysis"},
        ),
        rationale="Capability is not registered.",
    )

    available_capability = CapabilityDescriptor(
        id="file_read",
        name="File Read",
        description="Reads files.",
        version="1.0.0",
        entry_point="brain.file_read.FileRead",
        dependencies=frozenset(),
    )

    result = planner.plan(
        request,
        assessment,
        available_capabilities=(
            available_capability,
        ),
    )

    assert result.requested_capability == (
        "repository_analysis"
    )

    assert result.required_capabilities == (
        frozenset({"repository_analysis"})
    )

    assert result.tasks == (
        "implement capability: repository_analysis",
    )

    assert result.validation_strategy == (
        "run generated tests",
        "run existing engineering tests",
        "verify capability integration",
    )

def _experience(
    capability="web_research",
):
    return EvolutionExperience(
        evolution_id="evo-001",
        requested_capability=capability,
        task_id="task-001",
        task_description=(
            f"implement capability: {capability}"
        ),
        outcome="success",
        lesson="Previous implementation succeeded.",
        reusable=True,
    )


def test_planner_accepts_evolution_experience():
    planner = EvolutionPlanner()

    result = planner.plan(
        _request(),
        _missing_assessment(),
        experiences=(
            _experience(),
        ),
    )

    assert isinstance(
        result,
        EvolutionPlan,
    )

    assert result.requested_capability == (
        "web_research"
    )


def test_planner_rejects_non_tuple_experiences():
    with pytest.raises(TypeError):
        EvolutionPlanner().plan(
            _request(),
            _missing_assessment(),
            experiences=[],
        )


def test_planner_rejects_invalid_experience():
    with pytest.raises(TypeError):
        EvolutionPlanner().plan(
            _request(),
            _missing_assessment(),
            experiences=(None,),
        )


def test_planner_remains_backward_compatible_without_experience():
    result = EvolutionPlanner().plan(
        _request(),
        _missing_assessment(),
    )

    assert result.tasks == (
        "implement capability: web_research",
    )

    assert result.required_capabilities == (
        frozenset({"web_research"})
    )