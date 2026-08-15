from brain.browser.parsers.documentation_parser import (
    DocumentationParser,
)


def test_documentation_parser():

    content = """
# Introduction

Text.

## Installation

Text.

## Configuration

Text.
"""

    documentation = (
        DocumentationParser()
    ).parse(
        content,
    )

    assert (
        len(
            documentation.sections
        )
        == 3
    )

    assert (
        "Introduction"
        in documentation.sections
    )

    assert (
        "Installation"
        in documentation.sections
    )

    assert (
        "Configuration"
        in documentation.sections
    )