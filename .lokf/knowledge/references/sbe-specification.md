---
type: Reference
id: https://w3id.org/lmodel/fix-sbe/knowledge/references/sbe-specification
genre: reference
title: FIX Simple Binary Encoding
description: The FIX Trading Community's repository for SBE, `FIXTradingCommunity/fix-simple-binary-encoding`, which holds the specification, XSDs and examples of each edition under CC BY-ND 4.0.
resource: https://github.com/FIXTradingCommunity/fix-simple-binary-encoding
references:
  - https://w3id.org/lmodel/fix-sbe/knowledge/datasets/upstream-copy
sources:
  - id: check
    resource: scripts/check_upstream_release.py
    title: the pins
  - id: notice
    resource: NOTICE
    title: FIX Simple Binary Encoding
generated:
  by: process:ktl-librarian
  at: "2026-11-05T17:57:59Z"
status: draft
---

# FIX Simple Binary Encoding

The project pins SBE 1.0 at the tag `v1.0-errata-Nov-2020`, and SBE 2.0 RC3 at commit `418a8f6`, since no tag names RC3.[^check]

The specification remains the authority on what SBE says.[^notice]

[^check]: scripts/check_upstream_release.py, the pins
[^notice]: NOTICE, FIX Simple Binary Encoding
