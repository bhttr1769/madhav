from brain.engineering.analysis.complexity_quality_analyzer import (
    ComplexityQualityAnalyzer,
)

from brain.engineering.analysis.models.analysis_request import (
    AnalysisRequest,
)

from brain.engineering.analysis.models.complexity_quality_request import (
    ComplexityQualityRequest,
)

from brain.engineering.analysis.necessity_reuse_analyzer import (
    NecessityReuseAnalyzer,
)

from brain.engineering.generation.code_generator import (
    CodeGenerator,
)

from brain.engineering.generation.engineering_generation import (
    EngineeringGeneration,
)

from brain.engineering.generation.final_code_generator import (
    FinalCodeGenerator,
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

from brain.engineering.optimization.models.optimization_decision_request import (
    OptimizationDecisionRequest,
)

from brain.engineering.optimization.optimization_decision_analyzer import (
    OptimizationDecisionAnalyzer,
)


class AIEngineeringGeneration(
    EngineeringGeneration,
):
    """
    Orchestrates the complete engineering generation workflow.

    The workflow performs necessity and reuse analysis, generates a
    candidate implementation, evaluates its complexity and quality,
    determines whether optimization is justified, and finally
    generates the implementation that incorporates the resulting
    engineering decisions.
    """

    def __init__(
        self,
        necessity_reuse_analyzer: NecessityReuseAnalyzer,
        code_generator: CodeGenerator,
        complexity_quality_analyzer: ComplexityQualityAnalyzer,
        optimization_decision_analyzer: OptimizationDecisionAnalyzer,
        final_code_generator: FinalCodeGenerator,
    ):
        if not isinstance(
            necessity_reuse_analyzer,
            NecessityReuseAnalyzer,
        ):
            raise TypeError(
                "necessity_reuse_analyzer must be a NecessityReuseAnalyzer"
            )

        if not isinstance(
            code_generator,
            CodeGenerator,
        ):
            raise TypeError(
                "code_generator must be a CodeGenerator"
            )

        if not isinstance(
            complexity_quality_analyzer,
            ComplexityQualityAnalyzer,
        ):
            raise TypeError(
                "complexity_quality_analyzer must be a ComplexityQualityAnalyzer"
            )

        if not isinstance(
            optimization_decision_analyzer,
            OptimizationDecisionAnalyzer,
        ):
            raise TypeError(
                "optimization_decision_analyzer must be an OptimizationDecisionAnalyzer"
            )

        if not isinstance(
            final_code_generator,
            FinalCodeGenerator,
        ):
            raise TypeError(
                "final_code_generator must be a FinalCodeGenerator"
            )

        self._necessity_reuse_analyzer = (
            necessity_reuse_analyzer
        )

        self._code_generator = (
            code_generator
        )

        self._complexity_quality_analyzer = (
            complexity_quality_analyzer
        )

        self._optimization_decision_analyzer = (
            optimization_decision_analyzer
        )

        self._final_code_generator = (
            final_code_generator
        )

    def generate(
        self,
        request: EngineeringGenerationRequest,
    ) -> EngineeringGenerationResult:

        if not isinstance(
            request,
            EngineeringGenerationRequest,
        ):
            raise TypeError(
                "request must be an EngineeringGenerationRequest"
            )

        engineering_decision = (
            self._necessity_reuse_analyzer.analyze(
                AnalysisRequest(
                    task=request.task,
                    design=request.design,
                    plan=request.plan,
                    existing_code=request.existing_code,
                ),
            )
        )

        candidate_result = (
            self._code_generator.generate(
                GenerationRequest(
                    task=request.task,
                    design=request.design,
                    plan=request.plan,
                ),
            )
        )

        quality_assessment = (
            self._complexity_quality_analyzer.analyze(
                ComplexityQualityRequest(
                    task=request.task,
                    design=request.design,
                    plan=request.plan,
                    engineering_decision=engineering_decision,
                    existing_code=request.existing_code,
                    proposed_changes=candidate_result.changes,
                ),
            )
        )

        optimization_decision = (
            self._optimization_decision_analyzer.analyze(
                OptimizationDecisionRequest(
                    task=request.task,
                    design=request.design,
                    plan=request.plan,
                    engineering_decision=engineering_decision,
                    quality_assessment=quality_assessment,
                    existing_code=request.existing_code,
                    proposed_changes=candidate_result.changes,
                ),
            )
        )

        final_result = (
            self._final_code_generator.generate(
                FinalGenerationRequest(
                    task=request.task,
                    design=request.design,
                    plan=request.plan,
                    existing_code=request.existing_code,
                    engineering_decision=engineering_decision,
                    quality_assessment=quality_assessment,
                    optimization_decision=optimization_decision,
                    proposed_changes=candidate_result.changes,
                ),
            )
        )

        return EngineeringGenerationResult(
            changes=final_result.changes,
            engineering_decision=engineering_decision,
            quality_assessment=quality_assessment,
            optimization_decision=optimization_decision,
        )