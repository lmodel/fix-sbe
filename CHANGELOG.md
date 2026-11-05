# Changelog

All notable changes to this project are documented here. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

The `v0.0.0` tag is a baseline, not a release: it marks where versioning starts so the first real release is `0.1.0` rather than `1.0.0`. The schema stays below 1.0.0 until its shape settles, so a breaking change raises the minor version.

## [Unreleased]

### Added

- **`upstream/`**, holding FIX's XSDs, examples and licences for SBE 1.0 and 2.0 RC3, and the conformance suite's schemas, pinned by git object hash, with a weekly watch.
- **`scripts/sbe_xml_to_yaml.py`**, which turns an SBE document in XML into the record the model describes, and stops on anything the schema has no place for.
- **Rules a validator cannot state** in `tests/sbe_rules.py`, and JSON Schema rules for a constant, a null value and the choice between an offset and an alignment.
- **Tests** that hold each class to its XSD type, take FIX's documents through lxml, the JSON Schema and a separate walk of the XML, hold an example per class and a counter-example per constraint, and find any run of four words shared with the XSDs.
- **`.lokf/fix_sbe.yaml`, the schema's `lokf adapt` copy.** The knowledge release attaches it as `schema-<tag>-fix-sbe.yaml`.
- **The repository's Knowledge Trust Ladder (KTL) knowledge bundle and its sidecar automation**, from the KTL v0.61.0 templates with the lokf floor at 0.9.0, and a knowledge website that replaces the mkdocs site.
- **The governance files**: SECURITY.md, AI_COVENANT.md, NOTICE and the CONTRIBUTING checklist.

### Changed

- **Every class, enum and type takes the `Sbe` prefix and is named for what it is**, such as `SbeFieldV1` for `FieldTypeV1` and `SbeSimpleTypeV1` for `EncodedDataTypeV1`.
- **A composite's members keep their order.** They sit in one list, because their order is the wire's. The old schema split them by kind and lost it.
- **An encoding set's encodings sit in one list**, each naming its class in `encoding_kind`.
- **Eight attributes take another key**: `symbolic_name`, `sbe_id`, `encoding_name`, `schema_version`, `schema_package`, `array_length`, `deprecated_since` and `time_epoch`.
- **The block is a mixin**, so a message can be a knowledge bundle's concept while a group stays a value inside it.
- **Every description is this project's own**, in place of text copied from the XSDs, whose licence forbids sharing an adaptation.
- **The headers pin the editions**: SBE 1.0 at the tag `v1.0-errata-Nov-2020`, and SBE 2.0 RC3 at commit `418a8f6`.
- **The template settings** turn PyPI publishing and the docs preview off, linkml and linkml-runtime are locked at 1.12.1, and the Python project is named `fix-sbe-linkml`.

### Removed

- **The SSSOM sets and their overlay.** Their rows were seeded by hand and are not FIX's statements. The links FIX's transposer supports are mappings on the classes, and SBE's composite now maps to an Orchestra component, as the transposer has it, in place of a datatype.
- **The vendored conformance Java and its Maven project**, and the examples of the release candidates that are not pinned.
- **`scripts/schema_to_linkml.py`.** The schema is written by hand, and `tests/test_coverage.py` holds it to the XSDs.
- **The mkdocs site.**
