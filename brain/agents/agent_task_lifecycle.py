from brain.agents.models.agent_task_status import AgentTaskStatus


class AgentTaskLifecycle:
    _TRANSITIONS = {
        AgentTaskStatus.CREATED: frozenset({
            AgentTaskStatus.ACTIVE,
            AgentTaskStatus.CANCELLED,
        }),
        AgentTaskStatus.ACTIVE: frozenset({
            AgentTaskStatus.COMPLETED,
            AgentTaskStatus.FAILED,
            AgentTaskStatus.CANCELLED,
        }),
        AgentTaskStatus.COMPLETED: frozenset(),
        AgentTaskStatus.FAILED: frozenset(),
        AgentTaskStatus.CANCELLED: frozenset(),
    }

    @classmethod
    def can_transition(
        cls,
        current: AgentTaskStatus,
        target: AgentTaskStatus,
    ) -> bool:
        if not isinstance(current, AgentTaskStatus):
            raise TypeError("current must be an AgentTaskStatus")

        if not isinstance(target, AgentTaskStatus):
            raise TypeError("target must be an AgentTaskStatus")

        return target in cls._TRANSITIONS[current]

    @classmethod
    def transition(
        cls,
        current: AgentTaskStatus,
        target: AgentTaskStatus,
    ) -> AgentTaskStatus:
        if not cls.can_transition(current, target):
            raise ValueError(
                f"invalid agent task transition: "
                f"{current.value} -> {target.value}"
            )

        return target