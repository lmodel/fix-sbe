# Auto generated from fix_sbe.yaml by pythongen.py version: 0.0.1
# Schema: fix_sbe
#
# id: https://w3id.org/lmodel/fix-sbe
# description: A LinkML model of FIX Simple Binary Encoding, a standard from the FIX Trading Community for encoding messages in binary. It describes SBE message schemas: encodings, message templates, fields, groups and variable-length data. The two editions differ on the wire and in their XML, so each has a module of its own.
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

from linkml_runtime.linkml_model.types import Integer, String, Uri
from linkml_runtime.utils.metamodelcore import URI

metamodel_version = "1.12.0"
version = "1.0 and 2.0-rc3"

# Namespaces
FIX_ORCHESTRA = CurieNamespace('fix_orchestra', 'https://w3id.org/lmodel/fix-orchestra/')
FIX_SBE = CurieNamespace('fix_sbe', 'https://w3id.org/lmodel/fix-sbe/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
SCHEMA = CurieNamespace('schema', 'http://schema.org/')
XSD = CurieNamespace('xsd', 'http://www.w3.org/2001/XMLSchema#')
DEFAULT_ = FIX_SBE


# Types
class SbeSymbolicName(String):
    """ A name of one to 64 letters, digits and underscores that starts with a letter or underscore. """
    type_class_uri = XSD["string"]
    type_class_curie = "xsd:string"
    type_name = "SbeSymbolicName"
    type_model_uri = FIX_SBE.SbeSymbolicName


class SbeQualifiedName(String):
    """ An enumeration's name and one of its valid values' names, joined by a dot. """
    type_class_uri = XSD["string"]
    type_class_curie = "xsd:string"
    type_name = "SbeQualifiedName"
    type_model_uri = FIX_SBE.SbeQualifiedName


class SbeToken(String):
    """ Text with no line break, tab or doubled space, and no space at either end. """
    type_class_uri = XSD["token"]
    type_class_curie = "xsd:token"
    type_name = "SbeToken"
    type_model_uri = FIX_SBE.SbeToken


# Class references



@dataclass(repr=False)
class SbeVersionedMixin(YAMLRoot):
    """
    The two attributes that record when an element entered a schema and when it should leave.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIX_SBE["SbeVersionedMixin"]
    class_class_curie: ClassVar[str] = "fix_sbe:SbeVersionedMixin"
    class_name: ClassVar[str] = "SbeVersionedMixin"
    class_model_uri: ClassVar[URIRef] = FIX_SBE.SbeVersionedMixin

    since_version: Optional[int] = 0
    deprecated_since: Optional[int] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.since_version is not None and not isinstance(self.since_version, int):
            self.since_version = int(self.since_version)

        if self.deprecated_since is not None and not isinstance(self.deprecated_since, int):
            self.deprecated_since = int(self.deprecated_since)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class SbeValidValue(YAMLRoot):
    """
    One of the values an enumeration allows.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIX_SBE["SbeValidValue"]
    class_class_curie: ClassVar[str] = "fix_sbe:SbeValidValue"
    class_name: ClassVar[str] = "SbeValidValue"
    class_model_uri: ClassVar[URIRef] = FIX_SBE.SbeValidValue

    symbolic_name: Union[str, SbeSymbolicName] = None
    valid_value: Union[str, SbeToken] = None
    description: Optional[str] = None
    since_version: Optional[int] = 0
    deprecated_since: Optional[int] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.symbolic_name):
            self.MissingRequiredField("symbolic_name")
        if not isinstance(self.symbolic_name, SbeSymbolicName):
            self.symbolic_name = SbeSymbolicName(self.symbolic_name)

        if self._is_empty(self.valid_value):
            self.MissingRequiredField("valid_value")
        if not isinstance(self.valid_value, SbeToken):
            self.valid_value = SbeToken(self.valid_value)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.since_version is not None and not isinstance(self.since_version, int):
            self.since_version = int(self.since_version)

        if self.deprecated_since is not None and not isinstance(self.deprecated_since, int):
            self.deprecated_since = int(self.deprecated_since)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class SbeChoice(YAMLRoot):
    """
    One of the alternatives of a set, which is one bit of its encoding.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIX_SBE["SbeChoice"]
    class_class_curie: ClassVar[str] = "fix_sbe:SbeChoice"
    class_name: ClassVar[str] = "SbeChoice"
    class_model_uri: ClassVar[URIRef] = FIX_SBE.SbeChoice

    symbolic_name: Union[str, SbeSymbolicName] = None
    bit_position: int = None
    description: Optional[str] = None
    since_version: Optional[int] = 0
    deprecated_since: Optional[int] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.symbolic_name):
            self.MissingRequiredField("symbolic_name")
        if not isinstance(self.symbolic_name, SbeSymbolicName):
            self.symbolic_name = SbeSymbolicName(self.symbolic_name)

        if self._is_empty(self.bit_position):
            self.MissingRequiredField("bit_position")
        if not isinstance(self.bit_position, int):
            self.bit_position = int(self.bit_position)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.since_version is not None and not isinstance(self.since_version, int):
            self.since_version = int(self.since_version)

        if self.deprecated_since is not None and not isinstance(self.deprecated_since, int):
            self.deprecated_since = int(self.deprecated_since)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class SbeMessageSchemaV1(YAMLRoot):
    """
    One SBE 1.0 message schema, with its encodings and message templates.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIX_SBE["SbeMessageSchemaV1"]
    class_class_curie: ClassVar[str] = "fix_sbe:SbeMessageSchemaV1"
    class_name: ClassVar[str] = "SbeMessageSchemaV1"
    class_model_uri: ClassVar[URIRef] = FIX_SBE.SbeMessageSchemaV1

    schema_version: int = None
    encoding_sets: Union[Union[dict, "SbeEncodingSetV1"], list[Union[dict, "SbeEncodingSetV1"]]] = None
    messages: Union[Union[dict, "SbeMessageV1"], list[Union[dict, "SbeMessageV1"]]] = None
    schema_package: Optional[str] = None
    sbe_id: Optional[int] = None
    semantic_version: Optional[str] = None
    description: Optional[str] = None
    byte_order: Optional[Union[str, "SbeByteOrder"]] = 'littleEndian'
    header_type: Optional[Union[str, SbeSymbolicName]] = "messageHeader"

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.schema_version):
            self.MissingRequiredField("schema_version")
        if not isinstance(self.schema_version, int):
            self.schema_version = int(self.schema_version)

        if self._is_empty(self.encoding_sets):
            self.MissingRequiredField("encoding_sets")
        if not isinstance(self.encoding_sets, list):
            self.encoding_sets = [self.encoding_sets] if self.encoding_sets is not None else []
        self.encoding_sets = [v if isinstance(v, SbeEncodingSetV1) else SbeEncodingSetV1(**as_dict(v)) for v in self.encoding_sets]

        if self._is_empty(self.messages):
            self.MissingRequiredField("messages")
        self._normalize_inlined_as_list(slot_name="messages", slot_type=SbeMessageV1, key_name="symbolic_name", keyed=False)

        if self.schema_package is not None and not isinstance(self.schema_package, str):
            self.schema_package = str(self.schema_package)

        if self.sbe_id is not None and not isinstance(self.sbe_id, int):
            self.sbe_id = int(self.sbe_id)

        if self.semantic_version is not None and not isinstance(self.semantic_version, str):
            self.semantic_version = str(self.semantic_version)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.byte_order is not None and not isinstance(self.byte_order, SbeByteOrder):
            self.byte_order = SbeByteOrder(self.byte_order)

        if self.header_type is not None and not isinstance(self.header_type, SbeSymbolicName):
            self.header_type = SbeSymbolicName(self.header_type)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class SbeEncodingSetV1(YAMLRoot):
    """
    A set of encodings, listed in any order, whose names are unique across the whole schema.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIX_SBE["SbeEncodingSetV1"]
    class_class_curie: ClassVar[str] = "fix_sbe:SbeEncodingSetV1"
    class_name: ClassVar[str] = "SbeEncodingSetV1"
    class_model_uri: ClassVar[URIRef] = FIX_SBE.SbeEncodingSetV1

    encodings: Union[Union[dict, "SbeEncodingV1"], list[Union[dict, "SbeEncodingV1"]]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.encodings):
            self.MissingRequiredField("encodings")
        self._normalize_inlined_as_list(slot_name="encodings", slot_type=SbeEncodingV1, key_name="encoding_kind", keyed=False)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class SbeMemberV1(YAMLRoot):
    """
    Anything a composite may hold in the order it is sent.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIX_SBE["SbeMemberV1"]
    class_class_curie: ClassVar[str] = "fix_sbe:SbeMemberV1"
    class_name: ClassVar[str] = "SbeMemberV1"
    class_model_uri: ClassVar[URIRef] = FIX_SBE.SbeMemberV1

    encoding_kind: str = None
    symbolic_name: Union[str, SbeSymbolicName] = None
    offset: Optional[int] = None
    since_version: Optional[int] = 0
    deprecated_since: Optional[int] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.encoding_kind):
            self.MissingRequiredField("encoding_kind")
        self.encoding_kind = str(self.class_name)

        if self._is_empty(self.symbolic_name):
            self.MissingRequiredField("symbolic_name")
        if not isinstance(self.symbolic_name, SbeSymbolicName):
            self.symbolic_name = SbeSymbolicName(self.symbolic_name)

        if self.offset is not None and not isinstance(self.offset, int):
            self.offset = int(self.offset)

        if self.since_version is not None and not isinstance(self.since_version, int):
            self.since_version = int(self.since_version)

        if self.deprecated_since is not None and not isinstance(self.deprecated_since, int):
            self.deprecated_since = int(self.deprecated_since)

        super().__post_init__(**kwargs)


    def __new__(cls, *args, **kwargs):

        type_designator = "encoding_kind"
        if not type_designator in kwargs:
            return super().__new__(cls,*args,**kwargs)
        else:
            type_designator_value = kwargs[type_designator]
            target_cls = cls._class_for("class_name", type_designator_value)


            if target_cls is None:
                raise ValueError(f"Wrong type designator value: class {cls.__name__} "
                                 f"has no subclass with ['class_name']='{kwargs[type_designator]}'")
            return super().__new__(target_cls,*args,**kwargs)



