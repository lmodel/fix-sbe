# Changelog

All notable changes to this project are documented here. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

The `v0.0.0` tag is a baseline, not a release: it marks where versioning starts so the first real release is `0.1.0` rather than `1.0.0`. The schema stays below 1.0.0 until its shape settles, so a breaking change raises the minor version.

## [Unreleased]

## [0.2.0] - 2026-11-07

### Added

- **The schema as RDF Turtle and the merged schema**, in `project/rdf/` and `project/linkml/`, from `just gen-rdf` and `just gen-merged-schema`.

### Changed

- **The bundle's schema files sit in `.lokf/schema/`**: `lokf.yaml` and the `lokf adapt` copy `fix_sbe.yaml`, as KTL v0.62.0 lays them out.

## [0.1.0] - 2026-11-05

### Added

- **`upstream/`**, holding FIX's XSDs, examples and licences for SBE 1.0 and 2.0 RC3, and the conformance suite's schemas, pinned by git object hash, with a weekly watch.
- **`scripts/sbe_xml_to_yaml.py`**, which turns an SBE document in XML into the record the model describes, and stops on anything the schema has no place for, on an XInclude it cannot take, and on a file it cannot read or parse.
- **Rules a validator cannot state** in `tests/sbe_rules.py`, among them a repeated value or bit, a valid value that is its encoding's null or outside its type's range, a `char` of one character and an aligned composite member, and JSON Schema rules for a constant, a null value and the choice between an offset and an alignment.
- **`SbeFixDatatype`**, the datatypes of FIX Latest that a `semantic_type` may name, read from FIX's `orchestrations` repository, with `EncodedText` from the specification's summary table.
- **Tests** that compare each class with its XSD type, and check FIX's documents with lxml, the JSON Schema and a separate walk of the XML. They hold an example per class and a counter-example per constraint, and find any run of four words shared with the XSDs.
- **`.lokf/fix_sbe.yaml`, the schema's `lokf adapt` copy.** The knowledge release attaches it as `schema-<tag>-fix-sbe.yaml`.
- **The repository's Knowledge Trust Ladder (KTL) knowledge bundle and its sidecar automation**, from the KTL v0.61.0 templates with the lokf floor at 0.9.0, and a knowledge website that replaces the mkdocs site.
- **The governance files**: SECURITY.md, AI_COVENANT.md, NOTICE and the CONTRIBUTING checklist.

### Changed

- **Every class, enum and type takes the `Sbe` prefix and is named for what it is**, such as `SbeFieldV1` for `FieldTypeV1` and `SbeSimpleTypeV1` for `EncodedDataTypeV1`.
- **A composite's members keep their order.** They are in one list, because that order is their order on the wire. The old schema split them by kind and lost it.
- **An encoding set's encodings are in one list**, each naming its class in `encoding_kind`.
- **Eight attributes take another key**: `symbolic_name`, `sbe_id`, `encoding_name`, `schema_version`, `schema_package`, `array_length`, `deprecated_since` and `time_epoch`.
- **The block is a mixin**, so a message can be a knowledge bundle's concept while a group stays a value inside it.
- **Every description is this project's own**, in place of text copied from the XSDs, whose licence forbids sharing an adaptation.
- **The headers pin the editions**: SBE 1.0 at the tag `v1.0-errata-Nov-2020`, and SBE 2.0 RC3 at commit `418a8f6`.
- **The template settings** turn PyPI publishing and the docs preview off, linkml and linkml-runtime are locked at 1.12.1, and the Python project is named `fix-sbe-linkml`.

### Removed

- **The SSSOM sets and their overlay.** Their rows are labelled as manual curation and are not FIX's statements. The links FIX's transposer supports are mappings on the classes: SBE's composite now maps to an Orchestra component, as the transposer has it, in place of a datatype, and a composite's member type and a `ref` map to an Orchestra field.
- **The vendored conformance Java and its Maven project**, and the examples of the release candidates that are not pinned.
- **`scripts/schema_to_linkml.py`.** The schema is written by hand, and `tests/test_coverage.py` compares it with the XSDs.
- **The mkdocs site.**
