import re
from pathlib import Path

from taika.events import EventManager
from taika.ext import layouts


class FakeSite(object):
    def __init__(self):
        self.events = EventManager()
        self.config = {"layouts_path": "source/templates"}


def test_setup():
    site = FakeSite()
    layouts.setup(site)


def test_correct():
    site = FakeSite()
    renderer = layouts.JinjaRenderer(site.config)
    path = Path("non_existent.rst")
    content = "A simple phrase."
    document = dict(path=path, url=path, raw_content=content, content=content, title="Awesome!")
    site.documents = [document]

    renderer.render_content(site)

    assert "<title>Awesome!</title>" in document["content"]
    assert re.search("<body>.*A simple phrase\..*</body>", document["content"], re.DOTALL)


def test_body_rendering():
    site = FakeSite()
    renderer = layouts.JinjaRenderer(site.config)
    path = Path("non_existent.rst")
    content = "{{ document.title }}"
    document = dict(path=path, url=path, raw_content=content, content=content, title="Awesome!")
    site.documents = [document]

    renderer.render_content(site)

    assert "<title>Awesome!</title>" in document["content"]
    assert document["title"] == document["pre_render_content"]
    assert re.search("<body>.*Awesome!.*</body>", document["content"], re.DOTALL)


def test_option_layouts_pattern():
    site = FakeSite()
    site.config["layouts_pattern"] = "**/*.txt"
    renderer = layouts.JinjaRenderer(site.config)
    path = Path("non_existent.rst")
    content = "A simple phrase."
    document = dict(path=path, url=path, raw_content=content, content=content, title="Awesome!")
    site.documents = [document]

    renderer.render_content(site)

    assert "<title>Awesome!</title>" not in document["content"]
    assert not re.search("<body>.*A simple phrase\..*</body>", document["content"], re.DOTALL)


def test_option_layouts_default():
    site = FakeSite()
    site.config["layouts_default"] = "empty.html"
    renderer = layouts.JinjaRenderer(site.config)
    path = Path("non_existent.rst")
    content = "A simple phrase."
    document = dict(path=path, url=path, raw_content=content, content=content, title="Awesome!")
    site.documents = [document]

    renderer.render_content(site)

    assert document["content"] == ""


def test_frontmatter_layout():
    site = FakeSite()
    renderer = layouts.JinjaRenderer(site.config)
    path = Path("non_existent.rst")
    content = "A simple phrase."
    document = dict(
        path=path,
        url=path,
        raw_content=content,
        content=content,
        title="Awesome!",
        layout="empty.html",
    )
    site.documents = [document]

    renderer.render_content(site)

    assert document["content"] == ""


def test_frontmatter_layout_None():
    site = FakeSite()
    renderer = layouts.JinjaRenderer(site.config)
    path = Path("non_existent.rst")
    content = "A simple phrase."
    document = dict(
        path=path, url=path, raw_content=content, content=content, title="Awesome!", layout=None
    )
    prev_content = document["content"]
    site.documents = [document]

    renderer.render_content(site)

    assert document["content"] == prev_content


def test_option_layouts_options():
    site = FakeSite()
    site.config["layouts_options"] = {"autoescape": True}
    renderer = layouts.JinjaRenderer(site.config)
    path = Path("non_existent.rst")
    content = "<p>A simple phrase.</p>"
    document = dict(path=path, url=path, raw_content=content, content=content, title="Awesome!")
    site.documents = [document]

    renderer.render_content(site)

    assert "&lt;p&gt;" in document["content"]
