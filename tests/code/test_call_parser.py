from brain.code.models.call_model import (
    CallModel,
)

from brain.code.parsing.call_parser import (
    CallParser,
)


SOURCE = """
def calculate(value):
    return value * 2


def main():
    calculate(10)
    print("done")


class Calculator:

    def run(self):
        self.calculate()
        helper()


def helper():
    return 42
"""


def parse(
    tmp_path,
):

    file = (
        tmp_path
        / "example.py"
    )

    file.write_text(
        SOURCE,
        encoding="utf-8",
    )

    return (
        CallParser().parse(
            SOURCE,
            file,
        )
    )


def test_call_parser_extracts_function_calls(
    tmp_path,
):

    calls = parse(
        tmp_path,
    )

    assert CallModel(
        caller="main",
        callee="calculate",
        module="example",
    ) in calls

    assert CallModel(
        caller="main",
        callee="print",
        module="example",
    ) in calls


def test_call_parser_extracts_method_calls(
    tmp_path,
):

    calls = parse(
        tmp_path,
    )

    assert CallModel(
        caller="run",
        callee="self.calculate",
        module="example",
    ) in calls


def test_call_parser_extracts_multiple_calls(
    tmp_path,
):

    calls = parse(
        tmp_path,
    )

    assert CallModel(
        caller="run",
        callee="helper",
        module="example",
    ) in calls


def test_call_parser_returns_empty_for_no_calls(
    tmp_path,
):

    source = """
def hello():
    return 42
"""

    file = (
        tmp_path
        / "empty_calls.py"
    )

    file.write_text(
        source,
        encoding="utf-8",
    )

    calls = (
        CallParser().parse(
            source,
            file,
        )
    )

    assert calls == frozenset()