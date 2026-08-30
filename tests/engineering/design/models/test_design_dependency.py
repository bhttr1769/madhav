from brain.engineering.design.models.design_dependency import (
    DesignDependency,
)


def test_design_dependency_stores_definition():

    dependency = DesignDependency(
        source="WebApplication",
        target="AuthenticationService",
        reason="Authentication is required before accessing protected resources",
    )

    assert dependency.source == (
        "WebApplication"
    )

    assert dependency.target == (
        "AuthenticationService"
    )

    assert dependency.reason == (
        "Authentication is required before accessing protected resources"
    )


def test_design_dependency_is_frozen():

    dependency = DesignDependency(
        source="WebApplication",
        target="AuthenticationService",
        reason="Authentication is required",
    )

    try:
        dependency.source = "Changed"
    except AttributeError:
        pass
    else:
        raise AssertionError(
            "DesignDependency must be immutable"
        )