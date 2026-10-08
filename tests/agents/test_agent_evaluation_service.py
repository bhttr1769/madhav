import pytest

from brain.agents.agent_evaluation_service import (
    AgentEvaluationService,
)
from brain.agents.models.agent_evaluation_evidence import (
    AgentEvaluationEvidence,
)
from brain.agents.models.agent_performance_record import (
    AgentPerformanceRecord,
)
from brain.capabilities.models.capability_execution_result import (
    CapabilityExecutionResult,
)
from brain.capabilities.models.capability_verification import (
    CapabilityVerification,
)


def create_successful_execution():
    return CapabilityExecutionResult(
        capability_id="test.execute",
        output="done",
        status="success",
    )


def create_verified_result():
    return CapabilityVerification(
        capability_id="test.execute",
        passed=True,
        status="verified",
        evidence="done",
        rationale="Execution was verified.",
    )


def create_failed_execution():
    return CapabilityExecutionResult(
        capability_id="test.execute",
        output=None,
        status="failed",
        error="execution failed",
    )


def create_failed_verification():
    return CapabilityVerification(
        capability_id="test.execute",
        passed=False,
        status="failed",
        evidence="execution failed",
        rationale="Execution failed.",
    )


def create_unknown_verification():
    return CapabilityVerification(
        capability_id="test.execute",
        passed=False,
        status="unknown",
        evidence=None,
        rationale="Verification could not determine the outcome.",
    )


def test_evaluate_creates_successful_evidence():
    service = AgentEvaluationService()

    evidence = service.evaluate(
        agent_id="agent-1",
        task_id="task-1",
        execution_result=create_successful_execution(),
        verification=create_verified_result(),
    )

    assert isinstance(
        evidence,
        AgentEvaluationEvidence,
    )
    assert evidence.agent_id == "agent-1"
    assert evidence.task_id == "task-1"
    assert evidence.execution_status == "success"
    assert evidence.verification_status == "verified"
    assert evidence.verification_passed is True
    assert evidence.outcome == "successful"


def test_evaluate_creates_unsuccessful_evidence():
    service = AgentEvaluationService()

    evidence = service.evaluate(
        agent_id="agent-1",
        task_id="task-1",
        execution_result=create_failed_execution(),
        verification=create_failed_verification(),
    )

    assert evidence.execution_status == "failed"
    assert evidence.verification_status == "failed"
    assert evidence.verification_passed is False
    assert evidence.outcome == "unsuccessful"


def test_evaluate_creates_inconclusive_evidence():
    service = AgentEvaluationService()

    evidence = service.evaluate(
        agent_id="agent-1",
        task_id="task-1",
        execution_result=create_successful_execution(),
        verification=create_unknown_verification(),
    )

    assert evidence.execution_status == "success"
    assert evidence.verification_status == "unknown"
    assert evidence.verification_passed is False
    assert evidence.outcome == "inconclusive"


def test_evaluate_requires_matching_capability_ids():
    service = AgentEvaluationService()

    verification = CapabilityVerification(
        capability_id="different.capability",
        passed=True,
        status="verified",
        evidence="done",
        rationale="Verified.",
    )

    with pytest.raises(
        ValueError,
        match="capability IDs must match",
    ):
        service.evaluate(
            agent_id="agent-1",
            task_id="task-1",
            execution_result=create_successful_execution(),
            verification=verification,
        )


def test_evaluate_validates_execution_result():
    service = AgentEvaluationService()

    with pytest.raises(
        TypeError,
        match="execution_result",
    ):
        service.evaluate(
            agent_id="agent-1",
            task_id="task-1",
            execution_result=object(),
            verification=create_verified_result(),
        )


def test_evaluate_validates_verification():
    service = AgentEvaluationService()

    with pytest.raises(
        TypeError,
        match="verification",
    ):
        service.evaluate(
            agent_id="agent-1",
            task_id="task-1",
            execution_result=create_successful_execution(),
            verification=object(),
        )


