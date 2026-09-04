import pytest

from brain.code.models.code_structure import (
    CodeStructure,
)

from brain.engineering.analysis.complexity_quality_analyzer import (
    ComplexityQualityAnalyzer,
)

from brain.engineering.analysis.models.analysis_request import (
    AnalysisRequest,
)

from brain.engineering.analysis.models.complexity_quality_request import (
    ComplexityQualityRequest,
)

from brain.engineering.analysis.models.engineering_quality_assessment import (
    EngineeringQualityAssessment,
)

from brain.engineering.analysis.necessity_reuse_analyzer import (
    NecessityReuseAnalyzer,
)

from brain.engineering.design.models.system_design import (
    SystemDesign,
)

from brain.engineering.generation.ai_engineering_generation import (
    AIEngineeringGeneration,
)

from brain.engineering.generation.code_generator import (
    CodeGenerator,
)

from brain.engineering.generation.final_code_generator import (
    FinalCodeGenerator,
)

from brain.engineering.generation.models.code_change import (
    CodeChange,
)

from brain.engineering.generation.models.engineering_decision import (
    EngineeringDecision,
)

from brain.engineering.generation.models.engineering_generation_request import (
    EngineeringGenerationRequest,
)

from brain.engineering.generation.models.engineering_generation_result import (
    EngineeringGenerationResult,
)

from brain.engineering.generation.models.final_generation_request import (
    FinalGenerationRequest,
)

from brain.engineering.generation.models.generation_request import (
    GenerationRequest,
)

from brain.engineering.generation.models.generation_result import (
    GenerationResult,
)

from brain.engineering.optimization.models.optimization_decision import (
    OptimizationDecision,
)

from brain.engineering.optimization.models.optimization_decision_request import (
    OptimizationDecisionRequest,
)

