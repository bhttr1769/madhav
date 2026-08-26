from brain.architecture.services.architecture_understanding_service import (
    ArchitectureUnderstandingService,
)

from brain.architecture.models.architecture_model import (
    ArchitectureModel,
)


class FakeComponentDetector:

    def detect(
        self,
        files,
    ):

        return frozenset()


class FakeLayerDetector:

    def detect(
        self,
        components,
    ):

        return frozenset()


class FakeDependencyFlowDetector:

    def detect(
        self,
        components,
        imports,
    ):

        return frozenset()


class FakePatternDetector:

    def detect(
        self,
        components,
        layers,
        flows,
    ):

        return frozenset()


def test_service_returns_architecture_model():

    service = ArchitectureUnderstandingService(
        component_detector=FakeComponentDetector(),
        layer_detector=FakeLayerDetector(),
        dependency_flow_detector=(
            FakeDependencyFlowDetector()
        ),
        pattern_detector=FakePatternDetector(),
    )

    result = service.analyze(
        files=[],
        imports=[],
    )

    assert isinstance(
        result,
        ArchitectureModel,
    )

    assert result.name == "workspace"

    assert result.pattern == "unknown"

    assert result.components == frozenset()

    assert result.layers == frozenset()


def test_service_preserves_name():

    service = ArchitectureUnderstandingService(
        component_detector=FakeComponentDetector(),
        layer_detector=FakeLayerDetector(),
        dependency_flow_detector=(
            FakeDependencyFlowDetector()
        ),
        pattern_detector=FakePatternDetector(),
    )

    result = service.analyze(
        files=[],
        imports=[],
        name="Madhav",
    )

    assert result.name == "Madhav"