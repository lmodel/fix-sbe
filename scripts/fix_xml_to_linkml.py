#!/usr/bin/env python3
"""Convert a FIX Simple Binary Encoding (SBE) XML instance into LinkML YAML.

The generated LinkML schema
(``src/fix_sbe/schema/fix_sbe.yaml``,
the umbrella schema importing the v1.0 + v2.0 overlays + common module) expects
data in JSON-shaped form, but the upstream test instances are XML
(``<sbe:messageSchema>``, ``<messages>``, ``<types>``). This script bridges
them so ``linkml-validate`` can ingest an FIX-Trading-Community SBE sample
directly.

Transformations applied:

* Strip namespace prefixes from tags and attributes (``sbe:``, ``xsi:``,
  ``xi:``, ``xml:``).
* Convert XML names from camelCase to snake_case to match LinkML slot names.
* Drop XML-metadata attributes that have no LinkML counterpart
  (``xsi:schemaLocation``, ``xsi:type``, ``xmlns:*``, ``xml:base``).
* Force any slot the schema declares ``multivalued: true`` into a list, even
  when only one occurrence is present.
* Collapse single-child mixed content into a bare string when the slot range
  is a scalar / enum / type.
* Resolve the right SBE version overlay (``V1`` vs ``V2``) from the XML
  namespace URI so the root element maps to the correct LinkML class.

Version inference uses the namespace URI(s) observed in the XML:

* ``http://fixprotocol.io/sbe/rc3``,
  ``http://fixprotocol.io/sbe/rc4``,
  ``http://fixprotocol.io/2016/sbe``         -> SBE 1.0 (``...V1``)
* ``http://fixprotocol.io/2017/sbe``         -> SBE 2.0 (``...V2``)

Root-tag mapping (with the detected version suffix applied):

* ``messageSchema`` -> ``MessageSchemaV1`` / ``MessageSchemaV2``
* ``messages``      -> ``MessagesV2``  (v2 XInclude fragment)
* ``types``         -> ``TypesV2``     (v2 XInclude fragment)

Usage::

    python3 scripts/fix_xml_to_linkml.py \\
        --schema src/fix_sbe/schema/fix_sbe.yaml \\
        --target-class MessageSchemaV1 \\
        --in tests/data/third-party/fix-sbe/v1-0-STANDARD/Examples.xml \\
        --out /tmp/Examples.yaml

If ``--target-class`` is omitted it is inferred from the XML root tag plus
the detected SBE version.

Only the Python standard library plus PyYAML are required.
"""
from __future__ import annotations

import argparse
import re
import sys
import xml.etree.ElementTree as ET
from collections import OrderedDict
from pathlib import Path
from typing import Any

import yaml

# ---------------------------------------------------------------------------
# XML helpers
# ---------------------------------------------------------------------------

# Namespaces whose attributes should be entirely dropped at conversion time
# (they carry XML processing metadata, not domain data).
_DROP_NS = {
    'http://www.w3.org/2001/XMLSchema-instance',
    'http://www.w3.org/XML/1998/namespace',  # xml:base only - keep xml:lang
}


def local_name(tag: str) -> str:
    return tag.split('}', 1)[1] if '}' in tag else tag


def attr_local_name(name: str) -> str | None:
    """Return the local part of an attribute name, or ``None`` to drop it."""
    if name.startswith('{'):
        ns = name[1:].split('}', 1)[0]
        local = name.split('}', 1)[1]
        if ns in _DROP_NS:
            return None
        return local
    if name == 'xmlns' or name.startswith('xmlns:'):
        return None
    return name


_SNAKE1 = re.compile(r'([A-Z]+)([A-Z][a-z])')
_SNAKE2 = re.compile(r'([a-z0-9])([A-Z])')


def snake(name: str) -> str:
    s = _SNAKE1.sub(r'\1_\2', name)
    s = _SNAKE2.sub(r'\1_\2', s)
    return s.lower().replace('-', '_')


def pascal(name: str) -> str:
    """PascalCase derived from a snake_case or camelCase XSD name."""
    s = re.sub(r'(_t|_enum)$', '', name)
    parts = re.split(r'[_\-]', s)
    parts = [p[:1].upper() + p[1:] for p in parts if p]
    return ''.join(parts)


