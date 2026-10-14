
from dataclasses import FrozenInstanceError

import pytest

from brain.organization.models.reporting_relationship import (
    ReportingRelationship,
)


def test_creates_valid_relationship():
    relationship = ReportingRelationship(
        agent_id="researcher",
        manager_agent_id="research-lead",
    )

    assert relationship.agent_id == "researcher"
    assert relationship.manager_agent_id == "research-lead"


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("agent_id", ""),
        ("manager_agent_id", ""),
        ("agent_id", " "),
        ("manager_agent_id", " "),
    ],
)
def test_rejects_empty_ids(field, value):
    values = {
        "agent_id": "researcher",
        "manager_agent_id": "research-lead",
    }
    values[field] = value

    with pytest.raises(ValueError, match=field):
        ReportingRelationship(**values)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("agent_id", 123),
        ("manager_agent_id", None),
    ],
)
def test_rejects_non_string_ids(field, value):
    values = {
        "agent_id": "researcher",
        "manager_agent_id": "research-lead",
    }
    values[field] = value

    with pytest.raises(TypeError, match=field):
        ReportingRelationship(**values)


def test_rejects_self_reporting():
    with pytest.raises(ValueError, match="report to itself"):
        ReportingRelationship(
            agent_id="researcher",
            manager_agent_id="researcher",
        )


def test_relationship_is_immutable():
    relationship = ReportingRelationship("researcher", "research-lead")

    with pytest.raises(FrozenInstanceError):
        relationship.manager_agent_id = "director"


def test_relationship_equality():
    first = ReportingRelationship("researcher", "research-lead")
    second = ReportingRelationship("researcher", "research-lead")

    assert first == second
