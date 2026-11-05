---
type: Reference
id: https://w3id.org/lmodel/fix-sbe/knowledge/references/orchestra-transposer
genre: reference
title: FIX Orchestra transposer
description: "`FIXTradingCommunity/orchestra-transposer`, FIX's Apache-2.0 converters between SBE and Orchestra, whose `SBE2Orchestra10_10` and `SBE2Orchestra20_10` classes the schema's mappings follow."
resource: https://github.com/FIXTradingCommunity/orchestra-transposer
references:
  - https://w3id.org/lmodel/fix-sbe/knowledge/explanations/mappings
sources:
  - id: v1
    resource: src/fix_sbe/schema/fix_sbe_v1_0.yaml
    title: the notes
  - id: v2
    resource: src/fix_sbe/schema/fix_sbe_v2_0.yaml
    title: the notes
generated:
  by: process:ktl-librarian
  at: "2026-11-05T17:57:59Z"
status: draft
---

# FIX Orchestra transposer

The mappings of the SBE 1.0 module follow `SBE2Orchestra10_10`.[^v1]

The mappings of the SBE 2.0 module follow `SBE2Orchestra20_10`, which carries SBE 2.0 to Orchestra 1.0.[^v2]

[^v1]: src/fix_sbe/schema/fix_sbe_v1_0.yaml, the notes
[^v2]: src/fix_sbe/schema/fix_sbe_v2_0.yaml, the notes
