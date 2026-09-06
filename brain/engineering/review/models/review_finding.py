from dataclasses import dataclass


@dataclass(frozen=True)
class ReviewFinding:
    """
    Represents a single code review finding.
    """

    severity: str
    category: str
    path: str
    message: str
    recommendation: str