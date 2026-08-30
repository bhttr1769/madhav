import json

import pytest

from brain.engineering.design.ai_system_designer import (
    AISystemDesigner,
)

from brain.engineering.design.models.data_flow import (
    DataFlow,
)

from brain.engineering.design.models.design_component import (
    DesignComponent,
)

from brain.engineering.design.models.design_dependency import (
    DesignDependency,
)

from brain.engineering.design.models.design_interface import (
    DesignInterface,
)

from brain.engineering.design.models.system_design import (
    SystemDesign,
)

from brain.engineering.requirements.models.requirement import (
    Requirement,
)

from brain.engineering.tasks.models.task import (
    Task,
)

from brain.engineering.tasks.models.task_decomposition import (
    TaskDecomposition,
)


class FakeChatService:

    def __init__(
        self,
        response: str,
    ):
        self._response = response
        self.call_count = 0
        self.last_prompt = None

    def chat(
        self,
        prompt: str,
    ) -> str:
        self.call_count += 1
        self.last_prompt = prompt
        return self._response


def requirement() -> Requirement:

    return Requirement(
        original_request="Build an authentication API",
        objective="Add authentication to the application",
        functional_requirements=frozenset({
            "Users can authenticate",
        }),
        non_functional_requirements=frozenset({
            "Authentication must be secure",
        }),
        constraints=frozenset({
            "Use the existing backend",
        }),
        acceptance_criteria=frozenset({
            "Authenticated users can access protected resources",
        }),
        assumptions=frozenset({
            "A user database already exists",
        }),
        ambiguities=frozenset({
            "Authentication method is unspecified",
        }),
        affected_areas=frozenset({
            "authentication",
            "application backend",
        }),
        confidence=0.95,
    )


def task_decomposition() -> TaskDecomposition:

    req = requirement()

    task = Task(
        id="task-1",
        description="Implement authentication",
        category="implementation",
        dependencies=frozenset(),
        affected_areas=frozenset({
            "authentication",
        }),
        acceptance_criteria=frozenset({
            "Users can authenticate",
        }),
    )

    return TaskDecomposition(
        requirement=req,
        tasks=(task,),
    )


def valid_response() -> str:

    return json.dumps({
        "components": [
            {
                "id": "component-api",
                "name": "Authentication API",
                "responsibility": "Handle authentication requests",
                "layer": "application",
                "interfaces": [
                    "interface-auth",
                ],
            },
            {
                "id": "component-db",
                "name": "User Database",
                "responsibility": "Store and retrieve user credentials",
                "layer": "data",
                "interfaces": [],
            },
        ],
        "interfaces": [
            {
                "id": "interface-auth",
                "name": "Authentication Interface",
                "owner": "component-api",
                "consumers": [],
                "purpose": "Authenticate users",
            },
        ],
        "dependencies": [
            {
                "source": "component-api",
                "target": "component-db",
                "reason": "Authentication requires user data",
            },
        ],
        "data_flows": [
            {
                "source": "component-api",
                "target": "component-db",
                "data": "User credentials",
            },
        ],
        "constraints": [
            "Use the existing backend",
        ],
        "decisions": [
            "Separate authentication logic from data storage",
        ],
        "acceptance_criteria": [
            "Authenticated users can access protected resources",
        ],
    })


def designer(
    response=None,
):

    if response is None:
        response = valid_response()

    return AISystemDesigner(
        FakeChatService(response)
    )


def test_designer_returns_system_design():

    result = designer().design(
        task_decomposition()
    )

    assert isinstance(
        result,
        SystemDesign,
    )


def test_designer_preserves_requirement():

    decomposition = task_decomposition()

    result = designer().design(
        decomposition
    )

    assert result.requirement == decomposition.requirement


def test_designer_preserves_tasks():

    decomposition = task_decomposition()

    result = designer().design(
        decomposition
    )

    assert result.tasks == decomposition.tasks


