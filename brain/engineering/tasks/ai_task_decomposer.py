import json

from brain.engineering.requirements.models.requirement import (
    Requirement,
)

from brain.engineering.tasks.models.task import (
    Task,
)

from brain.engineering.tasks.models.task_decomposition import (
    TaskDecomposition,
)

from brain.engineering.tasks.task_decomposer import (
    TaskDecomposer,
)


class AITaskDecomposer(TaskDecomposer):
    """
    Uses the AI runtime to decompose structured requirements
    into ordered engineering tasks.
    """

    _CATEGORIES = frozenset({
        "analysis",
        "design",
        "implementation",
        "integration",
        "testing",
        "verification",
    })

    def __init__(
        self,
        chat_service,
    ):
        if not hasattr(chat_service, "chat"):
            raise TypeError(
                "chat_service must provide a chat method"
            )

        self._chat_service = chat_service

    def decompose(
        self,
        requirement: Requirement,
    ) -> TaskDecomposition:

        if not isinstance(
            requirement,
            Requirement,
        ):
            raise TypeError(
                "requirement must be a Requirement"
            )

        prompt = self._build_prompt(
            requirement,
        )

        response = self._chat_service.chat(
            prompt,
        )

        return self._parse_response(
            requirement,
            response,
        )

    @staticmethod
    def _build_prompt(
        requirement: Requirement,
    ) -> str:

        return f"""
You are an engineering task decomposition system.

Convert the structured engineering requirement below into
an ordered set of actionable engineering tasks.

Return ONLY valid JSON.
Do not use markdown.
Do not include explanations outside the JSON.

The JSON must contain exactly this field:

{{
  "tasks": [
    {{
      "id": "unique-task-id",
      "description": "string",
      "category": "analysis | design | implementation | integration | testing | verification",
      "dependencies": ["task-id"],
      "affected_areas": ["string"],
      "acceptance_criteria": ["string"]
    }}
  ]
}}

Rules:

- Decompose the actual requirement rather than inventing unrelated work.
- Every task must represent actionable engineering work.
- Every task description must clearly state an engineering action.
- Tasks must be ordered so that prerequisites occur before dependent tasks.
- Dependencies must reference task IDs in this response.
- Do not create circular dependencies.
- Do not create self-dependencies.
- Preserve relevant acceptance criteria from the requirement.
- Preserve relevant ambiguities from the requirement by creating appropriate
  tasks when resolving those ambiguities is necessary for implementation.
- Identify affected engineering areas only when supported.
- Do not assume technologies or implementation details that are not supported
  by the requirement.
- Do not use a fixed generic task sequence for every request.
- The number and nature of tasks must depend on the actual requirement.
- Do not return an empty task list.

Requirement:

Original request:
{requirement.original_request}

Objective:
{requirement.objective}

Functional requirements:
{sorted(requirement.functional_requirements)}

Non-functional requirements:
{sorted(requirement.non_functional_requirements)}

Constraints:
{sorted(requirement.constraints)}

Acceptance criteria:
{sorted(requirement.acceptance_criteria)}

Assumptions:
{sorted(requirement.assumptions)}

Ambiguities:
{sorted(requirement.ambiguities)}

Affected areas:
{sorted(requirement.affected_areas)}
""".strip()

    @classmethod
    def _parse_response(
        cls,
        requirement: Requirement,
        response: str,
    ) -> TaskDecomposition:

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

        if set(data) != {"tasks"}:
            raise ValueError(
                "AI response contains an invalid schema"
            )

        raw_tasks = data["tasks"]

        if not isinstance(raw_tasks, list):
            raise TypeError(
                "tasks must be a list"
            )

        if not raw_tasks:
            raise ValueError(
                "task decomposition must contain at least one task"
            )

        tasks = []

        for raw_task in raw_tasks:

            if not isinstance(raw_task, dict):
                raise TypeError(
                    "each task must be a JSON object"
                )

            required_fields = {
                "id",
                "description",
                "category",
                "dependencies",
                "affected_areas",
                "acceptance_criteria",
            }

            if set(raw_task) != required_fields:
                raise ValueError(
                    "task contains an invalid schema"
                )

            if not isinstance(
                raw_task["id"],
                str,
            ):
                raise TypeError(
                    "task id must be a string"
                )

            if not raw_task["id"].strip():
                raise ValueError(
                    "task id must not be empty"
                )

            if not isinstance(
                raw_task["description"],
                str,
            ):
                raise TypeError(
                    "task description must be a string"
                )

            description = raw_task["description"].strip()

            if not description:
                raise ValueError(
                    "task description must not be empty"
                )

            if not cls._is_actionable_description(
                description,
            ):
                raise ValueError(
                    "task description must represent actionable engineering work"
                )

            if raw_task["category"] not in cls._CATEGORIES:
                raise ValueError(
                    "task category is invalid"
                )

            for field in (
                "dependencies",
                "affected_areas",
                "acceptance_criteria",
            ):
                if not isinstance(
                    raw_task[field],
                    list,
                ):
                    raise TypeError(
                        f"{field} must be a list"
                    )

                if not all(
                    isinstance(item, str)
                    for item in raw_task[field]
                ):
                    raise TypeError(
                        f"{field} must contain only strings"
                    )

            tasks.append(
                Task(
                    id=raw_task["id"],
                    description=description,
                    category=raw_task["category"],
                    dependencies=frozenset(
                        raw_task["dependencies"]
                    ),
                    affected_areas=frozenset(
                        raw_task["affected_areas"]
                    ),
                    acceptance_criteria=frozenset(
                        raw_task["acceptance_criteria"]
                    ),
                )
            )

        cls._validate_tasks(
            tasks,
        )

        return TaskDecomposition(
            requirement=requirement,
            tasks=tuple(tasks),
        )

    @staticmethod
    def _is_actionable_description(
        description: str,
    ) -> bool:
        """
        Performs structural validation that a task description
        contains meaningful content rather than a placeholder.

        This deliberately avoids a hardcoded blacklist of words.
        """

        words = description.split()

        if len(words) < 2:
            return False

        return any(
            character.isalpha()
            for character in description
        )

    @staticmethod
    def _validate_tasks(
        tasks: list[Task],
    ) -> None:

        if not tasks:
            raise ValueError(
                "task decomposition must contain at least one task"
            )

        task_ids = [task.id for task in tasks]

        if len(task_ids) != len(set(task_ids)):
            raise ValueError(
                "task IDs must be unique"
            )

        descriptions = [
            task.description.strip().casefold()
            for task in tasks
        ]

        if len(descriptions) != len(set(descriptions)):
            raise ValueError(
                "task descriptions must be unique"
            )

        task_id_set = set(task_ids)

        for task in tasks:

            if task.id in task.dependencies:
                raise ValueError(
                    "task cannot depend on itself"
                )

            unknown_dependencies = (
                task.dependencies - task_id_set
            )

            if unknown_dependencies:
                raise ValueError(
                    "task contains unknown dependencies"
                )

        # Verify dependency graph is acyclic.
        visiting: set[str] = set()
        visited: set[str] = set()

        dependencies = {
            task.id: task.dependencies
            for task in tasks
        }

        def visit(task_id: str) -> None:

            if task_id in visiting:
                raise ValueError(
                    "task dependencies contain a cycle"
                )

            if task_id in visited:
                return

            visiting.add(task_id)

            for dependency in dependencies[task_id]:
                visit(dependency)

            visiting.remove(task_id)
            visited.add(task_id)

        for task_id in task_ids:
            visit(task_id)