---
type: GlossaryTerm
id: https://w3id.org/lmodel/fix-sbe/knowledge/glossary/block
title: Block
description: "Block: the body a message and a group entry share, with its fixed-length fields first, then groups, then variable-length data. `SbeBlockV1Mixin` and `SbeBlockV2Mixin` hold it."
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

# Block

The block is a mixin, so a message can be a concept while a group stays a value inside it.[^v1]

[^v1]: src/fix_sbe/schema/fix_sbe_v1_0.yaml, the class of that name
