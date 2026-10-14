
from datetime import datetime, timezone

import pytest

from brain.agents.agent_runtime import AgentRuntime
from brain.agents.agent_runtime_lifecycle import AgentRuntimeLifecycleState
from brain.agents.models.agent_definition import AgentDefinition
from brain.agents.models.agent_identity import AgentIdentity
from brain.capabilities.capability_executor import CapabilityExecutor
from brain.capabilities.capability_registry import CapabilityRegistry
from brain.capabilities.capability_runtime import CapabilityRuntime
from brain.capabilities.models.capability_descriptor import CapabilityDescriptor
from brain.capabilities.models.capability_execution_request import (
    CapabilityExecutionRequest,
)
from brain.capabilities.models.capability_execution_result import (
    CapabilityExecutionResult,
)
from brain.organization.authority_evaluation_service import (
    AuthorityEvaluationService,
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


class OrganizationPersistence:
    def __init__(self, state):
        self.state = state

    def load(self, organization_id):
        if organization_id != self.state.organization.id:
            raise KeyError(organization_id)
        return self.state


class ProtectedCommandCapability:
    """A capability that must pass SafetyService before executing."""

    def __init__(self, safety_service, approval_response):
        self.safety_service = safety_service
        self.approval_response = approval_response
        self.executed_inputs = []

    def execute(self, input_data):
        self.safety_service.authorize(
            Action("execute", "command", str(input_data)),
            self.approval_response,
        )
        self.executed_inputs.append(input_data)
        return "executed"


class FixedResolver:
    def __init__(self, implementation):
        self.implementation = implementation

    def resolve(self, entry_point):
        return self.implementation


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


def create_safety_service(approval_policy=PermissionDecision.ASK):
    persistence = OrganizationPersistence(create_state())

    risk_registry = RiskClassifierRegistry()
    risk_registry.register(FakeRiskClassifier())

    policy_registry = PolicyRegistry()
    policy_registry.register(
        Policy(
            category="command",
            maximum_risk=Risk.LOW,
            decision=approval_policy,
        )
    )

    authority_service = AuthorityEvaluationService(
        trusted_authorities={"org-1": "agent-1"}
    )

    service = SafetyService(
        risk_registry,
        policy_registry,
        organization_persistence=persistence,
        authority_evaluation_service=authority_service,
    )

    return service


def create_runtime(agent_id, capability):
    descriptor = CapabilityDescriptor(
        id="protected.command",
        name="Protected Command",
        description="A safety-enforced test capability",
        version="1.0.0",
        entry_point="test.protected.command",
        dependencies=frozenset(),
    )

    registry = CapabilityRegistry(capabilities=(descriptor,))
    executor = CapabilityExecutor(
        registry,
        resolver=FixedResolver(capability),
    )
    capability_runtime = CapabilityRuntime(executor)

    definition = AgentDefinition(
        identity=AgentIdentity(agent_id, "Test Agent"),
        description="Authority integration test agent",
        version="1.0.0",
        capabilities=frozenset({"protected.command"}),
    )

    runtime = AgentRuntime(
        definition,
        capability_runtime,
        runtime_id=f"runtime-{agent_id}",
        organization_id="org-1",
    )

    runtime.transition_to(AgentRuntimeLifecycleState.READY)
    runtime.transition_to(AgentRuntimeLifecycleState.RUNNING)

    return runtime


def test_unauthorized_agent_cannot_execute_even_with_approval():
    safety_service = create_safety_service()
    capability = ProtectedCommandCapability(
        safety_service,
        ApprovalResponse.APPROVE,
    )
    runtime = create_runtime("agent-2", capability)

    with pytest.raises(
        PermissionError,
        match="Organizational authority denied",
    ):
        runtime.execute_capability(
            "protected.command",
            "dangerous-operation",
        )

    assert capability.executed_inputs == []


def test_trusted_agent_executes_when_safety_policy_is_satisfied():
    safety_service = create_safety_service()
    capability = ProtectedCommandCapability(
        safety_service,
        ApprovalResponse.APPROVE,
    )
    runtime = create_runtime("agent-1", capability)

    result = runtime.execute_capability(
        "protected.command",
        "approved-operation",
    )

    assert result.status == "success"
    assert result.output == "executed"
    assert capability.executed_inputs == ["approved-operation"]


def test_trusted_authority_does_not_override_safety_policy_denial():
    safety_service = create_safety_service(
        approval_policy=PermissionDecision.DENY,
    )
    capability = ProtectedCommandCapability(
        safety_service,
        ApprovalResponse.APPROVE,
    )
    runtime = create_runtime("agent-1", capability)

    with pytest.raises(PermissionError):
        runtime.execute_capability(
            "protected.command",
            "policy-denied-operation",
        )

    assert capability.executed_inputs == []
