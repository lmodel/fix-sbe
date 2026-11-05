#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml>=6"]
# ///
"""Turn an SBE document in XML into the YAML record the LinkML schema describes.

The namespace of the root element says which edition a document follows. A record keeps every
attribute under the slot whose alias it is, keeps a composite's members in document order, and
names each encoding's class in encoding_kind, because an XML element's name stands for its
class. Whatever the schema has no place for stops the run, so nothing is lost without notice.

An XInclude brings in a file from the document's own folder only. Usage::

    uv run scripts/sbe_xml_to_yaml.py FILE [--out FILE]
"""

from __future__ import annotations

import argparse
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import yaml

V1 = "http://fixprotocol.io/2016/sbe"
V2 = "http://fixprotocol.io/2017/sbe"
EDITIONS = {V1: "V1", V2: "V2"}
XML = "{http://www.w3.org/XML/1998/namespace}"
XSI = "{http://www.w3.org/2001/XMLSchema-instance}"
XINCLUDE = "{http://www.w3.org/2001/XInclude}include"

# Each XML attribute, the slot that holds it and, for a number, its conversion.
ATTRIBUTES = {
    "alignment": "alignment",
    "blockLength": "block_length",
    "byteOrder": "byte_order",
    "characterEncoding": "character_encoding",
    "deprecated": "deprecated_since",
    "description": "description",
    "dimensionType": "dimension_type",
    "encodingType": "encoding_type",
    "epoch": "time_epoch",
    "headerType": "header_type",
    "id": "sbe_id",
    "length": "array_length",
    "maxValue": "max_value",
    "minValue": "min_value",
    "name": "symbolic_name",
    "nullValue": "null_value",
    "offset": "offset",
    "package": "schema_package",
    "presence": "presence",
    "primitiveType": "primitive_type",
    "semanticType": "semantic_type",
    "semanticVersion": "semantic_version",
    "sinceVersion": "since_version",
    "timeUnit": "time_unit",
    "type": "encoding_name",
    "valueRef": "value_ref",
    "version": "schema_version",
    "xml:base": "xml_base",
}
NUMBERS = {
    "alignment",
    "array_length",
    "block_length",
    "deprecated_since",
    "offset",
    "sbe_id",
    "schema_version",
    "since_version",
}


class Unmodelled(ValueError):
    """The document holds something the schema has no place for."""


def _local(element: ET.Element) -> str:
    return element.tag.rsplit("}", 1)[-1]


def _attributes(element: ET.Element) -> dict:
    """The element's attributes under their slots, leaving out where-to-find-the-XSD hints."""
    record = {}
    for name, value in element.attrib.items():
        if name.startswith(XSI):
            continue
        key = "xml:base" if name == f"{XML}base" else name
        if key not in ATTRIBUTES:
            raise Unmodelled(f"<{_local(element)}> has an attribute {name}")
        slot = ATTRIBUTES[key]
        record[slot] = int(value) if slot in NUMBERS else value
    return record


def _text(element: ET.Element) -> str:
    """The element's text with white space collapsed, as XML Schema's token type does."""
    return " ".join((element.text or "").split())


def _no_text(element: ET.Element) -> None:
    """Refuse text the schema has no place for, on an element the XSD calls mixed."""
    parts = [element.text] + [child.tail for child in element]
    if any(part and part.strip() for part in parts):
        raise Unmodelled(f"<{_local(element)}> holds text")


def _simple(element: ET.Element, kind: str) -> dict:
    record = {"encoding_kind": kind, **_attributes(element)}
    text = _text(element)
    if text:
        record["element_value"] = text
    if len(element):
        raise Unmodelled(f"<{_local(element)}> holds child elements")
    return record


def _valid_value(element: ET.Element) -> dict:
    return {**_attributes(element), "valid_value": _text(element)}


def _choice(element: ET.Element) -> dict:
    return {**_attributes(element), "bit_position": int(_text(element))}


def _children(element: ET.Element, name: str, build) -> list:
    found = []
    for child in element:
        if _local(child) != name:
            raise Unmodelled(f"<{_local(element)}> holds <{_local(child)}>")
        found.append(build(child))
    return found


def _enum(element: ET.Element, edition: str) -> dict:
    _no_text(element)
    return {
        "encoding_kind": f"SbeEnum{edition}",
        **_attributes(element),
        "valid_values": _children(element, "validValue", _valid_value),
    }


def _set(element: ET.Element, edition: str) -> dict:
    _no_text(element)
    return {
        "encoding_kind": f"SbeSet{edition}",
        **_attributes(element),
        "choices": _children(element, "choice", _choice),
    }


