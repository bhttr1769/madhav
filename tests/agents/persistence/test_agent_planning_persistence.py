from brain.agents.persistence.agent_planning_persistence import (
    AgentPlanningPersistence,
)


def test_agent_planning_persistence_is_abstract() -> None:
    assert AgentPlanningPersistence.__abstractmethods__ == {
        "save",
        "load",
    }