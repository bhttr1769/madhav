from brain.evolution.evolution_experience_extractor import (
    EvolutionExperienceExtractor,
)
from brain.evolution.models.evolution_result import (
    EvolutionResult,
)
from brain.evolution.models.evolution_task_result import (
    EvolutionTaskResult,
)


def _result(task_results):
    return EvolutionResult(
        requested_capability="web_research",
        requirement=None,
        task_decomposition=None,
        design=None,
        plan=None,
        task_results=tuple(task_results),
    )


def _task_result(
    task_id="task-001",
    task_description="implement capability: web_research",
    passed=True,
):
    from brain.engineering.loop.models.engineering_loop_result import (
        EngineeringLoopResult,
    )

    engineering_result = EngineeringLoopResult(
        changes=(),
        passed=passed,
        iterations=(),
        termination_reason=(
            "verification_passed"
            if passed
            else "max_iterations_reached"
        ),
    )

    return EvolutionTaskResult(
        task_id=task_id,
        task_description=task_description,
        proposed_changes=(),
        engineering_result=engineering_result,
    )


def test_extracts_successful_task_experience():
    extractor = EvolutionExperienceExtractor()

    result = _result(
        (
            _task_result(),
        )
    )

    experiences = extractor.extract(
        evolution_id="evo-001",
        result=result,
    )

    assert len(experiences) == 1

    experience = experiences[0]

    assert experience.evolution_id == "evo-001"
    assert experience.requested_capability == "web_research"
    assert experience.task_id == "task-001"
    assert experience.task_description == (
        "implement capability: web_research"
    )
    assert experience.outcome == "success"
    assert experience.reusable is True


def test_extracts_failed_task_experience():
    extractor = EvolutionExperienceExtractor()

    result = _result(
        (
            _task_result(
                task_id="task-002",
                task_description="implement failed capability",
                passed=False,
            ),
        )
    )

    experiences = extractor.extract(
        evolution_id="evo-002",
        result=result,
    )

    assert len(experiences) == 1

    experience = experiences[0]

    assert experience.outcome == "failure"
    assert experience.task_id == "task-002"
    assert experience.task_description == (
        "implement failed capability"
    )
    assert experience.reusable is True


def test_extracts_experience_for_each_task():
    extractor = EvolutionExperienceExtractor()

    result = _result(
        (
            _task_result(
                task_id="task-001",
                task_description="first task",
                passed=True,
            ),
            _task_result(
                task_id="task-002",
                task_description="second task",
                passed=False,
            ),
        )
    )

    experiences = extractor.extract(
        evolution_id="evo-003",
        result=result,
    )

    assert len(experiences) == 2
    assert experiences[0].task_id == "task-001"
    assert experiences[0].outcome == "success"
    assert experiences[1].task_id == "task-002"
    assert experiences[1].outcome == "failure"


def test_empty_task_results_produce_no_experience():
    extractor = EvolutionExperienceExtractor()

    result = _result(())

    experiences = extractor.extract(
        evolution_id="evo-004",
        result=result,
    )

    assert experiences == ()


def test_rejects_invalid_evolution_id():
    extractor = EvolutionExperienceExtractor()

    result = _result(())

    try:
        extractor.extract(
            evolution_id="",
            result=result,
        )
    except ValueError:
        pass
    else:
        raise AssertionError(
            "empty evolution_id must be rejected"
        )


def test_rejects_invalid_result():
    extractor = EvolutionExperienceExtractor()

    try:
        extractor.extract(
            evolution_id="evo-005",
            result=None,
        )
    except TypeError:
        pass
    else:
        raise AssertionError(
            "invalid result must be rejected"
        )