def _ref(element: ET.Element, edition: str) -> dict:
    _no_text(element)
    if len(element):
        raise Unmodelled("<ref> holds child elements")
    return {"encoding_kind": f"SbeRef{edition}", **_attributes(element)}


def _composite(element: ET.Element, edition: str) -> dict:
    _no_text(element)
    member_type = "SbeMemberTypeV2" if edition == "V2" else "SbeSimpleTypeV1"
    builders = {
        "type": lambda child: _simple(child, member_type),
        "enum": lambda child: _enum(child, edition),
        "set": lambda child: _set(child, edition),
        "composite": lambda child: _composite(child, edition),
        "ref": lambda child: _ref(child, edition),
    }
    members = []
    for child in element:
        if _local(child) not in builders:
            raise Unmodelled(f"<composite> holds <{_local(child)}>")
        members.append(builders[_local(child)](child))
    return {
        "encoding_kind": f"SbeComposite{edition}",
        **_attributes(element),
        "composite_members": members,
    }


def _encoding_set(element: ET.Element, edition: str) -> dict:
    _no_text(element)
    builders = {
        "type": lambda child: _simple(child, f"SbeSimpleType{edition}"),
        "composite": lambda child: _composite(child, edition),
        "enum": lambda child: _enum(child, edition),
        "set": lambda child: _set(child, edition),
    }
    encodings = []
    for child in element:
        if _local(child) not in builders:
            raise Unmodelled(f"<types> holds <{_local(child)}>")
        encodings.append(builders[_local(child)](child))
    return {**_attributes(element), "encodings": encodings}


def _field(element: ET.Element, edition: str) -> dict:
    record = _attributes(element)
    text = _text(element)
    if edition == "V2" and text:
        record["element_value"] = text
    elif text:
        raise Unmodelled("a <field> of SBE 1.0 holds text")
    if len(element):
        raise Unmodelled(f"<{_local(element)}> holds child elements")
    return record


def _block(element: ET.Element, edition: str) -> dict:
    _no_text(element)
    record = _attributes(element)
    lists = {
        "field": ("block_fields", _field),
        "group": ("repeating_groups", _block),
        "data": ("var_data_fields", _field),
    }
    for child in element:
        name = _local(child)
        if name not in lists:
            raise Unmodelled(f"<{_local(element)}> holds <{name}>")
        slot, build = lists[name]
        record.setdefault(slot, []).append(build(child, edition))
    return record


def _message_set(element: ET.Element, edition: str) -> dict:
    _no_text(element)
    messages = _children(element, "message", lambda child: _block(child, edition))
    return {**_attributes(element), "messages": messages}


def _message_schema(element: ET.Element, edition: str) -> dict:
    _no_text(element)
    record = _attributes(element)
    for child in element:
        name = _local(child)
        if name == "types":
            record.setdefault("encoding_sets", []).append(_encoding_set(child, edition))
        elif name == "message" and edition == "V1":
            record.setdefault("messages", []).append(_block(child, edition))
        elif name == "messages" and edition == "V2":
            record.setdefault("message_sets", []).append(_message_set(child, edition))
        else:
            raise Unmodelled(f"<messageSchema> holds <{name}>")
    return record


def _expand(root: ET.Element, folder: Path) -> None:
    """Replace each XInclude under the root with the root of the file it names."""
    for parent in root.iter():
        for index, child in enumerate(list(parent)):
            if child.tag != XINCLUDE:
                continue
            href = child.attrib["href"]
            target = (folder / href).resolve()
            if target.parent != folder.resolve():
                raise Unmodelled(f"an XInclude leaves the document's folder: {href}")
            included = ET.parse(target).getroot()
            included.tail = child.tail
            parent[index] = included


def convert(path: Path) -> tuple[str, dict]:
    """The class a document's root element stands for, and its record."""
    root = ET.parse(path).getroot()
    _expand(root, path.parent)
    namespace, _, name = root.tag[1:].partition("}")
    if namespace not in EDITIONS:
        raise Unmodelled(f"the root element is in the namespace {namespace!r}")
    edition = EDITIONS[namespace]
    if name == "messageSchema":
        return f"SbeMessageSchema{edition}", _message_schema(root, edition)
    if name == "types" and edition == "V2":
        return "SbeEncodingSetV2", _encoding_set(root, edition)
    if name == "messages" and edition == "V2":
        return "SbeMessageSetV2", _message_set(root, edition)
    raise Unmodelled(f"the root element is <{name}>")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("file", type=Path, help="The XML file to read")
    parser.add_argument(
        "--out", type=Path, help="Write here instead of standard output"
    )
    args = parser.parse_args(argv)
    _, record = convert(args.file)
    text = yaml.safe_dump(record, sort_keys=False, allow_unicode=True)
    if args.out:
        args.out.write_text(text, encoding="utf-8")
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
