
from unittest.mock import MagicMock

import pytest

from brain.browser.interactive.browser_executor import BrowserExecutor
from brain.browser.interactive.models.browser_action import BrowserAction
from brain.browser.interactive.models.browser_element import BrowserElement
from brain.browser.interactive.safety_browser_action_executor import (
    SafetyBrowserActionExecutor,
)
from brain.environment.models.command import Command
from brain.environment.terminals.safety_terminal import SafetyTerminal
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
from brain.safety.models.permission_decision import PermissionDecision
from brain.safety.models.policy import Policy
from brain.safety.models.risk import Risk
from brain.safety.registries.policy_registry import PolicyRegistry
from brain.safety.registries.risk_classifier_registry import (
    RiskClassifierRegistry,
)
from brain.safety.services.safety_service import SafetyService
from brain.ui.executors.safety_ui_action_executor import (
    SafetyUIActionExecutor,
)
from brain.ui.executors.ui_action_executor import UIActionExecutor
from brain.ui.models.ui_action import UIAction


class FakeRiskClassifier:
    def classify(self, action):
        return Risk.LOW


class OrganizationPersistence:
    def __init__(self):
        organization = Organization("org-1", "Test Organization")
        unit = OrganizationalUnit("unit-1", "org-1", "Engineering")
        role = OrganizationalRole("role-1", "org-1", "Administrator")

        membership = OrganizationMembership(
            "membership-1",
            "org-1",
            "agent-1",
            "unit-1",
            "role-1",
            MembershipStatus.ACTIVE,
        )

        self.state = OrganizationPersistenceState(
            organization=organization,
            units=(unit,),
            agents=(),
            roles=(role,),
            memberships=(membership,),
            reporting_relationships=(),
        )

    def load(self, organization_id):
        if organization_id != self.state.organization.id:
            raise KeyError(organization_id)
        return self.state


class FakeTerminal:
    def __init__(self):
        self.commands = []

    def execute(self, command):
        self.commands.append(command)
        return None


class FakeUIActionExecutor(UIActionExecutor):
    def __init__(self):
        self.actions = []

    def execute(self, action):
        self.actions.append(action)


def create_safety_service():
    risk_registry = RiskClassifierRegistry()
    risk_registry.register(FakeRiskClassifier())

    policy_registry = PolicyRegistry()
    for category in ("browser", "command", "ui"):
        policy_registry.register(
            Policy(
                category=category,
                maximum_risk=Risk.LOW,
                decision=PermissionDecision.ALLOW,
            )
        )

    return SafetyService(
        risk_registry,
        policy_registry,
        organization_persistence=OrganizationPersistence(),
        authority_evaluation_service=AuthorityEvaluationService(
            trusted_authorities={"org-1": "agent-1"}
        ),
    )


def create_browser_action():
    element = BrowserElement(
        element_type="button",
        name="Submit",
        text="Submit",
        selector="button:nth-of-type(1)",
        interactive=True,
    )
    return BrowserAction(action_type="click", target=element)


def create_browser_wrapper(safety_service):
    executor = MagicMock(spec=BrowserExecutor)
    wrapper = SafetyBrowserActionExecutor(
        safety_service=safety_service,
        executor=executor,
    )
    return wrapper, executor


def create_terminal_wrapper(safety_service):
    terminal = FakeTerminal()
    wrapper = SafetyTerminal(safety_service, terminal)
    return wrapper, terminal


def create_ui_wrapper(safety_service):
    executor = FakeUIActionExecutor()
    wrapper = SafetyUIActionExecutor(
        safety_service,
        executor=executor,
    )
    return wrapper, executor


@pytest.mark.parametrize(
    "wrapper_factory,action_factory,execution_attribute",
    [
        (
            create_browser_wrapper,
            create_browser_action,
            "execute",
        ),
        (
            create_terminal_wrapper,
            lambda: Command("echo hello"),
            "commands",
        ),
        (
            create_ui_wrapper,
            lambda: UIAction(action_type="click", x=100, y=200),
            "actions",
        ),
    ],
)
def test_sensitive_wrapper_denies_execution_without_authority(
    wrapper_factory,
    action_factory,
    execution_attribute,
):
    safety_service = create_safety_service()
    wrapper, executor = wrapper_factory(safety_service)

    with pytest.raises(
        PermissionError,
        match="Organizational authority denied",
    ):
        wrapper.execute(action_factory())

    if execution_attribute == "execute":
        executor.execute.assert_not_called()
    else:
        assert getattr(executor, execution_attribute) == []


@pytest.mark.parametrize(
    "wrapper_factory,action_factory,execution_attribute",
    [
        (
            create_browser_wrapper,
            create_browser_action,
            "execute",
        ),
        (
            create_terminal_wrapper,
            lambda: Command("echo hello"),
            "commands",
        ),
        (
            create_ui_wrapper,
            lambda: UIAction(action_type="click", x=100, y=200),
            "actions",
        ),
    ],
)
def test_sensitive_wrapper_allows_trusted_authority_when_policy_allows(
    wrapper_factory,
    action_factory,
    execution_attribute,
):
    safety_service = create_safety_service()
    wrapper, executor = wrapper_factory(safety_service)
    action = action_factory()

    with authority_execution_context("agent-1", "org-1"):
        wrapper.execute(action)

    if execution_attribute == "execute":
        executor.execute.assert_called_once_with(action)
    else:
        assert len(getattr(executor, execution_attribute)) == 1
