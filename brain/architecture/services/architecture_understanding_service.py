from brain.architecture.detectors.component_detector import (
    ComponentDetector,
)

from brain.architecture.detectors.dependency_flow_detector import (
    DependencyFlowDetector,
)

from brain.architecture.detectors.layer_detector import (
    LayerDetector,
)

from brain.architecture.detectors.pattern_detector import (
    PatternDetector,
)

from brain.architecture.models.architecture_model import (
    ArchitectureModel,
)


class ArchitectureUnderstandingService:
    """
    Orchestrates architectural understanding.
    """

    def __init__(
        self,
        component_detector=None,
        layer_detector=None,
        dependency_flow_detector=None,
        pattern_detector=None,
    ):

        self._component_detector = (
            component_detector
            if component_detector is not None
            else ComponentDetector()
        )

        self._layer_detector = (
            layer_detector
            if layer_detector is not None
            else LayerDetector()
        )

        self._dependency_flow_detector = (
            dependency_flow_detector
            if dependency_flow_detector is not None
            else DependencyFlowDetector()
        )

        self._pattern_detector = (
            pattern_detector
            if pattern_detector is not None
            else PatternDetector()
        )

    def analyze(
        self,
        files,
        imports,
        name: str = "workspace",
    ) -> ArchitectureModel:

        components = (
            self._component_detector.detect(
                files,
            )
        )

        layers = (
            self._layer_detector.detect(
                components,
            )
        )

        flows = (
            self._dependency_flow_detector.detect(
                components,
                imports,
            )
        )

        patterns = (
            self._pattern_detector.detect(
                components,
                layers,
                flows,
            )
        )

        pattern_names = frozenset(
            pattern.name
            for pattern in patterns
        )

        if pattern_names:

            pattern = ", ".join(
                sorted(
                    pattern_names
                )
            )

        else:

            pattern = "unknown"

        return ArchitectureModel(
            name=name,
            pattern=pattern,
            components=frozenset(
                component.name
                for component in components
            ),
            layers=frozenset(
                layer.name
                for layer in layers
            ),
        )