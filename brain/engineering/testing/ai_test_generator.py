from brain.engineering.generation.models.code_change import CodeChange
from brain.engineering.testing.models.test_generation_request import (
    TestGenerationRequest,
)
from brain.engineering.testing.models.test_generation_result import (
    TestGenerationResult,
)
from brain.engineering.testing.test_generation_response_parser import (
    TestGenerationResponseParser,
)
from brain.engineering.testing.test_generator import TestGenerator


class AITestGenerator(TestGenerator):
    """
    Uses the AI runtime to generate tests for a proposed implementation.
    """

    def __init__(self, chat_service):
        if not hasattr(chat_service, "chat"):
            raise TypeError("chat_service must provide a chat method")

        self._chat_service = chat_service

    def generate(
        self,
        request: TestGenerationRequest,
    ) -> TestGenerationResult:
        if not isinstance(request, TestGenerationRequest):
            raise TypeError(
                "request must be a TestGenerationRequest"
            )

        prompt = self._build_prompt(request)
        response = self._chat_service.chat(prompt)

        return TestGenerationResponseParser.parse(response)

    @staticmethod
    def _build_prompt(
        request: TestGenerationRequest,
    ) -> str:
        task = request.task
        design = request.design
        plan = request.plan
        existing_code = request.existing_code
        proposed_changes = request.proposed_changes

        return f"""
You are a senior software engineer responsible for test engineering.

Generate test changes for the supplied engineering task and proposed
implementation.

The tests must validate the proposed implementation against the supplied
task, system design, engineering plan, existing code structure, and
acceptance criteria.

Generate only the tests necessary to validate the proposed implementation.

Return ONLY valid JSON.
Do not use markdown.
Do not include explanations outside the JSON.

The JSON must contain exactly this field:

{{
  "changes": [
    {{
      "path": "tests/test_example.py",
      "operation": "create",
      "content": "complete file content"
    }}
  ]
}}

Rules:
- Generate tests only for the supplied task and proposed implementation.
- Do not modify production implementation files unless the task explicitly
  requires test-related changes to them.
- Prefer adding or modifying test files.
- Test the supplied acceptance criteria.
- Test important functional behavior.
- Test relevant error and boundary conditions when they are implied by the
  task or implementation.
- Reuse the existing project's testing conventions and structure.
- Inspect the supplied existing code structure before creating test files.
- Do not duplicate tests that already exist when existing tests can be
  extended or reused.
- Do not invent unrelated behavior.
- Do not introduce a new testing dependency unless the supplied engineering
  context establishes that it is available or required.
- Each change must identify a concrete file path.
- operation must be one of: create, modify, delete.
- content must contain the implementation associated with the operation.
- For create and modify operations, content must not be empty.
- For delete operations, content may be empty.
- Return an empty changes list if no test changes are necessary.
- Do not return any field other than changes.

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