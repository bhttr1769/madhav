from brain.engineering.improvement.improvement_response_parser import (
    ImprovementResponseParser,
)
from brain.engineering.improvement.models.engineering_improvement_request import (
    EngineeringImprovementRequest,
)
from brain.engineering.improvement.models.engineering_improvement_result import (
    EngineeringImprovementResult,
)


class AIEngineeringImprover:
    def __init__(self, chat_service):
        if not hasattr(chat_service, "chat"):
            raise TypeError(
                "chat_service must provide a chat method"
            )

        self._chat_service = chat_service

    def improve(
        self,
        request: EngineeringImprovementRequest,
    ) -> EngineeringImprovementResult:
        if not isinstance(
            request,
            EngineeringImprovementRequest,
        ):
            raise TypeError(
                "request must be an EngineeringImprovementRequest"
            )

        prompt = self._build_prompt(request)
        response = self._chat_service.chat(prompt)

        return ImprovementResponseParser.parse(
            response
        )

    @staticmethod
    def _build_prompt(
        request: EngineeringImprovementRequest,
    ) -> str:
        return f"""
You are a senior software engineer performing an
integrated engineering improvement assessment.

Your task is to identify justified improvements to the
implementation using the complete engineering context.

Consider:
- correctness
- maintainability
- design quality
- testing
- performance
- unnecessary complexity
- unnecessary duplication
- inappropriate abstractions
- consistency with the engineering plan

Preserve the intended behavior of the system.

Do not blindly refactor.
Do not introduce speculative improvements.
Do not fix unrelated problems.
Do not optimize without a concrete engineering reason.
Do not change behavior merely to satisfy stylistic preferences.

Engineering task:
{request.task}

System design:
{request.design}

Engineering plan:
{request.plan}

Existing code structure:
{request.existing_code}

Proposed changes:
{request.proposed_changes}

Determine whether the proposed implementation can be
meaningfully improved.

If improvements are justified, produce only the concrete
code changes required to implement them.

If no meaningful improvement is justified, return an empty
changes list.

Return ONLY valid JSON in exactly this format:

{{
  "changes": [
    {{
      "path": "relative/path/to/file.py",
      "operation": "create|modify|delete",
      "content": "complete file content for the change"
    }}
  ],
  "rationale": [
    "concise reason for the first improvement",
    "concise reason for the second improvement"
  ]
}}

Rules:
- "changes" must be a JSON array.
- Each change must contain exactly "path", "operation", and "content".
- "operation" must be one of: create, modify, delete.
- Paths must be relative and must not contain "..".
- Create and modify operations must contain non-empty content.
- Delete operations must use an empty content string.
- Preserve intended behavior.
- Every change must have a concrete engineering justification.
- Do not include unrelated changes.
- Do not include markdown fences.
- Do not include any text outside the JSON object.
""".strip()