# ---------------------------------------------------------------------------
# Schema-awareness: walk the LinkML schema YAML to learn each class's slot map
# ---------------------------------------------------------------------------

class SchemaIndex:
    """Indexes a LinkML schema for slot lookups by class."""

    def __init__(self, schema: dict):
        self.schema = schema
        self.classes: dict[str, dict] = schema.get('classes') or {}
        self.slots: dict[str, dict] = schema.get('slots') or {}
        self.enums: dict[str, dict] = schema.get('enums') or {}
        self.types: dict[str, dict] = schema.get('types') or {}
        # Caches
        self._effective_attrs: dict[str, dict] = {}

    def effective_attributes(self, class_name: str) -> dict[str, dict]:
        """Return the merged slot map for a class including is_a + mixins."""
        if class_name in self._effective_attrs:
            return self._effective_attrs[class_name]
        out: dict[str, dict] = {}
        cls = self.classes.get(class_name)
        if cls is None:
            self._effective_attrs[class_name] = out
            return out
        # Walk is_a chain (parents first so child overrides)
        chain: list[str] = []
        seen: set[str] = set()
        cur = class_name
        while cur and cur not in seen:
            seen.add(cur)
            chain.append(cur)
            parent = (self.classes.get(cur) or {}).get('is_a')
            cur = parent
        for cls_name in reversed(chain):
            cdef = self.classes.get(cls_name) or {}
            # Mixins contribute too
            for m in cdef.get('mixins') or []:
                for k, v in self.effective_attributes(m).items():
                    out[k] = v
            # Class-local attributes
            for k, v in (cdef.get('attributes') or {}).items():
                out[k] = dict(v) if isinstance(v, dict) else {}
            # `slots:` list refs (point at schema-level definitions)
            for sname in cdef.get('slots') or []:
                if sname not in out:
                    out[sname] = dict(self.slots.get(sname) or {})
            # slot_usage refinements
            for k, override in (cdef.get('slot_usage') or {}).items():
                if k not in out:
                    out[k] = {}
                if isinstance(override, dict):
                    out[k] = {**out[k], **override}
        self._effective_attrs[class_name] = out
        return out

    def slot_range(self, class_name: str, slot_name: str) -> str | None:
        attrs = self.effective_attributes(class_name)
        return (attrs.get(slot_name) or {}).get('range')

    def is_multivalued(self, class_name: str, slot_name: str) -> bool:
        attrs = self.effective_attributes(class_name)
        return bool((attrs.get(slot_name) or {}).get('multivalued'))

    def has_slot(self, class_name: str, slot_name: str) -> bool:
        return slot_name in self.effective_attributes(class_name)

    def class_for_range(self, range_name: str) -> str | None:
        """Resolve a slot range to a class name (or None if scalar/enum/type)."""
        if range_name in self.classes:
            return range_name
        return None

    _PRIMITIVES = {'string', 'integer', 'decimal', 'float', 'double',
                   'boolean', 'date', 'datetime', 'time', 'uri'}

    def effective_primitive(self, range_name: str | None) -> str:
        """Walk the type-of chain to find the underlying LinkML primitive.

        Custom types like ``EP`` (``typeof: integer``) and ``Version``
        (``typeof: string``) need to be unwrapped so the converter can coerce
        XML text content to the right Python scalar.
        """
        if not range_name or range_name in self._PRIMITIVES:
            return range_name or 'string'
        if range_name in self.enums:
            return 'string'
        if range_name in self.classes:
            return 'class'  # signals "don't coerce, recurse"
        t = self.types.get(range_name)
        if t is None:
            return 'string'
        seen: set[str] = set()
        while t and range_name not in seen:
            seen.add(range_name)
            tof = t.get('typeof') if isinstance(t, dict) else None
            if not tof:
                base = t.get('base') if isinstance(t, dict) else None
                if base == 'str':
                    return 'string'
                return 'string'
            if tof in self._PRIMITIVES:
                return tof
            range_name = tof
            t = self.types.get(tof)
        return 'string'


