---
type: Dataset
id: https://w3id.org/lmodel/fix-sbe/knowledge/datasets/common-module
genre: reference
title: The shared module
description: "`fix_sbe_common`: what SBE 1.0 and SBE 2.0 RC3 define alike, such as the name types, the presence, byte order and primitive value lists, the slots both editions use, and the valid value and the choice."
resource: src/fix_sbe/schema/fix_sbe_common.yaml
isPartOf:
  - https://w3id.org/lmodel/fix-sbe/knowledge/datasets/fix-sbe-linkml-schema
sources:
  - id: common
    resource: src/fix_sbe/schema/fix_sbe_common.yaml
    title: the header and SbeFixDatatype
generated:
  by: process:ktl-librarian
  at: "2026-11-05T17:57:59Z"
status: draft
---

# The shared module

An element's name in the XSD is the alias of its slot.[^common]

`SbeFixDatatype` lists the FIX datatypes the specification's summary table names as a semantic type. No slot ranges over it, because a message's `semantic_type` holds a MsgType value.[^common]

[^common]: src/fix_sbe/schema/fix_sbe_common.yaml, the header and SbeFixDatatype
