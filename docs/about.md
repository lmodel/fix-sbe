# About fix-simple-binary-encoding

A LinkML schema for the FIX Simple Binary Encoding (SBE) standard — the binary message encoding protocol defined by the FIX Trading Community's High Performance Working Group.

## Project Status

| Area | Status |
|------|--------|
| LinkML schema | **Complete** — umbrella `fix_sbe.yaml` imports `fix_sbe_common`, `fix_sbe_v1_0`, `fix_sbe_v2_0` overlays (4 YAML files) |
| XML→LinkML converter | **Complete** — `scripts/fix_xml_to_linkml.py` converts upstream SBE XML to LinkML-validated YAML |
| SSSOM overlay tool | **Complete** — `scripts/apply_sssom_overlay.py` applies semantic mappings |
| Schema generator | **Complete** — `scripts/schema_to_linkml.py` generates LinkML from upstream XSD |
| Test suite | **65 tests passing**, 0 skips |
| Upstream coverage | SBE v1.0 (RC3, RC4, Standard) and v2.0 (RC1, RC2, RC3) — 10 XML files validated end-to-end |
| Conformance suite | FIX SBE Conformance integrated — 3 schema versions (v0 → v1 → v2) exercising the `sinceVersion` extension mechanism |

## Design

### Schema layout

A small umbrella schema imports three version-scoped overlays:

- `fix_sbe.yaml` — top-level umbrella; re-exports common + v1.0 + v2.0
- `fix_sbe_common.yaml` — shared types and slots (`SemanticAttributes`, `VersionAttributes`, `ValidValue`, `Choice`, primitive-type enums)
- `fix_sbe_v1_0.yaml` — `BlockTypeV1`, `MessageSchemaV1`, `EnumTypeV1`, `FieldTypeV1`, …
- `fix_sbe_v2_0.yaml` — `BlockTypeV2`, `MessageSchemaV2`, `MessagesV2`, `TypesV2`, presence/offset/primitive-attribute overlays, …

Splitting by SBE version lets v2 add attributes (offset, presence, primitive-type) without disturbing v1, and lets the converter dispatch to a specific target class per upstream file shape.

### Validation pipeline

Upstream FIX XML is not natively LinkML-readable, so the test pipeline is a two-step *transform then validate*:

```
upstream .xml ──[ scripts/fix_xml_to_linkml.py ]──▶ .yaml ──[ linkml-validate ]──▶ result
                          --target-class                          --target-class
```

The target class is pinned per upstream file in [`tests/test_third_party.py`](../tests/test_third_party.py)'s `CASES` and `CONFORMANCE_SCHEMAS` tables — `MessageSchemaV1`, `MessageSchemaV2`, `MessagesV2`, `TypesV2` — so a new XML shape produces an explicit routing decision rather than a silent fall-through.

### Test corpus layout

Three categories under `tests/data/`:

- `valid/` — hand-authored class-stem fixtures (`<ClassName>-<desc>.yaml`) for round-trip loader checks against the generated Python datamodel
- `invalid/` — negative fixtures
- `third-party/` — upstream artefacts copied in-tree:
    - `fix-sbe/<version>/.../Examples.xml` — official FIX Trading Community samples
    - `fix-sbe-conformance/` — class-stem YAML fixtures derived from the conformance corpus
    - `fix-sbe-conformance/xml/schema{1,2,3}.xml` — raw conformance schemas, isolated in `xml/` so the parent directory keeps its class-stem YAML naming convention

Upstream artefacts are assumed well-formed; the suite intentionally has no separate XML parseability gate. A failure should mean the LinkML schema diverged from the standard, not that an upstream byte got corrupted.

### Test gates

[`tests/test_data.py`](../tests/test_data.py):

- `test_valid_data_files` — load each `valid/*.yaml` via `yaml_loader` against the LinkML-generated Python class derived from the filename stem
- `test_conformance_yaml_files` — same loader gate, over the 21 conformance YAML fixtures

[`tests/test_third_party.py`](../tests/test_third_party.py):

- `test_third_party_xml_validates_against_linkml` — XML → YAML → `linkml-validate` on the 10 upstream SBE samples; errors must stay within the per-file budget (`max_errors`, currently 0 across the board)
- `test_conformance_xml_validates_against_linkml` — same pipeline on the 3 conformance schemas
- `test_conformance_schema_version_progression` — semantic check on `sinceVersion`: every value must be ≤ the schema's own version, and v0 schemas must carry none at all

A session-scoped `fix_record_tally` fixture in [`tests/conftest.py`](../tests/conftest.py) accumulates per-file record counts and reports the corpus-wide total at session teardown (currently **25** records validated across all third-party files).

## Test Data

- **28** valid YAML fixtures (`tests/data/valid/`) — core LinkML class validation
- **16** invalid YAML fixtures (`tests/data/invalid/`) — negative validation cases
- **21** conformance YAML fixtures (`tests/data/third-party/fix-sbe-conformance/`) — extracted from FIX SBE Conformance schemas covering enums (char + int encoding), composites (`messageHeader`, `groupSizeEncoding`, `MONTH_YEAR`, `DATA`, decimal, qty), messages with repeating groups and variable-length data, and `VersionAttributes` progression (`sinceVersion`)
- **3** conformance XML schemas (`tests/data/third-party/fix-sbe-conformance/xml/`) — progressive versioning (v0 baseline → v1 field extension → v2 var-length data)
- **10** upstream SBE XML examples (`tests/data/third-party/fix-sbe/`) — official FIX Trading Community samples

## Schema Coverage

The LinkML schema models:

- **Primitive types** — all SBE wire types (uint8–uint64, int8–int64, float, double, char)
- **Encoded data types** — simple encodings with null/min/max/length attributes
- **Composite data types** — multi-part wire encodings (decimal, timestamp, headers)
- **Enum types** — with char and integer encoding types
- **Set types** — multi-value bitsets with choices
- **Field types** — message fields with presence semantics (required, optional, constant)
- **Block/Message types** — message templates with fixed fields, repeating groups, and variable-length data
- **Message schema** — root container with versioning, byte order, and header type
- **Version attributes** — `sinceVersion` / `deprecated` for schema extension mechanism
- **Semantic attributes** — FIX semantic type mappings

## Upstream Sources

- [FIX Simple Binary Encoding](https://github.com/FIXTradingCommunity/fix-simple-binary-encoding) — specification and XSD
- [FIX SBE Conformance](https://github.com/FIXTradingCommunity/fix-sbe-conformance) — interoperability test suite
