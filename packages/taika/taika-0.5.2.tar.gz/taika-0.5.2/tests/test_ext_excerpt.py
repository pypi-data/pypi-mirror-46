from pathlib import Path

import pytest

from taika.events import EventManager
from taika.ext.excerpt import get_excerpt


class FakeSite(object):
    def __init__(self):
        self.events = EventManager()
        self.config = {}


site = FakeSite()
empty = ""
text_a = """\
A

<!--more-->
B
"""

text_b = """\
<p>A</p>
<p>B</p>
<!--more-->
B
"""


def test_double_jump():
    document = {"content": text_a, "url": Path("document.html")}

    get_excerpt(site, document)
    assert document["excerpt"] == "A"


def test_first_paragraph():
    document = {"content": text_b, "url": Path("document.html")}

    get_excerpt(site, document)
    assert document["excerpt"] == "<p>A</p>"


def test_empty_document():
    document = {"content": empty, "url": Path("document.html")}

    get_excerpt(site, document)
    assert document["excerpt"] == ""


def test_global_separator():
    site.config["excerpt_separator"] = "<!--more-->"
    document = {"content": text_a, "url": Path("document.html")}

    get_excerpt(site, document)
    assert document["excerpt"] == "A\n\n"


def test_global_separator_overriden():
    site.config["excerpt_separator"] = "<!--more-->"
    document = {"content": text_b, "excerpt_separator": "<p>B</p>", "url": Path("document.html")}

    get_excerpt(site, document)
    assert document["excerpt"] == "<p>A</p>\n"


def test_global_frontmatter_separator():
    document = {"content": text_b, "excerpt_separator": "<!--more-->", "url": Path("document.html")}

    get_excerpt(site, document)
    assert document["excerpt"] == "<p>A</p>\n<p>B</p>\n"


def test_no_html():
    document = {"content": text_b, "url": Path("document.rst")}

    get_excerpt(site, document)
    assert "exceprt" not in document


def test_no_url():
    document = {}

    with pytest.raises(KeyError):
        get_excerpt(site, document)
