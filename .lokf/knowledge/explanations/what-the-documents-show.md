---
type: Explanation
id: https://w3id.org/lmodel/fix-sbe/knowledge/explanations/what-the-documents-show
genre: explanation
title: What FIX's documents show
description: "Facts found in FIX's own files: no document holds a `ref`, a `set` or a `choice`; SBE 2.0 RC3's XSD names two versions; and the 1.0 text shows a `ref` with a `semanticType` its XSD does not allow."
about:
  - https://w3id.org/lmodel/fix-sbe/knowledge/datasets/upstream-copy
sources:
  - id: about.md
    resource: docs/about.md
    title: What FIX's documents show
  - id: test_documents.py
    resource: tests/test_documents.py
    title: test_the_documents_are_not_trivial
generated:
  by: process:ktl-librarian
  at: "2026-11-05T17:57:59Z"
status: draft
---

# What FIX's documents show

None of the documents holds a `ref`, a `set` or a `choice`, so the project's own examples alone exercise those.[^test_documents.py]

SBE 2.0 RC3's XSD says `2.0RC3` in its `version` attribute and "2.0 RC2" in its header comment. The 1.0 text shows a `ref` with a `semanticType`, which the 1.0 XSD does not allow.[^about.md]

[^about.md]: docs/about.md, What FIX's documents show
[^test_documents.py]: tests/test_documents.py, test_the_documents_are_not_trivial
