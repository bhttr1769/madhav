from pathlib import Path

from brain.architecture.models.component import (
    Component,
)

from brain.architecture.models.dependency_flow import (
    DependencyFlow,
)

from brain.code.models.import_model import (
    ImportModel,
)


class DependencyFlowDetector:
    """
    Detects dependency flows between architectural components.
    """

    def detect(
        self,
        components: frozenset[Component],
        imports: frozenset[ImportModel],
    ) -> frozenset[DependencyFlow]:

        flows = {}

        for import_model in imports:

            source_component = (
                self._component_for_path(
                    import_model.path,
                    components,
                )
            )

            target_component = (
                self._component_for_module(
                    import_model.module,
                    components,
                )
            )

            if (
                source_component is None
                or target_component is None
            ):
                continue

            if (
                source_component
                == target_component
            ):
                continue

            key = (
                source_component,
                target_component,
            )

            if key not in flows:

                flows[key] = set()

            flows[key].add(
                import_model.module
            )

        return frozenset(
            DependencyFlow(
                source=source,
                target=target,
                imports=frozenset(
                    imported_modules
                ),
            )
            for (
                source,
                target,
            ), imported_modules in flows.items()
        )

    def _component_for_path(
        self,
        path: str,
        components: frozenset[Component],
    ) -> str | None:

        if not path:
            return None

        normalized_path = (
            Path(path)
            .as_posix()
        )

        for component in components:

            component_path = (
                Path(component.path)
                .as_posix()
                .rstrip("/")
            )

            if (
                normalized_path
                == component_path
                or normalized_path.startswith(
                    component_path + "/"
                )
            ):
                return component.name

        return None

    def _component_for_module(
        self,
        module: str,
        components: frozenset[Component],
    ) -> str | None:

        if not module:
            return None

        normalized_module = (
            module.replace(
                "/",
                ".",
            )
            .replace(
                "\\",
                ".",
            )
        )

        for component in components:

            component_path = (
                Path(component.path)
                .as_posix()
            )

            parts = component_path.split(
                "/"
            )

            if (
                "brain" not in parts
            ):
                continue

            brain_index = (
                parts.index(
                    "brain"
                )
            )

            component_parts = (
                parts[
                    brain_index:
                ]
            )

            component_module = ".".join(
                component_parts
            )

            if (
                normalized_module
                == component_module
                or normalized_module.startswith(
                    component_module + "."
                )
            ):
                return component.name

        return None