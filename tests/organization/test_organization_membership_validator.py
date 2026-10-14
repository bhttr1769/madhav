
import pytest

from brain.agents.models.agent_identity import AgentIdentity
from brain.organization.models.membership_status import MembershipStatus
from brain.organization.models.organization import Organization
from brain.organization.models.organizational_role import OrganizationalRole
from brain.organization.models.organization_membership import (
    OrganizationMembership,
)
from brain.organization.models.organizational_unit import OrganizationalUnit
from brain.organization.organization_membership_validator import (
    OrganizationMembershipValidator,
)


@pytest.fixture
def organization():
    return Organization("madhav", "Madhav AI")


@pytest.fixture
def units():
    return (
        OrganizationalUnit("engineering", "madhav", "Engineering"),
        OrganizationalUnit("research", "madhav", "Research"),
    )


@pytest.fixture
def agents():
    return (
        AgentIdentity("agent-1", "Agent One"),
        AgentIdentity("agent-2", "Agent Two"),
    )


@pytest.fixture
def roles():
    return (
        OrganizationalRole("developer", "madhav", "Developer"),
        OrganizationalRole("lead", "madhav", "Lead"),
    )


@pytest.fixture
def memberships():
    return (
        OrganizationMembership(
            "membership-1", "madhav", "agent-1", "engineering", "developer"
        ),
        OrganizationMembership(
            "membership-2", "madhav", "agent-2", "research", "lead"
        ),
    )


@pytest.fixture
def validator():
    return OrganizationMembershipValidator()


def test_accepts_valid_memberships(
    validator, organization, units, agents, roles, memberships
):
    assert validator.validate(
        organization, units, agents, roles, memberships
    ) is None


def test_accepts_empty_membership_collection(
    validator, organization, units, agents, roles
):
    assert validator.validate(
        organization, units, agents, roles, ()
    ) is None


def test_accepts_inactive_membership(
    validator, organization, units, agents, roles
):
    membership = OrganizationMembership(
        "membership-1",
        "madhav",
        "agent-1",
        "engineering",
        "developer",
        MembershipStatus.INACTIVE,
    )

    assert validator.validate(
        organization, units, agents, roles, (membership,)
    ) is None


def test_rejects_wrong_role_collection_type(
    validator, organization, units, agents
):
    with pytest.raises(TypeError, match="roles"):
        validator.validate(organization, units, agents, "invalid", ())


def test_rejects_wrong_membership_collection_type(
    validator, organization, units, agents, roles
):
    with pytest.raises(TypeError, match="memberships"):
        validator.validate(
            organization, units, agents, roles, "invalid"
        )


def test_rejects_invalid_role_item(
    validator, organization, units, agents
):
    with pytest.raises(TypeError, match="OrganizationalRole"):
        validator.validate(
            organization, units, agents, ("invalid",), ()
        )


def test_rejects_role_from_another_organization(
    validator, organization, units, agents
):
    roles = (OrganizationalRole("developer", "other", "Developer"),)

    with pytest.raises(ValueError, match="different organization"):
        validator.validate(organization, units, agents, roles, ())


def test_rejects_duplicate_role_ids(
    validator, organization, units, agents
):
    roles = (
        OrganizationalRole("developer", "madhav", "Developer"),
        OrganizationalRole("developer", "madhav", "Senior Developer"),
    )

    with pytest.raises(ValueError, match="duplicate organizational role ID"):
        validator.validate(organization, units, agents, roles, ())


def test_rejects_invalid_membership_item(
    validator, organization, units, agents, roles
):
    with pytest.raises(TypeError, match="OrganizationMembership"):
        validator.validate(organization, units, agents, roles, ("invalid",))


def test_rejects_membership_from_another_organization(
    validator, organization, units, agents, roles
):
    membership = OrganizationMembership(
        "membership-1", "other", "agent-1", "engineering", "developer"
    )

    with pytest.raises(ValueError, match="different organization"):
        validator.validate(
            organization, units, agents, roles, (membership,)
        )


def test_rejects_unknown_membership_agent(
    validator, organization, units, agents, roles
):
    membership = OrganizationMembership(
        "membership-1", "madhav", "unknown", "engineering", "developer"
    )

    with pytest.raises(ValueError, match="unknown agent"):
        validator.validate(
            organization, units, agents, roles, (membership,)
        )


def test_rejects_unknown_membership_unit(
    validator, organization, units, agents, roles
):
    membership = OrganizationMembership(
        "membership-1", "madhav", "agent-1", "unknown", "developer"
    )

    with pytest.raises(ValueError, match="unknown organizational unit"):
        validator.validate(
            organization, units, agents, roles, (membership,)
        )


def test_rejects_unknown_membership_role(
    validator, organization, units, agents, roles
):
    membership = OrganizationMembership(
        "membership-1", "madhav", "agent-1", "engineering", "unknown"
    )

    with pytest.raises(ValueError, match="unknown role"):
        validator.validate(
            organization, units, agents, roles, (membership,)
        )


def test_rejects_duplicate_membership_ids(
    validator, organization, units, agents, roles
):
    memberships = (
        OrganizationMembership(
            "membership-1", "madhav", "agent-1", "engineering", "developer"
        ),
        OrganizationMembership(
            "membership-1", "madhav", "agent-2", "research", "lead"
        ),
    )

    with pytest.raises(ValueError, match="duplicate membership ID"):
        validator.validate(
            organization, units, agents, roles, memberships
        )


def test_rejects_multiple_memberships_for_same_agent(
    validator, organization, units, agents, roles
):
    memberships = (
        OrganizationMembership(
            "membership-1", "madhav", "agent-1", "engineering", "developer"
        ),
        OrganizationMembership(
            "membership-2", "madhav", "agent-1", "research", "lead"
        ),
    )

    with pytest.raises(ValueError, match="multiple memberships"):
        validator.validate(
            organization, units, agents, roles, memberships
        )


def test_accepts_inactive_membership_without_duplicate_assignment(
    validator, organization, units, agents, roles
):
    membership = OrganizationMembership(
        "membership-1",
        "madhav",
        "agent-1",
        "engineering",
        "developer",
        MembershipStatus.INACTIVE,
    )

    assert validator.validate(
        organization, units, agents, roles, (membership,)
    ) is None


def test_rejects_invalid_structure_before_membership_validation(
    validator, organization, agents, roles
):
    units = (
        OrganizationalUnit(
            "engineering", "madhav", "Engineering", "missing"
        ),
    )

    with pytest.raises(ValueError, match="parent unit does not exist"):
        validator.validate(organization, units, agents, roles, ())
