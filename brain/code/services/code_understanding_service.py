from pathlib import Path

from brain.code.models.code_structure import (
    CodeStructure,
)

from brain.code.parsing.code_structure_builder import (
    CodeStructureBuilder,
)


class CodeUnderstandingService:
    """
    Provides the public interface for Python code understanding.
    """

    def __init__(
        self,
        builder: CodeStructureBuilder | None = None,
    ):

        self._builder = (
            builder
            if builder is not None
            else CodeStructureBuilder()
        )

    def analyze_file(
        self,
        file: str | Path,
    ) -> CodeStructure:

        return self._builder.build(
            [file],
        )

    def analyze_files(
        self,
        files: list[str | Path],
    ) -> CodeStructure:

        return self._builder.build(
            files,
        )

    def analyze_directory(
        self,
        directory: str | Path,
    ) -> CodeStructure:

        directory = Path(
            directory
        )

        files = [
            path
            for path in directory.rglob(
                "*.py"
            )
            if path.is_file()
        ]

        return self._builder.build(
            files,
        )