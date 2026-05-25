#!/usr/bin/env python3
"""Convert FIX Simple Binary Encoding upstream XSDs into LinkML schemas.

Two upstream XSD versions are modelled side-by-side:

  * v1-0-STANDARD  (namespace ``http://fixprotocol.io/2016/sbe``)
  * v2-0-RC3       (namespace ``http://fixprotocol.io/2017/sbe``)

Each version produces a standalone, self-contained overlay schema
(``fix_sbe_v1_0.yaml`` and ``fix_sbe_v2_0.yaml``).  Every emitted class /
enum / type name carries a ``V1`` or ``V2`` suffix so the two overlays can
be imported side-by-side by the umbrella schema
(``fix_sbe.yaml``) without name collisions.

Per-class ``attributes:`` are emitted inline (no schema-level slot
promotion) so attribute / element names like ``name``, ``id``, ``type``
remain scoped to their owning class and don't clash across overlays.

Default inputs / outputs (relative to repo root):

    inputs:
      upstream-releases/fix-simple-binary-encoding/v1-0-STANDARD/resources/sbe.xsd
      upstream-releases/fix-simple-binary-encoding/v2-0-RC3/resources/xsd/sbe-2.0rc3.xsd
    outputs:
      src/fix_sbe/schema/fix_sbe_common.yaml
      src/fix_sbe/schema/fix_sbe_v1_0.yaml
      src/fix_sbe/schema/fix_sbe_v2_0.yaml
      src/fix_sbe/schema/fix_sbe.yaml

Run from the repo root::

    python3 scripts/schema_to_linkml.py

Only the Python standard library is required.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
import xml.etree.ElementTree as ET
from collections import OrderedDict
from pathlib import Path

XS = "{http://www.w3.org/2001/XMLSchema}"


# ---------------------------------------------------------------------------
# Helpers (string / XML)
# ---------------------------------------------------------------------------


def local(tag: str) -> str:
    return tag.split("}", 1)[1] if "}" in tag else tag


def nons(qname: str | None) -> str | None:
    if qname is None:
        return None
    return qname.split(":", 1)[1] if ":" in qname else qname


def doc_of(elt: ET.Element | None) -> str | None:
    if elt is None:
        return None
    ann = elt.find(f"{XS}annotation")
    if ann is None:
        return None
    parts = []
    for d in ann.findall(f"{XS}documentation"):
        txt = " ".join("".join(d.itertext()).split())
        if txt:
            parts.append(txt)
    joined = " ".join(parts)
    if len(joined) > 1200:
        joined = joined[:1197] + "..."
    return joined or None


_SNAKE1 = re.compile(r"([A-Z]+)([A-Z][a-z])")
_SNAKE2 = re.compile(r"([a-z0-9])([A-Z])")


def snake(name: str) -> str:
    s = _SNAKE1.sub(r"\1_\2", name)
    s = _SNAKE2.sub(r"\1_\2", s)
    return s.lower().replace("-", "_")


def pascal(name: str) -> str:
    """PascalCase, stripping XSD ``_t`` suffix used for SBE simpleTypes."""
    base = re.sub(r"_t$", "", name)
    parts = re.split(r"[_\-]", base)
    parts = [p[:1].upper() + p[1:] for p in parts if p]
    out = "".join(parts)
    return out[:1].upper() + out[1:] if out else out


# XSD primitive -> LinkML built-in type
PRIM: dict[str, str] = {
    "string": "string",
    "token": "string",
    "normalizedString": "string",
    "NMTOKEN": "string",
    "NCName": "string",
    "Name": "string",
    "QName": "string",
    "ID": "string",
    "IDREF": "string",
    "integer": "integer",
    "positiveInteger": "integer",
    "nonNegativeInteger": "integer",
    "int": "integer",
    "long": "integer",
    "short": "integer",
    "byte": "integer",
    "unsignedInt": "integer",
    "unsignedLong": "integer",
    "unsignedShort": "integer",
    "unsignedByte": "integer",
    "decimal": "decimal",
    "float": "float",
    "double": "double",
    "boolean": "boolean",
    "anyURI": "uri",
    "anyType": "string",
    "anySimpleType": "string",
}

# LinkML's built-in primitive type names — used as a guard when a typeof base
# resolves to a non-primitive (force fall-back to string).
_PRIMITIVES = {
    "string", "integer", "decimal", "float", "double", "boolean",
    "date", "datetime", "time", "uri",
}


# ---------------------------------------------------------------------------
# XSD parsing
# ---------------------------------------------------------------------------


def parse_xsd(path: Path) -> dict:
    tree = ET.parse(path)
    root = tree.getroot()
    out: dict = {
        "target_namespace": root.get("targetNamespace"),
        "version": root.get("version"),
        "schema_doc": doc_of(root),
        "simple_types": OrderedDict(),
        "complex_types": OrderedDict(),
        "attribute_groups": OrderedDict(),
        "elements": OrderedDict(),
    }
    for child in root:
        tag = local(child.tag)
        name = child.get("name")
        if not name:
            continue
        if tag == "simpleType":
            out["simple_types"][name] = parse_simple(child)
        elif tag == "complexType":
            out["complex_types"][name] = parse_complex(child)
        elif tag == "attributeGroup":
            out["attribute_groups"][name] = parse_attr_group(child)
        elif tag == "element":
            out["elements"][name] = parse_top_element(child)
    return out


def parse_simple(elt: ET.Element) -> dict:
    info: dict = {
        "doc": doc_of(elt),
        "kind": None,
        "base": None,
        "enums": [],
        "pattern": None,
        "min_length": None,
        "max_length": None,
    }
    r = elt.find(f"{XS}restriction")
    if r is not None:
        info["base"] = r.get("base")
        enums = []
        for enu in r.findall(f"{XS}enumeration"):
            enums.append({"value": enu.get("value"), "doc": doc_of(enu)})
        if enums:
            info["kind"] = "enum"
            info["enums"] = enums
        else:
            info["kind"] = "restriction"
        for facet, key in (
            ("pattern", "pattern"),
            ("minLength", "min_length"),
            ("maxLength", "max_length"),
        ):
            f = r.find(f"{XS}{facet}")
            if f is not None:
                info[key] = f.get("value")
    return info


def parse_complex(elt: ET.Element) -> dict:
    info: dict = {
        "doc": doc_of(elt),
        "abstract": elt.get("abstract") == "true",
        "mixed": elt.get("mixed") == "true",
        "base": None,
        "simple_extension_base": None,
        "elements": [],
        "attributes": [],
        "attribute_groups": [],
    }
    holder = elt
    cc = elt.find(f"{XS}complexContent")
    sc = elt.find(f"{XS}simpleContent")
    if cc is not None:
        ext = cc.find(f"{XS}extension")
        if ext is not None:
            info["base"] = ext.get("base")
            holder = ext
    elif sc is not None:
        ext = sc.find(f"{XS}extension")
        if ext is not None:
            info["simple_extension_base"] = ext.get("base")
            holder = ext
            info["mixed"] = True
    walk_holder(holder, info)
    return info


def walk_holder(holder: ET.Element, info: dict) -> None:
    for tag in ("sequence", "choice", "all"):
        for c in holder.findall(f"{XS}{tag}"):
            walk_particle(c, info, parent_unbounded=False)
    for a in holder.findall(f"{XS}attribute"):
        info["attributes"].append(parse_attribute(a))
    for ag in holder.findall(f"{XS}attributeGroup"):
        ref = ag.get("ref")
        if ref:
            info["attribute_groups"].append(nons(ref))


def walk_particle(
    particle: ET.Element,
    info: dict,
    parent_unbounded: bool,
    parent_is_choice: bool = False,
) -> None:
    cmax = particle.get("maxOccurs", "1")
    container_unbounded = (
        parent_unbounded or cmax == "unbounded" or (cmax.isdigit() and int(cmax) > 1)
    )
    is_choice = local(particle.tag) == "choice"
    children_optional = parent_is_choice or is_choice
    for child in particle:
        tag = local(child.tag)
        if tag == "element":
            info["elements"].append(
                parse_local_element(
                    child, container_unbounded, force_optional=children_optional
                )
            )
        elif tag in ("sequence", "choice", "all"):
            walk_particle(
                child, info, container_unbounded, parent_is_choice=children_optional
            )


def parse_local_element(
    elt: ET.Element, parent_unbounded: bool, force_optional: bool = False
) -> dict:
    ref = elt.get("ref")
    if ref:
        name = nons(ref)
        type_q = ref
        is_ref = True
    else:
        name = elt.get("name")
        type_q = elt.get("type")
        is_ref = False
    minocc = elt.get("minOccurs", "1")
    maxocc = elt.get("maxOccurs", "1")
    if parent_unbounded and maxocc == "1":
        maxocc = "unbounded"
    if force_optional and minocc == "1":
        minocc = "0"
    return {
        "name": name,
        "type": type_q,
        "ref": is_ref,
        "min_occurs": int(minocc) if minocc.isdigit() else 0,
        "max_occurs": maxocc,
        "doc": doc_of(elt),
    }


def parse_attribute(elt: ET.Element) -> dict:
    """Parse an <xs:attribute>. Inline enums (anonymous <xs:simpleType> with
    enumerations) are captured under ``inline_enum`` so the caller can lift
    them into a named LinkML enum and re-range the attribute accordingly.
    """
    info: dict = {
        "name": elt.get("name"),
        "type": elt.get("type"),
        "use": elt.get("use", "optional"),
        "default": elt.get("default"),
        "fixed": elt.get("fixed"),
        "doc": doc_of(elt),
        "inline_enum": None,
        "inline_restriction": None,
    }
    st = elt.find(f"{XS}simpleType")
    if st is not None:
        parsed = parse_simple(st)
        if parsed["kind"] == "enum":
            info["inline_enum"] = parsed
        elif parsed["kind"] == "restriction":
            info["inline_restriction"] = parsed
    return info


def parse_attr_group(elt: ET.Element) -> dict:
    info: dict = {"doc": doc_of(elt), "attributes": [], "attribute_groups": []}
    for a in elt.findall(f"{XS}attribute"):
        info["attributes"].append(parse_attribute(a))
    for ag in elt.findall(f"{XS}attributeGroup"):
        ref = ag.get("ref")
        if ref:
            info["attribute_groups"].append(nons(ref))
    return info


def parse_top_element(elt: ET.Element) -> dict:
    info: dict = {
        "doc": doc_of(elt),
        "type": elt.get("type"),
        "inline": None,
    }
    ct = elt.find(f"{XS}complexType")
    if ct is not None:
        info["inline"] = parse_complex(ct)
    return info


# ---------------------------------------------------------------------------
# Emitter — one overlay schema per SBE version.
# ---------------------------------------------------------------------------


class VersionEmitter:
    """Emit a single SBE version's overlay schema.

    All emitted PascalCase names (classes, enums, types) get suffixed with
    ``suffix`` (e.g. ``V1``, ``V2``) so two overlays can coexist under an
    umbrella schema without collision. Slot names stay short because every
    attribute is emitted inline as a per-class ``attributes:`` member — the
    name is scoped to its owning class.
    """

    def __init__(
        self,
        parsed: dict,
        suffix: str,
        subset: str,
        sbe_prefix_local: str,
        upstream_namespace: str,
    ) -> None:
        self.parsed = parsed
        self.suffix = suffix
        self.subset = subset
        # Local CURIE prefix used in exact_mappings for upstream identity, e.g.
        # ``sbe_v1`` -> http://fixprotocol.io/2016/sbe/. Distinct per version
        # because v1 and v2 sit in different XML target namespaces.
        self.sbe_prefix_local = sbe_prefix_local
        self.upstream_namespace = upstream_namespace
        self.classes: OrderedDict[str, OrderedDict] = OrderedDict()
        self.enums: OrderedDict[str, OrderedDict] = OrderedDict()
        self.types: OrderedDict[str, OrderedDict] = OrderedDict()
        # Registry mapping XSD name (complexType / simpleType / attributeGroup
        # / top-level element) -> {"kind": ..., "name": <linkml-name>}.
        self.registry: dict[str, dict] = {}

    # --------------- naming -------------------------------------------

    def cn(self, xsd_name: str) -> str:
        """Suffixed LinkML class/enum/type name from an XSD name."""
        return pascal(xsd_name) + self.suffix

    def upstream_curie(self, xsd_name: str) -> str:
        return f"{self.sbe_prefix_local}:{xsd_name}"

    # --------------- registry population ------------------------------

    def build_registry(self) -> None:
        for n, info in self.parsed["simple_types"].items():
            kind = "enum" if info["kind"] == "enum" else "type"
            self.registry[n] = {"kind": kind, "name": self.cn(n)}
        for n in self.parsed["complex_types"]:
            self.registry[n] = {"kind": "class", "name": self.cn(n)}
        for n in self.parsed["attribute_groups"]:
            self.registry[n] = {"kind": "mixin", "name": self.cn(n)}
        for n in self.parsed["elements"]:
            self.registry[n] = {"kind": "class", "name": self.cn(n)}

    def resolve_range(self, qname: str | None) -> tuple[str, bool]:
        """(linkml_name, is_class_like) for an XSD QName."""
        if not qname:
            return ("string", False)
        if ":" in qname:
            prefix, name = qname.split(":", 1)
        else:
            prefix, name = "", qname
        if prefix in ("xs", "xsd"):
            return (PRIM.get(name, "string"), False)
        if name in self.registry:
            entry = self.registry[name]
            return (entry["name"], entry["kind"] in ("class", "enum", "mixin"))
        return ("string", False)

    # --------------- shared synthetic enums ---------------------------

    def lift_inline_enum(
        self,
        attr_name: str,
        parsed_enum: dict,
        owner_xsd: str,
    ) -> str:
        """Create (or reuse) a named LinkML enum from an inline <xs:simpleType>.

        The enum is named PascalCase(attr_name) + suffix (e.g. ``ByteOrderV2``).
        If a name collision arises across attributes, a numeric counter is
        appended to keep both definitions distinct.
        """
        base = pascal(attr_name) + self.suffix
        target = base
        # Two attribute uses (e.g. byteOrder in messageSchema vs another) with
        # identical value sets would dedupe by value-set equality.
        n = 2
        while target in self.enums:
            existing = self.enums[target]
            existing_values = list((existing.get("permissible_values") or {}).keys())
            new_values = [e["value"] for e in parsed_enum["enums"]]
            if existing_values == new_values:
                return target
            target = f"{base}_{n}"
            n += 1
        perm: OrderedDict = OrderedDict()
        for e in parsed_enum["enums"]:
            body: OrderedDict = OrderedDict()
            if e["doc"]:
                body["description"] = e["doc"]
            perm[e["value"]] = body if body else None
        out: OrderedDict = OrderedDict()
        out["description"] = (
            f"Inline enumeration lifted from XSD attribute "
            f"``{attr_name}`` on ``{owner_xsd}``."
        )
        out["enum_uri"] = f"fix_sbe:{target}"
        out["in_subset"] = [self.subset]
        out["permissible_values"] = perm
        self.enums[target] = out
        return target

    # --------------- simple types -------------------------------------

    def emit_simple_type(self, src_name: str, info: dict) -> None:
        ln = self.cn(src_name)
        if info["kind"] == "enum":
            perm: OrderedDict = OrderedDict()
            for e in info["enums"]:
                body: OrderedDict = OrderedDict()
                if e["doc"]:
                    body["description"] = e["doc"]
                perm[e["value"]] = body if body else None
            out: OrderedDict = OrderedDict()
            if info["doc"]:
                out["description"] = info["doc"]
            out["enum_uri"] = f"fix_sbe:{ln}"
            out["exact_mappings"] = [self.upstream_curie(src_name)]
            if src_name != ln:
                out["aliases"] = [src_name]
            out["in_subset"] = [self.subset]
            out["permissible_values"] = perm
            self.enums[ln] = out
            return
        base_range, _ = self.resolve_range(info["base"])
        if base_range not in _PRIMITIVES:
            base_range = "string"
        out = OrderedDict()
        if info["doc"]:
            out["description"] = info["doc"]
        out["typeof"] = base_range
        out["uri"] = f"fix_sbe:{ln}"
        out["exact_mappings"] = [self.upstream_curie(src_name)]
        if src_name != ln:
            out["aliases"] = [src_name]
        out["in_subset"] = [self.subset]
        if info["pattern"]:
            out["pattern"] = info["pattern"]
        anno: OrderedDict = OrderedDict()
        if info["min_length"]:
            anno["xsd_min_length"] = int(info["min_length"])
        if info["max_length"]:
            anno["xsd_max_length"] = int(info["max_length"])
        if anno:
            out["annotations"] = anno
        self.types[ln] = out

    # --------------- attribute / element collection -------------------

    def attr_body(
        self,
        a: dict,
        owner_xsd: str,
    ) -> tuple[str, OrderedDict]:
        slot_name = snake(a["name"])
        # Resolve range: inline anonymous enum > named type > string default.
        if a.get("inline_enum"):
            rng = self.lift_inline_enum(a["name"], a["inline_enum"], owner_xsd)
        elif a.get("type"):
            rng, _ = self.resolve_range(a["type"])
        else:
            rng = "string"
        body: OrderedDict = OrderedDict()
        body["range"] = rng
        if a.get("doc"):
            body["description"] = a["doc"]
        if a.get("use") == "required":
            body["required"] = True
        if a.get("fixed") is not None:
            body["equals_string"] = a["fixed"]
            body["ifabsent"] = f"string({a['fixed']})"
        elif a.get("default") is not None:
            body["ifabsent"] = f"string({a['default']})"
        body["slot_uri"] = f"fix_sbe:{slot_name}"
        body["exact_mappings"] = [self.upstream_curie(a["name"])]
        if slot_name != a["name"]:
            body["aliases"] = [a["name"]]
        return slot_name, body

    def collect_attributes(
        self,
        info: dict,
        owner_xsd: str,
        include_mixed_value: bool,
    ) -> OrderedDict:
        attrs: OrderedDict = OrderedDict()
        # Child elements first (so they sort above the XML attributes in docs).
        for el in info.get("elements", []) or []:
            xsd_name = el["name"]
            slot_name = snake(xsd_name)
            rng = "string"
            is_class_like = False
            if el.get("ref"):
                entry = self.registry.get(xsd_name)
                if entry:
                    rng = entry["name"]
                    is_class_like = entry["kind"] in ("class", "enum", "mixin")
            else:
                rng, is_class_like = self.resolve_range(el.get("type"))
            body: OrderedDict = OrderedDict()
            body["range"] = rng
            if el.get("doc"):
                body["description"] = el["doc"]
            unbounded = el["max_occurs"] == "unbounded" or (
                isinstance(el["max_occurs"], str)
                and el["max_occurs"].isdigit()
                and int(el["max_occurs"]) > 1
            )
            if unbounded:
                body["multivalued"] = True
                if is_class_like:
                    body["inlined"] = True
                    body["inlined_as_list"] = True
            if el["min_occurs"] >= 1:
                body["required"] = True
            body["slot_uri"] = f"fix_sbe:{slot_name}"
            body["exact_mappings"] = [self.upstream_curie(xsd_name)]
            if slot_name != xsd_name:
                body["aliases"] = [xsd_name]
            attrs[slot_name] = body
        # XML attributes.
        for a in info.get("attributes", []) or []:
            if not a.get("name"):
                continue
            slot_name, body = self.attr_body(a, owner_xsd)
            attrs[slot_name] = body
        # Mixed-content text. Most SBE simpleContent extensions hold a default
        # or constant value (e.g. <type>-3</type>); modelled as a ``value``
        # slot of range string.
        if include_mixed_value and "value" not in attrs:
            attrs["value"] = OrderedDict([
                ("range", "string"),
                (
                    "description",
                    "Text content of the element. For SBE this carries the "
                    "constant or default value (e.g. ``<type "
                    "presence='constant'>-3</type>``).",
                ),
            ])
        return attrs

    # --------------- emit attributeGroup as mixin --------------------

    def emit_attr_group(self, src_name: str, info: dict) -> None:
        ln = self.cn(src_name)
        out: OrderedDict = OrderedDict()
        if info["doc"]:
            out["description"] = info["doc"]
        out["mixin"] = True
        out["class_uri"] = f"fix_sbe:{ln}"
        out["exact_mappings"] = [self.upstream_curie(src_name)]
        if src_name != ln:
            out["aliases"] = [src_name]
        out["in_subset"] = [self.subset]
        attrs: OrderedDict = OrderedDict()
        for a in info["attributes"]:
            if not a.get("name"):
                continue
            slot_name, body = self.attr_body(a, src_name)
            attrs[slot_name] = body
        if attrs:
            out["attributes"] = attrs
        self.classes[ln] = out

    # --------------- emit complexType as class ------------------------

    def emit_complex(
        self,
        src_name: str,
        info: dict,
        tree_root: bool = False,
    ) -> None:
        ln = self.cn(src_name)
        out: OrderedDict = OrderedDict()
        if info["doc"]:
            out["description"] = info["doc"]
        if info["abstract"]:
            out["abstract"] = True
        # Inheritance via complexContent extension.
        if info["base"]:
            bname = nons(info["base"])
            entry = self.registry.get(bname)
            if entry and entry["kind"] == "class":
                out["is_a"] = entry["name"]
        if tree_root:
            out["tree_root"] = True
        # Mixin attributeGroups.
        mixins = []
        for ag in info.get("attribute_groups", []) or []:
            entry = self.registry.get(ag)
            if entry:
                mixins.append(entry["name"])
        if mixins:
            out["mixins"] = mixins
        out["class_uri"] = f"fix_sbe:{ln}"
        out["exact_mappings"] = [self.upstream_curie(src_name)]
        if src_name != ln:
            out["aliases"] = [src_name]
        out["in_subset"] = [self.subset]
        attrs = self.collect_attributes(
            info,
            owner_xsd=src_name,
            include_mixed_value=info.get("mixed", False)
            or bool(info.get("simple_extension_base")),
        )
        if attrs:
            out["attributes"] = attrs
        if info.get("simple_extension_base"):
            out.setdefault("annotations", OrderedDict())[
                "xsd_simple_extension"
            ] = info["simple_extension_base"]
        self.classes[ln] = out

    # --------------- emit top-level element ---------------------------

    def emit_top_element(
        self,
        src_name: str,
        info: dict,
        tree_root: bool = False,
    ) -> None:
        ln = self.cn(src_name)
        if info.get("inline"):
            inline = info["inline"]
            self.emit_complex(src_name, inline, tree_root=tree_root)
            # Use the element's own annotation as the class description when
            # the inner complexType has none.
            if info.get("doc") and not self.classes[ln].get("description"):
                self.classes[ln]["description"] = info["doc"]
            return
        if info.get("type"):
            rng, _ = self.resolve_range(info["type"])
            out: OrderedDict = OrderedDict()
            if info.get("doc"):
                out["description"] = info["doc"]
            out["is_a"] = rng
            if tree_root:
                out["tree_root"] = True
            out["class_uri"] = f"fix_sbe:{ln}"
            out["exact_mappings"] = [self.upstream_curie(src_name)]
            if src_name != ln:
                out["aliases"] = [src_name]
            out["in_subset"] = [self.subset]
            self.classes[ln] = out

    # --------------- run ----------------------------------------------

    def run(self, tree_root_element: str) -> None:
        self.build_registry()
        # Mixins first so emit_complex can reference them.
        for n, info in self.parsed["attribute_groups"].items():
            self.emit_attr_group(n, info)
        for n, info in self.parsed["simple_types"].items():
            self.emit_simple_type(n, info)
        for n, info in self.parsed["complex_types"].items():
            self.emit_complex(n, info)
        for n, info in self.parsed["elements"].items():
            self.emit_top_element(
                n, info, tree_root=(n == tree_root_element)
            )


# ---------------------------------------------------------------------------
# Phase 2 — common-overlay promotion via structural equality
# ---------------------------------------------------------------------------

# Regex matching version-suffixed PascalCase identifiers anywhere in a string.
_VERSION_SUFFIX_RE = re.compile(r"(?<![A-Za-z0-9_])([A-Z][A-Za-z0-9_]*?)V[12](?![A-Za-z0-9_])")

# Body fields that carry identity / provenance and must be stripped before
# comparing two entities for structural equality.
_IDENTITY_FIELDS = {
    "class_uri", "slot_uri", "enum_uri", "uri",
    "exact_mappings", "aliases", "in_subset", "description",
}


def _strip_version_in_str(s: str) -> str:
    return _VERSION_SUFFIX_RE.sub(r"\1", s)


def _normalize_for_compare(value):
    """Recursively strip identity fields and remove ``V1``/``V2`` suffixes
    from any PascalCase identifier-shaped substring so two entities that
    differ only by version-suffixed references compare equal."""
    if isinstance(value, dict):
        out: OrderedDict = OrderedDict()
        for k, v in value.items():
            if k in _IDENTITY_FIELDS:
                continue
            out[k] = _normalize_for_compare(v)
        return out
    if isinstance(value, list):
        return [_normalize_for_compare(x) for x in value]
    if isinstance(value, str):
        return _strip_version_in_str(value)
    return value


def _rewrite_refs(value, renames: dict[str, str]):
    """Walk a nested structure and rewrite any string equal to a key in
    ``renames`` (whole-string match) to its mapped value."""
    if isinstance(value, OrderedDict):
        out = OrderedDict()
        for k, v in value.items():
            out[k] = _rewrite_refs(v, renames)
        return out
    if isinstance(value, dict):
        return {k: _rewrite_refs(v, renames) for k, v in value.items()}
    if isinstance(value, list):
        return [_rewrite_refs(x, renames) for x in value]
    if isinstance(value, str) and value in renames:
        return renames[value]
    return value


def _strip_suffix(name: str, suffix: str) -> str | None:
    return name[: -len(suffix)] if name.endswith(suffix) else None


def _merged_description(body_v1: dict, body_v2: dict) -> str | None:
    """Prefer v2's description (newer spec); fall back to v1."""
    d2 = body_v2.get("description")
    d1 = body_v1.get("description")
    return d2 or d1


