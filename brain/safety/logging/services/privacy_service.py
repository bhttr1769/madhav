from typing import Any

from brain.safety.models.action import (
    Action,
)


class PrivacyService:
    """
    Sanitizes sensitive information before
    it is written to the action log.
    """

    SENSITIVE_KEYS = {
        "password",
        "passwd",
        "secret",
        "token",
        "api_key",
        "apikey",
        "access_token",
        "refresh_token",
        "authorization",
        "cookie",
    }

    REDACTED = "[REDACTED]"

    def sanitize_action(
        self,
        action: Action,
    ) -> Action:

        target = self.sanitize_text(
            action.target,
        )

        return Action(
            name=action.name,
            category=action.category,
            target=target,
        )

    def sanitize_metadata(
        self,
        metadata: dict[str, Any],
    ) -> dict[str, Any]:

        return {
            key: (
                self.REDACTED
                if self.is_sensitive_key(key)
                else self.sanitize_value(value)
            )
            for key, value in metadata.items()
        }

    def sanitize_value(
        self,
        value: Any,
    ) -> Any:

        if isinstance(
            value,
            str,
        ):

            return self.sanitize_text(
                value,
            )

        if isinstance(
            value,
            dict,
        ):

            return self.sanitize_metadata(
                value,
            )

        if isinstance(
            value,
            list,
        ):

            return [
                self.sanitize_value(
                    item,
                )
                for item in value
            ]

        return value

    def sanitize_text(
        self,
        text: str,
    ) -> str:

        result = text

        for key in self.SENSITIVE_KEYS:

            patterns = [
                f"{key}=",
                f"{key}:",
            ]

            for pattern in patterns:

                result = self._redact_after_separator(
                    result,
                    pattern,
                )

        return result

    def _redact_after_separator(
        self,
        text: str,
        pattern: str,
    ) -> str:

        lower_text = text.lower()
        lower_pattern = pattern.lower()

        start = lower_text.find(
            lower_pattern,
        )

        if start == -1:
            return text

        value_start = (
            start
            + len(pattern)
        )

        value_end = len(text)

        for separator in [
            " ",
            "&",
            ",",
        ]:

            position = text.find(
                separator,
                value_start,
            )

            if (
                position != -1
                and position < value_end
            ):

                value_end = position

        return (
            text[:value_start]
            + self.REDACTED
            + text[value_end:]
        )

    def is_sensitive_key(
        self,
        key: str,
    ) -> bool:

        normalized = (
            key.lower()
            .strip()
        )

        return (
            normalized
            in self.SENSITIVE_KEYS
        )