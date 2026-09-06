from abc import ABC, abstractmethod

from brain.engineering.review.models.code_review_request import (
    CodeReviewRequest,
)
from brain.engineering.review.models.code_review_result import (
    CodeReviewResult,
)


class CodeReviewer(ABC):
    """
    Interface for reviewing proposed code changes.
    """

    @abstractmethod
    def review(
        self,
        request: CodeReviewRequest,
    ) -> CodeReviewResult:
        """
        Review proposed code changes.
        """
        pass