def _build_common_body(
    body_v1: OrderedDict,
    body_v2: OrderedDict,
    common_name: str,
    kind: str,
    renames_v1: dict[str, str],
    renames_v2: dict[str, str],
) -> OrderedDict:
    """Build the common-overlay entity body by taking v2 as the base
    (after applying renames), restoring identity fields with shared values,
    and merging exact_mappings / aliases from both versions."""
    base = _rewrite_refs(body_v2, renames_v2)
    out: OrderedDict = OrderedDict()
    if base.get("description"):
        out["description"] = base["description"]
    elif body_v1.get("description"):
        out["description"] = _rewrite_refs(body_v1["description"], renames_v1)
    desc = _merged_description(body_v1, body_v2)
    if desc and "description" not in out:
        out["description"] = desc
    for k, v in base.items():
        if k in ("description", "class_uri", "slot_uri", "enum_uri", "uri",
                 "exact_mappings", "aliases", "in_subset"):
            continue
        out[k] = v
    # Identity / provenance.
    uri_key = {
        "classes": "class_uri",
        "enums": "enum_uri",
        "types": "uri",
    }[kind]
    out[uri_key] = f"fix_sbe:{common_name}"
    mappings = []
    for m in (body_v1.get("exact_mappings") or []):
        if m not in mappings:
            mappings.append(m)
    for m in (body_v2.get("exact_mappings") or []):
        if m not in mappings:
            mappings.append(m)
    if mappings:
        out["exact_mappings"] = mappings
    aliases = []
    for a in (body_v1.get("aliases") or []):
        if a not in aliases:
            aliases.append(a)
    for a in (body_v2.get("aliases") or []):
        if a not in aliases:
            aliases.append(a)
    if aliases:
        out["aliases"] = aliases
    out["in_subset"] = ["sbe_common"]
    return out


