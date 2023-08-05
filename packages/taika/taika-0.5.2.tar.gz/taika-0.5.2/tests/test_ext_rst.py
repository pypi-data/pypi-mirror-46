from pathlib import Path

import pytest

from taika.events import EventManager
from taika.ext import rst
from taika.taika import read_file


class FakeSite(object):
    def __init__(self):
        self.events = EventManager()
        self.config = {}
        self.source = Path("source")


def test_setup():
    site = FakeSite()
    rst.setup(site)


def test_defaults():
    site = FakeSite()
    path = Path("non_existent.rst")
    content = "A simple phrase."
    document = dict(path=path, url=path, content=content, raw_content=content)

    rst.parse_rst(site, document)

    assert document["url"].suffix == rst.OUT_SUFFIX
    assert document["path"].suffix != rst.OUT_SUFFIX
    assert "<p>" in document["content"]


def test_option_rst_suffix():
    site = FakeSite()
    site.config.update({"rst_suffix": rst.DEFAULT_SUFFIX})
    path = Path("non_existent.rst")
    content = "A simple phrase."
    document = dict(path=path, url=path, content=content, raw_content=content)

    rst.parse_rst(site, document)

    assert document["url"].suffix == rst.OUT_SUFFIX
    assert document["path"].suffix != rst.OUT_SUFFIX
    assert "<p>" in document["content"]


def test_suffix_no_match():
    site = FakeSite()
    path = Path("non_existent.md")
    content = "A simple phrase."
    document = dict(path=path, url=path, content=content, raw_content=content)

    rst.parse_rst(site, document)

    assert document["url"].suffix != rst.OUT_SUFFIX
    assert document["path"].suffix != rst.OUT_SUFFIX
    assert "<p>" not in document["content"]


def test_options_rst_suffix_list():
    site = FakeSite()
    site.config.update({"rst_suffix": [".md", ".txt"]})
    path = Path("non_existent")
    content = "A simple phrase."
    document_A = dict(path=path.with_suffix(".md"), url=path, content=content, raw_content=content)
    document_B = dict(path=path.with_suffix(".txt"), url=path, content=content, raw_content=content)

    rst.parse_rst(site, document_A)
    rst.parse_rst(site, document_B)

    assert document_A["url"].suffix == rst.OUT_SUFFIX
    assert document_A["path"].suffix != rst.OUT_SUFFIX
    assert "<p>" in document_A["content"]
    assert document_B["url"].suffix == rst.OUT_SUFFIX
    assert document_B["path"].suffix != rst.OUT_SUFFIX
    assert "<p>" in document_B["content"]


def test_strictness():
    site = FakeSite()
    document = read_file("source/bad-rst.rst")

    with pytest.raises(SystemExit):
        rst.parse_rst(site, document)


CODE = """This is a file with bad RST
===========================

.. code:: golang

   package main
"""


def test_rst_options_default_error():
    site = FakeSite()
    path = Path("non_existent.rst")
    content = CODE
    document = dict(path=path, url=path, content=content, raw_content=content)
    with pytest.raises(SystemExit):
        rst.parse_rst(site, document)


def test_rst_options_from_config_success():
    site = FakeSite()

    options = rst.RST_OPTIONS.copy()
    options.update({"syntax_highlight": "none"})
    site.config.update({"rst_options": options})

    path = Path("non_existent.rst")
    content = CODE
    document = dict(path=path, url=path, content=content, raw_content=content)

    rst.parse_rst(site, document)

    assert document["url"].suffix == rst.OUT_SUFFIX
    assert document["path"].suffix != rst.OUT_SUFFIX
    assert "<pre" in document["content"]
    assert "<code>" in document["content"]
    assert "golang" in document["content"]


def test_include_directive():
    site = FakeSite()

    included_path = Path("included.rst")
    included_content = "Include me."
    included_document = dict(
        path=included_path,
        url=included_path,
        content=included_content,
        raw_content=included_content,
    )
    (site.source / included_path).write_text(included_content)

    path = Path("non_existent.rst")
    content = ".. include:: included.rst"
    document = dict(path=path, url=path, content=content, raw_content=content)

    rst.parse_rst(site, document)
    rst.parse_rst(site, included_document)

    assert document["content"] == included_document["content"]
