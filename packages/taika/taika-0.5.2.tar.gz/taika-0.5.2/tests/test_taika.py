#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `taika` package."""

from pathlib import Path

import pytest

from taika import taika


def test_Taika(tmpdir):
    """Tests the function run in the taika module."""
    source = Path("source")
    dest = Path(tmpdir)

    site = taika.Taika(source, dest)
    site.process()

    assert dest.is_dir()


def test_read_file():
    path = "source/fm-simple.rst"
    expected_content = b"This document will have normal frontmatter."
    expected_path = "fm-simple.rst"

    document = taika.read_file(path)

    assert document
    assert document["layout"] is None
    assert document["permalink"] is None
    assert document["content"] == expected_content
    assert str(document["path"]) == expected_path


def test_write_file(tmpdir):
    document = {"content": "<html>Hey!</html>", "url": "this-is-an-invented-document.html"}

    taika.write_file(document, tmpdir)


def test_unexistent_conf_path(tmpdir):
    source = "source"
    with pytest.raises(SystemExit):
        taika.Taika(source, tmpdir, "I-dont't-exist.ini")


def test_empty_conf_path(tmpdir):
    source = "source"
    with pytest.raises(SystemExit):
        taika.Taika(source, tmpdir, conf_path="source/taika_empty.ini")


def test_document_keys(tmpdir):
    source = "source"
    site = taika.Taika(source, tmpdir)

    documents = site.read(site.source)
    for document in documents:
        assert "path" in document
        assert "url" in document
        assert "raw_content" in document
        assert "content" in document
