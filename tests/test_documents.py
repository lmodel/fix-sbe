"""Checks the schema against FIX's own documents, by three routes that share no code.

Every document upstream/ holds passes lxml against its edition's XSD, passes the committed JSON
Schema once scripts/sbe_xml_to_yaml.py has made a record of it, and gives back the same tree
when a separate walk of the XML is compared with the record. The comparison reads each slot's
XML name from the schema's aliases and each class's element from its annotation, so a converter
that drops or moves a value fails here whatever its own tables say.
"""

import json
from functools import cache

import jsonschema
import pytest
import yaml
from lxml import etree

from tests import conversion
from tests.paths import ROOT, SCHEMA_DIR
from tests.sbe_rules import rule_errors

COMMITTED = ROOT / "project" / "jsonschema" / "fix_sbe.schema.json"
STAND_IN = ROOT / "tests" / "xml-namespace.xsd"
XS = "{http://www.w3.org/2001/XMLSchema}"
XSI = "{http://www.w3.org/2001/XMLSchema-instance}"
XML_NS = "{http://www.w3.org/XML/1998/namespace}"
TEXT_SLOTS = {"element_value", "valid_value", "bit_position"}
DOCUMENTS = sorted(conversion.DOCUMENTS)


@cache
def xsd(path):
    """An edition's XSD, reading its one import from the stand-in in place of the network."""
    tree = etree.parse(str(path))
    for imported in tree.getroot().findall(f"{XS}import"):
        imported.set("schemaLocation", str(STAND_IN))
    return etree.XMLSchema(tree)


def _parse(path):
    tree = etree.parse(str(path), etree.XMLParser(no_network=True))
    tree.xinclude()
    return tree


@cache
def modules():
    merged = {"classes": {}, "slots": {}}
    for path in SCHEMA_DIR.glob("*.yaml"):
        doc = yaml.safe_load(path.read_text(encoding="utf-8"))
        for kind, elements in merged.items():
            elements.update(doc.get(kind) or {})
    return merged


def _xml_tree(element):
    """A plain tree of the XML, with no help from the converter."""
    attributes = {}
    for name, value in element.attrib.items():
        if name.startswith(XSI):
            continue
        attributes[name.replace(XML_NS, "xml:")] = value
    children = [_xml_tree(child) for child in element if isinstance(child.tag, str)]
    text = " ".join((element.text or "").split())
    return (
        etree.QName(element).localname,
        attributes,
        text if not children else "",
        children,
    )


def _class_slots(name):
    """The slots a record's key can name on a class, through its chain of parents."""
    classes = modules()["classes"]
    found = {}
    while name:
        cls = classes[name]
        for mixin in cls.get("mixins") or []:
            found.update(_class_slots(mixin))
        for slot, definition in (cls.get("attributes") or {}).items():
            found.setdefault(slot, definition)
        for slot in cls.get("slots") or []:
            found.setdefault(slot, modules()["slots"].get(slot, {}))
        name = cls.get("is_a")
    return found


def _range_of(owner, slot):
    """A list's range on a class, from the first slot_usage on it, its mixins or its parents."""
    classes = modules()["classes"]
    pending = [owner]
    while pending:
        name = pending.pop(0)
        usage = (classes[name].get("slot_usage") or {}).get(slot) or {}
        if usage.get("range"):
            return usage["range"]
        pending += classes[name].get("mixins") or []
        if classes[name].get("is_a"):
            pending.append(classes[name]["is_a"])
    return modules()["slots"][slot].get("range")


def _record_tree(record, class_name, element):
    """The same tree from a record, naming attributes and elements as the schema does."""
    slots = _class_slots(class_name)
    attributes, children, text = {}, [], ""
    for key, value in record.items():
        if key == "encoding_kind":
            continue
        if key in TEXT_SLOTS:
            text = str(value)
        elif isinstance(value, list):
            for item in value:
                kind = item.get("encoding_kind") or _range_of(class_name, key)
                annotations = modules()["classes"][kind].get("annotations") or {}
                aliases = slots[key]["aliases"]
                name = aliases[0] if len(aliases) == 1 else annotations["xml_element"]
                children.append(_record_tree(item, kind, name))
        else:
            attributes[slots[key]["aliases"][0]] = str(value)
    return element, attributes, text if not children else "", children


@pytest.mark.parametrize("path", DOCUMENTS, ids=lambda p: p.name)
def test_each_document_follows_its_xsd(path):
    schema = xsd(conversion.DOCUMENTS[path][0])
    assert schema.validate(_parse(path)), schema.error_log


@pytest.mark.parametrize("path", DOCUMENTS, ids=lambda p: p.name)
def test_each_document_makes_a_record_of_its_class(path):
    assert conversion.record(path)[0] == conversion.DOCUMENTS[path][1]