@dataclass(repr=False)
class SbeRefV1(SbeMemberV1):
    """
    A composite's member that reuses an encoding defined elsewhere in the schema.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIX_SBE["SbeRefV1"]
    class_class_curie: ClassVar[str] = "fix_sbe:SbeRefV1"
    class_name: ClassVar[str] = "SbeRefV1"
    class_model_uri: ClassVar[URIRef] = FIX_SBE.SbeRefV1

    encoding_kind: str = None
    symbolic_name: Union[str, SbeSymbolicName] = None
    encoding_name: Union[str, SbeSymbolicName] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.encoding_name):
            self.MissingRequiredField("encoding_name")
        if not isinstance(self.encoding_name, SbeSymbolicName):
            self.encoding_name = SbeSymbolicName(self.encoding_name)

        super().__post_init__(**kwargs)
        if self._is_empty(self.encoding_kind):
            self.MissingRequiredField("encoding_kind")
        self.encoding_kind = str(self.class_name)


@dataclass(repr=False)
class SbeEncodingV1(SbeMemberV1):
    """
    An encoding of SBE 1.0, which says how a value is laid out on the wire.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIX_SBE["SbeEncodingV1"]
    class_class_curie: ClassVar[str] = "fix_sbe:SbeEncodingV1"
    class_name: ClassVar[str] = "SbeEncodingV1"
    class_model_uri: ClassVar[URIRef] = FIX_SBE.SbeEncodingV1

    encoding_kind: str = None
    symbolic_name: Union[str, SbeSymbolicName] = None
    semantic_type: Optional[Union[str, SbeToken]] = None
    description: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.semantic_type is not None and not isinstance(self.semantic_type, SbeToken):
            self.semantic_type = SbeToken(self.semantic_type)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        super().__post_init__(**kwargs)
        if self._is_empty(self.encoding_kind):
            self.MissingRequiredField("encoding_kind")
        self.encoding_kind = str(self.class_name)


@dataclass(repr=False)
class SbeSimpleTypeV1(SbeEncodingV1):
    """
    An encoding backed by one primitive value, or several in an array.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIX_SBE["SbeSimpleTypeV1"]
    class_class_curie: ClassVar[str] = "fix_sbe:SbeSimpleTypeV1"
    class_name: ClassVar[str] = "SbeSimpleTypeV1"
    class_model_uri: ClassVar[URIRef] = FIX_SBE.SbeSimpleTypeV1

    encoding_kind: str = None
    symbolic_name: Union[str, SbeSymbolicName] = None
    primitive_type: Union[str, "SbePrimitiveType"] = None
    element_value: Optional[Union[str, SbeToken]] = None
    array_length: Optional[int] = 1
    character_encoding: Optional[str] = None
    null_value: Optional[str] = None
    min_value: Optional[str] = None
    max_value: Optional[str] = None
    presence: Optional[Union[str, "SbePresence"]] = 'required'
    value_ref: Optional[Union[str, SbeQualifiedName]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.primitive_type):
            self.MissingRequiredField("primitive_type")
        if not isinstance(self.primitive_type, SbePrimitiveType):
            self.primitive_type = SbePrimitiveType(self.primitive_type)

        if self.element_value is not None and not isinstance(self.element_value, SbeToken):
            self.element_value = SbeToken(self.element_value)

        if self.array_length is not None and not isinstance(self.array_length, int):
            self.array_length = int(self.array_length)

        if self.character_encoding is not None and not isinstance(self.character_encoding, str):
            self.character_encoding = str(self.character_encoding)

        if self.null_value is not None and not isinstance(self.null_value, str):
            self.null_value = str(self.null_value)

        if self.min_value is not None and not isinstance(self.min_value, str):
            self.min_value = str(self.min_value)

        if self.max_value is not None and not isinstance(self.max_value, str):
            self.max_value = str(self.max_value)

        if self.presence is not None and not isinstance(self.presence, SbePresence):
            self.presence = SbePresence(self.presence)

        if self.value_ref is not None and not isinstance(self.value_ref, SbeQualifiedName):
            self.value_ref = SbeQualifiedName(self.value_ref)

        super().__post_init__(**kwargs)
        if self._is_empty(self.encoding_kind):
            self.MissingRequiredField("encoding_kind")
        self.encoding_kind = str(self.class_name)


@dataclass(repr=False)
class SbeCompositeV1(SbeEncodingV1):
    """
    An encoding built from members sent one after another, such as a decimal's mantissa and exponent.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIX_SBE["SbeCompositeV1"]
    class_class_curie: ClassVar[str] = "fix_sbe:SbeCompositeV1"
    class_name: ClassVar[str] = "SbeCompositeV1"
    class_model_uri: ClassVar[URIRef] = FIX_SBE.SbeCompositeV1

    encoding_kind: str = None
    symbolic_name: Union[str, SbeSymbolicName] = None
    composite_members: Union[Union[dict, SbeMemberV1], list[Union[dict, SbeMemberV1]]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.composite_members):
            self.MissingRequiredField("composite_members")
        self._normalize_inlined_as_list(slot_name="composite_members", slot_type=SbeMemberV1, key_name="encoding_kind", keyed=False)

        super().__post_init__(**kwargs)
        if self._is_empty(self.encoding_kind):
            self.MissingRequiredField("encoding_kind")
        self.encoding_kind = str(self.class_name)


@dataclass(repr=False)
class SbeEnumV1(SbeEncodingV1):
    """
    An encoding whose value is one of a listed set of valid values.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIX_SBE["SbeEnumV1"]
    class_class_curie: ClassVar[str] = "fix_sbe:SbeEnumV1"
    class_name: ClassVar[str] = "SbeEnumV1"
    class_model_uri: ClassVar[URIRef] = FIX_SBE.SbeEnumV1

    encoding_kind: str = None
    symbolic_name: Union[str, SbeSymbolicName] = None
    encoding_type: Union[str, SbeSymbolicName] = None
    valid_values: Union[Union[dict, SbeValidValue], list[Union[dict, SbeValidValue]]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.encoding_type):
            self.MissingRequiredField("encoding_type")
        if not isinstance(self.encoding_type, SbeSymbolicName):
            self.encoding_type = SbeSymbolicName(self.encoding_type)

        if self._is_empty(self.valid_values):
            self.MissingRequiredField("valid_values")
        self._normalize_inlined_as_list(slot_name="valid_values", slot_type=SbeValidValue, key_name="symbolic_name", keyed=False)

        super().__post_init__(**kwargs)
        if self._is_empty(self.encoding_kind):
            self.MissingRequiredField("encoding_kind")
        self.encoding_kind = str(self.class_name)


@dataclass(repr=False)
class SbeSetV1(SbeEncodingV1):
    """
    An encoding whose value is any combination of up to 64 choices, sent as a bitset.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIX_SBE["SbeSetV1"]
    class_class_curie: ClassVar[str] = "fix_sbe:SbeSetV1"
    class_name: ClassVar[str] = "SbeSetV1"
    class_model_uri: ClassVar[URIRef] = FIX_SBE.SbeSetV1

    encoding_kind: str = None
    symbolic_name: Union[str, SbeSymbolicName] = None
    encoding_type: Union[str, SbeSymbolicName] = None
    choices: Union[Union[dict, SbeChoice], list[Union[dict, SbeChoice]]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.encoding_type):
            self.MissingRequiredField("encoding_type")
        if not isinstance(self.encoding_type, SbeSymbolicName):
            self.encoding_type = SbeSymbolicName(self.encoding_type)

        if self._is_empty(self.choices):
            self.MissingRequiredField("choices")
        self._normalize_inlined_as_list(slot_name="choices", slot_type=SbeChoice, key_name="symbolic_name", keyed=False)

        super().__post_init__(**kwargs)
        if self._is_empty(self.encoding_kind):
            self.MissingRequiredField("encoding_kind")
        self.encoding_kind = str(self.class_name)


