import json

import pytest

from brain.code.models.code_structure import (
    CodeStructure,
)

from brain.engineering.analysis.models.engineering_quality_assessment import (
    EngineeringQualityAssessment,
)

from brain.engineering.design.models.system_design import (
    SystemDesign,
)

from brain.engineering.generation.ai_final_code_generator import (
    AIFinalCodeGenerator,
)

from brain.engineering.generation.models.code_change import (
    CodeChange,
)

from brain.engineering.generation.models.engineering_decision import (
    EngineeringDecision,
)

from brain.engineering.generation.models.final_generation_request import (
    FinalGenerationRequest,
)

from brain.engineering.generation.models.generation_result import (
    GenerationResult,
)

from brain.engineering.optimization.models.optimization_decision import (
    OptimizationDecision,
)

from brain.engineering.planning.models.plan import (
    EngineeringPlan,
)

from brain.engineering.requirements.models.requirement import (
    Requirement,
)

from brain.engineering.tasks.models.task import (
    Task,
)


class FakeChatService:

    def __init__(
        self,
        response: str,
    ):
        self.response = response
        self.call_count = 0
        self.last_prompt = None

    def chat(
        self,
        prompt: str,
    ) -> str:

        self.call_count += 1
        self.last_prompt = prompt

        return self.response


def requirement() -> Requirement:

    return Requirement(
        original_request="Add a health endpoint",
        objective="Add a health endpoint",
        functional_requirements=frozenset({
            "Expose a health endpoint",
        }),
        non_functional_requirements=frozenset({
            "The endpoint should be reliable",
        }),
        constraints=frozenset({
            "Use the existing backend",
        }),
        acceptance_criteria=frozenset({
            "Health endpoint returns successfully",
        }),
        assumptions=frozenset({
            "The existing backend is available",
        }),
        ambiguities=frozenset(),
        affected_areas=frozenset({
            "backend",
        }),
        confidence=0.95,
    )


def task() -> Task:

    return Task(
        id="task-health",
        description="Implement the health endpoint",
        category="implementation",
        dependencies=frozenset(),
        affected_areas=frozenset({
            "backend",
        }),
        acceptance_criteria=frozenset({
            "Health endpoint returns successfully",
        }),
    )


def design() -> SystemDesign:

    return SystemDesign(
        requirement=requirement(),
        tasks=(task(),),
        components=(),
        interfaces=(),
        dependencies=(),
        data_flows=(),
        constraints=frozenset({
            "Use the existing backend",
        }),
        decisions=frozenset(),
        acceptance_criteria=frozenset({
            "Health endpoint returns successfully",
        }),
    )


def plan() -> EngineeringPlan:

    return EngineeringPlan(
        task_order=("task-health",),
        strategy=(
            "Implement the endpoint in the existing backend.",
        ),
        milestones=(
            "Health endpoint implemented",
        ),
        required_capabilities=frozenset({
            "Python",
        }),
        risks=frozenset({
            "Implementation may affect existing backend behavior",
        }),
        assumptions=frozenset({
            "The existing backend is available",
        }),
        validation_strategy=(
            "Run the backend test suite.",
        ),
        confidence=0.9,
    )


def existing_code() -> CodeStructure:

    return CodeStructure(
        modules=frozenset(),
        classes=frozenset(),
        functions=frozenset(),
        imports=frozenset(),
        calls=frozenset(),
    )


def engineering_decision() -> EngineeringDecision:

    return EngineeringDecision(
        necessity=(
            "A new implementation is required "
            "to satisfy the health endpoint task."
        ),
        reuse_existing=True,
        use_standard_library=True,
        use_existing_dependency=False,
        new_dependency_required=False,
        abstraction_justified=False,
        optimization_justified=True,
        rationale=(
            "The existing backend should be reused.",
            "No new dependency is required.",
        ),
    )


def quality_assessment() -> EngineeringQualityAssessment:

    return EngineeringQualityAssessment(
        complexity="low",
        structural_complexity="low",
        cognitive_complexity="low",
        algorithmic_complexity="constant",
        dependency_complexity="low",
        abstraction_complexity="low",
        maintainability="high",
        clarity="high",
        cohesion="high",
        coupling="low",
        testability="high",
        extensibility="high",
        over_engineering=False,
        issues=(),
        strengths=(
            "Simple implementation structure.",
        ),
        recommendations=(
            "Preserve the current structure.",
        ),
        rationale=(
            "The candidate implementation is simple.",
        ),
    )


def optimization_decision() -> OptimizationDecision:

    return OptimizationDecision(
        optimization_justified=True,
        primary_objective="runtime",
        optimization_scope="request processing",
        bottleneck="repeated computation",
        strategies=(
            "reuse computed results",
        ),
        avoid_strategies=(
            "speculative micro-optimization",
        ),
        trade_offs=(
            "slightly higher memory usage",
        ),
        measurement_required=True,
        rationale=(
            "Repeated computation is a credible performance concern.",
        ),
    )


def proposed_changes() -> tuple[CodeChange, ...]:

    return (
        CodeChange(
            path="backend/health.py",
            operation="create",
            content=(
                "def health():\n"
                "    return {'status': 'ok'}\n"
            ),
        ),
    )