def _has_versioned_refs(value) -> bool:
    """Return True if any structural reference anywhere in ``value`` is a
    PascalCase identifier ending in ``V1`` or ``V2`` (an as-yet-unpromoted
    reference into a sibling version overlay).

    Identity / provenance fields (``class_uri``, ``slot_uri``, ``enum_uri``,
    ``uri``, ``exact_mappings``, ``aliases``) are skipped because they
    embed the entity's own version-suffixed name as a substring of a
    CURIE — those substrings are not structural references and will be
    overwritten with common-overlay values by ``_build_common_body``.
    """
    if isinstance(value, dict):
        for k, v in value.items():
            if k in _IDENTITY_FIELDS:
                continue
            if _has_versioned_refs(v):
                return True
        return False
    if isinstance(value, list):
        return any(_has_versioned_refs(x) for x in value)
    if isinstance(value, str):
        return bool(re.fullmatch(r"[A-Z][A-Za-z0-9_]*V[12]", value))
    return False


def promote_common(
    v1_em: VersionEmitter,
    v2_em: VersionEmitter,
) -> tuple[OrderedDict, OrderedDict, OrderedDict, dict[str, str], dict[str, str]]:
    """Promote structurally-identical entities from the two version overlays
    into a shared common overlay.

    An entity ``FooV1`` is promoted iff a sibling ``FooV2`` exists, their
    bodies match structurally after (a) stripping identity / provenance
    fields and (b) ignoring ``V1`` / ``V2`` suffixes on PascalCase
    identifiers anywhere in the body, AND every reference in the rewritten
    body resolves to a promoted-common, linkml/xsd-primitive, or otherwise
    unsuffixed name. The check is iterated to a fixed point so promotions
    cascade (e.g. ``BlockType`` promotes first, then ``GroupType`` whose
    ``is_a: BlockTypeV2`` only resolves after the rename map gains
    ``BlockTypeV2 -> BlockType``).

    Returns:
        (common_classes, common_enums, common_types, renames_v1, renames_v2)
    """
    common_classes: OrderedDict = OrderedDict()
    common_enums: OrderedDict = OrderedDict()
    common_types: OrderedDict = OrderedDict()
    renames_v1: dict[str, str] = {}
    renames_v2: dict[str, str] = {}

    kind_specs = (
        ("types", v1_em.types, v2_em.types, common_types, "V1", "V2"),
        ("enums", v1_em.enums, v2_em.enums, common_enums, "V1", "V2"),
        ("classes", v1_em.classes, v2_em.classes, common_classes, "V1", "V2"),
    )

    while True:
        promoted_this_round = 0
        for kind, d1, d2, common_d, suffix1, suffix2 in kind_specs:
            for v1_name in list(d1.keys()):
                base = _strip_suffix(v1_name, suffix1)
                if base is None:
                    continue
                v2_name = base + suffix2
                if v2_name not in d2:
                    continue
                norm_v1 = _normalize_for_compare(d1[v1_name])
                norm_v2 = _normalize_for_compare(d2[v2_name])
                if norm_v1 != norm_v2:
                    continue
                # Apply current renames; if either rewritten body still has
                # version-suffixed references, defer to a later round.
                rw_v1 = _rewrite_refs(d1[v1_name], renames_v1)
                rw_v2 = _rewrite_refs(d2[v2_name], renames_v2)
                if _has_versioned_refs(rw_v1) or _has_versioned_refs(rw_v2):
                    continue
                common_d[base] = _build_common_body(
                    rw_v1, rw_v2, base, kind, renames_v1, renames_v2
                )
                renames_v1[v1_name] = base
                renames_v2[v2_name] = base
                del d1[v1_name]
                del d2[v2_name]
                promoted_this_round += 1
        if promoted_this_round == 0:
            break

    # Apply renames to remaining version-specific entities so their internal
    # references (range, is_a, mixins, etc.) point at the unsuffixed common
    # entities.
    def _apply(em: VersionEmitter, renames: dict[str, str]) -> None:
        em.classes = OrderedDict(
            (k, _rewrite_refs(v, renames)) for k, v in em.classes.items()
        )
        em.enums = OrderedDict(
            (k, _rewrite_refs(v, renames)) for k, v in em.enums.items()
        )
        em.types = OrderedDict(
            (k, _rewrite_refs(v, renames)) for k, v in em.types.items()
        )

    _apply(v1_em, renames_v1)
    _apply(v2_em, renames_v2)
    return common_classes, common_enums, common_types, renames_v1, renames_v2


