import json

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

from brain.engineering.design.system_designer import (
    SystemDesigner,
)

from brain.engineering.tasks.models.task_decomposition import (
    TaskDecomposition,
)


class AISystemDesigner(SystemDesigner):
    """
    Uses the AI runtime to produce a validated system design
    from an engineering task decomposition.
    """

    _REQUIRED_DESIGN_FIELDS = {
        "components",
        "interfaces",
        "dependencies",
        "data_flows",
        "constraints",
        "decisions",
        "acceptance_criteria",
    }

    _REQUIRED_COMPONENT_FIELDS = {
        "id",
        "name",
        "responsibility",
        "layer",
        "interfaces",
    }

    _REQUIRED_INTERFACE_FIELDS = {
        "id",
        "name",
        "owner",
        "consumers",
        "purpose",
    }

    _REQUIRED_DEPENDENCY_FIELDS = {
        "source",
        "target",
        "reason",
    }

    _REQUIRED_DATA_FLOW_FIELDS = {
        "source",
        "target",
        "data",
    }

    def __init__(
        self,
        chat_service,
    ):
        if not hasattr(chat_service, "chat"):
            raise TypeError(
                "chat_service must provide a chat method"
            )

        self._chat_service = chat_service

    def design(
        self,
        task_decomposition: TaskDecomposition,
    ) -> SystemDesign:

        if not isinstance(
            task_decomposition,
            TaskDecomposition,
        ):
            raise TypeError(
                "task_decomposition must be a TaskDecomposition"
            )

        prompt = self._build_prompt(
            task_decomposition,
        )

        response = self._chat_service.chat(
            prompt,
        )

        return self._parse_response(
            task_decomposition,
            response,
        )

    @staticmethod
    def _build_prompt(
        task_decomposition: TaskDecomposition,
    ) -> str:

        requirement = (
            task_decomposition.requirement
        )

        tasks = task_decomposition.tasks

        return f"""
You are a senior software architect.

Design the system required to satisfy the engineering
requirement and its decomposed engineering tasks.

Return ONLY valid JSON.
Do not use markdown.
Do not include explanations outside the JSON.

The JSON must contain exactly these fields:

{{
  "components": [
    {{
      "id": "unique-component-id",
      "name": "string",
      "responsibility": "string",
      "layer": "string",
      "interfaces": ["interface-id"]
    }}
  ],
  "interfaces": [
    {{
      "id": "unique-interface-id",
      "name": "string",
      "owner": "component-id",
      "consumers": ["component-id"],
      "purpose": "string"
    }}
  ],
  "dependencies": [
    {{
      "source": "component-id",
      "target": "component-id",
      "reason": "string"
    }}
  ],
  "data_flows": [
    {{
      "source": "component-id",
      "target": "component-id",
      "data": "string"
    }}
  ],
  "constraints": ["string"],
  "decisions": ["string"],
  "acceptance_criteria": ["string"]
}}

Rules:

- Design only what is supported by the requirement and tasks.
- Do not invent unrelated components or functionality.
- Every component must have a clear responsibility.
- Component IDs must be unique.
- Interface IDs must be unique.
- Dependencies must reference existing component IDs.
- Interface owners must reference existing component IDs.
- Interface consumers must reference existing component IDs.
- Data-flow sources and targets must reference existing component IDs.
- Component interface references must reference existing interface IDs.
- Do not create self-dependencies.
- Do not create circular component dependencies.
- Do not assume a specific technology unless supported by the requirement,
  constraints, or tasks.
- Preserve relevant constraints from the requirement.
- Preserve relevant acceptance criteria from the requirement.
- Design decisions must describe meaningful architectural choices.
- Do not use a fixed architecture pattern for every request.
- The design must be appropriate to the actual requirement.

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

Tasks:
{[
    {
        "id": task.id,
        "description": task.description,
        "category": task.category,
        "dependencies": sorted(task.dependencies),
        "affected_areas": sorted(task.affected_areas),
        "acceptance_criteria": sorted(
            task.acceptance_criteria
        ),
    }
    for task in tasks
]}
""".strip()

    @classmethod
    def _parse_response(
        cls,
        task_decomposition: TaskDecomposition,
        response: str,
    ) -> SystemDesign:

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

        if set(data) != cls._REQUIRED_DESIGN_FIELDS:
            raise ValueError(
                "AI response contains an invalid schema"
            )

        components = cls._parse_components(
            data["components"]
        )

        interfaces = cls._parse_interfaces(
            data["interfaces"]
        )

        dependencies = cls._parse_dependencies(
            data["dependencies"]
        )

        data_flows = cls._parse_data_flows(
            data["data_flows"]
        )

        constraints = cls._parse_string_list(
            data["constraints"],
            "constraints",
        )

        decisions = cls._parse_string_list(
            data["decisions"],
            "decisions",
        )

        acceptance_criteria = (
            cls._parse_string_list(
                data["acceptance_criteria"],
                "acceptance_criteria",
            )
        )

        cls._validate_design(
            components=components,
            interfaces=interfaces,
            dependencies=dependencies,
            data_flows=data_flows,
        )

        requirement = (
            task_decomposition.requirement
        )

        return SystemDesign(
            requirement=requirement,
            tasks=tuple(
                task_decomposition.tasks
            ),
            components=tuple(
                components
            ),
            interfaces=tuple(
                interfaces
            ),
            dependencies=tuple(
                dependencies
            ),
            data_flows=tuple(
                data_flows
            ),
            constraints=constraints,
            decisions=decisions,
            acceptance_criteria=(
                acceptance_criteria
            ),
        )

    @classmethod
    def _parse_components(
        cls,
        raw_components,
    ) -> list[DesignComponent]:

        if not isinstance(
            raw_components,
            list,
        ):
            raise TypeError(
                "components must be a list"
            )

        components = []

        for raw in raw_components:

            if not isinstance(
                raw,
                dict,
            ):
                raise TypeError(
                    "each component must be a JSON object"
                )

            if set(raw) != cls._REQUIRED_COMPONENT_FIELDS:
                raise ValueError(
                    "component contains an invalid schema"
                )

            cls._require_string(
                raw["id"],
                "component id",
            )

            cls._require_string(
                raw["name"],
                "component name",
            )

            cls._require_string(
                raw["responsibility"],
                "component responsibility",
            )

            cls._require_string(
                raw["layer"],
                "component layer",
            )

            interfaces = cls._parse_string_list(
                raw["interfaces"],
                "component interfaces",
            )

            components.append(
                DesignComponent(
                    id=raw["id"],
                    name=raw["name"],
                    responsibility=raw["responsibility"],
                    layer=raw["layer"],
                    interfaces=interfaces,
                )
            )

        return components

    @classmethod
    def _parse_interfaces(
        cls,
        raw_interfaces,
    ) -> list[DesignInterface]:

        if not isinstance(
            raw_interfaces,
            list,
        ):
            raise TypeError(
                "interfaces must be a list"
            )

        interfaces = []

        for raw in raw_interfaces:

            if not isinstance(
                raw,
                dict,
            ):
                raise TypeError(
                    "each interface must be a JSON object"
                )

            if set(raw) != cls._REQUIRED_INTERFACE_FIELDS:
                raise ValueError(
                    "interface contains an invalid schema"
                )

            cls._require_string(
                raw["id"],
                "interface id",
            )

            cls._require_string(
                raw["name"],
                "interface name",
            )

            cls._require_string(
                raw["owner"],
                "interface owner",
            )

            consumers = cls._parse_string_list(
                raw["consumers"],
                "interface consumers",
            )

            cls._require_string(
                raw["purpose"],
                "interface purpose",
            )

            interfaces.append(
                DesignInterface(
                    id=raw["id"],
                    name=raw["name"],
                    owner=raw["owner"],
                    consumers=consumers,
                    purpose=raw["purpose"],
                )
            )

        return interfaces

    @classmethod
    def _parse_dependencies(
        cls,
        raw_dependencies,
    ) -> list[DesignDependency]:

        if not isinstance(
            raw_dependencies,
            list,
        ):
            raise TypeError(
                "dependencies must be a list"
            )

        dependencies = []

        for raw in raw_dependencies:

            if not isinstance(
                raw,
                dict,
            ):
                raise TypeError(
                    "each dependency must be a JSON object"
                )

            if set(raw) != cls._REQUIRED_DEPENDENCY_FIELDS:
                raise ValueError(
                    "dependency contains an invalid schema"
                )

            cls._require_string(
                raw["source"],
                "dependency source",
            )

            cls._require_string(
                raw["target"],
                "dependency target",
            )

            cls._require_string(
                raw["reason"],
                "dependency reason",
            )

            dependencies.append(
                DesignDependency(
                    source=raw["source"],
                    target=raw["target"],
                    reason=raw["reason"],
                )
            )

        return dependencies

    @classmethod
    def _parse_data_flows(
        cls,
        raw_data_flows,
    ) -> list[DataFlow]:

        if not isinstance(
            raw_data_flows,
            list,
        ):
            raise TypeError(
                "data_flows must be a list"
            )

        data_flows = []

        for raw in raw_data_flows:

            if not isinstance(
                raw,
                dict,
            ):
                raise TypeError(
                    "each data flow must be a JSON object"
                )

            if set(raw) != cls._REQUIRED_DATA_FLOW_FIELDS:
                raise ValueError(
                    "data flow contains an invalid schema"
                )

            cls._require_string(
                raw["source"],
                "data flow source",
            )

            cls._require_string(
                raw["target"],
                "data flow target",
            )

            cls._require_string(
                raw["data"],
                "data flow data",
            )

            data_flows.append(
                DataFlow(
                    source=raw["source"],
                    target=raw["target"],
                    data=raw["data"],
                )
            )

        return data_flows

    @classmethod
    def _parse_string_list(
        cls,
        value,
        field_name: str,
    ) -> frozenset[str]:

        if not isinstance(
            value,
            list,
        ):
            raise TypeError(
                f"{field_name} must be a list"
            )

        if not all(
            isinstance(item, str)
            for item in value
        ):
            raise TypeError(
                f"{field_name} must contain only strings"
            )

        if any(
            not item.strip()
            for item in value
        ):
            raise ValueError(
                f"{field_name} must not contain empty strings"
            )

        return frozenset(value)

    @staticmethod
    def _require_string(
        value,
        field_name: str,
    ) -> None:

        if not isinstance(
            value,
            str,
        ):
            raise TypeError(
                f"{field_name} must be a string"
            )

        if not value.strip():
            raise ValueError(
                f"{field_name} must not be empty"
            )

    @classmethod
    def _validate_design(
        cls,
        components: list[DesignComponent],
        interfaces: list[DesignInterface],
        dependencies: list[DesignDependency],
        data_flows: list[DataFlow],
    ) -> None:

        component_ids = [
            component.id
            for component in components
        ]

        if len(component_ids) != len(
            set(component_ids)
        ):
            raise ValueError(
                "component IDs must be unique"
            )

        interface_ids = [
            interface.id
            for interface in interfaces
        ]

        if len(interface_ids) != len(
            set(interface_ids)
        ):
            raise ValueError(
                "interface IDs must be unique"
            )

        component_id_set = set(
            component_ids
        )

        interface_id_set = set(
            interface_ids
        )

        for component in components:

            unknown_interfaces = (
                component.interfaces
                - interface_id_set
            )

            if unknown_interfaces:
                raise ValueError(
                    "component references unknown interfaces"
                )

        for interface in interfaces:

            if interface.owner not in component_id_set:
                raise ValueError(
                    "interface references unknown owner"
                )

            unknown_consumers = (
                interface.consumers
                - component_id_set
            )

            if unknown_consumers:
                raise ValueError(
                    "interface references unknown consumers"
                )

        for dependency in dependencies:

            if dependency.source not in component_id_set:
                raise ValueError(
                    "dependency references unknown source"
                )

            if dependency.target not in component_id_set:
                raise ValueError(
                    "dependency references unknown target"
                )

            if dependency.source == dependency.target:
                raise ValueError(
                    "component cannot depend on itself"
                )

        for flow in data_flows:

            if flow.source not in component_id_set:
                raise ValueError(
                    "data flow references unknown source"
                )

            if flow.target not in component_id_set:
                raise ValueError(
                    "data flow references unknown target"
                )

            if flow.source == flow.target:
                raise ValueError(
                    "data flow cannot have identical source and target"
                )

        cls._validate_dependency_graph(
            dependencies
        )

    @staticmethod
    def _validate_dependency_graph(
        dependencies: list[DesignDependency],
    ) -> None:

        graph: dict[str, set[str]] = {}

        for dependency in dependencies:

            graph.setdefault(
                dependency.source,
                set(),
            ).add(
                dependency.target
            )

            graph.setdefault(
                dependency.target,
                set(),
            )

        visiting: set[str] = set()
        visited: set[str] = set()

        def visit(component_id: str):

            if component_id in visiting:
                raise ValueError(
                    "component dependencies contain a cycle"
                )

            if component_id in visited:
                return

            visiting.add(component_id)

            for dependency in graph[
                component_id
            ]:
                visit(dependency)

            visiting.remove(component_id)
            visited.add(component_id)

        for component_id in graph:
            visit(component_id)