@dataclass(repr=False)
class SbeBlockV1(YAMLRoot):
    """
    The body shared by a message and a group entry, which holds its fixed-length fields first, then groups, then
    variable-length data.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIX_SBE["SbeBlockV1"]
    class_class_curie: ClassVar[str] = "fix_sbe:SbeBlockV1"
    class_name: ClassVar[str] = "SbeBlockV1"
    class_model_uri: ClassVar[URIRef] = FIX_SBE.SbeBlockV1

    symbolic_name: Union[str, SbeSymbolicName] = None
    sbe_id: int = None
    block_length: Optional[int] = None
    semantic_type: Optional[Union[str, SbeToken]] = None
    description: Optional[str] = None
    block_fields: Optional[Union[Union[dict, "SbeFieldV1"], list[Union[dict, "SbeFieldV1"]]]] = empty_list()
    repeating_groups: Optional[Union[Union[dict, "SbeGroupV1"], list[Union[dict, "SbeGroupV1"]]]] = empty_list()
    var_data_fields: Optional[Union[Union[dict, "SbeFieldV1"], list[Union[dict, "SbeFieldV1"]]]] = empty_list()
    since_version: Optional[int] = 0
    deprecated_since: Optional[int] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.symbolic_name):
            self.MissingRequiredField("symbolic_name")
        if not isinstance(self.symbolic_name, SbeSymbolicName):
            self.symbolic_name = SbeSymbolicName(self.symbolic_name)

        if self._is_empty(self.sbe_id):
            self.MissingRequiredField("sbe_id")
        if not isinstance(self.sbe_id, int):
            self.sbe_id = int(self.sbe_id)

        if self.block_length is not None and not isinstance(self.block_length, int):
            self.block_length = int(self.block_length)

        if self.semantic_type is not None and not isinstance(self.semantic_type, SbeToken):
            self.semantic_type = SbeToken(self.semantic_type)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        self._normalize_inlined_as_list(slot_name="block_fields", slot_type=SbeFieldV1, key_name="symbolic_name", keyed=False)

        self._normalize_inlined_as_list(slot_name="repeating_groups", slot_type=SbeGroupV1, key_name="symbolic_name", keyed=False)

        self._normalize_inlined_as_list(slot_name="var_data_fields", slot_type=SbeFieldV1, key_name="symbolic_name", keyed=False)

        if self.since_version is not None and not isinstance(self.since_version, int):
            self.since_version = int(self.since_version)

        if self.deprecated_since is not None and not isinstance(self.deprecated_since, int):
            self.deprecated_since = int(self.deprecated_since)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class SbeMessageV1(SbeBlockV1):
    """
    A message template, whose number and block length are sent in each message's header.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIX_SBE["SbeMessageV1"]
    class_class_curie: ClassVar[str] = "fix_sbe:SbeMessageV1"
    class_name: ClassVar[str] = "SbeMessageV1"
    class_model_uri: ClassVar[URIRef] = FIX_SBE.SbeMessageV1

    symbolic_name: Union[str, SbeSymbolicName] = None
    sbe_id: int = None
    semantic_type: Optional[Union[str, SbeToken]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.sbe_id):
            self.MissingRequiredField("sbe_id")
        if not isinstance(self.sbe_id, int):
            self.sbe_id = int(self.sbe_id)

        if self.semantic_type is not None and not isinstance(self.semantic_type, SbeToken):
            self.semantic_type = SbeToken(self.semantic_type)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class SbeGroupV1(SbeBlockV1):
    """
    A repeating group, whose entries each hold the same fields, and which cannot be without a field.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIX_SBE["SbeGroupV1"]
    class_class_curie: ClassVar[str] = "fix_sbe:SbeGroupV1"
    class_name: ClassVar[str] = "SbeGroupV1"
    class_model_uri: ClassVar[URIRef] = FIX_SBE.SbeGroupV1

    symbolic_name: Union[str, SbeSymbolicName] = None
    sbe_id: int = None
    block_fields: Union[Union[dict, "SbeFieldV1"], list[Union[dict, "SbeFieldV1"]]] = None
    dimension_type: Optional[Union[str, SbeSymbolicName]] = "groupSizeEncoding"

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.block_fields):
            self.MissingRequiredField("block_fields")
        self._normalize_inlined_as_list(slot_name="block_fields", slot_type=SbeFieldV1, key_name="symbolic_name", keyed=False)

        if self.dimension_type is not None and not isinstance(self.dimension_type, SbeSymbolicName):
            self.dimension_type = SbeSymbolicName(self.dimension_type)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class SbeFieldV1(YAMLRoot):
    """
    A message's or group entry's field, which uses an encoding at a place in its block.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIX_SBE["SbeFieldV1"]
    class_class_curie: ClassVar[str] = "fix_sbe:SbeFieldV1"
    class_name: ClassVar[str] = "SbeFieldV1"
    class_model_uri: ClassVar[URIRef] = FIX_SBE.SbeFieldV1

    symbolic_name: Union[str, SbeSymbolicName] = None
    sbe_id: int = None
    encoding_name: Union[str, SbeSymbolicName] = None
    offset: Optional[int] = None
    presence: Optional[Union[str, "SbePresence"]] = 'required'
    value_ref: Optional[Union[str, SbeQualifiedName]] = None
    semantic_type: Optional[Union[str, SbeToken]] = None
    description: Optional[str] = None
    time_epoch: Optional[str] = "unix"
    time_unit: Optional[str] = "nanosecond"
    since_version: Optional[int] = 0
    deprecated_since: Optional[int] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.symbolic_name):
            self.MissingRequiredField("symbolic_name")
        if not isinstance(self.symbolic_name, SbeSymbolicName):
            self.symbolic_name = SbeSymbolicName(self.symbolic_name)

        if self._is_empty(self.sbe_id):
            self.MissingRequiredField("sbe_id")
        if not isinstance(self.sbe_id, int):
            self.sbe_id = int(self.sbe_id)

        if self._is_empty(self.encoding_name):
            self.MissingRequiredField("encoding_name")
        if not isinstance(self.encoding_name, SbeSymbolicName):
            self.encoding_name = SbeSymbolicName(self.encoding_name)

        if self.offset is not None and not isinstance(self.offset, int):
            self.offset = int(self.offset)

        if self.presence is not None and not isinstance(self.presence, SbePresence):
            self.presence = SbePresence(self.presence)

        if self.value_ref is not None and not isinstance(self.value_ref, SbeQualifiedName):
            self.value_ref = SbeQualifiedName(self.value_ref)

        if self.semantic_type is not None and not isinstance(self.semantic_type, SbeToken):
            self.semantic_type = SbeToken(self.semantic_type)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.time_epoch is not None and not isinstance(self.time_epoch, str):
            self.time_epoch = str(self.time_epoch)

        if self.time_unit is not None and not isinstance(self.time_unit, str):
            self.time_unit = str(self.time_unit)

        if self.since_version is not None and not isinstance(self.since_version, int):
            self.since_version = int(self.since_version)

        if self.deprecated_since is not None and not isinstance(self.deprecated_since, int):
            self.deprecated_since = int(self.deprecated_since)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class SbeMessageSchemaV2(YAMLRoot):
    """
    One SBE 2.0 message schema, with its encodings and message templates.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIX_SBE["SbeMessageSchemaV2"]
    class_class_curie: ClassVar[str] = "fix_sbe:SbeMessageSchemaV2"
    class_name: ClassVar[str] = "SbeMessageSchemaV2"
    class_model_uri: ClassVar[URIRef] = FIX_SBE.SbeMessageSchemaV2

    schema_version: int = None
    encoding_sets: Union[Union[dict, "SbeEncodingSetV2"], list[Union[dict, "SbeEncodingSetV2"]]] = None
    message_sets: Union[Union[dict, "SbeMessageSetV2"], list[Union[dict, "SbeMessageSetV2"]]] = None
    schema_package: Optional[str] = None
    sbe_id: Optional[int] = None
    semantic_version: Optional[str] = None
    description: Optional[str] = None
    byte_order: Optional[Union[str, "SbeByteOrder"]] = 'littleEndian'
    header_type: Optional[Union[str, SbeSymbolicName]] = "messageHeader"

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.schema_version):
            self.MissingRequiredField("schema_version")
        if not isinstance(self.schema_version, int):
            self.schema_version = int(self.schema_version)

        if self._is_empty(self.encoding_sets):
            self.MissingRequiredField("encoding_sets")
        if not isinstance(self.encoding_sets, list):
            self.encoding_sets = [self.encoding_sets] if self.encoding_sets is not None else []
        self.encoding_sets = [v if isinstance(v, SbeEncodingSetV2) else SbeEncodingSetV2(**as_dict(v)) for v in self.encoding_sets]

        if self._is_empty(self.message_sets):
            self.MissingRequiredField("message_sets")
        if not isinstance(self.message_sets, list):
            self.message_sets = [self.message_sets] if self.message_sets is not None else []
        self.message_sets = [v if isinstance(v, SbeMessageSetV2) else SbeMessageSetV2(**as_dict(v)) for v in self.message_sets]

        if self.schema_package is not None and not isinstance(self.schema_package, str):
            self.schema_package = str(self.schema_package)

        if self.sbe_id is not None and not isinstance(self.sbe_id, int):
            self.sbe_id = int(self.sbe_id)

        if self.semantic_version is not None and not isinstance(self.semantic_version, str):
            self.semantic_version = str(self.semantic_version)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.byte_order is not None and not isinstance(self.byte_order, SbeByteOrder):
            self.byte_order = SbeByteOrder(self.byte_order)

        if self.header_type is not None and not isinstance(self.header_type, SbeSymbolicName):
            self.header_type = SbeSymbolicName(self.header_type)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class SbeEncodingSetV2(YAMLRoot):
    """
    A set of encodings, in any order, that may have its own package and may come from another file.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIX_SBE["SbeEncodingSetV2"]
    class_class_curie: ClassVar[str] = "fix_sbe:SbeEncodingSetV2"
    class_name: ClassVar[str] = "SbeEncodingSetV2"
    class_model_uri: ClassVar[URIRef] = FIX_SBE.SbeEncodingSetV2

    encodings: Union[Union[dict, "SbeElementV2"], list[Union[dict, "SbeElementV2"]]] = None
    description: Optional[str] = None
    schema_package: Optional[str] = None
    xml_base: Optional[Union[str, URI]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.encodings):
            self.MissingRequiredField("encodings")
        self._normalize_inlined_as_list(slot_name="encodings", slot_type=SbeElementV2, key_name="encoding_kind", keyed=False)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.schema_package is not None and not isinstance(self.schema_package, str):
            self.schema_package = str(self.schema_package)

        if self.xml_base is not None and not isinstance(self.xml_base, URI):
            self.xml_base = URI(self.xml_base)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class SbeMessageSetV2(YAMLRoot):
    """
    Message templates held together, which may have their own package and may come from another file.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIX_SBE["SbeMessageSetV2"]
    class_class_curie: ClassVar[str] = "fix_sbe:SbeMessageSetV2"
    class_name: ClassVar[str] = "SbeMessageSetV2"
    class_model_uri: ClassVar[URIRef] = FIX_SBE.SbeMessageSetV2

    messages: Union[Union[dict, "SbeMessageV2"], list[Union[dict, "SbeMessageV2"]]] = None
    description: Optional[str] = None
    schema_package: Optional[str] = None
    xml_base: Optional[Union[str, URI]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.messages):
            self.MissingRequiredField("messages")
        self._normalize_inlined_as_list(slot_name="messages", slot_type=SbeMessageV2, key_name="symbolic_name", keyed=False)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.schema_package is not None and not isinstance(self.schema_package, str):
            self.schema_package = str(self.schema_package)

        if self.xml_base is not None and not isinstance(self.xml_base, URI):
            self.xml_base = URI(self.xml_base)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class SbeElementV2(YAMLRoot):
    """
    Anything that sets of encodings or composites hold, and the name and text they all have.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIX_SBE["SbeElementV2"]
    class_class_curie: ClassVar[str] = "fix_sbe:SbeElementV2"
    class_name: ClassVar[str] = "SbeElementV2"
    class_model_uri: ClassVar[URIRef] = FIX_SBE.SbeElementV2

    encoding_kind: str = None
    symbolic_name: Union[str, SbeSymbolicName] = None
    description: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.encoding_kind):
            self.MissingRequiredField("encoding_kind")
        self.encoding_kind = str(self.class_name)

        if self._is_empty(self.symbolic_name):
            self.MissingRequiredField("symbolic_name")
        if not isinstance(self.symbolic_name, SbeSymbolicName):
            self.symbolic_name = SbeSymbolicName(self.symbolic_name)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        super().__post_init__(**kwargs)


    def __new__(cls, *args, **kwargs):

        type_designator = "encoding_kind"
        if not type_designator in kwargs:
            return super().__new__(cls,*args,**kwargs)
        else:
            type_designator_value = kwargs[type_designator]
            target_cls = cls._class_for("class_name", type_designator_value)


            if target_cls is None:
                raise ValueError(f"Wrong type designator value: class {cls.__name__} "
                                 f"has no subclass with ['class_name']='{kwargs[type_designator]}'")
            return super().__new__(target_cls,*args,**kwargs)



