from dataclasses import dataclass

from brain.engineering.requirements.models.requirement import (
    Requirement,
)

from brain.engineering.tasks.models.task import (
    Task,
)

from brain.engineering.design.models.design_component import (
    DesignComponent,
)

from brain.engineering.design.models.design_interface import (
    DesignInterface,
)

from brain.engineering.design.models.design_dependency import (
    DesignDependency,
)

from brain.engineering.design.models.data_flow import (
    DataFlow,
)


@dataclass(frozen=True)
class SystemDesign:
    """
    Represents a proposed system architecture derived
    from an engineering requirement and its tasks.
    """

    requirement: Requirement

    tasks: tuple[Task, ...]

    components: tuple[DesignComponent, ...]

    interfaces: tuple[DesignInterface, ...]

    dependencies: tuple[DesignDependency, ...]

    data_flows: tuple[DataFlow, ...]

    constraints: frozenset[str]

    decisions: frozenset[str]

    acceptance_criteria: frozenset[str]