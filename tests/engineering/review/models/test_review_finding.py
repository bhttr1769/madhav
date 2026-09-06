from brain.engineering.review.models.review_finding import (
    ReviewFinding,
)


def test_review_finding_is_constructible():
    finding = ReviewFinding(
        severity="high",
        category="correctness",
        path="brain/example.py",
        message="Incorrect behavior.",
        recommendation="Fix the implementation.",
    )

    assert finding.severity == "high"
    assert finding.category == "correctness"
    assert finding.path == "brain/example.py"
    assert finding.message == "Incorrect behavior."
    assert finding.recommendation == "Fix the implementation."