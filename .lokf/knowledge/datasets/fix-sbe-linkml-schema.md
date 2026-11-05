---
type: Dataset
id: https://w3id.org/lmodel/fix-sbe/knowledge/datasets/fix-sbe-linkml-schema
genre: reference
title: The fix-sbe LinkML schema
description: The umbrella schema `src/fix_sbe/schema/fix_sbe.yaml`, which imports one shared module and one module per SBE edition and is the file the project names.
resource: src/fix_sbe/schema/fix_sbe.yaml
hasPart:
  - https://w3id.org/lmodel/fix-sbe/knowledge/datasets/common-module
  - https://w3id.org/lmodel/fix-sbe/knowledge/datasets/version-1-module
  - https://w3id.org/lmodel/fix-sbe/knowledge/datasets/version-2-module
derivedFrom:
  - https://w3id.org/lmodel/fix-sbe/knowledge/references/sbe-specification
sources:
  - id: schema
    resource: src/fix_sbe/schema/fix_sbe.yaml
    title: the header
  - id: test_coverage.py
    resource: tests/test_coverage.py
    title: the module's description
generated:
  by: process:ktl-librarian
  at: "2026-11-05T17:57:59Z"
status: draft
---

# The fix-sbe LinkML schema

The header pins both editions: SBE 1.0 at the tag `v1.0-errata-Nov-2020`, and SBE 2.0 Release Candidate 3 at commit `418a8f6`.[^schema]

A document of SBE 1.0 starts at `SbeMessageSchemaV1`, the tree root, and one of SBE 2.0 RC3 at `SbeMessageSchemaV2`.[^schema]

A test holds each class to its XSD type, with its attributes, children, ranges, defaults and repeat counts.[^test_coverage.py]

[^schema]: src/fix_sbe/schema/fix_sbe.yaml, the header
[^test_coverage.py]: tests/test_coverage.py, the module's description
