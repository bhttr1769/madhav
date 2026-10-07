from brain.agents.models.agent_definition import (
    AgentDefinition,
)
from brain.agents.models.agent_identity import (
    AgentIdentity,
)


class AgentDefinitionValidator:
    def validate(
        self,
        definition: AgentDefinition,
    ) -> None:
        if not isinstance(
            definition,
            AgentDefinition,
        ):
            raise TypeError(
                "definition must be an AgentDefinition"
            )

        if not isinstance(
            definition.identity,
            AgentIdentity,
        ):
            raise TypeError(
                "definition.identity must be an AgentIdentity"
            )

        if not isinstance(
            definition.identity.id,
            str,
        ):
            raise TypeError(
                "identity.id must be a string"
            )

        if not definition.identity.id.strip():
            raise ValueError(
                "identity.id must not be empty"
            )

        if not isinstance(
            definition.identity.name,
            str,
        ):
            raise TypeError(
                "identity.name must be a string"
            )

        if not definition.identity.name.strip():
            raise ValueError(
                "identity.name must not be empty"
            )

        if not isinstance(
            definition.description,
            str,
        ):
            raise TypeError(
                "description must be a string"
            )

        if not definition.description.strip():
            raise ValueError(
                "description must not be empty"
            )

        if not isinstance(
            definition.version,
            str,
        ):
            raise TypeError(
                "version must be a string"
            )

        if not definition.version.strip():
            raise ValueError(
                "version must not be empty"
            )

        if not isinstance(
            definition.capabilities,
            frozenset,
        ):
            raise TypeError(
                "capabilities must be a frozenset"
            )

        for capability_id in definition.capabilities:
            if not isinstance(
                capability_id,
                str,
            ):
                raise TypeError(
                    "capabilities must contain only strings"
                )

            if not capability_id.strip():
                raise ValueError(
                    "capability IDs must not be empty"
                )