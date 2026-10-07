import pytest

from brain.agents.agent_definition_validator import (
    AgentDefinitionValidator,
)
from brain.agents.models.agent_definition import (
    AgentDefinition,
)
from brain.agents.models.agent_identity import (
    AgentIdentity,
)


def create_definition(
    identity=None,
    description="Research agent.",
    version="1.0.0",
    capabilities=frozenset(),
):
    return AgentDefinition(
        identity=(
            identity
            if identity is not None
            else AgentIdentity(
                id="agent-001",
                name="Research Agent",
            )
        ),
        description=description,
        version=version,
        capabilities=capabilities,
    )


def test_valid_agent_definition_passes():
    definition = create_definition()

    AgentDefinitionValidator().validate(
        definition
    )


def test_invalid_definition_type_raises_type_error():
    with pytest.raises(TypeError):
        AgentDefinitionValidator().validate(
            object()
        )


def test_invalid_identity_type_raises_type_error():
    definition = create_definition(
        identity="invalid"
    )

    with pytest.raises(TypeError):
        AgentDefinitionValidator().validate(
            definition
        )


def test_empty_identity_id_raises_value_error():
    definition = create_definition(
        identity=AgentIdentity(
            id="",
            name="Research Agent",
        )
    )

    with pytest.raises(ValueError):
        AgentDefinitionValidator().validate(
            definition
        )


def test_empty_identity_name_raises_value_error():
    definition = create_definition(
        identity=AgentIdentity(
            id="agent-001",
            name="   ",
        )
    )

    with pytest.raises(ValueError):
        AgentDefinitionValidator().validate(
            definition
        )


def test_empty_description_raises_value_error():
    definition = create_definition(
        description="   "
    )

    with pytest.raises(ValueError):
        AgentDefinitionValidator().validate(
            definition
        )


def test_empty_version_raises_value_error():
    definition = create_definition(
        version=""
    )

    with pytest.raises(ValueError):
        AgentDefinitionValidator().validate(
            definition
        )


def test_invalid_capabilities_type_raises_type_error():
    definition = create_definition(
        capabilities={"research.execute"}
    )

    with pytest.raises(TypeError):
        AgentDefinitionValidator().validate(
            definition
        )


def test_non_string_capability_id_raises_type_error():
    definition = create_definition(
        capabilities=frozenset({123})
    )

    with pytest.raises(TypeError):
        AgentDefinitionValidator().validate(
            definition
        )


def test_empty_capability_id_raises_value_error():
    definition = create_definition(
        capabilities=frozenset({"   "})
    )

    with pytest.raises(ValueError):
        AgentDefinitionValidator().validate(
            definition
        )


def test_empty_capability_set_is_valid():
    definition = create_definition(
        capabilities=frozenset()
    )

    AgentDefinitionValidator().validate(
        definition
    )