# ---------------------------------------------------------------------------
# Document assembly + write
# ---------------------------------------------------------------------------


def overlay_document(
    em: VersionEmitter,
    *,
    schema_id: str,
    schema_name: str,
    title: str,
    description: str,
    version_label: str,
    xsd_relpath: str,
    xsd_namespace: str,
    upstream_url: str,
    sbe_prefix_local: str,
    subset_description: str,
    extra_imports: list[str] | None = None,
) -> OrderedDict:
    header: OrderedDict = OrderedDict()
    header["id"] = schema_id
    header["name"] = schema_name
    header["title"] = title
    header["description"] = description
    header["license"] = "Apache-2.0"
    header["see_also"] = [
        "https://www.fixtrading.org/standards/sbe/",
        "https://github.com/FIXTradingCommunity/fix-simple-binary-encoding",
        "https://lmodel.github.io/fix-simple-binary-encoding",
    ]
    header["source"] = upstream_url
    header["version"] = version_label
    header["notes"] = [
        "(c) Copyright 2014-2019 FIX Protocol Limited. Creative Commons "
        "Attribution-NoDerivatives 4.0 International Public License (CC BY-ND "
        "4.0) applies to the upstream XSD specification.",
        "This LinkML schema is auto-generated by scripts/schema_to_linkml.py "
        "- edit the script (or the upstream XSDs) and re-run, do not edit "
        "this file by hand.",
    ]
    header["annotations"] = OrderedDict([
        ("xsd_source", xsd_relpath),
        ("xsd_target_namespace_sbe", xsd_namespace),
    ])
    header["prefixes"] = OrderedDict([
        ("fix_sbe",
         "https://w3id.org/lmodel/fix-sbe/"),
        ("linkml", "https://w3id.org/linkml/"),
        ("rdf", "http://www.w3.org/1999/02/22-rdf-syntax-ns#"),
        ("rdfs", "http://www.w3.org/2000/01/rdf-schema#"),
        ("xsd", "http://www.w3.org/2001/XMLSchema#"),
        ("skos", "http://www.w3.org/2004/02/skos/core#"),
        ("schema", "http://schema.org/"),
        ("dct", "http://purl.org/dc/terms/"),
        (sbe_prefix_local, xsd_namespace + "/"),
    ])
    header["default_prefix"] = "fix_sbe"
    header["default_range"] = "string"
    header["imports"] = ["linkml:types", *(extra_imports or [])]
    subsets: OrderedDict = OrderedDict([
        (em.subset, OrderedDict([("description", subset_description)])),
    ])
    doc: OrderedDict = OrderedDict(header)
    if em.types:
        doc["types"] = em.types
    doc["subsets"] = subsets
    if em.enums:
        doc["enums"] = em.enums
    doc["classes"] = em.classes
    return doc


