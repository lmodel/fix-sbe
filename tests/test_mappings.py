"""Checks every mapping the schema states.

A mapping names its target by a CURIE whose prefix the module binds, so a projection raises no
warning. Each target's class must exist in the copy of lmodel/fix-orchestra in tests/neighbours/,
which is that repository's released asset, or its branch's until it releases.
"""

import pytest
import yaml

from tests.paths import ROOT, SCHEMA_DIR

NEIGHBOUR = ROOT / "tests" / "neighbours" / "fix-orchestra.yaml"
KINDS = ("exact_mappings", "close_mappings", "related_mappings", "broad_mappings", "narrow_mappings")

# What FIX's transposer does with each kind of SBE element, in its SBE2Orchestra classes. The
# set and the choice have no line there, so they stay related, with a comment in the schema.
EXPECTED = {
    "SbeMessageSchema": ("close_mappings", "OrchestraRepositoryV10"),
    "SbeMessage": ("close_mappings", "OrchestraMessageV10"),
    "SbeGroup": ("close_mappings", "OrchestraGroupV10"),
    "SbeField": ("close_mappings", "OrchestraFieldV10"),
    "SbeSimpleType": ("close_mappings", "OrchestraDatatypeV10"),
    "SbeMemberType": ("close_mappings", "OrchestraDatatypeV10"),
    "SbeComposite": ("close_mappings", "OrchestraComponentV10"),
    "SbeEnum": ("close_mappings", "OrchestraCodeSetV10"),
    "SbeSet": ("related_mappings", "OrchestraCodeSetV10"),
    "SbeValidValue": ("close_mappings", "OrchestraCodeV10"),
    "SbeChoice": ("related_mappings", "OrchestraCodeV10"),
}


def _modules():
    return {
        path.stem: yaml.safe_load(path.read_text(encoding="utf-8"))
        for path in sorted(SCHEMA_DIR.glob("*.yaml"))
    }


def _stated():
    """Every (module, class, kind, target) the schema states."""
    for name, module in _modules().items():
        for cls_name, cls in (module.get("classes") or {}).items():
            for kind in KINDS:
                for target in cls.get(kind) or []:
                    yield name, cls_name, kind, target


def test_every_mapping_has_a_bound_prefix():
    modules = _modules()
    for name, cls_name, _, target in _stated():
        prefix = target.partition(":")[0]
        assert prefix in modules[name]["prefixes"], (cls_name, target)


def test_the_mappings_are_the_ones_listed():
    """Each element maps as FIX's transposer carries it, and there are no others."""
    found = {(cls_name, kind, target) for _, cls_name, kind, target in _stated()}
    wanted = set()
    for stem, (kind, target) in EXPECTED.items():
        if stem in ("SbeValidValue", "SbeChoice"):
            wanted.add((stem, kind, f"fix_orchestra:{target}"))
        elif stem == "SbeMemberType":
            wanted.add((f"{stem}V2", kind, f"fix_orchestra:{target}"))
        else:
            for edition in ("V1", "V2"):
                wanted.add((f"{stem}{edition}", kind, f"fix_orchestra:{target}"))
    assert found == wanted


def test_no_mapping_says_exact():
    """An SBE element sits at a place on the wire, which no Orchestra element says, so none is
    the same thing."""
    assert not [row for row in _stated() if row[2] == "exact_mappings"]


def test_every_target_exists_in_the_neighbour():
    if not NEIGHBOUR.exists():
        pytest.skip("tests/neighbours/fix-orchestra.yaml waits for lmodel/fix-orchestra's asset")
    classes = yaml.safe_load(NEIGHBOUR.read_text(encoding="utf-8"))["classes"]
    missing = {
        target
        for *_, target in _stated()
        if target.partition(":")[2] not in classes
    }
    assert not missing
