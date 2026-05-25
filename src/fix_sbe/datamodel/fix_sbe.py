# Auto generated from fix_sbe.yaml by pythongen.py version: 0.0.1
# Generation date: 2026-05-25T19:08:30
# Schema: fix_sbe
#
# id: https://w3id.org/lmodel/fix-sbe
# description: Umbrella LinkML schema for the FIX Simple Binary Encoding (SBE) standard. Imports three overlays: ``fix_sbe_common`` (entities structurally identical across SBE versions, kept unsuffixed) plus two per-version overlays ``fix_sbe_v1_0`` and ``fix_sbe_v2_0`` (remaining version-specific entities, PascalCase names suffixed with ``V1`` or ``V2`` to disambiguate). Per-version validation can be performed by targeting an overlay file directly.
# license: Apache-2.0

import dataclasses
import re
from dataclasses import dataclass
from datetime import (
    date,
    datetime,
    time
)
from typing import (
    Any,
    ClassVar,
    Dict,
    List,
    Optional,
    Union
)

from jsonasobj2 import (
    JsonObj,
    as_dict
)
from linkml_runtime.linkml_model.meta import (
    EnumDefinition,
    PermissibleValue,
    PvFormulaOptions
)
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from linkml_runtime.utils.formatutils import (
    camelcase,
    sfx,
    underscore
)
from linkml_runtime.utils.metamodelcore import (
    bnode,
    empty_dict,
    empty_list
)
from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.yamlutils import (
    YAMLRoot,
    extended_float,
    extended_int,
    extended_str
)
from rdflib import (
    Namespace,
    URIRef
)

from linkml_runtime.linkml_model.types import Integer, String

metamodel_version = "1.11.0"
version = None

