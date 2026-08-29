import pytest

from brain.engineering.requirements.fake_requirement_interpreter import (
    FakeRequirementInterpreter,
)

from brain.engineering.requirements.models.requirement import (
    Requirement,
)

from brain.engineering.requirements.requirement_understanding_service import (
    RequirementUnderstandingService,
)


def make_requirement():
    return Requirement(
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


def test_service_returns_interpreter_result():

    requirement = make_requirement()

    interpreter = FakeRequirementInterpreter(
        result=requirement,
    )

    service = RequirementUnderstandingService(
        interpreter=interpreter,
    )

    result = service.understand(
        "build an API",
    )

    assert result == requirement


def test_service_strips_request():

    requirement = make_requirement()

    interpreter = FakeRequirementInterpreter(
        result=requirement,
    )

    service = RequirementUnderstandingService(
        interpreter=interpreter,
    )

    result = service.understand(
        "   build an API   ",
    )

    assert result == requirement


def test_service_rejects_non_string():

    interpreter = FakeRequirementInterpreter(
        result=make_requirement(),
    )

    service = RequirementUnderstandingService(
        interpreter=interpreter,
    )

    with pytest.raises(TypeError):
        service.understand(
            123,
        )


def test_service_rejects_empty_request():

    interpreter = FakeRequirementInterpreter(
        result=make_requirement(),
    )

    service = RequirementUnderstandingService(
        interpreter=interpreter,
    )

    with pytest.raises(ValueError):
        service.understand(
            "",
        )


def test_service_rejects_whitespace_request():

    interpreter = FakeRequirementInterpreter(
        result=make_requirement(),
    )

    service = RequirementUnderstandingService(
        interpreter=interpreter,
    )

    with pytest.raises(ValueError):
        service.understand(
            "   ",
        )


def test_service_rejects_invalid_interpreter_result():

    interpreter = FakeRequirementInterpreter(
        result="invalid",
    )

    service = RequirementUnderstandingService(
        interpreter=interpreter,
    )

    with pytest.raises(TypeError):
        service.understand(
            "build an API",
        )


def test_service_rejects_invalid_interpreter():

    with pytest.raises(TypeError):
        RequirementUnderstandingService(
            interpreter="invalid",
        )