"""Holds each rule of tests/sbe_rules.py to a counter-example of its own.

A change to the valid schema of one edition breaks one rule, and the test asserts the only
finding is that rule at that place. A rule that cannot see its fault fails here, and so does one
that sees more than it should.
"""

import copy
from pathlib import Path

import pytest
import yaml

from tests.sbe_rules import rule_errors

DATA = Path(__file__).parent / "data" / "valid"
SMALL = {
    edition: yaml.safe_load(
        (DATA / f"SbeMessageSchema{edition}-small.yaml").read_text(encoding="utf-8")
    )
    for edition in ("V1", "V2")
}


def _encoding(record, name):
    for group in record["encoding_sets"]:
        for encoding in group["encodings"]:
            if encoding["symbolic_name"] == name:
                return encoding
    raise KeyError(name)


def _message(record):
    return (
        record["messages"][0]
        if "messages" in record
        else record["message_sets"][0]["messages"][0]
    )


def _member(composite, name):
    return next(m for m in composite["composite_members"] if m["symbolic_name"] == name)


def _field(record, name):
    return next(
        f for f in _message(record)["block_fields"] if f["symbolic_name"] == name
    )


def _rename_header(record):
    _encoding(record, "messageHeader")["symbolic_name"] = "header"


def _header_without_schema_id(record):
    composite = _encoding(record, "messageHeader")
    composite["composite_members"] = [
        m for m in composite["composite_members"] if m["symbolic_name"] != "schemaId"
    ]


def _signed_template_id(record):
    _member(_encoding(record, "messageHeader"), "templateId")["primitive_type"] = (
        "int16"
    )


def _duplicate_encoding(record):
    record["encoding_sets"][-1]["encodings"].append(
        copy.deepcopy(_encoding(record, "idString"))
    )


def _duplicate_message_name(record):
    other = copy.deepcopy(_message(record))
    other["sbe_id"] = 2
    other["block_fields"] = other["block_fields"][:1]
    other.pop("repeating_groups")
    other.pop("var_data_fields")
    (record.get("messages") or record["message_sets"][0]["messages"]).append(other)


def _duplicate_message_id(record):
    other = copy.deepcopy(_message(record))
    other["symbolic_name"] = "Other"
    other["block_fields"] = other["block_fields"][:1]
    other.pop("repeating_groups")
    other.pop("var_data_fields")
    (record.get("messages") or record["message_sets"][0]["messages"]).append(other)


def _unknown_field_encoding(record):
    _field(record, "Quantity")["encoding_name"] = "noSuchEncoding"
    _field(record, "Quantity").pop("null_value", None)
    _field(record, "Quantity").pop("min_value", None)
    _field(record, "Quantity").pop("max_value", None)


def _unknown_ref(record):
    _member(_encoding(record, "quotedPrice"), "value")["encoding_name"] = (
        "noSuchEncoding"
    )


def _unknown_enum_encoding(record):
    _encoding(record, "sideEnum")["encoding_type"] = "noSuchEncoding"


def _unknown_set_encoding(record):
    _encoding(record, "orderFlags")["encoding_type"] = "noSuchEncoding"


def _signed_enum(record):
    _encoding(record, "sideEnum")["encoding_type"] = "int8"
    for value in _encoding(record, "sideEnum")["valid_values"]:
        value["valid_value"] = "1"


def _array_enum(record):
    _encoding(record, "sideEnum")["encoding_type"] = "idString"


def _char_set(record):
    _encoding(record, "orderFlags")["encoding_type"] = "char"


def _choice_past_bits(record):
    _encoding(record, "orderFlags")["choices"][0]["bit_position"] = 8


def _duplicate_value_name(record):
    values = _encoding(record, "sideEnum")["valid_values"]
    values[1]["symbolic_name"] = values[0]["symbolic_name"]


def _duplicate_choice_name(record):
    choices = _encoding(record, "orderFlags")["choices"]
    choices[1]["symbolic_name"] = choices[0]["symbolic_name"]


