import json

import pytest

from brain.engineering.requirements.models.requirement import (
    Requirement,
)

from brain.engineering.tasks.ai_task_decomposer import (
    AITaskDecomposer,
)


class FakeChatService:

    def __init__(
        self,
        response: str,
    ):
        self._response = response
        self.prompts = []

    def chat(
        self,
        prompt: str,
    ) -> str:

        self.prompts.append(prompt)

        return self._response


def requirement():

    return Requirement(
        original_request="Build an API",
        objective="Build an API",
        functional_requirements=frozenset({
            "The API must expose endpoints",
        }),
        non_functional_requirements=frozenset({
            "The API must be reliable",
        }),
        constraints=frozenset({
            "Use the existing backend",
        }),
        acceptance_criteria=frozenset({
            "The API responds successfully",
        }),
        assumptions=frozenset(),
        ambiguities=frozenset(),
        affected_areas=frozenset({
            "backend",
        }),
        confidence=0.95,
    )


def valid_response():

    return json.dumps({
        "tasks": [
            {
                "id": "task-1",
                "description": "Inspect the existing backend",
                "category": "analysis",
                "dependencies": [],
                "affected_areas": ["backend"],
                "acceptance_criteria": [],
            },
            {
                "id": "task-2",
                "description": "Implement the API",
                "category": "implementation",
                "dependencies": ["task-1"],
                "affected_areas": ["backend"],
                "acceptance_criteria": [
                    "The API responds successfully",
                ],
            },
        ],
    })


def test_decomposer_rejects_invalid_requirement_type():

    chat_service = FakeChatService(
        valid_response()
    )

    decomposer = AITaskDecomposer(
        chat_service
    )

    with pytest.raises(TypeError):
        decomposer.decompose(
            "Build an API"
        )


def test_decomposer_returns_task_decomposition():

    chat_service = FakeChatService(
        valid_response()
    )

    decomposer = AITaskDecomposer(
        chat_service
    )

    result = decomposer.decompose(
        requirement()
    )

    assert len(result.tasks) == 2

    assert result.tasks[0].id == "task-1"
    assert result.tasks[1].id == "task-2"

    assert result.tasks[1].dependencies == frozenset({
        "task-1",
    })


def test_decomposer_preserves_requirement():

    chat_service = FakeChatService(
        valid_response()
    )

    decomposer = AITaskDecomposer(
        chat_service
    )

    req = requirement()

    result = decomposer.decompose(
        req
    )

    assert result.requirement == req


def test_decomposer_builds_prompt_from_requirement():

    chat_service = FakeChatService(
        valid_response()
    )

    decomposer = AITaskDecomposer(
        chat_service
    )

    req = requirement()

    decomposer.decompose(
        req
    )

    assert len(chat_service.prompts) == 1

    prompt = chat_service.prompts[0]

    assert req.objective in prompt
    assert "The API must expose endpoints" in prompt
    assert "The API responds successfully" in prompt
    assert "backend" in prompt

def run_with_response(
    response,
    req=None,
):

    chat_service = FakeChatService(
        response
    )

    decomposer = AITaskDecomposer(
        chat_service
    )

    if req is None:
        req = requirement()

    return decomposer.decompose(
        req
    )

def test_decomposer_rejects_invalid_json():

    with pytest.raises(ValueError):
        run_with_response(
            "not valid json"
        )


def test_decomposer_rejects_non_object_json():

    with pytest.raises(ValueError):
        run_with_response(
            json.dumps([])
        )


def test_decomposer_rejects_missing_tasks_field():

    with pytest.raises(ValueError):
        run_with_response(
            json.dumps({})
        )


def test_decomposer_rejects_unexpected_top_level_field():

    with pytest.raises(ValueError):
        run_with_response(
            json.dumps({
                "tasks": [],
                "extra": "invalid",
            })
        )


def test_decomposer_rejects_tasks_that_are_not_a_list():

    with pytest.raises(TypeError):
        run_with_response(
            json.dumps({
                "tasks": {},
            })
        )


def test_decomposer_rejects_non_object_task():

    with pytest.raises(TypeError):
        run_with_response(
            json.dumps({
                "tasks": [
                    "invalid task",
                ],
            })
        )


