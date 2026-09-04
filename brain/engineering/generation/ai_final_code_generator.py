from brain.engineering.generation.final_code_generator import (
    FinalCodeGenerator,
)

from brain.engineering.generation.generation_response_parser import (
    GenerationResponseParser,
)

from brain.engineering.generation.models.final_generation_request import (
    FinalGenerationRequest,
)

from brain.engineering.generation.models.generation_result import (
    GenerationResult,
)


class AIFinalCodeGenerator(
    FinalCodeGenerator,
):
    """
    Uses the AI runtime to generate the final implementation after
    engineering analysis and optimization decisions have been made.
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

    def generate(
        self,
        request: FinalGenerationRequest,
    ) -> GenerationResult:

        if not isinstance(
            request,
            FinalGenerationRequest,
        ):
            raise TypeError(
                "request must be a FinalGenerationRequest"
            )

        prompt = self._build_prompt(
            request,
        )

        response = self._chat_service.chat(
            prompt,
        )

        return GenerationResponseParser.parse(
            response,
        )

    @staticmethod
    def _build_prompt(
        request: FinalGenerationRequest,
    ) -> str:

        task = request.task
        design = request.design
        plan = request.plan

        engineering_decision = (
            request.engineering_decision
        )

        quality_assessment = (
            request.quality_assessment
        )

        optimization_decision = (
            request.optimization_decision
        )

        existing_code = request.existing_code
        proposed_changes = request.proposed_changes

        return f"""
You are Madhav's senior software engineering implementation agent.

Generate the FINAL implementation for the supplied engineering task.

A candidate implementation has already been generated and independently
analyzed for necessity, reuse, complexity, implementation quality, and
optimization.

Your responsibility is to revise or preserve that candidate implementation
so that the final implementation satisfies the engineering task while
respecting all supplied engineering decisions.

Do not blindly optimize the implementation.

Do not introduce changes that are unsupported by the supplied engineering
context.

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

FINAL IMPLEMENTATION RULES

- Implement only the supplied task.
- Follow the supplied system design.
- Follow the supplied engineering plan.
- Preserve correct existing behavior.
- Reuse existing capabilities where the engineering decision requires reuse.
- Do not introduce unnecessary abstractions.
- Do not introduce unnecessary dependencies.
- Prefer the standard library when appropriate.
- Apply optimization only when the optimization decision justifies it.
- Respect the stated optimization objective and scope.
- Do not perform speculative optimization.
- Do not sacrifice correctness for optimization.
- Do not sacrifice maintainability for insignificant optimization gains.
- Do not implement optimization strategies that were explicitly identified
  as strategies to avoid.
- If measurement is required, do not claim that an optimization has been
  proven effective.
- Do not invent benchmark results.
- Do not invent performance measurements.
- Do not modify files unrelated to the task.
- Each change must identify a concrete file path.
- operation must be one of: create, modify, delete.
- content must contain the implementation associated with the operation.
- Do not assume a specific programming language unless the engineering
  context establishes one.
- The final implementation must remain consistent with the existing code
  structure.

ENGINEERING TASK

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

SYSTEM DESIGN

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

ENGINEERING PLAN

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

EXISTING CODE STRUCTURE

{existing_code!r}

NECESSITY AND REUSE DECISION

{engineering_decision!r}

COMPLEXITY AND IMPLEMENTATION-QUALITY ASSESSMENT

{quality_assessment!r}

OPTIMIZATION DECISION

{optimization_decision!r}

CANDIDATE IMPLEMENTATION

{proposed_changes!r}

FINAL ENGINEERING REQUIREMENT

The supplied engineering decisions are authoritative inputs to this
implementation pass.

The necessity/reuse decision determines whether the implementation should
exist and what existing capabilities should be reused.

The complexity/quality assessment identifies implementation weaknesses,
risks, and maintainability concerns that should be addressed when justified.

The optimization decision determines whether optimization is justified and,
if so, the appropriate optimization direction.

Use engineering judgment when these inputs interact. Do not mechanically
apply every recommendation if doing so would violate correctness,
architecture, maintainability, or the task requirements.

Generate the smallest complete final implementation that satisfies the task
and the justified engineering decisions.
""".strip()