def _value_outside_encoding(record):
    _member(_encoding(record, "quotedPrice"), "source")["valid_values"][0][
        "valid_value"
    ] = "256"


def _null_outside_type(record):
    _member(_encoding(record, "price4"), "mantissa")["null_value"] = "4294967296"


def _not_a_number(record):
    _member(_encoding(record, "price4"), "mantissa")["null_value"] = "none"


def _constant_outside_type(record):
    _member(_encoding(record, "price4"), "exponent")["element_value"] = "200"


def _since_after_schema(record):
    _message(record)["block_fields"][-1]["since_version"] = 9


def _deprecated_after_schema(record):
    _message(record)["block_fields"][-1]["deprecated_since"] = 9


def _choice_since_after_schema(record):
    _encoding(record, "orderFlags")["choices"][1]["since_version"] = 9


def _value_since_after_schema(record):
    _encoding(record, "sideEnum")["valid_values"][1]["since_version"] = 9


def _encoding_since_after_schema(record):
    _encoding(record, "sideEnum")["since_version"] = 9


def _message_since_after_schema(record):
    _message(record)["since_version"] = 9


def _out_of_order_field(record):
    fields = _message(record)["block_fields"]
    fields[-2]["since_version"] = 1
    fields[-1]["since_version"] = 0


def _out_of_order_group(record):
    groups = _message(record)["repeating_groups"]
    extra = copy.deepcopy(groups[0])
    groups[0]["since_version"] = 1
    extra["symbolic_name"] = "OtherGroup"
    extra["sbe_id"] = 454
    groups.append(extra)


def _out_of_order_data(record):
    fields = _message(record)["var_data_fields"]
    extra = copy.deepcopy(fields[0])
    fields[0]["since_version"] = 1
    extra["symbolic_name"] = "OtherText"
    extra["sbe_id"] = 59
    fields.append(extra)


def _overlapping_field(record):
    _field(record, "Side")["offset"] = 2


def _overlapping_member(record):
    composite = _encoding(record, "quotedPrice")
    _member(composite, "source")["offset"] = 1


def _offset_past_block(record):
    _message(record)["block_length"] = 40
    _field(record, "Flags").update(offset=50)
    _field(record, "Flags").pop("alignment", None)


def _short_block(record):
    _message(record)["block_length"] = 10


def _short_group_block(record):
    _message(record)["repeating_groups"][0]["block_length"] = 1


def _variable_field(record):
    _field(record, "Quantity")["encoding_name"] = "varText"
    for key in ("null_value", "min_value", "max_value", "semantic_type"):
        _field(record, "Quantity").pop(key, None)


def _group_without_dimension(record):
    _message(record)["repeating_groups"][0]["dimension_type"] = "noSuchEncoding"


def _dimension_without_counter(record):
    composite = _encoding(record, "groupSizeEncoding")
    composite["composite_members"] = [
        m for m in composite["composite_members"] if m["symbolic_name"] != "numInGroup"
    ]
    composite["composite_members"].append(
        {
            "encoding_kind": composite["composite_members"][0]["encoding_kind"],
            "symbolic_name": "other",
            "primitive_type": "uint16",
        }
    )


def _signed_dimension(record):
    _member(_encoding(record, "groupSizeEncoding"), "numInGroup")["primitive_type"] = (
        "int16"
    )


def _data_on_a_plain_type(record):
    _message(record)["var_data_fields"][0]["encoding_name"] = "counter"
    _message(record)["var_data_fields"][0].pop("semantic_type", None)


def _data_without_length(record):
    _member(_encoding(record, "varText"), "length")["symbolic_name"] = "size"


def _data_fixed_length(record):
    _member(_encoding(record, "varText"), "varData")["array_length"] = 4


def _composite_of_one(record):
    composite = _encoding(record, "quotedPrice")
    composite["composite_members"] = composite["composite_members"][:1]


def _duplicate_member(record):
    composite = _encoding(record, "quotedPrice")
    composite["composite_members"][1]["symbolic_name"] = "value"


def _field_id_two_names(record):
    _field(record, "Quantity")["sbe_id"] = 11


