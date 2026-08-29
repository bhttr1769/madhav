from brain.engineering.requirements.fake_requirement_interpreter import (
    FakeRequirementInterpreter,
)

from brain.engineering.requirements.models.requirement import (
    Requirement,
)

from brain.engineering.requirements.requirement_interpreter import (
    RequirementInterpreter,
)


def test_requirement_interpreter_is_interface():

    assert (
        RequirementInterpreter.__abstractmethods__
        == {"interpret"}
    )


def test_fake_requirement_interpreter_returns_result():

    requirement = Requirement(
        original_request="build an API",
        objective="build an API",
        functional_requirements=frozenset({
            "provide an API",
        }),
        non_functional_requirements=frozenset(),
        constraints=frozenset(),
        acceptance_criteria=frozenset(),
        assumptions=frozenset(),
        ambiguities=frozenset(),
        affected_areas=frozenset(),
        confidence=1.0,
    )

    interpreter = FakeRequirementInterpreter(
        result=requirement,
    )

    result = interpreter.interpret(
        "build an API",
    )

    assert result == requirement