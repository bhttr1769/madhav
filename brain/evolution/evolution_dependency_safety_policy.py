from brain.evolution.models.evolution_dependency_plan import (
    EvolutionDependencyPlan,
)
from brain.evolution.models.evolution_dependency_plan_operation import (
    EvolutionDependencyPlanOperation,
)
from brain.evolution.models.evolution_dependency_safety_result import (
    EvolutionDependencySafetyResult,
)
from brain.evolution.models.evolution_dependency_safety_status import (
    EvolutionDependencySafetyStatus,
)


class EvolutionDependencySafetyPolicy:
    """
    Enforces the safety boundary for dependency
    operations during evolution.

    Dependency resolution determines whether an
    operation can theoretically be performed.

    This policy determines whether that operation
    is permitted to proceed automatically.

    Dependency mutation is blocked by default.
    """

    def evaluate(
        self,
        plans: tuple[
            EvolutionDependencyPlan,
            ...,
        ],
    ) -> EvolutionDependencySafetyResult:
        if not isinstance(
            plans,
            tuple,
        ):
            raise TypeError(
                "plans must be a tuple"
            )

        for plan in plans:
            if not isinstance(
                plan,
                EvolutionDependencyPlan,
            ):
                raise TypeError(
                    "plans must contain only "
                    "EvolutionDependencyPlan instances"
                )

        if not plans:
            return EvolutionDependencySafetyResult(
                status=(
                    EvolutionDependencySafetyStatus.ALLOWED
                ),
                reason=(
                    "no dependency changes are "
                    "required"
                ),
            )

        for plan in plans:
            operation = plan.operation

            if (
                operation
                is EvolutionDependencyPlanOperation.BLOCKED
            ):
                return EvolutionDependencySafetyResult(
                    status=(
                        EvolutionDependencySafetyStatus.BLOCKED
                    ),
                    reason=(
                        "dependency plan is blocked: "
                        f"{plan.reason}"
                    ),
                )

            if (
                operation
                is EvolutionDependencyPlanOperation.ADD
            ):
                return EvolutionDependencySafetyResult(
                    status=(
                        EvolutionDependencySafetyStatus.BLOCKED
                    ),
                    reason=(
                        "dependency addition requires "
                        "explicit dependency mutation "
                        "authorization"
                    ),
                )

            if (
                operation
                is EvolutionDependencyPlanOperation.UPDATE
            ):
                return EvolutionDependencySafetyResult(
                    status=(
                        EvolutionDependencySafetyStatus.BLOCKED
                    ),
                    reason=(
                        "dependency update requires "
                        "explicit dependency mutation "
                        "authorization"
                    ),
                )

            if (
                operation
                is not EvolutionDependencyPlanOperation.NO_ACTION
            ):
                raise ValueError(
                    "unsupported dependency plan "
                    f"operation: {operation}"
                )

        return EvolutionDependencySafetyResult(
            status=(
                EvolutionDependencySafetyStatus.ALLOWED
            ),
            reason=(
                "all dependency plans require no "
                "environment mutation"
            ),
        )