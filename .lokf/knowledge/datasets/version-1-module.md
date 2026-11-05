---
type: Dataset
id: https://w3id.org/lmodel/fix-sbe/knowledge/datasets/version-1-module
genre: reference
title: The SBE 1.0 module
description: "`fix_sbe_v1_0`: the message schema of SBE 1.0, the final standard with its November 2020 errata, with classes such as `SbeMessageSchemaV1`, `SbeMessageV1`, `SbeFieldV1` and `SbeCompositeV1`."
resource: src/fix_sbe/schema/fix_sbe_v1_0.yaml
isPartOf:
  - https://w3id.org/lmodel/fix-sbe/knowledge/datasets/fix-sbe-linkml-schema
references:
  - https://w3id.org/lmodel/fix-sbe/knowledge/explanations/two-editions
  - https://w3id.org/lmodel/fix-sbe/knowledge/references/sbe-specification
sources:
  - id: v1
    resource: src/fix_sbe/schema/fix_sbe_v1_0.yaml
    title: the header and SbeFieldV1
generated:
  by: process:ktl-librarian
  at: "2026-11-05T17:57:59Z"
status: draft
---

# The SBE 1.0 module

The module's XSD namespace is `http://fixprotocol.io/2016/sbe`, and its version annotation is the XSD's own `1.0 Standard`.[^v1]

`SbeFieldV1` keeps `time_unit`, which is deprecated, and `time_epoch`.[^v1]

[^v1]: src/fix_sbe/schema/fix_sbe_v1_0.yaml, the header and SbeFieldV1
