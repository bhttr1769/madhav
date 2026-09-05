from brain.engineering.generation.code_generator import CodeGenerator
from brain.engineering.generation.models.code_change import CodeChange
from brain.engineering.generation.models.generation_request import GenerationRequest
from brain.engineering.generation.models.generation_result import GenerationResult
from brain.engineering.generation.generation_response_parser import (
    GenerationResponseParser,
)


class AICodeGenerator(CodeGenerator):
    """
    Uses the AI runtime to generate candidate implementation changes
    from a structured engineering generation request.
    """

    _SUPPORTED_OPERATIONS = {"create", "modify", "delete"}

    def __init__(self, chat_service):
        if not hasattr(chat_service, "chat"):
            raise TypeError("chat_service must provide a chat method")

        self._chat_service = chat_service

    def generate(self, request: GenerationRequest) -> GenerationResult:
        if not isinstance(request, GenerationRequest):
            raise TypeError("request must be a GenerationRequest")

        prompt = self._build_prompt(request)
        response = self._chat_service.chat(prompt)

        return self._parse_response(response)

    @staticmethod
    def _build_prompt(request: GenerationRequest) -> str:
        task = request.task
        design = request.design
        plan = request.plan
        existing_code = request.existing_code
        engineering_decision = request.engineering_decision

        return f"""
You are a senior software engineer.

Generate candidate implementation changes for the supplied engineering task.

The candidate implementation must follow the supplied system design and
engineering plan.

The authoritative engineering decision and existing codebase structure are
provided below. Use them as implementation constraints.

The authoritative engineering decision determines whether implementation
work is required and how reuse, dependencies, abstraction, and optimization
should be handled.

Do not contradict the authoritative engineering decision.

Generate only the code changes necessary to satisfy the task.

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
    "implementation_required": true,
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
- Respect the authoritative engineering decision.
- Inspect the supplied existing code structure before proposing new
  implementation.
- Reuse existing capabilities when they satisfy the task.
- Do not recreate functionality that already exists when it can be reused.
- Do not invent unrelated functionality.
- Do not modify files unrelated to the task.
- Each change must identify a concrete file path.
- operation must be one of: create, modify, delete.
- content must contain the implementation associated with the operation.
- Do not introduce a new dependency unless the authoritative engineering
  decision requires it.
- Prefer the standard library when it provides the required capability.
- Do not introduce unnecessary abstractions.
- Do not perform speculative optimization.
- Only propose optimization-related implementation when justified by the
  authoritative engineering decision.
- Do not assume a specific programming language unless the supplied
  engineering context establishes one.
- The candidate "decision" is metadata only and must not override the
  authoritative engineering decision.
- implementation_required in the candidate decision must be a direct boolean
  judgment about whether new implementation work is required.
- If implementation_required is false, changes must be an empty list.

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

Authoritative engineering decision:

Implementation required:
{engineering_decision.implementation_required}

Necessity:
{engineering_decision.necessity}

Reuse existing:
{engineering_decision.reuse_existing}

Use standard library:
{engineering_decision.use_standard_library}

Use existing dependency:
{engineering_decision.use_existing_dependency}

New dependency required:
{engineering_decision.new_dependency_required}

Abstraction justified:
{engineering_decision.abstraction_justified}

Optimization justified:
{engineering_decision.optimization_justified}

Rationale:
{list(engineering_decision.rationale)}

Existing code structure:

Modules:
{[
    {
        "name": module.name,
        "path": module.path,
    }
    for module in existing_code.modules
]}

Classes:
{[
    {
        "name": class_model.name,
        "module": class_model.module,
    }
    for class_model in existing_code.classes
]}

Functions:
{[
    {
        "name": function.name,
        "module": function.module,
    }
    for function in existing_code.functions
]}

Imports:
{[
    {
        "module": import_model.module,
        "name": import_model.name,
    }
    for import_model in existing_code.imports
]}

Calls:
{[
    {
        "caller": call.caller,
        "callee": call.callee,
    }
    for call in existing_code.calls
]}

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
    def _validate_changes(cls, changes: list[CodeChange]) -> None:
        paths: set[str] = set()

        for change in changes:
            operation = change.operation.strip().lower()
            path = change.path.strip()

            if operation not in cls._SUPPORTED_OPERATIONS:
                raise ValueError("change operation is not supported")

            if path.startswith(("/", "\\")):
                raise ValueError("change path must be relative")

            normalized_path = path.replace("\\", "/")
            parts = normalized_path.split("/")

            if ".." in parts:
                raise ValueError("change path must not contain parent traversal")

            if path in paths:
                raise ValueError("duplicate change paths are not allowed")

            paths.add(path)

            if operation in {"create", "modify"}:
                if not change.content.strip():
                    raise ValueError(
                        "create and modify changes must contain content"
                    )

    @staticmethod
    def _parse_response(
        response: str,
    ) -> GenerationResult:
        return GenerationResponseParser.parse(
            response,
        )
        