@dataclass(repr=False)
class SbeMemberV2(SbeElementV2):
    """
    Anything a composite may hold in the order it is sent.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIX_SBE["SbeMemberV2"]
    class_class_curie: ClassVar[str] = "fix_sbe:SbeMemberV2"
    class_name: ClassVar[str] = "SbeMemberV2"
    class_model_uri: ClassVar[URIRef] = FIX_SBE.SbeMemberV2

    encoding_kind: str = None
    symbolic_name: Union[str, SbeSymbolicName] = None
    offset: Optional[int] = None
    alignment: Optional[int] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.offset is not None and not isinstance(self.offset, int):
            self.offset = int(self.offset)

        if self.alignment is not None and not isinstance(self.alignment, int):
            self.alignment = int(self.alignment)

        super().__post_init__(**kwargs)
        if self._is_empty(self.encoding_kind):
            self.MissingRequiredField("encoding_kind")
        self.encoding_kind = str(self.class_name)


@dataclass(repr=False)
class SbeSimpleTypeV2(SbeElementV2):
    """
    A simple encoding that stands alone in a set, backed by one primitive value, or several in an array.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIX_SBE["SbeSimpleTypeV2"]
    class_class_curie: ClassVar[str] = "fix_sbe:SbeSimpleTypeV2"
    class_name: ClassVar[str] = "SbeSimpleTypeV2"
    class_model_uri: ClassVar[URIRef] = FIX_SBE.SbeSimpleTypeV2

    encoding_kind: str = None
    symbolic_name: Union[str, SbeSymbolicName] = None
    primitive_type: Union[str, "SbePrimitiveType"] = None
    element_value: Optional[Union[str, SbeToken]] = None
    array_length: Optional[int] = 1
    character_encoding: Optional[str] = None
    since_version: Optional[int] = 0
    deprecated_since: Optional[int] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.primitive_type):
            self.MissingRequiredField("primitive_type")
        if not isinstance(self.primitive_type, SbePrimitiveType):
            self.primitive_type = SbePrimitiveType(self.primitive_type)

        if self.element_value is not None and not isinstance(self.element_value, SbeToken):
            self.element_value = SbeToken(self.element_value)

        if self.array_length is not None and not isinstance(self.array_length, int):
            self.array_length = int(self.array_length)

        if self.character_encoding is not None and not isinstance(self.character_encoding, str):
            self.character_encoding = str(self.character_encoding)

        if self.since_version is not None and not isinstance(self.since_version, int):
            self.since_version = int(self.since_version)

        if self.deprecated_since is not None and not isinstance(self.deprecated_since, int):
            self.deprecated_since = int(self.deprecated_since)

        super().__post_init__(**kwargs)
        if self._is_empty(self.encoding_kind):
            self.MissingRequiredField("encoding_kind")
        self.encoding_kind = str(self.class_name)


@dataclass(repr=False)
class SbeMemberTypeV2(SbeMemberV2):
    """
    A simple encoding inside a composite, which may say it is optional or constant.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIX_SBE["SbeMemberTypeV2"]
    class_class_curie: ClassVar[str] = "fix_sbe:SbeMemberTypeV2"
    class_name: ClassVar[str] = "SbeMemberTypeV2"
    class_model_uri: ClassVar[URIRef] = FIX_SBE.SbeMemberTypeV2

    encoding_kind: str = None
    symbolic_name: Union[str, SbeSymbolicName] = None
    primitive_type: Union[str, "SbePrimitiveType"] = None
    element_value: Optional[Union[str, SbeToken]] = None
    array_length: Optional[int] = 1
    character_encoding: Optional[str] = None
    presence: Optional[Union[str, "SbePresence"]] = 'required'
    null_value: Optional[str] = None
    min_value: Optional[str] = None
    max_value: Optional[str] = None
    value_ref: Optional[Union[str, SbeQualifiedName]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.primitive_type):
            self.MissingRequiredField("primitive_type")
        if not isinstance(self.primitive_type, SbePrimitiveType):
            self.primitive_type = SbePrimitiveType(self.primitive_type)

        if self.element_value is not None and not isinstance(self.element_value, SbeToken):
            self.element_value = SbeToken(self.element_value)

        if self.array_length is not None and not isinstance(self.array_length, int):
            self.array_length = int(self.array_length)

        if self.character_encoding is not None and not isinstance(self.character_encoding, str):
            self.character_encoding = str(self.character_encoding)

        if self.presence is not None and not isinstance(self.presence, SbePresence):
            self.presence = SbePresence(self.presence)

        if self.null_value is not None and not isinstance(self.null_value, str):
            self.null_value = str(self.null_value)

        if self.min_value is not None and not isinstance(self.min_value, str):
            self.min_value = str(self.min_value)

        if self.max_value is not None and not isinstance(self.max_value, str):
            self.max_value = str(self.max_value)

        if self.value_ref is not None and not isinstance(self.value_ref, SbeQualifiedName):
            self.value_ref = SbeQualifiedName(self.value_ref)

        super().__post_init__(**kwargs)
        if self._is_empty(self.encoding_kind):
            self.MissingRequiredField("encoding_kind")
        self.encoding_kind = str(self.class_name)


@dataclass(repr=False)
class SbeRefV2(SbeMemberV2):
    """
    A composite's member that reuses an encoding defined elsewhere in the schema.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIX_SBE["SbeRefV2"]
    class_class_curie: ClassVar[str] = "fix_sbe:SbeRefV2"
    class_name: ClassVar[str] = "SbeRefV2"
    class_model_uri: ClassVar[URIRef] = FIX_SBE.SbeRefV2

    encoding_kind: str = None
    symbolic_name: Union[str, SbeSymbolicName] = None
    encoding_name: Union[str, SbeSymbolicName] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.encoding_name):
            self.MissingRequiredField("encoding_name")
        if not isinstance(self.encoding_name, SbeSymbolicName):
            self.encoding_name = SbeSymbolicName(self.encoding_name)

        super().__post_init__(**kwargs)
        if self._is_empty(self.encoding_kind):
            self.MissingRequiredField("encoding_kind")
        self.encoding_kind = str(self.class_name)


@dataclass(repr=False)
class SbeCompositeV2(SbeMemberV2):
    """
    An encoding built from members sent one after another, such as a decimal's mantissa and exponent.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIX_SBE["SbeCompositeV2"]
    class_class_curie: ClassVar[str] = "fix_sbe:SbeCompositeV2"
    class_name: ClassVar[str] = "SbeCompositeV2"
    class_model_uri: ClassVar[URIRef] = FIX_SBE.SbeCompositeV2

    encoding_kind: str = None
    symbolic_name: Union[str, SbeSymbolicName] = None
    composite_members: Union[Union[dict, SbeMemberV2], list[Union[dict, SbeMemberV2]]] = None
    since_version: Optional[int] = 0
    deprecated_since: Optional[int] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.composite_members):
            self.MissingRequiredField("composite_members")
        self._normalize_inlined_as_list(slot_name="composite_members", slot_type=SbeMemberV2, key_name="encoding_kind", keyed=False)

        if self.since_version is not None and not isinstance(self.since_version, int):
            self.since_version = int(self.since_version)

        if self.deprecated_since is not None and not isinstance(self.deprecated_since, int):
            self.deprecated_since = int(self.deprecated_since)

        super().__post_init__(**kwargs)
        if self._is_empty(self.encoding_kind):
            self.MissingRequiredField("encoding_kind")
        self.encoding_kind = str(self.class_name)


@dataclass(repr=False)
class SbeEnumV2(SbeMemberV2):
    """
    An encoding whose value is one of a listed set of valid values.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIX_SBE["SbeEnumV2"]
    class_class_curie: ClassVar[str] = "fix_sbe:SbeEnumV2"
    class_name: ClassVar[str] = "SbeEnumV2"
    class_model_uri: ClassVar[URIRef] = FIX_SBE.SbeEnumV2

    encoding_kind: str = None
    symbolic_name: Union[str, SbeSymbolicName] = None
    encoding_type: Union[str, SbeSymbolicName] = None
    valid_values: Union[Union[dict, SbeValidValue], list[Union[dict, SbeValidValue]]] = None
    since_version: Optional[int] = 0
    deprecated_since: Optional[int] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.encoding_type):
            self.MissingRequiredField("encoding_type")
        if not isinstance(self.encoding_type, SbeSymbolicName):
            self.encoding_type = SbeSymbolicName(self.encoding_type)

        if self._is_empty(self.valid_values):
            self.MissingRequiredField("valid_values")
        self._normalize_inlined_as_list(slot_name="valid_values", slot_type=SbeValidValue, key_name="symbolic_name", keyed=False)

        if self.since_version is not None and not isinstance(self.since_version, int):
            self.since_version = int(self.since_version)

        if self.deprecated_since is not None and not isinstance(self.deprecated_since, int):
            self.deprecated_since = int(self.deprecated_since)

        super().__post_init__(**kwargs)
        if self._is_empty(self.encoding_kind):
            self.MissingRequiredField("encoding_kind")
        self.encoding_kind = str(self.class_name)