def test_designer_parses_components():

    result = designer().design(
        task_decomposition()
    )

    assert result.components == (
        DesignComponent(
            id="component-api",
            name="Authentication API",
            responsibility="Handle authentication requests",
            layer="application",
            interfaces=frozenset({
                "interface-auth",
            }),
        ),
        DesignComponent(
            id="component-db",
            name="User Database",
            responsibility="Store and retrieve user credentials",
            layer="data",
            interfaces=frozenset(),
        ),
    )


def test_designer_parses_interfaces():

    result = designer().design(
        task_decomposition()
    )

    assert result.interfaces == (
        DesignInterface(
            id="interface-auth",
            name="Authentication Interface",
            owner="component-api",
            consumers=frozenset(),
            purpose="Authenticate users",
        ),
    )


def test_designer_parses_dependencies():

    result = designer().design(
        task_decomposition()
    )

    assert result.dependencies == (
        DesignDependency(
            source="component-api",
            target="component-db",
            reason="Authentication requires user data",
        ),
    )


def test_designer_parses_data_flows():

    result = designer().design(
        task_decomposition()
    )

    assert result.data_flows == (
        DataFlow(
            source="component-api",
            target="component-db",
            data="User credentials",
        ),
    )


def test_designer_parses_constraints():

    result = designer().design(
        task_decomposition()
    )

    assert result.constraints == frozenset({
        "Use the existing backend",
    })


def test_designer_parses_decisions():

    result = designer().design(
        task_decomposition()
    )

    assert result.decisions == frozenset({
        "Separate authentication logic from data storage",
    })


def test_designer_parses_acceptance_criteria():

    result = designer().design(
        task_decomposition()
    )

    assert result.acceptance_criteria == frozenset({
        "Authenticated users can access protected resources",
    })


def test_designer_calls_chat_service_once():

    chat_service = FakeChatService(
        valid_response()
    )

    designer_instance = AISystemDesigner(
        chat_service
    )

    designer_instance.design(
        task_decomposition()
    )

    assert chat_service.call_count == 1


def test_designer_sends_prompt_to_chat_service():

    chat_service = FakeChatService(
        valid_response()
    )

    designer_instance = AISystemDesigner(
        chat_service
    )

    designer_instance.design(
        task_decomposition()
    )

    assert chat_service.last_prompt is not None
    assert "Build an authentication API" in (
        chat_service.last_prompt
    )
    assert "Implement authentication" in (
        chat_service.last_prompt
    )
    assert "Users can authenticate" in (
        chat_service.last_prompt
    )


def test_designer_rejects_invalid_task_decomposition():

    designer_instance = designer()

    with pytest.raises(TypeError):
        designer_instance.design(
            None
        )


def test_designer_rejects_non_string_response():

    class InvalidChatService:

        def chat(self, prompt):

            return {
                "components": []
            }

    designer_instance = AISystemDesigner(
        InvalidChatService()
    )

    with pytest.raises(TypeError):
        designer_instance.design(
            task_decomposition()
        )


def test_designer_rejects_invalid_json():

    designer_instance = designer(
        "not valid json"
    )

    with pytest.raises(ValueError):
        designer_instance.design(
            task_decomposition()
        )


def test_designer_rejects_json_array():

    designer_instance = designer(
        json.dumps([])
    )

    with pytest.raises(ValueError):
        designer_instance.design(
            task_decomposition()
        )


def test_designer_rejects_missing_design_field():

    data = json.loads(
        valid_response()
    )

    del data["decisions"]

    designer_instance = designer(
        json.dumps(data)
    )

    with pytest.raises(ValueError):
        designer_instance.design(
            task_decomposition()
        )


def test_designer_rejects_extra_design_field():

    data = json.loads(
        valid_response()
    )

    data["extra"] = []

    designer_instance = designer(
        json.dumps(data)
    )

    with pytest.raises(ValueError):
        designer_instance.design(
            task_decomposition()
        )


def test_designer_rejects_non_list_components():

    data = json.loads(
        valid_response()
    )

    data["components"] = {}

    designer_instance = designer(
        json.dumps(data)
    )

    with pytest.raises(TypeError):
        designer_instance.design(
            task_decomposition()
        )


