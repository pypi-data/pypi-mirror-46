#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for the command line of `taika` package."""

from pathlib import Path

import pytest

from taika import cli


def test_basic(tmpdir):
    """Test the most basic command."""
    source = Path("source")
    dest = Path(tmpdir)

    result = cli.main([str(source), str(dest)])

    assert result == 0
    assert dest.is_dir()
    assert dest.glob("*")


def test_help(capsys):
    """Test the help."""
    with pytest.raises(SystemExit):
        cli.main(["--help"])

    out, __ = capsys.readouterr()

    assert "--help" in out
    assert "taika" in out
