import json

from brain.engineering.analysis.complexity_quality_analyzer import (
    ComplexityQualityAnalyzer,
)

from brain.engineering.analysis.models.complexity_quality_request import (
    ComplexityQualityRequest,
)

from brain.engineering.analysis.models.engineering_quality_assessment import (
    EngineeringQualityAssessment,
)


class AIComplexityQualityAnalyzer(
    ComplexityQualityAnalyzer,
):
    """
    Uses the AI runtime to assess complexity and implementation quality
    of a proposed engineering change.
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
        request: ComplexityQualityRequest,
    ) -> EngineeringQualityAssessment:

        if not isinstance(
            request,
            ComplexityQualityRequest,
        ):
            raise TypeError(
                "request must be a ComplexityQualityRequest"
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
        request: ComplexityQualityRequest,
    ) -> str:

        task = request.task
        design = request.design
        plan = request.plan
        engineering_decision = (
            request.engineering_decision
        )
        existing_code = request.existing_code
        proposed_changes = request.proposed_changes

        return f"""
You are a senior software engineer performing complexity and
implementation-quality analysis.

Assess the supplied proposed implementation in the context of the
engineering task, system design, engineering plan, engineering decision,
and existing code structure.

Do not generate code.

Do not modify files.

Do not perform optimization analysis.

Do not decide whether implementation is necessary.
That decision has already been made by the preceding engineering stage.

Do not install or introduce dependencies.

Do not perform repository-wide refactoring.

Evaluate the implementation that is actually supplied.
Do not invent implementation details that are not present in the context.

Return ONLY valid JSON.
Do not use markdown.
Do not include explanations outside the JSON.

The JSON must contain exactly these fields:

{{
  "complexity": "string",
  "structural_complexity": "string",
  "cognitive_complexity": "string",
  "algorithmic_complexity": "string",
  "dependency_complexity": "string",
  "abstraction_complexity": "string",
  "maintainability": "string",
  "clarity": "string",
  "cohesion": "string",
  "coupling": "string",
  "testability": "string",
  "extensibility": "string",
  "over_engineering": false,
  "issues": ["string"],
  "strengths": ["string"],
  "recommendations": ["string"],
  "rationale": ["string"]
}}

Analysis principles:

- Evaluate complexity relative to the requested task.
- Evaluate implementation quality relative to the supplied system design.
- Consider the engineering plan when assessing whether the implementation
  follows the intended implementation strategy.
- Consider the engineering decision when evaluating reuse and abstraction.
- Use the supplied existing-code structure to identify architectural
  consistency or unnecessary deviation.
- Distinguish structural complexity from cognitive complexity.
- Consider algorithmic complexity where it is meaningful.
- Consider dependency and abstraction complexity independently.
- Evaluate maintainability, clarity, cohesion, coupling, testability,
  and extensibility.
- Identify unnecessary complexity and over-engineering.
- Also identify under-engineering when it creates maintainability,
  robustness, or structural problems.
- Do not label an implementation as over-engineered merely because it
  contains abstractions. Determine whether those abstractions are
  justified by the supplied context.
- Do not claim that an implementation is functionally correct merely
  because it appears well designed.
- Do not invent performance problems without evidence in the supplied
  implementation.
- Recommendations must remain within complexity and implementation-quality
  analysis.
- Do not turn recommendations into a general optimization plan.
- Keep findings specific to the supplied engineering context.

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

Confidence:
{plan.confidence}

Engineering decision:

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

Proposed implementation changes:

{[
    {
        "path": change.path,
        "operation": change.operation,
        "content": change.content,
    }
    for change in proposed_changes
]}
""".strip()

    @staticmethod
    def _parse_response(
        response: str,
    ) -> EngineeringQualityAssessment:

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

        assessment_fields = {
            "complexity",
            "structural_complexity",
            "cognitive_complexity",
            "algorithmic_complexity",
            "dependency_complexity",
            "abstraction_complexity",
            "maintainability",
            "clarity",
            "cohesion",
            "coupling",
            "testability",
            "extensibility",
            "over_engineering",
            "issues",
            "strengths",
            "recommendations",
            "rationale",
        }

        if set(data) != assessment_fields:
            raise ValueError(
                "AI response contains an invalid schema"
            )

        string_fields = (
            "complexity",
            "structural_complexity",
            "cognitive_complexity",
            "algorithmic_complexity",
            "dependency_complexity",
            "abstraction_complexity",
            "maintainability",
            "clarity",
            "cohesion",
            "coupling",
            "testability",
            "extensibility",
        )

        for field in string_fields:

            if not isinstance(
                data[field],
                str,
            ):
                raise TypeError(
                    f"assessment {field} must be a string"
                )

            if not data[field].strip():
                raise ValueError(
                    f"assessment {field} must not be empty"
                )

        if not isinstance(
            data["over_engineering"],
            bool,
        ):
            raise TypeError(
                "assessment over_engineering must be a boolean"
            )

        list_fields = (
            "issues",
            "strengths",
            "recommendations",
            "rationale",
        )

        for field in list_fields:

            value = data[field]

            if not isinstance(
                value,
                list,
            ):
                raise TypeError(
                    f"assessment {field} must be a list"
                )

            if not all(
                isinstance(
                    item,
                    str,
                )
                for item in value
            ):
                raise TypeError(
                    f"assessment {field} must contain only strings"
                )

            if not all(
                item.strip()
                for item in value
            ):
                raise ValueError(
                    f"assessment {field} must not contain empty strings"
                )

        return EngineeringQualityAssessment(
            complexity=data["complexity"],
            structural_complexity=data[
                "structural_complexity"
            ],
            cognitive_complexity=data[
                "cognitive_complexity"
            ],
            algorithmic_complexity=data[
                "algorithmic_complexity"
            ],
            dependency_complexity=data[
                "dependency_complexity"
            ],
            abstraction_complexity=data[
                "abstraction_complexity"
            ],
            maintainability=data[
                "maintainability"
            ],
            clarity=data["clarity"],
            cohesion=data["cohesion"],
            coupling=data["coupling"],
            testability=data["testability"],
            extensibility=data["extensibility"],
            over_engineering=data[
                "over_engineering"
            ],
            issues=tuple(
                data["issues"]
            ),
            strengths=tuple(
                data["strengths"]
            ),
            recommendations=tuple(
                data["recommendations"]
            ),
            rationale=tuple(
                data["rationale"]
            ),
        )