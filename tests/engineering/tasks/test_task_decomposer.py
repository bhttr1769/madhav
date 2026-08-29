from brain.engineering.requirements.models.requirement import (
    Requirement,
)

from brain.engineering.tasks.models.task_decomposition import (
    TaskDecomposition,
)

from brain.engineering.tasks.task_decomposer import (
    TaskDecomposer,
)


class FakeTaskDecomposer(TaskDecomposer):

    def __init__(
        self,
        result: TaskDecomposition,
    ):
        self._result = result

    def decompose(
        self,
        requirement: Requirement,
    ) -> TaskDecomposition:

        return self._result


def test_task_decomposer_is_interface():

    assert TaskDecomposer.__abstractmethods__ == {
        "decompose",
    }


def test_fake_task_decomposer_returns_result():

    result = TaskDecomposition(
        requirement=Requirement(
            original_request="Build an API",
            objective="Build an API",
            functional_requirements=frozenset(),
            non_functional_requirements=frozenset(),
            constraints=frozenset(),
            acceptance_criteria=frozenset(),
            assumptions=frozenset(),
            ambiguities=frozenset(),
            affected_areas=frozenset(),
            confidence=1.0,
        ),
        tasks=(),
    )

    decomposer = FakeTaskDecomposer(
        result,
    )

    assert decomposer.decompose(
        result.requirement,
    ) == result