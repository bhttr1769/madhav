import ast
from pathlib import Path

from brain.code.models.module import (
    Module,
)

from brain.code.models.parsed_module import (
    ParsedModule,
)


class ModuleParser:
    """
    Converts a parsed Python module into
    structured module knowledge.
    """

    def parse(
        self,
        parsed_module: ParsedModule,
    ) -> Module:

        tree = ast.parse(
            parsed_module.source,
            filename=parsed_module.path,
        )

        imports = set()
        classes = set()
        functions = set()

        for node in tree.body:

            if isinstance(
                node,
                ast.Import,
            ):

                for alias in node.names:

                    imports.add(
                        alias.name
                    )

            elif isinstance(
                node,
                ast.ImportFrom,
            ):

                if node.module:

                    imports.add(
                        node.module
                    )

            elif isinstance(
                node,
                ast.ClassDef,
            ):

                classes.add(
                    node.name
                )

            elif isinstance(
                node,
                ast.FunctionDef,
            ):

                functions.add(
                    node.name
                )

            elif isinstance(
                node,
                ast.AsyncFunctionDef,
            ):

                functions.add(
                    node.name
                )

        return Module(
            name=Path(
                parsed_module.path
            ).stem,

            path=parsed_module.path,

            imports=frozenset(
                imports
            ),

            classes=frozenset(
                classes
            ),

            functions=frozenset(
                functions
            ),
        )