def common_document(
    classes: OrderedDict,
    enums: OrderedDict,
    types: OrderedDict,
    *,
    sbe_v1_ns: str,
    sbe_v2_ns: str,
) -> OrderedDict:
    """Build the ``fix_sbe_common`` overlay schema holding entities promoted
    from both v1 and v2 because their structures match exactly."""
    header: OrderedDict = OrderedDict()
    header["id"] = "https://w3id.org/lmodel/fix-sbe/common"
    header["name"] = "fix_sbe_common"
    header["title"] = "FIX Simple Binary Encoding — Common (cross-version)"
    header["description"] = (
        "Common LinkML overlay for FIX Simple Binary Encoding. Holds "
        "entities (classes, enums, types) whose structure is identical "
        "across the SBE v1.0 Standard and v2.0 RC3 XSDs and have therefore "
        "been promoted to a shared, unsuffixed name. Imported by the "
        "per-version overlays ``fix_sbe_v1_0`` and ``fix_sbe_v2_0`` and by "
        "the umbrella ``fix_sbe`` schema."
    )
    header["license"] = "Apache-2.0"
    header["see_also"] = [
        "https://www.fixtrading.org/standards/sbe/",
        "https://github.com/FIXTradingCommunity/fix-simple-binary-encoding",
        "https://lmodel.github.io/fix-simple-binary-encoding",
    ]
    header["source"] = (
        "https://github.com/FIXTradingCommunity/fix-simple-binary-encoding"
    )
    header["notes"] = [
        "(c) Copyright 2014-2019 FIX Protocol Limited. Creative Commons "
        "Attribution-NoDerivatives 4.0 International Public License (CC BY-ND "
        "4.0) applies to the upstream XSD specifications.",
        "This LinkML schema is auto-generated by scripts/schema_to_linkml.py "
        "- edit the script (or the upstream XSDs) and re-run, do not edit "
        "this file by hand.",
    ]
    header["annotations"] = OrderedDict([
        ("xsd_target_namespace_sbe_v1", sbe_v1_ns),
        ("xsd_target_namespace_sbe_v2", sbe_v2_ns),
    ])
    header["prefixes"] = OrderedDict([
        ("fix_sbe",
         "https://w3id.org/lmodel/fix-sbe/"),
        ("linkml", "https://w3id.org/linkml/"),
        ("rdf", "http://www.w3.org/1999/02/22-rdf-syntax-ns#"),
        ("rdfs", "http://www.w3.org/2000/01/rdf-schema#"),
        ("xsd", "http://www.w3.org/2001/XMLSchema#"),
        ("skos", "http://www.w3.org/2004/02/skos/core#"),
        ("schema", "http://schema.org/"),
        ("dct", "http://purl.org/dc/terms/"),
        ("sbe_v1", sbe_v1_ns + "/"),
        ("sbe_v2", sbe_v2_ns + "/"),
    ])
    header["default_prefix"] = "fix_sbe"
    header["default_range"] = "string"
    header["imports"] = ["linkml:types"]
    subsets: OrderedDict = OrderedDict([
        ("sbe_common", OrderedDict([
            ("description",
             "Entities common to SBE v1.0 Standard and v2.0 RC3 "
             "(structurally identical across both XSDs). Names are unsuffixed.")
        ])),
    ])
    doc: OrderedDict = OrderedDict(header)
    if types:
        doc["types"] = types
    doc["subsets"] = subsets
    if enums:
        doc["enums"] = enums
    doc["classes"] = classes
    return doc


