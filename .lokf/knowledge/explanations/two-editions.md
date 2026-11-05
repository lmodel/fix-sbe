---
type: Explanation
id: https://w3id.org/lmodel/fix-sbe/knowledge/explanations/two-editions
genre: explanation
title: Two editions
description: "Why the schema models SBE 1.0 and SBE 2.0 RC3 in separate modules, what the two share, and what SBE 2.0 changes: message and encoding sets, alignment, two shapes of simple type, and a constant on a field."
about:
  - https://w3id.org/lmodel/fix-sbe/knowledge/datasets/version-1-module
  - https://w3id.org/lmodel/fix-sbe/knowledge/datasets/version-2-module
sources:
  - id: about.md
    resource: docs/about.md
    title: Two editions
generated:
  by: process:ktl-librarian
  at: "2026-11-05T17:57:59Z"
status: draft
---

# Two editions

SBE 1.0 is the final standard, with its November 2020 errata. SBE 2.0 Release Candidate 3 is a draft. FIX says the two differ on the wire and in their XML, so each has a module, and each class carries its edition.[^about.md]

SBE 2.0 adds message and encoding sets, which may come from another file, and alignment. It gives a simple type two shapes, lets a field state its constant, and holds `semantic_type` on a field and a block only.[^about.md]

[^about.md]: docs/about.md, Two editions
