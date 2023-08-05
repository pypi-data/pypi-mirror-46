from taika.events import EventManager
from taika.ext import collections


class FakeSite(object):
    def __init__(self):
        self.events = EventManager()
        self.config = {}


def test_setup():
    site = FakeSite()
    collections.setup(site)


def test_correct():
    site = FakeSite()
    site.config = {"collections": {"posts": {"pattern": "posts/.*.html"}}}
    collector = collections.Collector(site.config)

    site.documents = [{"path": "posts/random_fake.html"}, {"path": "posts/random_fake.rst"}]

    collector.organize(site)
    assert len(site.collections["posts"]) == 1


def test_correct_under():
    site = FakeSite()
    site.config = {"collections": {"posts": {"pattern": "posts/*"}}}
    collector = collections.Collector(site.config)
    site.documents = [
        {"path": "posts/random_fake.html"},
        {"path": "posts/random_fake.rst"},
        {"path": "posts/nested/random_fake.html"},
    ]

    collector.organize(site)
    assert len(site.collections["posts"]) == 3


def test_correct_drafts():
    site = FakeSite()
    site.config = {
        "collections": {"posts": {"pattern": "posts/*"}, "drafts": {"pattern": "drafts/*"}}
    }
    collector = collections.Collector(site.config)
    site.documents = [
        {"path": "posts/random_fake.html"},
        {"path": "posts/random_fake.rst"},
        {"path": "drafts/random_fake.rst"},
    ]

    collector.organize(site)
    assert len(site.collections["posts"]) == 2
    assert len(site.collections["drafts"]) == 1
