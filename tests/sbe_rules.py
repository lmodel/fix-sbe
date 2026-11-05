"""The specification's rules that JSON Schema cannot state.

Most of them compare one element with another: a field with the encoding it names, an offset
with the sizes before it, a version with the schema's. Chapter 4's "Schema validation" lists
most of them, and each rule below names its source. They read a whole message schema as the
YAML record the LinkML schema describes, of either edition.

`rule_errors` returns (place, rule, message) tuples, and tests/test_rules.py holds each rule to
a counter-example.
"""

from __future__ import annotations

import math

import yaml

from tests.paths import SCHEMA_DIR

PRIMITIVE_OCTETS = {
    "char": 1,
    "int8": 1,
    "uint8": 1,
    "int16": 2,
    "uint16": 2,
    "int32": 4,
    "uint32": 4,
    "int64": 8,
    "uint64": 8,
    "float": 4,
    "double": 8,
}
UNSIGNED = {"uint8", "uint16", "uint32", "uint64"}
# The null value of each integer type where the schema states none (chapter 2). A float's is
# NaN, which no enumeration sits on.
DEFAULT_NULL = {
    "char": 0,
    "int8": -(2**7),
    "int16": -(2**15),
    "int32": -(2**31),
    "int64": -(2**63),
    "uint8": 2**8 - 1,
    "uint16": 2**16 - 1,
    "uint32": 2**32 - 1,
    "uint64": 2**64 - 1,
}
ENUM_ENCODINGS = UNSIGNED | {"char"}
FLOATING = {"float", "double"}
DECIMAL_TYPES = {"qty", "price", "priceoffset", "amt", "percentage"}
HEADER_MEMBERS = ("blockLength", "templateId", "schemaId", "version")
HEADER_COUNTERS = ("numGroups", "numVarDataFields")
DIMENSION_MEMBERS = ("blockLength", "numInGroup")
VAR_DATA_MEMBERS = ("length", "varData")

_common = yaml.safe_load(
    (SCHEMA_DIR / "fix_sbe_common.yaml").read_text(encoding="utf-8")
)
FIX_DATATYPES = {
    name.lower() for name in _common["enums"]["SbeFixDatatype"]["permissible_values"]
}


def _kind(element: dict) -> str:
    """The element's kind without its edition, such as Composite."""
    return element["encoding_kind"].removeprefix("Sbe")[:-2]


def _is_simple(element: dict) -> bool:
    return _kind(element) in ("SimpleType", "MemberType")


class _Schema:
    """One message schema's encodings by name, with the walks the rules share."""

    def __init__(self, record: dict):
        self.record = record
        self.version = record["schema_version"]
        self.encodings: dict[str, dict] = {}
        self.duplicates: list[tuple[str, str]] = []
        for s, group in enumerate(record.get("encoding_sets", [])):
            for e, encoding in enumerate(group["encodings"]):
                name = encoding["symbolic_name"]
                if name in self.encodings:
                    self.duplicates.append((f"encoding_sets/{s}/encodings/{e}", name))
                self.encodings.setdefault(name, encoding)
        self.messages = list(record.get("messages", []))
        for group in record.get("message_sets", []):
            self.messages += group["messages"]

    def enums(self):
        """Every enumeration, inside a composite or not, by its name."""

        def walk(element):
            if _kind(element) == "Enum":
                yield element
            for member in element.get("composite_members", []):
                yield from walk(member)

        for encoding in self.encodings.values():
            yield from walk(encoding)

    def primitive(self, name: str) -> tuple[str | None, int | None]:
        """What an enum's or set's encoding_type comes to: a primitive and its array length."""
        if name in self.encodings:
            target = self.encodings[name]
            if _is_simple(target):
                return target["primitive_type"], target.get("array_length", 1)
            return None, None
        if name in PRIMITIVE_OCTETS:
            return name, 1
        return None, None

    def octets(self, element: dict, seen: frozenset = frozenset()) -> int | None:
        """The octets an encoding takes, or None where the number is not fixed."""
        kind = _kind(element)
        if element.get("presence") == "constant":
            return 0
        if _is_simple(element):
            length = element.get("array_length", 1)
            return (
                PRIMITIVE_OCTETS[element["primitive_type"]] * length if length else None
            )
        if kind in ("Enum", "Set"):
            primitive, _ = self.primitive(element["encoding_type"])
            return PRIMITIVE_OCTETS[primitive] if primitive else None
        if kind == "Ref":
            name = element["encoding_name"]
            if name in seen or name not in self.encodings:
                return None
            return self.octets(self.encodings[name], seen | {name})
        total = 0
        for member in element["composite_members"]:
            size = self.octets(member, seen)
            if size is None:
                return None
            start = _aligned(total, member.get("alignment"))
            total = max(start, member.get("offset", start)) + size
        return total

    def is_variable(self, element: dict) -> bool:
        """Whether an encoding holds an array of no fixed length."""
        if element.get("array_length") == 0:
            return True
        return any(self.is_variable(m) for m in element.get("composite_members", []))


