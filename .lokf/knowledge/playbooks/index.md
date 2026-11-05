# Playbooks

* [Validate a message schema](validate-a-message-schema.md) - How to check an SBE document: turn the XML into a record with `scripts/sbe_xml_to_yaml.py`, then run `linkml-validate` naming `SbeMessageSchemaV1` or `SbeMessageSchemaV2`.
* [Regenerate and test](regenerate-and-test.md) - How to change the schema: edit a module under `src/fix_sbe/schema/`, run `just lint`, `just gen-project`, `just gen-doc`, `just lokf-adapt` and `just test`, and commit what they write.
* [Update the upstream pins](update-upstream-pins.md) - What to do when the watch reports a change in FIX's repositories: read what changed, replace `upstream/`, the pins and the headers together, and let the coverage test show what the schema must follow.
* [Cut a release](release.md) - How a release happens: write `## [Unreleased]`, merge with a releasing commit type, and `semantic-release.yml` tags, writes the changelog and dispatches the knowledge release, which attaches the assets.
* [Knowledge sources map](knowledge-sources.md) - The librarian's scrape map: every repository location and external source this bundle derives concepts from, how to re-check each, and the tracked paths left out with their reasons.
