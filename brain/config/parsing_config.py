from dataclasses import dataclass

from brain.config.base_config import BaseConfig


@dataclass(frozen=True)
class ParsingConfig(BaseConfig):
    """
    Configuration for parsing.
    """

    reading_speed_wpm: int = 200
