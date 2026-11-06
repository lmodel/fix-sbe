# Datasets

* [The fix-sbe LinkML schema](fix-sbe-linkml-schema.md) - The umbrella schema `src/fix_sbe/schema/fix_sbe.yaml`, which imports one shared module and one module per SBE edition and is the file the project names.
* [The shared module](common-module.md) - `fix_sbe_common`: what SBE 1.0 and SBE 2.0 RC3 define alike, such as the name types, the presence, byte order and primitive value lists, the slots both editions use, and the valid value and the choice.
* [The SBE 1.0 module](version-1-module.md) - `fix_sbe_v1_0`: the message schema of SBE 1.0, the final standard with its November 2020 errata, with classes such as `SbeMessageSchemaV1`, `SbeMessageV1`, `SbeFieldV1` and `SbeCompositeV1`.
* [The SBE 2.0 RC3 module](version-2-module.md) - `fix_sbe_v2_0`: the message schema of SBE 2.0 Release Candidate 3, a draft whose XML namespace is tentative, with classes such as `SbeMessageSchemaV2`, `SbeMessageSetV2`, `SbeMemberTypeV2` and `SbeFieldV2`.
* [The adapt copy](adapt-copy.md) - `.lokf/schema/fix_sbe.yaml`, which `just lokf-adapt` writes from the schema so that it can sit beside LOKF's: the file this bundle validates against, and the file a release attaches as `schema-<tag>-fix-sbe.yaml`.
* [The neighbours' copies](neighbour-copies.md) - `tests/neighbours/`: the adapt copies other lmodel repositories release, each the release's schema asset, which tests use to hold this copy's names apart from theirs.
* [The generated artefacts](generated-artefacts.md) - What the generators write from the schema: `project/`, `src/fix_sbe/datamodel/` and `docs/schema/fix_sbe.yaml`. They are committed and never edited.
* [The example data](example-data.md) - `tests/data/`: a valid example per class and a counter-example per constraint, named `ClassName-suffix.yaml`, each counter-example naming where it fails on its first line.
* [The copy of the upstream](upstream-copy.md) - `upstream/`: FIX's XSDs, examples and licences for SBE 1.0 and 2.0 RC3, and three schemas of the conformance suite, unchanged and pinned by git object hash in `scripts/upstream_pins.tsv`.
* [A message template, SBE 1.0](example-message-v1.md) - A heartbeat with no fields, written as a concept of type `SbeMessageV1`. It shows that the domain schema admits a message template as a concept.
* [A message template, SBE 2.0 RC3](example-message-v2.md) - A heartbeat with no fields, written as a concept of type `SbeMessageV2`. It shows that the domain schema admits a message template as a concept.
