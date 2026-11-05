---
type: Dataset
id: https://w3id.org/lmodel/fix-sbe/knowledge/datasets/version-2-module
genre: reference
title: The SBE 2.0 RC3 module
description: "`fix_sbe_v2_0`: the message schema of SBE 2.0 Release Candidate 3, a draft whose XML namespace is tentative, with classes such as `SbeMessageSchemaV2`, `SbeMessageSetV2`, `SbeMemberTypeV2` and `SbeFieldV2`."
resource: src/fix_sbe/schema/fix_sbe_v2_0.yaml
isPartOf:
  - https://w3id.org/lmodel/fix-sbe/knowledge/datasets/fix-sbe-linkml-schema
references:
  - https://w3id.org/lmodel/fix-sbe/knowledge/explanations/two-editions
  - https://w3id.org/lmodel/fix-sbe/knowledge/references/sbe-specification
sources:
  - id: v2
    resource: src/fix_sbe/schema/fix_sbe_v2_0.yaml
    title: the header and SbeEncodingSetV2
generated:
  by: process:ktl-librarian
  at: "2026-11-05T17:57:59Z"
status: draft
---

# The SBE 2.0 RC3 module

The module's XSD namespace is `http://fixprotocol.io/2017/sbe`, and its version annotation is the XSD's own `2.0RC3`.[^v2]

An encoding set lists a simple type, a composite, an enumeration or a set. A composite, an enumeration and a set may also appear inside a composite, where a simple type takes another shape, so no single class fits that list.[^v2]

[^v2]: src/fix_sbe/schema/fix_sbe_v2_0.yaml, the header and SbeEncodingSetV2
