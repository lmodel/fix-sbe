# Services

* [Documentation site](documentation-site.md) - The knowledge website in `website/`, an Astro Starlight site that the Knowledge website workflow publishes to GitHub Pages at `https://lmodel.github.io/fix-sbe`, built from the README, `docs/`, the schema's pages and this bundle.
* [The converter](converter.md) - `scripts/sbe_xml_to_yaml.py`: turns an SBE document in XML into the YAML record the model describes, and stops on anything the schema has no place for. `just sbe-to-yaml` runs it.
