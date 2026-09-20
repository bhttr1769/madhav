from datetime import datetime

import pytest

from brain.engineering.requirements.models.requirement import (
    Requirement,
)
from brain.engineering.tasks.models.task import (
    Task,
)
from brain.engineering.tasks.models.task_decomposition import (
    TaskDecomposition,
)
from brain.evolution.evolution_history_builder import (
    EvolutionHistoryBuilder,
)
from brain.evolution.models.evolution_history import (
    EvolutionHistory,
)
from brain.evolution.models.evolution_request import (
    EvolutionRequest,
)
from brain.evolution.models.evolution_result import (
    EvolutionResult,
)
from brain.engineering.generation.models.code_change import (
    CodeChange,
)
from brain.engineering.loop.models.engineering_loop_iteration import (
    EngineeringLoopIteration,
)
from brain.engineering.loop.models.engineering_loop_result import (
    EngineeringLoopResult,
)
from brain.evolution.models.evolution_task_result import (
    EvolutionTaskResult,
)


def _requirement():
    return Requirement(
        original_request="Add web research capability.",
        objective="Add web research capability.",
        functional_requirements=frozenset(
            {"web research must work"}
        ),
        non_functional_requirements=frozenset(),
        constraints=frozenset(),
        acceptance_criteria=frozenset(
            {"verification passes"}
        ),
        assumptions=frozenset(),
        ambiguities=frozenset(),
        affected_areas=frozenset(
            {"brain/research"}
        ),
        confidence=1.0,
    )


def _task():
    return Task(
        id="task-1",
        description="Implement web research.",
        category="implementation",
        dependencies=frozenset(),
        affected_areas=frozenset(
            {"brain/research"}
        ),
        acceptance_criteria=frozenset(
            {"verification passes"}
        ),
    )


def _decomposition():
    requirement = _requirement()

    first_task = Task(
        id="task-1",
        description="First task.",
        category="implementation",
        dependencies=frozenset(),
        affected_areas=frozenset(
            {"brain/research"}
        ),
        acceptance_criteria=frozenset(
            {"verification passes"}
        ),
    )

    second_task = Task(
        id="task-2",
        description="Second task.",
        category="implementation",
        dependencies=frozenset(),
        affected_areas=frozenset(
            {"brain/research"}
        ),
        acceptance_criteria=frozenset(
            {"verification passes"}
        ),
    )

    return TaskDecomposition(
        requirement=requirement,
        tasks=(
            first_task,
            second_task,
        ),
    )


def _request():
    return EvolutionRequest(
        requested_capability="web_research",
        objective="Add web research capability.",
        constraints=frozenset(),
        mode="supervised",
    )


def _result():
    return EvolutionResult(
        requested_capability="web_research",
        requirement=_requirement(),
        task_decomposition=_decomposition(),
        design=None,
        plan=None,
        task_results=(),
    )


def test_builder_creates_evolution_history():
    builder = EvolutionHistoryBuilder()

    started_at = datetime(
        2026,
        9,
        20,
        10,
        0,
    )

    completed_at = datetime(
        2026,
        9,
        20,
        10,
        5,
    )

    history = builder.build(
        evolution_id="evo-001",
        request=_request(),
        result=_result(),
        started_at=started_at,
        completed_at=completed_at,
        status="completed",
    )

    assert isinstance(
        history,
        EvolutionHistory,
    )

    assert history.evolution_id == "evo-001"

    assert (
        history.requested_capability
        == "web_research"
    )

    assert (
        history.objective
        == "Add web research capability."
    )

    assert history.mode == "supervised"
    assert history.status == "completed"

    assert history.started_at == started_at
    assert history.completed_at == completed_at

    assert history.task_count == 2
    assert history.completed_task_count == 0

    assert history.passed is True

    assert (
        history.termination_reason
        == "no_tasks_executed"
    )


def test_builder_rejects_invalid_evolution_id():
    builder = EvolutionHistoryBuilder()

    with pytest.raises(
        TypeError,
        match="evolution_id must be a string",
    ):
        builder.build(
            evolution_id=123,
            request=_request(),
            result=_result(),
            started_at=datetime.now(),
            completed_at=datetime.now(),
            status="completed",
        )


def test_builder_rejects_invalid_result():
    builder = EvolutionHistoryBuilder()

    with pytest.raises(
        TypeError,
        match="result must be an EvolutionResult",
    ):
        builder.build(
            evolution_id="evo-001",
            request=_request(),
            result=object(),
            started_at=datetime.now(),
            completed_at=datetime.now(),
            status="completed",
        )


def test_builder_rejects_invalid_started_at():
    builder = EvolutionHistoryBuilder()

    with pytest.raises(
        TypeError,
        match="started_at must be a datetime",
    ):
        builder.build(
            evolution_id="evo-001",
            request=_request(),
            result=_result(),
            started_at="invalid",
            completed_at=datetime.now(),
            status="completed",
        )


def test_builder_rejects_invalid_completed_at():
    builder = EvolutionHistoryBuilder()

    with pytest.raises(
        TypeError,
        match="completed_at must be a datetime",
    ):
        builder.build(
            evolution_id="evo-001",
            request=_request(),
            result=_result(),
            started_at=datetime.now(),
            completed_at="invalid",
            status="completed",
        )

def test_builder_records_completed_tasks_and_termination_reason():
    builder = EvolutionHistoryBuilder()

    first_change = CodeChange(
        path="first.py",
        operation="create",
        content="first",
    )

    second_change = CodeChange(
        path="second.py",
        operation="create",
        content="second",
    )

    first_iteration = EngineeringLoopIteration(
        iteration=1,
        changes=(first_change,),
        passed=True,
        summary="First task passed.",
    )

    second_iteration = EngineeringLoopIteration(
        iteration=1,
        changes=(second_change,),
        passed=True,
        summary="Second task passed.",
    )

    first_loop_result = EngineeringLoopResult(
        changes=(first_change,),
        passed=True,
        iterations=(first_iteration,),
        termination_reason="verification_passed",
    )

    second_loop_result = EngineeringLoopResult(
        changes=(second_change,),
        passed=True,
        iterations=(second_iteration,),
        termination_reason="verification_passed",
    )

    first_task_result = EvolutionTaskResult(
        task_id="task-1",
        task_description="First task.",
        proposed_changes=(first_change,),
        engineering_result=first_loop_result,
    )

    second_task_result = EvolutionTaskResult(
        task_id="task-2",
        task_description="Second task.",
        proposed_changes=(second_change,),
        engineering_result=second_loop_result,
    )

    result = EvolutionResult(
        requested_capability="web_research",
        requirement=_requirement(),
        task_decomposition=_decomposition(),
        design=None,
        plan=None,
        task_results=(
            first_task_result,
            second_task_result,
        ),
    )

    history = builder.build(
        evolution_id="evo-002",
        request=_request(),
        result=result,
        started_at=datetime(
            2026,
            9,
            20,
            10,
            0,
        ),
        completed_at=datetime(
            2026,
            9,
            20,
            10,
            5,
        ),
        status="completed",
    )

    assert history.task_count == 2
    assert history.completed_task_count == 2
    assert history.passed is True
    assert (
        history.termination_reason
        == "verification_passed"
    )