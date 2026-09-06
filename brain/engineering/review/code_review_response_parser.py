import json

from brain.engineering.review.models.code_review_result import (
    CodeReviewResult,
)

from brain.engineering.review.models.review_finding import (
    ReviewFinding,
)


class CodeReviewResponseParser:
    """
    Parses and validates AI responses for code review.
    """

    _SUPPORTED_SEVERITIES = {
        "critical",
        "high",
        "medium",
        "low",
    }

    _SUPPORTED_CATEGORIES = {
        "correctness",
        "security",
        "performance",
        "maintainability",
        "design",
        "testing",
        "style",
    }

    @classmethod
    def parse(
        cls,
        response: str,
    ) -> CodeReviewResult:

        if not isinstance(response, str):
            raise TypeError(
                "response must be a string"
            )

        try:
            payload = json.loads(response)
        except json.JSONDecodeError as exc:
            raise ValueError(
                "response must contain valid JSON"
            ) from exc

        if not isinstance(payload, dict):
            raise ValueError(
                "response must contain a JSON object"
            )

        if set(payload) != {
            "approved",
            "findings",
            "summary",
        }:
            raise ValueError(
                "response must contain exactly approved, findings, and summary"
            )

        approved = payload["approved"]
        findings = payload["findings"]
        summary = payload["summary"]

        if not isinstance(approved, bool):
            raise TypeError(
                "approved must be a boolean"
            )

        if not isinstance(findings, list):
            raise ValueError(
                "findings must be a list"
            )

        if not isinstance(summary, str):
            raise TypeError(
                "summary must be a string"
            )

        summary = summary.strip()

        if not summary:
            raise ValueError(
                "summary must not be empty"
            )

        parsed_findings: list[ReviewFinding] = []

        for raw_finding in findings:
            parsed_findings.append(
                cls._parse_finding(raw_finding)
            )

        return CodeReviewResult(
            approved=approved,
            findings=tuple(parsed_findings),
            summary=summary,
        )

    @classmethod
    def _parse_finding(
        cls,
        raw_finding,
    ) -> ReviewFinding:

        if not isinstance(raw_finding, dict):
            raise ValueError(
                "each finding must be an object"
            )

        if set(raw_finding) != {
            "severity",
            "category",
            "path",
            "message",
            "recommendation",
        }:
            raise ValueError(
                "each finding must contain exactly severity, category, path, message, and recommendation"
            )

        severity = raw_finding["severity"]
        category = raw_finding["category"]
        path = raw_finding["path"]
        message = raw_finding["message"]
        recommendation = raw_finding["recommendation"]

        fields = {
            "severity": severity,
            "category": category,
            "path": path,
            "message": message,
            "recommendation": recommendation,
        }

        for name, value in fields.items():
            if not isinstance(value, str):
                raise TypeError(
                    f"finding {name} must be a string"
                )

        severity = severity.strip().lower()
        category = category.strip().lower()
        path = path.strip()
        message = message.strip()
        recommendation = recommendation.strip()

        if not severity:
            raise ValueError(
                "finding severity must not be empty"
            )

        if severity not in cls._SUPPORTED_SEVERITIES:
            raise ValueError(
                "finding severity is not supported"
            )

        if not category:
            raise ValueError(
                "finding category must not be empty"
            )

        if category not in cls._SUPPORTED_CATEGORIES:
            raise ValueError(
                "finding category is not supported"
            )

        if not path:
            raise ValueError(
                "finding path must not be empty"
            )

        if path.startswith(("/", "\\")):
            raise ValueError(
                "finding path must be relative"
            )

        normalized_path = path.replace("\\", "/")
        parts = normalized_path.split("/")

        if ".." in parts:
            raise ValueError(
                "finding path must not contain parent traversal"
            )

        if not message:
            raise ValueError(
                "finding message must not be empty"
            )

        if not recommendation:
            raise ValueError(
                "finding recommendation must not be empty"
            )

        return ReviewFinding(
            severity=severity,
            category=category,
            path=path,
            message=message,
            recommendation=recommendation,
        )