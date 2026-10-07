from brain.agents.goal_task_persistence import GoalTaskPersistence


def test_goal_task_persistence_is_a_protocol():
    assert getattr(
        GoalTaskPersistence,
        "__protocol_attrs__",
        None,
    ) is not None