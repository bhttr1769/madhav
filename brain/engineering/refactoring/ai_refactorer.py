from brain.engineering.refactoring.refactoring_response_parser import (
    RefactoringResponseParser,
)
from brain.engineering.refactoring.models.refactoring_request import (
    RefactoringRequest,
)
from brain.engineering.refactoring.models.refactoring_result import (
    RefactoringResult,
)


class AIRefactorer:
    def __init__(self, chat_service):
        if not hasattr(chat_service, "chat"):
            raise TypeError(
                "chat_service must provide a chat method"
            )

        self._chat_service = chat_service

    def refactor(
        self,
        request: RefactoringRequest,
    ) -> RefactoringResult:
        if not isinstance(request, RefactoringRequest):
            raise TypeError(
                "request must be a RefactoringRequest"
            )

        prompt = self._build_prompt(request)
        response = self._chat_service.chat(prompt)

        return RefactoringResponseParser.parse(response)

    @staticmethod
    def _build_prompt(
        request: RefactoringRequest,
    ) -> str:
        return f"""
You are a senior software engineer performing
a rigorous code refactoring assessment.

Your task is to identify justified improvements to the
implementation while preserving its intended behavior.

Do not change externally observable behavior.
Do not fix unrelated bugs.
Do not introduce unnecessary abstractions.
Do not optimize unless the improvement is justified.
Do not make stylistic changes without a meaningful
maintainability or engineering benefit.

Engineering task:
{request.task}

System design:
{request.design}

Engineering plan:
{request.plan}

Existing code structure:
{request.existing_code}

Previously proposed changes:
{request.proposed_changes}

Analyze the implementation in the context of the task,
design, plan, existing code, and proposed changes.

Identify only concrete refactorings that provide a meaningful
engineering benefit while preserving intended behavior.

If no refactoring is justified, return an empty changes list.

Return ONLY valid JSON in exactly this format:

{{
  "changes": [
    {{
      "path": "relative/path/to/file.py",
      "operation": "create|modify|delete",
      "content": "complete file content for the change"
    }}
  ],
  "rationale": "concise explanation of why the refactoring is justified"
}}

Rules:
- "changes" must be a JSON array.
- Each change must contain exactly "path", "operation", and "content".
- "operation" must be one of: create, modify, delete.
- Paths must be relative and must not contain "..".
- Create and modify operations must contain non-empty content.
- Delete operations must use an empty content string.
- Preserve intended behavior.
- Do not include tests unless they are necessary to preserve
  or demonstrate existing behavior.
- Do not include markdown fences.
- Do not include any text outside the JSON object.
- Keep the rationale focused on the actual refactoring.
""".strip()