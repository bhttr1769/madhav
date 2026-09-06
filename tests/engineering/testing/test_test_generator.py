from brain.engineering.testing.test_generator import (
    TestGenerator,
)


def test_test_generator_is_abstract():

    assert TestGenerator.__abstractmethods__ == {
        "generate",
    }