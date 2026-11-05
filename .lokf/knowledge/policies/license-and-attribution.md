---
type: Policy
id: https://w3id.org/lmodel/fix-sbe/knowledge/policies/license-and-attribution
genre: reference
title: Licence and attribution
description: "Whose work each part is: the code and the schema under Apache-2.0, the bundle under CC BY 4.0, FIX's XSDs and examples whole and unchanged under CC BY-ND 4.0, and the conformance suite's schemas under Apache-2.0."
resource: NOTICE
references:
  - https://w3id.org/lmodel/fix-sbe/knowledge/references/sbe-specification
  - https://w3id.org/lmodel/fix-sbe/knowledge/references/sbe-conformance-suite
sources:
  - id: readme.md
    resource: README.md
    title: License
  - id: notice
    resource: NOTICE
    title: FIX Simple Binary Encoding
  - id: test_own_words.py
    resource: tests/test_own_words.py
    title: the module's description
  - resource: LICENSE
generated:
  by: process:ktl-librarian
  at: "2026-11-05T17:57:59Z"
status: draft
---

# Licence and attribution

The schema and the code are under the Apache License 2.0, and the knowledge bundle is under CC BY 4.0.[^readme.md]

CC BY-ND 4.0 lets a copy of FIX's files travel whole and unchanged, and does not let anyone share an adapted version. So `upstream/` holds those files unchanged, and every title, description and comment here was written from what the element does.[^notice]

A test finds any run of four words shared with the documentation in the XSDs.[^test_own_words.py]

This project is not endorsed by FIX Protocol Limited, and it takes nothing from fixtrading.org, whose terms bar automated copying.[^notice]

[^readme.md]: README.md, License
[^notice]: NOTICE, FIX Simple Binary Encoding
[^test_own_words.py]: tests/test_own_words.py, the module's description