@dataclass(repr=False)
class SbeSetV2(SbeMemberV2):
    """
    An encoding whose value is any combination of up to 64 choices, sent as a bitset.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIX_SBE["SbeSetV2"]
    class_class_curie: ClassVar[str] = "fix_sbe:SbeSetV2"
    class_name: ClassVar[str] = "SbeSetV2"
    class_model_uri: ClassVar[URIRef] = FIX_SBE.SbeSetV2

    encoding_kind: str = None
    symbolic_name: Union[str, SbeSymbolicName] = None
    encoding_type: Union[str, SbeSymbolicName] = None
    choices: Union[Union[dict, SbeChoice], list[Union[dict, SbeChoice]]] = None
    since_version: Optional[int] = 0
    deprecated_since: Optional[int] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.encoding_type):
            self.MissingRequiredField("encoding_type")
        if not isinstance(self.encoding_type, SbeSymbolicName):
            self.encoding_type = SbeSymbolicName(self.encoding_type)

        if self._is_empty(self.choices):
            self.MissingRequiredField("choices")
        self._normalize_inlined_as_list(slot_name="choices", slot_type=SbeChoice, key_name="symbolic_name", keyed=False)

        if self.since_version is not None and not isinstance(self.since_version, int):
            self.since_version = int(self.since_version)

        if self.deprecated_since is not None and not isinstance(self.deprecated_since, int):
            self.deprecated_since = int(self.deprecated_since)

        super().__post_init__(**kwargs)
        if self._is_empty(self.encoding_kind):
            self.MissingRequiredField("encoding_kind")
        self.encoding_kind = str(self.class_name)


@dataclass(repr=False)
class SbeBlockV2(YAMLRoot):
    """
    The body shared by a message and a group entry, which holds its fixed-length fields first, then groups, then
    variable-length data.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIX_SBE["SbeBlockV2"]
    class_class_curie: ClassVar[str] = "fix_sbe:SbeBlockV2"
    class_name: ClassVar[str] = "SbeBlockV2"
    class_model_uri: ClassVar[URIRef] = FIX_SBE.SbeBlockV2

    symbolic_name: Union[str, SbeSymbolicName] = None
    sbe_id: int = None
    block_length: Optional[int] = None
    alignment: Optional[int] = None
    semantic_type: Optional[Union[str, SbeToken]] = None
    description: Optional[str] = None
    block_fields: Optional[Union[Union[dict, "SbeFieldV2"], list[Union[dict, "SbeFieldV2"]]]] = empty_list()
    repeating_groups: Optional[Union[Union[dict, "SbeGroupV2"], list[Union[dict, "SbeGroupV2"]]]] = empty_list()
    var_data_fields: Optional[Union[Union[dict, "SbeFieldV2"], list[Union[dict, "SbeFieldV2"]]]] = empty_list()
    since_version: Optional[int] = 0
    deprecated_since: Optional[int] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.symbolic_name):
            self.MissingRequiredField("symbolic_name")
        if not isinstance(self.symbolic_name, SbeSymbolicName):
            self.symbolic_name = SbeSymbolicName(self.symbolic_name)

        if self._is_empty(self.sbe_id):
            self.MissingRequiredField("sbe_id")
        if not isinstance(self.sbe_id, int):
            self.sbe_id = int(self.sbe_id)

        if self.block_length is not None and not isinstance(self.block_length, int):
            self.block_length = int(self.block_length)

        if self.alignment is not None and not isinstance(self.alignment, int):
            self.alignment = int(self.alignment)

        if self.semantic_type is not None and not isinstance(self.semantic_type, SbeToken):
            self.semantic_type = SbeToken(self.semantic_type)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        self._normalize_inlined_as_list(slot_name="block_fields", slot_type=SbeFieldV2, key_name="symbolic_name", keyed=False)

        self._normalize_inlined_as_list(slot_name="repeating_groups", slot_type=SbeGroupV2, key_name="symbolic_name", keyed=False)

        self._normalize_inlined_as_list(slot_name="var_data_fields", slot_type=SbeFieldV2, key_name="symbolic_name", keyed=False)

        if self.since_version is not None and not isinstance(self.since_version, int):
            self.since_version = int(self.since_version)

        if self.deprecated_since is not None and not isinstance(self.deprecated_since, int):
            self.deprecated_since = int(self.deprecated_since)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class SbeMessageV2(SbeBlockV2):
    """
    A message template, whose number and block length are sent in each message's header.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIX_SBE["SbeMessageV2"]
    class_class_curie: ClassVar[str] = "fix_sbe:SbeMessageV2"
    class_name: ClassVar[str] = "SbeMessageV2"
    class_model_uri: ClassVar[URIRef] = FIX_SBE.SbeMessageV2

    symbolic_name: Union[str, SbeSymbolicName] = None
    sbe_id: int = None
    semantic_type: Optional[Union[str, SbeToken]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.sbe_id):
            self.MissingRequiredField("sbe_id")
        if not isinstance(self.sbe_id, int):
            self.sbe_id = int(self.sbe_id)

        if self.semantic_type is not None and not isinstance(self.semantic_type, SbeToken):
            self.semantic_type = SbeToken(self.semantic_type)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class SbeGroupV2(SbeBlockV2):
    """
    A repeating group, whose entries each hold the same fields, and which cannot be without a field.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIX_SBE["SbeGroupV2"]
    class_class_curie: ClassVar[str] = "fix_sbe:SbeGroupV2"
    class_name: ClassVar[str] = "SbeGroupV2"
    class_model_uri: ClassVar[URIRef] = FIX_SBE.SbeGroupV2

    symbolic_name: Union[str, SbeSymbolicName] = None
    sbe_id: int = None
    block_fields: Union[Union[dict, "SbeFieldV2"], list[Union[dict, "SbeFieldV2"]]] = None
    dimension_type: Optional[Union[str, SbeSymbolicName]] = "groupSizeEncoding"

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.block_fields):
            self.MissingRequiredField("block_fields")
        self._normalize_inlined_as_list(slot_name="block_fields", slot_type=SbeFieldV2, key_name="symbolic_name", keyed=False)

        if self.dimension_type is not None and not isinstance(self.dimension_type, SbeSymbolicName):
            self.dimension_type = SbeSymbolicName(self.dimension_type)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class SbeFieldV2(YAMLRoot):
    """
    A message's or group entry's field, which uses an encoding at a place in its block and may state a constant.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FIX_SBE["SbeFieldV2"]
    class_class_curie: ClassVar[str] = "fix_sbe:SbeFieldV2"
    class_name: ClassVar[str] = "SbeFieldV2"
    class_model_uri: ClassVar[URIRef] = FIX_SBE.SbeFieldV2

    symbolic_name: Union[str, SbeSymbolicName] = None
    sbe_id: int = None
    encoding_name: Union[str, SbeSymbolicName] = None
    element_value: Optional[Union[str, SbeToken]] = None
    offset: Optional[int] = None
    alignment: Optional[int] = None
    presence: Optional[Union[str, "SbePresence"]] = 'required'
    null_value: Optional[str] = None
    min_value: Optional[str] = None
    max_value: Optional[str] = None
    value_ref: Optional[Union[str, SbeQualifiedName]] = None
    semantic_type: Optional[Union[str, SbeToken]] = None
    description: Optional[str] = None
    since_version: Optional[int] = 0
    deprecated_since: Optional[int] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.symbolic_name):
            self.MissingRequiredField("symbolic_name")
        if not isinstance(self.symbolic_name, SbeSymbolicName):
            self.symbolic_name = SbeSymbolicName(self.symbolic_name)

        if self._is_empty(self.sbe_id):
            self.MissingRequiredField("sbe_id")
        if not isinstance(self.sbe_id, int):
            self.sbe_id = int(self.sbe_id)

        if self._is_empty(self.encoding_name):
            self.MissingRequiredField("encoding_name")
        if not isinstance(self.encoding_name, SbeSymbolicName):
            self.encoding_name = SbeSymbolicName(self.encoding_name)

        if self.element_value is not None and not isinstance(self.element_value, SbeToken):
            self.element_value = SbeToken(self.element_value)

        if self.offset is not None and not isinstance(self.offset, int):
            self.offset = int(self.offset)

        if self.alignment is not None and not isinstance(self.alignment, int):
            self.alignment = int(self.alignment)

        if self.presence is not None and not isinstance(self.presence, SbePresence):
            self.presence = SbePresence(self.presence)

        if self.null_value is not None and not isinstance(self.null_value, str):
            self.null_value = str(self.null_value)

        if self.min_value is not None and not isinstance(self.min_value, str):
            self.min_value = str(self.min_value)

        if self.max_value is not None and not isinstance(self.max_value, str):
            self.max_value = str(self.max_value)

        if self.value_ref is not None and not isinstance(self.value_ref, SbeQualifiedName):
            self.value_ref = SbeQualifiedName(self.value_ref)

        if self.semantic_type is not None and not isinstance(self.semantic_type, SbeToken):
            self.semantic_type = SbeToken(self.semantic_type)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.since_version is not None and not isinstance(self.since_version, int):
            self.since_version = int(self.since_version)

        if self.deprecated_since is not None and not isinstance(self.deprecated_since, int):
            self.deprecated_since = int(self.deprecated_since)

        super().__post_init__(**kwargs)


# Enumerations
class SbePresence(EnumDefinitionImpl):
    """
    Whether a value is on the wire, and whether it may be null.
    """
    required = PermissibleValue(
        text="required",
        description="A value is always sent, and it is never tested for null.")
    optional = PermissibleValue(
        text="optional",
        description="A value is sent, and a null marker says that none is set.")
    constant = PermissibleValue(
        text="constant",
        description="The schema states the value, so nothing is sent.")

    _defn = EnumDefinition(
        name="SbePresence",
        description="Whether a value is on the wire, and whether it may be null.",
    )

class SbeByteOrder(EnumDefinitionImpl):
    """
    The order of the octets in every multi-octet number of a message.
    """
    bigEndian = PermissibleValue(
        text="bigEndian",
        description="The most significant octet comes first.")
    littleEndian = PermissibleValue(
        text="littleEndian",
        description="The least significant octet comes first.")

    _defn = EnumDefinition(
        name="SbeByteOrder",
        description="The order of the octets in every multi-octet number of a message.",
    )

class SbePrimitiveType(EnumDefinitionImpl):
    """
    The wire types every encoding is finally built from.
    """
    char = PermissibleValue(
        text="char",
        description="One character of one octet.")
    int8 = PermissibleValue(
        text="int8",
        description="A signed integer of one octet.")
    int16 = PermissibleValue(
        text="int16",
        description="A signed integer of two octets.")
    int32 = PermissibleValue(
        text="int32",
        description="A signed integer of four octets.")
    int64 = PermissibleValue(
        text="int64",
        description="A signed integer of eight octets.")
    uint8 = PermissibleValue(
        text="uint8",
        description="An unsigned integer of one octet.")
    uint16 = PermissibleValue(
        text="uint16",
        description="An unsigned integer of two octets.")
    uint32 = PermissibleValue(
        text="uint32",
        description="An unsigned integer of four octets.")
    uint64 = PermissibleValue(
        text="uint64",
        description="An unsigned integer of eight octets.")
    float = PermissibleValue(
        text="float",
        description="A four-octet number in binary floating point.")
    double = PermissibleValue(
        text="double",
        description="An eight-octet number in binary floating point.")

    _defn = EnumDefinition(
        name="SbePrimitiveType",
        description="The wire types every encoding is finally built from.",
    )

class SbeFixDatatype(EnumDefinitionImpl):
    """
    The FIX datatypes the specification's summary table lists as a field's or an encoding's semantic type.
    """
    int = PermissibleValue(text="int")
    Length = PermissibleValue(text="Length")
    TagNum = PermissibleValue(text="TagNum")
    SeqNum = PermissibleValue(text="SeqNum")
    NumInGroup = PermissibleValue(text="NumInGroup")
    DayOfMonth = PermissibleValue(text="DayOfMonth")
    Qty = PermissibleValue(text="Qty")
    float = PermissibleValue(text="float")
    Price = PermissibleValue(text="Price")
    PriceOffset = PermissibleValue(text="PriceOffset")
    Amt = PermissibleValue(text="Amt")
    Percentage = PermissibleValue(text="Percentage")
    char = PermissibleValue(text="char")
    String = PermissibleValue(text="String")
    EncodedText = PermissibleValue(text="EncodedText")
    XMLData = PermissibleValue(text="XMLData")
    data = PermissibleValue(text="data")
    Country = PermissibleValue(text="Country")
    Currency = PermissibleValue(text="Currency")
    Exchange = PermissibleValue(text="Exchange")
    Language = PermissibleValue(text="Language")
    Boolean = PermissibleValue(text="Boolean")
    MultipleCharValue = PermissibleValue(text="MultipleCharValue")
    MultipleStringValue = PermissibleValue(text="MultipleStringValue")
    MonthYear = PermissibleValue(text="MonthYear")
    UTCTimestamp = PermissibleValue(text="UTCTimestamp")
    UTCTimeOnly = PermissibleValue(text="UTCTimeOnly")
    UTCDateOnly = PermissibleValue(text="UTCDateOnly")
    LocalMktDate = PermissibleValue(text="LocalMktDate")
    TZTimeOnly = PermissibleValue(text="TZTimeOnly")
    TZTimestamp = PermissibleValue(text="TZTimestamp")

    _defn = EnumDefinition(
        name="SbeFixDatatype",
        description="""The FIX datatypes the specification's summary table lists as a field's or an encoding's semantic type.""",
    )

