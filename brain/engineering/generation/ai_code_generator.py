import json

from brain.engineering.generation.code_generator import (
    CodeGenerator,
)

from brain.engineering.generation.models.code_change import (
    CodeChange,
)

from brain.engineering.generation.models.engineering_decision import (
    EngineeringDecision,
)

from brain.engineering.generation.models.generation_request import (
    GenerationRequest,
)

from brain.engineering.generation.models.generation_result import (
    GenerationResult,
)


class AICodeGenerator(CodeGenerator):
    """
    Uses the AI runtime to generate implementation changes
    from a structured engineering generation request.
    """

    _SUPPORTED_OPERATIONS = {
        "create",
        "modify",
        "delete",
    }

    def __init__(
        self,
        chat_service,
    ):
        if not hasattr(chat_service, "chat"):
            raise TypeError(
                "chat_service must provide a chat method"
            )

        self._chat_service = chat_service

    def generate(
        self,
        request: GenerationRequest,
    ) -> GenerationResult:

        if not isinstance(
            request,
            GenerationRequest,
        ):
            raise TypeError(
                "request must be a GenerationRequest"
            )

        prompt = self._build_prompt(
            request,
        )

        response = self._chat_service.chat(
            prompt,
        )

        return self._parse_response(
            request,
            response,
        )

    @staticmethod
    def _build_prompt(
        request: GenerationRequest,
    ) -> str:

        task = request.task
        design = request.design
        plan = request.plan

        return f"""
You are a senior software engineer.

Generate the implementation required for the supplied engineering task.

The implementation must follow the supplied system design and engineering
plan. Generate only the code changes necessary to satisfy the task.

Return ONLY valid JSON.
Do not use markdown.
Do not include explanations outside the JSON.

The JSON must contain exactly these fields:

{{
  "changes": [
    {{
      "path": "path/to/file",
      "operation": "create",
      "content": "complete file content"
    }}
  ],
  "decision": {{
    "necessity": "string",
    "reuse_existing": false,
    "use_standard_library": false,
    "use_existing_dependency": false,
    "new_dependency_required": false,
    "abstraction_justified": false,
    "optimization_justified": false,
    "rationale": ["string"]
  }}
}}

Rules:

- Implement only the supplied task.
- Follow the supplied system design.
- Follow the supplied engineering plan.
- Do not invent unrelated functionality.
- Do not modify files unrelated to the task.
- Each change must identify a concrete file path.
- operation must describe the intended codebase operation.
- content must contain the implementation associated with the operation.
- Do not introduce a new dependency unless the implementation genuinely requires it.
- Prefer the standard library when it provides the required capability.
- Reuse existing capabilities when the supplied engineering context indicates
  that they should be reused.
- Do not perform speculative optimization.
- Do not introduce unnecessary abstractions.
- The engineering decision must explain why implementation is or is not
  necessary and how reuse, dependencies, abstraction, and optimization were
  considered.
- Do not assume a specific programming language unless the supplied
  engineering context establishes one.

Engineering task:

ID:
{task.id}

Description:
{task.description}

Category:
{task.category}

Dependencies:
{sorted(task.dependencies)}

Affected areas:
{sorted(task.affected_areas)}

Task acceptance criteria:
{sorted(task.acceptance_criteria)}

System design:

Requirement objective:
{design.requirement.objective}

Components:
{[
    {
        "id": component.id,
        "name": component.name,
        "responsibility": component.responsibility,
        "layer": component.layer,
        "interfaces": sorted(component.interfaces),
    }
    for component in design.components
]}

Interfaces:
{[
    {
        "id": interface.id,
        "name": interface.name,
        "owner": interface.owner,
        "consumers": sorted(interface.consumers),
        "purpose": interface.purpose,
    }
    for interface in design.interfaces
]}

Dependencies:
{[
    {
        "source": dependency.source,
        "target": dependency.target,
        "reason": dependency.reason,
    }
    for dependency in design.dependencies
]}

Data flows:
{[
    {
        "source": flow.source,
        "target": flow.target,
        "data": flow.data,
    }
    for flow in design.data_flows
]}

Design constraints:
{sorted(design.constraints)}

Design decisions:
{sorted(design.decisions)}

Design acceptance criteria:
{sorted(design.acceptance_criteria)}

Engineering plan:

Task order:
{list(plan.task_order)}

Strategy:
{list(plan.strategy)}

Milestones:
{list(plan.milestones)}

Required capabilities:
{sorted(plan.required_capabilities)}

Risks:
{sorted(plan.risks)}

Assumptions:
{sorted(plan.assumptions)}

Validation strategy:
{list(plan.validation_strategy)}

Plan confidence:
{plan.confidence}
""".strip()

    @classmethod
    def _validate_changes(
        cls,
        changes: list[CodeChange],
    ) -> None:

        paths: set[str] = set()

        for change in changes:

            operation = change.operation.strip().lower()
            path = change.path.strip()

            if operation not in cls._SUPPORTED_OPERATIONS:
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
    def _parse_response(
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

        required_fields = {
            "changes",
            "decision",
        }

        if set(data) != required_fields:
            raise ValueError(
                "AI response contains an invalid schema"
            )

        raw_changes = data["changes"]

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

        raw_decision = data["decision"]

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

        AICodeGenerator._validate_changes(changes)

        decision = EngineeringDecision(
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

        return GenerationResult(
            changes=tuple(changes),
            decision=decision,
        )