@pytest.mark.parametrize("path", DOCUMENTS, ids=lambda p: p.name)
def test_each_record_follows_the_committed_json_schema(path):
    class_name, record = conversion.record(path)
    schema = json.loads(COMMITTED.read_text(encoding="utf-8"))
    schema = {"$ref": f"#/$defs/{class_name}", "$defs": schema["$defs"]}
    validator = jsonschema.validators.validator_for(schema)(schema)
    found = list(validator.iter_errors(record))
    assert not found, [e.message[:200] for e in found[:5]]


@pytest.mark.parametrize("path", DOCUMENTS, ids=lambda p: p.name)
def test_a_separate_walk_finds_what_the_record_holds(path):
    class_name, record = conversion.record(path)
    root = _parse(path).getroot()
    expected = _xml_tree(root)
    assert _record_tree(record, class_name, expected[0]) == expected


@pytest.mark.parametrize("path", conversion.WHOLE_SCHEMAS, ids=lambda p: p.name)
def test_each_whole_schema_keeps_the_rules(path):
    """FIX's own documents break none of the rules JSON Schema cannot state."""
    assert not rule_errors(conversion.record(path)[1])


def test_the_documents_are_not_trivial():
    """These kinds of element appear, so the walks above cannot pass on nothing. FIX's documents
    hold no ref, set or choice, so tests/data/valid/ alone exercises those."""
    tags = set()
    for path in DOCUMENTS:
        tags |= {
            etree.QName(e).localname
            for e in _parse(path).iter()
            if isinstance(e.tag, str)
        }
    assert tags >= {
        "messageSchema", "messages", "types", "type", "composite", "enum", "validValue",
        "message", "field", "group", "data",
    }  # fmt: skip


def test_the_converter_refuses_what_the_schema_has_no_place_for(tmp_path):
    """A stray attribute, element or text stops the run, so nothing is lost without notice."""
    convert = conversion.converter()
    template = (
        '<sbe:messageSchema xmlns:sbe="http://fixprotocol.io/2016/sbe" version="0"{a}>'
        "{t}<types>{c}</types></sbe:messageSchema>"
    )
    for attribute, text, child in (
        (' extra="1"', "", ""),
        ("", "stray", ""),
        ("", "", "<unknown/>"),
    ):
        path = tmp_path / "bad.xml"
        path.write_text(template.format(a=attribute, t=text, c=child), encoding="utf-8")
        with pytest.raises(convert.Unmodelled):
            convert.convert(path)


V2_ROOT = (
    '<messageSchema xmlns="http://fixprotocol.io/2017/sbe" version="0" '
    'xmlns:xi="http://www.w3.org/2001/XInclude">{}</messageSchema>'
)


@pytest.mark.parametrize(
    ("include", "reason"),
    [
        ("<xi:include/>", "names no file"),
        ('<xi:include href="types.xml" parse="text"/>', "text or for part"),
        ('<xi:include href="types.xml" xpointer="t"/>', "text or for part"),
        ('<xi:include href="types.xml"><xi:fallback/></xi:include>', "fallback"),
    ],
    ids=["no-href", "parse-text", "xpointer", "fallback"],
)
def test_the_converter_refuses_an_include_it_cannot_take(tmp_path, include, reason):
    convert = conversion.converter()
    path = tmp_path / "bad.xml"
    path.write_text(V2_ROOT.format(include), encoding="utf-8")
    with pytest.raises(convert.Unmodelled, match=reason):
        convert.convert(path)


@pytest.mark.parametrize(
    ("text", "reason"),
    [
        (V2_ROOT.format('<xi:include href="nope.xml"/>'), "No such file"),
        (V2_ROOT.format("<types>"), "mismatched tag"),
        (V2_ROOT.format("<types/>").replace('version="0"', 'version="0x1"'), "0x1"),
        (V2_ROOT.format("<unknown/>"), "holds <unknown>"),
    ],
    ids=["missing-file", "malformed-xml", "not-a-number", "unmodelled"],
)
def test_the_command_stops_with_one_line_on_a_bad_document(
    tmp_path, capsys, text, reason
):
    convert = conversion.converter()
    path = tmp_path / "bad.xml"
    path.write_text(text, encoding="utf-8")
    assert convert.main([str(path)]) == 1
    out, err = capsys.readouterr()
    assert out == ""
    assert err.count("\n") == 1 and reason in err


def test_the_converter_refuses_an_include_outside_its_folder(tmp_path):
    convert = conversion.converter()
    path = tmp_path / "bad.xml"
    path.write_text(
        '<messageSchema xmlns="http://fixprotocol.io/2017/sbe" version="0" '
        'xmlns:xi="http://www.w3.org/2001/XInclude">'
        '<xi:include href="../secret.xml"/></messageSchema>',
        encoding="utf-8",
    )
    with pytest.raises(convert.Unmodelled, match="leaves the document's folder"):
        convert.convert(path)