# Slots
class slots:
    pass

slots.symbolic_name = Slot(uri=FIX_SBE.symbolic_name, name="symbolic_name", curie=FIX_SBE.curie('symbolic_name'),
                   model_uri=FIX_SBE.symbolic_name, domain=None, range=Union[str, SbeSymbolicName],
                   pattern=re.compile(r'^[A-Za-z_][0-9A-Za-z_]{0,63}$'))

slots.sbe_id = Slot(uri=FIX_SBE.sbe_id, name="sbe_id", curie=FIX_SBE.curie('sbe_id'),
                   model_uri=FIX_SBE.sbe_id, domain=None, range=Optional[int])

slots.description = Slot(uri=SCHEMA.description, name="description", curie=SCHEMA.curie('description'),
                   model_uri=FIX_SBE.description, domain=None, range=Optional[str])

slots.semantic_type = Slot(uri=FIX_SBE.semantic_type, name="semantic_type", curie=FIX_SBE.curie('semantic_type'),
                   model_uri=FIX_SBE.semantic_type, domain=None, range=Optional[Union[str, SbeToken]],
                   pattern=re.compile(r'^\S+( \S+)*$'))

slots.since_version = Slot(uri=FIX_SBE.since_version, name="since_version", curie=FIX_SBE.curie('since_version'),
                   model_uri=FIX_SBE.since_version, domain=None, range=Optional[int])

slots.deprecated_since = Slot(uri=FIX_SBE.deprecated_since, name="deprecated_since", curie=FIX_SBE.curie('deprecated_since'),
                   model_uri=FIX_SBE.deprecated_since, domain=None, range=Optional[int])

slots.offset = Slot(uri=FIX_SBE.offset, name="offset", curie=FIX_SBE.curie('offset'),
                   model_uri=FIX_SBE.offset, domain=None, range=Optional[int])

slots.presence = Slot(uri=FIX_SBE.presence, name="presence", curie=FIX_SBE.curie('presence'),
                   model_uri=FIX_SBE.presence, domain=None, range=Optional[Union[str, "SbePresence"]])

slots.value_ref = Slot(uri=FIX_SBE.value_ref, name="value_ref", curie=FIX_SBE.curie('value_ref'),
                   model_uri=FIX_SBE.value_ref, domain=None, range=Optional[Union[str, SbeQualifiedName]],
                   pattern=re.compile(r'^[A-Za-z_][0-9A-Za-z_]*\.[A-Za-z_][0-9A-Za-z_]*$'))

slots.element_value = Slot(uri=FIX_SBE.element_value, name="element_value", curie=FIX_SBE.curie('element_value'),
                   model_uri=FIX_SBE.element_value, domain=None, range=Optional[Union[str, SbeToken]],
                   pattern=re.compile(r'^\S+( \S+)*$'))

slots.primitive_type = Slot(uri=FIX_SBE.primitive_type, name="primitive_type", curie=FIX_SBE.curie('primitive_type'),
                   model_uri=FIX_SBE.primitive_type, domain=None, range=Union[str, "SbePrimitiveType"])

slots.array_length = Slot(uri=FIX_SBE.array_length, name="array_length", curie=FIX_SBE.curie('array_length'),
                   model_uri=FIX_SBE.array_length, domain=None, range=Optional[int])

slots.character_encoding = Slot(uri=FIX_SBE.character_encoding, name="character_encoding", curie=FIX_SBE.curie('character_encoding'),
                   model_uri=FIX_SBE.character_encoding, domain=None, range=Optional[str])

slots.null_value = Slot(uri=FIX_SBE.null_value, name="null_value", curie=FIX_SBE.curie('null_value'),
                   model_uri=FIX_SBE.null_value, domain=None, range=Optional[str])

slots.min_value = Slot(uri=FIX_SBE.min_value, name="min_value", curie=FIX_SBE.curie('min_value'),
                   model_uri=FIX_SBE.min_value, domain=None, range=Optional[str])

slots.max_value = Slot(uri=FIX_SBE.max_value, name="max_value", curie=FIX_SBE.curie('max_value'),
                   model_uri=FIX_SBE.max_value, domain=None, range=Optional[str])

slots.encoding_type = Slot(uri=FIX_SBE.encoding_type, name="encoding_type", curie=FIX_SBE.curie('encoding_type'),
                   model_uri=FIX_SBE.encoding_type, domain=None, range=Union[str, SbeSymbolicName],
                   pattern=re.compile(r'^[A-Za-z_][0-9A-Za-z_]{0,63}$'))

