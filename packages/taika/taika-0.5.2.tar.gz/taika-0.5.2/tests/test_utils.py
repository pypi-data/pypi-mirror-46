import sys

from taika import utils


def test_add_syspath():
    paths = ["A", "B", "C"]
    prev_path = sys.path[:]

    with utils.add_syspath(paths):
        context_path = sys.path[:]

    assert prev_path != context_path
    assert prev_path == sys.path
    assert all([path in context_path for path in paths])
    assert not any([path in prev_path for path in paths])
