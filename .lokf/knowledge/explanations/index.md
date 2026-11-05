# Explanations

* [Two editions](two-editions.md) - Why the schema models SBE 1.0 and SBE 2.0 RC3 in separate modules, what the two share, and what SBE 2.0 changes: message and encoding sets, alignment, two shapes of simple type, and a constant on a field.
* [A record of a schema](a-record-of-a-schema.md) - How an SBE document in XML becomes a YAML record: snake_case slots whose alias is the XML name, eight attributes under another key, and a composite's members in one ordered list.
* [Rules that span a document](rules-that-span-a-document.md) - What `tests/sbe_rules.py` checks that the XSD and the JSON Schema cannot: references, unique names, versions, layout, the well-known composites, values, and agreement between a field and its encoding.
* [What the model leaves out](what-the-model-leaves-out.md) - What the schema does not hold: the specification's text, encoded messages, the Simple Open Framing Header, and a closed list on `semantic_type`.
* [What FIX's documents show](what-the-documents-show.md) - Facts found in FIX's own files: no document holds a `ref`, a `set` or a `choice`; SBE 2.0 RC3's XSD names two versions; and the 1.0 text shows a `ref` with a `semanticType` its XSD does not allow.
* [Mappings](mappings.md) - Why each element maps to the class of lmodel/fix-orchestra that FIX's transposer carries it to, why a set and a choice stay related, and why nothing is an exact match.
