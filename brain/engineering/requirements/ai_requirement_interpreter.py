import json

from brain.engineering.requirements.models.requirement import (
    Requirement,
)

from brain.engineering.requirements.requirement_interpreter import (
    RequirementInterpreter,
)


class AIRequirementInterpreter(
    RequirementInterpreter,
):
    """
    Uses the AI runtime to interpret engineering requests
    into structured requirements.
    """

    def __init__(
        self,
        chat_service,
    ):
        if not hasattr(chat_service, "chat"):
            raise TypeError(
                "chat_service must provide a chat method"
            )

        self._chat_service = chat_service

    def interpret(
        self,
        request: str,
    ) -> Requirement:

        if not isinstance(request, str):
            raise TypeError(
                "request must be a string"
            )

        request = request.strip()

        if not request:
            raise ValueError(
                "request must not be empty"
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
        request: str,
    ) -> str:

        return f"""
You are an engineering requirements analyst.

Analyze the following engineering request.

Return ONLY valid JSON.
Do not use markdown.
Do not include explanations outside the JSON.

The JSON must contain exactly these fields:

{{
  "objective": "string",
  "functional_requirements": ["string"],
  "non_functional_requirements": ["string"],
  "constraints": ["string"],
  "acceptance_criteria": ["string"],
  "assumptions": ["string"],
  "ambiguities": ["string"],
  "affected_areas": ["string"],
  "confidence": 0.0
}}

Rules:

- Preserve the user's actual intent.
- Do not invent requirements that are not supported by the request.
- Put uncertainty into assumptions or ambiguities.
- Do not treat assumptions as facts.
- Identify affected engineering areas only when reasonably supported.
- confidence must be a number between 0.0 and 1.0.

Engineering request:

{request}
""".strip()

    @staticmethod
    def _parse_response(
        request: str,
        response: str,
    ) -> Requirement:

        if not isinstance(response, str):
            raise TypeError(
                "AI response must be a string"
            )

        try:
            data = json.loads(response)

        except json.JSONDecodeError as e:
            raise ValueError(
                "AI response must contain valid JSON"
            ) from e

        if not isinstance(data, dict):
            raise ValueError(
                "AI response must be a JSON object"
            )

        required_fields = {
            "objective",
            "functional_requirements",
            "non_functional_requirements",
            "constraints",
            "acceptance_criteria",
            "assumptions",
            "ambiguities",
            "affected_areas",
            "confidence",
        }

        if set(data) != required_fields:
            raise ValueError(
                "AI response contains an invalid schema"
            )

        if not isinstance(
            data["objective"],
            str,
        ):
            raise TypeError(
                "objective must be a string"
            )

        for field in (
            "functional_requirements",
            "non_functional_requirements",
            "constraints",
            "acceptance_criteria",
            "assumptions",
            "ambiguities",
            "affected_areas",
        ):
            if not isinstance(
                data[field],
                list,
            ):
                raise TypeError(
                    f"{field} must be a list"
                )

            if not all(
                isinstance(item, str)
                for item in data[field]
            ):
                raise TypeError(
                    f"{field} must contain only strings"
                )

        confidence = data["confidence"]

        if (
            isinstance(confidence, bool)
            or not isinstance(
                confidence,
                (int, float),
            )
        ):
            raise TypeError(
                "confidence must be a number"
            )

        if not 0.0 <= confidence <= 1.0:
            raise ValueError(
                "confidence must be between 0.0 and 1.0"
            )

        return Requirement(
            original_request=request,
            objective=data["objective"],
            functional_requirements=frozenset(
                data["functional_requirements"]
            ),
            non_functional_requirements=frozenset(
                data["non_functional_requirements"]
            ),
            constraints=frozenset(
                data["constraints"]
            ),
            acceptance_criteria=frozenset(
                data["acceptance_criteria"]
            ),
            assumptions=frozenset(
                data["assumptions"]
            ),
            ambiguities=frozenset(
                data["ambiguities"]
            ),
            affected_areas=frozenset(
                data["affected_areas"]
            ),
            confidence=float(confidence),
        )