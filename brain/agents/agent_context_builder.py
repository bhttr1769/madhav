from brain.agents.models.agent_context import AgentContext


class AgentContextBuilder:
    """
    Builds agent context from existing subsystem context objects.

    This class coordinates source integration only.
    It does not create, retrieve, or transform source data.
    """

    def build(
        self,
        runtime_id: str,
        agent_id: str,
        user: object | None = None,
        project: object | None = None,
        environment: object | None = None,
        memory: object | None = None,
        knowledge: object | None = None,
        perception: object | None = None,
        runtime: object | None = None,
    ) -> AgentContext:
        return AgentContext(
            runtime_id=runtime_id,
            agent_id=agent_id,
            user=user,
            project=project,
            environment=environment,
            memory=memory,
            knowledge=knowledge,
            perception=perception,
            runtime=runtime,
        )