def _scalar_error(text: str, primitive: str) -> str | None:
    """Why a written value cannot be one value of a primitive type, if it cannot."""
    if primitive == "char":
        # FIX's documents write a char value as the character itself, never as its number.
        return None if len(text) == 1 else "is not one character"
    if primitive in FLOATING:
        try:
            value = float(text)
        except ValueError:
            return "is not a number"
        return None if math.isfinite(value) or math.isnan(value) else "is not finite"
    try:
        value = int(text)
    except ValueError:
        return "is not an integer"
    bits = PRIMITIVE_OCTETS[primitive] * 8
    if primitive.startswith("u"):
        low, high = 0, 2**bits - 1
    else:
        low, high = -(2 ** (bits - 1)), 2 ** (bits - 1) - 1
    return None if low <= value <= high else f"is outside {low} to {high}"


def _aligned(position: int, alignment: int | None) -> int:
    """The position moved up to the next multiple of the alignment, where one is stated."""
    if alignment:
        return position + (alignment - position % alignment) % alignment
    return position


def _as_number(text: str, primitive: str) -> int | float:
    """A written value that _scalar_error accepted, as the number it encodes."""
    if primitive == "char":
        return ord(text)
    return float(text) if primitive in FLOATING else int(text)


def _stated_bound(
    encoding: dict | None, slot: str, primitive: str
) -> int | float | None:
    """A null, lowest or highest value the enum's encoding type states, where it fits."""
    text = (encoding or {}).get(slot)
    if text is None or _scalar_error(text, primitive):
        return None
    return _as_number(text, primitive)


def _check_versions(schema: _Schema, element: dict, place: str, errors: list) -> None:
    """A version on an element cannot be later than the schema's (chapter 4, chapter 5)."""
    for slot in ("since_version", "deprecated_since"):
        value = element.get(slot)
        if value is not None and value > schema.version:
            errors.append(
                (place, "version-after-schema", f"{slot} {value} > {schema.version}")
            )


def _check_simple(element: dict, place: str, errors: list) -> None:
    """A simple encoding's values fit its type, and a constant has a value (chapter 4)."""
    primitive = element["primitive_type"]
    for slot in ("null_value", "min_value", "max_value"):
        if slot in element:
            why = _scalar_error(element[slot], primitive)
            if why:
                errors.append((place, "value-out-of-range", f"{slot} {why}"))
    if element.get("presence") == "constant" and not (
        element.get("element_value") or element.get("value_ref")
    ):
        errors.append((place, "constant-without-value", element["symbolic_name"]))
    value = element.get("element_value")
    if value is not None:
        length = element.get("array_length", 1)
        if primitive == "char":
            if length and len(value) > length:
                errors.append(
                    (place, "value-out-of-range", f"element_value is over {length}")
                )
        elif length == 1:
            why = _scalar_error(value, primitive)
            if why:
                errors.append((place, "value-out-of-range", f"element_value {why}"))


