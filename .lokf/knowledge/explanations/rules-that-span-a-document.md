---
type: Explanation
id: https://w3id.org/lmodel/fix-sbe/knowledge/explanations/rules-that-span-a-document
genre: explanation
title: Rules that span a document
description: "What `tests/sbe_rules.py` checks that the XSD and the JSON Schema cannot: references, unique names, versions, layout, the well-known composites, values, and agreement between a field and its encoding."
about:
  - https://w3id.org/lmodel/fix-sbe/knowledge/datasets/fix-sbe-linkml-schema
references:
  - https://w3id.org/lmodel/fix-sbe/knowledge/references/sbe-specification
sources:
  - id: about.md
    resource: docs/about.md
    title: Rules that span a document
  - id: rules
    resource: tests/sbe_rules.py
    title: the module's description
  - resource: tests/test_rules.py
generated:
  by: process:ktl-librarian
  at: "2026-11-05T17:57:59Z"
status: draft
---

# Rules that span a document

The XSD and the JSON Schema check one element at a time. These rules compare one part of a document with another, and each has a counter-example.[^about.md]

Most of them come from the specification's chapter 4, under "Schema validation".[^rules]

[^about.md]: docs/about.md, Rules that span a document
[^rules]: tests/sbe_rules.py, the module's description
