from brain.evolution.evolution_policy import EvolutionPolicy
from brain.evolution.models.evolution_mode import EvolutionMode


def test_proposal_cannot_implement():
    policy = EvolutionPolicy()

    assert not policy.allows_implementation(
        EvolutionMode.PROPOSAL
    )


def test_supervised_can_implement():
    policy = EvolutionPolicy()

    assert policy.allows_implementation(
        EvolutionMode.SUPERVISED
    )


def test_autonomous_can_implement():
    policy = EvolutionPolicy()

    assert policy.allows_implementation(
        EvolutionMode.AUTONOMOUS
    )


def test_proposal_cannot_verify():
    policy = EvolutionPolicy()

    assert not policy.allows_verification(
        EvolutionMode.PROPOSAL
    )


def test_supervised_can_verify():
    policy = EvolutionPolicy()

    assert policy.allows_verification(
        EvolutionMode.SUPERVISED
    )


def test_autonomous_can_verify():
    policy = EvolutionPolicy()

    assert policy.allows_verification(
        EvolutionMode.AUTONOMOUS
    )


def test_only_autonomous_can_integrate():
    policy = EvolutionPolicy()

    assert not policy.allows_integration(
        EvolutionMode.PROPOSAL
    )

    assert not policy.allows_integration(
        EvolutionMode.SUPERVISED
    )

    assert policy.allows_integration(
        EvolutionMode.AUTONOMOUS
    )


def test_policy_rejects_invalid_mode():
    policy = EvolutionPolicy()

    try:
        policy.allows_implementation("invalid")
    except TypeError:
        pass
    else:
        raise AssertionError(
            "expected TypeError"
        )
