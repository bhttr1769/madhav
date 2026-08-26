from brain.code.parsing.function_parser import (
    FunctionParser,
)


SOURCE = """
def add(a, b):
    return a + b


async def load(value, limit=10):
    return value


class Calculator:

    def multiply(self, a, b):
        return a * b

    async def calculate(self, value):
        return value


class AdvancedCalculator(Calculator):

    def divide(self, a, b):
        return a / b
"""


def parse(
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

    return (
        FunctionParser().parse(
            SOURCE,
            file,
        )
    )


def test_parser_extracts_functions(
    tmp_path,
):

    functions = parse(
        tmp_path,
    )

    names = {
        function.name
        for function in functions
    }

    assert names == {
        "add",
        "load",
        "multiply",
        "calculate",
        "divide",
    }


def test_parser_distinguishes_methods(
    tmp_path,
):

    functions = parse(
        tmp_path,
    )

    multiply = next(
        function
        for function in functions
        if function.name
        == "multiply"
    )

    add = next(
        function
        for function in functions
        if function.name
        == "add"
    )

    assert (
        multiply.class_name
        == "Calculator"
    )

    assert (
        add.class_name
        is None
    )


def test_parser_extracts_parameters(
    tmp_path,
):

    functions = parse(
        tmp_path,
    )

    add = next(
        function
        for function in functions
        if function.name
        == "add"
    )

    assert (
        add.parameters
        == frozenset({
            "a",
            "b",
        })
    )


def test_parser_extracts_async_functions(
    tmp_path,
):

    functions = parse(
        tmp_path,
    )

    load = next(
        function
        for function in functions
        if function.name
        == "load"
    )

    calculate = next(
        function
        for function in functions
        if function.name
        == "calculate"
    )

    assert load.is_async is True
    assert calculate.is_async is True


def test_parser_extracts_nested_class_methods(
    tmp_path,
):

    functions = parse(
        tmp_path,
    )

    divide = next(
        function
        for function in functions
        if function.name
        == "divide"
    )

    assert (
        divide.class_name
        == "AdvancedCalculator"
    )