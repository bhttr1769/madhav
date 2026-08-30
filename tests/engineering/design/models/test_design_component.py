from brain.engineering.design.models.design_component import (
    DesignComponent,
)


def test_design_component_is_immutable():

    component = DesignComponent(
        id="component-1",
        name="AuthenticationService",
        responsibility="Handles user authentication",
        layer="application",
        interfaces=frozenset({
            "authentication-api",
        }),
    )

    assert component.id == "component-1"
    assert component.name == "AuthenticationService"
    assert component.responsibility == (
        "Handles user authentication"
    )
    assert component.layer == "application"
    assert component.interfaces == frozenset({
        "authentication-api",
    })


def test_design_component_is_frozen():

    component = DesignComponent(
        id="component-1",
        name="AuthenticationService",
        responsibility="Handles user authentication",
        layer="application",
        interfaces=frozenset(),
    )

    try:
        component.name = "Changed"
    except AttributeError:
        pass
    else:
        raise AssertionError(
            "DesignComponent must be immutable"
        )