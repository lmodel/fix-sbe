"""Checks that the project's words are its own.

FIX licenses the specification and its XSDs under CC BY-ND 4.0, which lets a whole copy travel but
no adaptation, so no sentence of FIX's belongs in the schema or the docs. This test looks for a
run of four or more words the project's text shares with the documentation in the pinned XSDs,
the same check NOTICE describes.
"""

import re
import xml.etree.ElementTree as ET
from functools import cache

import pytest
import yaml

from tests.paths import ROOT, SCHEMA_DIR, XSD_V1, XSD_V2

XS = "{http://www.w3.org/2001/XMLSchema}"
RUN = 4
WORD = re.compile(r"[a-z0-9]+")

# A run that names a thing rather than says something: the licence's title, which NOTICE must
# state, and FIX's own organisation.
ALLOWED_RUNS = {
    "creative commons attribution noderivatives",
    "commons attribution noderivatives 4",
    "attribution noderivatives 4 0",
    "noderivatives 4 0 international",
    "4 0 international public",
    "0 international public license",
    "fix simple binary encoding",
}


def _words(text):
    return WORD.findall(text.lower())


def _runs(text):
    words = _words(text)
    return {" ".join(words[i : i + RUN]) for i in range(len(words) - RUN + 1)}


@cache
def fix_runs():
    """Every run of words in the pinned XSDs' documentation."""
    runs = set()
    for path in (XSD_V1, XSD_V2):
        for node in ET.parse(path).getroot().iter(f"{XS}documentation"):
            runs |= _runs(node.text or "")
    return runs


def _schema_texts(node):
    """Every piece of the schema that a reader takes for prose."""
    if isinstance(node, dict):
        for key, value in node.items():
            if key in ("description", "title", "comments", "notes") and isinstance(
                value, (str, list)
            ):
                yield from [value] if isinstance(value, str) else value
            else:
                yield from _schema_texts(value)
    elif isinstance(node, list):
        for item in node:
            yield from _schema_texts(item)


def _documents():
    docs = [ROOT / "README.md", ROOT / "docs" / "about.md", ROOT / "docs" / "index.md"]
    docs += sorted((ROOT / ".lokf" / "knowledge").rglob("*.md"))
    return [path for path in docs if path.exists()]


def test_the_check_has_something_to_compare():
    assert len(fix_runs()) > 300


@pytest.mark.parametrize(
    "path", sorted(SCHEMA_DIR.glob("*.yaml")), ids=lambda p: p.stem
)
def test_the_schema_shares_no_run_with_the_xsds(path):
    shared = {}
    for text in _schema_texts(yaml.safe_load(path.read_text(encoding="utf-8"))):
        found = (_runs(text) & fix_runs()) - ALLOWED_RUNS
        if found:
            shared[text[:60]] = sorted(found)
    assert not shared, shared


@pytest.mark.parametrize("path", _documents(), ids=lambda p: p.name)
def test_the_docs_share_no_run_with_the_xsds(path):
    assert not (_runs(path.read_text(encoding="utf-8")) & fix_runs()) - ALLOWED_RUNS


def test_a_shared_run_is_caught():
    """A sentence taken from the XSD fails, so a pass above means something."""
    node = next(ET.parse(XSD_V1).getroot().iter(f"{XS}documentation"))
    assert _runs(node.text) & fix_runs()
