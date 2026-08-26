from brain.code.models.code_structure import (
    CodeStructure,
)

from brain.code.services.code_understanding_service import (
    CodeUnderstandingService,
)


class FakeBuilder:

    def __init__(
        self,
    ):

        self.files = None

        self.result = CodeStructure(
            modules=frozenset(),
            classes=frozenset(),
            functions=frozenset(),
            imports=frozenset(),
            calls=frozenset(),
        )

    def build(
        self,
        files,
    ):

        self.files = files

        return self.result


def test_service_analyzes_file(
    tmp_path,
):

    file = (
        tmp_path
        / "example.py"
    )

    file.write_text(
        "def hello():\n    pass\n",
        encoding="utf-8",
    )

    builder = FakeBuilder()

    service = CodeUnderstandingService(
        builder,
    )

    result = service.analyze_file(
        file,
    )

    assert (
        result
        == builder.result
    )

    assert (
        builder.files
        == [file]
    )


def test_service_analyzes_multiple_files(
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

    builder = FakeBuilder()

    service = CodeUnderstandingService(
        builder,
    )

    result = service.analyze_files(
        [
            first,
            second,
        ]
    )

    assert (
        result
        == builder.result
    )

    assert (
        builder.files
        == [
            first,
            second,
        ]
    )


def test_service_analyzes_directory(
    tmp_path,
):

    source = (
        tmp_path
        / "src"
    )

    source.mkdir()

    first = (
        source
        / "first.py"
    )

    second = (
        source
        / "second.py"
    )

    ignored = (
        source
        / "notes.txt"
    )

    first.write_text(
        "def first():\n    pass\n",
        encoding="utf-8",
    )

    second.write_text(
        "def second():\n    pass\n",
        encoding="utf-8",
    )

    ignored.write_text(
        "not python",
        encoding="utf-8",
    )

    builder = FakeBuilder()

    service = CodeUnderstandingService(
        builder,
    )

    result = service.analyze_directory(
        source,
    )

    assert (
        result
        == builder.result
    )

    assert set(
        builder.files
    ) == {
        first,
        second,
    }


def test_service_analyzes_real_python_file(
    tmp_path,
):

    file = (
        tmp_path
        / "calculator.py"
    )

    file.write_text(
        """
import math


class Calculator:

    def add(self, a, b):
        return a + b


def main():
    print("hello")
""",
        encoding="utf-8",
    )

    service = CodeUnderstandingService()

    result = service.analyze_file(
        file,
    )

    assert len(
        result.modules
    ) == 1

    assert len(
        result.classes
    ) == 1

    assert len(
        result.functions
    ) == 2

    assert len(
        result.imports
    ) == 1

    assert len(
        result.calls
    ) == 1