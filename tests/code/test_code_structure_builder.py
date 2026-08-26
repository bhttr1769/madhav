from brain.code.parsing.code_structure_builder import (
    CodeStructureBuilder,
)


SOURCE = """
import os


class Calculator:

    def add(self, a, b):
        return a + b


def main():
    calculator = Calculator()
    calculator.add(1, 2)
"""


def test_builder_builds_code_structure(
    tmp_path,
):

    file = (
        tmp_path
        / "calculator.py"
    )

    file.write_text(
        SOURCE,
        encoding="utf-8",
    )

    structure = (
        CodeStructureBuilder().build(
            [file],
        )
    )

    assert len(
        structure.modules
    ) == 1

    assert len(
        structure.classes
    ) == 1

    assert len(
        structure.functions
    ) == 2

    assert len(
        structure.imports
    ) == 1

    assert len(
        structure.calls
    ) >= 2


def test_builder_preserves_module(
    tmp_path,
):

    file = (
        tmp_path
        / "calculator.py"
    )

    file.write_text(
        SOURCE,
        encoding="utf-8",
    )

    structure = (
        CodeStructureBuilder().build(
            [file],
        )
    )

    module = next(
        iter(
            structure.modules
        )
    )

    assert (
        module.name
        == "calculator"
    )


def test_builder_handles_multiple_files(
    tmp_path,
):

    first = (
        tmp_path
        / "first.py"
    )

    second = (
        tmp_path
        / "second.py"
    )

    first.write_text(
        "def first():\n    pass\n",
        encoding="utf-8",
    )

    second.write_text(
        "def second():\n    pass\n",
        encoding="utf-8",
    )

    structure = (
        CodeStructureBuilder().build(
            [
                first,
                second,
            ],
        )
    )

    assert len(
        structure.modules
    ) == 2

    assert len(
        structure.functions
    ) == 2