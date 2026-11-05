"""The pinned documents and their records, read once for all the tests."""

import importlib.util
from functools import cache

from tests.paths import ROOT, SPEC, SUITE, XSD_V1, XSD_V2

CONVERTER = ROOT / "scripts" / "sbe_xml_to_yaml.py"

# Every document upstream/ holds, the XSD it follows and the class of its root. A fragment is
# not a whole schema, so the rules on a whole schema read it through the document that
# includes it.
DOCUMENTS = {
    SPEC / "v1-0-STANDARD" / "resources" / "Examples.xml": (XSD_V1, "SbeMessageSchemaV1"),
    SPEC / "v2-0-RC3" / "resources" / "xml" / "examples.xml": (XSD_V2, "SbeMessageSchemaV2"),
    SPEC / "v2-0-RC3" / "resources" / "xml" / "types-include.xml": (XSD_V2, "SbeEncodingSetV2"),
    SPEC / "v2-0-RC3" / "resources" / "xml" / "messages-include.xml": (XSD_V2, "SbeMessageSetV2"),
    SUITE / "schema1.xml": (XSD_V1, "SbeMessageSchemaV1"),
    SUITE / "schema2.xml": (XSD_V1, "SbeMessageSchemaV1"),
    SUITE / "schema3.xml": (XSD_V1, "SbeMessageSchemaV1"),
}
WHOLE_SCHEMAS = [path for path, (_, cls) in DOCUMENTS.items() if "MessageSchema" in cls]


@cache
def converter():
    spec = importlib.util.spec_from_file_location("sbe_xml_to_yaml", CONVERTER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@cache
def record(path):
    """The class a document's root stands for, and its record."""
    return converter().convert(path)
