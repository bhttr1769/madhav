from typing import Any

from brain.engineering.optimization.models.optimization_decision import (
    OptimizationDecision,
)
from brain.engineering.optimization.models.optimization_decision_request import (
    OptimizationDecisionRequest,
)
from brain.engineering.optimization.optimization_decision_analyzer import (
    OptimizationDecisionAnalyzer,
)


class AIOptimizationDecisionAnalyzer(OptimizationDecisionAnalyzer):
    """
    AI-backed analyzer for optimization decisions.

    The analyzer determines whether optimization is justified and,
    if justified, what optimization direction is appropriate.

    It does not generate code, modify files, benchmark implementations,
    install dependencies, or perform optimization itself.
    """

    _REQUIRED_FIELDS = frozenset(
        {
            "optimization_justified",
            "primary_objective",
            "optimization_scope",
            "bottleneck",
            "strategies",
            "avoid_strategies",
            "trade_offs",
            "measurement_required",
            "rationale",
        }
    )

    _ALLOWED_OBJECTIVES = frozenset(
        {
            "runtime",
            "memory",
            "io",
            "database",
            "network",
            "concurrency",
            "startup",
            "dependency_overhead",
            "maintainability",
            "balanced",
            "none",
        }
    )

    def __init__(self, chat_service: Any):
        if chat_service is None or not callable(
            getattr(chat_service, "chat", None)
        ):
            raise TypeError(
                "chat_service must provide a callable chat method"
            )

        self._chat_service = chat_service

    def analyze(
        self,
        request: OptimizationDecisionRequest,
    ) -> OptimizationDecision:
        if not isinstance(request, OptimizationDecisionRequest):
            raise TypeError(
                "request must be an OptimizationDecisionRequest"
            )

        response = self._chat_service.chat(
            self._build_prompt(request)
        )

        payload = self._extract_payload(response)

        return self._build_decision(payload)

    def _build_prompt(
        self,
        request: OptimizationDecisionRequest,
    ) -> str:
        return f"""
You are Madhav's engineering optimization decision analyzer.

Your responsibility is to determine whether optimization of a proposed
implementation is justified and, if so, what optimization direction
is justified by the available engineering evidence.

You are making an ENGINEERING DECISION, not implementing the optimization.

ENGINEERING CONTEXT

Task:
{request.task!r}

System design:
{request.design!r}

Engineering plan:
{request.plan!r}

Necessity and reuse decision:
{request.engineering_decision!r}

Complexity and implementation-quality assessment:
{request.quality_assessment!r}

Existing code structure:
{request.existing_code!r}

Proposed code changes:
{request.proposed_changes!r}

DECISION RULES

1. Do not assume optimization is necessary merely because optimization
   is possible.

2. Optimization must be justified by the task, design, existing code,
   proposed changes, or quality assessment.

3. Prefer simple, measurable, evidence-based optimization.

4. Do not recommend speculative micro-optimizations without a credible
   engineering reason.

5. Do not sacrifice correctness, clarity, maintainability, testability,
   or architectural integrity for insignificant performance gains.

6. Do not recommend premature optimization when measurement is required
   to establish whether a real bottleneck exists.

7. Distinguish between:
   - an actual bottleneck,
   - a credible performance risk,
   - and an optimization opportunity with no demonstrated need.

8. If optimization is not justified:
   - optimization_justified must be false;
   - primary_objective must be "none";
   - strategies must be empty;
   - clearly explain why optimization should not be pursued.

9. If optimization is justified:
   - identify one primary objective;
   - identify the optimization scope;
   - identify the relevant bottleneck or performance risk;
   - provide concrete optimization strategies;
   - identify strategies that should be avoided;
   - explain the engineering trade-offs;
   - state whether measurement is required.

10. Optimization strategies must remain at the decision level.
    Do not generate source code, patches, algorithms, commands,
    file contents, or implementation steps.

11. Do not modify or rewrite the proposed changes.

12. Do not generate tests.

13. Do not install or introduce dependencies.

14. Do not perform repository-wide refactoring.

15. Do not perform benchmarking or claim measured performance unless
    measurement evidence is explicitly present in the supplied context.

16. Remain language-agnostic. Base decisions on engineering properties,
    not assumptions about a particular programming language.

17. Return ONLY valid JSON.

The JSON object must contain exactly these fields:

{{
  "optimization_justified": true,
  "primary_objective": "runtime",
  "optimization_scope": "specific scope",
  "bottleneck": "identified bottleneck or risk",
  "strategies": [
    "strategy"
  ],
  "avoid_strategies": [
    "strategy"
  ],
  "trade_offs": [
    "trade-off"
  ],
  "measurement_required": true,
  "rationale": [
    "reason"
  ]
}}

Allowed primary_objective values:

{sorted(self._ALLOWED_OBJECTIVES)}

Use "none" when optimization is not justified.
""".strip()

    @staticmethod
    def _extract_payload(response: Any) -> dict[str, Any]:
        if isinstance(response, dict):
            payload = response
        elif isinstance(response, str):
            import json

            try:
                payload = json.loads(response)
            except json.JSONDecodeError as exc:
                raise ValueError(
                    "AI response must contain valid JSON"
                ) from exc
        else:
            raise ValueError(
                "AI response must be a JSON object or JSON string"
            )

        if not isinstance(payload, dict):
            raise ValueError(
                "AI response must decode to a JSON object"
            )

        return payload

    def _build_decision(
        self,
        payload: dict[str, Any],
    ) -> OptimizationDecision:
        if set(payload) != self._REQUIRED_FIELDS:
            raise ValueError(
                "AI response must contain exactly the required "
                "optimization decision fields"
            )

        optimization_justified = payload["optimization_justified"]
        measurement_required = payload["measurement_required"]

        if not isinstance(optimization_justified, bool):
            raise ValueError(
                "optimization_justified must be a boolean"
            )

        if not isinstance(measurement_required, bool):
            raise ValueError(
                "measurement_required must be a boolean"
            )

        primary_objective = payload["primary_objective"]

        if (
            not isinstance(primary_objective, str)
            or primary_objective not in self._ALLOWED_OBJECTIVES
        ):
            raise ValueError(
                "primary_objective must be one of the allowed values"
            )

        optimization_scope = self._validate_string(
            payload["optimization_scope"],
            "optimization_scope",
        )

        bottleneck = self._validate_string(
            payload["bottleneck"],
            "bottleneck",
        )

        strategies = self._validate_string_list(
            payload["strategies"],
            "strategies",
        )

        avoid_strategies = self._validate_string_list(
            payload["avoid_strategies"],
            "avoid_strategies",
        )

        trade_offs = self._validate_string_list(
            payload["trade_offs"],
            "trade_offs",
        )

        rationale = self._validate_string_list(
            payload["rationale"],
            "rationale",
        )

        if not optimization_justified:
            if primary_objective != "none":
                raise ValueError(
                    "primary_objective must be 'none' when optimization "
                    "is not justified"
                )

            if strategies:
                raise ValueError(
                    "strategies must be empty when optimization "
                    "is not justified"
                )

        else:
            if primary_objective == "none":
                raise ValueError(
                    "primary_objective cannot be 'none' when optimization "
                    "is justified"
                )

            if not strategies:
                raise ValueError(
                    "strategies must not be empty when optimization "
                    "is justified"
                )

        return OptimizationDecision(
            optimization_justified=optimization_justified,
            primary_objective=primary_objective,
            optimization_scope=optimization_scope,
            bottleneck=bottleneck,
            strategies=tuple(strategies),
            avoid_strategies=tuple(avoid_strategies),
            trade_offs=tuple(trade_offs),
            measurement_required=measurement_required,
            rationale=tuple(rationale),
        )

    @staticmethod
    def _validate_string(
        value: Any,
        field_name: str,
    ) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError(
                f"{field_name} must be a non-empty string"
            )

        return value.strip()

    @classmethod
    def _validate_string_list(
        cls,
        value: Any,
        field_name: str,
    ) -> list[str]:
        if not isinstance(value, list):
            raise ValueError(
                f"{field_name} must be a list"
            )

        validated: list[str] = []

        for item in value:
            validated.append(
                cls._validate_string(item, field_name)
            )

        return validated