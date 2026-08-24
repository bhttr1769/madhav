from brain.safety.logging.services.privacy_service import (
    PrivacyService,
)

from brain.safety.models.action import (
    Action,
)


def test_sensitive_metadata_is_redacted():

    service = PrivacyService()

    result = service.sanitize_metadata(
        {
            "username": "parth",
            "password": "secret123",
            "api_key": "abc123",
        }
    )

    assert (
        result["username"]
        == "parth"
    )

    assert (
        result["password"]
        == "[REDACTED]"
    )

    assert (
        result["api_key"]
        == "[REDACTED]"
    )


def test_nested_sensitive_metadata_is_redacted():

    service = PrivacyService()

    result = service.sanitize_metadata(
        {
            "connection": {
                "host": "localhost",
                "token": "secret-token",
            }
        }
    )

    assert (
        result["connection"]["host"]
        == "localhost"
    )

    assert (
        result["connection"]["token"]
        == "[REDACTED]"
    )


def test_sensitive_action_target_is_redacted():

    service = PrivacyService()

    action = Action(
        name="execute",
        category="command",
        target=(
            "login password=secret123"
        ),
    )

    result = service.sanitize_action(
        action,
    )

    assert (
        "secret123"
        not in result.target
    )

    assert (
        "[REDACTED]"
        in result.target
    )


def test_non_sensitive_action_is_preserved():

    service = PrivacyService()

    action = Action(
        name="execute",
        category="command",
        target="echo hello",
    )

    result = service.sanitize_action(
        action,
    )

    assert (
        result
        == action
    )