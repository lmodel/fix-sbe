---
type: Dataset
id: https://w3id.org/lmodel/fix-sbe/knowledge/datasets/upstream-copy
genre: reference
title: The copy of the upstream
description: "`upstream/`: FIX's XSDs, examples and licences for SBE 1.0 and 2.0 RC3, and three schemas of the conformance suite, unchanged and pinned by git object hash in `scripts/upstream_pins.tsv`."
resource: upstream
derivedFrom:
  - https://w3id.org/lmodel/fix-sbe/knowledge/references/sbe-specification
  - https://w3id.org/lmodel/fix-sbe/knowledge/references/sbe-conformance-suite
sources:
  - id: notice
    resource: NOTICE
    title: FIX Simple Binary Encoding and FIX SBE conformance suite
  - id: test_upstream.py
    resource: tests/test_upstream.py
    title: the module's description
  - resource: scripts/upstream_pins.tsv
generated:
  by: process:ktl-librarian
  at: "2026-11-05T17:57:59Z"
status: draft
---

# The copy of the upstream

The specification's files are under CC BY-ND 4.0, which allows a copy that stays whole and unchanged. The conformance suite's are under Apache-2.0.[^notice]

The tests make the watch's comparison offline, and check the schema's headers against the same pins.[^test_upstream.py]

[^notice]: NOTICE, FIX Simple Binary Encoding and FIX SBE conformance suite
[^test_upstream.py]: tests/test_upstream.py, the module's description
