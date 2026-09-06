import json

from brain.engineering.testing.models.test_generation_result import (
    TestGenerationResult,
)

from brain.engineering.generation.models.code_change import (
    CodeChange,
)


class TestGenerationResponseParser:
    """
    Parses and validates AI responses for test generation.
    """

    _SUPPORTED_OPERATIONS = {
        "create",
        "modify",
        "delete",
    }

    @classmethod
    def parse(
        cls,
        response: str,
    ) -> TestGenerationResult:

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

        if set(payload) != {"changes"}:
            raise ValueError(
                "response must contain exactly the changes field"
            )

        raw_changes = payload["changes"]

        if not isinstance(raw_changes, list):
            raise ValueError(
                "changes must be a list"
            )

        changes: list[CodeChange] = []

        for raw_change in raw_changes:

            if not isinstance(raw_change, dict):
                raise ValueError(
                    "each change must be an object"
                )

            if set(raw_change) != {
                "path",
                "operation",
                "content",
            }:
                raise ValueError(
                    "each change must contain exactly path, operation, and content"
                )

            path = raw_change["path"]
            operation = raw_change["operation"]
            content = raw_change["content"]

            if not isinstance(path, str):
                raise TypeError(
                    "change path must be a string"
                )

            if not isinstance(operation, str):
                raise TypeError(
                    "change operation must be a string"
                )

            if not isinstance(content, str):
                raise TypeError(
                    "change content must be a string"
                )

            path = path.strip()
            operation = operation.strip().lower()

            if not path:
                raise ValueError(
                    "change path must not be empty"
                )

            if not operation:
                raise ValueError(
                    "change operation must not be empty"
                )

            if operation not in cls._SUPPORTED_OPERATIONS:
                raise ValueError(
                    "change operation is not supported"
                )

            if path.startswith(("/", "\\")):
                raise ValueError(
                    "change path must be relative"
                )

            normalized_path = path.replace("\\", "/")
            parts = normalized_path.split("/")

            if ".." in parts:
                raise ValueError(
                    "change path must not contain parent traversal"
                )

            if operation in {"create", "modify"}:
                if not content.strip():
                    raise ValueError(
                        "create and modify changes must contain content"
                    )

            changes.append(
                CodeChange(
                    path=path,
                    operation=operation,
                    content=content,
                )
            )

        cls._validate_duplicate_paths(changes)

        return TestGenerationResult(
            changes=tuple(changes),
        )

    @staticmethod
    def _validate_duplicate_paths(
        changes: list[CodeChange],
    ) -> None:

        paths: set[str] = set()

        for change in changes:
            if change.path in paths:
                raise ValueError(
                    "duplicate change paths are not allowed"
                )

            paths.add(change.path)