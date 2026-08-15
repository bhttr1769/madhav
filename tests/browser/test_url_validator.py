from brain.browser.url_validator import (
    UrlValidator,
)


def test_valid_url():

    validator = UrlValidator()

    assert validator.is_valid(
        "https://spring.io"
    )


def test_url_normalization():

    validator = UrlValidator()

    assert (
        validator.normalize(
            "spring.io"
        )
        == "https://spring.io"
    )


def test_invalid_url():

    validator = UrlValidator()

    assert not validator.is_valid(
        ""
    )