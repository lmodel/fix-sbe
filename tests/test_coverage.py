"""Checks the schema against the XSDs, element by element.

The tests walk each XSD with ElementTree and share no table with the schema. Each complex type
must have a class that holds exactly its attributes and child elements, under the alias that
names them, with the same required flag, range, default and repeat count. Anything the schema
states more strictly than the XSD is listed here with its reason.
"""

import re
import xml.etree.ElementTree as ET
from functools import cache

import pytest
import yaml
from linkml_runtime import SchemaView

from tests.paths import SCHEMA, SCHEMA_DIR, XSD_V1, XSD_V2

XS = "{http://www.w3.org/2001/XMLSchema}"
EDITIONS = {"V1": XSD_V1, "V2": XSD_V2}
TEXT_SLOTS = {"element_value", "valid_value", "bit_position"}

# The XSD lets these hold stray text. The specification gives it no meaning, so the schema has
# no slot for it, and the converter refuses it.
MIXED_WITHOUT_TEXT = {"compositeDataType", "enumType", "refType", "setType"}

# The specification's stated rule is stricter than the XSD: a repeating group must hold at
# least one field (chapter 3, "Schema specification of a group").
STRICTER_THAN_XSD = {("groupType", "field")}

NUMBER_RANGES = {
    "xs:unsignedShort": (0, 65535),
    "xs:unsignedInt": (0, 4294967295),
    "xs:nonNegativeInteger": (0, None),
    "xs:positiveInteger": (1, None),
}
NAME_RANGES = {
    "sbe:symbolicName_t": "SbeSymbolicName",
    "sbe:qualifiedName_t": "SbeQualifiedName",
    "xs:token": "SbeToken",
    "xs:string": "string",
}


@cache
def view():
    return SchemaView(str(SCHEMA))


@cache
def xsd(edition):
    return ET.parse(EDITIONS[edition]).getroot()


def _named(root, kind):
    return {node.get("name"): node for node in root.findall(f"{XS}{kind}")}


def _attribute_nodes(root, node):
    """Every attribute a type declares, through its groups and its base type."""
    groups = _named(root, "attributeGroup")
    types = _named(root, "complexType")
    for child in node:
        tag = child.tag.removeprefix(XS)
        if tag == "attribute":
            yield child
        elif tag == "attributeGroup":
            yield from _attribute_nodes(
                root, groups[child.get("ref").removeprefix("sbe:")]
            )
        elif tag in ("simpleContent", "complexContent"):
            yield from _attribute_nodes(root, child)
        elif tag == "extension":
            base = child.get("base")
            if base.startswith("sbe:"):
                yield from _attribute_nodes(root, types[base.removeprefix("sbe:")])
            yield from _attribute_nodes(root, child)


def _element_nodes(root, node, within=None):
    """Every child element a type declares, with the choice or sequence that holds it."""
    types = _named(root, "complexType")
    for child in node:
        tag = child.tag.removeprefix(XS)
        if tag == "element":
            yield child, within
        elif tag in ("sequence", "choice"):
            yield from _element_nodes(root, child, child if tag == "choice" else within)
        elif tag in ("complexContent", "extension"):
            base = child.get("base")
            if base and base.startswith("sbe:"):
                yield from _element_nodes(
                    root, types[base.removeprefix("sbe:")], within
                )
            yield from _element_nodes(root, child, within)


def _element_definition(root, name):
    """The global or anonymous definition an element name stands for."""
    for node in root.iter(f"{XS}element"):
        if node.get("name") == name and node.find(f"{XS}complexType") is not None:
            return node.find(f"{XS}complexType")
    return None


def _class_cases():
    """Each class that renders an XSD type or anonymous element, by edition."""
    cases = []
    for name, cls in view().all_classes().items():
        if cls.abstract or cls.mixin:
            continue
        annotations = {key: cls.annotations[key].value for key in cls.annotations}
        if "xsd_type" not in annotations and "xml_element" not in annotations:
            continue
        for edition in EDITIONS:
            if name.endswith(edition) or not re.search(r"V\d$", name):
                cases.append((name, edition, annotations))
    return cases


