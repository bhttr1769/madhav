from brain.factories.brain_factory import BrainFactory


def test_brain_end_to_end():

    brain = BrainFactory.create()

    brain.learn(
        "tests/models/sample.txt"
    )

    results = brain.search(
        "Hello"
    )

    assert len(results) > 0

    assert (
        results[0]
        .record
        .document_id
        == "sample.txt"
    )