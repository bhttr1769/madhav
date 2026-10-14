import json
from pathlib import Path

import pytest

from brain.agents.models.agent_identity import AgentIdentity
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
from brain.organization.persistence.json_organization_persistence import (
    JsonOrganizationPersistence,
)


@pytest.fixture
def persistence(tmp_path):
    return JsonOrganizationPersistence(tmp_path / "organizations")


@pytest.fixture
def state():
    organization = Organization("madhav", "Madhav AI")

    units = (
        OrganizationalUnit("engineering", "madhav", "Engineering"),
        OrganizationalUnit(
            "backend", "madhav", "Backend", "engineering"
        ),
    )

    agents = (
        AgentIdentity("director", "Director"),
        AgentIdentity("developer", "Developer"),
    )

    roles = (
        OrganizationalRole("lead-role", "madhav", "Lead"),
        OrganizationalRole("developer-role", "madhav", "Developer"),
    )

    memberships = (
        OrganizationMembership(
            "membership-director",
            "madhav",
            "director",
            "engineering",
            "lead-role",
        ),
        OrganizationMembership(
            "membership-developer",
            "madhav",
            "developer",
            "backend",
            "developer-role",
        ),
    )

    relationships = (
        ReportingRelationship("developer", "director"),
    )

    return OrganizationPersistenceState(
        organization=organization,
        units=units,
        agents=agents,
        roles=roles,
        memberships=memberships,
        reporting_relationships=relationships,
    )


def test_round_trip_preserves_complete_snapshot(persistence, state):
    persistence.save(state)

    loaded = persistence.load("madhav")

    assert loaded == state


def test_round_trip_preserves_inactive_membership(persistence, state):
    inactive_membership = OrganizationMembership(
        "membership-developer",
        "madhav",
        "developer",
        "backend",
        "developer-role",
        MembershipStatus.INACTIVE,
    )

    inactive_state = OrganizationPersistenceState(
        organization=state.organization,
        units=state.units,
        agents=state.agents,
        roles=state.roles,
        memberships=(state.memberships[0], inactive_membership),
        reporting_relationships=(),
    )

    persistence.save(inactive_state)

    assert persistence.load("madhav") == inactive_state


def test_raises_key_error_when_snapshot_is_missing(persistence):
    with pytest.raises(KeyError, match="madhav"):
        persistence.load("madhav")


def test_rejects_invalid_json(persistence):
    persistence._storage_dir.mkdir(parents=True)
    path = persistence._path_for("madhav")
    path.write_text("{invalid json", encoding="utf-8")

    with pytest.raises(ValueError, match="invalid JSON"):
        persistence.load("madhav")


def test_rejects_non_object_json(persistence):
    persistence._storage_dir.mkdir(parents=True)
    path = persistence._path_for("madhav")
    path.write_text("[]", encoding="utf-8")

    with pytest.raises(ValueError, match="JSON object"):
        persistence.load("madhav")


def test_rejects_unsupported_schema_version(persistence, state):
    persistence.save(state)

    path = persistence._path_for("madhav")
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["schema_version"] = 2
    path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(ValueError, match="schema version"):
        persistence.load("madhav")


def test_rejects_snapshot_with_wrong_organization_id(
    persistence, state
):
    persistence.save(state)

    path = persistence._path_for("madhav")
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["organization"]["id"] = "another-org"
    path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(ValueError, match="invalid state"):
        persistence.load("madhav")


def test_rejects_invalid_membership_reference(persistence, state):
    persistence.save(state)

    path = persistence._path_for("madhav")
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["memberships"][1]["role_id"] = "missing-role"
    path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(ValueError, match="invalid state"):
        persistence.load("madhav")


def test_rejects_invalid_reporting_relationship(persistence, state):
    invalid_state = OrganizationPersistenceState(
        organization=state.organization,
        units=state.units,
        agents=state.agents,
        roles=state.roles,
        memberships=state.memberships,
        reporting_relationships=(
            ReportingRelationship("unknown-agent", "director"),
        ),
    )

    with pytest.raises(ValueError, match="reporting agent does not exist"):
        persistence.save(invalid_state)

    with pytest.raises(KeyError):
        persistence.load("madhav")


def test_rejects_invalid_collection_shape(persistence, state):
    persistence.save(state)

    path = persistence._path_for("madhav")
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["units"] = {}
    path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(ValueError, match="invalid state"):
        persistence.load("madhav")


def test_failed_replace_preserves_previous_snapshot(
    persistence, state, monkeypatch
):
    persistence.save(state)
    path = persistence._path_for("madhav")
    original_contents = path.read_bytes()

    def fail_replace(self, target):
        raise OSError("simulated replacement failure")

    monkeypatch.setattr(Path, "replace", fail_replace)

    changed_state = OrganizationPersistenceState(
        organization=Organization("madhav", "Madhav AI Updated"),
        units=state.units,
        agents=state.agents,
        roles=state.roles,
        memberships=state.memberships,
        reporting_relationships=state.reporting_relationships,
    )

    with pytest.raises(OSError, match="simulated replacement failure"):
        persistence.save(changed_state)

    assert path.read_bytes() == original_contents


def test_rejects_wrong_state_type(persistence):
    with pytest.raises(TypeError, match="OrganizationPersistenceState"):
        persistence.save("invalid")