---
type: Explanation
id: https://w3id.org/lmodel/fix-sbe/knowledge/explanations/a-record-of-a-schema
genre: explanation
title: A record of a schema
description: "How an SBE document in XML becomes a YAML record: snake_case slots whose alias is the XML name, eight attributes under another key, and a composite's members in one ordered list."
about:
  - https://w3id.org/lmodel/fix-sbe/knowledge/datasets/fix-sbe-linkml-schema
references:
  - https://w3id.org/lmodel/fix-sbe/knowledge/services/converter
  - https://w3id.org/lmodel/fix-sbe/knowledge/glossary/composite
sources:
  - id: about.md
    resource: docs/about.md
    title: A record of a schema
generated:
  by: process:ktl-librarian
  at: "2026-11-05T17:57:59Z"
status: draft
---

# A record of a schema

Eight attributes take a different word because the plain one is taken elsewhere in the family: `name` is `symbolic_name`, `id` is `sbe_id`, `type` is `encoding_name`, `version` is `schema_version`, `package` is `schema_package`, `length` is `array_length`, `deprecated` is `deprecated_since` and `epoch` is `time_epoch`.[^about.md]

A composite's members sit in one list because their order is their order on the wire. A message keeps its fields, groups and variable-length data in three lists because the XSD fixes that sequence.[^about.md]

[^about.md]: docs/about.md, A record of a schema