def test_decomposer_rejects_missing_task_field():

    response = {
        "tasks": [
            {
                "id": "task-1",
                "description": "Inspect backend",
                "category": "analysis",
                "dependencies": [],
                "affected_areas": [],
            },
        ],
    }

    with pytest.raises(ValueError):
        run_with_response(
            json.dumps(response)
        )


def test_decomposer_rejects_unexpected_task_field():

    response = json.loads(
        valid_response()
    )

    response["tasks"][0]["extra"] = "invalid"

    with pytest.raises(ValueError):
        run_with_response(
            json.dumps(response)
        )


def test_decomposer_rejects_non_string_task_id():

    response = json.loads(
        valid_response()
    )

    response["tasks"][0]["id"] = 123

    with pytest.raises(TypeError):
        run_with_response(
            json.dumps(response)
        )


def test_decomposer_rejects_empty_task_id():

    response = json.loads(
        valid_response()
    )

    response["tasks"][0]["id"] = "   "

    with pytest.raises(ValueError):
        run_with_response(
            json.dumps(response)
        )


def test_decomposer_rejects_non_string_description():

    response = json.loads(
        valid_response()
    )

    response["tasks"][0]["description"] = 123

    with pytest.raises(TypeError):
        run_with_response(
            json.dumps(response)
        )


def test_decomposer_rejects_empty_description():

    response = json.loads(
        valid_response()
    )

    response["tasks"][0]["description"] = ""

    with pytest.raises(ValueError):
        run_with_response(
            json.dumps(response)
        )


def test_decomposer_rejects_invalid_category():

    response = json.loads(
        valid_response()
    )

    response["tasks"][0]["category"] = "deployment"

    with pytest.raises(ValueError):
        run_with_response(
            json.dumps(response)
        )


def test_decomposer_rejects_non_list_dependencies():

    response = json.loads(
        valid_response()
    )

    response["tasks"][0]["dependencies"] = "task-2"

    with pytest.raises(TypeError):
        run_with_response(
            json.dumps(response)
        )


def test_decomposer_rejects_non_string_dependencies():

    response = json.loads(
        valid_response()
    )

    response["tasks"][0]["dependencies"] = [123]

    with pytest.raises(TypeError):
        run_with_response(
            json.dumps(response)
        )


def test_decomposer_rejects_non_list_affected_areas():

    response = json.loads(
        valid_response()
    )

    response["tasks"][0]["affected_areas"] = "backend"

    with pytest.raises(TypeError):
        run_with_response(
            json.dumps(response)
        )


def test_decomposer_rejects_non_string_affected_areas():

    response = json.loads(
        valid_response()
    )

    response["tasks"][0]["affected_areas"] = [123]

    with pytest.raises(TypeError):
        run_with_response(
            json.dumps(response)
        )


def test_decomposer_rejects_non_list_acceptance_criteria():

    response = json.loads(
        valid_response()
    )

    response["tasks"][0]["acceptance_criteria"] = (
        "criterion"
    )

    with pytest.raises(TypeError):
        run_with_response(
            json.dumps(response)
        )


def test_decomposer_rejects_non_string_acceptance_criteria():

    response = json.loads(
        valid_response()
    )

    response["tasks"][0]["acceptance_criteria"] = [123]

    with pytest.raises(TypeError):
        run_with_response(
            json.dumps(response)
        )


def test_decomposer_rejects_duplicate_task_ids():

    response = json.loads(
        valid_response()
    )

    response["tasks"][1]["id"] = "task-1"

    with pytest.raises(ValueError):
        run_with_response(
            json.dumps(response)
        )


def test_decomposer_rejects_unknown_dependency():

    response = json.loads(
        valid_response()
    )

    response["tasks"][1]["dependencies"] = [
        "does-not-exist",
    ]

    with pytest.raises(ValueError):
        run_with_response(
            json.dumps(response)
        )


def test_decomposer_rejects_self_dependency():

    response = json.loads(
        valid_response()
    )

    response["tasks"][0]["dependencies"] = [
        "task-1",
    ]

    with pytest.raises(ValueError):
        run_with_response(
            json.dumps(response)
        )


