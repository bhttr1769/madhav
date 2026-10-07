import pytest

from brain.agents.agent_task_lifecycle import AgentTaskLifecycle
from brain.agents.models.agent_task_status import AgentTaskStatus


def test_valid_agent_task_transitions():
    assert AgentTaskLifecycle.transition(
        AgentTaskStatus.CREATED,
        AgentTaskStatus.ACTIVE,
    ) is AgentTaskStatus.ACTIVE

    assert AgentTaskLifecycle.transition(
        AgentTaskStatus.ACTIVE,
        AgentTaskStatus.COMPLETED,
    ) is AgentTaskStatus.COMPLETED

    assert AgentTaskLifecycle.transition(
        AgentTaskStatus.ACTIVE,
        AgentTaskStatus.FAILED,
    ) is AgentTaskStatus.FAILED

    assert AgentTaskLifecycle.transition(
        AgentTaskStatus.ACTIVE,
        AgentTaskStatus.CANCELLED,
    ) is AgentTaskStatus.CANCELLED


def test_agent_task_can_be_cancelled_before_activation():
    assert AgentTaskLifecycle.can_transition(
        AgentTaskStatus.CREATED,
        AgentTaskStatus.CANCELLED,
    )


@pytest.mark.parametrize(
    "current,target",
    [
        (AgentTaskStatus.CREATED, AgentTaskStatus.COMPLETED),
        (AgentTaskStatus.CREATED, AgentTaskStatus.FAILED),
        (AgentTaskStatus.COMPLETED, AgentTaskStatus.ACTIVE),
        (AgentTaskStatus.COMPLETED, AgentTaskStatus.FAILED),
        (AgentTaskStatus.FAILED, AgentTaskStatus.ACTIVE),
        (AgentTaskStatus.CANCELLED, AgentTaskStatus.ACTIVE),
    ],
)
def test_invalid_agent_task_transitions_are_rejected(current, target):
    assert not AgentTaskLifecycle.can_transition(current, target)

    with pytest.raises(ValueError):
        AgentTaskLifecycle.transition(current, target)


def test_agent_task_lifecycle_rejects_invalid_status_types():
    with pytest.raises(TypeError):
        AgentTaskLifecycle.can_transition(
            "created",
            AgentTaskStatus.ACTIVE,
        )

    with pytest.raises(TypeError):
        AgentTaskLifecycle.can_transition(
            AgentTaskStatus.CREATED,
            "active",
        )