def test_designer_rejects_component_with_invalid_schema():

    data = json.loads(
        valid_response()
    )

    del data["components"][0]["layer"]

    designer_instance = designer(
        json.dumps(data)
    )

    with pytest.raises(ValueError):
        designer_instance.design(
            task_decomposition()
        )


def test_designer_rejects_non_string_component_id():

    data = json.loads(
        valid_response()
    )

    data["components"][0]["id"] = 123

    designer_instance = designer(
        json.dumps(data)
    )

    with pytest.raises(TypeError):
        designer_instance.design(
            task_decomposition()
        )


def test_designer_rejects_empty_component_name():

    data = json.loads(
        valid_response()
    )

    data["components"][0]["name"] = " "

    designer_instance = designer(
        json.dumps(data)
    )

    with pytest.raises(ValueError):
        designer_instance.design(
            task_decomposition()
        )


def test_designer_rejects_component_with_unknown_interface():

    data = json.loads(
        valid_response()
    )

    data["components"][0]["interfaces"] = [
        "unknown-interface",
    ]

    designer_instance = designer(
        json.dumps(data)
    )

    with pytest.raises(ValueError):
        designer_instance.design(
            task_decomposition()
        )


def test_designer_rejects_duplicate_component_ids():

    data = json.loads(
        valid_response()
    )

    data["components"][1]["id"] = (
        data["components"][0]["id"]
    )

    designer_instance = designer(
        json.dumps(data)
    )

    with pytest.raises(ValueError):
        designer_instance.design(
            task_decomposition()
        )


def test_designer_rejects_non_list_interfaces():

    data = json.loads(
        valid_response()
    )

    data["interfaces"] = {}

    designer_instance = designer(
        json.dumps(data)
    )

    with pytest.raises(TypeError):
        designer_instance.design(
            task_decomposition()
        )


def test_designer_rejects_duplicate_interface_ids():

    data = json.loads(
        valid_response()
    )

    data["interfaces"].append(
        data["interfaces"][0].copy()
    )

    designer_instance = designer(
        json.dumps(data)
    )

    with pytest.raises(ValueError):
        designer_instance.design(
            task_decomposition()
        )


def test_designer_rejects_unknown_interface_owner():

    data = json.loads(
        valid_response()
    )

    data["interfaces"][0]["owner"] = (
        "unknown-component"
    )

    designer_instance = designer(
        json.dumps(data)
    )

    with pytest.raises(ValueError):
        designer_instance.design(
            task_decomposition()
        )


def test_designer_rejects_unknown_interface_consumer():

    data = json.loads(
        valid_response()
    )

    data["interfaces"][0]["consumers"] = [
        "unknown-component",
    ]

    designer_instance = designer(
        json.dumps(data)
    )

    with pytest.raises(ValueError):
        designer_instance.design(
            task_decomposition()
        )


def test_designer_rejects_non_list_dependencies():

    data = json.loads(
        valid_response()
    )

    data["dependencies"] = {}

    designer_instance = designer(
        json.dumps(data)
    )

    with pytest.raises(TypeError):
        designer_instance.design(
            task_decomposition()
        )


def test_designer_rejects_unknown_dependency_source():

    data = json.loads(
        valid_response()
    )

    data["dependencies"][0]["source"] = (
        "unknown-component"
    )

    designer_instance = designer(
        json.dumps(data)
    )

    with pytest.raises(ValueError):
        designer_instance.design(
            task_decomposition()
        )


def test_designer_rejects_unknown_dependency_target():

    data = json.loads(
        valid_response()
    )

    data["dependencies"][0]["target"] = (
        "unknown-component"
    )

    designer_instance = designer(
        json.dumps(data)
    )

    with pytest.raises(ValueError):
        designer_instance.design(
            task_decomposition()
        )


