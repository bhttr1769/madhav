from datetime import datetime, timezone

import pytest

from brain.agents.models.agent_identity import AgentIdentity
from brain.organization.authority_evaluation_service import (
    AuthorityEvaluationService,
)
from brain.organization.authority_execution_context import (
    authority_execution_context,
)
from brain.organization.models.organization import Organization
from brain.organization.models.organization_membership import (
    OrganizationMembership,
)
from brain.organization.models.organization_persistence_state import (
    OrganizationPersistenceState,
)
from brain.organization.models.organizational_role import OrganizationalRole
from brain.organization.models.organizational_unit import OrganizationalUnit
from brain.organization.models.membership_status import MembershipStatus
from brain.safety.models.action import Action
from brain.safety.models.approval_response import ApprovalResponse
from brain.safety.models.permission_decision import PermissionDecision
from brain.safety.models.policy import Policy
from brain.safety.models.risk import Risk
from brain.safety.registries.policy_registry import PolicyRegistry
from brain.safety.registries.risk_classifier_registry import (
    RiskClassifierRegistry,
)
from brain.safety.services.safety_service import SafetyService


class FakeRiskClassifier:
    def classify(self, action):
        return Risk.LOW


class CountingOrganizationPersistence:
    def __init__(self, state):
        self.state = state
        self.load_count = 0

    def load(self, organization_id):
        self.load_count += 1
        if organization_id != self.state.organization.id:
            raise KeyError(organization_id)
        return self.state


def create_state():
    organization = Organization("org-1", "Test Organization")
    unit = OrganizationalUnit("unit-1", "org-1", "Engineering")
    role = OrganizationalRole("role-1", "org-1", "Administrator")
    agent = AgentIdentity("agent-1", "Administrator")
    membership = OrganizationMembership(
        "membership-1",
        "org-1",
        "agent-1",
        "unit-1",
        "role-1",
        MembershipStatus.ACTIVE,
    )

    return OrganizationPersistenceState(
        organization=organization,
        units=(unit,),
        agents=(agent,),
        roles=(role,),
        memberships=(membership,),
        reporting_relationships=(),
    )


def create_safety_service(persistence):
    risk_registry = RiskClassifierRegistry()
    risk_registry.register(FakeRiskClassifier())

    policy_registry = PolicyRegistry()
    policy_registry.register(
        Policy(
            category="command",
            maximum_risk=Risk.LOW,
            decision=PermissionDecision.ASK,
        )
    )

    authority_service = AuthorityEvaluationService(
        trusted_authorities={"org-1": "agent-1"}
    )

    return SafetyService(
        risk_registry,
        policy_registry,
        organization_persistence=persistence,
        authority_evaluation_service=authority_service,
    )


def test_missing_execution_context_denies_even_with_approval():
    persistence = CountingOrganizationPersistence(create_state())
    service = create_safety_service(persistence)
    action = Action("execute", "command", "echo hello")

    with pytest.raises(PermissionError, match="Organizational authority denied"):
        service.authorize(action, ApprovalResponse.APPROVE)

    assert persistence.load_count == 0


def test_missing_organization_snapshot_fails_closed():
    persistence = CountingOrganizationPersistence(create_state())
    service = create_safety_service(persistence)
    action = Action("execute", "command", "echo hello")

    with authority_execution_context("agent-1", "missing-org"):
        with pytest.raises(
            PermissionError,
            match="Organizational authority denied",
        ):
            service.authorize(action, ApprovalResponse.APPROVE)

    assert persistence.load_count == 1


def test_trusted_authority_passes_organizational_check():
    persistence = CountingOrganizationPersistence(create_state())
    service = create_safety_service(persistence)
    action = Action("execute", "command", "echo hello")

    with authority_execution_context("agent-1", "org-1"):
        # Organizational authority passes. The safety policy still requires
        # explicit approval, so approval is supplied here.
        service.authorize(action, ApprovalResponse.APPROVE)

    assert persistence.load_count == 1


def test_every_authorization_reloads_the_snapshot():
    persistence = CountingOrganizationPersistence(create_state())
    service = create_safety_service(persistence)
    action = Action("execute", "command", "echo hello")

    with authority_execution_context("agent-1", "org-1"):
        service.authorize(action, ApprovalResponse.APPROVE)
        service.authorize(action, ApprovalResponse.APPROVE)

    assert persistence.load_count == 2


def test_evaluate_returns_deny_when_execution_context_is_missing():
    persistence = CountingOrganizationPersistence(create_state())
    service = create_safety_service(persistence)
    action = Action("execute", "command", "echo hello")

    assert service.evaluate(action) == PermissionDecision.DENY