def _check_enum(schema: _Schema, element: dict, place: str, errors: list) -> None:
    """An enum sits on char or an unsigned type, with distinct named values that fit it and
    are not its null (chapter 4)."""
    primitive, length = schema.primitive(element["encoding_type"])
    if primitive is None:
        errors.append((place, "unknown-encoding", element["encoding_type"]))
        return
    if primitive not in ENUM_ENCODINGS or length != 1:
        errors.append((place, "enum-encoding", f"{primitive}, length {length}"))
    names = [value["symbolic_name"] for value in element["valid_values"]]
    for name in sorted({name for name in names if names.count(name) > 1}):
        errors.append((place, "duplicate-value-name", name))
    # A value is neither the encoding's null, stated or the type's default, nor outside the
    # lowest and highest values the encoding type states, and no two values encode alike.
    encoding = schema.encodings.get(element["encoding_type"])
    null = _stated_bound(encoding, "null_value", primitive)
    if null is None:
        null = DEFAULT_NULL.get(primitive)
    low = _stated_bound(encoding, "min_value", primitive)
    high = _stated_bound(encoding, "max_value", primitive)
    numbers = []
    for v, value in enumerate(element["valid_values"]):
        here = f"{place}/valid_values/{v}"
        _check_versions(schema, value, here, errors)
        why = _scalar_error(value["valid_value"], primitive)
        if why:
            errors.append((here, "value-out-of-range", f"valid_value {why}"))
            continue
        number = _as_number(value["valid_value"], primitive)
        numbers.append(number)
        if number == null:
            errors.append((here, "value-is-null", value["valid_value"]))
        if (low is not None and number < low) or (high is not None and number > high):
            errors.append(
                (
                    here,
                    "value-outside-type-range",
                    f"{value['valid_value']} not in {low} to {high}",
                )
            )
    for number in sorted({n for n in numbers if numbers.count(n) > 1}):
        errors.append((place, "duplicate-value", str(number)))


def _check_set(schema: _Schema, element: dict, place: str, errors: list) -> None:
    """A set sits on an unsigned type, with one distinct bit per choice (chapter 4)."""
    primitive, length = schema.primitive(element["encoding_type"])
    if primitive is None:
        errors.append((place, "unknown-encoding", element["encoding_type"]))
        return
    if primitive not in UNSIGNED or length != 1:
        errors.append((place, "set-encoding", f"{primitive}, length {length}"))
        return
    width = PRIMITIVE_OCTETS[primitive] * 8
    names = [choice["symbolic_name"] for choice in element["choices"]]
    for name in sorted({name for name in names if names.count(name) > 1}):
        errors.append((place, "duplicate-value-name", name))
    bits = [choice["bit_position"] for choice in element["choices"]]
    for bit in sorted({bit for bit in bits if bits.count(bit) > 1}):
        errors.append((place, "duplicate-bit", str(bit)))
    for c, choice in enumerate(element["choices"]):
        _check_versions(schema, choice, f"{place}/choices/{c}", errors)
        if choice["bit_position"] >= width:
            errors.append(
                (
                    f"{place}/choices/{c}",
                    "choice-past-bits",
                    f"{choice['bit_position']} of {width}",
                )
            )


def _check_members(schema: _Schema, element: dict, place: str, errors: list) -> None:
    """A composite has two or more members, none overlapping another, each placed by its offset
    or its alignment (chapters 3 and 4)."""
    members = element["composite_members"]
    if len(members) < 2:
        errors.append((place, "composite-of-one", element["symbolic_name"]))
    names = [member["symbolic_name"] for member in members]
    for name in sorted({name for name in names if names.count(name) > 1}):
        errors.append((place, "duplicate-member-name", name))
    # The position is None once a member has no fixed size: the members after it are still
    # checked, and only the offset arithmetic stops.
    position: int | None = 0
    for m, member in enumerate(members):
        here = f"{place}/composite_members/{m}"
        _check_encoding(schema, member, here, errors)
        if position is None:
            continue
        position = _aligned(position, member.get("alignment"))
        offset = member.get("offset")
        if offset is not None and offset < position:
            errors.append((here, "offset-overlaps", f"{offset} < {position}"))
        size = schema.octets(member)
        position = None if size is None else max(position, offset or 0) + size


def _check_encoding(schema: _Schema, element: dict, place: str, errors: list) -> None:
    """Whatever applies to one encoding or composite member."""
    _check_versions(schema, element, place, errors)
    semantic = element.get("semantic_type")
    if semantic and semantic.lower() not in FIX_DATATYPES:
        errors.append((place, "unknown-semantic-type", semantic))
    kind = _kind(element)
    if _is_simple(element):
        _check_simple(element, place, errors)
    elif kind == "Enum":
        _check_enum(schema, element, place, errors)
    elif kind == "Set":
        _check_set(schema, element, place, errors)
    elif kind == "Ref":
        if element["encoding_name"] not in schema.encodings:
            errors.append((place, "unknown-encoding", element["encoding_name"]))
    elif kind == "Composite":
        _check_members(schema, element, place, errors)
        if semantic:
            _check_decimal(element, semantic, place, errors)


