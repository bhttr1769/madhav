from brain.engineering.planning.models.plan import (
    EngineeringPlan,
)

from brain.engineering.planning.planner import (
    Planner,
)

from brain.engineering.tasks.models.task_decomposition import (
    TaskDecomposition,
)


class FakePlanner(Planner):
    """
    Deterministic planner for testing.
    """

    def __init__(
        self,
        result: EngineeringPlan,
    ):
        self._result = result

    def plan(
        self,
        decomposition: TaskDecomposition,
    ) -> EngineeringPlan:

        return self._result