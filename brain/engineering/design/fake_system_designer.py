from brain.engineering.design.models.system_design import (
    SystemDesign,
)

from brain.engineering.design.system_designer import (
    SystemDesigner,
)

from brain.engineering.tasks.models.task_decomposition import (
    TaskDecomposition,
)


class FakeSystemDesigner(SystemDesigner):
    """
    Deterministic system designer for testing.
    """

    def __init__(
        self,
        result: SystemDesign,
    ):
        self._result = result

    def design(
        self,
        task_decomposition: TaskDecomposition,
    ) -> SystemDesign:

        return self._result