def _field_name_two_ids(record):
    group = _message(record)["repeating_groups"][0]
    group["block_fields"][0]["symbolic_name"] = "ClientOrderId"


def _unknown_semantic_on_field(record):
    _field(record, "ClientOrderId")["semantic_type"] = "NoSuchDatatype"
    _encoding(record, "idString").pop("semantic_type", None)


def _semantic_mismatch(record):
    _field(record, "ClientOrderId")["semantic_type"] = "Price"


def _constant_type_without_value(record):
    _member(_encoding(record, "price4"), "exponent").pop("element_value")


def _constant_field_without_value(record):
    _field(record, "Quantity")["presence"] = "constant"
    for key in ("null_value", "min_value", "max_value", "semantic_type"):
        _field(record, "Quantity").pop(key, None)


def _unknown_value_ref_enum(record):
    _member(_encoding(record, "price4"), "exponent").update(
        element_value="-4", value_ref="noSuchEnum.venue"
    )


def _unknown_value_ref_value(record):
    _member(_encoding(record, "price4"), "exponent").update(
        element_value="-4", value_ref="sideEnum.NoSuchValue"
    )


def _decimal_without_exponent(record):
    field = _field(record, "LimitPrice")
    field["semantic_type"] = "Price"
    composite = _encoding(record, "price4")
    composite.pop("semantic_type", None)
    _member(composite, "exponent")["symbolic_name"] = "scale"


def _month_without_month(record):
    _encoding(record, "expiry").pop("semantic_type")
    _field(record, "Expiry")["semantic_type"] = "MonthYear"
    _member(_encoding(record, "expiry"), "month")["symbolic_name"] = "moon"


