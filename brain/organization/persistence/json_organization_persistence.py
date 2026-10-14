import hashlib
import json
import os
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any

from brain.agents.models.agent_identity import AgentIdentity
from brain.organization.authority_delegation_validator import (
    AuthorityDelegationValidator,
)
from brain.organization.models.authority_delegation import AuthorityDelegation
from brain.organization.models.delegation_scope import DelegationScope
from brain.organization.models.delegation_status import DelegationStatus
from brain.organization.models.membership_status import MembershipStatus
from brain.organization.models.organization import Organization
from brain.organization.models.organization_membership import (
    OrganizationMembership,
)
from brain.organization.models.organization_persistence_state import (
    OrganizationPersistenceState,
)
from brain.organization.models.organizational_role import OrganizationalRole
from brain.organization.models.organizational_unit import OrganizationalUnit
from brain.organization.models.reporting_relationship import (
    ReportingRelationship,
)
from brain.organization.organization_integrity_validator import (
    OrganizationIntegrityValidator,
)


class JsonOrganizationPersistence:
    """Persist complete organization snapshots as versioned JSON files."""

    _SCHEMA_VERSION = 1

    def __init__(
        self,
        storage_dir: str | Path,
        integrity_validator: OrganizationIntegrityValidator | None = None,
        delegation_validator: AuthorityDelegationValidator | None = None,
    ) -> None:
        if integrity_validator is not None and not isinstance(
            integrity_validator,
            OrganizationIntegrityValidator,
        ):
            raise TypeError(
                "integrity_validator must be an "
                "OrganizationIntegrityValidator or None"
            )

        if delegation_validator is not None and not isinstance(
            delegation_validator,
            AuthorityDelegationValidator,
        ):
            raise TypeError(
                "delegation_validator must be an "
                "AuthorityDelegationValidator or None"
            )

        self._storage_dir = Path(storage_dir)
        self._integrity_validator = (
            integrity_validator or OrganizationIntegrityValidator()
        )
        self._delegation_validator = (
            delegation_validator or AuthorityDelegationValidator()
        )

    def save(self, state: OrganizationPersistenceState) -> None:
        """Validate and atomically replace an organization's snapshot."""
        if not isinstance(state, OrganizationPersistenceState):
            raise TypeError(
                "state must be an OrganizationPersistenceState"
            )

        self._validate_state(state)

        payload = {
            "schema_version": self._SCHEMA_VERSION,
            "organization": {
                "id": state.organization.id,
                "name": state.organization.name,
            },
            "units": [
                {
                    "id": unit.id,
                    "organization_id": unit.organization_id,
                    "name": unit.name,
                    "parent_unit_id": unit.parent_unit_id,
                }
                for unit in state.units
            ],
            "agents": [
                {"id": agent.id, "name": agent.name}
                for agent in state.agents
            ],
            "roles": [
                {
                    "id": role.id,
                    "organization_id": role.organization_id,
                    "name": role.name,
                }
                for role in state.roles
            ],
            "memberships": [
                {
                    "id": membership.id,
                    "organization_id": membership.organization_id,
                    "agent_id": membership.agent_id,
                    "organizational_unit_id": (
                        membership.organizational_unit_id
                    ),
                    "role_id": membership.role_id,
                    "status": membership.status.value,
                }
                for membership in state.memberships
            ],
            "reporting_relationships": [
                {
                    "agent_id": relationship.agent_id,
                    "manager_agent_id": relationship.manager_agent_id,
                }
                for relationship in state.reporting_relationships
            ],
            "delegations": [
                self._serialize_delegation(delegation)
                for delegation in state.delegations
            ],
        }

        self._storage_dir.mkdir(parents=True, exist_ok=True)
        target_path = self._path_for(state.organization.id)
        temporary_path: Path | None = None

        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=self._storage_dir,
                suffix=".tmp",
                delete=False,
            ) as file:
                temporary_path = Path(file.name)
                json.dump(payload, file, indent=2)
                file.flush()
                os.fsync(file.fileno())

            temporary_path.replace(target_path)
        finally:
            if temporary_path is not None:
                temporary_path.unlink(missing_ok=True)

    def load(self, organization_id: str) -> OrganizationPersistenceState:
        """Load a complete snapshot or reject it without partial data."""
        if not isinstance(organization_id, str):
            raise TypeError("organization_id must be a string")

        if not organization_id.strip():
            raise ValueError("organization_id must not be empty")

        path = self._path_for(organization_id)

        try:
            with path.open("r", encoding="utf-8") as file:
                payload = json.load(file)
        except FileNotFoundError:
            raise KeyError(organization_id) from None
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            raise ValueError(
                "organization persistence contains invalid JSON"
            ) from exc

        if not isinstance(payload, dict):
            raise ValueError(
                "organization persistence must be a JSON object"
            )

        schema_version = payload.get("schema_version")
        if (
            type(schema_version) is not int
            or schema_version != self._SCHEMA_VERSION
        ):
            raise ValueError(
                "unsupported organization persistence schema version"
            )

        try:
            state = self._deserialize(payload, organization_id)
            self._validate_state(state)
            return state
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError(
                "organization persistence contains invalid state"
            ) from exc

    @staticmethod
    def _serialize_delegation(
        delegation: AuthorityDelegation,
    ) -> dict[str, Any]:
        return {
            "id": delegation.id,
            "organization_id": delegation.organization_id,
            "delegator_agent_id": delegation.delegator_agent_id,
            "delegate_agent_id": delegation.delegate_agent_id,
            "scope": {
                "actions": list(delegation.scope.actions),
                "targets": list(delegation.scope.targets),
            },
            "granted_at": delegation.granted_at.isoformat(),
            "expires_at": (
                delegation.expires_at.isoformat()
                if delegation.expires_at is not None
                else None
            ),
            "status": delegation.status.value,
            "revoked_at": (
                delegation.revoked_at.isoformat()
                if delegation.revoked_at is not None
                else None
            ),
            "parent_delegation_id": delegation.parent_delegation_id,
            "allow_onward_delegation": (
                delegation.allow_onward_delegation
            ),
        }

    @staticmethod
    def _deserialize_delegation(
        item: dict[str, Any],
    ) -> AuthorityDelegation:
        scope_data = item["scope"]
        if not isinstance(scope_data, dict):
            raise TypeError("delegation scope must be a JSON object")

        actions = scope_data["actions"]
        targets = scope_data["targets"]

        if not isinstance(actions, list) or not isinstance(targets, list):
            raise TypeError("delegation scope values must be JSON arrays")

        return AuthorityDelegation(
            id=item["id"],
            organization_id=item["organization_id"],
            delegator_agent_id=item["delegator_agent_id"],
            delegate_agent_id=item["delegate_agent_id"],
            scope=DelegationScope(
                actions=tuple(actions),
                targets=tuple(targets),
            ),
            granted_at=datetime.fromisoformat(item["granted_at"]),
            expires_at=(
                datetime.fromisoformat(item["expires_at"])
                if item["expires_at"] is not None
                else None
            ),
            status=DelegationStatus(item["status"]),
            revoked_at=(
                datetime.fromisoformat(item["revoked_at"])
                if item["revoked_at"] is not None
                else None
            ),
            parent_delegation_id=item["parent_delegation_id"],
            allow_onward_delegation=item["allow_onward_delegation"],
        )

    def _deserialize(
        self,
        payload: dict[str, Any],
        requested_organization_id: str,
    ) -> OrganizationPersistenceState:
        organization_data = payload["organization"]
        if not isinstance(organization_data, dict):
            raise TypeError("organization must be a JSON object")

        organization = Organization(
            id=organization_data["id"],
            name=organization_data["name"],
        )

        if organization.id != requested_organization_id:
            raise ValueError(
                "persisted organization ID does not match requested ID"
            )

        units_data = self._require_list(payload, "units")
        agents_data = self._require_list(payload, "agents")
        roles_data = self._require_list(payload, "roles")
        memberships_data = self._require_list(payload, "memberships")
        relationships_data = self._require_list(
            payload,
            "reporting_relationships",
        )

        # Keep compatibility with existing version-1 snapshots that predate
        # delegation persistence.
        delegations_data = payload.get("delegations", [])
        if not isinstance(delegations_data, list):
            raise TypeError("delegations must be a JSON array")

        units = tuple(
            OrganizationalUnit(
                id=item["id"],
                organization_id=item["organization_id"],
                name=item["name"],
                parent_unit_id=item["parent_unit_id"],
            )
            for item in self._require_object_items(units_data, "units")
        )

        agents = tuple(
            AgentIdentity(
                id=item["id"],
                name=item["name"],
            )
            for item in self._require_object_items(agents_data, "agents")
        )

        roles = tuple(
            OrganizationalRole(
                id=item["id"],
                organization_id=item["organization_id"],
                name=item["name"],
            )
            for item in self._require_object_items(roles_data, "roles")
        )

        memberships = tuple(
            OrganizationMembership(
                id=item["id"],
                organization_id=item["organization_id"],
                agent_id=item["agent_id"],
                organizational_unit_id=item["organizational_unit_id"],
                role_id=item["role_id"],
                status=MembershipStatus(item["status"]),
            )
            for item in self._require_object_items(
                memberships_data,
                "memberships",
            )
        )

        relationships = tuple(
            ReportingRelationship(
                agent_id=item["agent_id"],
                manager_agent_id=item["manager_agent_id"],
            )
            for item in self._require_object_items(
                relationships_data,
                "reporting_relationships",
            )
        )

        delegations = tuple(
            self._deserialize_delegation(item)
            for item in self._require_object_items(
                delegations_data,
                "delegations",
            )
        )

        return OrganizationPersistenceState(
            organization=organization,
            units=units,
            agents=agents,
            roles=roles,
            memberships=memberships,
            reporting_relationships=relationships,
            delegations=delegations,
        )

    @staticmethod
    def _require_list(
        payload: dict[str, Any],
        field_name: str,
    ) -> list[Any]:
        value = payload[field_name]
        if not isinstance(value, list):
            raise TypeError(f"{field_name} must be a JSON array")
        return value

    @staticmethod
    def _require_object_items(
        items: list[Any],
        field_name: str,
    ) -> list[dict[str, Any]]:
        if not all(isinstance(item, dict) for item in items):
            raise TypeError(
                f"{field_name} must contain only JSON objects"
            )
        return items

    def _validate_state(self, state: OrganizationPersistenceState) -> None:
        # Validate organization structure and references first.
        self._integrity_validator.validate(
            organization=state.organization,
            units=state.units,
            agents=state.agents,
            roles=state.roles,
            memberships=state.memberships,
            reporting_relationships=state.reporting_relationships,
        )

        # Then validate delegation membership, parent chains, scope limits,
        # onward-delegation rules, and cycles across the complete snapshot.
        self._delegation_validator.validate(
            organization=state.organization,
            memberships=state.memberships,
            delegations=state.delegations,
        )

    def _path_for(self, organization_id: str) -> Path:
        digest = hashlib.sha256(
            organization_id.encode("utf-8")
        ).hexdigest()
        return self._storage_dir / f"organization-{digest}.json"