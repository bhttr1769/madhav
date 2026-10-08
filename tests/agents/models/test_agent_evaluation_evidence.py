import pytest

from brain.agents.models.agent_evaluation_evidence import (
    AgentEvaluationEvidence,
)


def test_valid_successful_evidence():
    evidence = AgentEvaluationEvidence(
        agent_id="agent-1",
        task_id="task-1",
        execution_status="success",
        verification_status="verified",
        verification_passed=True,
        outcome="successful",
    )

    assert evidence.agent_id == "agent-1"
    assert evidence.task_id == "task-1"
    assert evidence.execution_status == "success"
    assert evidence.verification_status == "verified"
    assert evidence.verification_passed is True
    assert evidence.outcome == "successful"


def test_valid_unsuccessful_evidence():
    evidence = AgentEvaluationEvidence(
        agent_id="agent-1",
        task_id="task-1",
        execution_status="failed",
        verification_status="failed",
        verification_passed=False,
        outcome="unsuccessful",
    )

    assert evidence.outcome == "unsuccessful"


def test_valid_inconclusive_evidence():
    evidence = AgentEvaluationEvidence(
        agent_id="agent-1",
        task_id="task-1",
        execution_status="success",
        verification_status="unknown",
        verification_passed=False,
        outcome="inconclusive",
    )

    assert evidence.outcome == "inconclusive"


def test_agent_id_must_be_non_empty_string():
    with pytest.raises(TypeError):
        AgentEvaluationEvidence(
            agent_id=123,
            task_id="task-1",
            execution_status="success",
            verification_status="verified",
            verification_passed=True,
            outcome="successful",
        )

    with pytest.raises(ValueError):
        AgentEvaluationEvidence(
            agent_id="",
            task_id="task-1",
            execution_status="success",
            verification_status="verified",
            verification_passed=True,
            outcome="successful",
        )


def test_task_id_must_be_non_empty_string():
    with pytest.raises(TypeError):
        AgentEvaluationEvidence(
            agent_id="agent-1",
            task_id=123,
            execution_status="success",
            verification_status="verified",
            verification_passed=True,
            outcome="successful",
        )

    with pytest.raises(ValueError):
        AgentEvaluationEvidence(
            agent_id="agent-1",
            task_id="",
            execution_status="success",
            verification_status="verified",
            verification_passed=True,
            outcome="successful",
        )


def test_execution_status_must_be_supported():
    with pytest.raises(ValueError):
        AgentEvaluationEvidence(
            agent_id="agent-1",
            task_id="task-1",
            execution_status="unknown",
            verification_status="verified",
            verification_passed=True,
            outcome="successful",
        )


def test_verification_status_must_be_supported():
    with pytest.raises(ValueError):
        AgentEvaluationEvidence(
            agent_id="agent-1",
            task_id="task-1",
            execution_status="success",
            verification_status="invalid",
            verification_passed=True,
            outcome="successful",
        )


def test_verified_requires_passed_true():
    with pytest.raises(ValueError):
        AgentEvaluationEvidence(
            agent_id="agent-1",
            task_id="task-1",
            execution_status="success",
            verification_status="verified",
            verification_passed=False,
            outcome="successful",
        )


def test_failed_verification_requires_passed_false():
    with pytest.raises(ValueError):
        AgentEvaluationEvidence(
            agent_id="agent-1",
            task_id="task-1",
            execution_status="failed",
            verification_status="failed",
            verification_passed=True,
            outcome="unsuccessful",
        )


def test_unknown_verification_requires_passed_false():
    with pytest.raises(ValueError):
        AgentEvaluationEvidence(
            agent_id="agent-1",
            task_id="task-1",
            execution_status="success",
            verification_status="unknown",
            verification_passed=True,
            outcome="inconclusive",
        )


def test_verified_requires_successful_outcome():
    with pytest.raises(ValueError):
        AgentEvaluationEvidence(
            agent_id="agent-1",
            task_id="task-1",
            execution_status="success",
            verification_status="verified",
            verification_passed=True,
            outcome="inconclusive",
        )


def test_failed_verification_requires_unsuccessful_outcome():
    with pytest.raises(ValueError):
        AgentEvaluationEvidence(
            agent_id="agent-1",
            task_id="task-1",
            execution_status="failed",
            verification_status="failed",
            verification_passed=False,
            outcome="successful",
        )


def test_unknown_verification_requires_inconclusive_outcome():
    with pytest.raises(ValueError):
        AgentEvaluationEvidence(
            agent_id="agent-1",
            task_id="task-1",
            execution_status="success",
            verification_status="unknown",
            verification_passed=False,
            outcome="successful",
        )


def test_evidence_is_immutable():
    evidence = AgentEvaluationEvidence(
        agent_id="agent-1",
        task_id="task-1",
        execution_status="success",
        verification_status="verified",
        verification_passed=True,
        outcome="successful",
    )

    with pytest.raises(AttributeError):
        evidence.outcome = "unsuccessful"