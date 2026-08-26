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


class PatternDetector:
    """
    Infers architectural patterns from structural evidence.
    """

    def detect(
        self,
        components: frozenset[Component],
        layers: frozenset[Layer],
        flows: frozenset[DependencyFlow],
    ) -> frozenset[ArchitecturePattern]:

        patterns = set()

        layered = self._detect_layered(
            components,
            layers,
            flows,
        )

        if layered is not None:
            patterns.add(
                layered
            )

        return frozenset(
            patterns
        )

    def _detect_layered(
        self,
        components: frozenset[Component],
        layers: frozenset[Layer],
        flows: frozenset[DependencyFlow],
    ) -> ArchitecturePattern | None:

        if len(layers) < 2:
            return None

        if not components:
            return None

        evidence = set()

        evidence.add(
            "multiple architectural layers"
        )

        if flows:
            evidence.add(
                "dependencies exist between components"
            )

        confidence = 0.7

        if flows:
            confidence += 0.15

        if len(layers) >= 3:
            confidence += 0.1

        confidence = min(
            confidence,
            1.0,
        )

        return ArchitecturePattern(
            name="layered",
            confidence=confidence,
            evidence=frozenset(
                evidence
            ),
        )