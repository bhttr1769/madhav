from brain.architecture.models.architecture_model import (
    ArchitectureModel,
)

from brain.architecture.models.architecture_pattern import (
    ArchitecturePattern,
)

from brain.architecture.models.component import (
    Component,
)

from brain.architecture.models.dependency_flow import (
    DependencyFlow,
)

from brain.architecture.models.layer import (
    Layer,
)

from brain.knowledge.builders.graph_builder import (
    GraphBuilder,
)

from brain.knowledge.models.edge_type import (
    EdgeType,
)

from brain.knowledge.models.node_type import (
    NodeType,
)

from brain.knowledge.stores.graph_store import (
    GraphStore,
)


class ArchitectureKnowledgeBuilder:
    """
    Converts architecture understanding into
    knowledge graph nodes and relationships.
    """

    def __init__(
        self,
        builder: GraphBuilder,
    ):

        self._builder = builder

    def build(
        self,
        architecture: ArchitectureModel,
        components: frozenset[Component],
        layers: frozenset[Layer],
        flows: frozenset[DependencyFlow],
        patterns: frozenset[ArchitecturePattern],
        workspace_id: str = "workspace",
    ) -> GraphStore:

        self._ensure_workspace(
            workspace_id,
        )

        architecture_node = (
            self._build_architecture(
                workspace_id,
                architecture,
            )
        )

        component_nodes = (
            self._build_components(
                architecture_node.id,
                components,
            )
        )

        self._build_layers(
            architecture_node.id,
            layers,
        )

        self._build_patterns(
            architecture_node.id,
            patterns,
        )

        self._build_flows(
            component_nodes,
            flows,
        )

        return self._builder._store

    def _ensure_workspace(
        self,
        workspace_id: str,
    ) -> None:

        if (
            self._builder._store.get_node(
                workspace_id,
            )
            is None
        ):

            self._builder.add_node(
                node_type=NodeType.PROJECT,
                name="Workspace",
                metadata={
                    "source": "architecture",
                },
                node_id=workspace_id,
            )

    def _build_architecture(
        self,
        workspace_id: str,
        architecture: ArchitectureModel,
    ):

        node_id = (
            f"architecture:"
            f"{architecture.name}"
        )

        node = (
            self._builder.add_node(
                node_type=NodeType.ARCHITECTURE,
                name=architecture.name,
                properties={
                    "pattern": architecture.pattern,
                    "components": sorted(
                        architecture.components,
                    ),
                    "layers": sorted(
                        architecture.layers,
                    ),
                },
                metadata={
                    "source": "architecture",
                    "entity": "architecture",
                },
                node_id=node_id,
            )
        )

        self._builder.add_edge(
            source_id=workspace_id,
            target_id=node.id,
            edge_type=EdgeType.BUILT_WITH,
            metadata={
                "source": "architecture",
            },
        )

        return node

    def _build_components(
        self,
        architecture_id: str,
        components: frozenset[Component],
    ) -> dict[str, object]:

        nodes = {}

        for component in components:

            node_id = (
                f"architecture-component:"
                f"{component.name}"
            )

            node = (
                self._builder.add_node(
                    node_type=NodeType.DIRECTORY,
                    name=component.name,
                    properties={
                        "path": component.path,
                        "layer": component.layer,
                        "modules": sorted(
                            component.modules,
                        ),
                    },
                    metadata={
                        "source": "architecture",
                        "entity": "component",
                    },
                    node_id=node_id,
                )
            )

            self._builder.add_edge(
                source_id=architecture_id,
                target_id=node.id,
                edge_type=EdgeType.CONTAINS,
                metadata={
                    "source": "architecture",
                },
            )

            nodes[component.name] = node

        return nodes

    def _build_layers(
        self,
        architecture_id: str,
        layers: frozenset[Layer],
    ) -> None:

        for layer in layers:

            node_id = (
                f"architecture-layer:"
                f"{layer.name}"
            )

            node = (
                self._builder.add_node(
                    node_type=NodeType.ARCHITECTURE,
                    name=(
                        f"Layer: "
                        f"{layer.name}"
                    ),
                    properties={
                        "components": sorted(
                            layer.components,
                        ),
                        "confidence": (
                            layer.confidence
                        ),
                    },
                    metadata={
                        "source": "architecture",
                        "entity": "layer",
                    },
                    node_id=node_id,
                )
            )

            self._builder.add_edge(
                source_id=architecture_id,
                target_id=node.id,
                edge_type=EdgeType.CONTAINS,
                metadata={
                    "source": "architecture",
                },
            )

    def _build_patterns(
        self,
        architecture_id: str,
        patterns: frozenset[ArchitecturePattern],
    ) -> None:

        for pattern in patterns:

            node_id = (
                f"architecture-pattern:"
                f"{pattern.name}"
            )

            node = (
                self._builder.add_node(
                    node_type=NodeType.ARCHITECTURE,
                    name=(
                        f"Pattern: "
                        f"{pattern.name}"
                    ),
                    properties={
                        "confidence": (
                            pattern.confidence
                        ),
                        "evidence": sorted(
                            pattern.evidence,
                        ),
                    },
                    metadata={
                        "source": "architecture",
                        "entity": "pattern",
                    },
                    node_id=node_id,
                )
            )

            self._builder.add_edge(
                source_id=architecture_id,
                target_id=node.id,
                edge_type=EdgeType.IMPLEMENTS,
                metadata={
                    "source": "architecture",
                },
            )

    def _build_flows(
        self,
        component_nodes: dict[str, object],
        flows: frozenset[DependencyFlow],
    ) -> None:

        for flow in flows:

            source_node = component_nodes.get(
                flow.source,
            )

            target_node = component_nodes.get(
                flow.target,
            )

            if (
                source_node is None
                or target_node is None
            ):
                continue

            self._builder.add_edge(
                source_id=source_node.id,
                target_id=target_node.id,
                edge_type=EdgeType.DEPENDS_ON,
                properties={
                    "imports": sorted(
                        flow.imports,
                    ),
                },
                metadata={
                    "source": "architecture",
                    "entity": "dependency_flow",
                },
            )