# ---------------------------------------------------------------------------
# XML -> dict conversion (schema-driven)
# ---------------------------------------------------------------------------

# When emitting a slot whose range is a class, the converter needs to know the
# child class. We resolve recursively; the entry point is target_class.

def convert_xml(xml_path: Path, schema_index: SchemaIndex,
                target_class: str) -> dict:
    """Top-level: parse XML, return a dict matching schema layout."""
    tree = ET.parse(xml_path)
    return _convert_element(tree.getroot(), target_class, schema_index)


def _convert_element(elt: ET.Element, class_name: str,
                     idx: SchemaIndex) -> dict | str:
    """Recursively convert one XML element to a LinkML-shaped dict.

    Returns a bare string instead of dict when the element has no useful
    attributes and a single text node (mixed-content collapse).
    """
    attrs = idx.effective_attributes(class_name)
    extra_attr_slot = 'extra_attributes' if 'extra_attributes' in attrs else None

    out: "OrderedDict[str, Any]" = OrderedDict()
    extras: list[str] = []

    # ---- Attributes ----
    for raw_name, raw_value in elt.attrib.items():
        local = attr_local_name(raw_name)
        if local is None:
            continue
        slot = snake(local)
        if slot in attrs:
            range_name = (attrs[slot] or {}).get('range')
            out[slot] = _coerce_scalar(raw_value,
                                       idx.effective_primitive(range_name))
        elif extra_attr_slot:
            extras.append(f"{local}={raw_value}")
        # else: silently drop unrecognised attribute

    # ---- Children ----
    children_by_slot: "OrderedDict[str, list[Any]]" = OrderedDict()
    for child in elt:
        cname = local_name(child.tag)
        slot = snake(cname)
        if slot not in attrs:
            # Try the un-snaked form (matches LinkML aliases occasionally)
            alt = cname
            if alt in attrs:
                slot = alt
        if slot not in attrs:
            # Drop unknown child elements (e.g. DC element refinements not in
            # the local class's attributes)
            continue
        child_range = (attrs[slot] or {}).get('range') or 'string'
        child_class = idx.class_for_range(child_range)
        if child_class:
            child_value = _convert_element(child, child_class, idx)
        else:
            # Scalar range: take the element's text, ignore attributes
            child_value = _text_value(child, idx.effective_primitive(child_range))
        children_by_slot.setdefault(slot, []).append(child_value)

    # Merge children into out, respecting multivalued schema declarations.
    for slot, vals in children_by_slot.items():
        if idx.is_multivalued(class_name, slot):
            out[slot] = vals
        elif len(vals) == 1:
            out[slot] = vals[0]
        else:
            # Schema says single-valued but XML provided multiple. Keep first
            # and stash the rest in extras (best-effort).
            out[slot] = vals[0]

    # ---- Mixed text content ----
    text = (elt.text or '').strip()
    if text:
        if 'value' in attrs:
            out['value'] = _coerce_scalar(
                text,
                idx.effective_primitive((attrs['value'] or {}).get('range')))
        elif not out:
            # Pure text element with no other content / no value slot:
            # collapse to bare string (caller handles).
            return text

    # ---- xs:anyAttribute bucket ----
    if extras and extra_attr_slot:
        out[extra_attr_slot] = extras

    return out


def _coerce_scalar(text: str, range_name: str | None) -> Any:
    if range_name in ('integer',):
        try:
            return int(text)
        except ValueError:
            return text
    if range_name in ('float', 'double', 'decimal'):
        try:
            return float(text)
        except ValueError:
            return text
    if range_name == 'boolean':
        return text.lower() in ('true', '1')
    return text


def _text_value(elt: ET.Element, range_name: str | None) -> Any:
    """Get the textual content of a scalar-ranged element, ignoring attrs."""
    text = (elt.text or '').strip()
    if not text:
        # Maybe the element has only children with their own text - take
        # the concatenation of all descendant text.
        text = ''.join(elt.itertext()).strip()
    return _coerce_scalar(text, range_name)