def _type_node(root, annotations):
    if "xsd_type" in annotations:
        return annotations["xsd_type"], _named(root, "complexType")[
            annotations["xsd_type"]
        ]
    element = annotations["xml_element"]
    return element, _element_definition(root, element)


def _slots_by_alias(class_name):
    found = {}
    for slot in view().class_induced_slots(class_name):
        for alias in slot.aliases:
            found[alias] = slot
    return found


CASES = _class_cases()
IDS = [f"{name}-{edition}" for name, edition, _ in CASES]


def test_every_xsd_type_has_a_class():
    """No complex type of either XSD goes without a class."""
    for edition in EDITIONS:
        rendered = {
            annotations["xsd_type"]
            for _, case_edition, annotations in CASES
            if case_edition == edition and "xsd_type" in annotations
        }
        assert set(_named(xsd(edition), "complexType")) == rendered, edition


@pytest.mark.parametrize(("name", "edition", "annotations"), CASES, ids=IDS)
def test_each_class_holds_its_types_attributes(name, edition, annotations):
    root = xsd(edition)
    _, node = _type_node(root, annotations)
    declared = {a.get("name") or a.get("ref"): a for a in _attribute_nodes(root, node)}
    slots = _slots_by_alias(name)
    children = {
        (child.get("name") or child.get("ref").removeprefix("sbe:"))
        for child, _ in _element_nodes(root, node)
    }
    attribute_slots = {alias for alias in slots if alias not in children}
    assert attribute_slots == set(declared), name
    for alias, attribute in declared.items():
        slot = slots[alias]
        assert bool(slot.required) == (attribute.get("use") == "required"), alias
        default = attribute.get("default")
        if default is None:
            assert slot.ifabsent is None, alias
        elif slot.range == "integer":
            assert slot.ifabsent == f"int({default})", alias
        else:
            assert slot.ifabsent == f"string({default})", alias
        kind = attribute.get("type")
        if kind in NUMBER_RANGES:
            low, high = NUMBER_RANGES[kind]
            assert slot.range == "integer", alias
            assert slot.minimum_value == low, alias
            assert slot.maximum_value == high, alias
        elif kind in NAME_RANGES:
            assert slot.range == NAME_RANGES[kind], alias
        elif attribute.get("ref") == "xml:base":
            # An xs:anyURI may be relative, as an XInclude's address is, and LinkML's uri may not.
            assert slot.range == "string", alias
        else:
            values = [e.get("value") for e in attribute.iter(f"{XS}enumeration")]
            permissible = view().get_enum(slot.range).permissible_values
            assert set(values) == set(permissible), alias


@pytest.mark.parametrize(("name", "edition", "annotations"), CASES, ids=IDS)
def test_each_class_holds_its_types_children(name, edition, annotations):
    root = xsd(edition)
    xsd_name, node = _type_node(root, annotations)
    slots = _slots_by_alias(name)
    for child, choice in _element_nodes(root, node):
        element = child.get("name") or child.get("ref").removeprefix("sbe:")
        assert element in slots, (name, element)
        slot = slots[element]
        holder = choice if choice is not None else child
        low = int(holder.get("minOccurs", "1"))
        high = (
            child.get("maxOccurs", "1")
            if choice is None
            else holder.get("maxOccurs", "1")
        )
        assert slot.multivalued == (high != "1"), element
        if (xsd_name, element) in STRICTER_THAN_XSD:
            assert slot.required, element
        else:
            assert bool(slot.required) == (low >= 1), element
        if slot.required:
            assert slot.minimum_cardinality == 1, element
        if high.isdigit() and int(high) > 1:
            assert slot.maximum_cardinality == int(high), element


def _xsd_type_of_element(root, element, child):
    """The XSD type an element under a type stands for."""
    if child.get("type"):
        return child.get("type").removeprefix("sbe:")
    if child.get("ref"):
        target = _named(root, "element")[child.get("ref").removeprefix("sbe:")]
        return target.get("type", "").removeprefix("sbe:") or element
    return element


def _classes_under(slot):
    """The concrete classes a slot's range admits."""
    names = (
        [slot.range] if not slot.any_of else [option.range for option in slot.any_of]
    )
    found = []
    for name in names:
        for candidate in [name, *view().class_descendants(name)]:
            if not view().get_class(candidate).abstract and candidate not in found:
                found.append(candidate)
    return found


