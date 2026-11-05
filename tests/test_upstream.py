"""Checks that upstream/ holds the editions the schema models.

upstream/ holds FIX's XSDs, examples and licences, and the conformance suite's schemas, as they
are published. scripts/check_upstream_release.py compares them with GitHub. These tests make the
same comparison offline, and hold the schema's headers and NOTICE to the same pins.
"""

import hashlib
import importlib.util
import xml.etree.ElementTree as ET
from functools import cache

import yaml

from tests.paths import ROOT, SCHEMA_DIR, UPSTREAM, XSD_V1, XSD_V2

WATCH = ROOT / "scripts" / "check_upstream_release.py"


@cache
def _watch():
    spec = importlib.util.spec_from_file_location("watch_pins", WATCH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _blob(path):
    data = path.read_bytes()
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def _header(name):
    return yaml.safe_load((SCHEMA_DIR / f"{name}.yaml").read_text(encoding="utf-8"))


def test_upstream_holds_only_the_pinned_files():
    found = {
        path.relative_to(UPSTREAM).as_posix()
        for path in UPSTREAM.rglob("*")
        if path.is_file()
    }
    assert found == set(_watch().pins())
    assert len(found) == 11


def test_copies_match_the_pinned_blobs():
    """Each file has the git object hash the watch pins."""
    wrong = [
        path for path, sha in _watch().pins().items() if _blob(UPSTREAM / path) != sha
    ]
    assert not wrong


def test_the_modules_name_the_pinned_editions():
    watch = _watch()
    version_one = _header("fix_sbe_v1_0")
    version_two = _header("fix_sbe_v2_0")
    assert version_one["version"] == watch.V1_EDITION
    assert version_two["version"] == watch.V2_EDITION
    assert version_one["source"].endswith(f"/tree/{watch.V1_TAG}/{watch.V1_FOLDER}")
    assert version_two["source"].endswith(f"/tree/{watch.V2_COMMIT}/{watch.V2_FOLDER}")
    for name in ("fix_sbe", "fix_sbe_common"):
        assert _header(name)["version"] == f"{watch.V1_EDITION} and {watch.V2_EDITION}"


def test_the_umbrella_names_the_pinned_commits():
    watch = _watch()
    annotations = _header("fix_sbe")["annotations"]
    assert annotations["upstream_v1_tag"] == watch.V1_TAG
    assert annotations["upstream_v1_commit"] == watch.V1_COMMIT
    assert annotations["upstream_v2_commit"] == watch.V2_COMMIT


def test_each_module_says_what_it_is_licensed_under():
    for path in SCHEMA_DIR.glob("*.yaml"):
        assert (
            yaml.safe_load(path.read_text(encoding="utf-8"))["license"] == "Apache-2.0"
        )


def test_the_xsds_state_the_editions_they_hold():
    assert ET.parse(XSD_V1).getroot().get("version") == "1.0 Standard"
    assert ET.parse(XSD_V2).getroot().get("version") == "2.0RC3"


def test_the_notice_carries_what_the_licences_ask():
    """CC BY-ND asks for attribution and a link to the licence, and Apache-2.0 for its notice,
    and FIX's marks stay FIX's."""
    notice = (ROOT / "NOTICE").read_text(encoding="utf-8")
    for needed in (
        "FIX Protocol Limited",
        "Creative Commons Attribution-NoDerivatives 4.0",
        "https://creativecommons.org/licenses/by-nd/4.0/legalcode",
        "fix-simple-binary-encoding",
        "fix-sbe-conformance",
        "Infopaq",
        "does not imply endorsement",
    ):
        assert needed in notice, needed
