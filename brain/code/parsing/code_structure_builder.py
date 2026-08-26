from pathlib import Path

from brain.code.models.code_structure import (
    CodeStructure,
)

from brain.code.models.parsed_module import (
    ParsedModule,
)

from brain.code.parsing.call_parser import (
    CallParser,
)

from brain.code.parsing.class_parser import (
    ClassParser,
)

from brain.code.parsing.function_parser import (
    FunctionParser,
)

from brain.code.parsing.import_parser import (
    ImportParser,
)

from brain.code.parsing.module_parser import (
    ModuleParser,
)


class CodeStructureBuilder:
    """
    Builds complete code structure knowledge
    from Python source files.
    """

    def __init__(
        self,
        module_parser=None,
        class_parser=None,
        function_parser=None,
        import_parser=None,
        call_parser=None,
    ):

        self._module_parser = (
            module_parser
            if module_parser is not None
            else ModuleParser()
        )

        self._class_parser = (
            class_parser
            if class_parser is not None
            else ClassParser()
        )

        self._function_parser = (
            function_parser
            if function_parser is not None
            else FunctionParser()
        )

        self._import_parser = (
            import_parser
            if import_parser is not None
            else ImportParser()
        )

        self._call_parser = (
            call_parser
            if call_parser is not None
            else CallParser()
        )

    def build(
        self,
        files: list[str | Path],
    ) -> CodeStructure:

        modules = set()
        classes = set()
        functions = set()
        imports = set()
        calls = set()

        for file in files:

            path = Path(file)

            source = path.read_text(
                encoding="utf-8",
            )

            parsed_module = ParsedModule(
                path=str(path),
                source=source,
                node_count=0,
            )

            modules.add(
                self._module_parser.parse(
                    parsed_module,
                )
            )

            classes.update(
                self._class_parser.parse(
                    source,
                    path,
                )
            )

            functions.update(
                self._function_parser.parse(
                    source,
                    path,
                )
            )

            imports.update(
                self._import_parser.parse(
                    source,
                    path,
                )
            )

            calls.update(
                self._call_parser.parse(
                    source,
                    path,
                )
            )

        return CodeStructure(
            modules=frozenset(
                modules
            ),
            classes=frozenset(
                classes
            ),
            functions=frozenset(
                functions
            ),
            imports=frozenset(
                imports
            ),
            calls=frozenset(
                calls
            ),
        )