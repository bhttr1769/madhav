import json

from brain.engineering.analysis.models.analysis_request import (
    NecessityReuseRequest,
)

from brain.engineering.analysis.necessity_reuse_analyzer import (
    NecessityReuseAnalyzer,
)

from brain.engineering.generation.models.engineering_decision import (
    EngineeringDecision,
)


class AINecessityReuseAnalyzer(
    NecessityReuseAnalyzer,
):
    """
    Uses the AI runtime to determine whether an implementation
    is necessary and whether existing capabilities should be reused.
    """

    def __init__(
        self,
        chat_service,
    ):
        if not hasattr(
            chat_service,
            "chat",
        ):
            raise TypeError(
                "chat_service must provide a chat method"
            )

        self._chat_service = chat_service

    def analyze(
        self,
        request: NecessityReuseRequest,
    ) -> EngineeringDecision:

        if not isinstance(
            request,
            NecessityReuseRequest,
        ):
            raise TypeError(
                "request must be a NecessityReuseRequest"
            )

        prompt = self._build_prompt(
            request,
        )

        response = self._chat_service.chat(
            prompt,
        )

        return self._parse_response(
            response,
        )

    @staticmethod
    def _build_prompt(
        request: NecessityReuseRequest,
    ) -> str:

        task = request.task
        design = request.design
        existing_code = request.existing_code

        return f"""
You are a senior software engineer performing necessity and reuse analysis.

Determine whether implementation is necessary for the supplied engineering
task and whether existing project capabilities should be reused.

Do not generate code.

Do not perform optimization analysis.

Do not perform code review.

Do not propose refactoring.

Return ONLY valid JSON.
Do not use markdown.
Do not include explanations outside the JSON.

The JSON must contain exactly these fields:

{{
  "necessity": "string",
  "reuse_existing": false,
  "use_standard_library": false,
  "use_existing_dependency": false,
  "new_dependency_required": false,
  "abstraction_justified": false,
  "optimization_justified": false,
  "rationale": ["string"]
}}

Rules:

- Determine whether the requested implementation is actually necessary.
- Determine whether an existing project capability can satisfy the task.
- Consider the standard library.
- Consider dependencies already present in the project.
- Only justify a new dependency when genuinely required.
- Only justify a new abstraction when genuinely required.
- Do not perform optimization analysis.
- Do not invent capabilities that are not present in the supplied context.
- Base reuse analysis on the supplied existing-code structure.
- Keep the rationale specific to the supplied engineering context.

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

Acceptance criteria:
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

Existing code structure:

Modules:
{sorted(
    repr(module)
    for module in existing_code.modules
)}

Classes:
{sorted(
    repr(class_model)
    for class_model in existing_code.classes
)}

Functions:
{sorted(
    repr(function)
    for function in existing_code.functions
)}

Imports:
{sorted(
    repr(import_model)
    for import_model in existing_code.imports
)}

Calls:
{sorted(
    repr(call)
    for call in existing_code.calls
)}
""".strip()

    @staticmethod
    def _parse_response(
        response: str,
    ) -> EngineeringDecision:

        if not isinstance(
            response,
            str,
        ):
            raise TypeError(
                "AI response must be a string"
            )

        try:
            data = json.loads(
                response,
            )

        except json.JSONDecodeError as error:
            raise ValueError(
                "AI response must contain valid JSON"
            ) from error

        if not isinstance(
            data,
            dict,
        ):
            raise ValueError(
                "AI response must be a JSON object"
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

        if set(data) != decision_fields:
            raise ValueError(
                "AI response contains an invalid schema"
            )

        necessity = data["necessity"]

        if not isinstance(
            necessity,
            str,
        ):
            raise TypeError(
                "decision necessity must be a string"
            )

        if not necessity.strip():
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
                data[field],
                bool,
            ):
                raise TypeError(
                    f"decision {field} must be a boolean"
                )

        rationale = data["rationale"]

        if not isinstance(
            rationale,
            list,
        ):
            raise TypeError(
                "decision rationale must be a list"
            )

        if not all(
            isinstance(
                item,
                str,
            )
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
            necessity=necessity,
            reuse_existing=data[
                "reuse_existing"
            ],
            use_standard_library=data[
                "use_standard_library"
            ],
            use_existing_dependency=data[
                "use_existing_dependency"
            ],
            new_dependency_required=data[
                "new_dependency_required"
            ],
            abstraction_justified=data[
                "abstraction_justified"
            ],
            optimization_justified=data[
                "optimization_justified"
            ],
            rationale=tuple(
                rationale
            ),
        )