def test_decomposer_rejects_circular_dependencies():

    response = json.loads(
        valid_response()
    )

    response["tasks"][0]["dependencies"] = [
        "task-2",
    ]

    response["tasks"][1]["dependencies"] = [
        "task-1",
    ]

    with pytest.raises(ValueError):
        run_with_response(
            json.dumps(response)
        )


def test_decomposer_accepts_multiple_dependency_levels():

    response = {
        "tasks": [
            {
                "id": "task-1",
                "description": "Inspect system",
                "category": "analysis",
                "dependencies": [],
                "affected_areas": [],
                "acceptance_criteria": [],
            },
            {
                "id": "task-2",
                "description": "Design solution",
                "category": "design",
                "dependencies": ["task-1"],
                "affected_areas": [],
                "acceptance_criteria": [],
            },
            {
                "id": "task-3",
                "description": "Implement solution",
                "category": "implementation",
                "dependencies": ["task-2"],
                "affected_areas": [],
                "acceptance_criteria": [],
            },
            {
                "id": "task-4",
                "description": "Test solution",
                "category": "testing",
                "dependencies": ["task-3"],
                "affected_areas": [],
                "acceptance_criteria": [],
            },
        ],
    }

    result = run_with_response(
        json.dumps(response)
    )

    assert [
        task.id
        for task in result.tasks
    ] == [
        "task-1",
        "task-2",
        "task-3",
        "task-4",
    ]


def test_decomposer_preserves_acceptance_criteria():

    result = run_with_response(
        valid_response()
    )

    assert (
        "The API responds successfully"
        in result.tasks[1].acceptance_criteria
    )

def test_decomposition_contains_at_least_one_task():

    result = run_with_response(
        valid_response()
    )

    assert len(result.tasks) > 0


def test_decomposition_preserves_requirement_objective():

    result = run_with_response(
        valid_response()
    )

    assert result.requirement.objective == (
        requirement().objective
    )


def test_decomposition_preserves_functional_requirement_coverage():

    req = requirement()

    response = json.loads(
        valid_response()
    )

    functional_requirement = next(
        iter(req.functional_requirements)
    )

    response["tasks"][0]["acceptance_criteria"] = [
        functional_requirement
    ]

    result = run_with_response(
        json.dumps(response)
    )

    covered = {
        criterion
        for task in result.tasks
        for criterion in task.acceptance_criteria
    }

    assert functional_requirement in covered


def test_decomposition_preserves_non_functional_requirement_coverage():

    req = requirement()

    response = json.loads(
        valid_response()
    )

    non_functional = next(
        iter(req.non_functional_requirements)
    )

    response["tasks"][0]["acceptance_criteria"] = [
        non_functional
    ]

    result = run_with_response(
        json.dumps(response)
    )

    covered = {
        criterion
        for task in result.tasks
        for criterion in task.acceptance_criteria
    }

    assert non_functional in covered


def test_decomposition_preserves_constraints():

    req = requirement()

    response = json.loads(
        valid_response()
    )

    constraint = next(
        iter(req.constraints)
    )

    response["tasks"][0]["affected_areas"] = [
        constraint
    ]

    result = run_with_response(
        json.dumps(response)
    )

    assert constraint in (
        result.tasks[0].affected_areas
    )


def test_decomposition_preserves_ambiguities():

    req = Requirement(
        original_request="Build an API",
        objective="Build an API",
        functional_requirements=frozenset({
            "Provide API endpoints",
        }),
        non_functional_requirements=frozenset(),
        constraints=frozenset(),
        acceptance_criteria=frozenset(),
        assumptions=frozenset(),
        ambiguities=frozenset({
            "Authentication method is unspecified",
        }),
        affected_areas=frozenset({
            "backend",
        }),
        confidence=0.8,
    )

    response = json.loads(
        valid_response()
    )

    ambiguity = next(
        iter(req.ambiguities)
    )

    response["tasks"][0]["description"] = (
        f"Resolve ambiguity: {ambiguity}"
    )

    result = run_with_response(
        json.dumps(response),
        req,
    )

    assert ambiguity in (
        result.tasks[0].description
    )


