---
type: Policy
id: https://w3id.org/lmodel/fix-sbe/knowledge/policies/security-policy
genre: reference
title: Security policy
description: How to report a vulnerability, what this repository releases, what executes here and what holds each surface. A report goes through GitHub's private vulnerability reporting, and only the latest release receives fixes.
resource: SECURITY.md
references:
  - https://w3id.org/lmodel/fix-sbe/knowledge/workflows/semantic-release
  - https://w3id.org/lmodel/fix-sbe/knowledge/workflows/knowledge-release
sources:
  - id: security
    resource: SECURITY.md
    title: Reporting a vulnerability, What this repository releases and Not covered
generated:
  by: process:ktl-librarian
  at: "2026-11-05T17:57:59Z"
status: draft
---

# Security policy

Use GitHub's private vulnerability reporting. Only the latest release receives fixes.[^security]

The documents under `upstream/` are FIX's, and this repository treats them as data: tests validate them, and nothing executes them. The converter follows an XInclude only within the folder of the file it reads.[^security]

A problem in SBE itself belongs with the FIX Trading Community.[^security]

[^security]: SECURITY.md, Reporting a vulnerability, What this repository releases and Not covered