COMMON = [
    (
        "the header's encoding is missing",
        _rename_header,
        [("header_type", "message-header")],
    ),
    (
        "the header lacks a member",
        _header_without_schema_id,
        [("header_type", "message-header")],
    ),
    (
        "the header holds a signed member",
        _signed_template_id,
        [("header_type", "message-header")],
    ),
    (
        "an encoding name is used twice",
        _duplicate_encoding,
        [("LAST_ENCODING", "duplicate-encoding")],
    ),
    (
        "a message name is used twice",
        _duplicate_message_name,
        [("messages/1", "duplicate-message")],
    ),
    (
        "a message id is used twice",
        _duplicate_message_id,
        [("messages/1", "duplicate-message")],
    ),
    (
        "a field names no encoding",
        _unknown_field_encoding,
        [("FIELD_Quantity", "unknown-encoding")],
    ),
    (
        "a ref names no encoding",
        _unknown_ref,
        [("ENC_quotedPrice/composite_members/0", "unknown-encoding")],
    ),
    (
        "an enum names no encoding",
        _unknown_enum_encoding,
        [("ENC_sideEnum", "unknown-encoding")],
    ),
    (
        "a set names no encoding",
        _unknown_set_encoding,
        [("ENC_orderFlags", "unknown-encoding")],
    ),
    (
        "an enum sits on a signed type",
        _signed_enum,
        [("ENC_sideEnum", "enum-encoding")],
    ),
    ("an enum sits on an array", _array_enum, [("ENC_sideEnum", "enum-encoding")]),
    ("a set sits on char", _char_set, [("ENC_orderFlags", "set-encoding")]),
    (
        "a choice is past the encoding's bits",
        _choice_past_bits,
        [("ENC_orderFlags/choices/0", "choice-past-bits")],
    ),
    (
        "two valid values share a name",
        _duplicate_value_name,
        [("ENC_sideEnum", "duplicate-value-name")],
    ),
    (
        "two choices share a name",
        _duplicate_choice_name,
        [("ENC_orderFlags", "duplicate-value-name")],
    ),
    (
        "a valid value does not fit",
        _value_outside_encoding,
        [("ENC_quotedPrice/composite_members/1/valid_values/0", "value-out-of-range")],
    ),
    (
        "a null value does not fit",
        _null_outside_type,
        [("ENC_price4/composite_members/0", "value-out-of-range")],
    ),
    (
        "a null value is no number",
        _not_a_number,
        [("ENC_price4/composite_members/0", "value-out-of-range")],
    ),
    (
        "a constant does not fit",
        _constant_outside_type,
        [("ENC_price4/composite_members/1", "value-out-of-range")],
    ),
    (
        "a field is added after the schema",
        _since_after_schema,
        [("FIELD_LAST", "version-after-schema")],
    ),
    (
        "a field is deprecated after the schema",
        _deprecated_after_schema,
        [("FIELD_LAST", "version-after-schema")],
    ),
    (
        "a choice is added after the schema",
        _choice_since_after_schema,
        [("ENC_orderFlags/choices/1", "version-after-schema")],
    ),
    (
        "a value is added after the schema",
        _value_since_after_schema,
        [("ENC_sideEnum/valid_values/1", "version-after-schema")],
    ),
    (
        "an encoding is added after the schema",
        _encoding_since_after_schema,
        [("ENC_sideEnum", "version-after-schema")],
    ),
    (
        "a message is added after the schema",
        _message_since_after_schema,
        [("messages/0", "version-after-schema")],
    ),
    (
        "an older field follows a newer one",
        _out_of_order_field,
        [("FIELD_LAST", "extension-out-of-order")],
    ),
    (
        "an older group follows a newer one",
        _out_of_order_group,
        [("messages/0/repeating_groups/1", "extension-out-of-order")],
    ),
    (
        "older data follows newer data",
        _out_of_order_data,
        [("messages/0/var_data_fields/1", "extension-out-of-order")],
    ),
    (
        "a field overlaps the one before",
        _overlapping_field,
        [("FIELD_Side", "offset-overlaps")],
    ),
    (
        "a member overlaps the one before",
        _overlapping_member,
        [("ENC_quotedPrice/composite_members/1", "offset-overlaps")],
    ),
    (
        "a field's offset is past the block",
        _offset_past_block,
        [("FIELD_Flags", "offset-past-block"), ("messages/0", "block-too-short")],
    ),
    (
        "a block is shorter than its fields",
        _short_block,
        [("messages/0", "block-too-short")],
    ),
    (
        "a group's block is shorter than its fields",
        _short_group_block,
        [("messages/0/repeating_groups/0", "block-too-short")],
    ),
    (
        "a fixed-length field is variable",
        _variable_field,
        [("FIELD_Quantity", "variable-length-field")],
    ),
    (
        "a group's dimension is missing",
        _group_without_dimension,
        [("messages/0/repeating_groups/0", "group-dimension")],
    ),
    (
        "a dimension has no counter",
        _dimension_without_counter,
        [("messages/0/repeating_groups/0", "group-dimension")],
    ),
    (
        "a dimension holds a signed member",
        _signed_dimension,
        [("messages/0/repeating_groups/0", "group-dimension")],
    ),
    (
        "data sits on a plain type",
        _data_on_a_plain_type,
        [("messages/0/var_data_fields/0", "var-data-encoding")],
    ),
    (
        "data's composite has no length",
        _data_without_length,
        [("messages/0/var_data_fields/0", "var-data-encoding")],
    ),
    (
        "data's composite is not variable",
        _data_fixed_length,
        [("messages/0/var_data_fields/0", "var-data-encoding")],
    ),
    (
        "a composite has one member",
        _composite_of_one,
        [("ENC_quotedPrice", "composite-of-one")],
    ),
    (
        "two members share a name",
        _duplicate_member,
        [("ENC_quotedPrice", "duplicate-member-name")],
    ),
    (
        "one id has two names",
        _field_id_two_names,
        [("FIELD_Quantity", "field-identity")],
    ),
    (
        "one name has two ids",
        _field_name_two_ids,
        [("messages/0/repeating_groups/0/block_fields/0", "field-identity")],
    ),
    (
        "a field's semantic type is no FIX datatype",
        _unknown_semantic_on_field,
        [("FIELD_ClientOrderId", "unknown-semantic-type")],
    ),
    (
        "a constant type has no value",
        _constant_type_without_value,
        [("ENC_price4/composite_members/1", "constant-without-value")],
    ),
    (
        "a constant field has no value",
        _constant_field_without_value,
        [("FIELD_Quantity", "constant-without-value")],
    ),
    (
        "a reference names no enum",
        _unknown_value_ref_enum,
        [("ENC_price4/composite_members/1", "value-ref-unknown")],
    ),
    (
        "a reference names no value",
        _unknown_value_ref_value,
        [("ENC_price4/composite_members/1", "value-ref-unknown")],
    ),
    (
        "a decimal has no exponent",
        _decimal_without_exponent,
        [("FIELD_LimitPrice", "reserved-members")],
    ),
]