def umbrella_document(
    overlay_names: list[str],
    *,
    sbe_v1_ns: str,
    sbe_v2_ns: str,
) -> OrderedDict:
    header: OrderedDict = OrderedDict()
    header["id"] = "https://w3id.org/lmodel/fix-sbe"
    header["name"] = "fix_sbe"
    header["title"] = "FIX Simple Binary Encoding"
    header["description"] = (
        "Umbrella LinkML schema for the FIX Simple Binary Encoding (SBE) "
        "standard. Imports three overlays: ``fix_sbe_common`` (entities "
        "structurally identical across SBE versions, kept unsuffixed) plus "
        "two per-version overlays ``fix_sbe_v1_0`` and ``fix_sbe_v2_0`` "
        "(remaining version-specific entities, PascalCase names suffixed "
        "with ``V1`` or ``V2`` to disambiguate). Per-version validation can "
        "be performed by targeting an overlay file directly."
    )
    header["license"] = "Apache-2.0"
    header["see_also"] = [
        "https://www.fixtrading.org/standards/sbe/",
        "https://github.com/FIXTradingCommunity/fix-simple-binary-encoding",
        "https://lmodel.github.io/fix-simple-binary-encoding",
    ]
    header["source"] = (
        "https://github.com/FIXTradingCommunity/fix-simple-binary-encoding"
    )
    header["notes"] = [
        "(c) Copyright 2014-2019 FIX Protocol Limited. Creative Commons "
        "Attribution-NoDerivatives 4.0 International Public License (CC BY-ND "
        "4.0) applies to the upstream XSD specifications.",
        "This umbrella schema is auto-generated by "
        "scripts/schema_to_linkml.py - do not edit this file by hand.",
    ]
    header["annotations"] = OrderedDict([
        ("xsd_target_namespace_sbe_v1", sbe_v1_ns),
        ("xsd_target_namespace_sbe_v2", sbe_v2_ns),
    ])
    header["prefixes"] = OrderedDict([
        ("fix_sbe",
         "https://w3id.org/lmodel/fix-sbe/"),
        ("linkml", "https://w3id.org/linkml/"),
        ("rdf", "http://www.w3.org/1999/02/22-rdf-syntax-ns#"),
        ("rdfs", "http://www.w3.org/2000/01/rdf-schema#"),
        ("xsd", "http://www.w3.org/2001/XMLSchema#"),
        ("skos", "http://www.w3.org/2004/02/skos/core#"),
        ("schema", "http://schema.org/"),
        ("dct", "http://purl.org/dc/terms/"),
        ("sbe_v1", sbe_v1_ns + "/"),
        ("sbe_v2", sbe_v2_ns + "/"),
    ])
    header["default_prefix"] = "fix_sbe"
    header["default_range"] = "string"
    header["imports"] = ["linkml:types", *overlay_names]
    doc: OrderedDict = OrderedDict(header)
    # Subsets ``sbe_v1_0`` / ``sbe_v2_0`` are declared by the imported
    # overlays — re-declaring them here would trigger a ``Conflicting URIs``
    # error from the LinkML schema loader during merge.
    # The umbrella has no own classes — all entities come via imports.
    doc["classes"] = OrderedDict()
    return doc


