from pathlib import Path

from brain.architecture.models.component import (
    Component,
)


class ComponentDetector:
    """
    Detects logical architectural components from
    a Python source tree.
    """

    def detect(
        self,
        files: list[str | Path],
    ) -> frozenset[Component]:

        components = {}

        for file in files:

            path = Path(file)

            parts = path.parts

            if not parts:
                continue

            if (
                "brain"
                in parts
            ):

                brain_index = (
                    parts.index(
                        "brain"
                    )
                )

                if (
                    len(parts)
                    <= brain_index + 1
                ):
                    continue

                component_name = (
                    parts[
                        brain_index + 1
                    ]
                )

                component_path = str(
                    Path(
                        *parts[
                            :brain_index + 2
                        ]
                    )
                )

            else:

                component_name = (
                    path.parent.name
                )

                component_path = str(
                    path.parent
                )

            if component_name not in components:

                components[
                    component_name
                ] = {
                    "path": component_path,
                    "modules": set(),
                }

            components[
                component_name
            ][
                "modules"
            ].add(
                path.stem
            )

        result = set()

        for name, data in components.items():

            result.add(
                Component(
                    name=name,
                    path=data["path"],
                    layer=None,
                    modules=frozenset(
                        data["modules"]
                    ),
                )
            )

        return frozenset(
            result
        )