from brain.engineering.optimization.optimization_decision_analyzer import (
    OptimizationDecisionAnalyzer,
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


def request() -> EngineeringGenerationRequest:

    return EngineeringGenerationRequest(
        task=task(),
        design=design(),
        plan=plan(),
        existing_code=existing_code(),
    )


def engineering_decision() -> EngineeringDecision:

    return EngineeringDecision(
        necessity="Implementation is required.",
        reuse_existing=True,
        use_standard_library=True,
        use_existing_dependency=False,
        new_dependency_required=False,
        abstraction_justified=False,
        optimization_justified=False,
        rationale=(
            "The existing backend should be reused.",
        ),
    )


def candidate_decision() -> EngineeringDecision:

    return EngineeringDecision(
        necessity="Candidate decision.",
        reuse_existing=False,
        use_standard_library=False,
        use_existing_dependency=False,
        new_dependency_required=True,
        abstraction_justified=True,
        optimization_justified=True,
        rationale=(
            "This decision must not become authoritative.",
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
            "Simple implementation.",
        ),
        recommendations=(
            "Preserve the current structure.",
        ),
        rationale=(
            "The candidate is simple.",
        ),
    )


def optimization_decision() -> OptimizationDecision:

    return OptimizationDecision(
        optimization_justified=False,
        primary_objective="none",
        optimization_scope="none",
        bottleneck="none",
        strategies=(),
        avoid_strategies=(
            "speculative optimization",
        ),
        trade_offs=(),
        measurement_required=False,
        rationale=(
            "No optimization is justified.",
        ),
    )


def changes() -> tuple[CodeChange, ...]:

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


class FakeNecessityReuseAnalyzer(
    NecessityReuseAnalyzer,
):

    def __init__(
        self,
        decision: EngineeringDecision,
        events: list[str],
    ):
        self.decision = decision
        self.events = events
        self.last_request = None

    def analyze(
        self,
        request: AnalysisRequest,
    ) -> EngineeringDecision:

        self.events.append(
            "necessity",
        )

        self.last_request = request

        return self.decision


class FakeCodeGenerator(
    CodeGenerator,
):

    def __init__(
        self,
        result: GenerationResult,
        events: list[str],
    ):
        self.result = result
        self.events = events
        self.last_request = None

    def generate(
        self,
        request: GenerationRequest,
    ) -> GenerationResult:

        self.events.append(
            "candidate",
        )

        self.last_request = request

        return self.result


class FakeComplexityQualityAnalyzer(
    ComplexityQualityAnalyzer,
):

    def __init__(
        self,
        assessment: EngineeringQualityAssessment,
        events: list[str],
    ):
        self.assessment = assessment
        self.events = events
        self.last_request = None

    def analyze(
        self,
        request: ComplexityQualityRequest,
    ) -> EngineeringQualityAssessment:

        self.events.append(
            "quality",
        )

        self.last_request = request

        return self.assessment


class FakeOptimizationDecisionAnalyzer(
    OptimizationDecisionAnalyzer,
):

    def __init__(
        self,
        decision: OptimizationDecision,
        events: list[str],
    ):
        self.decision = decision
        self.events = events
        self.last_request = None

    def analyze(
        self,
        request: OptimizationDecisionRequest,
    ) -> OptimizationDecision:

        self.events.append(
            "optimization",
        )

        self.last_request = request

        return self.decision


class FakeFinalCodeGenerator(
    FinalCodeGenerator,
):

    def __init__(
        self,
        result: GenerationResult,
        events: list[str],
    ):
        self.result = result
        self.events = events
        self.last_request = None

    def generate(
        self,
        request: FinalGenerationRequest,
    ) -> GenerationResult:

        self.events.append(
            "final",
        )

        self.last_request = request

        return self.result


def create_generation():

    events = []

    necessity = FakeNecessityReuseAnalyzer(
        engineering_decision(),
        events,
    )

    candidate = FakeCodeGenerator(
        GenerationResult(
            changes=changes(),
            decision=candidate_decision(),
        ),
        events,
    )

    quality = FakeComplexityQualityAnalyzer(
        quality_assessment(),
        events,
    )

    optimization = FakeOptimizationDecisionAnalyzer(
        optimization_decision(),
        events,
    )

    final = FakeFinalCodeGenerator(
        GenerationResult(
            changes=changes(),
            decision=candidate_decision(),
        ),
        events,
    )

    generation = AIEngineeringGeneration(
        necessity_reuse_analyzer=necessity,
        code_generator=candidate,
        complexity_quality_analyzer=quality,
        optimization_decision_analyzer=optimization,
        final_code_generator=final,
    )

    return (
        generation,
        necessity,
        candidate,
        quality,
        optimization,
        final,
        events,
    )


def test_engineering_generation_produces_result():

    generation, *_ = create_generation()

    result = generation.generate(
        request(),
    )

    assert isinstance(
        result,
        EngineeringGenerationResult,
    )


def test_engineering_generation_executes_stages_in_order():

    generation, *rest = create_generation()

    events = rest[-1]

    generation.generate(
        request(),
    )

    assert events == [
        "necessity",
        "candidate",
        "quality",
        "optimization",
        "final",
    ]


def test_engineering_generation_returns_final_changes():

    generation, *_ = create_generation()

    result = generation.generate(
        request(),
    )

    assert result.changes == changes()


def test_engineering_generation_returns_authoritative_engineering_decision():

    generation, necessity, *_ = create_generation()

    result = generation.generate(
        request(),
    )

    assert result.engineering_decision is (
        necessity.decision
    )


def test_candidate_decision_is_not_authoritative():

    generation, necessity, candidate, *_ = create_generation()

    result = generation.generate(
        request(),
    )

    assert result.engineering_decision is (
        necessity.decision
    )

    assert result.engineering_decision != (
        candidate.result.decision
    )


def test_necessity_request_contains_complete_context():

    generation, necessity, *_ = create_generation()

    generation.generate(
        request(),
    )

    assert necessity.last_request == AnalysisRequest(
        task=task(),
        design=design(),
        plan=plan(),
        existing_code=existing_code(),
    )


def test_candidate_generation_receives_generation_request():

    generation, _, candidate, *_ = create_generation()

    generation.generate(
        request(),
    )

    assert candidate.last_request == GenerationRequest(
        task=task(),
        design=design(),
        plan=plan(),
    )


def test_quality_analysis_receives_authoritative_decision():

    generation, necessity, _, quality, *_ = create_generation()

    generation.generate(
        request(),
    )

    assert quality.last_request.engineering_decision is (
        necessity.decision
    )


def test_quality_analysis_receives_candidate_changes():

    generation, _, candidate, quality, *_ = create_generation()

    generation.generate(
        request(),
    )

    assert quality.last_request.proposed_changes == (
        candidate.result.changes
    )


def test_optimization_analysis_receives_quality_assessment():

    generation, _, _, quality, optimization, *_ = (
        create_generation()
    )

    generation.generate(
        request(),
    )

    assert optimization.last_request.quality_assessment is (
        quality.assessment
    )


def test_optimization_analysis_receives_candidate_changes():

    generation, _, candidate, _, optimization, *_ = (
        create_generation()
    )

    generation.generate(
        request(),
    )

    assert optimization.last_request.proposed_changes == (
        candidate.result.changes
    )


def test_final_generation_receives_authoritative_decision():

    generation, necessity, _, _, _, final, _ = (
        create_generation()
    )

    generation.generate(
        request(),
    )

    assert final.last_request.engineering_decision is (
        necessity.decision
    )


def test_final_generation_receives_quality_assessment():

    generation, _, _, quality, _, final, _ = (
        create_generation()
    )

    generation.generate(
        request(),
    )

    assert final.last_request.quality_assessment is (
        quality.assessment
    )


def test_final_generation_receives_optimization_decision():

    generation, _, _, _, optimization, final, _ = (
        create_generation()
    )

    generation.generate(
        request(),
    )

    assert final.last_request.optimization_decision is (
        optimization.decision
    )


def test_final_generation_receives_candidate_changes():

    generation, _, candidate, _, _, final, _ = (
        create_generation()
    )

    generation.generate(
        request(),
    )

    assert final.last_request.proposed_changes == (
        candidate.result.changes
    )


def test_final_generation_receives_existing_code():

    generation, _, _, _, _, final, _ = (
        create_generation()
    )

    engineering_request = request()

    generation.generate(
        engineering_request,
    )

    assert final.last_request.existing_code is (
        engineering_request.existing_code
    )


def test_engineering_generation_rejects_invalid_request():

    generation, *_ = create_generation()

    with pytest.raises(TypeError):

        generation.generate(
            object(),
        )


def test_engineering_generation_requires_necessity_analyzer():

    events = []

    with pytest.raises(TypeError):

        AIEngineeringGeneration(
            necessity_reuse_analyzer=object(),
            code_generator=FakeCodeGenerator(
                GenerationResult(
                    changes=changes(),
                    decision=candidate_decision(),
                ),
                events,
            ),
            complexity_quality_analyzer=FakeComplexityQualityAnalyzer(
                quality_assessment(),
                events,
            ),
            optimization_decision_analyzer=FakeOptimizationDecisionAnalyzer(
                optimization_decision(),
                events,
            ),
            final_code_generator=FakeFinalCodeGenerator(
                GenerationResult(
                    changes=changes(),
                    decision=candidate_decision(),
                ),
                events,
            ),
        )


def test_engineering_generation_requires_code_generator():

    events = []

    with pytest.raises(TypeError):

        AIEngineeringGeneration(
            necessity_reuse_analyzer=FakeNecessityReuseAnalyzer(
                engineering_decision(),
                events,
            ),
            code_generator=object(),
            complexity_quality_analyzer=FakeComplexityQualityAnalyzer(
                quality_assessment(),
                events,
            ),
            optimization_decision_analyzer=FakeOptimizationDecisionAnalyzer(
                optimization_decision(),
                events,
            ),
            final_code_generator=FakeFinalCodeGenerator(
                GenerationResult(
                    changes=changes(),
                    decision=candidate_decision(),
                ),
                events,
            ),
        )


def test_engineering_generation_requires_quality_analyzer():

    events = []

    with pytest.raises(TypeError):

        AIEngineeringGeneration(
            necessity_reuse_analyzer=FakeNecessityReuseAnalyzer(
                engineering_decision(),
                events,
            ),
            code_generator=FakeCodeGenerator(
                GenerationResult(
                    changes=changes(),
                    decision=candidate_decision(),
                ),
                events,
            ),
            complexity_quality_analyzer=object(),
            optimization_decision_analyzer=FakeOptimizationDecisionAnalyzer(
                optimization_decision(),
                events,
            ),
            final_code_generator=FakeFinalCodeGenerator(
                GenerationResult(
                    changes=changes(),
                    decision=candidate_decision(),
                ),
                events,
            ),
        )


def test_engineering_generation_requires_optimization_analyzer():

    events = []

    with pytest.raises(TypeError):

        AIEngineeringGeneration(
            necessity_reuse_analyzer=FakeNecessityReuseAnalyzer(
                engineering_decision(),
                events,
            ),
            code_generator=FakeCodeGenerator(
                GenerationResult(
                    changes=changes(),
                    decision=candidate_decision(),
                ),
                events,
            ),
            complexity_quality_analyzer=FakeComplexityQualityAnalyzer(
                quality_assessment(),
                events,
            ),
            optimization_decision_analyzer=object(),
            final_code_generator=FakeFinalCodeGenerator(
                GenerationResult(
                    changes=changes(),
                    decision=candidate_decision(),
                ),
                events,
            ),
        )


def test_engineering_generation_requires_final_generator():

    events = []

    with pytest.raises(TypeError):

        AIEngineeringGeneration(
            necessity_reuse_analyzer=FakeNecessityReuseAnalyzer(
                engineering_decision(),
                events,
            ),
            code_generator=FakeCodeGenerator(
                GenerationResult(
                    changes=changes(),
                    decision=candidate_decision(),
                ),
                events,
            ),
            complexity_quality_analyzer=FakeComplexityQualityAnalyzer(
                quality_assessment(),
                events,
            ),
            optimization_decision_analyzer=FakeOptimizationDecisionAnalyzer(
                optimization_decision(),
                events,
            ),
            final_code_generator=object(),
        )