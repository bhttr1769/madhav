
from collections.abc import Sequence

from brain.agents.models.agent_identity import AgentIdentity
from brain.organization.models.organization import Organization
from brain.organization.models.organizational_unit import OrganizationalUnit
from brain.organization.models.reporting_relationship import (
    ReportingRelationship,
)


class OrganizationStructureValidator:
    """Validate the structural integrity of an organization snapshot."""

    def validate(
        self,
        organization: Organization,
        units: Sequence[OrganizationalUnit],
        agents: Sequence[AgentIdentity],
        reporting_relationships: Sequence[ReportingRelationship],
    ) -> None:
        if not isinstance(organization, Organization):
            raise TypeError("organization must be an Organization")

        if not isinstance(units, (tuple, list)):
            raise TypeError("units must be a tuple or list")

        if not isinstance(agents, (tuple, list)):
            raise TypeError("agents must be a tuple or list")

        if not isinstance(reporting_relationships, (tuple, list)):
            raise TypeError(
                "reporting_relationships must be a tuple or list"
            )

        unit_by_id: dict[str, OrganizationalUnit] = {}

        for unit in units:
            if not isinstance(unit, OrganizationalUnit):
                raise TypeError(
                    "units must contain only OrganizationalUnit instances"
                )

            if unit.id in unit_by_id:
                raise ValueError(f"duplicate organizational unit ID: {unit.id}")

            if unit.organization_id != organization.id:
                raise ValueError(
                    f"unit {unit.id} belongs to a different organization"
                )

            unit_by_id[unit.id] = unit

        for unit in units:
            parent_id = unit.parent_unit_id

            if parent_id is not None and parent_id not in unit_by_id:
                raise ValueError(
                    f"parent unit does not exist: {parent_id}"
                )

        self._validate_unit_hierarchy(unit_by_id)

        agent_ids: set[str] = set()

        for agent in agents:
            if not isinstance(agent, AgentIdentity):
                raise TypeError(
                    "agents must contain only AgentIdentity instances"
                )

            if not isinstance(agent.id, str):
                raise TypeError("agent ID must be a string")

            if not agent.id.strip():
                raise ValueError("agent ID must not be empty")

            if agent.id in agent_ids:
                raise ValueError(f"duplicate agent ID: {agent.id}")

            agent_ids.add(agent.id)

        subordinate_ids: set[str] = set()

        for relationship in reporting_relationships:
            if not isinstance(relationship, ReportingRelationship):
                raise TypeError(
                    "reporting_relationships must contain only "
                    "ReportingRelationship instances"
                )

            if relationship.agent_id not in agent_ids:
                raise ValueError(
                    "reporting agent does not exist: "
                    f"{relationship.agent_id}"
                )

            if relationship.manager_agent_id not in agent_ids:
                raise ValueError(
                    "manager agent does not exist: "
                    f"{relationship.manager_agent_id}"
                )

            if relationship.agent_id in subordinate_ids:
                raise ValueError(
                    "agent has multiple direct managers: "
                    f"{relationship.agent_id}"
                )

            subordinate_ids.add(relationship.agent_id)

        self._validate_reporting_hierarchy(reporting_relationships)

    @staticmethod
    def _validate_unit_hierarchy(
        unit_by_id: dict[str, OrganizationalUnit],
    ) -> None:
        for start_id in unit_by_id:
            visited: set[str] = set()
            current_id: str | None = start_id

            while current_id is not None:
                if current_id in visited:
                    raise ValueError(
                        "organizational unit hierarchy contains a cycle"
                    )

                visited.add(current_id)
                current_id = unit_by_id[current_id].parent_unit_id

    @staticmethod
    def _validate_reporting_hierarchy(
        relationships: Sequence[ReportingRelationship],
    ) -> None:
        manager_by_agent = {
            relationship.agent_id: relationship.manager_agent_id
            for relationship in relationships
        }

        for start_id in manager_by_agent:
            visited: set[str] = set()
            current_id: str | None = start_id

            while current_id is not None:
                if current_id in visited:
                    raise ValueError(
                        "agent reporting hierarchy contains a cycle"
                    )

                visited.add(current_id)
                current_id = manager_by_agent.get(current_id)
