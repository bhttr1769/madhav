import json

from brain.engineering.generation.models.code_change import (
    CodeChange,
)

from brain.engineering.generation.models.engineering_decision import (
    EngineeringDecision,
)

from brain.engineering.generation.models.generation_result import (
    GenerationResult,
)


class GenerationResponseParser:
    """
    Parses and validates AI-generated code-generation responses.

    This component owns deterministic validation of generated changes
    and engineering decisions. It performs no AI interaction and does
    not modify files.
    """

    SUPPORTED_OPERATIONS = frozenset(
        {
            "create",
            "modify",
            "delete",
        }
    )

    @classmethod
    def parse(
        cls,
        response: str,
    ) -> GenerationResult:

        if not isinstance(response, str):
            raise TypeError(
                "AI response must be a string"
            )

        try:
            data = json.loads(response)

        except json.JSONDecodeError as e:
            raise ValueError(
                "AI response must contain valid JSON"
            ) from e

        if not isinstance(data, dict):
            raise ValueError(
                "AI response must be a JSON object"
            )

        if set(data) != {
            "changes",
            "decision",
        }:
            raise ValueError(
                "AI response contains an invalid schema"
            )

        changes = cls._parse_changes(
            data["changes"],
        )

        decision = cls._parse_decision(
            data["decision"],
        )

        cls._validate_changes(
            changes,
        )

        return GenerationResult(
            changes=tuple(changes),
            decision=decision,
        )

    @classmethod
    def _parse_changes(
        cls,
        raw_changes,
    ) -> list[CodeChange]:

        if not isinstance(
            raw_changes,
            list,
        ):
            raise TypeError(
                "changes must be a list"
            )

        changes = []

        for raw_change in raw_changes:

            if not isinstance(
                raw_change,
                dict,
            ):
                raise TypeError(
                    "each change must be a JSON object"
                )

            if set(raw_change) != {
                "path",
                "operation",
                "content",
            }:
                raise ValueError(
                    "change contains an invalid schema"
                )

            for field in (
                "path",
                "operation",
                "content",
            ):
                if not isinstance(
                    raw_change[field],
                    str,
                ):
                    raise TypeError(
                        f"change {field} must be a string"
                    )

                if not raw_change[field].strip():
                    raise ValueError(
                        f"change {field} must not be empty"
                    )

            changes.append(
                CodeChange(
                    path=raw_change["path"],
                    operation=raw_change["operation"],
                    content=raw_change["content"],
                )
            )

        return changes

    @classmethod
    def _validate_changes(
        cls,
        changes: list[CodeChange],
    ) -> None:

        paths: set[str] = set()

        for change in changes:

            operation = change.operation.strip().lower()
            path = change.path.strip()

            if operation not in cls.SUPPORTED_OPERATIONS:
                raise ValueError(
                    "change operation is not supported"
                )

            if path.startswith(("/", "\\")):
                raise ValueError(
                    "change path must be relative"
                )

            normalized_path = path.replace(
                "\\",
                "/",
            )

            parts = normalized_path.split("/")

            if ".." in parts:
                raise ValueError(
                    "change path must not contain parent traversal"
                )

            if path in paths:
                raise ValueError(
                    "duplicate change paths are not allowed"
                )

            paths.add(path)

            if operation in {
                "create",
                "modify",
            }:
                if not change.content.strip():
                    raise ValueError(
                        "create and modify changes must contain content"
                    )

    @staticmethod
    def _parse_decision(
        raw_decision,
    ) -> EngineeringDecision:

        if not isinstance(
            raw_decision,
            dict,
        ):
            raise TypeError(
                "decision must be a JSON object"
            )

        decision_fields = {
            "necessity",
            "reuse_existing",
            "use_standard_library",
            "use_existing_dependency",
            "new_dependency_required",
            "abstraction_justified",
            "optimization_justified",
            "rationale",
        }

        if set(raw_decision) != decision_fields:
            raise ValueError(
                "decision contains an invalid schema"
            )

        if not isinstance(
            raw_decision["necessity"],
            str,
        ):
            raise TypeError(
                "decision necessity must be a string"
            )

        if not raw_decision["necessity"].strip():
            raise ValueError(
                "decision necessity must not be empty"
            )

        boolean_fields = (
            "reuse_existing",
            "use_standard_library",
            "use_existing_dependency",
            "new_dependency_required",
            "abstraction_justified",
            "optimization_justified",
        )

        for field in boolean_fields:

            if not isinstance(
                raw_decision[field],
                bool,
            ):
                raise TypeError(
                    f"decision {field} must be a boolean"
                )

        rationale = raw_decision["rationale"]

        if not isinstance(
            rationale,
            list,
        ):
            raise TypeError(
                "decision rationale must be a list"
            )

        if not all(
            isinstance(item, str)
            for item in rationale
        ):
            raise TypeError(
                "decision rationale must contain only strings"
            )

        if not all(
            item.strip()
            for item in rationale
        ):
            raise ValueError(
                "decision rationale must not contain empty strings"
            )

        return EngineeringDecision(
            necessity=raw_decision["necessity"],
            reuse_existing=raw_decision[
                "reuse_existing"
            ],
            use_standard_library=raw_decision[
                "use_standard_library"
            ],
            use_existing_dependency=raw_decision[
                "use_existing_dependency"
            ],
            new_dependency_required=raw_decision[
                "new_dependency_required"
            ],
            abstraction_justified=raw_decision[
                "abstraction_justified"
            ],
            optimization_justified=raw_decision[
                "optimization_justified"
            ],
            rationale=tuple(
                rationale
            ),
        )