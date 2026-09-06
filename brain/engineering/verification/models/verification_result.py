from dataclasses import dataclass


@dataclass(frozen=True)
class VerificationResult:
    passed: bool
    return_code: int
    stdout: str
    stderr: str