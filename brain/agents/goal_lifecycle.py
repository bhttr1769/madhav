from brain.agents.models.goal_status import GoalStatus


class GoalLifecycle:
    _TRANSITIONS = {
        GoalStatus.CREATED: frozenset({
            GoalStatus.ACTIVE,
            GoalStatus.CANCELLED,
        }),
        GoalStatus.ACTIVE: frozenset({
            GoalStatus.COMPLETED,
            GoalStatus.FAILED,
            GoalStatus.CANCELLED,
        }),
        GoalStatus.COMPLETED: frozenset(),
        GoalStatus.FAILED: frozenset(),
        GoalStatus.CANCELLED: frozenset(),
    }

    @classmethod
    def can_transition(
        cls,
        current: GoalStatus,
        target: GoalStatus,
    ) -> bool:
        if not isinstance(current, GoalStatus):
            raise TypeError("current must be a GoalStatus")

        if not isinstance(target, GoalStatus):
            raise TypeError("target must be a GoalStatus")

        return target in cls._TRANSITIONS[current]

    @classmethod
    def transition(
        cls,
        current: GoalStatus,
        target: GoalStatus,
    ) -> GoalStatus:
        if not cls.can_transition(current, target):
            raise ValueError(
                f"invalid goal transition: {current.value} -> {target.value}"
            )

        return target