def _own_month_without_month(record):
    _member(_encoding(record, "expiry"), "month")["symbolic_name"] = "moon"


ONLY_V1 = [
    (
        "a MonthYear encoding has no month",
        _own_month_without_month,
        [("ENC_expiry", "reserved-members")],
    ),
    (
        "a field's semantic type differs from its encoding's",
        _semantic_mismatch,
        [("FIELD_ClientOrderId", "semantic-type-mismatch")],
    ),
    (
        "a MonthYear has no month",
        _month_without_month,
        [("FIELD_Expiry", "reserved-members")],
    ),
]


def _places(record):
    """What the short names in the tables stand for, in one schema."""
    found = {}
    for s, group in enumerate(record["encoding_sets"]):
        for e, encoding in enumerate(group["encodings"]):
            found[f"ENC_{encoding['symbolic_name']}"] = (
                f"encoding_sets/{s}/encodings/{e}"
            )
    for f, field in enumerate(_message(record)["block_fields"]):
        found[f"FIELD_{field['symbolic_name']}"] = f"messages/0/block_fields/{f}"
    found["FIELD_LAST"] = f"messages/0/block_fields/{f}"
    return found


def _expected(record, wanted):
    places = _places(record)
    last = len(record["encoding_sets"]) - 1
    size = len(record["encoding_sets"][last]["encodings"])
    expanded = []
    for place, rule in wanted:
        head, _, tail = place.partition("/")
        if place == "LAST_ENCODING":
            place = f"encoding_sets/{last}/encodings/{size - 1}"
        elif head in places:
            place = places[head] + ("/" + tail if tail else "")
        expanded.append((place, rule))
    return sorted(expanded)


@pytest.mark.parametrize("edition", ["V1", "V2"])
def test_the_valid_schema_breaks_no_rule(edition):
    assert not rule_errors(SMALL[edition])


@pytest.mark.parametrize(
    ("edition", "name", "change", "wanted"),
    [("V1", *case) for case in COMMON + ONLY_V1] + [("V2", *case) for case in COMMON],
    ids=lambda value: value if isinstance(value, str) else "",
)
def test_each_rule_catches_its_fault(edition, name, change, wanted):
    record = copy.deepcopy(SMALL[edition])
    change(record)
    found = sorted((place, rule) for place, rule, _ in rule_errors(record))
    assert found == _expected(record, wanted), [e for e in rule_errors(record)]


def test_a_presence_mismatch_is_caught():
    """A field's presence differs from its encoding's, in the edition where both can state it."""
    record = copy.deepcopy(SMALL["V1"])
    _encoding(record, "counter")["presence"] = "optional"
    _field(record, "Quantity")["presence"] = "required"
    found = [(place, rule) for place, rule, _ in rule_errors(record)]
    assert found == [("messages/0/block_fields/3", "presence-mismatch")]


def test_a_semantic_type_matches_without_regard_to_case():
    """The specification suggests matching a type's name without regard to case."""
    record = copy.deepcopy(SMALL["V1"])
    _field(record, "ClientOrderId")["semantic_type"] = "STRING"
    assert not rule_errors(record)


def test_a_primitive_may_stand_as_an_enums_encoding():
    """An enum's encoding names a simple type of the schema or a primitive directly."""
    record = copy.deepcopy(SMALL["V1"])
    _encoding(record, "sideEnum")["encoding_type"] = "char"
    assert not rule_errors(record)