@pytest.mark.parametrize(("name", "edition", "annotations"), CASES, ids=IDS)
def test_each_child_ranges_over_the_type_the_xsd_names(name, edition, annotations):
    root = xsd(edition)
    _, node = _type_node(root, annotations)
    slots = _slots_by_alias(name)
    for child, _ in _element_nodes(root, node):
        element = child.get("name") or child.get("ref").removeprefix("sbe:")
        wanted = _xsd_type_of_element(root, element, child)
        offered = {}
        for option in _classes_under(slots[element]):
            cls = view().get_class(option)
            found = {key: cls.annotations[key].value for key in cls.annotations}
            offered[found.get("xml_element")] = found.get(
                "xsd_type", found.get("xml_element")
            )
        if child.get("type"):
            field_like = wanted == "fieldType" or wanted == "blockType"
            assert wanted in offered.values() or field_like, (name, element, offered)
        else:
            assert element in offered or wanted in offered.values(), (
                name,
                element,
                offered,
            )


@pytest.mark.parametrize(("name", "edition", "annotations"), CASES, ids=IDS)
def test_each_class_holds_text_only_where_the_xsd_does(name, edition, annotations):
    root = xsd(edition)
    xsd_name, node = _type_node(root, annotations)
    holds_text = node.find(f"{XS}simpleContent") is not None or (
        node.get("mixed") == "true" and xsd_name not in MIXED_WITHOUT_TEXT
    )
    slots = {slot.name for slot in view().class_induced_slots(name)}
    assert bool(slots & TEXT_SLOTS) == holds_text, name


@pytest.mark.parametrize(
    ("edition", "kind", "pattern_slot"),
    [
        ("V1", "symbolicName_t", "symbolic_name"),
        ("V2", "symbolicName_t", "symbolic_name"),
        ("V1", "qualifiedName_t", "value_ref"),
        ("V2", "qualifiedName_t", "value_ref"),
    ],
)
def test_the_name_patterns_accept_what_the_xsd_accepts(edition, kind, pattern_slot):
    """The XSD's pattern is implicitly anchored and its length a separate facet."""
    node = _named(xsd(edition), "simpleType")[kind]
    restriction = node.find(f"{XS}restriction")
    theirs = re.compile("^" + restriction.find(f"{XS}pattern").get("value") + "$")
    longest = restriction.find(f"{XS}maxLength")
    limit = int(longest.get("value")) if longest is not None else None
    ours = re.compile(view().get_slot(pattern_slot).pattern)
    samples = [
        "a",
        "_",
        "a1",
        "A_b",
        "1a",
        "a b",
        "",
        "a.b",
        "a.",
        ".b",
        "a.b.c",
        "x" * 64,
        "x" * 65,
    ]
    for sample in samples:
        accepted = bool(theirs.match(sample)) and (
            limit is None or len(sample) <= limit
        )
        assert bool(ours.match(sample)) == accepted, sample


@pytest.mark.parametrize("edition", EDITIONS)
def test_each_module_names_its_xsd(edition):
    """A module's namespace and version annotations are the XSD's own."""
    module = "fix_sbe_v1_0" if edition == "V1" else "fix_sbe_v2_0"
    header = yaml.safe_load((SCHEMA_DIR / f"{module}.yaml").read_text(encoding="utf-8"))
    root = xsd(edition)
    assert header["annotations"]["xsd_namespace"] == root.get("targetNamespace")
    assert header["annotations"]["xsd_version"] == root.get("version")


def test_every_slot_is_used_by_a_class():
    """A slot no class lists holds nothing a document can say."""
    used = set()
    for name in view().all_classes():
        used |= {slot.name for slot in view().class_induced_slots(name)}
    assert set(view().all_slots()) <= used


def test_every_description_is_there():
    """Every class, slot, enum and type says what it is, as linkml-lint does not check."""
    for elements in (
        view().all_classes(),
        view().all_slots(),
        view().all_enums(),
        {k: v for k, v in view().all_types().items() if k.startswith("Sbe")},
    ):
        for name, element in elements.items():
            assert element.description, name
