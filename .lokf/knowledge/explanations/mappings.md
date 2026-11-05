---
type: Explanation
id: https://w3id.org/lmodel/fix-sbe/knowledge/explanations/mappings
genre: explanation
title: Mappings
description: Why each element maps to the class of lmodel/fix-orchestra that FIX's transposer carries it to, why a set and a choice stay related, and why nothing is an exact match.
about:
  - https://w3id.org/lmodel/fix-sbe/knowledge/datasets/fix-sbe-linkml-schema
references:
  - https://w3id.org/lmodel/fix-sbe/knowledge/references/orchestra-transposer
sources:
  - id: about.md
    resource: docs/about.md
    title: Mappings
  - id: test_mappings.py
    resource: tests/test_mappings.py
    title: EXPECTED
generated:
  by: process:ktl-librarian
  at: "2026-11-05T17:57:59Z"
status: draft
---

# Mappings

Each element maps to the Orchestra class FIX's own transposer carries it to, with `close_mappings`. A set and a choice have no line in the transposer, so they are `related_mappings`.[^about.md]

Nothing is exact, since an SBE element sits at a place on the wire and an Orchestra element does not.[^about.md]

A test lists every mapping, and holds each target to lmodel/fix-orchestra's copy once that copy is in `tests/neighbours/`.[^test_mappings.py]

[^about.md]: docs/about.md, Mappings
[^test_mappings.py]: tests/test_mappings.py, EXPECTED
