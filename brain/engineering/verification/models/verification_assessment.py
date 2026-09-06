from dataclasses import dataclass


@dataclass(frozen=True)
class VerificationAssessment:
    passed: bool
    status: str
    summary: str
    failure_output: str