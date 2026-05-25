# About fix-simple-binary-encoding

A LinkML schema for the FIX Simple Binary Encoding (SBE) standard — the binary message encoding protocol defined by the FIX Trading Community's High Performance Working Group.

## Project Status

| Area | Status |
|------|--------|
| LinkML schema | **Complete** — umbrella schema importing `fix_sbe_common`, `fix_sbe_v1_0`, `fix_sbe_v2_0` overlays (4 YAML files) |
| XML→LinkML converter | **Complete** — `scripts/fix_xml_to_linkml.py` converts upstream SBE XML to LinkML-validated YAML |
| SSSOM overlay tool | **Complete** — `scripts/apply_sssom_overlay.py` applies semantic mappings |
| Schema generator | **Complete** — `scripts/schema_to_linkml.py` generates LinkML from upstream XSD |
| Test suite | **78 tests passing** |
| Upstream coverage | SBE v1.0 (RC3, RC4, Standard) and v2.0 (RC1, RC2, RC3) — 10 XML sample files |
| Conformance suite | FIX SBE Conformance Test Suite integrated — 3 schema versions (v0→v1→v2) exercising schema extension mechanism |

## Test Data

- **28** valid YAML fixtures (`tests/data/valid/`) — core LinkML class validation
- **16** invalid YAML fixtures (`tests/data/invalid/`) — negative validation cases
- **21** conformance YAML fixtures (`tests/data/third-party/fix-sbe-conformance/`) — extracted from FIX SBE Conformance schemas covering enums (char + int encoding), composites (messageHeader, groupSizeEncoding, MONTH_YEAR, DATA, decimal, qty), messages with repeating groups and variable-length data, and VersionAttributes progression (sinceVersion)
- **3** conformance XML schemas — progressive versioning (v0 baseline → v1 field extension → v2 var-length data)
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

