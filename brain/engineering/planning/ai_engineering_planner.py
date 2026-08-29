import json

from brain.engineering.planning.models.plan import (
    EngineeringPlan,
)

from brain.engineering.planning.planner import (
    Planner,
)

from brain.engineering.tasks.models.task_decomposition import (
    TaskDecomposition,
)


class AIEngineeringPlanner(Planner):
    """
    Uses the AI runtime to create a structured engineering plan
    from an ordered task decomposition.
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

    def plan(
        self,
        decomposition: TaskDecomposition,
    ) -> EngineeringPlan:

        if not isinstance(
            decomposition,
            TaskDecomposition,
        ):
            raise TypeError(
                "decomposition must be a TaskDecomposition"
            )

        prompt = self._build_prompt(
            decomposition,
        )

        response = self._chat_service.chat(
            prompt,
        )

        return self._parse_response(
            decomposition,
            response,
        )

    @staticmethod
    def _build_prompt(
        decomposition: TaskDecomposition,
    ) -> str:

        tasks = []

        for task in decomposition.tasks:
            tasks.append({
                "id": task.id,
                "description": task.description,
                "category": task.category,
                "dependencies": sorted(
                    task.dependencies
                ),
                "affected_areas": sorted(
                    task.affected_areas
                ),
                "acceptance_criteria": sorted(
                    task.acceptance_criteria
                ),
            })

        return f"""
You are an engineering planning system.

Create a concrete engineering plan from the supplied task decomposition.

Return ONLY valid JSON.
Do not use markdown.
Do not include explanations outside the JSON.

The JSON must contain exactly these fields:

{{
  "task_order": ["task-id"],
  "strategy": ["string"],
  "milestones": ["string"],
  "required_capabilities": ["string"],
  "risks": ["string"],
  "assumptions": ["string"],
  "validation_strategy": ["string"],
  "confidence": 0.0
}}

Rules:

- Every task must appear exactly once in task_order.
- task_order must contain only task IDs from the supplied decomposition.
- Respect every task dependency.
- A dependency must appear before the task that depends on it.
- Do not invent tasks.
- Do not omit tasks.
- Strategy must describe how the supplied work should be executed.
- Milestones must represent meaningful completion points.
- Identify capabilities actually required by the supplied work.
- Do not invent technologies or capabilities without support from the tasks,
  requirements, constraints, or affected areas.
- Risks must represent plausible engineering risks.
- Assumptions must remain explicitly identified as assumptions.
- Do not convert assumptions into facts.
- validation_strategy must explain how completion will be verified.
- Do not use a fixed generic plan for every request.
- confidence must be a number between 0.0 and 1.0.

Task decomposition:

Requirement objective:
{decomposition.requirement.objective}

Tasks:
{json.dumps(tasks, indent=2)}

Requirement acceptance criteria:
{json.dumps(sorted(decomposition.requirement.acceptance_criteria), indent=2)}

Requirement constraints:
{json.dumps(sorted(decomposition.requirement.constraints), indent=2)}

Requirement assumptions:
{json.dumps(sorted(decomposition.requirement.assumptions), indent=2)}

Requirement ambiguities:
{json.dumps(sorted(decomposition.requirement.ambiguities), indent=2)}

Affected areas:
{json.dumps(sorted(decomposition.requirement.affected_areas), indent=2)}
""".strip()

    @classmethod
    def _parse_response(
        cls,
        decomposition: TaskDecomposition,
        response: str,
    ) -> EngineeringPlan:

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
            "task_order",
            "strategy",
            "milestones",
            "required_capabilities",
            "risks",
            "assumptions",
            "validation_strategy",
            "confidence",
        }

        if set(data) != required_fields:
            raise ValueError(
                "AI response contains an invalid schema"
            )

        list_fields = (
            "task_order",
            "strategy",
            "milestones",
            "required_capabilities",
            "risks",
            "assumptions",
            "validation_strategy",
        )

        for field in list_fields:

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

            if not all(
                item.strip()
                for item in data[field]
            ):
                raise ValueError(
                    f"{field} must not contain empty strings"
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

        cls._validate_task_order(
            decomposition,
            data["task_order"],
        )

        return EngineeringPlan(
            task_order=tuple(
                data["task_order"]
            ),
            strategy=tuple(
                data["strategy"]
            ),
            milestones=tuple(
                data["milestones"]
            ),
            required_capabilities=frozenset(
                data["required_capabilities"]
            ),
            risks=frozenset(
                data["risks"]
            ),
            assumptions=frozenset(
                data["assumptions"]
            ),
            validation_strategy=tuple(
                data["validation_strategy"]
            ),
            confidence=float(confidence),
        )

    @staticmethod
    def _validate_task_order(
        decomposition: TaskDecomposition,
        task_order: list[str],
    ) -> None:

        tasks = {
            task.id: task
            for task in decomposition.tasks
        }

        expected_ids = set(tasks)
        actual_ids = set(task_order)

        if len(task_order) != len(actual_ids):
            raise ValueError(
                "task_order must not contain duplicate task IDs"
            )

        if actual_ids != expected_ids:
            missing = expected_ids - actual_ids
            unknown = actual_ids - expected_ids

            if missing:
                raise ValueError(
                    "task_order is missing task IDs"
                )

            if unknown:
                raise ValueError(
                    "task_order contains unknown task IDs"
                )

        positions = {
            task_id: index
            for index, task_id in enumerate(task_order)
        }

        for task in decomposition.tasks:

            task_position = positions[task.id]

            for dependency in task.dependencies:

                dependency_position = positions[dependency]

                if dependency_position >= task_position:
                    raise ValueError(
                        "task_order violates task dependencies"
                    )