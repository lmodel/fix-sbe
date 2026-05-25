"""Validate FIX-Trading-Community sample SBE XML files against the LinkML schema.

Upstream FIX Simple Binary Encoding (SBE) sample files have been copied into
``tests/data/third-party/fix-sbe/<version>/``. They cover every published
release of the SBE technical standard (v1.0 RC3, RC4, STANDARD; v2.0 RC1, RC2,
RC3) and include the XInclude fragments shipped with the v2 releases
(``types-include.xml``, ``messages-include.xml``).

The corpus exercises two gates:

1. **XML well-formedness** - every ``.xml`` parses without error.
2. **LinkML-schema validation** - each XML is converted via
   ``scripts/fix_xml_to_linkml.py`` and validated by ``linkml-validate`` against
   the SBE LinkML umbrella schema. The number of errors must be
   ``<= max_errors`` for the file. ``max_errors > 0`` flags a *known* upstream
   data quirk; investigate before incrementing the budget.

The LinkML-level gate is automatically skipped until the SBE XML->LinkML
converter (``scripts/fix_xml_to_linkml.py``) lands; the well-formedness gate
runs unconditionally so the upstream fixtures remain parseable.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

import pytest
import yaml

PROJECT = Path(__file__).parent.parent
SCHEMA = (
    PROJECT
    / "src"
    / "fix_sbe/"
    / "schema"
    / "fix_sbe/.yaml"
)
CONV = PROJECT / "scripts" / "fix_xml_to_linkml.py"

_CORPUS = PROJECT / "tests" / "data" / "third-party" / "fix-sbe"

_LARGE_THRESHOLD = 1_000_000  # 1 MB

# (relative-path-under-corpus, target-class, max-allowed-validation-errors, note)
#
# Target class follows the SBE LinkML overlay convention:
#   * v1.0 releases (RC3, RC4, STANDARD)        -> MessageSchemaV1
#   * v2.0 releases (RC1, RC2, RC3)             -> MessageSchemaV2
#   * v2 XInclude fragments (messages-include)  -> MessagesV2
#   * v2 XInclude fragments (types-include)     -> TypesV2
#
# A non-zero ``max_errors`` flags a *known* data quirk in the upstream SBE
# corpus, not a converter or schema bug. Investigate before incrementing.
CASES = [
    # v1.0 -- single Examples.xml per release, schema root = MessageSchemaV1
    ("v1-0-RC3/Examples.xml",             "MessageSchemaV1", 0,
     "SBE 1.0 RC3 sample messageSchema (rc3 namespace)."),
    ("v1-0-RC4/Examples.xml",             "MessageSchemaV1", 0,
     "SBE 1.0 RC4 sample messageSchema (rc4 namespace)."),
    ("v1-0-STANDARD/Examples.xml",        "MessageSchemaV1", 0,
     "SBE 1.0 published-standard sample messageSchema (2016 namespace)."),

    # v2.0 RC1 -- uses the 2017 namespace but is structurally v1-shape: schema
    # root lists ``<sbe:message>`` elements directly (no ``<messages>`` wrapper),
    # which only fits ``MessageSchemaV1``.
    ("v2-0-RC1/Examples.xml",             "MessageSchemaV1", 0,
     "SBE 2.0 RC1 sample messageSchema (2017 ns, v1-shape body)."),

    # v2.0 RC2 -- main schema + XInclude fragments
    ("v2-0-RC2/xml/examples.xml",         "MessageSchemaV2", 0,
     "SBE 2.0 RC2 main messageSchema (XIncludes types- and messages-include)."),
    ("v2-0-RC2/xml/messages-include.xml", "MessagesV2", 0,
     "SBE 2.0 RC2 reusable <messages> fragment for XInclude."),
    ("v2-0-RC2/xml/types-include.xml",    "TypesV2", 0,
     "SBE 2.0 RC2 reusable <types> fragment for XInclude."),

    # v2.0 RC3 -- same shape as RC2 with the 2.0rc3 XSD
    ("v2-0-RC3/xml/examples.xml",         "MessageSchemaV2", 0,
     "SBE 2.0 RC3 main messageSchema (XIncludes types- and messages-include)."),
    ("v2-0-RC3/xml/messages-include.xml", "MessagesV2", 0,
     "SBE 2.0 RC3 reusable <messages> fragment for XInclude."),
    ("v2-0-RC3/xml/types-include.xml",    "TypesV2", 0,
     "SBE 2.0 RC3 reusable <types> fragment for XInclude."),
]


def _have(cmd: str) -> bool:
    return shutil.which(cmd) is not None


def _params():
    out = []
    for relpath, target, max_err, note in CASES:
        path = _CORPUS / relpath
        marks: list = []
        if path.is_file() and path.stat().st_size > _LARGE_THRESHOLD:
            marks.append(pytest.mark.slow)
        out.append(pytest.param(relpath, target, max_err, note,
                                id=relpath, marks=marks))
    return out


# ---------------------------------------------------------------------------
# Well-formedness gate
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("relpath,target,max_errors,note", _params())
def test_third_party_xml_wellformed(relpath, target, max_errors, note, capsys):
    """The XML must parse without error."""
    src = _CORPUS / relpath
    if not src.is_file():
        pytest.skip(f"missing upstream file {src}")
    tree = ET.parse(str(src))
    counts = _count_xml_records(tree.getroot())
    with capsys.disabled():
        print(f"\n  [wellformed] {relpath}: "
              f"parsed OK -- {_fmt_counts(counts, verb='counted')}")


# ---------------------------------------------------------------------------
# LinkML-schema validation gate
# ---------------------------------------------------------------------------

@pytest.mark.skipif(not _have("linkml-validate"),
                    reason="linkml-validate not on PATH (run `uv sync`).")
@pytest.mark.skipif(not CONV.exists(),
                    reason="scripts/fix_xml_to_linkml.py not yet implemented.")
@pytest.mark.parametrize("relpath,target,max_errors,note", _params())
def test_third_party_xml_validates_against_linkml(
        tmp_path, relpath, target, max_errors, note, capsys,
        fix_record_tally):
    """Convert the XML to YAML and assert LinkML validation stays within the
    per-file error budget."""
    src = _CORPUS / relpath
    if not src.is_file():
        pytest.skip(f"missing upstream file {src}")
    yaml_out = tmp_path / (Path(relpath).stem + ".yaml")

    conv = subprocess.run(
        [sys.executable, str(CONV), "--schema", str(SCHEMA),
         "--target-class", target, "--in", str(src), "--out", str(yaml_out)],
        capture_output=True, text=True, check=False,
    )
    assert conv.returncode == 0, (
        f"converter failed for {relpath}:\nstdout={conv.stdout}\n"
        f"stderr={conv.stderr}")
    assert yaml_out.exists()

    val = subprocess.run(
        ["linkml-validate", "-s", str(SCHEMA),
         "--target-class", target, str(yaml_out)],
        capture_output=True, text=True, check=False,
    )
    error_lines = [ln for ln in val.stdout.splitlines()
                   if ln.startswith("[ERROR]")]
    actual = len(error_lines)

    yaml_obj = yaml.safe_load(yaml_out.read_text())
    counts = _count_yaml_records(yaml_obj)
    fix_record_tally["total"] += sum(counts.values())
    budget_msg = (f"{actual}/{max_errors} errors (within budget)"
                  if max_errors > 0 else "no errors")
    with capsys.disabled():
        print(f"\n  [validate]   {relpath} ({target}): "
              f"{_fmt_counts(counts, verb='linkml schema validated')}; {budget_msg}")

    assert actual <= max_errors, (
        f"{relpath}: {actual} validation errors, expected <= "
        f"{max_errors}. Note: {note}\n"
        f"First 5 errors:\n  " + "\n  ".join(error_lines[:5]))


# ---------------------------------------------------------------------------
# Record-count helpers (used to surface processing volume per file)
# ---------------------------------------------------------------------------

# XML local tag names whose direct children are counted as "records" in a
# FIX SBE messageSchema document. Ordered roughly by domain weight.
_XML_CONTAINERS = [
    "types",      # <type>, <composite>, <enum>, <set>, <ref>
    "composite",  # nested member encodings
    "enum",       # <validValue>
    "set",        # <choice>
    "messages",   # <message> (v2 only; v1 nests <sbe:message> directly under root)
    "message",    # <field>, <group>
    "group",      # <field>, nested <group>
]


def _count_xml_records(root: ET.Element) -> dict[str, int]:
    """Count children of each well-known SBE container element.

    v1.0 messageSchema lists ``<sbe:message>`` elements directly under the
    schema root (no ``<messages>`` wrapper), so they are tallied separately.
    """
    def local(tag: str) -> str:
        return tag.split("}", 1)[1] if "}" in tag else tag

    out: dict[str, int] = {}
    for elt in root.iter():
        lname = local(elt.tag)
        if lname in _XML_CONTAINERS:
            n = sum(1 for c in elt if local(c.tag) != "description")
            out[lname] = out.get(lname, 0) + n

    if local(root.tag) == "messageSchema":
        n_msg_direct = sum(1 for c in root if local(c.tag) == "message")
        if n_msg_direct:
            out["message"] = out.get("message", 0) + n_msg_direct
    return out


# YAML slot names whose multivalued contents we count after conversion. Mirrors
# the SBE LinkML overlays (V1 / V2 + common). Exact slot names will firm up
# once ``scripts/fix_xml_to_linkml.py`` lands; until then this mapping is the
# best-faith mirror of the XML containers above.
_YAML_RECORD_PATHS = [
    ("types",    "type"),
    ("types",    "composite"),
    ("types",    "enum"),
    ("types",    "set"),
    ("types",    "ref"),
    ("messages", "message"),
]


def _count_yaml_records(doc: Any) -> dict[str, int]:
    """Count entries inside the well-known SBE containers in a converted YAML."""
    out: dict[str, int] = {}
    if not isinstance(doc, dict):
        return out
    for container, child in _YAML_RECORD_PATHS:
        node = doc.get(container)
        if isinstance(node, dict):
            items = node.get(child)
            if isinstance(items, list):
                out[child] = out.get(child, 0) + len(items)
    # Fragment files (MessagesV2 / TypesV2) carry the list at the root.
    for k in ("type", "composite", "enum", "set", "ref", "message"):
        if isinstance(doc.get(k), list):
            out[k] = out.get(k, 0) + len(doc[k])
    return out


_GREEN = "\033[32m"
_RESET = "\033[0m"


def _green(s: str) -> str:
    """Wrap ``s`` in ANSI green codes when stdout is a TTY (no-op otherwise)."""
    return f"{_GREEN}{s}{_RESET}" if sys.stdout.isatty() else s


def _fmt_counts(counts: dict[str, int], verb: str = "counted") -> str:
    """Format a record-count summary as ``<verb> N records (k1=v1, k2=v2, ...)``."""
    if not counts:
        return _green(f"{verb} 0 records")
    total = sum(counts.values())
    parts = [f"{k}={v}" for k, v in sorted(counts.items(),
                                            key=lambda kv: -kv[1])]
    return f"{_green(f'{verb} {total} records')} ({', '.join(parts)})"
