from brain.code.parsing.class_parser import (
    ClassParser,
)


SOURCE = """
class BaseCalculator:
    pass


class Calculator(BaseCalculator):

    def add(self, a, b):
        return a + b

    async def calculate(self):
        return 42


class Empty:
    pass
"""


def test_class_parser_extracts_classes(
    tmp_path,
):

    file = (
        tmp_path
        / "calculator.py"
    )

    classes = ClassParser().parse(
        SOURCE,
        file,
    )

    names = {
        class_model.name
        for class_model in classes
    }

    assert names == {
        "BaseCalculator",
        "Calculator",
        "Empty",
    }


def test_class_parser_extracts_module(
    tmp_path,
):

    file = (
        tmp_path
        / "calculator.py"
    )

    classes = ClassParser().parse(
        SOURCE,
        file,
    )

    calculator = next(
        class_model
        for class_model in classes
        if class_model.name
        == "Calculator"
    )

    assert (
        calculator.module
        == "calculator"
    )


def test_class_parser_extracts_bases(
    tmp_path,
):

    file = (
        tmp_path
        / "calculator.py"
    )

    classes = ClassParser().parse(
        SOURCE,
        file,
    )

    calculator = next(
        class_model
        for class_model in classes
        if class_model.name
        == "Calculator"
    )

    assert (
        calculator.bases
        == frozenset({
            "BaseCalculator",
        })
    )


def test_class_parser_extracts_methods(
    tmp_path,
):

    file = (
        tmp_path
        / "calculator.py"
    )

    classes = ClassParser().parse(
        SOURCE,
        file,
    )

    calculator = next(
        class_model
        for class_model in classes
        if class_model.name
        == "Calculator"
    )

    assert (
        calculator.methods
        == frozenset({
            "add",
            "calculate",
        })
    )


def test_class_parser_handles_empty_class(
    tmp_path,
):

    file = (
        tmp_path
        / "calculator.py"
    )

    classes = ClassParser().parse(
        SOURCE,
        file,
    )

    empty = next(
        class_model
        for class_model in classes
        if class_model.name
        == "Empty"
    )

    assert (
        empty.methods
        == frozenset()
    )