# ---------------------------------------------------------------------------
# CLI / SBE version inference
# ---------------------------------------------------------------------------

# Namespace URI fragments that identify a given SBE major version.
_SBE_V1_NAMESPACE_FRAGMENTS = ('/sbe/rc3', '/sbe/rc4', '/2016/sbe')
_SBE_V2_NAMESPACE_FRAGMENTS = ('/2017/sbe',)

# Root XML tag -> bare LinkML class stem. The detected version suffix
# (``V1`` / ``V2``) is appended at runtime.
_ROOT_TO_CLASS_STEM = {
    'messageSchema': 'MessageSchema',
    'messages':      'Messages',
    'types':         'Types',
}


def _all_namespaces(root: ET.Element) -> set[str]:
    """Collect every namespace URI seen on ``root`` and its descendants."""
    out: set[str] = set()
    for elt in root.iter():
        if '}' in elt.tag:
            out.add(elt.tag.split('}', 1)[0][1:])
        for k in elt.attrib:
            if '}' in k:
                out.add(k.split('}', 1)[0][1:])
    return out


def detect_sbe_version(root: ET.Element) -> str:
    """Return ``'V1'`` or ``'V2'`` based on the XML namespaces present.

    Falls back to ``'V2'`` when no recognised SBE namespace is found.
    """
    nss = _all_namespaces(root)
    for ns in nss:
        if any(frag in ns for frag in _SBE_V1_NAMESPACE_FRAGMENTS):
            return 'V1'
    for ns in nss:
        if any(frag in ns for frag in _SBE_V2_NAMESPACE_FRAGMENTS):
            return 'V2'
    return 'V2'


def infer_target_class(xml_path: Path) -> str:
    root = ET.parse(xml_path).getroot()
    root_tag = local_name(root.tag)
    version = detect_sbe_version(root)
    stem = _ROOT_TO_CLASS_STEM.get(root_tag)
    if stem is not None:
        return f'{stem}{version}'
    return pascal(root_tag)


def main(argv: list[str] | None = None) -> int:
    here = Path(__file__).resolve().parent
    project_dir = here.parent
    default_schema = (project_dir / 'src' / 'fix_sbe'
                      / 'schema' / 'fix_sbe.yaml')

    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument('--schema', type=Path, default=default_schema,
                   help='path to the LinkML schema YAML')
    p.add_argument('--target-class', default=None,
                   help='LinkML class name to convert against. Inferred from '
                        'the XML root tag if omitted.')
    p.add_argument('--in', dest='input', type=Path, required=True,
                   help='input XML file')
    p.add_argument('--out', dest='output', type=Path,
                   help='output YAML path (default: <in>.yaml)')
    args = p.parse_args(argv)

    schema = yaml.safe_load(args.schema.read_text())
    # Merge locally-resolvable imports so SchemaIndex can see DC classes.
    for imp in schema.get("imports") or []:
        if ":" in imp:
            continue  # skip linkml:types etc.
        for ext in (".yaml", ".yml"):
            imp_path = args.schema.parent / (imp + ext)
            if imp_path.is_file():
                imp_schema = yaml.safe_load(imp_path.read_text())
                for section in ("classes", "slots", "types", "enums"):
                    base = schema.setdefault(section, {})
                    base.update(imp_schema.get(section) or {})
                break
    idx = SchemaIndex(schema)

    target = args.target_class or infer_target_class(args.input)
    if target not in idx.classes:
        print(f"ERROR: target class {target!r} not found in schema",
              file=sys.stderr)
        return 1

    converted = convert_xml(args.input, idx, target)
    out_path = args.output or args.input.with_suffix('.yaml')
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(yaml.safe_dump(_plain(converted), sort_keys=False,
                                       allow_unicode=True))
    print(f"Wrote {out_path} (target_class={target})", file=sys.stderr)
    return 0


def _plain(obj: Any) -> Any:
    """Recursively convert OrderedDicts to plain dicts for YAML serialisation."""
    if isinstance(obj, dict):
        return {k: _plain(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_plain(v) for v in obj]
    return obj


if __name__ == '__main__':
    sys.exit(main())
