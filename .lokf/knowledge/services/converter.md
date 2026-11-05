---
type: Service
id: https://w3id.org/lmodel/fix-sbe/knowledge/services/converter
genre: reference
title: The converter
description: "`scripts/sbe_xml_to_yaml.py`: turns an SBE document in XML into the YAML record the model describes, and stops on anything the schema has no place for. `just sbe-to-yaml` runs it."
resource: scripts/sbe_xml_to_yaml.py
references:
  - https://w3id.org/lmodel/fix-sbe/knowledge/datasets/fix-sbe-linkml-schema
  - https://w3id.org/lmodel/fix-sbe/knowledge/explanations/a-record-of-a-schema
sources:
  - id: converter
    resource: scripts/sbe_xml_to_yaml.py
    title: the module's description
  - id: test_documents.py
    resource: tests/test_documents.py
    title: the module's description and test_the_converter_refuses_what_the_schema_has_no_place_for
generated:
  by: process:ktl-librarian
  at: "2026-11-05T17:57:59Z"
status: draft
---

# The converter

The namespace of the root element says which edition a document follows. Each attribute goes under the slot whose alias it is, and a composite's members stay in document order.[^converter]

A stray attribute, element or text stops the run, and an XInclude may bring in a file only from the document's own folder.[^test_documents.py]

A separate walk of the XML, which shares no code with the converter, finds the same tree in each record.[^test_documents.py]

[^converter]: scripts/sbe_xml_to_yaml.py, the module's description
[^test_documents.py]: tests/test_documents.py, the module's description and test_the_converter_refuses_what_the_schema_has_no_place_for
