---
type: GlossaryTerm
id: https://w3id.org/lmodel/fix-sbe/knowledge/glossary/message-schema
title: Message schema
description: "Message schema: the XML document SBE defines, which lists the encodings and message templates two counterparties share. `SbeMessageSchemaV1` and `SbeMessageSchemaV2` describe one."
relatedTo:
  - https://w3id.org/lmodel/fix-sbe/knowledge/datasets/version-1-module
  - https://w3id.org/lmodel/fix-sbe/knowledge/datasets/version-2-module
sources:
  - id: v1
    resource: src/fix_sbe/schema/fix_sbe_v1_0.yaml
    title: the class of that name
generated:
  by: process:ktl-librarian
  at: "2026-11-05T17:57:59Z"
status: draft
---

# Message schema

A record of one has a `schema_version`, at least one encoding set, and at least one message or message set.[^v1]

[^v1]: src/fix_sbe/schema/fix_sbe_v1_0.yaml, the class of that name
