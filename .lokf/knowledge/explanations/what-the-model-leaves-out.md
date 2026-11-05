---
type: Explanation
id: https://w3id.org/lmodel/fix-sbe/knowledge/explanations/what-the-model-leaves-out
genre: explanation
title: What the model leaves out
description: "What the schema does not hold: the specification's text, encoded messages, the Simple Open Framing Header, and a closed list on `semantic_type`."
about:
  - https://w3id.org/lmodel/fix-sbe/knowledge/datasets/fix-sbe-linkml-schema
references:
  - https://w3id.org/lmodel/fix-sbe/knowledge/policies/license-and-attribution
sources:
  - id: about.md
    resource: docs/about.md
    title: What the model leaves out
generated:
  by: process:ktl-librarian
  at: "2026-11-05T17:57:59Z"
status: draft
---

# What the model leaves out

The specification's text is under CC BY-ND 4.0, so every description here is this project's own.[^about.md]

The schema describes a message schema, not encoded data, so the rules for a received message are out of scope. The Simple Open Framing Header is a separate standard.[^about.md]

`semantic_type` has no closed list in the schema itself, because a message's value is a FIX MsgType.[^about.md]

[^about.md]: docs/about.md, What the model leaves out
