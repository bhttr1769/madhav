from brain.agents.agent_registry import AgentRegistry
from brain.agents.models.agent_assignment import AgentAssignment
from brain.agents.models.agent_definition import AgentDefinition
from brain.agents.models.agent_performance_record import (
    AgentPerformanceRecord,
)
from brain.agents.models.agent_task import AgentTask


class AgentSelector:
    def __init__(self, registry: AgentRegistry):
        if not isinstance(registry, AgentRegistry):
            raise TypeError("registry must be an AgentRegistry")

        self._registry = registry

    def select(
        self,
        required_capabilities: frozenset[str],
        performance_records: tuple[
            AgentPerformanceRecord, ...
        ] = (),
    ) -> AgentDefinition:
        if not isinstance(required_capabilities, frozenset):
            raise TypeError(
                "required_capabilities must be a frozenset"
            )

        for capability_id in required_capabilities:
            if not isinstance(capability_id, str):
                raise TypeError(
                    "required_capabilities must contain only strings"
                )

            if not capability_id.strip():
                raise ValueError(
                    "required_capabilities must contain only "
                    "non-empty strings"
                )

        if not isinstance(performance_records, tuple):
            raise TypeError(
                "performance_records must be a tuple"
            )

        for record in performance_records:
            if not isinstance(
                record,
                AgentPerformanceRecord,
            ):
                raise TypeError(
                    "performance_records must contain only "
                    "AgentPerformanceRecord instances"
                )

        matching_agents = tuple(
            agent
            for agent in self._registry.all()
            if required_capabilities.issubset(
                agent.capabilities
            )
        )

        if not matching_agents:
            raise ValueError(
                "No registered agent matches the required capabilities"
            )

        # Preserve existing selector behavior.
        if len(matching_agents) == 1:
            return matching_agents[0]

        # Preserve existing ambiguity behavior when
        # performance data is not available.
        if not performance_records:
            raise ValueError(
                "Multiple registered agents match the required capabilities"
            )

        records_by_agent_id = {
            record.agent_id: record
            for record in performance_records
        }

        matching_agent_ids = tuple(
            agent.identity.id
            for agent in matching_agents
        )

        # Missing performance data must not be interpreted
        # as poor performance.
        if not all(
            agent_id in records_by_agent_id
            for agent_id in matching_agent_ids
        ):
            raise ValueError(
                "Multiple registered agents match the required "
                "capabilities and performance data is incomplete"
            )

        highest_reliability = max(
            records_by_agent_id[agent_id].reliability
            for agent_id in matching_agent_ids
        )

        best_agents = tuple(
            agent
            for agent in matching_agents
            if records_by_agent_id[
                agent.identity.id
            ].reliability == highest_reliability
        )

        if len(best_agents) != 1:
            raise ValueError(
                "Multiple registered agents match the required "
                "capabilities with equal performance"
            )

        return best_agents[0]

    def delegate(
        self,
        task: AgentTask,
        required_capabilities: frozenset[str],
        performance_records: tuple[
            AgentPerformanceRecord, ...
        ] = (),
    ) -> AgentAssignment:
        if not isinstance(task, AgentTask):
            raise TypeError(
                "task must be an AgentTask"
            )

        selected_agent = self.select(
            required_capabilities=required_capabilities,
            performance_records=performance_records,
        )

        return AgentAssignment(
            task_id=task.id,
            agent_id=selected_agent.identity.id,
        )