# Namespaces
DCT = CurieNamespace('dct', 'http://purl.org/dc/terms/')
FIX_ORCHESTRA = CurieNamespace('fix_orchestra', 'https://w3id.org/lmodel/fix-orchestra/')
FIX_SBE = CurieNamespace('fix_sbe', 'https://w3id.org/lmodel/fix-sbe/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
RDF = CurieNamespace('rdf', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#')
RDFS = CurieNamespace('rdfs', 'http://www.w3.org/2000/01/rdf-schema#')
SBE_V1 = CurieNamespace('sbe_v1', 'http://fixprotocol.io/2016/sbe/')
SBE_V2 = CurieNamespace('sbe_v2', 'http://fixprotocol.io/2017/sbe/')
SCHEMA = CurieNamespace('schema', 'http://schema.org/')
SKOS = CurieNamespace('skos', 'http://www.w3.org/2004/02/skos/core#')
XSD = CurieNamespace('xsd', 'http://www.w3.org/2001/XMLSchema#')
DEFAULT_ = FIX_SBE


# Types
class SymbolicName(String):
    type_class_uri = FIX_SBE["SymbolicName"]
    type_class_curie = "fix_sbe:SymbolicName"
    type_name = "SymbolicName"
    type_model_uri = FIX_SBE.SymbolicName


class QualifiedName(String):
    type_class_uri = FIX_SBE["QualifiedName"]
    type_class_curie = "fix_sbe:QualifiedName"
    type_name = "QualifiedName"
    type_model_uri = FIX_SBE.QualifiedName


# Class references



@dataclass(repr=False)
class SemanticAttributes(YAMLRoot):
    """
    Application layer class. Maps a field to a FIX data type or a template to a FIX message.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIX_SBE["SemanticAttributes"]
    class_class_curie: ClassVar[str] = "fix_sbe:SemanticAttributes"
    class_name: ClassVar[str] = "SemanticAttributes"
    class_model_uri: ClassVar[URIRef] = FIX_SBE.SemanticAttributes

    semantic_type: Optional[str] = None
    description: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.semantic_type is not None and not isinstance(self.semantic_type, str):
            self.semantic_type = str(self.semantic_type)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class VersionAttributes(YAMLRoot):
    """
    Schema versioning supports message extension
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIX_SBE["VersionAttributes"]
    class_class_curie: ClassVar[str] = "fix_sbe:VersionAttributes"
    class_name: ClassVar[str] = "VersionAttributes"
    class_model_uri: ClassVar[URIRef] = FIX_SBE.VersionAttributes

    since_version: Optional[int] = 0
    deprecated: Optional[int] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.since_version is not None and not isinstance(self.since_version, int):
            self.since_version = int(self.since_version)

        if self.deprecated is not None and not isinstance(self.deprecated, int):
            self.deprecated = int(self.deprecated)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ValidValue(YAMLRoot):
    """
    Valid value as a string
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIX_SBE["ValidValue"]
    class_class_curie: ClassVar[str] = "fix_sbe:ValidValue"
    class_name: ClassVar[str] = "ValidValue"
    class_model_uri: ClassVar[URIRef] = FIX_SBE.ValidValue

    name: Union[str, SymbolicName] = None
    description: Optional[str] = None
    value: Optional[str] = None
    since_version: Optional[int] = 0
    deprecated: Optional[int] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.name):
            self.MissingRequiredField("name")
        if not isinstance(self.name, SymbolicName):
            self.name = SymbolicName(self.name)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.value is not None and not isinstance(self.value, str):
            self.value = str(self.value)

        if self.since_version is not None and not isinstance(self.since_version, int):
            self.since_version = int(self.since_version)

        if self.deprecated is not None and not isinstance(self.deprecated, int):
            self.deprecated = int(self.deprecated)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Choice(YAMLRoot):
    """
    A choice within a multi value set. Value is the position within a bitset (zero-based index).
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIX_SBE["Choice"]
    class_class_curie: ClassVar[str] = "fix_sbe:Choice"
    class_name: ClassVar[str] = "Choice"
    class_model_uri: ClassVar[URIRef] = FIX_SBE.Choice

    name: Union[str, SymbolicName] = None
    description: Optional[str] = None
    value: Optional[str] = None
    since_version: Optional[int] = 0
    deprecated: Optional[int] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.name):
            self.MissingRequiredField("name")
        if not isinstance(self.name, SymbolicName):
            self.name = SymbolicName(self.name)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.value is not None and not isinstance(self.value, str):
            self.value = str(self.value)

        if self.since_version is not None and not isinstance(self.since_version, int):
            self.since_version = int(self.since_version)

        if self.deprecated is not None and not isinstance(self.deprecated, int):
            self.deprecated = int(self.deprecated)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class AlignmentAttributesV1(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIX_SBE["AlignmentAttributesV1"]
    class_class_curie: ClassVar[str] = "fix_sbe:AlignmentAttributesV1"
    class_name: ClassVar[str] = "AlignmentAttributesV1"
    class_model_uri: ClassVar[URIRef] = FIX_SBE.AlignmentAttributesV1

    offset: Optional[int] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.offset is not None and not isinstance(self.offset, int):
            self.offset = int(self.offset)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class PresenceAttributesV1(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIX_SBE["PresenceAttributesV1"]
    class_class_curie: ClassVar[str] = "fix_sbe:PresenceAttributesV1"
    class_name: ClassVar[str] = "PresenceAttributesV1"
    class_model_uri: ClassVar[URIRef] = FIX_SBE.PresenceAttributesV1

    presence: Optional[Union[str, "Presence"]] = 'required'
    value_ref: Optional[Union[str, QualifiedName]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.presence is not None and not isinstance(self.presence, Presence):
            self.presence = Presence(self.presence)

        if self.value_ref is not None and not isinstance(self.value_ref, QualifiedName):
            self.value_ref = QualifiedName(self.value_ref)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class BlockTypeV1(YAMLRoot):
    """
    Base type of message and repeating group entry
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIX_SBE["BlockTypeV1"]
    class_class_curie: ClassVar[str] = "fix_sbe:BlockTypeV1"
    class_name: ClassVar[str] = "BlockTypeV1"
    class_model_uri: ClassVar[URIRef] = FIX_SBE.BlockTypeV1

    name: Union[str, SymbolicName] = None
    id: int = None
    field: Optional[Union[Union[dict, "FieldTypeV1"], list[Union[dict, "FieldTypeV1"]]]] = empty_list()
    group: Optional[Union[Union[dict, "GroupTypeV1"], list[Union[dict, "GroupTypeV1"]]]] = empty_list()
    data: Optional[Union[Union[dict, "FieldTypeV1"], list[Union[dict, "FieldTypeV1"]]]] = empty_list()
    block_length: Optional[int] = None
    semantic_type: Optional[str] = None
    description: Optional[str] = None
    since_version: Optional[int] = 0
    deprecated: Optional[int] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.name):
            self.MissingRequiredField("name")
        if not isinstance(self.name, SymbolicName):
            self.name = SymbolicName(self.name)

        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, int):
            self.id = int(self.id)

        self._normalize_inlined_as_list(slot_name="field", slot_type=FieldTypeV1, key_name="name", keyed=False)

        self._normalize_inlined_as_list(slot_name="group", slot_type=GroupTypeV1, key_name="name", keyed=False)

        self._normalize_inlined_as_list(slot_name="data", slot_type=FieldTypeV1, key_name="name", keyed=False)

        if self.block_length is not None and not isinstance(self.block_length, int):
            self.block_length = int(self.block_length)

        if self.semantic_type is not None and not isinstance(self.semantic_type, str):
            self.semantic_type = str(self.semantic_type)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.since_version is not None and not isinstance(self.since_version, int):
            self.since_version = int(self.since_version)

        if self.deprecated is not None and not isinstance(self.deprecated, int):
            self.deprecated = int(self.deprecated)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class GroupTypeV1(BlockTypeV1):
    """
    A repeating group contains an array of entries
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIX_SBE["GroupTypeV1"]
    class_class_curie: ClassVar[str] = "fix_sbe:GroupTypeV1"
    class_name: ClassVar[str] = "GroupTypeV1"
    class_model_uri: ClassVar[URIRef] = FIX_SBE.GroupTypeV1

    name: Union[str, SymbolicName] = None
    id: int = None
    dimension_type: Optional[Union[str, SymbolicName]] = "groupSizeEncoding"

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.dimension_type is not None and not isinstance(self.dimension_type, SymbolicName):
            self.dimension_type = SymbolicName(self.dimension_type)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class EncodedDataTypeV1(YAMLRoot):
    """
    Simple wire encoding consisting of a primitive type or array of primitives
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIX_SBE["EncodedDataTypeV1"]
    class_class_curie: ClassVar[str] = "fix_sbe:EncodedDataTypeV1"
    class_name: ClassVar[str] = "EncodedDataTypeV1"
    class_model_uri: ClassVar[URIRef] = FIX_SBE.EncodedDataTypeV1

    name: Union[str, SymbolicName] = None
    primitive_type: Union[str, "PrimitiveTypeV1"] = None
    null_value: Optional[str] = None
    min_value: Optional[str] = None
    max_value: Optional[str] = None
    length: Optional[int] = 1
    character_encoding: Optional[str] = None
    value: Optional[str] = None
    offset: Optional[int] = None
    presence: Optional[Union[str, "Presence"]] = 'required'
    value_ref: Optional[Union[str, QualifiedName]] = None
    semantic_type: Optional[str] = None
    description: Optional[str] = None
    since_version: Optional[int] = 0
    deprecated: Optional[int] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.name):
            self.MissingRequiredField("name")
        if not isinstance(self.name, SymbolicName):
            self.name = SymbolicName(self.name)

        if self._is_empty(self.primitive_type):
            self.MissingRequiredField("primitive_type")
        if not isinstance(self.primitive_type, PrimitiveTypeV1):
            self.primitive_type = PrimitiveTypeV1(self.primitive_type)

        if self.null_value is not None and not isinstance(self.null_value, str):
            self.null_value = str(self.null_value)

        if self.min_value is not None and not isinstance(self.min_value, str):
            self.min_value = str(self.min_value)

        if self.max_value is not None and not isinstance(self.max_value, str):
            self.max_value = str(self.max_value)

        if self.length is not None and not isinstance(self.length, int):
            self.length = int(self.length)

        if self.character_encoding is not None and not isinstance(self.character_encoding, str):
            self.character_encoding = str(self.character_encoding)

        if self.value is not None and not isinstance(self.value, str):
            self.value = str(self.value)

        if self.offset is not None and not isinstance(self.offset, int):
            self.offset = int(self.offset)

        if self.presence is not None and not isinstance(self.presence, Presence):
            self.presence = Presence(self.presence)

        if self.value_ref is not None and not isinstance(self.value_ref, QualifiedName):
            self.value_ref = QualifiedName(self.value_ref)

        if self.semantic_type is not None and not isinstance(self.semantic_type, str):
            self.semantic_type = str(self.semantic_type)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.since_version is not None and not isinstance(self.since_version, int):
            self.since_version = int(self.since_version)

        if self.deprecated is not None and not isinstance(self.deprecated, int):
            self.deprecated = int(self.deprecated)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class CompositeDataTypeV1(YAMLRoot):
    """
    A wire encoding composed of multiple parts
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIX_SBE["CompositeDataTypeV1"]
    class_class_curie: ClassVar[str] = "fix_sbe:CompositeDataTypeV1"
    class_name: ClassVar[str] = "CompositeDataTypeV1"
    class_model_uri: ClassVar[URIRef] = FIX_SBE.CompositeDataTypeV1

    name: Union[str, SymbolicName] = None
    type: Optional[Union[Union[dict, EncodedDataTypeV1], list[Union[dict, EncodedDataTypeV1]]]] = empty_list()
    enum: Optional[Union[Union[dict, "EnumTypeV1"], list[Union[dict, "EnumTypeV1"]]]] = empty_list()
    set: Optional[Union[Union[dict, "SetTypeV1"], list[Union[dict, "SetTypeV1"]]]] = empty_list()
    composite: Optional[Union[Union[dict, "CompositeDataTypeV1"], list[Union[dict, "CompositeDataTypeV1"]]]] = empty_list()
    ref: Optional[Union[Union[dict, "RefTypeV1"], list[Union[dict, "RefTypeV1"]]]] = empty_list()
    value: Optional[str] = None
    offset: Optional[int] = None
    semantic_type: Optional[str] = None
    description: Optional[str] = None
    since_version: Optional[int] = 0
    deprecated: Optional[int] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.name):
            self.MissingRequiredField("name")
        if not isinstance(self.name, SymbolicName):
            self.name = SymbolicName(self.name)

        self._normalize_inlined_as_list(slot_name="type", slot_type=EncodedDataTypeV1, key_name="name", keyed=False)

        self._normalize_inlined_as_list(slot_name="enum", slot_type=EnumTypeV1, key_name="name", keyed=False)

        self._normalize_inlined_as_list(slot_name="set", slot_type=SetTypeV1, key_name="name", keyed=False)

        self._normalize_inlined_as_list(slot_name="composite", slot_type=CompositeDataTypeV1, key_name="name", keyed=False)

        self._normalize_inlined_as_list(slot_name="ref", slot_type=RefTypeV1, key_name="name", keyed=False)

        if self.value is not None and not isinstance(self.value, str):
            self.value = str(self.value)

        if self.offset is not None and not isinstance(self.offset, int):
            self.offset = int(self.offset)

        if self.semantic_type is not None and not isinstance(self.semantic_type, str):
            self.semantic_type = str(self.semantic_type)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.since_version is not None and not isinstance(self.since_version, int):
            self.since_version = int(self.since_version)

        if self.deprecated is not None and not isinstance(self.deprecated, int):
            self.deprecated = int(self.deprecated)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class EnumTypeV1(YAMLRoot):
    """
    An enumeration of valid values
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIX_SBE["EnumTypeV1"]
    class_class_curie: ClassVar[str] = "fix_sbe:EnumTypeV1"
    class_name: ClassVar[str] = "EnumTypeV1"
    class_model_uri: ClassVar[URIRef] = FIX_SBE.EnumTypeV1

    valid_value: Union[Union[dict, ValidValue], list[Union[dict, ValidValue]]] = None
    name: Union[str, SymbolicName] = None
    encoding_type: Union[str, SymbolicName] = None
    value: Optional[str] = None
    offset: Optional[int] = None
    semantic_type: Optional[str] = None
    description: Optional[str] = None
    since_version: Optional[int] = 0
    deprecated: Optional[int] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.valid_value):
            self.MissingRequiredField("valid_value")
        self._normalize_inlined_as_list(slot_name="valid_value", slot_type=ValidValue, key_name="name", keyed=False)

        if self._is_empty(self.name):
            self.MissingRequiredField("name")
        if not isinstance(self.name, SymbolicName):
            self.name = SymbolicName(self.name)

        if self._is_empty(self.encoding_type):
            self.MissingRequiredField("encoding_type")
        if not isinstance(self.encoding_type, SymbolicName):
            self.encoding_type = SymbolicName(self.encoding_type)

        if self.value is not None and not isinstance(self.value, str):
            self.value = str(self.value)

        if self.offset is not None and not isinstance(self.offset, int):
            self.offset = int(self.offset)

        if self.semantic_type is not None and not isinstance(self.semantic_type, str):
            self.semantic_type = str(self.semantic_type)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.since_version is not None and not isinstance(self.since_version, int):
            self.since_version = int(self.since_version)

        if self.deprecated is not None and not isinstance(self.deprecated, int):
            self.deprecated = int(self.deprecated)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class RefTypeV1(YAMLRoot):
    """
    A reference to any existing encoding type (simple type, enum or set) to reuse as a member of a composite type
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIX_SBE["RefTypeV1"]
    class_class_curie: ClassVar[str] = "fix_sbe:RefTypeV1"
    class_name: ClassVar[str] = "RefTypeV1"
    class_model_uri: ClassVar[URIRef] = FIX_SBE.RefTypeV1

    name: Union[str, SymbolicName] = None
    type: Union[str, SymbolicName] = None
    value: Optional[str] = None
    offset: Optional[int] = None
    since_version: Optional[int] = 0
    deprecated: Optional[int] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.name):
            self.MissingRequiredField("name")
        if not isinstance(self.name, SymbolicName):
            self.name = SymbolicName(self.name)

        if self._is_empty(self.type):
            self.MissingRequiredField("type")
        if not isinstance(self.type, SymbolicName):
            self.type = SymbolicName(self.type)

        if self.value is not None and not isinstance(self.value, str):
            self.value = str(self.value)

        if self.offset is not None and not isinstance(self.offset, int):
            self.offset = int(self.offset)

        if self.since_version is not None and not isinstance(self.since_version, int):
            self.since_version = int(self.since_version)

        if self.deprecated is not None and not isinstance(self.deprecated, int):
            self.deprecated = int(self.deprecated)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class SetTypeV1(YAMLRoot):
    """
    A multi value choice (encoded as a bitset)
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIX_SBE["SetTypeV1"]
    class_class_curie: ClassVar[str] = "fix_sbe:SetTypeV1"
    class_name: ClassVar[str] = "SetTypeV1"
    class_model_uri: ClassVar[URIRef] = FIX_SBE.SetTypeV1

    choice: Union[Union[dict, Choice], list[Union[dict, Choice]]] = None
    name: Union[str, SymbolicName] = None
    encoding_type: Union[str, SymbolicName] = None
    value: Optional[str] = None
    offset: Optional[int] = None
    semantic_type: Optional[str] = None
    description: Optional[str] = None
    since_version: Optional[int] = 0
    deprecated: Optional[int] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.choice):
            self.MissingRequiredField("choice")
        self._normalize_inlined_as_list(slot_name="choice", slot_type=Choice, key_name="name", keyed=False)

        if self._is_empty(self.name):
            self.MissingRequiredField("name")
        if not isinstance(self.name, SymbolicName):
            self.name = SymbolicName(self.name)

        if self._is_empty(self.encoding_type):
            self.MissingRequiredField("encoding_type")
        if not isinstance(self.encoding_type, SymbolicName):
            self.encoding_type = SymbolicName(self.encoding_type)

        if self.value is not None and not isinstance(self.value, str):
            self.value = str(self.value)

        if self.offset is not None and not isinstance(self.offset, int):
            self.offset = int(self.offset)

        if self.semantic_type is not None and not isinstance(self.semantic_type, str):
            self.semantic_type = str(self.semantic_type)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.since_version is not None and not isinstance(self.since_version, int):
            self.since_version = int(self.since_version)

        if self.deprecated is not None and not isinstance(self.deprecated, int):
            self.deprecated = int(self.deprecated)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class FieldTypeV1(YAMLRoot):
    """
    A field of a message of a specified dataType
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIX_SBE["FieldTypeV1"]
    class_class_curie: ClassVar[str] = "fix_sbe:FieldTypeV1"
    class_name: ClassVar[str] = "FieldTypeV1"
    class_model_uri: ClassVar[URIRef] = FIX_SBE.FieldTypeV1

    name: Union[str, SymbolicName] = None
    id: int = None
    type: Union[str, SymbolicName] = None
    epoch: Optional[str] = "unix"
    time_unit: Optional[str] = "nanosecond"
    offset: Optional[int] = None
    presence: Optional[Union[str, "Presence"]] = 'required'
    value_ref: Optional[Union[str, QualifiedName]] = None
    semantic_type: Optional[str] = None
    description: Optional[str] = None
    since_version: Optional[int] = 0
    deprecated: Optional[int] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.name):
            self.MissingRequiredField("name")
        if not isinstance(self.name, SymbolicName):
            self.name = SymbolicName(self.name)

        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, int):
            self.id = int(self.id)

        if self._is_empty(self.type):
            self.MissingRequiredField("type")
        if not isinstance(self.type, SymbolicName):
            self.type = SymbolicName(self.type)

        if self.epoch is not None and not isinstance(self.epoch, str):
            self.epoch = str(self.epoch)

        if self.time_unit is not None and not isinstance(self.time_unit, str):
            self.time_unit = str(self.time_unit)

        if self.offset is not None and not isinstance(self.offset, int):
            self.offset = int(self.offset)

        if self.presence is not None and not isinstance(self.presence, Presence):
            self.presence = Presence(self.presence)

        if self.value_ref is not None and not isinstance(self.value_ref, QualifiedName):
            self.value_ref = QualifiedName(self.value_ref)

        if self.semantic_type is not None and not isinstance(self.semantic_type, str):
            self.semantic_type = str(self.semantic_type)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.since_version is not None and not isinstance(self.since_version, int):
            self.since_version = int(self.since_version)

        if self.deprecated is not None and not isinstance(self.deprecated, int):
            self.deprecated = int(self.deprecated)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class MessageSchemaV1(YAMLRoot):
    """
    Root of XML document, holds all message templates and their elements
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIX_SBE["MessageSchemaV1"]
    class_class_curie: ClassVar[str] = "fix_sbe:MessageSchemaV1"
    class_name: ClassVar[str] = "MessageSchemaV1"
    class_model_uri: ClassVar[URIRef] = FIX_SBE.MessageSchemaV1

    types: Union[str, list[str]] = None
    message: Union[Union[dict, "MessageV1"], list[Union[dict, "MessageV1"]]] = None
    version: int = None
    package: Optional[str] = None
    id: Optional[int] = None
    semantic_version: Optional[str] = None
    description: Optional[str] = None
    byte_order: Optional[Union[str, "ByteOrder"]] = 'littleEndian'
    header_type: Optional[Union[str, SymbolicName]] = "messageHeader"

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.types):
            self.MissingRequiredField("types")
        if not isinstance(self.types, list):
            self.types = [self.types] if self.types is not None else []
        self.types = [v if isinstance(v, str) else str(v) for v in self.types]

        if self._is_empty(self.message):
            self.MissingRequiredField("message")
        self._normalize_inlined_as_list(slot_name="message", slot_type=MessageV1, key_name="name", keyed=False)

        if self._is_empty(self.version):
            self.MissingRequiredField("version")
        if not isinstance(self.version, int):
            self.version = int(self.version)

        if self.package is not None and not isinstance(self.package, str):
            self.package = str(self.package)

        if self.id is not None and not isinstance(self.id, int):
            self.id = int(self.id)

        if self.semantic_version is not None and not isinstance(self.semantic_version, str):
            self.semantic_version = str(self.semantic_version)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.byte_order is not None and not isinstance(self.byte_order, ByteOrder):
            self.byte_order = ByteOrder(self.byte_order)

        if self.header_type is not None and not isinstance(self.header_type, SymbolicName):
            self.header_type = SymbolicName(self.header_type)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class MessageV1(BlockTypeV1):
    """
    A message type, also known as a message template
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIX_SBE["MessageV1"]
    class_class_curie: ClassVar[str] = "fix_sbe:MessageV1"
    class_name: ClassVar[str] = "MessageV1"
    class_model_uri: ClassVar[URIRef] = FIX_SBE.MessageV1

    name: Union[str, SymbolicName] = None
    id: int = None

