from brain.workspace.detectors.language_detector import (
    LanguageDetector,
)

from brain.workspace.plugins.languages.fake_language_detector import (
    FakeLanguageDetector,
)

from brain.workspace.registries.detector_registry import (
    DetectorRegistry,
)


def test_language_detector():

    registry = DetectorRegistry()

    registry.register(
        FakeLanguageDetector(),
    )

    technologies = (
        LanguageDetector(
            registry,
        )
    ).detect(
        set(),
    )

    assert len(
        technologies
    ) == 1

    assert next(
        iter(
            technologies,
        )
    ).name == "FakeLanguage"