slots.encoding_name = Slot(uri=FIX_SBE.encoding_name, name="encoding_name", curie=FIX_SBE.curie('encoding_name'),
                   model_uri=FIX_SBE.encoding_name, domain=None, range=Union[str, SbeSymbolicName],
                   pattern=re.compile(r'^[A-Za-z_][0-9A-Za-z_]{0,63}$'))

slots.block_length = Slot(uri=FIX_SBE.block_length, name="block_length", curie=FIX_SBE.curie('block_length'),
                   model_uri=FIX_SBE.block_length, domain=None, range=Optional[int])

slots.dimension_type = Slot(uri=FIX_SBE.dimension_type, name="dimension_type", curie=FIX_SBE.curie('dimension_type'),
                   model_uri=FIX_SBE.dimension_type, domain=None, range=Optional[Union[str, SbeSymbolicName]],
                   pattern=re.compile(r'^[A-Za-z_][0-9A-Za-z_]{0,63}$'))

slots.schema_package = Slot(uri=FIX_SBE.schema_package, name="schema_package", curie=FIX_SBE.curie('schema_package'),
                   model_uri=FIX_SBE.schema_package, domain=None, range=Optional[str])

slots.schema_version = Slot(uri=FIX_SBE.schema_version, name="schema_version", curie=FIX_SBE.curie('schema_version'),
                   model_uri=FIX_SBE.schema_version, domain=None, range=int)

slots.semantic_version = Slot(uri=FIX_SBE.semantic_version, name="semantic_version", curie=FIX_SBE.curie('semantic_version'),
                   model_uri=FIX_SBE.semantic_version, domain=None, range=Optional[str])

slots.byte_order = Slot(uri=FIX_SBE.byte_order, name="byte_order", curie=FIX_SBE.curie('byte_order'),
                   model_uri=FIX_SBE.byte_order, domain=None, range=Optional[Union[str, "SbeByteOrder"]])

slots.header_type = Slot(uri=FIX_SBE.header_type, name="header_type", curie=FIX_SBE.curie('header_type'),
                   model_uri=FIX_SBE.header_type, domain=None, range=Optional[Union[str, SbeSymbolicName]],
                   pattern=re.compile(r'^[A-Za-z_][0-9A-Za-z_]{0,63}$'))

slots.encoding_kind = Slot(uri=FIX_SBE.encoding_kind, name="encoding_kind", curie=FIX_SBE.curie('encoding_kind'),
                   model_uri=FIX_SBE.encoding_kind, domain=None, range=str)

slots.encoding_sets = Slot(uri=FIX_SBE.encoding_sets, name="encoding_sets", curie=FIX_SBE.curie('encoding_sets'),
                   model_uri=FIX_SBE.encoding_sets, domain=None, range=Union[str, list[str]])

slots.message_sets = Slot(uri=FIX_SBE.message_sets, name="message_sets", curie=FIX_SBE.curie('message_sets'),
                   model_uri=FIX_SBE.message_sets, domain=None, range=Union[str, list[str]])

slots.messages = Slot(uri=FIX_SBE.messages, name="messages", curie=FIX_SBE.curie('messages'),
                   model_uri=FIX_SBE.messages, domain=None, range=Union[str, list[str]])

slots.encodings = Slot(uri=FIX_SBE.encodings, name="encodings", curie=FIX_SBE.curie('encodings'),
                   model_uri=FIX_SBE.encodings, domain=None, range=Union[str, list[str]])

slots.composite_members = Slot(uri=FIX_SBE.composite_members, name="composite_members", curie=FIX_SBE.curie('composite_members'),
                   model_uri=FIX_SBE.composite_members, domain=None, range=Union[str, list[str]])

slots.valid_values = Slot(uri=FIX_SBE.valid_values, name="valid_values", curie=FIX_SBE.curie('valid_values'),
                   model_uri=FIX_SBE.valid_values, domain=None, range=Union[Union[dict, SbeValidValue], list[Union[dict, SbeValidValue]]])

slots.choices = Slot(uri=FIX_SBE.choices, name="choices", curie=FIX_SBE.curie('choices'),
                   model_uri=FIX_SBE.choices, domain=None, range=Union[Union[dict, SbeChoice], list[Union[dict, SbeChoice]]])

slots.block_fields = Slot(uri=FIX_SBE.block_fields, name="block_fields", curie=FIX_SBE.curie('block_fields'),
                   model_uri=FIX_SBE.block_fields, domain=None, range=Optional[Union[str, list[str]]])

slots.repeating_groups = Slot(uri=FIX_SBE.repeating_groups, name="repeating_groups", curie=FIX_SBE.curie('repeating_groups'),
                   model_uri=FIX_SBE.repeating_groups, domain=None, range=Optional[Union[str, list[str]]])

slots.var_data_fields = Slot(uri=FIX_SBE.var_data_fields, name="var_data_fields", curie=FIX_SBE.curie('var_data_fields'),
                   model_uri=FIX_SBE.var_data_fields, domain=None, range=Optional[Union[str, list[str]]])

slots.alignment = Slot(uri=FIX_SBE.alignment, name="alignment", curie=FIX_SBE.curie('alignment'),
                   model_uri=FIX_SBE.alignment, domain=None, range=Optional[int])

slots.xml_base = Slot(uri=FIX_SBE.xml_base, name="xml_base", curie=FIX_SBE.curie('xml_base'),
                   model_uri=FIX_SBE.xml_base, domain=None, range=Optional[Union[str, URI]])

slots.sbeValidValue__valid_value = Slot(uri=FIX_SBE.valid_value, name="sbeValidValue__valid_value", curie=FIX_SBE.curie('valid_value'),
                   model_uri=FIX_SBE.sbeValidValue__valid_value, domain=None, range=Union[str, SbeToken],
                   pattern=re.compile(r'^\S+( \S+)*$'))

slots.sbeChoice__bit_position = Slot(uri=FIX_SBE.bit_position, name="sbeChoice__bit_position", curie=FIX_SBE.curie('bit_position'),
                   model_uri=FIX_SBE.sbeChoice__bit_position, domain=None, range=int)

slots.sbeFieldV1__time_epoch = Slot(uri=FIX_SBE.time_epoch, name="sbeFieldV1__time_epoch", curie=FIX_SBE.curie('time_epoch'),
                   model_uri=FIX_SBE.sbeFieldV1__time_epoch, domain=None, range=Optional[str])

slots.sbeFieldV1__time_unit = Slot(uri=FIX_SBE.time_unit, name="sbeFieldV1__time_unit", curie=FIX_SBE.curie('time_unit'),
                   model_uri=FIX_SBE.sbeFieldV1__time_unit, domain=None, range=Optional[str])

slots.SbeMessageSchemaV1_sbe_id = Slot(uri=FIX_SBE.sbe_id, name="SbeMessageSchemaV1_sbe_id", curie=FIX_SBE.curie('sbe_id'),
                   model_uri=FIX_SBE.SbeMessageSchemaV1_sbe_id, domain=SbeMessageSchemaV1, range=Optional[int])

slots.SbeMessageSchemaV1_encoding_sets = Slot(uri=FIX_SBE.encoding_sets, name="SbeMessageSchemaV1_encoding_sets", curie=FIX_SBE.curie('encoding_sets'),
                   model_uri=FIX_SBE.SbeMessageSchemaV1_encoding_sets, domain=SbeMessageSchemaV1, range=Union[Union[dict, "SbeEncodingSetV1"], list[Union[dict, "SbeEncodingSetV1"]]])

slots.SbeMessageSchemaV1_messages = Slot(uri=FIX_SBE.messages, name="SbeMessageSchemaV1_messages", curie=FIX_SBE.curie('messages'),
                   model_uri=FIX_SBE.SbeMessageSchemaV1_messages, domain=SbeMessageSchemaV1, range=Union[Union[dict, "SbeMessageV1"], list[Union[dict, "SbeMessageV1"]]])

slots.SbeEncodingSetV1_encodings = Slot(uri=FIX_SBE.encodings, name="SbeEncodingSetV1_encodings", curie=FIX_SBE.curie('encodings'),
                   model_uri=FIX_SBE.SbeEncodingSetV1_encodings, domain=SbeEncodingSetV1, range=Union[Union[dict, "SbeEncodingV1"], list[Union[dict, "SbeEncodingV1"]]])

slots.SbeEncodingV1_semantic_type = Slot(uri=FIX_SBE.semantic_type, name="SbeEncodingV1_semantic_type", curie=FIX_SBE.curie('semantic_type'),
                   model_uri=FIX_SBE.SbeEncodingV1_semantic_type, domain=SbeEncodingV1, range=Optional[Union[str, SbeToken]],
                   pattern=re.compile(r'^\S+( \S+)*$'))

slots.SbeCompositeV1_composite_members = Slot(uri=FIX_SBE.composite_members, name="SbeCompositeV1_composite_members", curie=FIX_SBE.curie('composite_members'),
                   model_uri=FIX_SBE.SbeCompositeV1_composite_members, domain=SbeCompositeV1, range=Union[Union[dict, SbeMemberV1], list[Union[dict, SbeMemberV1]]])

slots.SbeBlockV1_sbe_id = Slot(uri=FIX_SBE.sbe_id, name="SbeBlockV1_sbe_id", curie=FIX_SBE.curie('sbe_id'),
                   model_uri=FIX_SBE.SbeBlockV1_sbe_id, domain=SbeBlockV1, range=int)

slots.SbeBlockV1_block_fields = Slot(uri=FIX_SBE.block_fields, name="SbeBlockV1_block_fields", curie=FIX_SBE.curie('block_fields'),
                   model_uri=FIX_SBE.SbeBlockV1_block_fields, domain=SbeBlockV1, range=Optional[Union[Union[dict, "SbeFieldV1"], list[Union[dict, "SbeFieldV1"]]]])

