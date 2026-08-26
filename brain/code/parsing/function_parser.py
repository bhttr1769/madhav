import ast
from pathlib import Path

from brain.code.models.function_model import (
    FunctionModel,
)


class FunctionParser:
    """
    Extracts Python functions and methods from source code.
    """

    def parse(
        self,
        source: str,
        path: str | Path,
    ) -> frozenset[FunctionModel]:

        tree = ast.parse(
            source,
            filename=str(path),
        )

        functions = set()

        module_name = Path(
            path
        ).stem

        def extract_parameters(
            node,
        ):

            parameters = set()

            for argument in (
                node.args.posonlyargs
                + node.args.args
                + node.args.kwonlyargs
            ):

                parameters.add(
                    argument.arg
                )

            if node.args.vararg:

                parameters.add(
                    node.args.vararg.arg
                )

            if node.args.kwarg:

                parameters.add(
                    node.args.kwarg.arg
                )

            return frozenset(
                parameters
            )

        def visit(
            node,
            class_name=None,
        ):

            if isinstance(
                node,
                ast.ClassDef,
            ):

                for child in node.body:

                    if isinstance(
                        child,
                        (
                            ast.FunctionDef,
                            ast.AsyncFunctionDef,
                        ),
                    ):

                        functions.add(
                            FunctionModel(
                                name=child.name,
                                module=module_name,
                                class_name=node.name,
                                parameters=(
                                    extract_parameters(
                                        child
                                    )
                                ),
                                is_async=isinstance(
                                    child,
                                    ast.AsyncFunctionDef,
                                ),
                            )
                        )

                    elif isinstance(
                        child,
                        ast.ClassDef,
                    ):

                        visit(
                            child,
                            node.name,
                        )

                return

            if isinstance(
                node,
                (
                    ast.FunctionDef,
                    ast.AsyncFunctionDef,
                ),
            ):

                functions.add(
                    FunctionModel(
                        name=node.name,
                        module=module_name,
                        class_name=class_name,
                        parameters=(
                            extract_parameters(
                                node
                            )
                        ),
                        is_async=isinstance(
                            node,
                            ast.AsyncFunctionDef,
                        ),
                    )
                )

                return

            for child in ast.iter_child_nodes(
                node
            ):

                visit(
                    child,
                    class_name,
                )

        visit(tree)

        return frozenset(
            functions
        )