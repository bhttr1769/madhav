import ast
from pathlib import Path

from brain.code.models.parsed_module import (
    ParsedModule,
)


class PythonASTParser:
    """
    Parses Python source code using the standard AST parser.
    """

    def parse(
        self,
        path: str | Path,
    ) -> ParsedModule:

        path = Path(path)

        source = path.read_text(
            encoding="utf-8",
        )

        tree = ast.parse(
            source,
            filename=str(path),
        )

        return ParsedModule(
            path=str(path),
            source=source,
            node_count=sum(
                1
                for _ in ast.walk(tree)
            ),
        )