slots.SbeBlockV1_repeating_groups = Slot(uri=FIX_SBE.repeating_groups, name="SbeBlockV1_repeating_groups", curie=FIX_SBE.curie('repeating_groups'),
                   model_uri=FIX_SBE.SbeBlockV1_repeating_groups, domain=SbeBlockV1, range=Optional[Union[Union[dict, "SbeGroupV1"], list[Union[dict, "SbeGroupV1"]]]])

slots.SbeBlockV1_var_data_fields = Slot(uri=FIX_SBE.var_data_fields, name="SbeBlockV1_var_data_fields", curie=FIX_SBE.curie('var_data_fields'),
                   model_uri=FIX_SBE.SbeBlockV1_var_data_fields, domain=SbeBlockV1, range=Optional[Union[Union[dict, "SbeFieldV1"], list[Union[dict, "SbeFieldV1"]]]])

slots.SbeMessageV1_sbe_id = Slot(uri=FIX_SBE.sbe_id, name="SbeMessageV1_sbe_id", curie=FIX_SBE.curie('sbe_id'),
                   model_uri=FIX_SBE.SbeMessageV1_sbe_id, domain=SbeMessageV1, range=int)

slots.SbeMessageV1_semantic_type = Slot(uri=FIX_SBE.semantic_type, name="SbeMessageV1_semantic_type", curie=FIX_SBE.curie('semantic_type'),
                   model_uri=FIX_SBE.SbeMessageV1_semantic_type, domain=SbeMessageV1, range=Optional[Union[str, SbeToken]],
                   pattern=re.compile(r'^\S+( \S+)*$'))

slots.SbeGroupV1_block_fields = Slot(uri=FIX_SBE.block_fields, name="SbeGroupV1_block_fields", curie=FIX_SBE.curie('block_fields'),
                   model_uri=FIX_SBE.SbeGroupV1_block_fields, domain=SbeGroupV1, range=Union[Union[dict, "SbeFieldV1"], list[Union[dict, "SbeFieldV1"]]])

slots.SbeFieldV1_sbe_id = Slot(uri=FIX_SBE.sbe_id, name="SbeFieldV1_sbe_id", curie=FIX_SBE.curie('sbe_id'),
                   model_uri=FIX_SBE.SbeFieldV1_sbe_id, domain=SbeFieldV1, range=int)

slots.SbeFieldV1_semantic_type = Slot(uri=FIX_SBE.semantic_type, name="SbeFieldV1_semantic_type", curie=FIX_SBE.curie('semantic_type'),
                   model_uri=FIX_SBE.SbeFieldV1_semantic_type, domain=SbeFieldV1, range=Optional[Union[str, SbeToken]],
                   pattern=re.compile(r'^\S+( \S+)*$'))

slots.SbeMessageSchemaV2_sbe_id = Slot(uri=FIX_SBE.sbe_id, name="SbeMessageSchemaV2_sbe_id", curie=FIX_SBE.curie('sbe_id'),
                   model_uri=FIX_SBE.SbeMessageSchemaV2_sbe_id, domain=SbeMessageSchemaV2, range=Optional[int])

slots.SbeMessageSchemaV2_encoding_sets = Slot(uri=FIX_SBE.encoding_sets, name="SbeMessageSchemaV2_encoding_sets", curie=FIX_SBE.curie('encoding_sets'),
                   model_uri=FIX_SBE.SbeMessageSchemaV2_encoding_sets, domain=SbeMessageSchemaV2, range=Union[Union[dict, "SbeEncodingSetV2"], list[Union[dict, "SbeEncodingSetV2"]]])

slots.SbeMessageSchemaV2_message_sets = Slot(uri=FIX_SBE.message_sets, name="SbeMessageSchemaV2_message_sets", curie=FIX_SBE.curie('message_sets'),
                   model_uri=FIX_SBE.SbeMessageSchemaV2_message_sets, domain=SbeMessageSchemaV2, range=Union[Union[dict, "SbeMessageSetV2"], list[Union[dict, "SbeMessageSetV2"]]])

slots.SbeEncodingSetV2_schema_package = Slot(uri=FIX_SBE.schema_package, name="SbeEncodingSetV2_schema_package", curie=FIX_SBE.curie('schema_package'),
                   model_uri=FIX_SBE.SbeEncodingSetV2_schema_package, domain=SbeEncodingSetV2, range=Optional[str])

slots.SbeEncodingSetV2_encodings = Slot(uri=FIX_SBE.encodings, name="SbeEncodingSetV2_encodings", curie=FIX_SBE.curie('encodings'),
                   model_uri=FIX_SBE.SbeEncodingSetV2_encodings, domain=SbeEncodingSetV2, range=Union[Union[dict, "SbeElementV2"], list[Union[dict, "SbeElementV2"]]])

slots.SbeMessageSetV2_schema_package = Slot(uri=FIX_SBE.schema_package, name="SbeMessageSetV2_schema_package", curie=FIX_SBE.curie('schema_package'),
                   model_uri=FIX_SBE.SbeMessageSetV2_schema_package, domain=SbeMessageSetV2, range=Optional[str])

slots.SbeMessageSetV2_messages = Slot(uri=FIX_SBE.messages, name="SbeMessageSetV2_messages", curie=FIX_SBE.curie('messages'),
                   model_uri=FIX_SBE.SbeMessageSetV2_messages, domain=SbeMessageSetV2, range=Union[Union[dict, "SbeMessageV2"], list[Union[dict, "SbeMessageV2"]]])

slots.SbeCompositeV2_composite_members = Slot(uri=FIX_SBE.composite_members, name="SbeCompositeV2_composite_members", curie=FIX_SBE.curie('composite_members'),
                   model_uri=FIX_SBE.SbeCompositeV2_composite_members, domain=SbeCompositeV2, range=Union[Union[dict, SbeMemberV2], list[Union[dict, SbeMemberV2]]])

slots.SbeBlockV2_sbe_id = Slot(uri=FIX_SBE.sbe_id, name="SbeBlockV2_sbe_id", curie=FIX_SBE.curie('sbe_id'),
                   model_uri=FIX_SBE.SbeBlockV2_sbe_id, domain=SbeBlockV2, range=int)

slots.SbeBlockV2_alignment = Slot(uri=FIX_SBE.alignment, name="SbeBlockV2_alignment", curie=FIX_SBE.curie('alignment'),
                   model_uri=FIX_SBE.SbeBlockV2_alignment, domain=SbeBlockV2, range=Optional[int])

slots.SbeBlockV2_block_fields = Slot(uri=FIX_SBE.block_fields, name="SbeBlockV2_block_fields", curie=FIX_SBE.curie('block_fields'),
                   model_uri=FIX_SBE.SbeBlockV2_block_fields, domain=SbeBlockV2, range=Optional[Union[Union[dict, "SbeFieldV2"], list[Union[dict, "SbeFieldV2"]]]])

slots.SbeBlockV2_repeating_groups = Slot(uri=FIX_SBE.repeating_groups, name="SbeBlockV2_repeating_groups", curie=FIX_SBE.curie('repeating_groups'),
                   model_uri=FIX_SBE.SbeBlockV2_repeating_groups, domain=SbeBlockV2, range=Optional[Union[Union[dict, "SbeGroupV2"], list[Union[dict, "SbeGroupV2"]]]])

slots.SbeBlockV2_var_data_fields = Slot(uri=FIX_SBE.var_data_fields, name="SbeBlockV2_var_data_fields", curie=FIX_SBE.curie('var_data_fields'),
                   model_uri=FIX_SBE.SbeBlockV2_var_data_fields, domain=SbeBlockV2, range=Optional[Union[Union[dict, "SbeFieldV2"], list[Union[dict, "SbeFieldV2"]]]])

slots.SbeMessageV2_sbe_id = Slot(uri=FIX_SBE.sbe_id, name="SbeMessageV2_sbe_id", curie=FIX_SBE.curie('sbe_id'),
                   model_uri=FIX_SBE.SbeMessageV2_sbe_id, domain=SbeMessageV2, range=int)

slots.SbeMessageV2_semantic_type = Slot(uri=FIX_SBE.semantic_type, name="SbeMessageV2_semantic_type", curie=FIX_SBE.curie('semantic_type'),
                   model_uri=FIX_SBE.SbeMessageV2_semantic_type, domain=SbeMessageV2, range=Optional[Union[str, SbeToken]],
                   pattern=re.compile(r'^\S+( \S+)*$'))

slots.SbeGroupV2_block_fields = Slot(uri=FIX_SBE.block_fields, name="SbeGroupV2_block_fields", curie=FIX_SBE.curie('block_fields'),
                   model_uri=FIX_SBE.SbeGroupV2_block_fields, domain=SbeGroupV2, range=Union[Union[dict, "SbeFieldV2"], list[Union[dict, "SbeFieldV2"]]])

slots.SbeFieldV2_sbe_id = Slot(uri=FIX_SBE.sbe_id, name="SbeFieldV2_sbe_id", curie=FIX_SBE.curie('sbe_id'),
                   model_uri=FIX_SBE.SbeFieldV2_sbe_id, domain=SbeFieldV2, range=int)

slots.SbeFieldV2_semantic_type = Slot(uri=FIX_SBE.semantic_type, name="SbeFieldV2_semantic_type", curie=FIX_SBE.curie('semantic_type'),
                   model_uri=FIX_SBE.SbeFieldV2_semantic_type, domain=SbeFieldV2, range=Optional[Union[str, SbeToken]],
                   pattern=re.compile(r'^\S+( \S+)*$'))

slots.SbeFieldV2_alignment = Slot(uri=FIX_SBE.alignment, name="SbeFieldV2_alignment", curie=FIX_SBE.curie('alignment'),
                   model_uri=FIX_SBE.SbeFieldV2_alignment, domain=SbeFieldV2, range=Optional[int])
