from brain.engineering.design.models.design_interface import (
    DesignInterface,
)


def test_design_interface_stores_definition():

    interface = DesignInterface(
        id="interface-1",
        name="AuthenticationAPI",
        owner="AuthenticationService",
        consumers=frozenset({
            "UserService",
            "WebApplication",
        }),
        purpose="Provides authentication operations",
    )

    assert interface.id == "interface-1"

    assert interface.name == (
        "AuthenticationAPI"
    )

    assert interface.owner == (
        "AuthenticationService"
    )

    assert interface.consumers == frozenset({
        "UserService",
        "WebApplication",
    })

    assert interface.purpose == (
        "Provides authentication operations"
    )


def test_design_interface_is_frozen():

    interface = DesignInterface(
        id="interface-1",
        name="AuthenticationAPI",
        owner="AuthenticationService",
        consumers=frozenset(),
        purpose="Provides authentication operations",
    )

    try:
        interface.name = "Changed"
    except AttributeError:
        pass
    else:
        raise AssertionError(
            "DesignInterface must be immutable"
        )