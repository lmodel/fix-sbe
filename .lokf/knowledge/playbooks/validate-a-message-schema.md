---
type: Playbook
id: https://w3id.org/lmodel/fix-sbe/knowledge/playbooks/validate-a-message-schema
genre: how-to
title: Validate a message schema
description: "How to check an SBE document: turn the XML into a record with `scripts/sbe_xml_to_yaml.py`, then run `linkml-validate` naming `SbeMessageSchemaV1` or `SbeMessageSchemaV2`."
references:
  - https://w3id.org/lmodel/fix-sbe/knowledge/services/converter
  - https://w3id.org/lmodel/fix-sbe/knowledge/explanations/rules-that-span-a-document
sources:
  - id: index.md
    resource: docs/index.md
    title: Validating a message schema and What the validator cannot check
generated:
  by: process:ktl-librarian
  at: "2026-11-05T17:57:59Z"
status: draft
---

# Validate a message schema

1. Run `uv run scripts/sbe_xml_to_yaml.py my-schema.xml --out my-schema.yaml`.[^index.md]
2. Run `uv run linkml-validate -s src/fix_sbe/schema/fix_sbe.yaml -C SbeMessageSchemaV1 my-schema.yaml`. For SBE 2.0, name `SbeMessageSchemaV2`.[^index.md]

`project/jsonschema/fix_sbe.schema.json` is the same schema for anyone without LinkML, and its `$defs` hold each class.[^index.md]

The validator checks one element at a time, and `tests/sbe_rules.py` holds what compares one part of a document with another.[^index.md]

[^index.md]: docs/index.md, Validating a message schema and What the validator cannot check
