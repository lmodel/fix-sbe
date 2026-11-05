---
type: Dataset
id: https://w3id.org/lmodel/fix-sbe/knowledge/datasets/generated-artefacts
genre: reference
title: The generated artefacts
description: "What the generators write from the schema: `project/`, `src/fix_sbe/datamodel/` and `docs/schema/fix_sbe.yaml`. They are committed and never edited."
resource: project
derivedFrom:
  - https://w3id.org/lmodel/fix-sbe/knowledge/datasets/fix-sbe-linkml-schema
sources:
  - id: generators.yaml
    resource: .linkml/generators.yaml
    title: jsonschema
  - id: test_generated_json_schema.py
    resource: tests/test_generated_json_schema.py
    title: test_the_committed_file_is_the_generators_output
  - resource: src/fix_sbe/datamodel
  - resource: docs/schema
generated:
  by: process:ktl-librarian
  at: "2026-11-05T17:57:59Z"
status: draft
---

# The generated artefacts

`.linkml/generators.yaml` holds the generators' settings. Its JSON Schema settings include the range class's descendants, because an encoding set's encodings and a composite's members range over an abstract class.[^generators.yaml]

A test holds the committed JSON Schema to the generator's output.[^test_generated_json_schema.py]

[^generators.yaml]: .linkml/generators.yaml, jsonschema
[^test_generated_json_schema.py]: tests/test_generated_json_schema.py, test_the_committed_file_is_the_generators_output
