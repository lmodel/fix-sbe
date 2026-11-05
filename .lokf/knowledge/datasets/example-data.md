---
type: Dataset
id: https://w3id.org/lmodel/fix-sbe/knowledge/datasets/example-data
genre: reference
title: The example data
description: "`tests/data/`: a valid example per class and a counter-example per constraint, named `ClassName-suffix.yaml`, each counter-example naming where it fails on its first line."
resource: tests/data
references:
  - https://w3id.org/lmodel/fix-sbe/knowledge/datasets/fix-sbe-linkml-schema
sources:
  - id: test_data.py
    resource: tests/test_data.py
    title: test_every_concrete_class_has_an_example and test_counter_examples_fail_where_they_say
generated:
  by: process:ktl-librarian
  at: "2026-11-05T17:57:59Z"
status: draft
---

# The example data

Each concrete class has a valid example, and a test fails when one lacks it.[^test_data.py]

A counter-example must fail at the place its first line names, and nowhere else but on the way to it.[^test_data.py]

[^test_data.py]: tests/test_data.py, test_every_concrete_class_has_an_example and test_counter_examples_fail_where_they_say
