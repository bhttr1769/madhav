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

from brain.engineering.generation.generation_response_parser import (
    GenerationResponseParser,
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
        request: GenerationRequest,
        response: str,
    ) -> GenerationResult:

        return GenerationResponseParser.parse(
            response,
        )