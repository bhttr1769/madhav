from brain.code.parsing.python_ast_parser import (
    PythonASTParser,
)


def test_parser_parses_python_file(
    tmp_path,
):

    file = (
        tmp_path
        / "example.py"
    )

    file.write_text(
        """
import os

def hello():
    return "hello"
""",
        encoding="utf-8",
    )

    result = (
        PythonASTParser().parse(
            file,
        )
    )

    assert (
        result.path
        == str(file)
    )

    assert (
        result.source
        != ""
    )

    assert (
        result.node_count
        > 0
    )


def test_parser_handles_empty_file(
    tmp_path,
):

    file = (
        tmp_path
        / "empty.py"
    )

    file.write_text(
        "",
        encoding="utf-8",
    )

    result = (
        PythonASTParser().parse(
            file,
        )
    )

    assert (
        result.node_count
        == 1
    )


def test_parser_rejects_invalid_python(
    tmp_path,
):

    file = (
        tmp_path
        / "broken.py"
    )

    file.write_text(
        "def broken(:",
        encoding="utf-8",
    )

    try:

        PythonASTParser().parse(
            file,
        )

    except SyntaxError:

        return

    assert False, (
        "Expected SyntaxError"
    )