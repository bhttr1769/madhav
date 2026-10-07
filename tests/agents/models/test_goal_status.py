from brain.agents.models.goal_status import GoalStatus


def test_goal_status_contains_expected_states():
    assert GoalStatus.CREATED.value == "created"
    assert GoalStatus.ACTIVE.value == "active"
    assert GoalStatus.COMPLETED.value == "completed"
    assert GoalStatus.FAILED.value == "failed"
    assert GoalStatus.CANCELLED.value == "cancelled"


def test_goal_status_values_are_unique():
    values = [status.value for status in GoalStatus]

    assert len(values) == len(set(values))