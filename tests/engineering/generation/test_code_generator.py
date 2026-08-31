from brain.engineering.generation.code_generator import (
    CodeGenerator,
)

from brain.engineering.generation.models.generation_result import (
    GenerationResult,
)


class FakeCodeGenerator(CodeGenerator):

    def generate(
        self,
        request,
    ) -> GenerationResult:

        raise NotImplementedError


def test_code_generator_is_abstract():

    assert CodeGenerator.__abstractmethods__ == {
        "generate",
    }


def test_concrete_code_generator_can_be_implemented():

    generator = FakeCodeGenerator()

    assert isinstance(
        generator,
        CodeGenerator,
    )