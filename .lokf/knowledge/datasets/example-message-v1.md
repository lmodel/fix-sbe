---
type: SbeMessageV1
id: https://w3id.org/lmodel/fix-sbe/knowledge/datasets/example-message-v1
genre: reference
title: A message template, SBE 1.0
description: A heartbeat with no fields, written as a concept of type `SbeMessageV1`. It shows that the domain schema admits a message template as a concept.
resource: tests/data/valid/SbeMessageV1-no-members.yaml
symbolic_name: Heartbeat
sbe_id: 1
block_length: 0
semantic_type: "0"
since_version: 1
deprecated_since: 2
derivedFrom:
  - https://w3id.org/lmodel/fix-sbe/knowledge/datasets/example-data
sources:
  - id: test_schema_rules.py
    resource: tests/test_schema_rules.py
    title: test_a_message_concept_validates_against_the_copy
generated:
  by: process:ktl-librarian
  at: "2026-11-05T17:57:59Z"
status: draft
---

# A message template

This concept shows how a host describes a message template: its `type` is `SbeMessageV1`, and its keys are that class's slots beside LOKF's own.[^test_schema_rules.py]

[^test_schema_rules.py]: tests/test_schema_rules.py, test_a_message_concept_validates_against_the_copy