# ---------------------------------------------------------------------------
# Hand-rolled YAML emitter (preserves OrderedDict insertion order).
# ---------------------------------------------------------------------------


def yaml_quote(s: str) -> str:
    s = str(s)
    if "\n" in s:
        s = " ".join(s.split())
    if s == "":
        return "''"
    if re.fullmatch(r"-?\d+(\.\d+)?([eE][+-]?\d+)?", s):
        return f"'{s}'"
    if s.lower() in ("true", "false", "null", "yes", "no", "on", "off", "~"):
        return f"'{s}'"
    first = s[0]
    needs_quote = (
        first in "'\"|>!@`[{&*%"
        or first == "#"
        or first == ":"
        or (first == "-" and len(s) > 1 and s[1] in " \t")
        or (first == "?" and len(s) > 1 and s[1] in " \t")
        or ": " in s
        or s.endswith(":")
        or " #" in s
        or s[0].isspace()
        or s[-1].isspace()
    )
    if needs_quote:
        if "'" not in s:
            return f"'{s}'"
        esc = s.replace("\\", "\\\\").replace('"', '\\"')
        return f'"{esc}"'
    return s


def yaml_key(k) -> str:
    return (
        yaml_quote(k) if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", str(k)) else str(k)
    )


def scalar(v) -> str:
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return str(v)
    if v is None:
        return "null"
    return yaml_quote(v)


SEPARATED_DICT_KEYS = {
    "types", "enums", "classes", "slots", "subsets",
    "attributes", "permissible_values",
}


def dump_yaml(value, indent: int = 0, separate: bool = False) -> list[str]:
    pad = "  " * indent
    lines: list[str] = []
    if isinstance(value, dict):
        if not value:
            return ["{}"]
        items = list(value.items())
        prev_complex = False
        for idx, (k, v) in enumerate(items):
            this_complex = (isinstance(v, dict) and v) or (isinstance(v, list) and v)
            if idx > 0 and separate and (this_complex or prev_complex):
                lines.append("")
            key = yaml_key(k)
            child_separate = isinstance(v, dict) and k in SEPARATED_DICT_KEYS
            if isinstance(v, dict):
                if not v:
                    lines.append(f"{pad}{key}: {{}}")
                else:
                    lines.append(f"{pad}{key}:")
                    lines.extend(dump_yaml(v, indent + 1, separate=child_separate))
            elif isinstance(v, list):
                if not v:
                    lines.append(f"{pad}{key}: []")
                else:
                    lines.append(f"{pad}{key}:")
                    for item in v:
                        if isinstance(item, (dict, list)):
                            sub = dump_yaml(item, indent + 1)
                            first = sub[0].lstrip()
                            lines.append(f"{pad}- {first}")
                            for s in sub[1:]:
                                lines.append(s)
                        else:
                            lines.append(f"{pad}- {scalar(item)}")
            elif v is None:
                lines.append(f"{pad}{key}:")
            else:
                lines.append(f"{pad}{key}: {scalar(v)}")
            prev_complex = this_complex
    return lines


def write_yaml(out_file: Path, doc: OrderedDict, header_comment: str) -> None:
    out_lines = [
        "---",
        "# Auto-generated by scripts/schema_to_linkml.py",
        f"# {header_comment}",
        "# DO NOT EDIT BY HAND - re-run the script to regenerate.",
        "",
    ]
    out_lines.extend(dump_yaml(doc, separate=True))
    out_lines.append("")
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text("\n".join(out_lines), encoding="utf-8")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


