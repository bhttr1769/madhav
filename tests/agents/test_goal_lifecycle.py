import pytest

from brain.agents.goal_lifecycle import GoalLifecycle
from brain.agents.models.goal_status import GoalStatus


def test_valid_goal_transitions():
    assert GoalLifecycle.transition(
        GoalStatus.CREATED,
        GoalStatus.ACTIVE,
    ) is GoalStatus.ACTIVE

    assert GoalLifecycle.transition(
        GoalStatus.ACTIVE,
        GoalStatus.COMPLETED,
    ) is GoalStatus.COMPLETED

    assert GoalLifecycle.transition(
        GoalStatus.ACTIVE,
        GoalStatus.FAILED,
    ) is GoalStatus.FAILED

    assert GoalLifecycle.transition(
        GoalStatus.ACTIVE,
        GoalStatus.CANCELLED,
    ) is GoalStatus.CANCELLED


def test_goal_can_be_cancelled_before_activation():
    assert GoalLifecycle.can_transition(
        GoalStatus.CREATED,
        GoalStatus.CANCELLED,
    )


@pytest.mark.parametrize(
    "current,target",
    [
        (GoalStatus.CREATED, GoalStatus.COMPLETED),
        (GoalStatus.CREATED, GoalStatus.FAILED),
        (GoalStatus.COMPLETED, GoalStatus.ACTIVE),
        (GoalStatus.COMPLETED, GoalStatus.FAILED),
        (GoalStatus.FAILED, GoalStatus.ACTIVE),
        (GoalStatus.CANCELLED, GoalStatus.ACTIVE),
    ],
)
def test_invalid_goal_transitions_are_rejected(current, target):
    assert not GoalLifecycle.can_transition(current, target)

    with pytest.raises(ValueError):
        GoalLifecycle.transition(current, target)


def test_goal_lifecycle_rejects_invalid_status_types():
    with pytest.raises(TypeError):
        GoalLifecycle.can_transition("created", GoalStatus.ACTIVE)

    with pytest.raises(TypeError):
        GoalLifecycle.can_transition(GoalStatus.CREATED, "active")