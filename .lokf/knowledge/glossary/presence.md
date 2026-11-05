---
type: GlossaryTerm
id: https://w3id.org/lmodel/fix-sbe/knowledge/glossary/presence
title: Presence
description: "Presence: whether a value is required, optional or constant. `SbePresence` lists the three, and a value left out counts as required."
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

# Presence

A constant is not sent, and an optional value that is not set is sent as a null marker.[^common]

[^common]: src/fix_sbe/schema/fix_sbe_common.yaml, the slot or class of that name