# Per-version configuration. ``tree_root_element`` is the XSD top-level
# <xs:element> whose generated class gets ``tree_root: true``.
VERSIONS = [
    {
        "key": "v1_0",
        "suffix": "V1",
        "subset": "sbe_v1_0",
        "title": "FIX Simple Binary Encoding v1.0 Standard",
        "version_label": "1.0-standard",
        "xsd_relpath": (
            "upstream-releases/fix-simple-binary-encoding/v1-0-STANDARD/"
            "resources/sbe.xsd"
        ),
        "xsd_namespace": "http://fixprotocol.io/2016/sbe",
        "sbe_prefix_local": "sbe_v1",
        "upstream_url": (
            "https://github.com/FIXTradingCommunity/fix-simple-binary-encoding/"
            "tree/master/v1-0-STANDARD"
        ),
        "tree_root_element": "messageSchema",
        "out_basename": "fix_sbe_v1_0.yaml",
        "schema_id": "https://w3id.org/lmodel/fix-sbe/v1_0",
        "schema_name": "fix_sbe_v1_0",
        "subset_description": (
            "Entities sourced from SBE v1.0 Standard (sbe.xsd, target "
            "namespace http://fixprotocol.io/2016/sbe). All PascalCase names "
            "in this overlay carry a ``V1`` suffix."
        ),
    },
    {
        "key": "v2_0",
        "suffix": "V2",
        "subset": "sbe_v2_0",
        "title": "FIX Simple Binary Encoding v2.0 RC3",
        "version_label": "2.0-RC3",
        "xsd_relpath": (
            "upstream-releases/fix-simple-binary-encoding/v2-0-RC3/"
            "resources/xsd/sbe-2.0rc3.xsd"
        ),
        "xsd_namespace": "http://fixprotocol.io/2017/sbe",
        "sbe_prefix_local": "sbe_v2",
        "upstream_url": (
            "https://github.com/FIXTradingCommunity/fix-simple-binary-encoding/"
            "tree/master/v2-0-RC3"
        ),
        "tree_root_element": "messageSchema",
        "out_basename": "fix_sbe_v2_0.yaml",
        "schema_id": "https://w3id.org/lmodel/fix-sbe/v2_0",
        "schema_name": "fix_sbe_v2_0",
        "subset_description": (
            "Entities sourced from SBE v2.0 RC3 (sbe-2.0rc3.xsd, target "
            "namespace http://fixprotocol.io/2017/sbe). All PascalCase names "
            "in this overlay carry a ``V2`` suffix."
        ),
    },
]


def convert(repo_root: Path, schema_dir: Path) -> None:
    # Phase 1: parse + emit both version overlays in memory (without writing).
    emitters: list[tuple[dict, VersionEmitter]] = []
    for cfg in VERSIONS:
        xsd_path = repo_root / cfg["xsd_relpath"]
        if not xsd_path.is_file():
            print(f"ERROR: missing XSD {xsd_path}", file=sys.stderr)
            sys.exit(1)
        parsed = parse_xsd(xsd_path)
        em = VersionEmitter(
            parsed,
            suffix=cfg["suffix"],
            subset=cfg["subset"],
            sbe_prefix_local=cfg["sbe_prefix_local"],
            upstream_namespace=cfg["xsd_namespace"],
        )
        em.run(tree_root_element=cfg["tree_root_element"])
        emitters.append((cfg, em))

    (v1_cfg, v1_em), (v2_cfg, v2_em) = emitters

    # Pre-promotion counts for the coverage report.
    pre_counts = {
        v1_cfg["key"]: (len(v1_em.classes), len(v1_em.enums), len(v1_em.types)),
        v2_cfg["key"]: (len(v2_em.classes), len(v2_em.enums), len(v2_em.types)),
    }

    # Phase 2: structural-equality promotion to a common overlay.
    common_classes, common_enums, common_types, renames_v1, renames_v2 = (
        promote_common(v1_em, v2_em)
    )

    # Write common overlay.
    common_path = schema_dir / "fix_sbe_common.yaml"
    common_doc = common_document(
        common_classes,
        common_enums,
        common_types,
        sbe_v1_ns=v1_cfg["xsd_namespace"],
        sbe_v2_ns=v2_cfg["xsd_namespace"],
    )
    write_yaml(common_path, common_doc,
               "Common overlay: entities structurally identical in v1 and v2.")
    print(
        f"=== Common (promoted) ===\n"
        f"  Emitted             : classes={len(common_classes)} "
        f"enums={len(common_enums)} types={len(common_types)}\n"
        f"  Wrote               : {common_path}",
        file=sys.stderr,
    )

    # Write per-version overlays (now slimmed, importing fix_sbe_common).
    overlay_basenames: list[str] = []
    for cfg, em in emitters:
        doc = overlay_document(
            em,
            schema_id=cfg["schema_id"],
            schema_name=cfg["schema_name"],
            title=cfg["title"],
            description=(
                f"LinkML schema generated from the FIX Simple Binary "
                f"Encoding {cfg['version_label']} XSD "
                f"({Path(cfg['xsd_relpath']).name}). PascalCase class / enum "
                f"/ type names that are unique to this version carry the "
                f"``{cfg['suffix']}`` suffix; structurally-shared entities "
                f"are imported unsuffixed from ``fix_sbe_common``."
            ),
            version_label=cfg["version_label"],
            xsd_relpath=cfg["xsd_relpath"],
            xsd_namespace=cfg["xsd_namespace"],
            upstream_url=cfg["upstream_url"],
            sbe_prefix_local=cfg["sbe_prefix_local"],
            subset_description=cfg["subset_description"],
            extra_imports=["fix_sbe_common"],
        )
        out_path = schema_dir / cfg["out_basename"]
        write_yaml(out_path, doc, f"Source: {cfg['xsd_relpath']}")

        pre = pre_counts[cfg["key"]]
        post = (len(em.classes), len(em.enums), len(em.types))
        print(
            f"=== {cfg['title']} ===\n"
            f"  XSD                 : {cfg['xsd_relpath']}\n"
            f"  Pre-promotion       : classes={pre[0]} enums={pre[1]} "
            f"types={pre[2]}\n"
            f"  Post-promotion      : classes={post[0]} enums={post[1]} "
            f"types={post[2]}\n"
            f"  Wrote               : {out_path}",
            file=sys.stderr,
        )
        overlay_basenames.append(Path(cfg["out_basename"]).stem)

    # Umbrella schema imports common + both per-version overlays.
    umbrella_path = schema_dir / "fix_sbe.yaml"
    umbrella = umbrella_document(
        overlay_names=["fix_sbe_common", *overlay_basenames],
        sbe_v1_ns=v1_cfg["xsd_namespace"],
        sbe_v2_ns=v2_cfg["xsd_namespace"],
    )
    write_yaml(
        umbrella_path,
        umbrella,
        "Umbrella schema importing common + per-version SBE overlays.",
    )
    print(f"=== Umbrella ===\n  Wrote               : {umbrella_path}",
          file=sys.stderr)


def main(argv: list[str] | None = None) -> int:
    here = Path(__file__).resolve().parent
    repo_root = here.parent
    default_schema_dir = repo_root / "src" / "fix_sbe" / "schema"
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument(
        "--repo-root",
        type=Path,
        default=Path(os.environ.get("REPO_ROOT", repo_root)),
        help="repository root (default: parent of scripts/)",
    )
    p.add_argument(
        "--schema-dir",
        type=Path,
        default=Path(os.environ.get("SCHEMA_DIR", default_schema_dir)),
        help="output directory for generated LinkML YAML files",
    )
    args = p.parse_args(argv)
    convert(args.repo_root, args.schema_dir)
    return 0


if __name__ == "__main__":
    sys.exit(main())
