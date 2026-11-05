---
type: GlossaryTerm
id: https://w3id.org/lmodel/fix-sbe/knowledge/glossary/semantic-type
title: Semantic type
description: "A semantic type: what an element means at the FIX application layer. On an encoding or a field it names a FIX datatype, and on a message it holds a FIX MsgType value."
relatedTo:
  - https://w3id.org/lmodel/fix-sbe/knowledge/datasets/common-module
sources:
  - id: common
    resource: src/fix_sbe/schema/fix_sbe_common.yaml
    title: the slot or class of that name
generated:
  by: process:ktl-librarian
  at: "2026-11-05T17:57:59Z"
status: draft
---

# Semantic type

`tests/sbe_rules.py` checks the semantic type of an encoding and of a field against the list in `SbeFixDatatype`, ignoring case.[^common]

[^common]: src/fix_sbe/schema/fix_sbe_common.yaml, the slot or class of that name
