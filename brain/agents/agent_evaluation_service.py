from dataclasses import replace

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


class AgentEvaluationService:
    """
    Converts authoritative execution and verification results into
    evaluation evidence and aggregates that evidence into a new
    performance record.

    This service does not execute capabilities or perform verification.
    """

    def evaluate(
        self,
        agent_id: str,
        task_id: str,
        execution_result: CapabilityExecutionResult,
        verification: CapabilityVerification,
    ) -> AgentEvaluationEvidence:
        self._validate_agent_id(agent_id)
        self._validate_task_id(task_id)

        if not isinstance(
            execution_result,
            CapabilityExecutionResult,
        ):
            raise TypeError(
                "execution_result must be a CapabilityExecutionResult"
            )

        if not isinstance(
            verification,
            CapabilityVerification,
        ):
            raise TypeError(
                "verification must be a CapabilityVerification"
            )

        if (
            execution_result.capability_id
            != verification.capability_id
        ):
            raise ValueError(
                "execution and verification capability IDs must match"
            )

        if verification.status == "verified":
            outcome = "successful"
        elif verification.status == "failed":
            outcome = "unsuccessful"
        else:
            outcome = "inconclusive"

        return AgentEvaluationEvidence(
            agent_id=agent_id,
            task_id=task_id,
            execution_status=execution_result.status,
            verification_status=verification.status,
            verification_passed=verification.passed,
            outcome=outcome,
        )

    def record_evidence(
        self,
        record: AgentPerformanceRecord,
        evidence: AgentEvaluationEvidence,
    ) -> AgentPerformanceRecord:
        if not isinstance(
            record,
            AgentPerformanceRecord,
        ):
            raise TypeError(
                "record must be an AgentPerformanceRecord"
            )

        if not isinstance(
            evidence,
            AgentEvaluationEvidence,
        ):
            raise TypeError(
                "evidence must be an AgentEvaluationEvidence"
            )

        if record.agent_id != evidence.agent_id:
            raise ValueError(
                "evidence agent_id must match performance record agent_id"
            )

        successful = record.successful_outcomes
        unsuccessful = record.unsuccessful_outcomes
        inconclusive = record.inconclusive_outcomes
        verified_successes = record.verified_successes
        verified_failures = record.verified_failures

        if evidence.outcome == "successful":
            successful += 1
        elif evidence.outcome == "unsuccessful":
            unsuccessful += 1
        else:
            inconclusive += 1

        if evidence.verification_status == "verified":
            verified_successes += 1
        elif evidence.verification_status == "failed":
            verified_failures += 1

        return replace(
            record,
            total_evaluations=record.total_evaluations + 1,
            successful_outcomes=successful,
            unsuccessful_outcomes=unsuccessful,
            inconclusive_outcomes=inconclusive,
            verified_successes=verified_successes,
            verified_failures=verified_failures,
        )

    @staticmethod
    def _validate_agent_id(agent_id: str) -> None:
        if not isinstance(agent_id, str):
            raise TypeError("agent_id must be a string")

        if not agent_id.strip():
            raise ValueError("agent_id must not be empty")

    @staticmethod
    def _validate_task_id(task_id: str) -> None:
        if not isinstance(task_id, str):
            raise TypeError("task_id must be a string")

        if not task_id.strip():
            raise ValueError("task_id must not be empty")