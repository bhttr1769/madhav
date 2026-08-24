from enum import Enum


class NodeType(Enum):
    """
    Defines the types of entities that can exist
    in the knowledge graph.
    """

    PROJECT = "project"

    REPOSITORY = "repository"

    DIRECTORY = "directory"

    FILE = "file"

    MODULE = "module"

    CLASS = "class"

    FUNCTION = "function"

    PACKAGE = "package"

    DEPENDENCY = "dependency"

    TECHNOLOGY = "technology"

    FRAMEWORK = "framework"

    ARCHITECTURE = "architecture"

    API = "api"