
import pytest

from brain.agents.models.agent_identity import AgentIdentity
from brain.organization.models.organization import Organization
from brain.organization.models.organizational_unit import OrganizationalUnit
from brain.organization.models.reporting_relationship import (
    ReportingRelationship,
)
from brain.organization.organization_structure_validator import (
    OrganizationStructureValidator,
)


@pytest.fixture
def validator():
    return OrganizationStructureValidator()


@pytest.fixture
def organization():
    return Organization("madhav", "Madhav AI")


@pytest.fixture
def agents():
    return (
        AgentIdentity("director", "Director"),
        AgentIdentity("lead", "Engineering Lead"),
        AgentIdentity("developer", "Developer"),
    )


def test_accepts_valid_structure(validator, organization, agents):
    units = (
        OrganizationalUnit("engineering", "madhav", "Engineering"),
        OrganizationalUnit("research", "madhav", "Research"),
        OrganizationalUnit(
            "backend", "madhav", "Backend", "engineering"
        ),
    )
    relationships = (
        ReportingRelationship("lead", "director"),
        ReportingRelationship("developer", "lead"),
    )

    assert validator.validate(
        organization, units, agents, relationships
    ) is None


def test_accepts_multiple_root_units(validator, organization):
    units = (
        OrganizationalUnit("engineering", "madhav", "Engineering"),
        OrganizationalUnit("research", "madhav", "Research"),
    )
    assert validator.validate(organization, units, (), ()) is None


def test_accepts_agents_without_managers(validator, organization, agents):
    assert validator.validate(organization, (), agents, ()) is None


def test_rejects_invalid_organization(validator):
    with pytest.raises(TypeError, match="organization"):
        validator.validate("madhav", (), (), ())


@pytest.mark.parametrize(
    ("units", "message"),
    [
        (
            (
                OrganizationalUnit("eng", "madhav", "Engineering"),
                OrganizationalUnit("eng", "madhav", "Duplicate"),
            ),
            "duplicate organizational unit ID",
        ),
        (
            (OrganizationalUnit("eng", "other", "Engineering"),),
            "different organization",
        ),
        (
            (
                OrganizationalUnit(
                    "eng", "madhav", "Engineering", "missing"
                ),
            ),
            "parent unit does not exist",
        ),
        (
            (
                OrganizationalUnit(
                    "eng", "madhav", "Engineering", "backend"
                ),
                OrganizationalUnit(
                    "backend", "madhav", "Backend", "eng"
                ),
            ),
            "contains a cycle",
        ),
    ],
)
def test_rejects_invalid_unit_structures(
    validator, organization, units, message
):
    with pytest.raises(ValueError, match=message):
        validator.validate(organization, units, (), ())


def test_rejects_duplicate_agent_ids(validator, organization):
    agents = (
        AgentIdentity("agent-1", "First"),
        AgentIdentity("agent-1", "Second"),
    )

    with pytest.raises(ValueError, match="duplicate agent ID"):
        validator.validate(organization, (), agents, ())


def test_rejects_unknown_reporting_agent(validator, organization, agents):
    relationships = (ReportingRelationship("unknown", "director"),)

    with pytest.raises(ValueError, match="reporting agent does not exist"):
        validator.validate(organization, (), agents, relationships)


def test_rejects_unknown_manager(validator, organization, agents):
    relationships = (ReportingRelationship("developer", "unknown"),)

    with pytest.raises(ValueError, match="manager agent does not exist"):
        validator.validate(organization, (), agents, relationships)


def test_rejects_multiple_managers(validator, organization, agents):
    relationships = (
        ReportingRelationship("developer", "lead"),
        ReportingRelationship("developer", "director"),
    )

    with pytest.raises(ValueError, match="multiple direct managers"):
        validator.validate(organization, (), agents, relationships)


def test_rejects_reporting_cycle(validator, organization, agents):
    relationships = (
        ReportingRelationship("director", "lead"),
        ReportingRelationship("lead", "developer"),
        ReportingRelationship("developer", "director"),
    )

    with pytest.raises(ValueError, match="reporting hierarchy contains a cycle"):
        validator.validate(organization, (), agents, relationships)


@pytest.mark.parametrize(
    ("units", "agents", "relationships", "message"),
    [
        (("invalid",), (), (), "OrganizationalUnit"),
        ((), ("invalid",), (), "AgentIdentity"),
        ((), (), ("invalid",), "ReportingRelationship"),
    ],
)
def test_rejects_invalid_collection_items(
    validator, organization, units, agents, relationships, message
):
    with pytest.raises(TypeError, match=message):
        validator.validate(organization, units, agents, relationships)


def test_rejects_invalid_collection_type(validator, organization):
    with pytest.raises(TypeError, match="units"):
        validator.validate(organization, "invalid", (), ())
