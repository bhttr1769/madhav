from brain.engineering.review.code_reviewer import CodeReviewer
from brain.engineering.review.code_review_response_parser import (
    CodeReviewResponseParser,
)
from brain.engineering.review.models.code_review_request import (
    CodeReviewRequest,
)
from brain.engineering.review.models.code_review_result import (
    CodeReviewResult,
)


class AICodeReviewer(CodeReviewer):
    """
    Uses the AI runtime to review proposed implementation changes.
    """

    def __init__(self, chat_service):
        if not hasattr(chat_service, "chat"):
            raise TypeError("chat_service must provide a chat method")

        self._chat_service = chat_service

    def review(
        self,
        request: CodeReviewRequest,
    ) -> CodeReviewResult:
        if not isinstance(request, CodeReviewRequest):
            raise TypeError(
                "request must be a CodeReviewRequest"
            )

        prompt = self._build_prompt(request)
        response = self._chat_service.chat(prompt)

        return CodeReviewResponseParser.parse(response)

    @staticmethod
    def _build_prompt(
        request: CodeReviewRequest,
    ) -> str:
        task = request.task
        design = request.design
        plan = request.plan
        existing_code = request.existing_code
        proposed_changes = request.proposed_changes

        return f"""
You are a senior software engineer performing a rigorous code review.

Review the supplied proposed implementation against the engineering task,
system design, engineering plan, existing code structure, and acceptance
criteria.

Identify concrete problems that could affect correctness, security,
performance, maintainability, design, testing, or code quality.

Do not modify the implementation.
Do not generate replacement code.
Do not invent unrelated concerns.

Return ONLY valid JSON.
Do not use markdown.
Do not include explanations outside the JSON.

The JSON must contain exactly these fields:

{{
  "approved": true,
  "findings": [
    {{
      "severity": "medium",
      "category": "correctness",
      "path": "brain/example.py",
      "message": "Description of the problem.",
      "recommendation": "Recommended corrective action."
    }}
  ],
  "summary": "Concise overall review summary."
}}

Rules:
- Review only the supplied task and proposed implementation.
- Treat the supplied task acceptance criteria as authoritative.
- Evaluate the implementation against the supplied system design.
- Evaluate the implementation against the supplied engineering plan.
- Consider the existing code structure when identifying integration problems.
- Identify concrete, actionable findings.
- Do not report purely hypothetical problems without evidence in the
  supplied context.
- Do not report stylistic preferences as correctness problems.
- Use severity only from: critical, high, medium, low.
- Use category only from: correctness, security, performance,
  maintainability, design, testing, style.
- Each finding must identify the affected file path.
- Paths must be relative to the project root.
- Do not use parent traversal in paths.
- The recommendation must explain what should be changed or investigated.
- Set approved to true only when the proposed implementation is acceptable
  for the supplied task and no finding requires correction.
- Set approved to false when one or more findings require correction.
- Return an empty findings list when no findings exist.
- Do not return any field other than approved, findings, and summary.

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
        "name": function_model.name,
        "module": function_model.module,
    }
    for function_model in existing_code.functions
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