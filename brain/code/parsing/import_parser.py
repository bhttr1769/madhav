import ast

from brain.code.models.import_model import (
    ImportModel,
)


class ImportParser:
    """
    Extracts structured imports from Python source code.
    """

    def parse(
        self,
        source: str,
        path: str = "<unknown>",
    ) -> frozenset[ImportModel]:

        tree = ast.parse(
            source,
            filename=path,
        )

        imports = set()

        for node in ast.walk(tree):

            if isinstance(
                node,
                ast.Import,
            ):

                for alias in node.names:

                    imports.add(
                        ImportModel(
                            module=alias.name,
                            name=None,
                            alias=alias.asname,
                        )
                    )

            elif isinstance(
                node,
                ast.ImportFrom,
            ):

                module = (
                    node.module
                    or ""
                )

                for alias in node.names:

                    imports.add(
                        ImportModel(
                            module=module,
                            name=alias.name,
                            alias=alias.asname,
                            level=node.level,
                        )
                    )

        return frozenset(
            imports
        )