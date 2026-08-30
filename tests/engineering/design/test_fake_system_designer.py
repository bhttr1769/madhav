from brain.engineering.design.fake_system_designer import (
    FakeSystemDesigner,
)

from brain.engineering.design.models.system_design import (
    SystemDesign,
)


def test_fake_system_designer_returns_result():

    design = SystemDesign(
        requirement=None,
        tasks=(),
        components=(),
        interfaces=(),
        dependencies=(),
        data_flows=(),
        constraints=frozenset(),
        decisions=frozenset(),
        acceptance_criteria=frozenset(),
    )

    designer = FakeSystemDesigner(
        result=design,
    )

    result = designer.design(
        task_decomposition=None,
    )

    assert result is design