def test_tasks_are_returned_in_dependency_order():

    response = {
        "tasks": [
            {
                "id": "task-1",
                "description": "Inspect system",
                "category": "analysis",
                "dependencies": [],
                "affected_areas": [],
                "acceptance_criteria": [],
            },
            {
                "id": "task-2",
                "description": "Design solution",
                "category": "design",
                "dependencies": ["task-1"],
                "affected_areas": [],
                "acceptance_criteria": [],
            },
            {
                "id": "task-3",
                "description": "Implement solution",
                "category": "implementation",
                "dependencies": ["task-2"],
                "affected_areas": [],
                "acceptance_criteria": [],
            },
        ],
    }

    result = run_with_response(
        json.dumps(response)
    )

    positions = {
        task.id: index
        for index, task in enumerate(
            result.tasks
        )
    }

    assert positions["task-1"] < positions["task-2"]
    assert positions["task-2"] < positions["task-3"]


def test_independent_tasks_do_not_require_dependencies():

    response = {
        "tasks": [
            {
                "id": "task-1",
                "description": "Inspect backend",
                "category": "analysis",
                "dependencies": [],
                "affected_areas": ["backend"],
                "acceptance_criteria": [],
            },
            {
                "id": "task-2",
                "description": "Inspect frontend",
                "category": "analysis",
                "dependencies": [],
                "affected_areas": ["frontend"],
                "acceptance_criteria": [],
            },
        ],
    }

    result = run_with_response(
        json.dumps(response)
    )

    assert all(
        not task.dependencies
        for task in result.tasks
    )


def test_decomposer_rejects_empty_task_decomposition():

    response = {
        "tasks": [],
    }

    with pytest.raises(ValueError):
        run_with_response(
            json.dumps(response)
        )


def test_decomposer_rejects_duplicate_task_descriptions():

    response = {
        "tasks": [
            {
                "id": "task-1",
                "description": "Implement authentication",
                "category": "implementation",
                "dependencies": [],
                "affected_areas": [],
                "acceptance_criteria": [],
            },
            {
                "id": "task-2",
                "description": "Implement authentication",
                "category": "implementation",
                "dependencies": [],
                "affected_areas": [],
                "acceptance_criteria": [],
            },
        ],
    }

    with pytest.raises(ValueError):
        run_with_response(
            json.dumps(response)
        )


def test_decomposer_rejects_task_with_no_actionable_description():

    response = json.loads(
        valid_response()
    )

    response["tasks"][0]["description"] = (
        "task"
    )

    with pytest.raises(ValueError):
        run_with_response(
            json.dumps(response)
        )


def test_decomposer_propagates_chat_service_failure():

    class FailingChatService:

        def chat(self, prompt):

            raise RuntimeError(
                "AI unavailable"
            )

    decomposer = AITaskDecomposer(
        FailingChatService()
    )

    with pytest.raises(RuntimeError):
        decomposer.decompose(
            requirement()
        )


def test_decomposer_sends_requirement_to_chat_service():

    class RecordingChatService:

        def __init__(self):

            self.prompt = None

        def chat(self, prompt):

            self.prompt = prompt

            return valid_response()

    chat_service = RecordingChatService()

    decomposer = AITaskDecomposer(
        chat_service
    )

    req = requirement()

    decomposer.decompose(
        req
    )

    assert req.objective in chat_service.prompt


def test_decomposer_prompt_requires_json():

    class RecordingChatService:

        def __init__(self):

            self.prompt = None

        def chat(self, prompt):

            self.prompt = prompt

            return valid_response()

    chat_service = RecordingChatService()

    decomposer = AITaskDecomposer(
        chat_service
    )

    decomposer.decompose(
        requirement()
    )

    assert "JSON" in chat_service.prompt


def test_decomposer_prompt_requires_dependency_information():

    class RecordingChatService:

        def __init__(self):

            self.prompt = None

        def chat(self, prompt):

            self.prompt = prompt

            return valid_response()

    chat_service = RecordingChatService()

    decomposer = AITaskDecomposer(
        chat_service
    )

    decomposer.decompose(
        requirement()
    )

    assert "dependencies" in (
        chat_service.prompt.lower()
    )