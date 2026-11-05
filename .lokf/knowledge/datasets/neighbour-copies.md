---
type: Dataset
id: https://w3id.org/lmodel/fix-sbe/knowledge/datasets/neighbour-copies
genre: reference
title: The neighbours' copies
description: "`tests/neighbours/`: the adapt copies other lmodel repositories release, each the release's schema asset, which tests use to hold this copy's names apart from theirs."
resource: tests/neighbours
references:
  - https://w3id.org/lmodel/fix-sbe/knowledge/datasets/adapt-copy
sources:
  - id: test_schema_rules.py
    resource: tests/test_schema_rules.py
    title: NEIGHBOURS and test_names_apart_from_each_neighbour
generated:
  by: process:ktl-librarian
  at: "2026-11-05T17:57:59Z"
status: draft
---

# The neighbours' copies

Each copy is pinned by its SHA-256, and each came from a release, checked against its `.sha256` and its attestation.[^test_schema_rules.py]

This copy shares no class, enum, type, subset or key with any of them.[^test_schema_rules.py]

[^test_schema_rules.py]: tests/test_schema_rules.py, NEIGHBOURS and test_names_apart_from_each_neighbour