@dataclass(repr=False)
class AlignmentAttributesV2(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIX_SBE["AlignmentAttributesV2"]
    class_class_curie: ClassVar[str] = "fix_sbe:AlignmentAttributesV2"
    class_name: ClassVar[str] = "AlignmentAttributesV2"
    class_model_uri: ClassVar[URIRef] = FIX_SBE.AlignmentAttributesV2

    alignment: Optional[int] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.alignment is not None and not isinstance(self.alignment, int):
            self.alignment = int(self.alignment)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class OffsetAttributesV2(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIX_SBE["OffsetAttributesV2"]
    class_class_curie: ClassVar[str] = "fix_sbe:OffsetAttributesV2"
    class_name: ClassVar[str] = "OffsetAttributesV2"
    class_model_uri: ClassVar[URIRef] = FIX_SBE.OffsetAttributesV2

    offset: Optional[int] = None
    alignment: Optional[int] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.offset is not None and not isinstance(self.offset, int):
            self.offset = int(self.offset)

        if self.alignment is not None and not isinstance(self.alignment, int):
            self.alignment = int(self.alignment)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class PresenceAttributesV2(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIX_SBE["PresenceAttributesV2"]
    class_class_curie: ClassVar[str] = "fix_sbe:PresenceAttributesV2"
    class_name: ClassVar[str] = "PresenceAttributesV2"
    class_model_uri: ClassVar[URIRef] = FIX_SBE.PresenceAttributesV2

    presence: Optional[Union[str, "Presence"]] = 'required'
    null_value: Optional[str] = None
    min_value: Optional[str] = None
    max_value: Optional[str] = None
    value_ref: Optional[Union[str, QualifiedName]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.presence is not None and not isinstance(self.presence, Presence):
            self.presence = Presence(self.presence)

        if self.null_value is not None and not isinstance(self.null_value, str):
            self.null_value = str(self.null_value)

        if self.min_value is not None and not isinstance(self.min_value, str):
            self.min_value = str(self.min_value)

        if self.max_value is not None and not isinstance(self.max_value, str):
            self.max_value = str(self.max_value)

        if self.value_ref is not None and not isinstance(self.value_ref, QualifiedName):
            self.value_ref = QualifiedName(self.value_ref)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class PrimitiveTypeAttributesV2(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIX_SBE["PrimitiveTypeAttributesV2"]
    class_class_curie: ClassVar[str] = "fix_sbe:PrimitiveTypeAttributesV2"
    class_name: ClassVar[str] = "PrimitiveTypeAttributesV2"
    class_model_uri: ClassVar[URIRef] = FIX_SBE.PrimitiveTypeAttributesV2

    primitive_type: Union[str, "PrimitiveTypeV2"] = None
    length: Optional[int] = 1
    character_encoding: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.primitive_type):
            self.MissingRequiredField("primitive_type")
        if not isinstance(self.primitive_type, PrimitiveTypeV2):
            self.primitive_type = PrimitiveTypeV2(self.primitive_type)

        if self.length is not None and not isinstance(self.length, int):
            self.length = int(self.length)

        if self.character_encoding is not None and not isinstance(self.character_encoding, str):
            self.character_encoding = str(self.character_encoding)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class BlockTypeV2(YAMLRoot):
    """
    Base type of message and repeating group entry
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIX_SBE["BlockTypeV2"]
    class_class_curie: ClassVar[str] = "fix_sbe:BlockTypeV2"
    class_name: ClassVar[str] = "BlockTypeV2"
    class_model_uri: ClassVar[URIRef] = FIX_SBE.BlockTypeV2

    name: Union[str, SymbolicName] = None
    id: int = None
    field: Optional[Union[Union[dict, "FieldTypeV2"], list[Union[dict, "FieldTypeV2"]]]] = empty_list()
    group: Optional[Union[Union[dict, "GroupTypeV2"], list[Union[dict, "GroupTypeV2"]]]] = empty_list()
    data: Optional[Union[Union[dict, "FieldTypeV2"], list[Union[dict, "FieldTypeV2"]]]] = empty_list()
    block_length: Optional[int] = None
    alignment: Optional[int] = None
    semantic_type: Optional[str] = None
    description: Optional[str] = None
    since_version: Optional[int] = 0
    deprecated: Optional[int] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.name):
            self.MissingRequiredField("name")
        if not isinstance(self.name, SymbolicName):
            self.name = SymbolicName(self.name)

        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, int):
            self.id = int(self.id)

        self._normalize_inlined_as_list(slot_name="field", slot_type=FieldTypeV2, key_name="name", keyed=False)

        self._normalize_inlined_as_list(slot_name="group", slot_type=GroupTypeV2, key_name="name", keyed=False)

        self._normalize_inlined_as_list(slot_name="data", slot_type=FieldTypeV2, key_name="name", keyed=False)

        if self.block_length is not None and not isinstance(self.block_length, int):
            self.block_length = int(self.block_length)

        if self.alignment is not None and not isinstance(self.alignment, int):
            self.alignment = int(self.alignment)

        if self.semantic_type is not None and not isinstance(self.semantic_type, str):
            self.semantic_type = str(self.semantic_type)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.since_version is not None and not isinstance(self.since_version, int):
            self.since_version = int(self.since_version)

        if self.deprecated is not None and not isinstance(self.deprecated, int):
            self.deprecated = int(self.deprecated)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class GroupTypeV2(BlockTypeV2):
    """
    A repeating group contains an array of entries
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIX_SBE["GroupTypeV2"]
    class_class_curie: ClassVar[str] = "fix_sbe:GroupTypeV2"
    class_name: ClassVar[str] = "GroupTypeV2"
    class_model_uri: ClassVar[URIRef] = FIX_SBE.GroupTypeV2

    name: Union[str, SymbolicName] = None
    id: int = None
    dimension_type: Optional[Union[str, SymbolicName]] = "groupSizeEncoding"

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.dimension_type is not None and not isinstance(self.dimension_type, SymbolicName):
            self.dimension_type = SymbolicName(self.dimension_type)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class SimpleDataTypeV2(YAMLRoot):
    """
    Simple wire encoding consisting of a primitive type or array of primitives
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIX_SBE["SimpleDataTypeV2"]
    class_class_curie: ClassVar[str] = "fix_sbe:SimpleDataTypeV2"
    class_name: ClassVar[str] = "SimpleDataTypeV2"
    class_model_uri: ClassVar[URIRef] = FIX_SBE.SimpleDataTypeV2

    name: Union[str, SymbolicName] = None
    primitive_type: Union[str, "PrimitiveTypeV2"] = None
    description: Optional[str] = None
    value: Optional[str] = None
    length: Optional[int] = 1
    character_encoding: Optional[str] = None
    since_version: Optional[int] = 0
    deprecated: Optional[int] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.name):
            self.MissingRequiredField("name")
        if not isinstance(self.name, SymbolicName):
            self.name = SymbolicName(self.name)

        if self._is_empty(self.primitive_type):
            self.MissingRequiredField("primitive_type")
        if not isinstance(self.primitive_type, PrimitiveTypeV2):
            self.primitive_type = PrimitiveTypeV2(self.primitive_type)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.value is not None and not isinstance(self.value, str):
            self.value = str(self.value)

        if self.length is not None and not isinstance(self.length, int):
            self.length = int(self.length)

        if self.character_encoding is not None and not isinstance(self.character_encoding, str):
            self.character_encoding = str(self.character_encoding)

        if self.since_version is not None and not isinstance(self.since_version, int):
            self.since_version = int(self.since_version)

        if self.deprecated is not None and not isinstance(self.deprecated, int):
            self.deprecated = int(self.deprecated)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class MemberDataTypeV2(YAMLRoot):
    """
    A simple type used as a member of a composite type
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIX_SBE["MemberDataTypeV2"]
    class_class_curie: ClassVar[str] = "fix_sbe:MemberDataTypeV2"
    class_name: ClassVar[str] = "MemberDataTypeV2"
    class_model_uri: ClassVar[URIRef] = FIX_SBE.MemberDataTypeV2

    name: Union[str, SymbolicName] = None
    primitive_type: Union[str, "PrimitiveTypeV2"] = None
    description: Optional[str] = None
    value: Optional[str] = None
    length: Optional[int] = 1
    character_encoding: Optional[str] = None
    offset: Optional[int] = None
    alignment: Optional[int] = None
    presence: Optional[Union[str, "Presence"]] = 'required'
    null_value: Optional[str] = None
    min_value: Optional[str] = None
    max_value: Optional[str] = None
    value_ref: Optional[Union[str, QualifiedName]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.name):
            self.MissingRequiredField("name")
        if not isinstance(self.name, SymbolicName):
            self.name = SymbolicName(self.name)

        if self._is_empty(self.primitive_type):
            self.MissingRequiredField("primitive_type")
        if not isinstance(self.primitive_type, PrimitiveTypeV2):
            self.primitive_type = PrimitiveTypeV2(self.primitive_type)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.value is not None and not isinstance(self.value, str):
            self.value = str(self.value)

        if self.length is not None and not isinstance(self.length, int):
            self.length = int(self.length)

        if self.character_encoding is not None and not isinstance(self.character_encoding, str):
            self.character_encoding = str(self.character_encoding)

        if self.offset is not None and not isinstance(self.offset, int):
            self.offset = int(self.offset)

        if self.alignment is not None and not isinstance(self.alignment, int):
            self.alignment = int(self.alignment)

        if self.presence is not None and not isinstance(self.presence, Presence):
            self.presence = Presence(self.presence)

        if self.null_value is not None and not isinstance(self.null_value, str):
            self.null_value = str(self.null_value)

        if self.min_value is not None and not isinstance(self.min_value, str):
            self.min_value = str(self.min_value)

        if self.max_value is not None and not isinstance(self.max_value, str):
            self.max_value = str(self.max_value)

        if self.value_ref is not None and not isinstance(self.value_ref, QualifiedName):
            self.value_ref = QualifiedName(self.value_ref)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class CompositeDataTypeV2(YAMLRoot):
    """
    A wire encoding composed of multiple parts
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIX_SBE["CompositeDataTypeV2"]
    class_class_curie: ClassVar[str] = "fix_sbe:CompositeDataTypeV2"
    class_name: ClassVar[str] = "CompositeDataTypeV2"
    class_model_uri: ClassVar[URIRef] = FIX_SBE.CompositeDataTypeV2

    name: Union[str, SymbolicName] = None
    type: Optional[Union[Union[dict, MemberDataTypeV2], list[Union[dict, MemberDataTypeV2]]]] = empty_list()
    enum: Optional[Union[Union[dict, "EnumTypeV2"], list[Union[dict, "EnumTypeV2"]]]] = empty_list()
    set: Optional[Union[Union[dict, "SetTypeV2"], list[Union[dict, "SetTypeV2"]]]] = empty_list()
    composite: Optional[Union[Union[dict, "CompositeDataTypeV2"], list[Union[dict, "CompositeDataTypeV2"]]]] = empty_list()
    ref: Optional[Union[Union[dict, "RefTypeV2"], list[Union[dict, "RefTypeV2"]]]] = empty_list()
    description: Optional[str] = None
    value: Optional[str] = None
    offset: Optional[int] = None
    alignment: Optional[int] = None
    since_version: Optional[int] = 0
    deprecated: Optional[int] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.name):
            self.MissingRequiredField("name")
        if not isinstance(self.name, SymbolicName):
            self.name = SymbolicName(self.name)

        self._normalize_inlined_as_list(slot_name="type", slot_type=MemberDataTypeV2, key_name="name", keyed=False)

        self._normalize_inlined_as_list(slot_name="enum", slot_type=EnumTypeV2, key_name="name", keyed=False)

        self._normalize_inlined_as_list(slot_name="set", slot_type=SetTypeV2, key_name="name", keyed=False)

        self._normalize_inlined_as_list(slot_name="composite", slot_type=CompositeDataTypeV2, key_name="name", keyed=False)

        self._normalize_inlined_as_list(slot_name="ref", slot_type=RefTypeV2, key_name="name", keyed=False)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.value is not None and not isinstance(self.value, str):
            self.value = str(self.value)

        if self.offset is not None and not isinstance(self.offset, int):
            self.offset = int(self.offset)

        if self.alignment is not None and not isinstance(self.alignment, int):
            self.alignment = int(self.alignment)

        if self.since_version is not None and not isinstance(self.since_version, int):
            self.since_version = int(self.since_version)

        if self.deprecated is not None and not isinstance(self.deprecated, int):
            self.deprecated = int(self.deprecated)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class EnumTypeV2(YAMLRoot):
    """
    An enumeration of valid values
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIX_SBE["EnumTypeV2"]
    class_class_curie: ClassVar[str] = "fix_sbe:EnumTypeV2"
    class_name: ClassVar[str] = "EnumTypeV2"
    class_model_uri: ClassVar[URIRef] = FIX_SBE.EnumTypeV2

    valid_value: Union[Union[dict, ValidValue], list[Union[dict, ValidValue]]] = None
    name: Union[str, SymbolicName] = None
    encoding_type: Union[str, SymbolicName] = None
    description: Optional[str] = None
    value: Optional[str] = None
    offset: Optional[int] = None
    alignment: Optional[int] = None
    since_version: Optional[int] = 0
    deprecated: Optional[int] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.valid_value):
            self.MissingRequiredField("valid_value")
        self._normalize_inlined_as_list(slot_name="valid_value", slot_type=ValidValue, key_name="name", keyed=False)

        if self._is_empty(self.name):
            self.MissingRequiredField("name")
        if not isinstance(self.name, SymbolicName):
            self.name = SymbolicName(self.name)

        if self._is_empty(self.encoding_type):
            self.MissingRequiredField("encoding_type")
        if not isinstance(self.encoding_type, SymbolicName):
            self.encoding_type = SymbolicName(self.encoding_type)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.value is not None and not isinstance(self.value, str):
            self.value = str(self.value)

        if self.offset is not None and not isinstance(self.offset, int):
            self.offset = int(self.offset)

        if self.alignment is not None and not isinstance(self.alignment, int):
            self.alignment = int(self.alignment)

        if self.since_version is not None and not isinstance(self.since_version, int):
            self.since_version = int(self.since_version)

        if self.deprecated is not None and not isinstance(self.deprecated, int):
            self.deprecated = int(self.deprecated)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class RefTypeV2(YAMLRoot):
    """
    A reference to any existing encoding type (simple type, enum or set) to reuse as a member of a composite type
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIX_SBE["RefTypeV2"]
    class_class_curie: ClassVar[str] = "fix_sbe:RefTypeV2"
    class_name: ClassVar[str] = "RefTypeV2"
    class_model_uri: ClassVar[URIRef] = FIX_SBE.RefTypeV2

    name: Union[str, SymbolicName] = None
    type: Union[str, SymbolicName] = None
    description: Optional[str] = None
    value: Optional[str] = None
    offset: Optional[int] = None
    alignment: Optional[int] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.name):
            self.MissingRequiredField("name")
        if not isinstance(self.name, SymbolicName):
            self.name = SymbolicName(self.name)

        if self._is_empty(self.type):
            self.MissingRequiredField("type")
        if not isinstance(self.type, SymbolicName):
            self.type = SymbolicName(self.type)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.value is not None and not isinstance(self.value, str):
            self.value = str(self.value)

        if self.offset is not None and not isinstance(self.offset, int):
            self.offset = int(self.offset)

        if self.alignment is not None and not isinstance(self.alignment, int):
            self.alignment = int(self.alignment)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class SetTypeV2(YAMLRoot):
    """
    A multi value choice (encoded as a bitset)
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIX_SBE["SetTypeV2"]
    class_class_curie: ClassVar[str] = "fix_sbe:SetTypeV2"
    class_name: ClassVar[str] = "SetTypeV2"
    class_model_uri: ClassVar[URIRef] = FIX_SBE.SetTypeV2

    choice: Union[Union[dict, Choice], list[Union[dict, Choice]]] = None
    name: Union[str, SymbolicName] = None
    encoding_type: Union[str, SymbolicName] = None
    description: Optional[str] = None
    value: Optional[str] = None
    offset: Optional[int] = None
    alignment: Optional[int] = None
    since_version: Optional[int] = 0
    deprecated: Optional[int] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.choice):
            self.MissingRequiredField("choice")
        self._normalize_inlined_as_list(slot_name="choice", slot_type=Choice, key_name="name", keyed=False)

        if self._is_empty(self.name):
            self.MissingRequiredField("name")
        if not isinstance(self.name, SymbolicName):
            self.name = SymbolicName(self.name)

        if self._is_empty(self.encoding_type):
            self.MissingRequiredField("encoding_type")
        if not isinstance(self.encoding_type, SymbolicName):
            self.encoding_type = SymbolicName(self.encoding_type)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.value is not None and not isinstance(self.value, str):
            self.value = str(self.value)

        if self.offset is not None and not isinstance(self.offset, int):
            self.offset = int(self.offset)

        if self.alignment is not None and not isinstance(self.alignment, int):
            self.alignment = int(self.alignment)

        if self.since_version is not None and not isinstance(self.since_version, int):
            self.since_version = int(self.since_version)

        if self.deprecated is not None and not isinstance(self.deprecated, int):
            self.deprecated = int(self.deprecated)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class FieldTypeV2(YAMLRoot):
    """
    A field of a message of a specified dataType
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIX_SBE["FieldTypeV2"]
    class_class_curie: ClassVar[str] = "fix_sbe:FieldTypeV2"
    class_name: ClassVar[str] = "FieldTypeV2"
    class_model_uri: ClassVar[URIRef] = FIX_SBE.FieldTypeV2

    name: Union[str, SymbolicName] = None
    id: int = None
    type: Union[str, SymbolicName] = None
    value: Optional[str] = None
    offset: Optional[int] = None
    alignment: Optional[int] = None
    presence: Optional[Union[str, "Presence"]] = 'required'
    null_value: Optional[str] = None
    min_value: Optional[str] = None
    max_value: Optional[str] = None
    value_ref: Optional[Union[str, QualifiedName]] = None
    semantic_type: Optional[str] = None
    description: Optional[str] = None
    since_version: Optional[int] = 0
    deprecated: Optional[int] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.name):
            self.MissingRequiredField("name")
        if not isinstance(self.name, SymbolicName):
            self.name = SymbolicName(self.name)

        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, int):
            self.id = int(self.id)

        if self._is_empty(self.type):
            self.MissingRequiredField("type")
        if not isinstance(self.type, SymbolicName):
            self.type = SymbolicName(self.type)

        if self.value is not None and not isinstance(self.value, str):
            self.value = str(self.value)

        if self.offset is not None and not isinstance(self.offset, int):
            self.offset = int(self.offset)

        if self.alignment is not None and not isinstance(self.alignment, int):
            self.alignment = int(self.alignment)

        if self.presence is not None and not isinstance(self.presence, Presence):
            self.presence = Presence(self.presence)

        if self.null_value is not None and not isinstance(self.null_value, str):
            self.null_value = str(self.null_value)

        if self.min_value is not None and not isinstance(self.min_value, str):
            self.min_value = str(self.min_value)

        if self.max_value is not None and not isinstance(self.max_value, str):
            self.max_value = str(self.max_value)

        if self.value_ref is not None and not isinstance(self.value_ref, QualifiedName):
            self.value_ref = QualifiedName(self.value_ref)

        if self.semantic_type is not None and not isinstance(self.semantic_type, str):
            self.semantic_type = str(self.semantic_type)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.since_version is not None and not isinstance(self.since_version, int):
            self.since_version = int(self.since_version)

        if self.deprecated is not None and not isinstance(self.deprecated, int):
            self.deprecated = int(self.deprecated)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class MessageSchemaV2(YAMLRoot):
    """
    Root of XML document, holds all message templates and their elements
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIX_SBE["MessageSchemaV2"]
    class_class_curie: ClassVar[str] = "fix_sbe:MessageSchemaV2"
    class_name: ClassVar[str] = "MessageSchemaV2"
    class_model_uri: ClassVar[URIRef] = FIX_SBE.MessageSchemaV2

    types: Union[Union[dict, "TypesV2"], list[Union[dict, "TypesV2"]]] = None
    messages: Union[Union[dict, "MessagesV2"], list[Union[dict, "MessagesV2"]]] = None
    version: int = None
    package: Optional[str] = None
    id: Optional[int] = None
    semantic_version: Optional[str] = None
    description: Optional[str] = None
    byte_order: Optional[Union[str, "ByteOrder"]] = 'littleEndian'
    header_type: Optional[Union[str, SymbolicName]] = "messageHeader"

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.types):
            self.MissingRequiredField("types")
        if not isinstance(self.types, list):
            self.types = [self.types] if self.types is not None else []
        self.types = [v if isinstance(v, TypesV2) else TypesV2(**as_dict(v)) for v in self.types]

        if self._is_empty(self.messages):
            self.MissingRequiredField("messages")
        if not isinstance(self.messages, list):
            self.messages = [self.messages] if self.messages is not None else []
        self.messages = [v if isinstance(v, MessagesV2) else MessagesV2(**as_dict(v)) for v in self.messages]

        if self._is_empty(self.version):
            self.MissingRequiredField("version")
        if not isinstance(self.version, int):
            self.version = int(self.version)

        if self.package is not None and not isinstance(self.package, str):
            self.package = str(self.package)

        if self.id is not None and not isinstance(self.id, int):
            self.id = int(self.id)

        if self.semantic_version is not None and not isinstance(self.semantic_version, str):
            self.semantic_version = str(self.semantic_version)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.byte_order is not None and not isinstance(self.byte_order, ByteOrder):
            self.byte_order = ByteOrder(self.byte_order)

        if self.header_type is not None and not isinstance(self.header_type, SymbolicName):
            self.header_type = SymbolicName(self.header_type)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class MessagesV2(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIX_SBE["MessagesV2"]
    class_class_curie: ClassVar[str] = "fix_sbe:MessagesV2"
    class_name: ClassVar[str] = "MessagesV2"
    class_model_uri: ClassVar[URIRef] = FIX_SBE.MessagesV2

    message: Union[Union[dict, BlockTypeV2], list[Union[dict, BlockTypeV2]]] = None
    description: Optional[str] = None
    package: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.message):
            self.MissingRequiredField("message")
        self._normalize_inlined_as_list(slot_name="message", slot_type=BlockTypeV2, key_name="name", keyed=False)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.package is not None and not isinstance(self.package, str):
            self.package = str(self.package)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class TypesV2(YAMLRoot):
    """
    More than one set of types may be provided. Names must be unique across all encoding types. Encoding types may
    appear in any order.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIX_SBE["TypesV2"]
    class_class_curie: ClassVar[str] = "fix_sbe:TypesV2"
    class_name: ClassVar[str] = "TypesV2"
    class_model_uri: ClassVar[URIRef] = FIX_SBE.TypesV2

    type: Optional[Union[Union[dict, SimpleDataTypeV2], list[Union[dict, SimpleDataTypeV2]]]] = empty_list()
    composite: Optional[Union[Union[dict, CompositeDataTypeV2], list[Union[dict, CompositeDataTypeV2]]]] = empty_list()
    enum: Optional[Union[Union[dict, EnumTypeV2], list[Union[dict, EnumTypeV2]]]] = empty_list()
    set: Optional[Union[Union[dict, SetTypeV2], list[Union[dict, SetTypeV2]]]] = empty_list()
    description: Optional[str] = None
    package: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        self._normalize_inlined_as_list(slot_name="type", slot_type=SimpleDataTypeV2, key_name="name", keyed=False)

        self._normalize_inlined_as_list(slot_name="composite", slot_type=CompositeDataTypeV2, key_name="name", keyed=False)

        self._normalize_inlined_as_list(slot_name="enum", slot_type=EnumTypeV2, key_name="name", keyed=False)

        self._normalize_inlined_as_list(slot_name="set", slot_type=SetTypeV2, key_name="name", keyed=False)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.package is not None and not isinstance(self.package, str):
            self.package = str(self.package)

        super().__post_init__(**kwargs)


# Enumerations
class Presence(EnumDefinitionImpl):
    """
    Inline enumeration lifted from XSD attribute ``presence`` on ``presenceAttributes``.
    """
    required = PermissibleValue(
        text="required",
        description="The value must always be populated")
    optional = PermissibleValue(
        text="optional",
        description="Value may be set to nullValue for its data type")
    constant = PermissibleValue(
        text="constant",
        description="Value does not vary so it need not be serialized on the wire")

    _defn = EnumDefinition(
        name="Presence",
        description="Inline enumeration lifted from XSD attribute ``presence`` on ``presenceAttributes``.",
    )

class ByteOrder(EnumDefinitionImpl):
    """
    Inline enumeration lifted from XSD attribute ``byteOrder`` on ``messageSchema``.
    """
    bigEndian = PermissibleValue(text="bigEndian")
    littleEndian = PermissibleValue(text="littleEndian")

    _defn = EnumDefinition(
        name="ByteOrder",
        description="Inline enumeration lifted from XSD attribute ``byteOrder`` on ``messageSchema``.",
    )

class PrimitiveTypeV1(EnumDefinitionImpl):
    """
    Inline enumeration lifted from XSD attribute ``primitiveType`` on ``encodedDataType``.
    """
    char = PermissibleValue(text="char")
    int8 = PermissibleValue(text="int8")
    int16 = PermissibleValue(text="int16")
    int32 = PermissibleValue(text="int32")
    int64 = PermissibleValue(text="int64")
    uint8 = PermissibleValue(text="uint8")
    uint16 = PermissibleValue(text="uint16")
    uint32 = PermissibleValue(text="uint32")
    uint64 = PermissibleValue(text="uint64")
    float = PermissibleValue(text="float")
    double = PermissibleValue(text="double")

    _defn = EnumDefinition(
        name="PrimitiveTypeV1",
        description="Inline enumeration lifted from XSD attribute ``primitiveType`` on ``encodedDataType``.",
    )

class PrimitiveTypeV2(EnumDefinitionImpl):
    """
    Inline enumeration lifted from XSD attribute ``primitiveType`` on ``primitiveTypeAttributes``.
    """
    char = PermissibleValue(
        text="char",
        description="A value of a single-byte character set")
    int8 = PermissibleValue(text="int8")
    int16 = PermissibleValue(text="int16")
    int32 = PermissibleValue(text="int32")
    int64 = PermissibleValue(text="int64")
    uint8 = PermissibleValue(text="uint8")
    uint16 = PermissibleValue(text="uint16")
    uint32 = PermissibleValue(text="uint32")
    uint64 = PermissibleValue(text="uint64")
    float = PermissibleValue(text="float")
    double = PermissibleValue(text="double")

    _defn = EnumDefinition(
        name="PrimitiveTypeV2",
        description="Inline enumeration lifted from XSD attribute ``primitiveType`` on ``primitiveTypeAttributes``.",
    )

# Slots
class slots:
    pass

slots.semanticAttributes__semantic_type = Slot(uri=FIX_SBE.semantic_type, name="semanticAttributes__semantic_type", curie=FIX_SBE.curie('semantic_type'),
                   model_uri=FIX_SBE.semanticAttributes__semantic_type, domain=None, range=Optional[str])

slots.semanticAttributes__description = Slot(uri=FIX_SBE.description, name="semanticAttributes__description", curie=FIX_SBE.curie('description'),
                   model_uri=FIX_SBE.semanticAttributes__description, domain=None, range=Optional[str])

slots.versionAttributes__since_version = Slot(uri=FIX_SBE.since_version, name="versionAttributes__since_version", curie=FIX_SBE.curie('since_version'),
                   model_uri=FIX_SBE.versionAttributes__since_version, domain=None, range=Optional[int])

slots.versionAttributes__deprecated = Slot(uri=FIX_SBE.deprecated, name="versionAttributes__deprecated", curie=FIX_SBE.curie('deprecated'),
                   model_uri=FIX_SBE.versionAttributes__deprecated, domain=None, range=Optional[int])

slots.validValue__name = Slot(uri=FIX_SBE.name, name="validValue__name", curie=FIX_SBE.curie('name'),
                   model_uri=FIX_SBE.validValue__name, domain=None, range=Union[str, SymbolicName])

slots.validValue__description = Slot(uri=FIX_SBE.description, name="validValue__description", curie=FIX_SBE.curie('description'),
                   model_uri=FIX_SBE.validValue__description, domain=None, range=Optional[str])

slots.validValue__value = Slot(uri=FIX_SBE.value, name="validValue__value", curie=FIX_SBE.curie('value'),
                   model_uri=FIX_SBE.validValue__value, domain=None, range=Optional[str])

slots.choice__name = Slot(uri=FIX_SBE.name, name="choice__name", curie=FIX_SBE.curie('name'),
                   model_uri=FIX_SBE.choice__name, domain=None, range=Union[str, SymbolicName])

slots.choice__description = Slot(uri=FIX_SBE.description, name="choice__description", curie=FIX_SBE.curie('description'),
                   model_uri=FIX_SBE.choice__description, domain=None, range=Optional[str])

slots.choice__value = Slot(uri=FIX_SBE.value, name="choice__value", curie=FIX_SBE.curie('value'),
                   model_uri=FIX_SBE.choice__value, domain=None, range=Optional[str])

slots.alignmentAttributesV1__offset = Slot(uri=FIX_SBE.offset, name="alignmentAttributesV1__offset", curie=FIX_SBE.curie('offset'),
                   model_uri=FIX_SBE.alignmentAttributesV1__offset, domain=None, range=Optional[int])

slots.presenceAttributesV1__presence = Slot(uri=FIX_SBE.presence, name="presenceAttributesV1__presence", curie=FIX_SBE.curie('presence'),
                   model_uri=FIX_SBE.presenceAttributesV1__presence, domain=None, range=Optional[Union[str, "Presence"]])

slots.presenceAttributesV1__value_ref = Slot(uri=FIX_SBE.value_ref, name="presenceAttributesV1__value_ref", curie=FIX_SBE.curie('value_ref'),
                   model_uri=FIX_SBE.presenceAttributesV1__value_ref, domain=None, range=Optional[Union[str, QualifiedName]])

slots.blockTypeV1__field = Slot(uri=FIX_SBE.field, name="blockTypeV1__field", curie=FIX_SBE.curie('field'),
                   model_uri=FIX_SBE.blockTypeV1__field, domain=None, range=Optional[Union[Union[dict, FieldTypeV1], list[Union[dict, FieldTypeV1]]]])

slots.blockTypeV1__group = Slot(uri=FIX_SBE.group, name="blockTypeV1__group", curie=FIX_SBE.curie('group'),
                   model_uri=FIX_SBE.blockTypeV1__group, domain=None, range=Optional[Union[Union[dict, GroupTypeV1], list[Union[dict, GroupTypeV1]]]])

slots.blockTypeV1__data = Slot(uri=FIX_SBE.data, name="blockTypeV1__data", curie=FIX_SBE.curie('data'),
                   model_uri=FIX_SBE.blockTypeV1__data, domain=None, range=Optional[Union[Union[dict, FieldTypeV1], list[Union[dict, FieldTypeV1]]]])

slots.blockTypeV1__name = Slot(uri=FIX_SBE.name, name="blockTypeV1__name", curie=FIX_SBE.curie('name'),
                   model_uri=FIX_SBE.blockTypeV1__name, domain=None, range=Union[str, SymbolicName])

slots.blockTypeV1__id = Slot(uri=FIX_SBE.id, name="blockTypeV1__id", curie=FIX_SBE.curie('id'),
                   model_uri=FIX_SBE.blockTypeV1__id, domain=None, range=int)

slots.blockTypeV1__block_length = Slot(uri=FIX_SBE.block_length, name="blockTypeV1__block_length", curie=FIX_SBE.curie('block_length'),
                   model_uri=FIX_SBE.blockTypeV1__block_length, domain=None, range=Optional[int])

slots.groupTypeV1__dimension_type = Slot(uri=FIX_SBE.dimension_type, name="groupTypeV1__dimension_type", curie=FIX_SBE.curie('dimension_type'),
                   model_uri=FIX_SBE.groupTypeV1__dimension_type, domain=None, range=Optional[Union[str, SymbolicName]])

slots.encodedDataTypeV1__name = Slot(uri=FIX_SBE.name, name="encodedDataTypeV1__name", curie=FIX_SBE.curie('name'),
                   model_uri=FIX_SBE.encodedDataTypeV1__name, domain=None, range=Union[str, SymbolicName])

slots.encodedDataTypeV1__null_value = Slot(uri=FIX_SBE.null_value, name="encodedDataTypeV1__null_value", curie=FIX_SBE.curie('null_value'),
                   model_uri=FIX_SBE.encodedDataTypeV1__null_value, domain=None, range=Optional[str])

slots.encodedDataTypeV1__min_value = Slot(uri=FIX_SBE.min_value, name="encodedDataTypeV1__min_value", curie=FIX_SBE.curie('min_value'),
                   model_uri=FIX_SBE.encodedDataTypeV1__min_value, domain=None, range=Optional[str])

slots.encodedDataTypeV1__max_value = Slot(uri=FIX_SBE.max_value, name="encodedDataTypeV1__max_value", curie=FIX_SBE.curie('max_value'),
                   model_uri=FIX_SBE.encodedDataTypeV1__max_value, domain=None, range=Optional[str])

slots.encodedDataTypeV1__length = Slot(uri=FIX_SBE.length, name="encodedDataTypeV1__length", curie=FIX_SBE.curie('length'),
                   model_uri=FIX_SBE.encodedDataTypeV1__length, domain=None, range=Optional[int])

slots.encodedDataTypeV1__primitive_type = Slot(uri=FIX_SBE.primitive_type, name="encodedDataTypeV1__primitive_type", curie=FIX_SBE.curie('primitive_type'),
                   model_uri=FIX_SBE.encodedDataTypeV1__primitive_type, domain=None, range=Union[str, "PrimitiveTypeV1"])

slots.encodedDataTypeV1__character_encoding = Slot(uri=FIX_SBE.character_encoding, name="encodedDataTypeV1__character_encoding", curie=FIX_SBE.curie('character_encoding'),
                   model_uri=FIX_SBE.encodedDataTypeV1__character_encoding, domain=None, range=Optional[str])

slots.encodedDataTypeV1__value = Slot(uri=FIX_SBE.value, name="encodedDataTypeV1__value", curie=FIX_SBE.curie('value'),
                   model_uri=FIX_SBE.encodedDataTypeV1__value, domain=None, range=Optional[str])

slots.compositeDataTypeV1__type = Slot(uri=FIX_SBE.type, name="compositeDataTypeV1__type", curie=FIX_SBE.curie('type'),
                   model_uri=FIX_SBE.compositeDataTypeV1__type, domain=None, range=Optional[Union[Union[dict, EncodedDataTypeV1], list[Union[dict, EncodedDataTypeV1]]]])

slots.compositeDataTypeV1__enum = Slot(uri=FIX_SBE.enum, name="compositeDataTypeV1__enum", curie=FIX_SBE.curie('enum'),
                   model_uri=FIX_SBE.compositeDataTypeV1__enum, domain=None, range=Optional[Union[Union[dict, EnumTypeV1], list[Union[dict, EnumTypeV1]]]])

slots.compositeDataTypeV1__set = Slot(uri=FIX_SBE.set, name="compositeDataTypeV1__set", curie=FIX_SBE.curie('set'),
                   model_uri=FIX_SBE.compositeDataTypeV1__set, domain=None, range=Optional[Union[Union[dict, SetTypeV1], list[Union[dict, SetTypeV1]]]])

slots.compositeDataTypeV1__composite = Slot(uri=FIX_SBE.composite, name="compositeDataTypeV1__composite", curie=FIX_SBE.curie('composite'),
                   model_uri=FIX_SBE.compositeDataTypeV1__composite, domain=None, range=Optional[Union[Union[dict, CompositeDataTypeV1], list[Union[dict, CompositeDataTypeV1]]]])

slots.compositeDataTypeV1__ref = Slot(uri=FIX_SBE.ref, name="compositeDataTypeV1__ref", curie=FIX_SBE.curie('ref'),
                   model_uri=FIX_SBE.compositeDataTypeV1__ref, domain=None, range=Optional[Union[Union[dict, RefTypeV1], list[Union[dict, RefTypeV1]]]])

slots.compositeDataTypeV1__name = Slot(uri=FIX_SBE.name, name="compositeDataTypeV1__name", curie=FIX_SBE.curie('name'),
                   model_uri=FIX_SBE.compositeDataTypeV1__name, domain=None, range=Union[str, SymbolicName])

slots.compositeDataTypeV1__value = Slot(uri=FIX_SBE.value, name="compositeDataTypeV1__value", curie=FIX_SBE.curie('value'),
                   model_uri=FIX_SBE.compositeDataTypeV1__value, domain=None, range=Optional[str])

slots.enumTypeV1__valid_value = Slot(uri=FIX_SBE.valid_value, name="enumTypeV1__valid_value", curie=FIX_SBE.curie('valid_value'),
                   model_uri=FIX_SBE.enumTypeV1__valid_value, domain=None, range=Union[Union[dict, ValidValue], list[Union[dict, ValidValue]]])

slots.enumTypeV1__name = Slot(uri=FIX_SBE.name, name="enumTypeV1__name", curie=FIX_SBE.curie('name'),
                   model_uri=FIX_SBE.enumTypeV1__name, domain=None, range=Union[str, SymbolicName])

slots.enumTypeV1__encoding_type = Slot(uri=FIX_SBE.encoding_type, name="enumTypeV1__encoding_type", curie=FIX_SBE.curie('encoding_type'),
                   model_uri=FIX_SBE.enumTypeV1__encoding_type, domain=None, range=Union[str, SymbolicName])

slots.enumTypeV1__value = Slot(uri=FIX_SBE.value, name="enumTypeV1__value", curie=FIX_SBE.curie('value'),
                   model_uri=FIX_SBE.enumTypeV1__value, domain=None, range=Optional[str])

slots.refTypeV1__name = Slot(uri=FIX_SBE.name, name="refTypeV1__name", curie=FIX_SBE.curie('name'),
                   model_uri=FIX_SBE.refTypeV1__name, domain=None, range=Union[str, SymbolicName])

slots.refTypeV1__type = Slot(uri=FIX_SBE.type, name="refTypeV1__type", curie=FIX_SBE.curie('type'),
                   model_uri=FIX_SBE.refTypeV1__type, domain=None, range=Union[str, SymbolicName])

slots.refTypeV1__value = Slot(uri=FIX_SBE.value, name="refTypeV1__value", curie=FIX_SBE.curie('value'),
                   model_uri=FIX_SBE.refTypeV1__value, domain=None, range=Optional[str])

slots.setTypeV1__choice = Slot(uri=FIX_SBE.choice, name="setTypeV1__choice", curie=FIX_SBE.curie('choice'),
                   model_uri=FIX_SBE.setTypeV1__choice, domain=None, range=Union[Union[dict, Choice], list[Union[dict, Choice]]])

slots.setTypeV1__name = Slot(uri=FIX_SBE.name, name="setTypeV1__name", curie=FIX_SBE.curie('name'),
                   model_uri=FIX_SBE.setTypeV1__name, domain=None, range=Union[str, SymbolicName])

slots.setTypeV1__encoding_type = Slot(uri=FIX_SBE.encoding_type, name="setTypeV1__encoding_type", curie=FIX_SBE.curie('encoding_type'),
                   model_uri=FIX_SBE.setTypeV1__encoding_type, domain=None, range=Union[str, SymbolicName])

slots.setTypeV1__value = Slot(uri=FIX_SBE.value, name="setTypeV1__value", curie=FIX_SBE.curie('value'),
                   model_uri=FIX_SBE.setTypeV1__value, domain=None, range=Optional[str])

slots.fieldTypeV1__name = Slot(uri=FIX_SBE.name, name="fieldTypeV1__name", curie=FIX_SBE.curie('name'),
                   model_uri=FIX_SBE.fieldTypeV1__name, domain=None, range=Union[str, SymbolicName])

slots.fieldTypeV1__id = Slot(uri=FIX_SBE.id, name="fieldTypeV1__id", curie=FIX_SBE.curie('id'),
                   model_uri=FIX_SBE.fieldTypeV1__id, domain=None, range=int)

slots.fieldTypeV1__type = Slot(uri=FIX_SBE.type, name="fieldTypeV1__type", curie=FIX_SBE.curie('type'),
                   model_uri=FIX_SBE.fieldTypeV1__type, domain=None, range=Union[str, SymbolicName])

slots.fieldTypeV1__epoch = Slot(uri=FIX_SBE.epoch, name="fieldTypeV1__epoch", curie=FIX_SBE.curie('epoch'),
                   model_uri=FIX_SBE.fieldTypeV1__epoch, domain=None, range=Optional[str])

slots.fieldTypeV1__time_unit = Slot(uri=FIX_SBE.time_unit, name="fieldTypeV1__time_unit", curie=FIX_SBE.curie('time_unit'),
                   model_uri=FIX_SBE.fieldTypeV1__time_unit, domain=None, range=Optional[str])

slots.messageSchemaV1__types = Slot(uri=FIX_SBE.types, name="messageSchemaV1__types", curie=FIX_SBE.curie('types'),
                   model_uri=FIX_SBE.messageSchemaV1__types, domain=None, range=Union[str, list[str]])

slots.messageSchemaV1__message = Slot(uri=FIX_SBE.message, name="messageSchemaV1__message", curie=FIX_SBE.curie('message'),
                   model_uri=FIX_SBE.messageSchemaV1__message, domain=None, range=Union[Union[dict, MessageV1], list[Union[dict, MessageV1]]])

slots.messageSchemaV1__package = Slot(uri=FIX_SBE.package, name="messageSchemaV1__package", curie=FIX_SBE.curie('package'),
                   model_uri=FIX_SBE.messageSchemaV1__package, domain=None, range=Optional[str])

slots.messageSchemaV1__id = Slot(uri=FIX_SBE.id, name="messageSchemaV1__id", curie=FIX_SBE.curie('id'),
                   model_uri=FIX_SBE.messageSchemaV1__id, domain=None, range=Optional[int])

slots.messageSchemaV1__version = Slot(uri=FIX_SBE.version, name="messageSchemaV1__version", curie=FIX_SBE.curie('version'),
                   model_uri=FIX_SBE.messageSchemaV1__version, domain=None, range=int)

slots.messageSchemaV1__semantic_version = Slot(uri=FIX_SBE.semantic_version, name="messageSchemaV1__semantic_version", curie=FIX_SBE.curie('semantic_version'),
                   model_uri=FIX_SBE.messageSchemaV1__semantic_version, domain=None, range=Optional[str])

slots.messageSchemaV1__description = Slot(uri=FIX_SBE.description, name="messageSchemaV1__description", curie=FIX_SBE.curie('description'),
                   model_uri=FIX_SBE.messageSchemaV1__description, domain=None, range=Optional[str])

slots.messageSchemaV1__byte_order = Slot(uri=FIX_SBE.byte_order, name="messageSchemaV1__byte_order", curie=FIX_SBE.curie('byte_order'),
                   model_uri=FIX_SBE.messageSchemaV1__byte_order, domain=None, range=Optional[Union[str, "ByteOrder"]])

slots.messageSchemaV1__header_type = Slot(uri=FIX_SBE.header_type, name="messageSchemaV1__header_type", curie=FIX_SBE.curie('header_type'),
                   model_uri=FIX_SBE.messageSchemaV1__header_type, domain=None, range=Optional[Union[str, SymbolicName]])

slots.alignmentAttributesV2__alignment = Slot(uri=FIX_SBE.alignment, name="alignmentAttributesV2__alignment", curie=FIX_SBE.curie('alignment'),
                   model_uri=FIX_SBE.alignmentAttributesV2__alignment, domain=None, range=Optional[int])

slots.offsetAttributesV2__offset = Slot(uri=FIX_SBE.offset, name="offsetAttributesV2__offset", curie=FIX_SBE.curie('offset'),
                   model_uri=FIX_SBE.offsetAttributesV2__offset, domain=None, range=Optional[int])

slots.offsetAttributesV2__alignment = Slot(uri=FIX_SBE.alignment, name="offsetAttributesV2__alignment", curie=FIX_SBE.curie('alignment'),
                   model_uri=FIX_SBE.offsetAttributesV2__alignment, domain=None, range=Optional[int])

slots.presenceAttributesV2__presence = Slot(uri=FIX_SBE.presence, name="presenceAttributesV2__presence", curie=FIX_SBE.curie('presence'),
                   model_uri=FIX_SBE.presenceAttributesV2__presence, domain=None, range=Optional[Union[str, "Presence"]])

slots.presenceAttributesV2__null_value = Slot(uri=FIX_SBE.null_value, name="presenceAttributesV2__null_value", curie=FIX_SBE.curie('null_value'),
                   model_uri=FIX_SBE.presenceAttributesV2__null_value, domain=None, range=Optional[str])

slots.presenceAttributesV2__min_value = Slot(uri=FIX_SBE.min_value, name="presenceAttributesV2__min_value", curie=FIX_SBE.curie('min_value'),
                   model_uri=FIX_SBE.presenceAttributesV2__min_value, domain=None, range=Optional[str])

slots.presenceAttributesV2__max_value = Slot(uri=FIX_SBE.max_value, name="presenceAttributesV2__max_value", curie=FIX_SBE.curie('max_value'),
                   model_uri=FIX_SBE.presenceAttributesV2__max_value, domain=None, range=Optional[str])

slots.presenceAttributesV2__value_ref = Slot(uri=FIX_SBE.value_ref, name="presenceAttributesV2__value_ref", curie=FIX_SBE.curie('value_ref'),
                   model_uri=FIX_SBE.presenceAttributesV2__value_ref, domain=None, range=Optional[Union[str, QualifiedName]])

slots.primitiveTypeAttributesV2__primitive_type = Slot(uri=FIX_SBE.primitive_type, name="primitiveTypeAttributesV2__primitive_type", curie=FIX_SBE.curie('primitive_type'),
                   model_uri=FIX_SBE.primitiveTypeAttributesV2__primitive_type, domain=None, range=Union[str, "PrimitiveTypeV2"])

slots.primitiveTypeAttributesV2__length = Slot(uri=FIX_SBE.length, name="primitiveTypeAttributesV2__length", curie=FIX_SBE.curie('length'),
                   model_uri=FIX_SBE.primitiveTypeAttributesV2__length, domain=None, range=Optional[int])

slots.primitiveTypeAttributesV2__character_encoding = Slot(uri=FIX_SBE.character_encoding, name="primitiveTypeAttributesV2__character_encoding", curie=FIX_SBE.curie('character_encoding'),
                   model_uri=FIX_SBE.primitiveTypeAttributesV2__character_encoding, domain=None, range=Optional[str])

slots.blockTypeV2__field = Slot(uri=FIX_SBE.field, name="blockTypeV2__field", curie=FIX_SBE.curie('field'),
                   model_uri=FIX_SBE.blockTypeV2__field, domain=None, range=Optional[Union[Union[dict, FieldTypeV2], list[Union[dict, FieldTypeV2]]]])

slots.blockTypeV2__group = Slot(uri=FIX_SBE.group, name="blockTypeV2__group", curie=FIX_SBE.curie('group'),
                   model_uri=FIX_SBE.blockTypeV2__group, domain=None, range=Optional[Union[Union[dict, GroupTypeV2], list[Union[dict, GroupTypeV2]]]])

slots.blockTypeV2__data = Slot(uri=FIX_SBE.data, name="blockTypeV2__data", curie=FIX_SBE.curie('data'),
                   model_uri=FIX_SBE.blockTypeV2__data, domain=None, range=Optional[Union[Union[dict, FieldTypeV2], list[Union[dict, FieldTypeV2]]]])

slots.blockTypeV2__name = Slot(uri=FIX_SBE.name, name="blockTypeV2__name", curie=FIX_SBE.curie('name'),
                   model_uri=FIX_SBE.blockTypeV2__name, domain=None, range=Union[str, SymbolicName])

slots.blockTypeV2__id = Slot(uri=FIX_SBE.id, name="blockTypeV2__id", curie=FIX_SBE.curie('id'),
                   model_uri=FIX_SBE.blockTypeV2__id, domain=None, range=int)

slots.blockTypeV2__block_length = Slot(uri=FIX_SBE.block_length, name="blockTypeV2__block_length", curie=FIX_SBE.curie('block_length'),
                   model_uri=FIX_SBE.blockTypeV2__block_length, domain=None, range=Optional[int])

slots.groupTypeV2__dimension_type = Slot(uri=FIX_SBE.dimension_type, name="groupTypeV2__dimension_type", curie=FIX_SBE.curie('dimension_type'),
                   model_uri=FIX_SBE.groupTypeV2__dimension_type, domain=None, range=Optional[Union[str, SymbolicName]])

slots.simpleDataTypeV2__name = Slot(uri=FIX_SBE.name, name="simpleDataTypeV2__name", curie=FIX_SBE.curie('name'),
                   model_uri=FIX_SBE.simpleDataTypeV2__name, domain=None, range=Union[str, SymbolicName])

slots.simpleDataTypeV2__description = Slot(uri=FIX_SBE.description, name="simpleDataTypeV2__description", curie=FIX_SBE.curie('description'),
                   model_uri=FIX_SBE.simpleDataTypeV2__description, domain=None, range=Optional[str])

slots.simpleDataTypeV2__value = Slot(uri=FIX_SBE.value, name="simpleDataTypeV2__value", curie=FIX_SBE.curie('value'),
                   model_uri=FIX_SBE.simpleDataTypeV2__value, domain=None, range=Optional[str])

slots.memberDataTypeV2__name = Slot(uri=FIX_SBE.name, name="memberDataTypeV2__name", curie=FIX_SBE.curie('name'),
                   model_uri=FIX_SBE.memberDataTypeV2__name, domain=None, range=Union[str, SymbolicName])

slots.memberDataTypeV2__description = Slot(uri=FIX_SBE.description, name="memberDataTypeV2__description", curie=FIX_SBE.curie('description'),
                   model_uri=FIX_SBE.memberDataTypeV2__description, domain=None, range=Optional[str])

slots.memberDataTypeV2__value = Slot(uri=FIX_SBE.value, name="memberDataTypeV2__value", curie=FIX_SBE.curie('value'),
                   model_uri=FIX_SBE.memberDataTypeV2__value, domain=None, range=Optional[str])

slots.compositeDataTypeV2__type = Slot(uri=FIX_SBE.type, name="compositeDataTypeV2__type", curie=FIX_SBE.curie('type'),
                   model_uri=FIX_SBE.compositeDataTypeV2__type, domain=None, range=Optional[Union[Union[dict, MemberDataTypeV2], list[Union[dict, MemberDataTypeV2]]]])

slots.compositeDataTypeV2__enum = Slot(uri=FIX_SBE.enum, name="compositeDataTypeV2__enum", curie=FIX_SBE.curie('enum'),
                   model_uri=FIX_SBE.compositeDataTypeV2__enum, domain=None, range=Optional[Union[Union[dict, EnumTypeV2], list[Union[dict, EnumTypeV2]]]])

slots.compositeDataTypeV2__set = Slot(uri=FIX_SBE.set, name="compositeDataTypeV2__set", curie=FIX_SBE.curie('set'),
                   model_uri=FIX_SBE.compositeDataTypeV2__set, domain=None, range=Optional[Union[Union[dict, SetTypeV2], list[Union[dict, SetTypeV2]]]])

slots.compositeDataTypeV2__composite = Slot(uri=FIX_SBE.composite, name="compositeDataTypeV2__composite", curie=FIX_SBE.curie('composite'),
                   model_uri=FIX_SBE.compositeDataTypeV2__composite, domain=None, range=Optional[Union[Union[dict, CompositeDataTypeV2], list[Union[dict, CompositeDataTypeV2]]]])

slots.compositeDataTypeV2__ref = Slot(uri=FIX_SBE.ref, name="compositeDataTypeV2__ref", curie=FIX_SBE.curie('ref'),
                   model_uri=FIX_SBE.compositeDataTypeV2__ref, domain=None, range=Optional[Union[Union[dict, RefTypeV2], list[Union[dict, RefTypeV2]]]])

slots.compositeDataTypeV2__name = Slot(uri=FIX_SBE.name, name="compositeDataTypeV2__name", curie=FIX_SBE.curie('name'),
                   model_uri=FIX_SBE.compositeDataTypeV2__name, domain=None, range=Union[str, SymbolicName])

slots.compositeDataTypeV2__description = Slot(uri=FIX_SBE.description, name="compositeDataTypeV2__description", curie=FIX_SBE.curie('description'),
                   model_uri=FIX_SBE.compositeDataTypeV2__description, domain=None, range=Optional[str])

slots.compositeDataTypeV2__value = Slot(uri=FIX_SBE.value, name="compositeDataTypeV2__value", curie=FIX_SBE.curie('value'),
                   model_uri=FIX_SBE.compositeDataTypeV2__value, domain=None, range=Optional[str])

slots.enumTypeV2__valid_value = Slot(uri=FIX_SBE.valid_value, name="enumTypeV2__valid_value", curie=FIX_SBE.curie('valid_value'),
                   model_uri=FIX_SBE.enumTypeV2__valid_value, domain=None, range=Union[Union[dict, ValidValue], list[Union[dict, ValidValue]]])

slots.enumTypeV2__name = Slot(uri=FIX_SBE.name, name="enumTypeV2__name", curie=FIX_SBE.curie('name'),
                   model_uri=FIX_SBE.enumTypeV2__name, domain=None, range=Union[str, SymbolicName])

slots.enumTypeV2__encoding_type = Slot(uri=FIX_SBE.encoding_type, name="enumTypeV2__encoding_type", curie=FIX_SBE.curie('encoding_type'),
                   model_uri=FIX_SBE.enumTypeV2__encoding_type, domain=None, range=Union[str, SymbolicName])

slots.enumTypeV2__description = Slot(uri=FIX_SBE.description, name="enumTypeV2__description", curie=FIX_SBE.curie('description'),
                   model_uri=FIX_SBE.enumTypeV2__description, domain=None, range=Optional[str])

slots.enumTypeV2__value = Slot(uri=FIX_SBE.value, name="enumTypeV2__value", curie=FIX_SBE.curie('value'),
                   model_uri=FIX_SBE.enumTypeV2__value, domain=None, range=Optional[str])

slots.refTypeV2__name = Slot(uri=FIX_SBE.name, name="refTypeV2__name", curie=FIX_SBE.curie('name'),
                   model_uri=FIX_SBE.refTypeV2__name, domain=None, range=Union[str, SymbolicName])

slots.refTypeV2__type = Slot(uri=FIX_SBE.type, name="refTypeV2__type", curie=FIX_SBE.curie('type'),
                   model_uri=FIX_SBE.refTypeV2__type, domain=None, range=Union[str, SymbolicName])

slots.refTypeV2__description = Slot(uri=FIX_SBE.description, name="refTypeV2__description", curie=FIX_SBE.curie('description'),
                   model_uri=FIX_SBE.refTypeV2__description, domain=None, range=Optional[str])

slots.refTypeV2__value = Slot(uri=FIX_SBE.value, name="refTypeV2__value", curie=FIX_SBE.curie('value'),
                   model_uri=FIX_SBE.refTypeV2__value, domain=None, range=Optional[str])

slots.setTypeV2__choice = Slot(uri=FIX_SBE.choice, name="setTypeV2__choice", curie=FIX_SBE.curie('choice'),
                   model_uri=FIX_SBE.setTypeV2__choice, domain=None, range=Union[Union[dict, Choice], list[Union[dict, Choice]]])

slots.setTypeV2__name = Slot(uri=FIX_SBE.name, name="setTypeV2__name", curie=FIX_SBE.curie('name'),
                   model_uri=FIX_SBE.setTypeV2__name, domain=None, range=Union[str, SymbolicName])

slots.setTypeV2__encoding_type = Slot(uri=FIX_SBE.encoding_type, name="setTypeV2__encoding_type", curie=FIX_SBE.curie('encoding_type'),
                   model_uri=FIX_SBE.setTypeV2__encoding_type, domain=None, range=Union[str, SymbolicName])

slots.setTypeV2__description = Slot(uri=FIX_SBE.description, name="setTypeV2__description", curie=FIX_SBE.curie('description'),
                   model_uri=FIX_SBE.setTypeV2__description, domain=None, range=Optional[str])

slots.setTypeV2__value = Slot(uri=FIX_SBE.value, name="setTypeV2__value", curie=FIX_SBE.curie('value'),
                   model_uri=FIX_SBE.setTypeV2__value, domain=None, range=Optional[str])

slots.fieldTypeV2__name = Slot(uri=FIX_SBE.name, name="fieldTypeV2__name", curie=FIX_SBE.curie('name'),
                   model_uri=FIX_SBE.fieldTypeV2__name, domain=None, range=Union[str, SymbolicName])

slots.fieldTypeV2__id = Slot(uri=FIX_SBE.id, name="fieldTypeV2__id", curie=FIX_SBE.curie('id'),
                   model_uri=FIX_SBE.fieldTypeV2__id, domain=None, range=int)

slots.fieldTypeV2__type = Slot(uri=FIX_SBE.type, name="fieldTypeV2__type", curie=FIX_SBE.curie('type'),
                   model_uri=FIX_SBE.fieldTypeV2__type, domain=None, range=Union[str, SymbolicName])

slots.fieldTypeV2__value = Slot(uri=FIX_SBE.value, name="fieldTypeV2__value", curie=FIX_SBE.curie('value'),
                   model_uri=FIX_SBE.fieldTypeV2__value, domain=None, range=Optional[str])

slots.messageSchemaV2__types = Slot(uri=FIX_SBE.types, name="messageSchemaV2__types", curie=FIX_SBE.curie('types'),
                   model_uri=FIX_SBE.messageSchemaV2__types, domain=None, range=Union[Union[dict, TypesV2], list[Union[dict, TypesV2]]])

slots.messageSchemaV2__messages = Slot(uri=FIX_SBE.messages, name="messageSchemaV2__messages", curie=FIX_SBE.curie('messages'),
                   model_uri=FIX_SBE.messageSchemaV2__messages, domain=None, range=Union[Union[dict, MessagesV2], list[Union[dict, MessagesV2]]])

slots.messageSchemaV2__package = Slot(uri=FIX_SBE.package, name="messageSchemaV2__package", curie=FIX_SBE.curie('package'),
                   model_uri=FIX_SBE.messageSchemaV2__package, domain=None, range=Optional[str])

slots.messageSchemaV2__id = Slot(uri=FIX_SBE.id, name="messageSchemaV2__id", curie=FIX_SBE.curie('id'),
                   model_uri=FIX_SBE.messageSchemaV2__id, domain=None, range=Optional[int])

slots.messageSchemaV2__version = Slot(uri=FIX_SBE.version, name="messageSchemaV2__version", curie=FIX_SBE.curie('version'),
                   model_uri=FIX_SBE.messageSchemaV2__version, domain=None, range=int)

slots.messageSchemaV2__semantic_version = Slot(uri=FIX_SBE.semantic_version, name="messageSchemaV2__semantic_version", curie=FIX_SBE.curie('semantic_version'),
                   model_uri=FIX_SBE.messageSchemaV2__semantic_version, domain=None, range=Optional[str])

slots.messageSchemaV2__description = Slot(uri=FIX_SBE.description, name="messageSchemaV2__description", curie=FIX_SBE.curie('description'),
                   model_uri=FIX_SBE.messageSchemaV2__description, domain=None, range=Optional[str])

slots.messageSchemaV2__byte_order = Slot(uri=FIX_SBE.byte_order, name="messageSchemaV2__byte_order", curie=FIX_SBE.curie('byte_order'),
                   model_uri=FIX_SBE.messageSchemaV2__byte_order, domain=None, range=Optional[Union[str, "ByteOrder"]])

slots.messageSchemaV2__header_type = Slot(uri=FIX_SBE.header_type, name="messageSchemaV2__header_type", curie=FIX_SBE.curie('header_type'),
                   model_uri=FIX_SBE.messageSchemaV2__header_type, domain=None, range=Optional[Union[str, SymbolicName]])

slots.messagesV2__message = Slot(uri=FIX_SBE.message, name="messagesV2__message", curie=FIX_SBE.curie('message'),
                   model_uri=FIX_SBE.messagesV2__message, domain=None, range=Union[Union[dict, BlockTypeV2], list[Union[dict, BlockTypeV2]]])

slots.messagesV2__description = Slot(uri=FIX_SBE.description, name="messagesV2__description", curie=FIX_SBE.curie('description'),
                   model_uri=FIX_SBE.messagesV2__description, domain=None, range=Optional[str])

slots.messagesV2__package = Slot(uri=FIX_SBE.package, name="messagesV2__package", curie=FIX_SBE.curie('package'),
                   model_uri=FIX_SBE.messagesV2__package, domain=None, range=Optional[str])

slots.typesV2__type = Slot(uri=FIX_SBE.type, name="typesV2__type", curie=FIX_SBE.curie('type'),
                   model_uri=FIX_SBE.typesV2__type, domain=None, range=Optional[Union[Union[dict, SimpleDataTypeV2], list[Union[dict, SimpleDataTypeV2]]]])

slots.typesV2__composite = Slot(uri=FIX_SBE.composite, name="typesV2__composite", curie=FIX_SBE.curie('composite'),
                   model_uri=FIX_SBE.typesV2__composite, domain=None, range=Optional[Union[Union[dict, CompositeDataTypeV2], list[Union[dict, CompositeDataTypeV2]]]])

slots.typesV2__enum = Slot(uri=FIX_SBE.enum, name="typesV2__enum", curie=FIX_SBE.curie('enum'),
                   model_uri=FIX_SBE.typesV2__enum, domain=None, range=Optional[Union[Union[dict, EnumTypeV2], list[Union[dict, EnumTypeV2]]]])

slots.typesV2__set = Slot(uri=FIX_SBE.set, name="typesV2__set", curie=FIX_SBE.curie('set'),
                   model_uri=FIX_SBE.typesV2__set, domain=None, range=Optional[Union[Union[dict, SetTypeV2], list[Union[dict, SetTypeV2]]]])

slots.typesV2__description = Slot(uri=FIX_SBE.description, name="typesV2__description", curie=FIX_SBE.curie('description'),
                   model_uri=FIX_SBE.typesV2__description, domain=None, range=Optional[str])

slots.typesV2__package = Slot(uri=FIX_SBE.package, name="typesV2__package", curie=FIX_SBE.curie('package'),
                   model_uri=FIX_SBE.typesV2__package, domain=None, range=Optional[str])
