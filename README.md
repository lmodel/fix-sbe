<a href="https://github.com/linkml/linkml-project-copier"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/copier-org/copier/master/img/badge/badge-grayscale-inverted-border-teal.json" alt="Copier Badge" style="max-width:100%;"/></a>

# fix-sbe

FIX Simple Binary Encoding (SBE) 1.0 and 2.0 RC3 (LinkML)

> **Only want to ask?** Install `ktl-docent` into any agent you use, by a route from [the install page](https://w3id.org/ktl/docs/install/), and ask it about this project. It answers from the bundle and says how far each answer has been checked.
>
> **Agents:** if `.lokf/knowledge/index.md` exists, read it first. `llms.txt` says how to weigh it.

## Documentation Website

[https://lmodel.github.io/fix-sbe](https://lmodel.github.io/fix-sbe)

## What it models

The schema describes a message schema of [FIX Simple Binary Encoding](https://github.com/FIXTradingCommunity/fix-simple-binary-encoding), in the two editions FIX publishes: the 1.0 Technical Standard with its November 2020 errata, and 2.0 Release Candidate 3 as it stood in September 2026, which has a different wire format. It covers encodings, message templates, fields, groups and variable-length data, and the rules the specification states about them.

`upstream/` holds FIX's XSDs and examples, pinned by hash, and `scripts/sbe_xml_to_yaml.py` turns an SBE document in XML into the record the model describes. [docs/about.md](docs/about.md) says how the schema reads SBE and what it leaves out.

## Mappings

* **[lmodel/fix-orchestra](https://github.com/lmodel/fix-orchestra)**: each element maps to the class FIX's own [transposer](https://github.com/FIXTradingCommunity/orchestra-transposer) carries it to, with `close_mappings`, or `related_mappings` for a set and a choice, which it does not carry. `tests/test_mappings.py` lists them.

## Repository Structure

* [docs/](docs/): the website's own pages
* [project/](project/): generated project files (do not edit them)
* [scripts/](scripts/): the converter from XML and the upstream watch
* [src/fix_sbe/schema/](src/fix_sbe/schema): the LinkML schema, which you edit
* [src/fix_sbe/datamodel/](src/fix_sbe/datamodel): the generated Python datamodel
* [tests/](tests/): Python tests, with example data in [data/](tests/data) and the neighbours' adapt copies in [neighbours/](tests/neighbours)
* [upstream/](upstream/): FIX's XSDs, examples and licences, and the conformance suite's schemas, unchanged
* [website/](website/): the Astro Starlight site built from the README, `docs/`, the schema's pages and the knowledge bundle

## Developer Tools

Run `just` to list the project's [just](https://github.com/casey/just/) recipes.

## Knowledge Trust Ladder (KTL)

`.lokf/` holds this project's [KTL](https://w3id.org/ktl/) knowledge bundle. Its domain schema, `.lokf/fix_sbe.yaml`, is the copy `just lokf-adapt` writes from `src/fix_sbe/schema/fix_sbe.yaml`, and `just lokf-adapt-check` says when it is stale. Edit the source, never the copy.

The copy roots a message schema and a message template of each edition on `Concept`. A schema's concept holds its messages inline, each as a concept with its own `id`, `type`, `title` and `description`. In Obsidian, add these to the KTL plugins' *Known LOKF types* setting:

```text
SbeMessageSchemaV1, SbeMessageSchemaV2, SbeMessageV1, SbeMessageV2
```

`description` folds into LOKF's, and no other key needs renaming. `tests/test_schema_rules.py` holds the copy's keys apart from LOKF and the released copies in `tests/neighbours/`, and it lists the keys shared with a neighbour.

## License

The schema and the code are under the Apache License 2.0 ([LICENSE](LICENSE)), and the knowledge bundle in [.lokf/knowledge/](.lokf/knowledge) is under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

FIX's own files in `upstream/` keep their licences: CC BY-ND 4.0 for the specification's XSDs and examples, and Apache-2.0 for the conformance suite. [NOTICE](NOTICE) states the position, and this project is not endorsed by FIX Protocol Limited.

## Contributing and security

[CONTRIBUTING.md](CONTRIBUTING.md) is the checklist for pull requests and
releases, [AI_COVENANT.md](AI_COVENANT.md) sets the rules for AI-assisted work,
[SECURITY.md](SECURITY.md) says how to report a vulnerability, and
[CHANGELOG.md](CHANGELOG.md) records the changes.

## Credits

Built from the [linkml-project-copier](https://github.com/linkml/linkml-project-copier) template ([doi:10.5281/zenodo.15163584](https://doi.org/10.5281/zenodo.15163584)).
