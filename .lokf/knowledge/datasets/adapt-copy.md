---
type: Dataset
id: https://w3id.org/lmodel/fix-sbe/knowledge/datasets/adapt-copy
genre: reference
title: The adapt copy
description: "`.lokf/fix_sbe.yaml`, which `just lokf-adapt` writes from the schema so that it can sit beside LOKF's: the file this bundle validates against, and the file a release attaches as `schema-<tag>-fix-sbe.yaml`."
resource: .lokf/fix_sbe.yaml
derivedFrom:
  - https://w3id.org/lmodel/fix-sbe/knowledge/datasets/fix-sbe-linkml-schema
about:
  - https://w3id.org/lmodel/fix-sbe/knowledge/glossary/adapt-copy
sources:
  - id: readme.md
    resource: README.md
    title: Knowledge Trust Ladder (KTL)
  - id: test_schema_rules.py
    resource: tests/test_schema_rules.py
    title: test_the_copy_keeps_each_class_and_slot and test_copy_roots_the_concept_classes
  - resource: project.justfile
    title: lokf_adapt_roots
generated:
  by: process:ktl-librarian
  at: "2026-11-05T17:57:59Z"
status: draft
---

# The adapt copy

The copy roots a message schema and a message template of each edition on `Concept`, and `just lokf-adapt-check` says when it is stale.[^readme.md]

It keeps every class and slot of the source, folds `description` into LOKF's, and renames nothing.[^test_schema_rules.py]

[^readme.md]: README.md, Knowledge Trust Ladder (KTL)
[^test_schema_rules.py]: tests/test_schema_rules.py, test_the_copy_keeps_each_class_and_slot and test_copy_roots_the_concept_classes
