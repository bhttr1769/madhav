from enum import Enum


class ContextSource(str, Enum):
    USER = "user"
    PROJECT = "project"
    ENVIRONMENT = "environment"
    MEMORY = "memory"
    KNOWLEDGE = "knowledge"
    PERCEPTION = "perception"
    RUNTIME = "runtime"