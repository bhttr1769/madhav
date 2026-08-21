from brain.safety.models.risk import (
    Risk,
)


def test_risk():

    assert (
        Risk.SAFE.value
        == 0
    )

    assert (
        Risk.LOW.value
        == 1
    )

    assert (
        Risk.MEDIUM.value
        == 2
    )

    assert (
        Risk.HIGH.value
        == 3
    )

    assert (
        Risk.CRITICAL.value
        == 4
    )