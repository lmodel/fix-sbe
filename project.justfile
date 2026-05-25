## Add your own just recipes here. This is imported by the main justfile.

# Overriding recipes from the root justfile by adding a recipe with the same
# name in this file is not possible until a known issue in just is fixed,
# https://github.com/casey/just/issues/2540

# Validate upstream third-party FIX SBE fixtures (XML well-formedness + optional
# XSD validation when lxml is available). Wired into the main `test` recipe.
[group('model development')]
_test-third-party:
  uv run python -m pytest tests/test_third_party.py -v

# Apply curated SSSOM mapping TSVs to the generated LinkML schema YAMLs.
# Merges SKOS exact/close/broad/narrow/related matches into the matching
# class / enum / type bodies and declares any referenced object-side prefixes.
# Idempotent: re-running on a clean tree produces no further changes. Run
# after `schema_to_linkml.py` regenerates the YAMLs and before `gen-project`.
[group('model development')]
apply-sssom-overlay:
  uv run python scripts/apply_sssom_overlay.py \
    --schema-dir src/fix_sbe//schema \
    --mappings-dir src/fix_sbe//mappings

# Regenerate the LinkML schemas from the upstream SBE XSDs, then overlay the
# curated SSSOM mappings. This is the canonical "rebuild the model" recipe;
# run it whenever the XSDs or the SSSOM TSVs change. Outputs:
#   src/fix_sbe//schema/fix_sbe_common.yaml
#   src/fix_sbe//schema/fix_sbe_v1_0.yaml
#   src/fix_sbe//schema/fix_sbe_v2_0.yaml
#   src/fix_sbe//schema/fix_sbe/.yaml
[group('model development')]
gen-linkml: && apply-sssom-overlay
  uv run python scripts/schema_to_linkml.py
