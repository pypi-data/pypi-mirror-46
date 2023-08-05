import pytest

from taika import Taika
from taika import events


def test_extensions_path(tmpdir):
    source = "source"
    site = Taika(source, tmpdir)
    prev_extension_number = sum([len(event_funcs) for event_funcs in site.events.funcs.values()])
    site.config["extension_paths"] = ["source/extensions"]
    site.config["extensions"] = ["rst"]

    site.import_extensions()

    post_extension_number = sum([len(event_funcs) for event_funcs in site.events.funcs.values()])

    assert post_extension_number == 1 + prev_extension_number


def test_extensions_path_nested(tmpdir):
    source = "source"
    site = Taika(source, tmpdir)
    prev_extension_number = sum([len(event_funcs) for event_funcs in site.events.funcs.values()])
    site.config["extension_paths"] = ["extensions/nested"]
    site.config["extensions"] = ["rst"]

    site.import_extensions()

    post_extension_number = sum([len(event_funcs) for event_funcs in site.events.funcs.values()])

    assert post_extension_number == 1 + prev_extension_number


def test_event_not_found():
    manager = events.EventManager()
    with pytest.raises(events.EventNotFound):
        manager.register("non-existent-event", lambda x: x)
