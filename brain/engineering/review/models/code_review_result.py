from dataclasses import dataclass

from brain.engineering.review.models.review_finding import ReviewFinding


@dataclass(frozen=True)
class CodeReviewResult:
    """
    Represents the result of reviewing proposed code changes.
    """

    approved: bool
    findings: tuple[ReviewFinding, ...]
    summary: str