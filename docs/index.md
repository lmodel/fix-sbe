# fix-sbe

This project is a LinkML model of FIX Simple Binary Encoding (SBE), the FIX Trading Community's standard for binary messages. It describes a message schema in either edition: SBE 1.0, the final standard, and SBE 2.0 Release Candidate 3, a draft that differs on the wire.

- [Schema documentation](elements/index.md), generated from the schema
- [About](about.md): how the schema reads SBE, where each part comes from and what it leaves out
- [`fix_sbe.yaml`](schema/fix_sbe.yaml): the schema, with its modules merged

## Validating a message schema

An SBE message schema is XML, and the model describes the record it makes. The namespace of the root element says which edition a file follows.

```bash
uv run scripts/sbe_xml_to_yaml.py my-schema.xml --out my-schema.yaml
uv run linkml-validate -s src/fix_sbe/schema/fix_sbe.yaml -C SbeMessageSchemaV1 my-schema.yaml
```

For SBE 2.0, name `SbeMessageSchemaV2`. `project/jsonschema/fix_sbe.schema.json` is the same schema for anyone without LinkML, and its `$defs` hold each class.

## A record

```yaml
schema_version: 0
encoding_sets:
  - encodings:
      - encoding_kind: SbeSimpleTypeV1
        symbolic_name: counter
        primitive_type: uint32
messages:
  - symbolic_name: Heartbeat
    sbe_id: 1
```

## What the validator cannot check

`tests/sbe_rules.py` holds what compares one part of a document with another. It names an encoding a field uses, an offset against the sizes before it, a version against the schema's, and the rest of [About](about.md#rules-that-span-a-document).