def _member_problems(schema: _Schema, name: str, wanted: tuple[str, ...]) -> list[str]:
    """Which of the named members an unsigned counter or length composite gets wrong."""
    composite = schema.encodings.get(name)
    if composite is None or _kind(composite) != "Composite":
        return [f"{name} is not a composite of this schema"]
    members = {m["symbolic_name"]: m for m in composite["composite_members"]}
    problems = []
    for member in wanted:
        if member not in members:
            problems.append(f"{name} has no member {member}")
    for member, element in members.items():
        if member in wanted + HEADER_COUNTERS and _is_simple(element):
            if element["primitive_type"] not in UNSIGNED:
                problems.append(f"{name}.{member} is not an unsigned integer")
    return problems


def _resolved_presence(field: dict, encoding: dict | None) -> str | None:
    """The presence a field states or, failing that, its encoding states."""
    return field.get("presence") or (encoding or {}).get("presence")


def _is_constant_encoding(encoding: dict | None) -> bool:
    return bool(encoding) and encoding.get("presence") == "constant"


def _check_field(schema: _Schema, field: dict, place: str, errors: list) -> None:
    """A field against the encoding it names (chapter 4, "Schema validation")."""
    _check_versions(schema, field, place, errors)
    name = field["encoding_name"]
    encoding = schema.encodings.get(name)
    if encoding is None:
        errors.append((place, "unknown-encoding", name))
    semantic = field.get("semantic_type")
    if semantic and semantic.lower() not in FIX_DATATYPES:
        errors.append((place, "unknown-semantic-type", semantic))
    other = (encoding or {}).get("semantic_type")
    if semantic and other and semantic.lower() != other.lower():
        errors.append((place, "semantic-type-mismatch", f"{semantic} and {other}"))
    stated, other = field.get("presence"), (encoding or {}).get("presence")
    if stated and other and stated != other:
        errors.append((place, "presence-mismatch", f"{stated} and {other}"))
    if _resolved_presence(field, encoding) == "constant" and not (
        field.get("value_ref")
        or field.get("element_value")
        or _is_constant_encoding(encoding)
    ):
        errors.append((place, "constant-without-value", field["symbolic_name"]))
    if encoding and _kind(encoding) == "Composite" and semantic:
        _check_decimal(encoding, semantic, place, errors)


def _check_decimal(composite: dict, semantic: str, place: str, errors: list) -> None:
    """A composite for a decimal or MonthYear holds the reserved members (chapters 2, 4)."""
    members = {m["symbolic_name"] for m in composite["composite_members"]}
    if semantic.lower() in DECIMAL_TYPES and not {"mantissa", "exponent"} <= members:
        errors.append(
            (place, "reserved-members", f"{composite['symbolic_name']} for {semantic}")
        )
    if semantic.lower() == "monthyear" and not {"year", "month"} <= members:
        errors.append(
            (place, "reserved-members", f"{composite['symbolic_name']} for {semantic}")
        )


def _check_block(
    schema: _Schema, block: dict, place: str, errors: list, identities: dict
) -> None:
    """A block's fields, then its groups, then its data (chapters 3, 4 and 5)."""
    _check_versions(schema, block, place, errors)
    position = 0
    last = 0
    for f, field in enumerate(block.get("block_fields", [])):
        here = f"{place}/block_fields/{f}"
        _check_field(schema, field, here, errors)
        _check_identity(field, here, errors, identities)
        since = field.get("since_version", 0)
        if since < last:
            errors.append((here, "extension-out-of-order", f"{since} after {last}"))
        last = max(last, since)
        encoding = schema.encodings.get(field["encoding_name"])
        constant = field.get("presence") == "constant"
        size = 0 if constant or encoding is None else schema.octets(encoding)
        if size is None:
            if schema.is_variable(encoding):
                errors.append((here, "variable-length-field", field["encoding_name"]))
            size = 0
        offset = field.get("offset")
        alignment = field.get("alignment")
        if offset is not None and offset < position:
            errors.append((here, "offset-overlaps", f"{offset} < {position}"))
        position = _aligned(position, alignment)
        start = max(position, offset or 0)
        length = block.get("block_length")
        if offset is not None and length is not None and offset > length:
            errors.append((here, "offset-past-block", f"{offset} > {length}"))
        position = start + size
    length = block.get("block_length")
    if length is not None and length < position:
        errors.append((place, "block-too-short", f"{length} < {position}"))
    last = 0
    for g, group in enumerate(block.get("repeating_groups", [])):
        here = f"{place}/repeating_groups/{g}"
        since = group.get("since_version", 0)
        if since < last:
            errors.append((here, "extension-out-of-order", f"{since} after {last}"))
        last = max(last, since)
        _check_identity(group, here, errors, identities)
        name = group.get("dimension_type", "groupSizeEncoding")
        for problem in _member_problems(schema, name, DIMENSION_MEMBERS):
            errors.append((here, "group-dimension", problem))
        _check_block(schema, group, here, errors, identities)
    last = 0
    for d, data in enumerate(block.get("var_data_fields", [])):
        here = f"{place}/var_data_fields/{d}"
        _check_field(schema, data, here, errors)
        _check_identity(data, here, errors, identities)
        since = data.get("since_version", 0)
        if since < last:
            errors.append((here, "extension-out-of-order", f"{since} after {last}"))
        last = max(last, since)
        name = data["encoding_name"]
        for problem in _member_problems(schema, name, VAR_DATA_MEMBERS):
            errors.append((here, "var-data-encoding", problem))
        if not _member_problems(schema, name, VAR_DATA_MEMBERS):
            members = {
                m["symbolic_name"]: m
                for m in schema.encodings[name]["composite_members"]
            }
            if members["varData"].get("array_length", 1) != 0:
                errors.append(
                    (here, "var-data-encoding", f"{name}.varData is not variable")
                )


