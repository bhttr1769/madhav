from brain.code.parsing.import_parser import (
    ImportParser,
)

from brain.code.models.import_model import (
    ImportModel,
)


SOURCE = """
import os
import numpy as np

from pathlib import Path
from collections import defaultdict as dd
from package.submodule import thing
"""


def test_import_parser_extracts_imports():

    imports = ImportParser().parse(
        SOURCE,
        "example.py",
    )

    assert imports == frozenset({
        ImportModel(
            module="os",
            name=None,
            alias=None,
        ),
        ImportModel(
            module="numpy",
            name=None,
            alias="np",
        ),
        ImportModel(
            module="pathlib",
            name="Path",
            alias=None,
        ),
        ImportModel(
            module="collections",
            name="defaultdict",
            alias="dd",
        ),
        ImportModel(
            module="package.submodule",
            name="thing",
            alias=None,
        ),
    })


def test_import_parser_handles_multiple_names():

    source = """
from os import path, environ
"""

    imports = ImportParser().parse(
        source,
        "example.py",
    )

    assert imports == frozenset({
        ImportModel(
            module="os",
            name="path",
            alias=None,
        ),
        ImportModel(
            module="os",
            name="environ",
            alias=None,
        ),
    })


def test_import_parser_handles_relative_import():

    source = """
from .utils import helper
"""

    imports = ImportParser().parse(
        source,
        "example.py",
    )

    assert imports == frozenset({
        ImportModel(
            module="utils",
            name="helper",
            alias=None,
            level=1,
        ),
    })


def test_import_parser_handles_empty_source():

    imports = ImportParser().parse(
        "",
        "empty.py",
    )

    assert imports == frozenset()