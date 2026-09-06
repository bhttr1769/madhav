from brain.engineering.debugging.debugging_response_parser import (
    DebuggingResponseParser,
)
from brain.engineering.debugging.models.debugging_request import (
    DebuggingRequest,
)
from brain.engineering.debugging.models.debugging_result import (
    DebuggingResult,
)


class AIDebugger:
    def __init__(self, chat_service):
        if not hasattr(chat_service, "chat"):
            raise TypeError(
                "chat_service must provide a chat method"
            )

        self._chat_service = chat_service

    def debug(
        self,
        request: DebuggingRequest,
    ) -> DebuggingResult:
        if not isinstance(request, DebuggingRequest):
            raise TypeError(
                "request must be a DebuggingRequest"
            )

        prompt = self._build_prompt(request)
        response = self._chat_service.chat(prompt)

        return DebuggingResponseParser.parse(response)

    @staticmethod
    def _build_prompt(
        request: DebuggingRequest,
    ) -> str:
        return f"""
You are a senior software engineer performing
a rigorous debugging investigation.

Your task is to diagnose the reported failure and
produce the minimal code changes required to resolve it.

Do not guess beyond the available evidence.
Do not introduce unrelated improvements.
Do not redesign working parts of the system.

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

Error message:
{request.error_message}

Traceback:
{request.traceback}

Analyze the failure in the context of the task,
design, plan, existing code, and proposed changes.

Determine the most likely root cause from the available
evidence and make only the changes necessary to resolve it.

Return ONLY valid JSON in exactly this format:

{{
  "changes": [
    {{
      "path": "relative/path/to/file.py",
      "operation": "create|modify|delete",
      "content": "complete file content for the change"
    }}
  ],
  "diagnosis": "concise explanation of the root cause and fix"
}}

Rules:
- "changes" must be a JSON array.
- Each change must contain exactly "path", "operation", and "content".
- "operation" must be one of: create, modify, delete.
- Paths must be relative and must not contain "..".
- Create and modify operations must contain non-empty content.
- Delete operations must use an empty content string.
- Do not include markdown fences.
- Do not include any text outside the JSON object.
- Keep the diagnosis focused on the actual failure.
""".strip()