def _check_identity(element: dict, place: str, errors: list, identities: dict) -> None:
    """One number means one name across the schema's fields and groups, and one name one number
    (chapter 4)."""
    number, name = element["sbe_id"], element["symbolic_name"]
    by_number, by_name = identities["numbers"], identities["names"]
    if by_number.setdefault(number, name) != name:
        errors.append(
            (place, "field-identity", f"id {number} is {name} and {by_number[number]}")
        )
    if by_name.setdefault(name, number) != number:
        errors.append(
            (place, "field-identity", f"{name} is {number} and {by_name[name]}")
        )


def _check_value_refs(schema: _Schema, errors: list) -> None:
    """A value_ref names an enumeration of the schema and one of its values (chapter 4)."""
    values = {
        enum["symbolic_name"]: {v["symbolic_name"] for v in enum["valid_values"]}
        for enum in schema.enums()
    }

    def check(element: dict, place: str) -> None:
        ref = element.get("value_ref")
        if ref:
            enum, _, value = ref.partition(".")
            if value not in values.get(enum, ()):
                errors.append((place, "value-ref-unknown", ref))
        for key in (
            "composite_members",
            "block_fields",
            "repeating_groups",
            "var_data_fields",
        ):
            for index, child in enumerate(element.get(key, [])):
                check(child, f"{place}/{key}/{index}")

    for s, group in enumerate(schema.record.get("encoding_sets", [])):
        for e, encoding in enumerate(group["encodings"]):
            check(encoding, f"encoding_sets/{s}/encodings/{e}")
    for m, message in enumerate(schema.messages):
        check(message, f"messages/{m}")


def rule_errors(record: dict) -> list[tuple[str, str, str]]:
    """Every rule a whole message schema breaks, as (place, rule, message) tuples."""
    errors: list[tuple[str, str, str]] = []
    schema = _Schema(record)
    for place, name in schema.duplicates:
        errors.append((place, "duplicate-encoding", name))
    header = record.get("header_type", "messageHeader")
    for problem in _member_problems(schema, header, HEADER_MEMBERS):
        errors.append(("header_type", "message-header", problem))
    for s, group in enumerate(record.get("encoding_sets", [])):
        for e, encoding in enumerate(group["encodings"]):
            _check_encoding(
                schema, encoding, f"encoding_sets/{s}/encodings/{e}", errors
            )
    names: dict[str, int] = {}
    numbers: dict[int, str] = {}
    identities: dict[str, dict] = {"numbers": {}, "names": {}}
    for m, message in enumerate(schema.messages):
        place = f"messages/{m}"
        name, number = message["symbolic_name"], message["sbe_id"]
        if name in names:
            errors.append((place, "duplicate-message", f"name {name}"))
        if number in numbers:
            errors.append((place, "duplicate-message", f"id {number}"))
        names[name] = number
        numbers[number] = name
        _check_block(schema, message, place, errors, identities)
    _check_value_refs(schema, errors)
    return errors
