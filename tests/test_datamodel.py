"""Checks what the generated models and the JSON-LD context do with real documents.

The Pydantic models and the dataclasses load the record of each FIX document, and a composite's
members keep their classes and their order, which is the wire's order.
"""

import json

import pytest
import rdflib
from linkml_runtime.loaders import json_loader

from fix_sbe.datamodel import fix_sbe as dataclasses_module
from fix_sbe.datamodel import fix_sbe_pydantic
from tests import conversion
from tests.paths import ROOT

CONTEXT = ROOT / "project" / "jsonld" / "fix_sbe.context.jsonld"
NAMESPACE = "https://w3id.org/lmodel/fix-sbe/"
DOCUMENTS = sorted(conversion.DOCUMENTS)


@pytest.mark.parametrize("path", DOCUMENTS, ids=lambda p: p.name)
def test_each_document_loads_into_the_pydantic_models(path):
    class_name, record = conversion.record(path)
    assert getattr(fix_sbe_pydantic, class_name)(**record)


@pytest.mark.parametrize("path", DOCUMENTS, ids=lambda p: p.name)
def test_each_document_loads_into_the_dataclasses(path):
    class_name, record = conversion.record(path)
    loaded = json_loader.loads(
        json.dumps(record), target_class=getattr(dataclasses_module, class_name)
    )
    assert loaded


def test_a_composites_members_keep_their_class_and_order():
    """The dataclasses pick each member's class from encoding_kind, in document order."""
    path = next(p for p in DOCUMENTS if p.name == "Examples.xml")
    _, record = conversion.record(path)
    loaded = json_loader.loads(
        json.dumps(record), target_class=dataclasses_module.SbeMessageSchemaV1
    )
    composites = [
        encoding
        for group in loaded.encoding_sets
        for encoding in group.encodings
        if isinstance(encoding, dataclasses_module.SbeCompositeV1)
    ]
    header = next(c for c in composites if c.symbolic_name == "messageHeader")
    members = [m.symbolic_name for m in header.composite_members]
    assert members[:4] == ["blockLength", "templateId", "schemaId", "version"]
    assert all(isinstance(m, dataclasses_module.SbeSimpleTypeV1) for m in header.composite_members)


def test_json_ld_projects_a_key_under_this_schemas_iri():
    """A record joined with the generated context says its facts under fix_sbe's IRIs."""
    context = json.loads(CONTEXT.read_text(encoding="utf-8"))["@context"]
    document = {
        "@context": context,
        "symbolic_name": "OrderEntry",
        "sbe_id": 1,
        "block_length": 8,
    }
    graph = rdflib.Graph().parse(data=json.dumps(document), format="json-ld", base=NAMESPACE)
    predicates = {str(p) for _, p, _ in graph}
    assert f"{NAMESPACE}block_length" in predicates
    assert f"{NAMESPACE}symbolic_name" in predicates
