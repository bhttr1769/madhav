from brain.engineering.design.models.data_flow import (
    DataFlow,
)

from brain.engineering.design.models.design_component import (
    DesignComponent,
)

from brain.engineering.design.models.design_dependency import (
    DesignDependency,
)

from brain.engineering.design.models.design_interface import (
    DesignInterface,
)

from brain.engineering.design.models.system_design import (
    SystemDesign,
)

from brain.engineering.requirements.models.requirement import (
    Requirement,
)

from brain.engineering.tasks.models.task import (
    Task,
)


def requirement() -> Requirement:

    return Requirement(
        original_request="Build an authenticated API",
        objective="Build an authenticated API",
        functional_requirements=frozenset({
            "Users can authenticate",
        }),
        non_functional_requirements=frozenset({
            "Authentication must be secure",
        }),
        constraints=frozenset({
            "Use the existing backend",
        }),
        acceptance_criteria=frozenset({
            "Authenticated users can access protected resources",
        }),
        assumptions=frozenset(),
        ambiguities=frozenset(),
        affected_areas=frozenset({
            "backend",
            "authentication",
        }),
        confidence=0.95,
    )


def task() -> Task:

    return Task(
        id="task-1",
        description="Implement authentication",
        category="implementation",
        dependencies=frozenset(),
        affected_areas=frozenset({
            "authentication",
        }),
        acceptance_criteria=frozenset({
            "Users can authenticate",
        }),
    )


def component() -> DesignComponent:

    return DesignComponent(
        id="component-1",
        name="AuthenticationService",
        responsibility="Handles user authentication",
        layer="application",
        interfaces=frozenset({
            "interface-1",
        }),
    )


def interface() -> DesignInterface:

    return DesignInterface(
        id="interface-1",
        name="AuthenticationAPI",
        owner="AuthenticationService",
        consumers=frozenset({
            "APIController",
        }),
        purpose="Provides authentication operations",
    )


def dependency() -> DesignDependency:

    return DesignDependency(
        source="APIController",
        target="AuthenticationService",
        reason="Authentication is required for protected operations",
    )


def data_flow() -> DataFlow:

    return DataFlow(
        source="APIController",
        target="AuthenticationService",
        data="Authentication credentials",
    )


def test_system_design_stores_complete_design():

    req = requirement()
    task_value = task()

    design = SystemDesign(
        requirement=req,
        tasks=(task_value,),
        components=(component(),),
        interfaces=(interface(),),
        dependencies=(dependency(),),
        data_flows=(data_flow(),),
        constraints=frozenset({
            "Use the existing backend",
        }),
        decisions=frozenset({
            "Authentication is isolated in a dedicated service",
        }),
        acceptance_criteria=frozenset({
            "Authenticated users can access protected resources",
        }),
    )

    assert design.requirement == req

    assert design.tasks == (
        task_value,
    )

    assert design.components == (
        component(),
    )

    assert design.interfaces == (
        interface(),
    )

    assert design.dependencies == (
        dependency(),
    )

    assert design.data_flows == (
        data_flow(),
    )

    assert design.constraints == frozenset({
        "Use the existing backend",
    })

    assert design.decisions == frozenset({
        "Authentication is isolated in a dedicated service",
    })

    assert design.acceptance_criteria == frozenset({
        "Authenticated users can access protected resources",
    })


def test_system_design_is_frozen():

    design = SystemDesign(
        requirement=requirement(),
        tasks=(),
        components=(),
        interfaces=(),
        dependencies=(),
        data_flows=(),
        constraints=frozenset(),
        decisions=frozenset(),
        acceptance_criteria=frozenset(),
    )

    try:
        design.constraints = frozenset({
            "changed",
        })
    except AttributeError:
        pass
    else:
        raise AssertionError(
            "SystemDesign must be immutable"
        )