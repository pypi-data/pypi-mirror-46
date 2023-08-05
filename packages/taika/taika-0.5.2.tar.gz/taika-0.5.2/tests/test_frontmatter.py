from taika import frontmatter


def test_frontmatter_complex_ok():
    """Test that the frontmatter is correctly handled."""

    expected_fm = {
        "name": "Martin D'vloper",
        "job": "Developer",
        "skill": "Elite",
        "employed": True,
        "foods": ["Apple", "Orange", "Strawberry", "Mango"],
        "languages": {"perl": "Elite", "python": "Elite", "pascal": "Lame"},
        "education": "4 GCSEs\n3 A-Levels\nBSc in the Internet of Things",
    }
    expected_body = b"Some title\n==========\n\nAnd subtitles too\n-----------------\n\nAnd text."
    with open("source/fm-complex-ok.rst", "rb") as fd:
        content = fd.read()

    fm, body = frontmatter.parse(content)

    assert fm == expected_fm
    assert body == expected_body


def test_frontmatter_no_closing_tag():
    expected_fm = {}
    with open("source/fm-no-closing-tag.rst", "rb") as fd:
        content = fd.read()
    expected_body = content

    fm, body = frontmatter.parse(content)

    assert fm == expected_fm
    assert body == expected_body.strip(b"\n")
