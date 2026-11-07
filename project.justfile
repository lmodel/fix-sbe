## Add your own just recipes here. This is imported by the main justfile.

# Overriding recipes from the root justfile by adding a recipe with the same
# name in this file is not possible until a known issue in just is fixed,
# https://github.com/casey/just/issues/2540

# Turn an SBE message schema in XML into the record the model describes, on standard output.
[group('model development')]
sbe-to-yaml FILE:
  uv run --quiet scripts/sbe_xml_to_yaml.py {{FILE}}

# ============ Knowledge bundle: the adapted domain schema ============

# `.lokf/schema/fix_sbe.yaml` is the copy `lokf adapt` writes from the schema so that it can sit
# beside `.lokf/schema/lokf.yaml` (`lokf adapt --help` lists the moves). The roots are the two kinds
# of element a person documents: a whole message schema and a message template, in each
# edition. A concept names one of them as its `type`. Everything else stays a value inside
# them. The recipes run the `lokf` the sidecar's floor pins (0.9.0 or later); LOKF_CMD runs
# another, such as a checkout: LOKF_CMD="uv run --project ../lokf lokf" just lokf-adapt
lokf_cmd := env_var_or_default("LOKF_CMD", "uv run --project .lokf lokf")
lokf_adapt_roots := "--root SbeMessageSchemaV1 --root SbeMessageSchemaV2 --root SbeMessageV1 --root SbeMessageV2"

# Rewrite .lokf/schema/fix_sbe.yaml from the schema (run after every schema change)
[group('knowledge bundle')]
lokf-adapt:
  {{lokf_cmd}} adapt {{source_schema_path}} {{lokf_adapt_roots}} --lokf .lokf/schema/lokf.yaml -o .lokf/schema/fix_sbe.yaml

# Fail when .lokf/schema/fix_sbe.yaml is stale against the schema or .lokf/schema/lokf.yaml
[group('knowledge bundle')]
lokf-adapt-check:
  {{lokf_cmd}} adapt {{source_schema_path}} {{lokf_adapt_roots}} --lokf .lokf/schema/lokf.yaml -o .lokf/schema/fix_sbe.yaml --check

# ============ Artefacts gen-project does not write ============

# Write one LinkML YAML with every import merged, as the copier template's recipe does
[group('model development - extended')]
gen-merged-schema:
  mkdir -p {{dest}}/linkml
  uv run gen-linkml --mergeimports -o {{dest}}/linkml/{{schema_name}}.merged.linkml.yaml {{source_schema_path}}

# Write the schema as RDF Turtle; gen-project's rdf generator is switched off in LinkML
[group('model development - extended')]
gen-rdf:
  mkdir -p {{dest}}/rdf
  uv run gen-rdf --mergeimports {{source_schema_path}} > {{dest}}/rdf/{{schema_name}}.ttl