def test_evaluate_validates_agent_id():
    service = AgentEvaluationService()

    with pytest.raises(TypeError):
        service.evaluate(
            agent_id=123,
            task_id="task-1",
            execution_result=create_successful_execution(),
            verification=create_verified_result(),
        )


def test_evaluate_validates_task_id():
    service = AgentEvaluationService()

    with pytest.raises(TypeError):
        service.evaluate(
            agent_id="agent-1",
            task_id=123,
            execution_result=create_successful_execution(),
            verification=create_verified_result(),
        )


def test_record_evidence_updates_successful_record():
    service = AgentEvaluationService()

    record = AgentPerformanceRecord(
        agent_id="agent-1",
    )

    evidence = service.evaluate(
        agent_id="agent-1",
        task_id="task-1",
        execution_result=create_successful_execution(),
        verification=create_verified_result(),
    )

    updated = service.record_evidence(
        record,
        evidence,
    )

    assert updated.total_evaluations == 1
    assert updated.successful_outcomes == 1
    assert updated.unsuccessful_outcomes == 0
    assert updated.inconclusive_outcomes == 0
    assert updated.verified_successes == 1
    assert updated.verified_failures == 0
    assert updated.reliability == 1.0


def test_record_evidence_updates_failed_record():
    service = AgentEvaluationService()

    record = AgentPerformanceRecord(
        agent_id="agent-1",
    )

    evidence = service.evaluate(
        agent_id="agent-1",
        task_id="task-1",
        execution_result=create_failed_execution(),
        verification=create_failed_verification(),
    )

    updated = service.record_evidence(
        record,
        evidence,
    )

    assert updated.total_evaluations == 1
    assert updated.successful_outcomes == 0
    assert updated.unsuccessful_outcomes == 1
    assert updated.inconclusive_outcomes == 0
    assert updated.verified_successes == 0
    assert updated.verified_failures == 1
    assert updated.reliability == 0.0


def test_record_evidence_keeps_unknown_inconclusive():
    service = AgentEvaluationService()

    record = AgentPerformanceRecord(
        agent_id="agent-1",
    )

    evidence = service.evaluate(
        agent_id="agent-1",
        task_id="task-1",
        execution_result=create_successful_execution(),
        verification=create_unknown_verification(),
    )

    updated = service.record_evidence(
        record,
        evidence,
    )

    assert updated.total_evaluations == 1
    assert updated.successful_outcomes == 0
    assert updated.unsuccessful_outcomes == 0
    assert updated.inconclusive_outcomes == 1
    assert updated.verified_successes == 0
    assert updated.verified_failures == 0
    assert updated.reliability == 0.0


def test_record_evidence_does_not_mutate_original():
    service = AgentEvaluationService()

    record = AgentPerformanceRecord(
        agent_id="agent-1",
    )

    evidence = service.evaluate(
        agent_id="agent-1",
        task_id="task-1",
        execution_result=create_successful_execution(),
        verification=create_verified_result(),
    )

    updated = service.record_evidence(
        record,
        evidence,
    )

    assert record.total_evaluations == 0
    assert updated is not record


def test_record_evidence_requires_matching_agent():
    service = AgentEvaluationService()

    record = AgentPerformanceRecord(
        agent_id="agent-1",
    )

    evidence = AgentEvaluationEvidence(
        agent_id="agent-2",
        task_id="task-1",
        execution_status="success",
        verification_status="verified",
        verification_passed=True,
        outcome="successful",
    )

    with pytest.raises(
        ValueError,
        match="agent_id",
    ):
        service.record_evidence(
            record,
            evidence,
        )


def test_record_evidence_validates_record():
    service = AgentEvaluationService()

    evidence = AgentEvaluationEvidence(
        agent_id="agent-1",
        task_id="task-1",
        execution_status="success",
        verification_status="verified",
        verification_passed=True,
        outcome="successful",
    )

    with pytest.raises(TypeError):
        service.record_evidence(
            object(),
            evidence,
        )


def test_record_evidence_validates_evidence():
    service = AgentEvaluationService()

    record = AgentPerformanceRecord(
        agent_id="agent-1",
    )

    with pytest.raises(TypeError):
        service.record_evidence(
            record,
            object(),
        )