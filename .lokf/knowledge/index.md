---
lokf_version: "0.2"
okf_version: "0.2"
base_iri: https://w3id.org/lmodel/fix-sbe/knowledge/
context: https://w3id.org/lokf/context.jsonld
title: fix-sbe Knowledge Bundle
description: FIX Simple Binary Encoding (SBE) 1.0 and 2.0 RC3 (LinkML)
license: https://creativecommons.org/licenses/by/4.0/
publisher:
  type: Person
  id: https://w3id.org/lmodel/fix-sbe/knowledge/person/noel-mcloughlin
  name: Noel McLoughlin
---

# fix-sbe Knowledge Bundle

A [LOKF](https://lokf.nolan-nichols.com) knowledge base for fix-sbe. Every Markdown file under `knowledge/` is one concept; together they form a queryable knowledge graph, derived from this repository's code and docs.

# Workflows

* [Build and test (main.yaml)](workflows/main.md) - The Build and test workflow: on every pull request and push to `main`, it runs `just test` on Python 3.10 to 3.14, and lints the schema and checks the adapt copy on 3.13.
* [Lint and docs (lint-and-docs.yaml)](workflows/lint-and-docs.md) - The static checks on pull requests and on `main`: ShellCheck, actionlint, the governance files' word budgets, markdownlint, lychee and codespell.
* [Semantic release (semantic-release.yml)](workflows/semantic-release.md) - The workflow that computes the next version from Conventional Commits on `main`, promotes the changelog, tags and publishes the GitHub Release, and dispatches the knowledge release.
* [Knowledge registrar (knowledge-registrar.yaml)](workflows/knowledge-registrar.md) - The gate on the bundle: it validates the bundle on each pull request that touches it, and checks who vouched for what.
* [Knowledge librarian (knowledge-librarian.yaml)](workflows/knowledge-librarian.md) - The sidecar's scheduled agent run that keeps the bundle in step with the repository. It stays inert until `KNOWLEDGE_LIBRARIAN_ENABLED` is `true`, and a person merges what it proposes.
* [Knowledge release (knowledge-release.yaml)](workflows/knowledge-release.md) - The workflow that attaches the bundle, a Copilot skill and the schema's adapt copy to a GitHub release, each with its `.sha256` and an attestation, when the bundle or the schema changed.
* [Knowledge sync (knowledge-sync.yaml)](workflows/knowledge-sync.md) - The weekly workflow that keeps the sidecar's copies and the skills pin at the newest release of Knowledge Trust Ladder, by a pull request a person merges.
* [Knowledge website (knowledge-website.yaml)](workflows/knowledge-website.md) - The workflow that builds `website/` on each pull request that touches its inputs, and deploys it from `main` once `KNOWLEDGE_WEBSITE_ENABLED` is `true`.
* [Upstream watch (upstream-watch.yaml)](workflows/upstream-watch.md) - The weekly check that `scripts/check_upstream_release.py` runs: a new tag or edition folder of SBE, a moved tag, a changed or missing pinned file, or a changed licence opens or updates an issue.

# Services

* [Documentation site](services/documentation-site.md) - The knowledge website in `website/`, an Astro Starlight site that the Knowledge website workflow publishes to GitHub Pages at `https://lmodel.github.io/fix-sbe`, built from the README, `docs/`, the schema's pages and this bundle.
* [The converter](services/converter.md) - `scripts/sbe_xml_to_yaml.py`: turns an SBE document in XML into the YAML record the model describes, and stops on anything the schema has no place for. `just sbe-to-yaml` runs it.

# Datasets

* [The fix-sbe LinkML schema](datasets/fix-sbe-linkml-schema.md) - The umbrella schema `src/fix_sbe/schema/fix_sbe.yaml`, which imports one shared module and one module per SBE edition and is the file the project names.
* [The shared module](datasets/common-module.md) - `fix_sbe_common`: what SBE 1.0 and SBE 2.0 RC3 define alike, such as the name types, the presence, byte order and primitive value lists, the slots both editions use, and the valid value and the choice.
* [The SBE 1.0 module](datasets/version-1-module.md) - `fix_sbe_v1_0`: the message schema of SBE 1.0, the final standard with its November 2020 errata, with classes such as `SbeMessageSchemaV1`, `SbeMessageV1`, `SbeFieldV1` and `SbeCompositeV1`.
* [The SBE 2.0 RC3 module](datasets/version-2-module.md) - `fix_sbe_v2_0`: the message schema of SBE 2.0 Release Candidate 3, a draft whose XML namespace is tentative, with classes such as `SbeMessageSchemaV2`, `SbeMessageSetV2`, `SbeMemberTypeV2` and `SbeFieldV2`.
* [The adapt copy](datasets/adapt-copy.md) - `.lokf/fix_sbe.yaml`, which `just lokf-adapt` writes from the schema so that it can sit beside LOKF's: the file this bundle validates against, and the file a release attaches as `schema-<tag>-fix-sbe.yaml`.
* [The neighbours' copies](datasets/neighbour-copies.md) - `tests/neighbours/`: the adapt copies other lmodel repositories release, each the release's schema asset, which tests use to hold this copy's names apart from theirs.
* [The generated artefacts](datasets/generated-artefacts.md) - What the generators write from the schema: `project/`, `src/fix_sbe/datamodel/` and `docs/schema/fix_sbe.yaml`. They are committed and never edited.
* [The example data](datasets/example-data.md) - `tests/data/`: a valid example per class and a counter-example per constraint, named `ClassName-suffix.yaml`, each counter-example naming where it fails on its first line.
* [The copy of the upstream](datasets/upstream-copy.md) - `upstream/`: FIX's XSDs, examples and licences for SBE 1.0 and 2.0 RC3, and three schemas of the conformance suite, unchanged and pinned by git object hash in `scripts/upstream_pins.tsv`.
* [A message template, SBE 1.0](datasets/example-message-v1.md) - A heartbeat with no fields, written as a concept of type `SbeMessageV1`. It shows that the domain schema admits a message template as a concept.
* [A message template, SBE 2.0 RC3](datasets/example-message-v2.md) - A heartbeat with no fields, written as a concept of type `SbeMessageV2`. It shows that the domain schema admits a message template as a concept.

# Explanations

* [Two editions](explanations/two-editions.md) - Why the schema models SBE 1.0 and SBE 2.0 RC3 in separate modules, what the two share, and what SBE 2.0 changes: message and encoding sets, alignment, two shapes of simple type, and a constant on a field.
* [A record of a schema](explanations/a-record-of-a-schema.md) - How an SBE document in XML becomes a YAML record: snake_case slots whose alias is the XML name, eight attributes under another key, and a composite's members in one ordered list.
* [Rules that span a document](explanations/rules-that-span-a-document.md) - What `tests/sbe_rules.py` checks that the XSD and the JSON Schema cannot: references, unique names, versions, layout, the well-known composites, values, and agreement between a field and its encoding.
* [What the model leaves out](explanations/what-the-model-leaves-out.md) - What the schema does not hold: the specification's text, encoded messages, the Simple Open Framing Header, and a closed list on `semantic_type`.
* [What FIX's documents show](explanations/what-the-documents-show.md) - Facts found in FIX's own files: no document holds a `ref`, a `set` or a `choice`; SBE 2.0 RC3's XSD names two versions; and the 1.0 text shows a `ref` with a `semanticType` its XSD does not allow.
* [Mappings](explanations/mappings.md) - Why each element maps to the class of lmodel/fix-orchestra that FIX's transposer carries it to, why a set and a choice stay related, and why nothing is an exact match.

# Glossary

* [Adapt copy](glossary/adapt-copy.md) - An adapt copy: the form of a schema `lokf adapt` writes so that it can sit beside LOKF's, in which concept classes descend from `Concept`. Here it is `.lokf/fix_sbe.yaml`.
* [Message schema](glossary/message-schema.md) - Message schema: the XML document SBE defines, which lists the encodings and message templates two counterparties share. `SbeMessageSchemaV1` and `SbeMessageSchemaV2` describe one.
* [Message template](glossary/message-template.md) - A message template: one kind of message in a schema, with a number that each message's header sends. `SbeMessageV1` and `SbeMessageV2` describe one.
* [Encoding](glossary/encoding.md) - An encoding: how a value is laid out on the wire. SBE has a simple type, a composite, an enumeration and a set, and a field names one by `encoding_name`.
* [Composite](glossary/composite.md) - A composite: an encoding built from members sent one after another, such as a decimal's mantissa and exponent. `SbeCompositeV1` and `SbeCompositeV2` describe one.
* [Block](glossary/block.md) - Block: the body a message and a group entry share, with its fixed-length fields first, then groups, then variable-length data. `SbeBlockV1Mixin` and `SbeBlockV2Mixin` hold it.
* [Semantic type](glossary/semantic-type.md) - A semantic type: what an element means at the FIX application layer. On an encoding or a field it names a FIX datatype, and on a message it holds a FIX MsgType value.
* [Presence](glossary/presence.md) - Presence: whether a value is required, optional or constant. `SbePresence` lists the three, and a value left out counts as required.

# Playbooks

* [Validate a message schema](playbooks/validate-a-message-schema.md) - How to check an SBE document: turn the XML into a record with `scripts/sbe_xml_to_yaml.py`, then run `linkml-validate` naming `SbeMessageSchemaV1` or `SbeMessageSchemaV2`.
* [Regenerate and test](playbooks/regenerate-and-test.md) - How to change the schema: edit a module under `src/fix_sbe/schema/`, run `just lint`, `just gen-project`, `just gen-doc`, `just lokf-adapt` and `just test`, and commit what they write.
* [Update the upstream pins](playbooks/update-upstream-pins.md) - What to do when the watch reports a change in FIX's repositories: read what changed, replace `upstream/`, the pins and the headers together, and let the coverage test show what the schema must follow.
* [Cut a release](playbooks/release.md) - How a release happens: write `## [Unreleased]`, merge with a releasing commit type, and `semantic-release.yml` tags, writes the changelog and dispatches the knowledge release, which attaches the assets.
* [Knowledge sources map](playbooks/knowledge-sources.md) - The librarian's scrape map: every repository location and external source this bundle derives concepts from, how to re-check each, and the tracked paths left out with their reasons.

# Policies

* [AI covenant](policies/ai-covenant.md) - The rules for AI-assisted work here: a person owns every contribution, an element says what the XSD says, a rule states only what the specification states, a mapping follows FIX's transposer or is absent, and FIX's words stay FIX's.
* [Licence and attribution](policies/license-and-attribution.md) - Whose work each part is: the code and the schema under Apache-2.0, the bundle under CC BY 4.0, FIX's XSDs and examples whole and unchanged under CC BY-ND 4.0, and the conformance suite's schemas under Apache-2.0.
* [Security policy](policies/security-policy.md) - How to report a vulnerability, what this repository releases, what executes here and what holds each surface. A report goes through GitHub's private vulnerability reporting, and only the latest release receives fixes.

# References

* [FIX Simple Binary Encoding](references/sbe-specification.md) - The FIX Trading Community's repository for SBE, `FIXTradingCommunity/fix-simple-binary-encoding`, which holds the specification, XSDs and examples of each edition under CC BY-ND 4.0.
* [FIX SBE conformance suite](references/sbe-conformance-suite.md) - `FIXTradingCommunity/fix-sbe-conformance`, FIX's test suite for SBE implementations under Apache-2.0, three of whose SBE 1.0 message schemas this repository holds at the tag `v1.0`.
* [FIX Orchestra transposer](references/orchestra-transposer.md) - `FIXTradingCommunity/orchestra-transposer`, FIX's Apache-2.0 converters between SBE and Orchestra, whose `SBE2Orchestra10_10` and `SBE2Orchestra20_10` classes the schema's mappings follow.
