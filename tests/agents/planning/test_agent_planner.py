from brain.agents.planning.agent_planner import AgentPlanner


def test_agent_planner_is_abstract() -> None:
    assert AgentPlanner.__abstractmethods__ == {"plan"}