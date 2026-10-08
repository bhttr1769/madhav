from dataclasses import dataclass

from brain.agents.models.agent_assignment import AgentAssignment
from brain.agents.models.agent_plan import AgentPlan


@dataclass(frozen=True)
class AgentPlanningPersistenceState:
    """
    Persistable planning and delegation state.

    The state contains the generated plan and the assignments
    derived from that plan.
    """

    plan: AgentPlan
    assignments: tuple[AgentAssignment, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.plan, AgentPlan):
            raise TypeError("plan must be an AgentPlan")

        if not isinstance(self.assignments, tuple):
            raise TypeError("assignments must be a tuple")

        for assignment in self.assignments:
            if not isinstance(assignment, AgentAssignment):
                raise TypeError(
                    "assignments must contain only "
                    "AgentAssignment instances"
                )