"""Where the tests find the repository's files, in one place."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_DIR = ROOT / "src" / "fix_sbe" / "schema"
SCHEMA = SCHEMA_DIR / "fix_sbe.yaml"
UPSTREAM = ROOT / "upstream"
SPEC = UPSTREAM / "fix-simple-binary-encoding"
SUITE = UPSTREAM / "fix-sbe-conformance" / "src" / "main" / "resources"
XSD_V1 = SPEC / "v1-0-STANDARD" / "resources" / "sbe.xsd"
XSD_V2 = SPEC / "v2-0-RC3" / "resources" / "xsd" / "sbe-2.0rc3.xsd"
