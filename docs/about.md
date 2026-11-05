# About fix-sbe

This page says how the schema reads SBE, where each part comes from, and what the model leaves out. It is for someone who will use the schema or change it.

## Two editions

SBE 1.0 is the final standard, with its November 2020 errata. SBE 2.0 Release Candidate 3 is a draft, and FIX says it differs from 1.0 both on the wire and in its XML. So each has a module, `fix_sbe_v1_0` and `fix_sbe_v2_0`, and each class carries its edition: `SbeFieldV1`, `SbeFieldV2`. `fix_sbe_common` holds what the two define alike, and the umbrella `fix_sbe` imports all three. A host can import one edition's module alone.

| In SBE 2.0 | Compared with SBE 1.0 |
| --- | --- |
| `SbeMessageSetV2` and `SbeEncodingSetV2` | A set may carry a package and may come from another file by XInclude. In 1.0 a schema lists its messages directly. |
| `alignment` | New on a block, a field and a composite's members, and a field cannot have both an alignment and an offset. |
| `SbeSimpleTypeV2`, `SbeMemberTypeV2` | A simple type has two shapes. One stands alone, and one inside a composite can be optional or constant. |
| `element_value` on a field | A field may state its constant, as only a simple type can in 1.0. |
| `semantic_type` | Only a field and a block hold it. In 1.0 an encoding may too. |

## A record of a schema

SBE's schemas are XML, so a record is YAML that `scripts/sbe_xml_to_yaml.py` writes. Each attribute becomes a snake_case slot, and the slot's alias is the XML name. Eight take a different word because the plain one is taken elsewhere in the family: `name` is `symbolic_name`, `id` is `sbe_id`, `type` is `encoding_name`, `version` is `schema_version`, `package` is `schema_package`, `length` is `array_length`, `deprecated` is `deprecated_since` and `epoch` is `time_epoch`.

A composite's members are in one list, each naming its class in `encoding_kind`, because their order is their order on the wire. A message keeps its fields, groups and variable-length data in three lists, because the XSD fixes that sequence.

`upstream/` holds the XSDs, FIX's examples and the conformance suite's schemas, pinned by git object hash. `tests/test_coverage.py` compares each class with its XSD type. `tests/test_documents.py` checks each document with lxml, with the JSON Schema and with a separate walk of the XML.

## Rules that span a document

The XSD and the JSON Schema check one element at a time. `tests/sbe_rules.py` checks what the specification states about one part against another, and each rule has a counter-example in `tests/test_rules.py`.

- **References.** A field, a ref, a group's dimension and an enum's or set's encoding each name something that exists, and a `value_ref` names an enumeration and one of its values.
- **Names.** No two encodings share a name across the sets, a message's name and number are unique, and a field or group's number means one name across the schema, and the other way round.
- **Versions.** Nothing has a `since_version` or `deprecated_since` later than the schema's version, and a later field cannot come before an earlier one in its list.
- **Layout.** An offset does not overlap what came before it or pass the block's end, and a block is long enough for its fields. A field in `block_fields` does not use a variable-length encoding.
- **Well-known composites.** The header has `blockLength`, `templateId`, `schemaId` and `version`. A group's dimension has `blockLength` and `numInGroup`. Variable-length data has `length` and `varData`. Each counter and length is unsigned. A decimal has `mantissa` and `exponent`, and a MonthYear has `year` and `month`.
- **Values.** A null, lowest, highest or constant value fits its primitive type, an enum uses `char` or an unsigned type, a set uses an unsigned type, and a choice's bit fits its encoding.
- **Agreement.** A field and its encoding agree on `semantic_type` and `presence`, where both state them. A field's or an encoding's `semantic_type` is a FIX datatype of the specification's list, ignoring case.

## What the model leaves out

- The specification's text. It is under CC BY-ND 4.0, so every description here is this project's own, and [NOTICE](https://github.com/lmodel/fix-sbe/blob/main/NOTICE) states the position.
- Encoded messages. The schema describes a message schema, not encoded data, so the specification's rules for a received message are out of scope.
- The Simple Open Framing Header, a separate standard that the specification only cites.
- A closed list on `semantic_type` in the schema itself. A message's value is a FIX MsgType, and FIX adds to those.

## What FIX's documents show

- None of them holds a `ref`, a `set` or a `choice`, so `tests/data/valid/` alone exercises those.
- SBE 2.0 RC3's XSD says `2.0RC3` in its `version` attribute and "2.0 RC2" in its header comment.
- The 1.0 text shows a `ref` with a `semanticType`, which the 1.0 XSD does not allow.

## Mappings

Each element maps to the class of lmodel/fix-orchestra that FIX's own transposer carries it to, with `close_mappings`. A set and a choice have no line in the transposer, so they are `related_mappings`. No mapping is exact, because an SBE element has a place on the wire and an Orchestra element does not. `tests/test_mappings.py` lists them.
