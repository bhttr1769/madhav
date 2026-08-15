from brain.browser.pipelines.browser_learning_pipeline import (
    BrowserLearningPipeline,
)


def test_browser_learning_pipeline():

    result = (
        BrowserLearningPipeline()
    ).learn(
        "https://example.com",
    )

    assert len(
        result.text,
    ) > 0