from brain.evolution.evolution_id_generator import (
    EvolutionIdGenerator,
)


def test_generator_creates_evolution_id():
    generator = EvolutionIdGenerator()

    evolution_id = generator.generate()

    assert isinstance(
        evolution_id,
        str,
    )

    assert evolution_id.startswith(
        "evo-"
    )


def test_generator_creates_unique_ids():
    generator = EvolutionIdGenerator()

    first = generator.generate()
    second = generator.generate()

    assert first != second


def test_generated_ids_have_expected_format():
    generator = EvolutionIdGenerator()

    evolution_id = generator.generate()

    assert evolution_id.startswith(
        "evo-"
    )

    assert len(evolution_id) == 36