def test_designer_rejects_self_dependency():

    data = json.loads(
        valid_response()
    )

    data["dependencies"][0]["target"] = (
        data["dependencies"][0]["source"]
    )

    designer_instance = designer(
        json.dumps(data)
    )

    with pytest.raises(ValueError):
        designer_instance.design(
            task_decomposition()
        )


def test_designer_rejects_dependency_cycle():

    data = json.loads(
        valid_response()
    )

    data["dependencies"].append({
        "source": "component-db",
        "target": "component-api",
        "reason": "Creates a reverse dependency",
    })

    designer_instance = designer(
        json.dumps(data)
    )

    with pytest.raises(ValueError):
        designer_instance.design(
            task_decomposition()
        )


def test_designer_rejects_non_list_data_flows():

    data = json.loads(
        valid_response()
    )

    data["data_flows"] = {}

    designer_instance = designer(
        json.dumps(data)
    )

    with pytest.raises(TypeError):
        designer_instance.design(
            task_decomposition()
        )


def test_designer_rejects_unknown_data_flow_source():

    data = json.loads(
        valid_response()
    )

    data["data_flows"][0]["source"] = (
        "unknown-component"
    )

    designer_instance = designer(
        json.dumps(data)
    )

    with pytest.raises(ValueError):
        designer_instance.design(
            task_decomposition()
        )


def test_designer_rejects_unknown_data_flow_target():

    data = json.loads(
        valid_response()
    )

    data["data_flows"][0]["target"] = (
        "unknown-component"
    )

    designer_instance = designer(
        json.dumps(data)
    )

    with pytest.raises(ValueError):
        designer_instance.design(
            task_decomposition()
        )


def test_designer_rejects_identical_data_flow_source_and_target():

    data = json.loads(
        valid_response()
    )

    data["data_flows"][0]["target"] = (
        data["data_flows"][0]["source"]
    )

    designer_instance = designer(
        json.dumps(data)
    )

    with pytest.raises(ValueError):
        designer_instance.design(
            task_decomposition()
        )


def test_designer_rejects_non_list_constraints():

    data = json.loads(
        valid_response()
    )

    data["constraints"] = {}

    designer_instance = designer(
        json.dumps(data)
    )

    with pytest.raises(TypeError):
        designer_instance.design(
            task_decomposition()
        )


def test_designer_rejects_non_string_constraint():

    data = json.loads(
        valid_response()
    )

    data["constraints"] = [
        123,
    ]

    designer_instance = designer(
        json.dumps(data)
    )

    with pytest.raises(TypeError):
        designer_instance.design(
            task_decomposition()
        )


def test_designer_rejects_empty_constraint():

    data = json.loads(
        valid_response()
    )

    data["constraints"] = [
        " ",
    ]

    designer_instance = designer(
        json.dumps(data)
    )

    with pytest.raises(ValueError):
        designer_instance.design(
            task_decomposition()
        )


def test_designer_rejects_non_list_decisions():

    data = json.loads(
        valid_response()
    )

    data["decisions"] = {}

    designer_instance = designer(
        json.dumps(data)
    )

    with pytest.raises(TypeError):
        designer_instance.design(
            task_decomposition()
        )


def test_designer_rejects_empty_decision():

    data = json.loads(
        valid_response()
    )

    data["decisions"] = [
        " ",
    ]

    designer_instance = designer(
        json.dumps(data)
    )

    with pytest.raises(ValueError):
        designer_instance.design(
            task_decomposition()
        )


def test_designer_rejects_non_list_acceptance_criteria():

    data = json.loads(
        valid_response()
    )

    data["acceptance_criteria"] = {}

    designer_instance = designer(
        json.dumps(data)
    )

    with pytest.raises(TypeError):
        designer_instance.design(
            task_decomposition()
        )


def test_designer_rejects_empty_acceptance_criterion():

    data = json.loads(
        valid_response()
    )

    data["acceptance_criteria"] = [
        " ",
    ]

    designer_instance = designer(
        json.dumps(data)
    )

    with pytest.raises(ValueError):
        designer_instance.design(
            task_decomposition()
        )
