from dataclasses import dataclass


@dataclass(frozen=True)
class OptimizationDecision:
    """
    Represents the engineering decision regarding optimization
    of a proposed implementation.
    """

    optimization_justified: bool
    primary_objective: str
    optimization_scope: str
    bottleneck: str
    strategies: tuple[str, ...]
    avoid_strategies: tuple[str, ...]
    trade_offs: tuple[str, ...]
    measurement_required: bool
    rationale: tuple[str, ...]