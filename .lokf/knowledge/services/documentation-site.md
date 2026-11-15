---
type: Service
id: https://w3id.org/lmodel/fix-sbe/knowledge/services/documentation-site
genre: reference
title: Documentation site
description: The knowledge website in `website/`, a Hugo site that the Knowledge website workflow publishes to GitHub Pages at `https://lmodel.github.io/fix-sbe`, built from the README, `docs/`, the schema's pages and this bundle.
resource: website
dependsOn:
  - https://w3id.org/lmodel/fix-sbe/knowledge/datasets/generated-artefacts
references:
  - https://w3id.org/lmodel/fix-sbe/knowledge/workflows/knowledge-website
sources:
  - id: site.toml
    resource: website/site.toml
    title: the site's address, title and redirects
  - id: website-readme.md
    resource: website/README.md
generated:
  by: process:ktl-librarian
  at: "2026-11-15T02:37:45Z"
status: draft
---

# Documentation site

The site replaces the mkdocs site. Its options redirect the old main pages, `/about` and `/elements`, to the new ones, and each old schema page to the page of the same name. A class the schema renamed has no such page.[^site.toml]

`website/README.md` says how to build it.[^website-readme.md]

[^site.toml]: website/site.toml, the site's address, title and redirects
[^website-readme.md]: website/README.md
