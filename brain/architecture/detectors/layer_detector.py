from brain.architecture.models.component import (
    Component,
)

from brain.architecture.models.layer import (
    Layer,
)


class LayerDetector:
    """
    Detects logical architectural layers from components.
    """

    LAYER_RULES = {
        "model": {
            "models",
            "model",
            "entities",
            "entity",
            "domain",
        },
        "service": {
            "services",
            "service",
        },
        "parsing": {
            "parsing",
            "parser",
            "parsers",
            "extraction",
            "extractors",
        },
        "storage": {
            "storage",
            "stores",
            "persistence",
            "repositories",
            "repository",
        },
        "integration": {
            "integrations",
            "integration",
            "clients",
            "api",
        },
        "infrastructure": {
            "environment",
            "filesystem",
            "io",
            "execution",
        },
        "registry": {
            "registry",
            "registries",
        },
        "pipeline": {
            "pipeline",
            "pipelines",
        },
    }

    def detect(
        self,
        components: frozenset[Component],
    ) -> frozenset[Layer]:

        layers = {}

        for component in components:

            component_name = (
                component.name.lower()
            )

            for (
                layer_name,
                component_names,
            ) in self.LAYER_RULES.items():

                if (
                    component_name
                    not in component_names
                ):
                    continue

                if layer_name not in layers:

                    layers[
                        layer_name
                    ] = set()

                layers[
                    layer_name
                ].add(
                    component.name
                )

        result = set()

        for (
            layer_name,
            component_names,
        ) in layers.items():

            result.add(
                Layer(
                    name=layer_name,
                    components=frozenset(
                        component_names
                    ),
                    confidence=1.0,
                )
            )

        return frozenset(
            result
        )