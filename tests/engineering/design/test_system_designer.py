from brain.engineering.design.system_designer import (
    SystemDesigner,
)


def test_system_designer_is_interface():

    assert SystemDesigner.__abstractmethods__ == {
        "design",
    }