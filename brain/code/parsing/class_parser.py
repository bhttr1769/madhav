import ast
from pathlib import Path

from brain.code.models.class_model import (
    ClassModel,
)


class ClassParser:
    """
    Extracts class structure from a Python AST.
    """

    def parse(
        self,
        source: str,
        path: str | Path,
    ) -> frozenset[ClassModel]:

        tree = ast.parse(
            source,
            filename=str(path),
        )

        classes = set()

        module_name = Path(
            path
        ).stem

        for node in ast.walk(tree):

            if not isinstance(
                node,
                ast.ClassDef,
            ):
                continue

            bases = set()

            for base in node.bases:

                if isinstance(
                    base,
                    ast.Name,
                ):

                    bases.add(
                        base.id
                    )

                elif isinstance(
                    base,
                    ast.Attribute,
                ):

                    bases.add(
                        ast.unparse(base)
                    )

            methods = set()

            for child in node.body:

                if isinstance(
                    child,
                    (
                        ast.FunctionDef,
                        ast.AsyncFunctionDef,
                    ),
                ):

                    methods.add(
                        child.name
                    )

            classes.add(
                ClassModel(
                    name=node.name,
                    module=module_name,
                    bases=frozenset(
                        bases
                    ),
                    methods=frozenset(
                        methods
                    ),
                )
            )

        return frozenset(
            classes
        )