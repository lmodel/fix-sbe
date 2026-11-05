---
type: Service
id: https://w3id.org/lmodel/fix-sbe/knowledge/workflows/knowledge-release
genre: reference
title: Knowledge release (knowledge-release.yaml)
description: The workflow that attaches the bundle, a Copilot skill and the schema's adapt copy to a GitHub release, each with its `.sha256` and an attestation, when the bundle or the schema changed.
resource: .github/workflows/knowledge-release.yaml
references:
  - https://w3id.org/lmodel/fix-sbe/knowledge/datasets/adapt-copy
sources:
  - id: security.md
    resource: SECURITY.md
    title: What this repository releases and What executes here
generated:
  by: process:ktl-librarian
  at: "2026-11-05T17:57:59Z"
status: draft
---

# Knowledge release (knowledge-release.yaml)

The workflow stays inert until dispatched, and only its `attach` job, which runs no third-party packages, can write.[^security.md]

[^security.md]: SECURITY.md, What this repository releases and What executes here