def final_generation_request() -> FinalGenerationRequest:

    return FinalGenerationRequest(
        task=task(),
        design=design(),
        plan=plan(),
        existing_code=existing_code(),
        engineering_decision=engineering_decision(),
        quality_assessment=quality_assessment(),
        optimization_decision=optimization_decision(),
        proposed_changes=proposed_changes(),
    )


def valid_response() -> str:

    return json.dumps({
        "changes": [
            {
                "path": "backend/health.py",
                "operation": "create",
                "content": (
                    "def health():\n"
                    "    return {'status': 'ok'}\n"
                ),
            },
        ],
        "decision": {
            "necessity": (
                "A new implementation is required "
                "to satisfy the health endpoint task."
            ),
            "reuse_existing": True,
            "use_standard_library": True,
            "use_existing_dependency": False,
            "new_dependency_required": False,
            "abstraction_justified": False,
            "optimization_justified": True,
            "rationale": [
                "The existing backend should be reused.",
                "No new dependency is required.",
            ],
        },
    })


def create_generator(
    response=None,
):

    if response is None:
        response = valid_response()

    chat_service = FakeChatService(
        response,
    )

    generator = AIFinalCodeGenerator(
        chat_service,
    )

    return generator, chat_service


def test_final_generator_requires_chat_service():

    with pytest.raises(TypeError):

        AIFinalCodeGenerator(
            None,
        )


def test_final_generator_requires_chat_method():

    class InvalidChatService:
        pass

    with pytest.raises(TypeError):

        AIFinalCodeGenerator(
            InvalidChatService(),
        )


def test_final_generator_rejects_invalid_request():

    generator, _ = create_generator()

    with pytest.raises(TypeError):

        generator.generate(
            object(),
        )


def test_final_generator_returns_generation_result():

    generator, _ = create_generator()

    result = generator.generate(
        final_generation_request(),
    )

    assert isinstance(
        result,
        GenerationResult,
    )


def test_final_generator_preserves_final_changes():

    generator, _ = create_generator()

    result = generator.generate(
        final_generation_request(),
    )

    assert result.changes == proposed_changes()


def test_final_generator_uses_shared_response_validation():

    generator, _ = create_generator(
        "not json",
    )

    with pytest.raises(ValueError):

        generator.generate(
            final_generation_request(),
        )


def test_final_generator_sends_engineering_context_to_ai():

    generator, chat_service = create_generator()

    generator.generate(
        final_generation_request(),
    )

    assert chat_service.call_count == 1

    assert "task-health" in chat_service.last_prompt
    assert "Implement the health endpoint" in (
        chat_service.last_prompt
    )
    assert "Health endpoint returns successfully" in (
        chat_service.last_prompt
    )
    assert "Use the existing backend" in (
        chat_service.last_prompt
    )


def test_final_generator_sends_engineering_decision_to_ai():

    generator, chat_service = create_generator()

    generator.generate(
        final_generation_request(),
    )

    prompt = chat_service.last_prompt

    assert "NECESSITY AND REUSE DECISION" in prompt
    assert "reuse_existing=True" in prompt
    assert "use_standard_library=True" in prompt
    assert "new_dependency_required=False" in prompt
    assert "abstraction_justified=False" in prompt


def test_final_generator_sends_quality_assessment_to_ai():

    generator, chat_service = create_generator()

    generator.generate(
        final_generation_request(),
    )

    prompt = chat_service.last_prompt

    assert (
        "COMPLEXITY AND IMPLEMENTATION-QUALITY ASSESSMENT"
        in prompt
    )
    assert "maintainability='high'" in prompt
    assert "over_engineering=False" in prompt


def test_final_generator_sends_optimization_decision_to_ai():

    generator, chat_service = create_generator()

    generator.generate(
        final_generation_request(),
    )

    prompt = chat_service.last_prompt

    assert "OPTIMIZATION DECISION" in prompt
    assert "optimization_justified=True" in prompt
    assert "primary_objective='runtime'" in prompt
    assert "measurement_required=True" in prompt


def test_final_generator_sends_candidate_changes_to_ai():

    generator, chat_service = create_generator()

    generator.generate(
        final_generation_request(),
    )

    prompt = chat_service.last_prompt

    assert "CANDIDATE IMPLEMENTATION" in prompt
    assert "backend/health.py" in prompt
    assert "return {'status': 'ok'}" in prompt


def test_final_generator_prompt_requires_optimization_to_be_justified():

    generator, chat_service = create_generator()

    generator.generate(
        final_generation_request(),
    )

    prompt = chat_service.last_prompt

    assert "Do not blindly optimize" in prompt
    assert "Do not perform speculative optimization" in prompt
    assert (
        "Apply optimization only when the optimization decision justifies it."
        in prompt
    )


def test_final_generator_prompt_forbids_invented_measurements():

    generator, chat_service = create_generator()

    generator.generate(
        final_generation_request(),
    )

    prompt = chat_service.last_prompt

    assert "Do not invent benchmark results." in prompt
    assert "Do not invent performance measurements." in prompt