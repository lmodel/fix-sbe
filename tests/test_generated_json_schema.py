"""Checks the JSON Schema this project commits, as a user of it would read it.

project/jsonschema/fix_sbe.schema.json is what a consumer without LinkML validates with. It is read
here under the draft it declares, and held to the generator's settings in .linkml/generators.yaml.
"""

import json
from functools import cache

import jsonschema
import pytest
import yaml
from linkml.generators.jsonschemagen import JsonSchemaGenerator

from tests.paths import ROOT, SCHEMA

COMMITTED = ROOT / "project" / "jsonschema" / "fix_sbe.schema.json"
DATA = ROOT / "tests" / "data"


@cache
def schema():
    return json.loads(COMMITTED.read_text(encoding="utf-8"))


def validator(class_name):
    wrapped = {"$ref": f"#/$defs/{class_name}", "$defs": schema()["$defs"]}
    return jsonschema.validators.validator_for(wrapped)(wrapped)


def _load(name):
    return yaml.safe_load((DATA / "valid" / f"{name}.yaml").read_text(encoding="utf-8"))


def test_the_schema_is_valid_under_the_draft_it_declares():
    jsonschema.validators.validator_for(schema()).check_schema(schema())


def test_the_committed_file_is_the_generators_output():
    """A schema edit without `just gen-project` fails here."""
    settings = yaml.safe_load((ROOT / ".linkml" / "generators.yaml").read_text())
    args = settings["generator_args"]["jsonschema"]
    generated = JsonSchemaGenerator(str(SCHEMA), **args).serialize()
    assert json.loads(generated) == schema()


def test_the_top_of_the_file_is_a_1_0_message_schema():
    """The root takes the final standard's document, and refuses any other key."""
    assert schema()["title"] == "fix_sbe"
    assert schema()["additionalProperties"] is False
    assert set(schema()["required"]) == {"schema_version", "encoding_sets", "messages"}
    assert not list(
        jsonschema.Draft202012Validator(schema()).iter_errors(
            _load("SbeMessageSchemaV1-small")
        )
    )


def test_every_class_is_closed():
    """A key the XSD does not declare is refused everywhere."""
    for name, definition in schema()["$defs"].items():
        if definition.get("type") == "object":
            assert definition["additionalProperties"] is False, name


@pytest.mark.parametrize("edition", ["V1", "V2"])
def test_each_edition_validates_under_its_own_class(edition):
    name = f"SbeMessageSchema{edition}"
    assert not list(validator(name).iter_errors(_load(f"{name}-small")))


def test_an_edition_refuses_the_others_document():
    assert list(
        validator("SbeMessageSchemaV1").iter_errors(_load("SbeMessageSchemaV2-small"))
    )
    assert list(
        validator("SbeMessageSchemaV2").iter_errors(_load("SbeMessageSchemaV1-small"))
    )


def test_a_rule_reaches_the_file():
    """A rule in the schema is a condition in the committed file, deep inside a document."""
    document = _load("SbeMessageSchemaV2-small")
    field = document["message_sets"][0]["messages"][0]["block_fields"][0]
    field.update(offset=0, alignment=8)
    assert list(validator("SbeMessageSchemaV2").iter_errors(document))
