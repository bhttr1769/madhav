import ast
from pathlib import Path

from brain.code.models.call_model import (
    CallModel,
)


class CallParser:
    """
    Extracts function and method calls from Python source code.
    """

    def parse(
        self,
        source: str,
        path: str | Path,
    ) -> frozenset[CallModel]:

        tree = ast.parse(
            source,
            filename=str(path),
        )

        calls = set()

        module_name = Path(
            path
        ).stem

        def get_callee_name(
            node,
        ):

            if isinstance(
                node,
                ast.Name,
            ):

                return node.id

            if isinstance(
                node,
                ast.Attribute,
            ):

                value = (
                    get_callee_name(
                        node.value
                    )
                )

                if value:

                    return (
                        f"{value}."
                        f"{node.attr}"
                    )

                return node.attr

            return None

        def visit(
            node,
            caller=None,
        ):

            if isinstance(
                node,
                ast.FunctionDef,
            ):

                current_caller = (
                    node.name
                )

                for child in ast.walk(
                    node
                ):

                    if isinstance(
                        child,
                        ast.Call,
                    ):

                        callee = (
                            get_callee_name(
                                child.func
                            )
                        )

                        if callee:

                            calls.add(
                                CallModel(
                                    caller=(
                                        current_caller
                                    ),
                                    callee=callee,
                                    module=(
                                        module_name
                                    ),
                                )
                            )

                return

            if isinstance(
                node,
                ast.AsyncFunctionDef,
            ):

                current_caller = (
                    node.name
                )

                for child in ast.walk(
                    node
                ):

                    if isinstance(
                        child,
                        ast.Call,
                    ):

                        callee = (
                            get_callee_name(
                                child.func
                            )
                        )

                        if callee:

                            calls.add(
                                CallModel(
                                    caller=(
                                        current_caller
                                    ),
                                    callee=callee,
                                    module=(
                                        module_name
                                    ),
                                )
                            )

                return

            for child in ast.iter_child_nodes(
                node
            ):

                visit(
                    child,
                    caller,
                )

        visit(tree)

        return frozenset(
            calls
        )