import json
from pathlib import PurePosixPath

from brain.engineering.debugging.models.debugging_result import (
    DebuggingResult,
)
from brain.engineering.generation.models.code_change import CodeChange


class DebuggingResponseParser:
    _ALLOWED_OPERATIONS = frozenset(
        {"create", "modify", "delete"}
    )
    _REQUIRED_KEYS = frozenset({"changes", "diagnosis"})
    _CHANGE_KEYS = frozenset(
        {"path", "operation", "content"}
    )

    @classmethod
    def parse(cls, response: str) -> DebuggingResult:
        if not isinstance(response, str):
            raise TypeError("response must be a string")

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

        if set(payload) != cls._REQUIRED_KEYS:
            raise ValueError(
                "response must contain exactly "
                "'changes' and 'diagnosis'"
            )

        changes = payload["changes"]
        diagnosis = payload["diagnosis"]

        if not isinstance(changes, list):
            raise ValueError("changes must be a list")

        if not isinstance(diagnosis, str):
            raise ValueError(
                "diagnosis must be a string"
            )

        if not diagnosis.strip():
            raise ValueError(
                "diagnosis must not be empty"
            )

        parsed_changes = []
        paths = set()

        for change in changes:
            if not isinstance(change, dict):
                raise ValueError(
                    "each change must be an object"
                )

            if set(change) != cls._CHANGE_KEYS:
                raise ValueError(
                    "each change must contain exactly "
                    "'path', 'operation', and 'content'"
                )

            path = change["path"]
            operation = change["operation"]
            content = change["content"]

            if not isinstance(path, str):
                raise ValueError(
                    "change path must be a string"
                )

            if not isinstance(operation, str):
                raise ValueError(
                    "change operation must be a string"
                )

            if not isinstance(content, str):
                raise ValueError(
                    "change content must be a string"
                )

            operation = operation.lower()

            if operation not in cls._ALLOWED_OPERATIONS:
                raise ValueError(
                    f"unsupported change operation: {operation}"
                )

            cls._validate_path(path)

            if path in paths:
                raise ValueError(
                    f"duplicate change path: {path}"
                )

            paths.add(path)

            if operation in {"create", "modify"}:
                if not content.strip():
                    raise ValueError(
                        "create and modify changes "
                        "must contain content"
                    )

            parsed_changes.append(
                CodeChange(
                    path=path,
                    operation=operation,
                    content=content,
                )
            )

        return DebuggingResult(
            changes=tuple(parsed_changes),
            diagnosis=diagnosis,
        )

    @staticmethod
    def _validate_path(path: str) -> None:
        if not path.strip():
            raise ValueError(
                "change path must not be empty"
            )

        pure_path = PurePosixPath(path)

        if pure_path.is_absolute():
            raise ValueError(
                "change path must be relative"
            )

        if path.startswith(("\\", "/")):
            raise ValueError(
                "change path must be relative"
            )

        if ".." in pure_path.parts:
            raise ValueError(
                "change path must not contain '..'"
            )