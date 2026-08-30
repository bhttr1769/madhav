from brain.engineering.design.models.data_flow import (
    DataFlow,
)


def test_data_flow_stores_definition():

    flow = DataFlow(
        source="WebApplication",
        target="AuthenticationService",
        data="User credentials",
    )

    assert flow.source == (
        "WebApplication"
    )

    assert flow.target == (
        "AuthenticationService"
    )

    assert flow.data == (
        "User credentials"
    )


def test_data_flow_is_frozen():

    flow = DataFlow(
        source="WebApplication",
        target="AuthenticationService",
        data="User credentials",
    )

    try:
        flow.source = "Changed"
    except AttributeError:
        pass
    else:
        raise AssertionError(
            "DataFlow must be immutable"
        )