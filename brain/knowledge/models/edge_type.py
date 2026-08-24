from enum import Enum


class EdgeType(Enum):
    """
    Defines the types of relationships that can exist
    between knowledge graph nodes.
    """

    CONTAINS = "contains"

    IMPORTS = "imports"

    DEPENDS_ON = "depends_on"

    USES = "uses"

    IMPLEMENTS = "implements"

    EXTENDS = "extends"

    CALLS = "calls"

    DEFINES = "defines"

    PART_OF = "part_of"

    BUILT_WITH = "built_with"