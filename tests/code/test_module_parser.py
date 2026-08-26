from brain.code.models.parsed_module import (
    ParsedModule,
)

from brain.code.parsing.module_parser import (
    ModuleParser,
)


def create_module(
    tmp_path,
):

    file = (
        tmp_path
        / "calculator.py"
    )

    source = """
import os
from pathlib import Path

class Calculator:
    pass

def add(a, b):
    return a + b

async def calculate():
    return 42
"""

    file.write_text(
        source,
        encoding="utf-8",
    )

    return ParsedModule(
        path=str(file),
        source=source,
        node_count=10,
    )


def test_module_parser_extracts_name(
    tmp_path,
):

    module = ModuleParser().parse(
        create_module(
            tmp_path,
        )
    )

    assert (
        module.name
        == "calculator"
    )


def test_module_parser_extracts_imports(
    tmp_path,
):

    module = ModuleParser().parse(
        create_module(
            tmp_path,
        )
    )

    assert (
        module.imports
        == frozenset({
            "os",
            "pathlib",
        })
    )


def test_module_parser_extracts_classes(
    tmp_path,
):

    module = ModuleParser().parse(
        create_module(
            tmp_path,
        )
    )

    assert (
        module.classes
        == frozenset({
            "Calculator",
        })
    )


def test_module_parser_extracts_functions(
    tmp_path,
):

    module = ModuleParser().parse(
        create_module(
            tmp_path,
        )
    )

    assert (
        module.functions
        == frozenset({
            "add",
            "calculate",
        })
    )


def test_module_parser_preserves_path(
    tmp_path,
):

    parsed = create_module(
        tmp_path,
    )

    module = ModuleParser().parse(
        parsed,
    )

    assert (
        module.path
        == parsed.path
    )