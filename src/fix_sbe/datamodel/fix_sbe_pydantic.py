from __future__ import annotations

import re
import sys
from datetime import (
    date,
    datetime,
    time
)
from decimal import Decimal
from enum import Enum
from typing import (
    Any,
    ClassVar,
    Literal,
    Optional,
    Union
)

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    RootModel,
    SerializationInfo,
    SerializerFunctionWrapHandler,
    field_validator,
    model_serializer
)


metamodel_version = "1.12.0"
version = "1.0 and 2.0-rc3"


class ConfiguredBaseModel(BaseModel):
    model_config = ConfigDict(
        serialize_by_alias = True,
        validate_by_name = True,
        validate_assignment = True,
        validate_default = True,
        extra = "forbid",
        arbitrary_types_allowed = True,
        use_enum_values = True,
        strict = False,
    )





class LinkMLMeta(RootModel):
    root: dict[str, Any] = {}
    model_config = ConfigDict(frozen=True)

    def __getattr__(self, key:str):
        return getattr(self.root, key)

    def __getitem__(self, key:str):
        return self.root[key]

    def __setitem__(self, key:str, value):
        self.root[key] = value

    def __contains__(self, key:str) -> bool:
        return key in self.root


linkml_meta = LinkMLMeta({'annotations': {'upstream_v1_commit': {'tag': 'upstream_v1_commit',
                                            'value': '6321e6b9bce5bc198f88f462054cbaf4f33d8f60'},
                     'upstream_v1_tag': {'tag': 'upstream_v1_tag',
                                         'value': 'v1.0-errata-Nov-2020'},
                     'upstream_v2_commit': {'tag': 'upstream_v2_commit',
                                            'value': '418a8f6a8b93c65b308638dab2bc6a35dddcd864'}},
     'comments': ['A document of SBE 1.0 starts at SbeMessageSchemaV1, the tree '
                  'root, and one of SBE 2.0 RC3 at SbeMessageSchemaV2. upstream/ '
                  'holds both XSDs unchanged, tests/test_coverage.py holds the '
                  'modules to them, and scripts/check_upstream_release.py reports '
                  'when either moves.'],
     'default_prefix': 'fix_sbe',
     'default_range': 'string',
     'description': 'A LinkML model of FIX Simple Binary Encoding, a standard from '
                    'the FIX Trading Community for encoding messages in binary. It '
                    'describes SBE message schemas: encodings, message templates, '
                    'fields, groups and variable-length data. The two editions '
                    'differ on the wire and in their XML, so each has a module of '
                    'its own.',
     'id': 'https://w3id.org/lmodel/fix-sbe',
     'imports': ['linkml:types',
                 './fix_sbe_common',
                 './fix_sbe_v1_0',
                 './fix_sbe_v2_0'],
     'keywords': ['FIX', 'SBE', 'binary encoding', 'message schema', 'wire format'],
     'license': 'Apache-2.0',
     'name': 'fix_sbe',
     'prefixes': {'fix_orchestra': {'prefix_prefix': 'fix_orchestra',
                                    'prefix_reference': 'https://w3id.org/lmodel/fix-orchestra/'},
                  'fix_sbe': {'prefix_prefix': 'fix_sbe',
                              'prefix_reference': 'https://w3id.org/lmodel/fix-sbe/'},
                  'linkml': {'prefix_prefix': 'linkml',
                             'prefix_reference': 'https://w3id.org/linkml/'},
                  'schema': {'prefix_prefix': 'schema',
                             'prefix_reference': 'http://schema.org/'}},
     'see_also': ['https://lmodel.github.io/fix-sbe',
                  'https://github.com/FIXTradingCommunity/fix-simple-binary-encoding',
                  'https://www.iana.org/assignments/media-types/application/sbe'],
     'source': 'https://github.com/FIXTradingCommunity/fix-simple-binary-encoding',
     'source_file': 'src/fix_sbe/schema/fix_sbe.yaml',
     'title': 'FIX Simple Binary Encoding (SBE)'} )

class SbePresence(str, Enum):
    """
    Whether a value is on the wire, and whether it may be null.
    """
    required = "required"
    """
    A value is always sent, and it is never tested for null.
    """
    optional = "optional"
    """
    A value is sent, and a null marker says that none is set.
    """
    constant = "constant"
    """
    The schema states the value, so nothing is sent.
    """


class SbeByteOrder(str, Enum):
    """
    The order of the octets in every multi-octet number of a message.
    """
    bigEndian = "bigEndian"
    """
    The most significant octet comes first.
    """
    littleEndian = "littleEndian"
    """
    The least significant octet comes first.
    """


class SbePrimitiveType(str, Enum):
    """
    The wire types every encoding is finally built from.
    """
    char = "char"
    """
    One character of one octet.
    """
    int8 = "int8"
    """
    A signed integer of one octet.
    """
    int16 = "int16"
    """
    A signed integer of two octets.
    """
    int32 = "int32"
    """
    A signed integer of four octets.
    """
    int64 = "int64"
    """
    A signed integer of eight octets.
    """
    uint8 = "uint8"
    """
    An unsigned integer of one octet.
    """
    uint16 = "uint16"
    """
    An unsigned integer of two octets.
    """
    uint32 = "uint32"
    """
    An unsigned integer of four octets.
    """
    uint64 = "uint64"
    """
    An unsigned integer of eight octets.
    """
    float = "float"
    """
    A four-octet number in binary floating point.
    """
    double = "double"
    """
    An eight-octet number in binary floating point.
    """


class SbeFixDatatype(str, Enum):
    """
    The FIX datatypes the specification's summary table lists as a field's or an encoding's semantic type.
    """
    int = "int"
    Length = "Length"
    TagNum = "TagNum"
    SeqNum = "SeqNum"
    NumInGroup = "NumInGroup"
    DayOfMonth = "DayOfMonth"
    Qty = "Qty"
    float = "float"
    Price = "Price"
    PriceOffset = "PriceOffset"
    Amt = "Amt"
    Percentage = "Percentage"
    char = "char"
    String = "String"
    EncodedText = "EncodedText"
    XMLData = "XMLData"
    data = "data"
    Country = "Country"
    Currency = "Currency"
    Exchange = "Exchange"
    Language = "Language"
    Boolean = "Boolean"
    MultipleCharValue = "MultipleCharValue"
    MultipleStringValue = "MultipleStringValue"
    MonthYear = "MonthYear"
    UTCTimestamp = "UTCTimestamp"
    UTCTimeOnly = "UTCTimeOnly"
    UTCDateOnly = "UTCDateOnly"
    LocalMktDate = "LocalMktDate"
    TZTimeOnly = "TZTimeOnly"
    TZTimestamp = "TZTimestamp"



class SbeVersionedMixin(ConfiguredBaseModel):
    """
    The two attributes that record when an element entered a schema and when it should leave.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'xsd_attribute_group': {'tag': 'xsd_attribute_group',
                                                 'value': 'versionAttributes'}},
         'from_schema': 'https://w3id.org/lmodel/fix-sbe/schema/fix_sbe_common',
         'mixin': True})

    since_version: Optional[int] = Field(default=0, description="""The schema version that added this element.""", ge=0, json_schema_extra = { "linkml_meta": {'aliases': ['sinceVersion'],
         'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '5: Since version'},
                         'xsd_type': {'tag': 'xsd_type',
                                      'value': 'xs:nonNegativeInteger'}},
         'domain_of': ['SbeVersionedMixin'],
         'ifabsent': 'int(0)'} })
    deprecated_since: Optional[int] = Field(default=None, description="""The schema version that retired this element, which stays only for older applications.""", ge=0, json_schema_extra = { "linkml_meta": {'aliases': ['deprecated'],
         'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '5: Deprecated elements'},
                         'xsd_type': {'tag': 'xsd_type',
                                      'value': 'xs:nonNegativeInteger'}},
         'domain_of': ['SbeVersionedMixin']} })


class SbeValidValue(SbeVersionedMixin):
    """
    One of the values an enumeration allows.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'xsd_type': {'tag': 'xsd_type', 'value': 'validValue'}},
         'close_mappings': ['fix_orchestra:OrchestraCodeV10'],
         'from_schema': 'https://w3id.org/lmodel/fix-sbe/schema/fix_sbe_common',
         'mixins': ['SbeVersionedMixin']})

    symbolic_name: str = Field(default=..., description="""What the schema calls this element.""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['SbeValidValue',
                       'SbeChoice',
                       'SbeMemberV1',
                       'SbeBlockV1Mixin',
                       'SbeFieldV1',
                       'SbeElementV2',
                       'SbeBlockV2Mixin',
                       'SbeFieldV2']} })
    description: Optional[str] = Field(default=None, description="""Free text about this element, for the people who read the schema.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'domain_of': ['SbeValidValue',
                       'SbeChoice',
                       'SbeMessageSchemaV1',
                       'SbeEncodingV1',
                       'SbeBlockV1Mixin',
                       'SbeFieldV1',
                       'SbeMessageSchemaV2',
                       'SbeEncodingSetV2',
                       'SbeMessageSetV2',
                       'SbeElementV2',
                       'SbeBlockV2Mixin',
                       'SbeFieldV2'],
         'slot_uri': 'schema:description'} })
    valid_value: str = Field(default=..., description="""The value as it is written in the schema, which must convert to the enumeration's encoding.""", json_schema_extra = { "linkml_meta": {'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '4: Schema validation'},
                         'xsd_type': {'tag': 'xsd_type', 'value': 'xs:token'}},
         'domain_of': ['SbeValidValue']} })
    since_version: Optional[int] = Field(default=0, description="""The schema version that added this element.""", ge=0, json_schema_extra = { "linkml_meta": {'aliases': ['sinceVersion'],
         'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '5: Since version'},
                         'xsd_type': {'tag': 'xsd_type',
                                      'value': 'xs:nonNegativeInteger'}},
         'domain_of': ['SbeVersionedMixin'],
         'ifabsent': 'int(0)'} })
    deprecated_since: Optional[int] = Field(default=None, description="""The schema version that retired this element, which stays only for older applications.""", ge=0, json_schema_extra = { "linkml_meta": {'aliases': ['deprecated'],
         'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '5: Deprecated elements'},
                         'xsd_type': {'tag': 'xsd_type',
                                      'value': 'xs:nonNegativeInteger'}},
         'domain_of': ['SbeVersionedMixin']} })

    @field_validator('symbolic_name')
    def pattern_symbolic_name(cls, v):
        pattern=re.compile(r"^[A-Za-z_][0-9A-Za-z_]{0,63}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid symbolic_name format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid symbolic_name format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('valid_value')
    def pattern_valid_value(cls, v):
        pattern=re.compile(r"^\S+( \S+)*$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid valid_value format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid valid_value format: {v}"
            raise ValueError(err_msg)
        return v


class SbeChoice(SbeVersionedMixin):
    """
    One of the alternatives of a set, which is one bit of its encoding.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'xsd_type': {'tag': 'xsd_type', 'value': 'choice'}},
         'comments': ["FIX's transposer does not carry a set to Orchestra, so the "
                      "mapping is related. FIX's MultipleCharValue and "
                      'MultipleStringValue fields hold such choices in a code set.'],
         'from_schema': 'https://w3id.org/lmodel/fix-sbe/schema/fix_sbe_common',
         'mixins': ['SbeVersionedMixin'],
         'related_mappings': ['fix_orchestra:OrchestraCodeV10']})

    symbolic_name: str = Field(default=..., description="""What the schema calls this element.""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['SbeValidValue',
                       'SbeChoice',
                       'SbeMemberV1',
                       'SbeBlockV1Mixin',
                       'SbeFieldV1',
                       'SbeElementV2',
                       'SbeBlockV2Mixin',
                       'SbeFieldV2']} })
    description: Optional[str] = Field(default=None, description="""Free text about this element, for the people who read the schema.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'domain_of': ['SbeValidValue',
                       'SbeChoice',
                       'SbeMessageSchemaV1',
                       'SbeEncodingV1',
                       'SbeBlockV1Mixin',
                       'SbeFieldV1',
                       'SbeMessageSchemaV2',
                       'SbeEncodingSetV2',
                       'SbeMessageSetV2',
                       'SbeElementV2',
                       'SbeBlockV2Mixin',
                       'SbeFieldV2'],
         'slot_uri': 'schema:description'} })
    bit_position: int = Field(default=..., description="""Which bit stands for this choice, counted from zero at the least significant.""", ge=0, json_schema_extra = { "linkml_meta": {'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '4: choice element content'},
                         'xsd_type': {'tag': 'xsd_type',
                                      'value': 'xs:nonNegativeInteger'}},
         'domain_of': ['SbeChoice']} })
    since_version: Optional[int] = Field(default=0, description="""The schema version that added this element.""", ge=0, json_schema_extra = { "linkml_meta": {'aliases': ['sinceVersion'],
         'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '5: Since version'},
                         'xsd_type': {'tag': 'xsd_type',
                                      'value': 'xs:nonNegativeInteger'}},
         'domain_of': ['SbeVersionedMixin'],
         'ifabsent': 'int(0)'} })
    deprecated_since: Optional[int] = Field(default=None, description="""The schema version that retired this element, which stays only for older applications.""", ge=0, json_schema_extra = { "linkml_meta": {'aliases': ['deprecated'],
         'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '5: Deprecated elements'},
                         'xsd_type': {'tag': 'xsd_type',
                                      'value': 'xs:nonNegativeInteger'}},
         'domain_of': ['SbeVersionedMixin']} })

    @field_validator('symbolic_name')
    def pattern_symbolic_name(cls, v):
        pattern=re.compile(r"^[A-Za-z_][0-9A-Za-z_]{0,63}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid symbolic_name format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid symbolic_name format: {v}"
            raise ValueError(err_msg)
        return v


class SbeMessageSchemaV1(ConfiguredBaseModel):
    """
    One SBE 1.0 message schema, with its encodings and message templates.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'xml_element': {'tag': 'xml_element',
                                         'value': 'messageSchema'}},
         'close_mappings': ['fix_orchestra:OrchestraRepositoryV10'],
         'from_schema': 'https://w3id.org/lmodel/fix-sbe/schema/fix_sbe_v1_0',
         'slot_usage': {'encoding_sets': {'name': 'encoding_sets',
                                          'range': 'SbeEncodingSetV1'},
                        'messages': {'name': 'messages', 'range': 'SbeMessageV1'},
                        'sbe_id': {'description': 'The number that identifies this '
                                                  'schema between counterparties.',
                                   'name': 'sbe_id'}},
         'tree_root': True})

    schema_package: Optional[str] = Field(default=None, description="""The name or category that a set of counterparties knows this schema or part of it by.""", json_schema_extra = { "linkml_meta": {'aliases': ['package'],
         'domain_of': ['SbeMessageSchemaV1',
                       'SbeMessageSchemaV2',
                       'SbeEncodingSetV2',
                       'SbeMessageSetV2']} })
    sbe_id: Optional[int] = Field(default=None, description="""The number that identifies this schema between counterparties.""", ge=0, le=65535, json_schema_extra = { "linkml_meta": {'aliases': ['id'],
         'annotations': {'xsd_type': {'tag': 'xsd_type', 'value': 'xs:unsignedShort'}},
         'domain_of': ['SbeMessageSchemaV1',
                       'SbeBlockV1Mixin',
                       'SbeFieldV1',
                       'SbeMessageSchemaV2',
                       'SbeBlockV2Mixin',
                       'SbeFieldV2']} })
    schema_version: int = Field(default=..., description="""The version of this message schema, starting at zero.""", ge=0, json_schema_extra = { "linkml_meta": {'aliases': ['version'],
         'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '4: Schema versioning'},
                         'xsd_type': {'tag': 'xsd_type',
                                      'value': 'xs:nonNegativeInteger'}},
         'domain_of': ['SbeMessageSchemaV1', 'SbeMessageSchemaV2']} })
    semantic_version: Optional[str] = Field(default=None, description="""The version of FIX whose meanings this schema uses.""", json_schema_extra = { "linkml_meta": {'aliases': ['semanticVersion'],
         'domain_of': ['SbeMessageSchemaV1', 'SbeMessageSchemaV2']} })
    description: Optional[str] = Field(default=None, description="""Free text about this element, for the people who read the schema.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'domain_of': ['SbeValidValue',
                       'SbeChoice',
                       'SbeMessageSchemaV1',
                       'SbeEncodingV1',
                       'SbeBlockV1Mixin',
                       'SbeFieldV1',
                       'SbeMessageSchemaV2',
                       'SbeEncodingSetV2',
                       'SbeMessageSetV2',
                       'SbeElementV2',
                       'SbeBlockV2Mixin',
                       'SbeFieldV2'],
         'slot_uri': 'schema:description'} })
    byte_order: Optional[SbeByteOrder] = Field(default=SbeByteOrder("littleEndian"), description="""How the octets of every number in this schema's messages are ordered.""", json_schema_extra = { "linkml_meta": {'aliases': ['byteOrder'],
         'domain_of': ['SbeMessageSchemaV1', 'SbeMessageSchemaV2'],
         'ifabsent': 'string(littleEndian)'} })
    header_type: Optional[str] = Field(default="messageHeader", description="""The composite, by name, that sends each message's header in this schema.""", json_schema_extra = { "linkml_meta": {'aliases': ['headerType'],
         'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '3: Message header schema'}},
         'domain_of': ['SbeMessageSchemaV1', 'SbeMessageSchemaV2'],
         'ifabsent': 'string(messageHeader)'} })
    encoding_sets: list[SbeEncodingSetV1] = Field(default=..., description="""The sets of encodings this schema's messages use.""", min_length=1, json_schema_extra = { "linkml_meta": {'aliases': ['types'],
         'domain_of': ['SbeMessageSchemaV1', 'SbeMessageSchemaV2']} })
    messages: list[SbeMessageV1] = Field(default=..., description="""The message templates of this set.""", min_length=1, json_schema_extra = { "linkml_meta": {'aliases': ['message'], 'domain_of': ['SbeMessageSchemaV1', 'SbeMessageSetV2']} })

    @field_validator('header_type')
    def pattern_header_type(cls, v):
        pattern=re.compile(r"^[A-Za-z_][0-9A-Za-z_]{0,63}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid header_type format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid header_type format: {v}"
            raise ValueError(err_msg)
        return v


class SbeEncodingSetV1(ConfiguredBaseModel):
    """
    A set of encodings, listed in any order, whose names are unique across the whole schema.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'xml_element': {'tag': 'xml_element', 'value': 'types'}},
         'from_schema': 'https://w3id.org/lmodel/fix-sbe/schema/fix_sbe_v1_0',
         'slot_usage': {'encodings': {'name': 'encodings', 'range': 'SbeEncodingV1'}}})

    encodings: list[Union[SbeSimpleTypeV1,SbeCompositeV1,SbeEnumV1,SbeSetV1]] = Field(default=..., description="""The encodings of this set.""", min_length=1, json_schema_extra = { "linkml_meta": {'aliases': ['type', 'composite', 'enum', 'set'],
         'domain_of': ['SbeEncodingSetV1', 'SbeEncodingSetV2']} })


class SbeMemberV1(SbeVersionedMixin):
    """
    Anything a composite may hold in the order it is sent.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'abstract': True,
         'from_schema': 'https://w3id.org/lmodel/fix-sbe/schema/fix_sbe_v1_0',
         'mixins': ['SbeVersionedMixin']})

    encoding_kind: Literal["SbeMemberV1"] = Field(default="SbeMemberV1", description="""The class of this encoding or composite member, which stands for its XML element.""", json_schema_extra = { "linkml_meta": {'designates_type': True, 'domain_of': ['SbeMemberV1', 'SbeElementV2']} })
    symbolic_name: str = Field(default=..., description="""What the schema calls this element.""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['SbeValidValue',
                       'SbeChoice',
                       'SbeMemberV1',
                       'SbeBlockV1Mixin',
                       'SbeFieldV1',
                       'SbeElementV2',
                       'SbeBlockV2Mixin',
                       'SbeFieldV2']} })
    offset: Optional[int] = Field(default=None, description="""The octet this element starts at, counted from zero at the start of its block or composite.""", ge=0, le=4294967295, json_schema_extra = { "linkml_meta": {'aliases': ['offset'],
         'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '3: Field offset specified by '
                                                  'message schema'},
                         'xsd_type': {'tag': 'xsd_type', 'value': 'xs:unsignedInt'}},
         'domain_of': ['SbeMemberV1', 'SbeFieldV1', 'SbeMemberV2', 'SbeFieldV2']} })
    since_version: Optional[int] = Field(default=0, description="""The schema version that added this element.""", ge=0, json_schema_extra = { "linkml_meta": {'aliases': ['sinceVersion'],
         'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '5: Since version'},
                         'xsd_type': {'tag': 'xsd_type',
                                      'value': 'xs:nonNegativeInteger'}},
         'domain_of': ['SbeVersionedMixin'],
         'ifabsent': 'int(0)'} })
    deprecated_since: Optional[int] = Field(default=None, description="""The schema version that retired this element, which stays only for older applications.""", ge=0, json_schema_extra = { "linkml_meta": {'aliases': ['deprecated'],
         'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '5: Deprecated elements'},
                         'xsd_type': {'tag': 'xsd_type',
                                      'value': 'xs:nonNegativeInteger'}},
         'domain_of': ['SbeVersionedMixin']} })

    @field_validator('symbolic_name')
    def pattern_symbolic_name(cls, v):
        pattern=re.compile(r"^[A-Za-z_][0-9A-Za-z_]{0,63}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid symbolic_name format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid symbolic_name format: {v}"
            raise ValueError(err_msg)
        return v


class SbeRefV1(SbeMemberV1):
    """
    A composite's member that reuses an encoding defined elsewhere in the schema.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'xml_element': {'tag': 'xml_element', 'value': 'ref'},
                         'xsd_type': {'tag': 'xsd_type', 'value': 'refType'}},
         'from_schema': 'https://w3id.org/lmodel/fix-sbe/schema/fix_sbe_v1_0'})

    encoding_name: str = Field(default=..., description="""Which encoding this element uses, by name.""", json_schema_extra = { "linkml_meta": {'aliases': ['type'],
         'comments': ['It holds a name and not a class reference, because a name is '
                      'unique only within one schema document, where several documents '
                      'may be listed side by side. tests/sbe_rules.py holds each to an '
                      'encoding of its document.'],
         'domain_of': ['SbeRefV1', 'SbeFieldV1', 'SbeRefV2', 'SbeFieldV2']} })
    encoding_kind: Literal["SbeRefV1"] = Field(default="SbeRefV1", description="""The class of this encoding or composite member, which stands for its XML element.""", json_schema_extra = { "linkml_meta": {'designates_type': True, 'domain_of': ['SbeMemberV1', 'SbeElementV2']} })
    symbolic_name: str = Field(default=..., description="""What the schema calls this element.""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['SbeValidValue',
                       'SbeChoice',
                       'SbeMemberV1',
                       'SbeBlockV1Mixin',
                       'SbeFieldV1',
                       'SbeElementV2',
                       'SbeBlockV2Mixin',
                       'SbeFieldV2']} })
    offset: Optional[int] = Field(default=None, description="""The octet this element starts at, counted from zero at the start of its block or composite.""", ge=0, le=4294967295, json_schema_extra = { "linkml_meta": {'aliases': ['offset'],
         'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '3: Field offset specified by '
                                                  'message schema'},
                         'xsd_type': {'tag': 'xsd_type', 'value': 'xs:unsignedInt'}},
         'domain_of': ['SbeMemberV1', 'SbeFieldV1', 'SbeMemberV2', 'SbeFieldV2']} })
    since_version: Optional[int] = Field(default=0, description="""The schema version that added this element.""", ge=0, json_schema_extra = { "linkml_meta": {'aliases': ['sinceVersion'],
         'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '5: Since version'},
                         'xsd_type': {'tag': 'xsd_type',
                                      'value': 'xs:nonNegativeInteger'}},
         'domain_of': ['SbeVersionedMixin'],
         'ifabsent': 'int(0)'} })
    deprecated_since: Optional[int] = Field(default=None, description="""The schema version that retired this element, which stays only for older applications.""", ge=0, json_schema_extra = { "linkml_meta": {'aliases': ['deprecated'],
         'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '5: Deprecated elements'},
                         'xsd_type': {'tag': 'xsd_type',
                                      'value': 'xs:nonNegativeInteger'}},
         'domain_of': ['SbeVersionedMixin']} })

    @field_validator('encoding_name')
    def pattern_encoding_name(cls, v):
        pattern=re.compile(r"^[A-Za-z_][0-9A-Za-z_]{0,63}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid encoding_name format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid encoding_name format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('symbolic_name')
    def pattern_symbolic_name(cls, v):
        pattern=re.compile(r"^[A-Za-z_][0-9A-Za-z_]{0,63}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid symbolic_name format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid symbolic_name format: {v}"
            raise ValueError(err_msg)
        return v


class SbeEncodingV1(SbeMemberV1):
    """
    An encoding of SBE 1.0, which says how a value is laid out on the wire.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'abstract': True,
         'from_schema': 'https://w3id.org/lmodel/fix-sbe/schema/fix_sbe_v1_0',
         'slot_usage': {'semantic_type': {'description': 'The FIX datatype this '
                                                         'encoding carries.',
                                          'name': 'semantic_type'}}})

    semantic_type: Optional[str] = Field(default=None, description="""The FIX datatype this encoding carries.""", json_schema_extra = { "linkml_meta": {'aliases': ['semanticType'],
         'annotations': {'xsd_type': {'tag': 'xsd_type', 'value': 'xs:token'}},
         'domain_of': ['SbeEncodingV1',
                       'SbeBlockV1Mixin',
                       'SbeFieldV1',
                       'SbeBlockV2Mixin',
                       'SbeFieldV2']} })
    description: Optional[str] = Field(default=None, description="""Free text about this element, for the people who read the schema.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'domain_of': ['SbeValidValue',
                       'SbeChoice',
                       'SbeMessageSchemaV1',
                       'SbeEncodingV1',
                       'SbeBlockV1Mixin',
                       'SbeFieldV1',
                       'SbeMessageSchemaV2',
                       'SbeEncodingSetV2',
                       'SbeMessageSetV2',
                       'SbeElementV2',
                       'SbeBlockV2Mixin',
                       'SbeFieldV2'],
         'slot_uri': 'schema:description'} })
    encoding_kind: Literal["SbeEncodingV1"] = Field(default="SbeEncodingV1", description="""The class of this encoding or composite member, which stands for its XML element.""", json_schema_extra = { "linkml_meta": {'designates_type': True, 'domain_of': ['SbeMemberV1', 'SbeElementV2']} })
    symbolic_name: str = Field(default=..., description="""What the schema calls this element.""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['SbeValidValue',
                       'SbeChoice',
                       'SbeMemberV1',
                       'SbeBlockV1Mixin',
                       'SbeFieldV1',
                       'SbeElementV2',
                       'SbeBlockV2Mixin',
                       'SbeFieldV2']} })
    offset: Optional[int] = Field(default=None, description="""The octet this element starts at, counted from zero at the start of its block or composite.""", ge=0, le=4294967295, json_schema_extra = { "linkml_meta": {'aliases': ['offset'],
         'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '3: Field offset specified by '
                                                  'message schema'},
                         'xsd_type': {'tag': 'xsd_type', 'value': 'xs:unsignedInt'}},
         'domain_of': ['SbeMemberV1', 'SbeFieldV1', 'SbeMemberV2', 'SbeFieldV2']} })
    since_version: Optional[int] = Field(default=0, description="""The schema version that added this element.""", ge=0, json_schema_extra = { "linkml_meta": {'aliases': ['sinceVersion'],
         'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '5: Since version'},
                         'xsd_type': {'tag': 'xsd_type',
                                      'value': 'xs:nonNegativeInteger'}},
         'domain_of': ['SbeVersionedMixin'],
         'ifabsent': 'int(0)'} })
    deprecated_since: Optional[int] = Field(default=None, description="""The schema version that retired this element, which stays only for older applications.""", ge=0, json_schema_extra = { "linkml_meta": {'aliases': ['deprecated'],
         'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '5: Deprecated elements'},
                         'xsd_type': {'tag': 'xsd_type',
                                      'value': 'xs:nonNegativeInteger'}},
         'domain_of': ['SbeVersionedMixin']} })

    @field_validator('semantic_type')
    def pattern_semantic_type(cls, v):
        pattern=re.compile(r"^\S+( \S+)*$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid semantic_type format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid semantic_type format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('symbolic_name')
    def pattern_symbolic_name(cls, v):
        pattern=re.compile(r"^[A-Za-z_][0-9A-Za-z_]{0,63}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid symbolic_name format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid symbolic_name format: {v}"
            raise ValueError(err_msg)
        return v


class SbeSimpleTypeV1(SbeEncodingV1):
    """
    An encoding backed by one primitive value, or several in an array.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'xml_element': {'tag': 'xml_element', 'value': 'type'},
                         'xsd_type': {'tag': 'xsd_type', 'value': 'encodedDataType'}},
         'close_mappings': ['fix_orchestra:OrchestraDatatypeV10'],
         'from_schema': 'https://w3id.org/lmodel/fix-sbe/schema/fix_sbe_v1_0',
         'rules': [{'annotations': {'sbe_section': {'tag': 'sbe_section',
                                                    'value': '4: Field attributes'}},
                    'description': 'A value_ref is valid only on an element whose '
                                   'presence is constant.',
                    'postconditions': {'slot_conditions': {'presence': {'equals_string': 'constant',
                                                                        'name': 'presence'}}},
                    'preconditions': {'slot_conditions': {'value_ref': {'name': 'value_ref',
                                                                        'value_presence': 'PRESENT'}}},
                    'title': 'A reference to a value needs a constant'},
                   {'annotations': {'sbe_section': {'tag': 'sbe_section',
                                                    'value': '4: Schema validation'}},
                    'description': 'A null value cannot sit beside a presence of '
                                   'required.',
                    'postconditions': {'slot_conditions': {'null_value': {'name': 'null_value',
                                                                          'value_presence': 'ABSENT'}}},
                    'preconditions': {'slot_conditions': {'presence': {'equals_string': 'required',
                                                                       'name': 'presence'}}},
                    'title': 'A required value has no null'},
                   {'annotations': {'sbe_section': {'tag': 'sbe_section',
                                                    'value': '2: Common field schema '
                                                             'attributes'}},
                    'description': 'A null value cannot sit beside a presence of '
                                   'constant.',
                    'postconditions': {'slot_conditions': {'null_value': {'name': 'null_value',
                                                                          'value_presence': 'ABSENT'}}},
                    'preconditions': {'slot_conditions': {'presence': {'equals_string': 'constant',
                                                                       'name': 'presence'}}},
                    'title': 'A constant has no null'},
                   {'annotations': {'sbe_section': {'tag': 'sbe_section',
                                                    'value': '2: Common field schema '
                                                             'attributes'}},
                    'description': 'A lowest value cannot sit beside a presence of '
                                   'constant.',
                    'postconditions': {'slot_conditions': {'min_value': {'name': 'min_value',
                                                                         'value_presence': 'ABSENT'}}},
                    'preconditions': {'slot_conditions': {'presence': {'equals_string': 'constant',
                                                                       'name': 'presence'}}},
                    'title': 'A constant has no lowest value'},
                   {'annotations': {'sbe_section': {'tag': 'sbe_section',
                                                    'value': '2: Common field schema '
                                                             'attributes'}},
                    'description': 'A highest value cannot sit beside a presence of '
                                   'constant.',
                    'postconditions': {'slot_conditions': {'max_value': {'name': 'max_value',
                                                                         'value_presence': 'ABSENT'}}},
                    'preconditions': {'slot_conditions': {'presence': {'equals_string': 'constant',
                                                                       'name': 'presence'}}},
                    'title': 'A constant has no highest value'}]})

    element_value: Optional[str] = Field(default=None, description="""The text of the XML element, which is the constant when presence is constant.""", json_schema_extra = { "linkml_meta": {'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '4: Constant value'},
                         'xsd_type': {'tag': 'xsd_type', 'value': 'xs:token'}},
         'domain_of': ['SbeSimpleTypeV1',
                       'SbeSimpleTypeV2',
                       'SbeMemberTypeV2',
                       'SbeFieldV2']} })
    primitive_type: SbePrimitiveType = Field(default=..., description="""The wire type under this encoding.""", json_schema_extra = { "linkml_meta": {'aliases': ['primitiveType'],
         'domain_of': ['SbeSimpleTypeV1', 'SbeSimpleTypeV2', 'SbeMemberTypeV2']} })
    array_length: Optional[int] = Field(default=1, description="""How many values of the primitive type the encoding holds, where zero means a variable number.""", ge=0, json_schema_extra = { "linkml_meta": {'aliases': ['length'],
         'annotations': {'xsd_type': {'tag': 'xsd_type',
                                      'value': 'xs:nonNegativeInteger'}},
         'domain_of': ['SbeSimpleTypeV1', 'SbeSimpleTypeV2', 'SbeMemberTypeV2'],
         'ifabsent': 'int(1)'} })
    character_encoding: Optional[str] = Field(default=None, description="""Which character set, or which Unicode scheme, character data follows.""", json_schema_extra = { "linkml_meta": {'aliases': ['characterEncoding'],
         'domain_of': ['SbeSimpleTypeV1', 'SbeSimpleTypeV2', 'SbeMemberTypeV2']} })
    null_value: Optional[str] = Field(default=None, description="""The value that stands for null in place of the primitive type's default, written as text.""", json_schema_extra = { "linkml_meta": {'aliases': ['nullValue'],
         'domain_of': ['SbeSimpleTypeV1', 'SbeMemberTypeV2', 'SbeFieldV2']} })
    min_value: Optional[str] = Field(default=None, description="""The lowest value allowed, written as text.""", json_schema_extra = { "linkml_meta": {'aliases': ['minValue'],
         'domain_of': ['SbeSimpleTypeV1', 'SbeMemberTypeV2', 'SbeFieldV2']} })
    max_value: Optional[str] = Field(default=None, description="""The highest value allowed, written as text.""", json_schema_extra = { "linkml_meta": {'aliases': ['maxValue'],
         'domain_of': ['SbeSimpleTypeV1', 'SbeMemberTypeV2', 'SbeFieldV2']} })
    presence: Optional[SbePresence] = Field(default=SbePresence("required"), description="""Whether this element's value is required, optional or constant.""", json_schema_extra = { "linkml_meta": {'aliases': ['presence'],
         'domain_of': ['SbeSimpleTypeV1',
                       'SbeFieldV1',
                       'SbeMemberTypeV2',
                       'SbeFieldV2'],
         'ifabsent': 'string(required)'} })
    value_ref: Optional[str] = Field(default=None, description="""The valid value that gives a constant element its value.""", json_schema_extra = { "linkml_meta": {'aliases': ['valueRef'],
         'domain_of': ['SbeSimpleTypeV1',
                       'SbeFieldV1',
                       'SbeMemberTypeV2',
                       'SbeFieldV2']} })
    semantic_type: Optional[str] = Field(default=None, description="""The FIX datatype this encoding carries.""", json_schema_extra = { "linkml_meta": {'aliases': ['semanticType'],
         'annotations': {'xsd_type': {'tag': 'xsd_type', 'value': 'xs:token'}},
         'domain_of': ['SbeEncodingV1',
                       'SbeBlockV1Mixin',
                       'SbeFieldV1',
                       'SbeBlockV2Mixin',
                       'SbeFieldV2']} })
    description: Optional[str] = Field(default=None, description="""Free text about this element, for the people who read the schema.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'domain_of': ['SbeValidValue',
                       'SbeChoice',
                       'SbeMessageSchemaV1',
                       'SbeEncodingV1',
                       'SbeBlockV1Mixin',
                       'SbeFieldV1',
                       'SbeMessageSchemaV2',
                       'SbeEncodingSetV2',
                       'SbeMessageSetV2',
                       'SbeElementV2',
                       'SbeBlockV2Mixin',
                       'SbeFieldV2'],
         'slot_uri': 'schema:description'} })
    encoding_kind: Literal["SbeSimpleTypeV1"] = Field(default="SbeSimpleTypeV1", description="""The class of this encoding or composite member, which stands for its XML element.""", json_schema_extra = { "linkml_meta": {'designates_type': True, 'domain_of': ['SbeMemberV1', 'SbeElementV2']} })
    symbolic_name: str = Field(default=..., description="""What the schema calls this element.""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['SbeValidValue',
                       'SbeChoice',
                       'SbeMemberV1',
                       'SbeBlockV1Mixin',
                       'SbeFieldV1',
                       'SbeElementV2',
                       'SbeBlockV2Mixin',
                       'SbeFieldV2']} })
    offset: Optional[int] = Field(default=None, description="""The octet this element starts at, counted from zero at the start of its block or composite.""", ge=0, le=4294967295, json_schema_extra = { "linkml_meta": {'aliases': ['offset'],
         'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '3: Field offset specified by '
                                                  'message schema'},
                         'xsd_type': {'tag': 'xsd_type', 'value': 'xs:unsignedInt'}},
         'domain_of': ['SbeMemberV1', 'SbeFieldV1', 'SbeMemberV2', 'SbeFieldV2']} })
    since_version: Optional[int] = Field(default=0, description="""The schema version that added this element.""", ge=0, json_schema_extra = { "linkml_meta": {'aliases': ['sinceVersion'],
         'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '5: Since version'},
                         'xsd_type': {'tag': 'xsd_type',
                                      'value': 'xs:nonNegativeInteger'}},
         'domain_of': ['SbeVersionedMixin'],
         'ifabsent': 'int(0)'} })
    deprecated_since: Optional[int] = Field(default=None, description="""The schema version that retired this element, which stays only for older applications.""", ge=0, json_schema_extra = { "linkml_meta": {'aliases': ['deprecated'],
         'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '5: Deprecated elements'},
                         'xsd_type': {'tag': 'xsd_type',
                                      'value': 'xs:nonNegativeInteger'}},
         'domain_of': ['SbeVersionedMixin']} })

    @field_validator('element_value')
    def pattern_element_value(cls, v):
        pattern=re.compile(r"^\S+( \S+)*$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid element_value format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid element_value format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('value_ref')
    def pattern_value_ref(cls, v):
        pattern=re.compile(r"^[A-Za-z_][0-9A-Za-z_]*\.[A-Za-z_][0-9A-Za-z_]*$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid value_ref format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid value_ref format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('semantic_type')
    def pattern_semantic_type(cls, v):
        pattern=re.compile(r"^\S+( \S+)*$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid semantic_type format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid semantic_type format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('symbolic_name')
    def pattern_symbolic_name(cls, v):
        pattern=re.compile(r"^[A-Za-z_][0-9A-Za-z_]{0,63}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid symbolic_name format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid symbolic_name format: {v}"
            raise ValueError(err_msg)
        return v


class SbeCompositeV1(SbeEncodingV1):
    """
    An encoding built from members sent one after another, such as a decimal's mantissa and exponent.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'xml_element': {'tag': 'xml_element', 'value': 'composite'},
                         'xsd_type': {'tag': 'xsd_type', 'value': 'compositeDataType'}},
         'close_mappings': ['fix_orchestra:OrchestraComponentV10'],
         'comments': ['The members keep one list because their order is the order on '
                      'the wire. Separate lists per kind of member could not say that '
                      'an enum comes between two types.'],
         'from_schema': 'https://w3id.org/lmodel/fix-sbe/schema/fix_sbe_v1_0',
         'slot_usage': {'composite_members': {'name': 'composite_members',
                                              'range': 'SbeMemberV1'}}})

    composite_members: list[Union[SbeRefV1,SbeSimpleTypeV1,SbeCompositeV1,SbeEnumV1,SbeSetV1]] = Field(default=..., description="""The members of this composite, in the order they are sent.""", min_length=1, json_schema_extra = { "linkml_meta": {'aliases': ['type', 'enum', 'set', 'composite', 'ref'],
         'domain_of': ['SbeCompositeV1', 'SbeCompositeV2']} })
    semantic_type: Optional[str] = Field(default=None, description="""The FIX datatype this encoding carries.""", json_schema_extra = { "linkml_meta": {'aliases': ['semanticType'],
         'annotations': {'xsd_type': {'tag': 'xsd_type', 'value': 'xs:token'}},
         'domain_of': ['SbeEncodingV1',
                       'SbeBlockV1Mixin',
                       'SbeFieldV1',
                       'SbeBlockV2Mixin',
                       'SbeFieldV2']} })
    description: Optional[str] = Field(default=None, description="""Free text about this element, for the people who read the schema.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'domain_of': ['SbeValidValue',
                       'SbeChoice',
                       'SbeMessageSchemaV1',
                       'SbeEncodingV1',
                       'SbeBlockV1Mixin',
                       'SbeFieldV1',
                       'SbeMessageSchemaV2',
                       'SbeEncodingSetV2',
                       'SbeMessageSetV2',
                       'SbeElementV2',
                       'SbeBlockV2Mixin',
                       'SbeFieldV2'],
         'slot_uri': 'schema:description'} })
    encoding_kind: Literal["SbeCompositeV1"] = Field(default="SbeCompositeV1", description="""The class of this encoding or composite member, which stands for its XML element.""", json_schema_extra = { "linkml_meta": {'designates_type': True, 'domain_of': ['SbeMemberV1', 'SbeElementV2']} })
    symbolic_name: str = Field(default=..., description="""What the schema calls this element.""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['SbeValidValue',
                       'SbeChoice',
                       'SbeMemberV1',
                       'SbeBlockV1Mixin',
                       'SbeFieldV1',
                       'SbeElementV2',
                       'SbeBlockV2Mixin',
                       'SbeFieldV2']} })
    offset: Optional[int] = Field(default=None, description="""The octet this element starts at, counted from zero at the start of its block or composite.""", ge=0, le=4294967295, json_schema_extra = { "linkml_meta": {'aliases': ['offset'],
         'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '3: Field offset specified by '
                                                  'message schema'},
                         'xsd_type': {'tag': 'xsd_type', 'value': 'xs:unsignedInt'}},
         'domain_of': ['SbeMemberV1', 'SbeFieldV1', 'SbeMemberV2', 'SbeFieldV2']} })
    since_version: Optional[int] = Field(default=0, description="""The schema version that added this element.""", ge=0, json_schema_extra = { "linkml_meta": {'aliases': ['sinceVersion'],
         'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '5: Since version'},
                         'xsd_type': {'tag': 'xsd_type',
                                      'value': 'xs:nonNegativeInteger'}},
         'domain_of': ['SbeVersionedMixin'],
         'ifabsent': 'int(0)'} })
    deprecated_since: Optional[int] = Field(default=None, description="""The schema version that retired this element, which stays only for older applications.""", ge=0, json_schema_extra = { "linkml_meta": {'aliases': ['deprecated'],
         'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '5: Deprecated elements'},
                         'xsd_type': {'tag': 'xsd_type',
                                      'value': 'xs:nonNegativeInteger'}},
         'domain_of': ['SbeVersionedMixin']} })

    @field_validator('semantic_type')
    def pattern_semantic_type(cls, v):
        pattern=re.compile(r"^\S+( \S+)*$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid semantic_type format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid semantic_type format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('symbolic_name')
    def pattern_symbolic_name(cls, v):
        pattern=re.compile(r"^[A-Za-z_][0-9A-Za-z_]{0,63}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid symbolic_name format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid symbolic_name format: {v}"
            raise ValueError(err_msg)
        return v


class SbeEnumV1(SbeEncodingV1):
    """
    An encoding whose value is one of a listed set of valid values.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'xml_element': {'tag': 'xml_element', 'value': 'enum'},
                         'xsd_type': {'tag': 'xsd_type', 'value': 'enumType'}},
         'close_mappings': ['fix_orchestra:OrchestraCodeSetV10'],
         'from_schema': 'https://w3id.org/lmodel/fix-sbe/schema/fix_sbe_v1_0'})

    encoding_type: str = Field(default=..., description="""The simple encoding or primitive type that an enumeration or set is sent as.""", json_schema_extra = { "linkml_meta": {'aliases': ['encodingType'],
         'domain_of': ['SbeEnumV1', 'SbeSetV1', 'SbeEnumV2', 'SbeSetV2']} })
    valid_values: list[SbeValidValue] = Field(default=..., description="""The values this enumeration allows.""", min_length=1, json_schema_extra = { "linkml_meta": {'aliases': ['validValue'], 'domain_of': ['SbeEnumV1', 'SbeEnumV2']} })
    semantic_type: Optional[str] = Field(default=None, description="""The FIX datatype this encoding carries.""", json_schema_extra = { "linkml_meta": {'aliases': ['semanticType'],
         'annotations': {'xsd_type': {'tag': 'xsd_type', 'value': 'xs:token'}},
         'domain_of': ['SbeEncodingV1',
                       'SbeBlockV1Mixin',
                       'SbeFieldV1',
                       'SbeBlockV2Mixin',
                       'SbeFieldV2']} })
    description: Optional[str] = Field(default=None, description="""Free text about this element, for the people who read the schema.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'domain_of': ['SbeValidValue',
                       'SbeChoice',
                       'SbeMessageSchemaV1',
                       'SbeEncodingV1',
                       'SbeBlockV1Mixin',
                       'SbeFieldV1',
                       'SbeMessageSchemaV2',
                       'SbeEncodingSetV2',
                       'SbeMessageSetV2',
                       'SbeElementV2',
                       'SbeBlockV2Mixin',
                       'SbeFieldV2'],
         'slot_uri': 'schema:description'} })
    encoding_kind: Literal["SbeEnumV1"] = Field(default="SbeEnumV1", description="""The class of this encoding or composite member, which stands for its XML element.""", json_schema_extra = { "linkml_meta": {'designates_type': True, 'domain_of': ['SbeMemberV1', 'SbeElementV2']} })
    symbolic_name: str = Field(default=..., description="""What the schema calls this element.""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['SbeValidValue',
                       'SbeChoice',
                       'SbeMemberV1',
                       'SbeBlockV1Mixin',
                       'SbeFieldV1',
                       'SbeElementV2',
                       'SbeBlockV2Mixin',
                       'SbeFieldV2']} })
    offset: Optional[int] = Field(default=None, description="""The octet this element starts at, counted from zero at the start of its block or composite.""", ge=0, le=4294967295, json_schema_extra = { "linkml_meta": {'aliases': ['offset'],
         'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '3: Field offset specified by '
                                                  'message schema'},
                         'xsd_type': {'tag': 'xsd_type', 'value': 'xs:unsignedInt'}},
         'domain_of': ['SbeMemberV1', 'SbeFieldV1', 'SbeMemberV2', 'SbeFieldV2']} })
    since_version: Optional[int] = Field(default=0, description="""The schema version that added this element.""", ge=0, json_schema_extra = { "linkml_meta": {'aliases': ['sinceVersion'],
         'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '5: Since version'},
                         'xsd_type': {'tag': 'xsd_type',
                                      'value': 'xs:nonNegativeInteger'}},
         'domain_of': ['SbeVersionedMixin'],
         'ifabsent': 'int(0)'} })
    deprecated_since: Optional[int] = Field(default=None, description="""The schema version that retired this element, which stays only for older applications.""", ge=0, json_schema_extra = { "linkml_meta": {'aliases': ['deprecated'],
         'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '5: Deprecated elements'},
                         'xsd_type': {'tag': 'xsd_type',
                                      'value': 'xs:nonNegativeInteger'}},
         'domain_of': ['SbeVersionedMixin']} })

    @field_validator('encoding_type')
    def pattern_encoding_type(cls, v):
        pattern=re.compile(r"^[A-Za-z_][0-9A-Za-z_]{0,63}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid encoding_type format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid encoding_type format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('semantic_type')
    def pattern_semantic_type(cls, v):
        pattern=re.compile(r"^\S+( \S+)*$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid semantic_type format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid semantic_type format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('symbolic_name')
    def pattern_symbolic_name(cls, v):
        pattern=re.compile(r"^[A-Za-z_][0-9A-Za-z_]{0,63}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid symbolic_name format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid symbolic_name format: {v}"
            raise ValueError(err_msg)
        return v


class SbeSetV1(SbeEncodingV1):
    """
    An encoding whose value is any combination of up to 64 choices, sent as a bitset.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'xml_element': {'tag': 'xml_element', 'value': 'set'},
                         'xsd_type': {'tag': 'xsd_type', 'value': 'setType'}},
         'comments': ["FIX's transposer does not carry a set to Orchestra, so the "
                      "mapping is related. FIX's MultipleCharValue and "
                      'MultipleStringValue fields hold such choices in a code set.'],
         'from_schema': 'https://w3id.org/lmodel/fix-sbe/schema/fix_sbe_v1_0',
         'related_mappings': ['fix_orchestra:OrchestraCodeSetV10']})

    encoding_type: str = Field(default=..., description="""The simple encoding or primitive type that an enumeration or set is sent as.""", json_schema_extra = { "linkml_meta": {'aliases': ['encodingType'],
         'domain_of': ['SbeEnumV1', 'SbeSetV1', 'SbeEnumV2', 'SbeSetV2']} })
    choices: list[SbeChoice] = Field(default=..., description="""The alternatives of this set.""", min_length=1, max_length=64, json_schema_extra = { "linkml_meta": {'aliases': ['choice'], 'domain_of': ['SbeSetV1', 'SbeSetV2']} })
    semantic_type: Optional[str] = Field(default=None, description="""The FIX datatype this encoding carries.""", json_schema_extra = { "linkml_meta": {'aliases': ['semanticType'],
         'annotations': {'xsd_type': {'tag': 'xsd_type', 'value': 'xs:token'}},
         'domain_of': ['SbeEncodingV1',
                       'SbeBlockV1Mixin',
                       'SbeFieldV1',
                       'SbeBlockV2Mixin',
                       'SbeFieldV2']} })
    description: Optional[str] = Field(default=None, description="""Free text about this element, for the people who read the schema.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'domain_of': ['SbeValidValue',
                       'SbeChoice',
                       'SbeMessageSchemaV1',
                       'SbeEncodingV1',
                       'SbeBlockV1Mixin',
                       'SbeFieldV1',
                       'SbeMessageSchemaV2',
                       'SbeEncodingSetV2',
                       'SbeMessageSetV2',
                       'SbeElementV2',
                       'SbeBlockV2Mixin',
                       'SbeFieldV2'],
         'slot_uri': 'schema:description'} })
    encoding_kind: Literal["SbeSetV1"] = Field(default="SbeSetV1", description="""The class of this encoding or composite member, which stands for its XML element.""", json_schema_extra = { "linkml_meta": {'designates_type': True, 'domain_of': ['SbeMemberV1', 'SbeElementV2']} })
    symbolic_name: str = Field(default=..., description="""What the schema calls this element.""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['SbeValidValue',
                       'SbeChoice',
                       'SbeMemberV1',
                       'SbeBlockV1Mixin',
                       'SbeFieldV1',
                       'SbeElementV2',
                       'SbeBlockV2Mixin',
                       'SbeFieldV2']} })
    offset: Optional[int] = Field(default=None, description="""The octet this element starts at, counted from zero at the start of its block or composite.""", ge=0, le=4294967295, json_schema_extra = { "linkml_meta": {'aliases': ['offset'],
         'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '3: Field offset specified by '
                                                  'message schema'},
                         'xsd_type': {'tag': 'xsd_type', 'value': 'xs:unsignedInt'}},
         'domain_of': ['SbeMemberV1', 'SbeFieldV1', 'SbeMemberV2', 'SbeFieldV2']} })
    since_version: Optional[int] = Field(default=0, description="""The schema version that added this element.""", ge=0, json_schema_extra = { "linkml_meta": {'aliases': ['sinceVersion'],
         'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '5: Since version'},
                         'xsd_type': {'tag': 'xsd_type',
                                      'value': 'xs:nonNegativeInteger'}},
         'domain_of': ['SbeVersionedMixin'],
         'ifabsent': 'int(0)'} })
    deprecated_since: Optional[int] = Field(default=None, description="""The schema version that retired this element, which stays only for older applications.""", ge=0, json_schema_extra = { "linkml_meta": {'aliases': ['deprecated'],
         'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '5: Deprecated elements'},
                         'xsd_type': {'tag': 'xsd_type',
                                      'value': 'xs:nonNegativeInteger'}},
         'domain_of': ['SbeVersionedMixin']} })

    @field_validator('encoding_type')
    def pattern_encoding_type(cls, v):
        pattern=re.compile(r"^[A-Za-z_][0-9A-Za-z_]{0,63}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid encoding_type format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid encoding_type format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('semantic_type')
    def pattern_semantic_type(cls, v):
        pattern=re.compile(r"^\S+( \S+)*$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid semantic_type format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid semantic_type format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('symbolic_name')
    def pattern_symbolic_name(cls, v):
        pattern=re.compile(r"^[A-Za-z_][0-9A-Za-z_]{0,63}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid symbolic_name format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid symbolic_name format: {v}"
            raise ValueError(err_msg)
        return v


class SbeBlockV1Mixin(ConfiguredBaseModel):
    """
    The body shared by a message and a group entry, which holds its fixed-length fields first, then groups, then variable-length data.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/lmodel/fix-sbe/schema/fix_sbe_v1_0',
         'mixin': True,
         'slot_usage': {'block_fields': {'name': 'block_fields', 'range': 'SbeFieldV1'},
                        'repeating_groups': {'name': 'repeating_groups',
                                             'range': 'SbeGroupV1'},
                        'sbe_id': {'name': 'sbe_id', 'required': True},
                        'var_data_fields': {'name': 'var_data_fields',
                                            'range': 'SbeFieldV1'}}})

    symbolic_name: str = Field(default=..., description="""What the schema calls this element.""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['SbeValidValue',
                       'SbeChoice',
                       'SbeMemberV1',
                       'SbeBlockV1Mixin',
                       'SbeFieldV1',
                       'SbeElementV2',
                       'SbeBlockV2Mixin',
                       'SbeFieldV2']} })
    sbe_id: int = Field(default=..., description="""The number that identifies this element.""", ge=0, le=65535, json_schema_extra = { "linkml_meta": {'aliases': ['id'],
         'annotations': {'xsd_type': {'tag': 'xsd_type', 'value': 'xs:unsignedShort'}},
         'domain_of': ['SbeMessageSchemaV1',
                       'SbeBlockV1Mixin',
                       'SbeFieldV1',
                       'SbeMessageSchemaV2',
                       'SbeBlockV2Mixin',
                       'SbeFieldV2']} })
    block_length: Optional[int] = Field(default=None, description="""The octets set aside for a message's fixed-length fields, or for those of each group entry.""", ge=0, json_schema_extra = { "linkml_meta": {'aliases': ['blockLength'],
         'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '3: Root block length'},
                         'xsd_type': {'tag': 'xsd_type',
                                      'value': 'xs:nonNegativeInteger'}},
         'domain_of': ['SbeBlockV1Mixin', 'SbeBlockV2Mixin']} })
    semantic_type: Optional[str] = Field(default=None, description="""What this element means at the FIX application layer.""", json_schema_extra = { "linkml_meta": {'aliases': ['semanticType'],
         'annotations': {'xsd_type': {'tag': 'xsd_type', 'value': 'xs:token'}},
         'domain_of': ['SbeEncodingV1',
                       'SbeBlockV1Mixin',
                       'SbeFieldV1',
                       'SbeBlockV2Mixin',
                       'SbeFieldV2']} })
    description: Optional[str] = Field(default=None, description="""Free text about this element, for the people who read the schema.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'domain_of': ['SbeValidValue',
                       'SbeChoice',
                       'SbeMessageSchemaV1',
                       'SbeEncodingV1',
                       'SbeBlockV1Mixin',
                       'SbeFieldV1',
                       'SbeMessageSchemaV2',
                       'SbeEncodingSetV2',
                       'SbeMessageSetV2',
                       'SbeElementV2',
                       'SbeBlockV2Mixin',
                       'SbeFieldV2'],
         'slot_uri': 'schema:description'} })
    block_fields: Optional[list[SbeFieldV1]] = Field(default=None, description="""Fixed-length fields, listed in wire order.""", json_schema_extra = { "linkml_meta": {'aliases': ['field'], 'domain_of': ['SbeBlockV1Mixin', 'SbeBlockV2Mixin']} })
    repeating_groups: Optional[list[SbeGroupV1]] = Field(default=None, description="""Repeating groups, listed in wire order.""", json_schema_extra = { "linkml_meta": {'aliases': ['group'], 'domain_of': ['SbeBlockV1Mixin', 'SbeBlockV2Mixin']} })
    var_data_fields: Optional[list[SbeFieldV1]] = Field(default=None, description="""Variable-length fields, listed in wire order.""", json_schema_extra = { "linkml_meta": {'aliases': ['data'], 'domain_of': ['SbeBlockV1Mixin', 'SbeBlockV2Mixin']} })

    @field_validator('symbolic_name')
    def pattern_symbolic_name(cls, v):
        pattern=re.compile(r"^[A-Za-z_][0-9A-Za-z_]{0,63}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid symbolic_name format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid symbolic_name format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('semantic_type')
    def pattern_semantic_type(cls, v):
        pattern=re.compile(r"^\S+( \S+)*$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid semantic_type format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid semantic_type format: {v}"
            raise ValueError(err_msg)
        return v


class SbeMessageV1(SbeBlockV1Mixin, SbeVersionedMixin):
    """
    A message template, whose number and block length are sent in each message's header.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'xml_element': {'tag': 'xml_element', 'value': 'message'},
                         'xsd_type': {'tag': 'xsd_type', 'value': 'blockType'}},
         'close_mappings': ['fix_orchestra:OrchestraMessageV10'],
         'from_schema': 'https://w3id.org/lmodel/fix-sbe/schema/fix_sbe_v1_0',
         'mixins': ['SbeVersionedMixin', 'SbeBlockV1Mixin'],
         'slot_usage': {'sbe_id': {'description': "The template's number, which no "
                                                  'other template in the schema '
                                                  'shares.',
                                   'name': 'sbe_id'},
                        'semantic_type': {'description': 'The FIX MsgType(35) this '
                                                         'template stands for, where '
                                                         'several templates may share '
                                                         'one.',
                                          'name': 'semantic_type'}}})

    since_version: Optional[int] = Field(default=0, description="""The schema version that added this element.""", ge=0, json_schema_extra = { "linkml_meta": {'aliases': ['sinceVersion'],
         'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '5: Since version'},
                         'xsd_type': {'tag': 'xsd_type',
                                      'value': 'xs:nonNegativeInteger'}},
         'domain_of': ['SbeVersionedMixin'],
         'ifabsent': 'int(0)'} })
    deprecated_since: Optional[int] = Field(default=None, description="""The schema version that retired this element, which stays only for older applications.""", ge=0, json_schema_extra = { "linkml_meta": {'aliases': ['deprecated'],
         'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '5: Deprecated elements'},
                         'xsd_type': {'tag': 'xsd_type',
                                      'value': 'xs:nonNegativeInteger'}},
         'domain_of': ['SbeVersionedMixin']} })
    symbolic_name: str = Field(default=..., description="""What the schema calls this element.""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['SbeValidValue',
                       'SbeChoice',
                       'SbeMemberV1',
                       'SbeBlockV1Mixin',
                       'SbeFieldV1',
                       'SbeElementV2',
                       'SbeBlockV2Mixin',
                       'SbeFieldV2']} })
    sbe_id: int = Field(default=..., description="""The template's number, which no other template in the schema shares.""", ge=0, le=65535, json_schema_extra = { "linkml_meta": {'aliases': ['id'],
         'annotations': {'xsd_type': {'tag': 'xsd_type', 'value': 'xs:unsignedShort'}},
         'domain_of': ['SbeMessageSchemaV1',
                       'SbeBlockV1Mixin',
                       'SbeFieldV1',
                       'SbeMessageSchemaV2',
                       'SbeBlockV2Mixin',
                       'SbeFieldV2']} })
    block_length: Optional[int] = Field(default=None, description="""The octets set aside for a message's fixed-length fields, or for those of each group entry.""", ge=0, json_schema_extra = { "linkml_meta": {'aliases': ['blockLength'],
         'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '3: Root block length'},
                         'xsd_type': {'tag': 'xsd_type',
                                      'value': 'xs:nonNegativeInteger'}},
         'domain_of': ['SbeBlockV1Mixin', 'SbeBlockV2Mixin']} })
    semantic_type: Optional[str] = Field(default=None, description="""The FIX MsgType(35) this template stands for, where several templates may share one.""", json_schema_extra = { "linkml_meta": {'aliases': ['semanticType'],
         'annotations': {'xsd_type': {'tag': 'xsd_type', 'value': 'xs:token'}},
         'domain_of': ['SbeEncodingV1',
                       'SbeBlockV1Mixin',
                       'SbeFieldV1',
                       'SbeBlockV2Mixin',
                       'SbeFieldV2']} })
    description: Optional[str] = Field(default=None, description="""Free text about this element, for the people who read the schema.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'domain_of': ['SbeValidValue',
                       'SbeChoice',
                       'SbeMessageSchemaV1',
                       'SbeEncodingV1',
                       'SbeBlockV1Mixin',
                       'SbeFieldV1',
                       'SbeMessageSchemaV2',
                       'SbeEncodingSetV2',
                       'SbeMessageSetV2',
                       'SbeElementV2',
                       'SbeBlockV2Mixin',
                       'SbeFieldV2'],
         'slot_uri': 'schema:description'} })
    block_fields: Optional[list[SbeFieldV1]] = Field(default=None, description="""Fixed-length fields, listed in wire order.""", json_schema_extra = { "linkml_meta": {'aliases': ['field'], 'domain_of': ['SbeBlockV1Mixin', 'SbeBlockV2Mixin']} })
    repeating_groups: Optional[list[SbeGroupV1]] = Field(default=None, description="""Repeating groups, listed in wire order.""", json_schema_extra = { "linkml_meta": {'aliases': ['group'], 'domain_of': ['SbeBlockV1Mixin', 'SbeBlockV2Mixin']} })
    var_data_fields: Optional[list[SbeFieldV1]] = Field(default=None, description="""Variable-length fields, listed in wire order.""", json_schema_extra = { "linkml_meta": {'aliases': ['data'], 'domain_of': ['SbeBlockV1Mixin', 'SbeBlockV2Mixin']} })

    @field_validator('symbolic_name')
    def pattern_symbolic_name(cls, v):
        pattern=re.compile(r"^[A-Za-z_][0-9A-Za-z_]{0,63}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid symbolic_name format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid symbolic_name format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('semantic_type')
    def pattern_semantic_type(cls, v):
        pattern=re.compile(r"^\S+( \S+)*$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid semantic_type format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid semantic_type format: {v}"
            raise ValueError(err_msg)
        return v


class SbeGroupV1(SbeBlockV1Mixin, SbeVersionedMixin):
    """
    A repeating group, whose entries each hold the same fields, and which cannot be without a field.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'xml_element': {'tag': 'xml_element', 'value': 'group'},
                         'xsd_type': {'tag': 'xsd_type', 'value': 'groupType'}},
         'close_mappings': ['fix_orchestra:OrchestraGroupV10'],
         'from_schema': 'https://w3id.org/lmodel/fix-sbe/schema/fix_sbe_v1_0',
         'mixins': ['SbeVersionedMixin', 'SbeBlockV1Mixin'],
         'slot_usage': {'block_fields': {'minimum_cardinality': 1,
                                         'name': 'block_fields',
                                         'required': True}}})

    dimension_type: Optional[str] = Field(default="groupSizeEncoding", description="""The composite, by name, that sends a repeating group's entry count and entry size.""", json_schema_extra = { "linkml_meta": {'aliases': ['dimensionType'],
         'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '3: Encoding of repeating group '
                                                  'dimensions'}},
         'domain_of': ['SbeGroupV1', 'SbeGroupV2'],
         'ifabsent': 'string(groupSizeEncoding)'} })
    since_version: Optional[int] = Field(default=0, description="""The schema version that added this element.""", ge=0, json_schema_extra = { "linkml_meta": {'aliases': ['sinceVersion'],
         'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '5: Since version'},
                         'xsd_type': {'tag': 'xsd_type',
                                      'value': 'xs:nonNegativeInteger'}},
         'domain_of': ['SbeVersionedMixin'],
         'ifabsent': 'int(0)'} })
    deprecated_since: Optional[int] = Field(default=None, description="""The schema version that retired this element, which stays only for older applications.""", ge=0, json_schema_extra = { "linkml_meta": {'aliases': ['deprecated'],
         'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '5: Deprecated elements'},
                         'xsd_type': {'tag': 'xsd_type',
                                      'value': 'xs:nonNegativeInteger'}},
         'domain_of': ['SbeVersionedMixin']} })
    symbolic_name: str = Field(default=..., description="""What the schema calls this element.""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['SbeValidValue',
                       'SbeChoice',
                       'SbeMemberV1',
                       'SbeBlockV1Mixin',
                       'SbeFieldV1',
                       'SbeElementV2',
                       'SbeBlockV2Mixin',
                       'SbeFieldV2']} })
    sbe_id: int = Field(default=..., description="""The number that identifies this element.""", ge=0, le=65535, json_schema_extra = { "linkml_meta": {'aliases': ['id'],
         'annotations': {'xsd_type': {'tag': 'xsd_type', 'value': 'xs:unsignedShort'}},
         'domain_of': ['SbeMessageSchemaV1',
                       'SbeBlockV1Mixin',
                       'SbeFieldV1',
                       'SbeMessageSchemaV2',
                       'SbeBlockV2Mixin',
                       'SbeFieldV2']} })
    block_length: Optional[int] = Field(default=None, description="""The octets set aside for a message's fixed-length fields, or for those of each group entry.""", ge=0, json_schema_extra = { "linkml_meta": {'aliases': ['blockLength'],
         'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '3: Root block length'},
                         'xsd_type': {'tag': 'xsd_type',
                                      'value': 'xs:nonNegativeInteger'}},
         'domain_of': ['SbeBlockV1Mixin', 'SbeBlockV2Mixin']} })
    semantic_type: Optional[str] = Field(default=None, description="""What this element means at the FIX application layer.""", json_schema_extra = { "linkml_meta": {'aliases': ['semanticType'],
         'annotations': {'xsd_type': {'tag': 'xsd_type', 'value': 'xs:token'}},
         'domain_of': ['SbeEncodingV1',
                       'SbeBlockV1Mixin',
                       'SbeFieldV1',
                       'SbeBlockV2Mixin',
                       'SbeFieldV2']} })
    description: Optional[str] = Field(default=None, description="""Free text about this element, for the people who read the schema.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'domain_of': ['SbeValidValue',
                       'SbeChoice',
                       'SbeMessageSchemaV1',
                       'SbeEncodingV1',
                       'SbeBlockV1Mixin',
                       'SbeFieldV1',
                       'SbeMessageSchemaV2',
                       'SbeEncodingSetV2',
                       'SbeMessageSetV2',
                       'SbeElementV2',
                       'SbeBlockV2Mixin',
                       'SbeFieldV2'],
         'slot_uri': 'schema:description'} })
    block_fields: list[SbeFieldV1] = Field(default=..., description="""Fixed-length fields, listed in wire order.""", min_length=1, json_schema_extra = { "linkml_meta": {'aliases': ['field'], 'domain_of': ['SbeBlockV1Mixin', 'SbeBlockV2Mixin']} })
    repeating_groups: Optional[list[SbeGroupV1]] = Field(default=None, description="""Repeating groups, listed in wire order.""", json_schema_extra = { "linkml_meta": {'aliases': ['group'], 'domain_of': ['SbeBlockV1Mixin', 'SbeBlockV2Mixin']} })
    var_data_fields: Optional[list[SbeFieldV1]] = Field(default=None, description="""Variable-length fields, listed in wire order.""", json_schema_extra = { "linkml_meta": {'aliases': ['data'], 'domain_of': ['SbeBlockV1Mixin', 'SbeBlockV2Mixin']} })

    @field_validator('dimension_type')
    def pattern_dimension_type(cls, v):
        pattern=re.compile(r"^[A-Za-z_][0-9A-Za-z_]{0,63}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid dimension_type format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid dimension_type format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('symbolic_name')
    def pattern_symbolic_name(cls, v):
        pattern=re.compile(r"^[A-Za-z_][0-9A-Za-z_]{0,63}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid symbolic_name format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid symbolic_name format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('semantic_type')
    def pattern_semantic_type(cls, v):
        pattern=re.compile(r"^\S+( \S+)*$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid semantic_type format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid semantic_type format: {v}"
            raise ValueError(err_msg)
        return v


class SbeFieldV1(SbeVersionedMixin):
    """
    A message's or group entry's field, which uses an encoding at a place in its block.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'xml_element': {'tag': 'xml_element', 'value': 'field'},
                         'xsd_type': {'tag': 'xsd_type', 'value': 'fieldType'}},
         'close_mappings': ['fix_orchestra:OrchestraFieldV10'],
         'comments': ['The old mapping called this an exact match of an Orchestra '
                      'field, but the two differ. This one sits at a place in one '
                      "block, and FIX's transposer carries one with a composite "
                      'encoding to a component reference, not a field.'],
         'from_schema': 'https://w3id.org/lmodel/fix-sbe/schema/fix_sbe_v1_0',
         'mixins': ['SbeVersionedMixin'],
         'rules': [{'annotations': {'sbe_section': {'tag': 'sbe_section',
                                                    'value': '4: Field attributes'}},
                    'description': 'A value_ref is valid only on an element whose '
                                   'presence is constant.',
                    'postconditions': {'slot_conditions': {'presence': {'equals_string': 'constant',
                                                                        'name': 'presence'}}},
                    'preconditions': {'slot_conditions': {'value_ref': {'name': 'value_ref',
                                                                        'value_presence': 'PRESENT'}}},
                    'title': 'A reference to a value needs a constant'}],
         'slot_usage': {'sbe_id': {'description': "The field's FIX tag number.",
                                   'name': 'sbe_id',
                                   'required': True},
                        'semantic_type': {'description': 'The FIX datatype this field '
                                                         'carries.',
                                          'name': 'semantic_type'}}})

    symbolic_name: str = Field(default=..., description="""What the schema calls this element.""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['SbeValidValue',
                       'SbeChoice',
                       'SbeMemberV1',
                       'SbeBlockV1Mixin',
                       'SbeFieldV1',
                       'SbeElementV2',
                       'SbeBlockV2Mixin',
                       'SbeFieldV2']} })
    sbe_id: int = Field(default=..., description="""The field's FIX tag number.""", ge=0, le=65535, json_schema_extra = { "linkml_meta": {'aliases': ['id'],
         'annotations': {'xsd_type': {'tag': 'xsd_type', 'value': 'xs:unsignedShort'}},
         'domain_of': ['SbeMessageSchemaV1',
                       'SbeBlockV1Mixin',
                       'SbeFieldV1',
                       'SbeMessageSchemaV2',
                       'SbeBlockV2Mixin',
                       'SbeFieldV2']} })
    encoding_name: str = Field(default=..., description="""Which encoding this element uses, by name.""", json_schema_extra = { "linkml_meta": {'aliases': ['type'],
         'comments': ['It holds a name and not a class reference, because a name is '
                      'unique only within one schema document, where several documents '
                      'may be listed side by side. tests/sbe_rules.py holds each to an '
                      'encoding of its document.'],
         'domain_of': ['SbeRefV1', 'SbeFieldV1', 'SbeRefV2', 'SbeFieldV2']} })
    offset: Optional[int] = Field(default=None, description="""The octet this element starts at, counted from zero at the start of its block or composite.""", ge=0, le=4294967295, json_schema_extra = { "linkml_meta": {'aliases': ['offset'],
         'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '3: Field offset specified by '
                                                  'message schema'},
                         'xsd_type': {'tag': 'xsd_type', 'value': 'xs:unsignedInt'}},
         'domain_of': ['SbeMemberV1', 'SbeFieldV1', 'SbeMemberV2', 'SbeFieldV2']} })
    presence: Optional[SbePresence] = Field(default=SbePresence("required"), description="""Whether this element's value is required, optional or constant.""", json_schema_extra = { "linkml_meta": {'aliases': ['presence'],
         'domain_of': ['SbeSimpleTypeV1',
                       'SbeFieldV1',
                       'SbeMemberTypeV2',
                       'SbeFieldV2'],
         'ifabsent': 'string(required)'} })
    value_ref: Optional[str] = Field(default=None, description="""The valid value that gives a constant element its value.""", json_schema_extra = { "linkml_meta": {'aliases': ['valueRef'],
         'domain_of': ['SbeSimpleTypeV1',
                       'SbeFieldV1',
                       'SbeMemberTypeV2',
                       'SbeFieldV2']} })
    semantic_type: Optional[str] = Field(default=None, description="""The FIX datatype this field carries.""", json_schema_extra = { "linkml_meta": {'aliases': ['semanticType'],
         'annotations': {'xsd_type': {'tag': 'xsd_type', 'value': 'xs:token'}},
         'domain_of': ['SbeEncodingV1',
                       'SbeBlockV1Mixin',
                       'SbeFieldV1',
                       'SbeBlockV2Mixin',
                       'SbeFieldV2']} })
    description: Optional[str] = Field(default=None, description="""Free text about this element, for the people who read the schema.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'domain_of': ['SbeValidValue',
                       'SbeChoice',
                       'SbeMessageSchemaV1',
                       'SbeEncodingV1',
                       'SbeBlockV1Mixin',
                       'SbeFieldV1',
                       'SbeMessageSchemaV2',
                       'SbeEncodingSetV2',
                       'SbeMessageSetV2',
                       'SbeElementV2',
                       'SbeBlockV2Mixin',
                       'SbeFieldV2'],
         'slot_uri': 'schema:description'} })
    time_epoch: Optional[str] = Field(default="unix", description="""Where the period a time value counts from begins.""", json_schema_extra = { "linkml_meta": {'aliases': ['epoch'],
         'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '2: Date and time encoding'}},
         'domain_of': ['SbeFieldV1'],
         'ifabsent': 'string(unix)'} })
    time_unit: Optional[str] = Field(default="nanosecond", description="""The unit of a time value.""", json_schema_extra = { "linkml_meta": {'aliases': ['timeUnit'],
         'deprecated': 'The XSD keeps this only for schemas written against release '
                       'candidate 2 of SBE 1.0.',
         'domain_of': ['SbeFieldV1'],
         'ifabsent': 'string(nanosecond)'} })
    since_version: Optional[int] = Field(default=0, description="""The schema version that added this element.""", ge=0, json_schema_extra = { "linkml_meta": {'aliases': ['sinceVersion'],
         'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '5: Since version'},
                         'xsd_type': {'tag': 'xsd_type',
                                      'value': 'xs:nonNegativeInteger'}},
         'domain_of': ['SbeVersionedMixin'],
         'ifabsent': 'int(0)'} })
    deprecated_since: Optional[int] = Field(default=None, description="""The schema version that retired this element, which stays only for older applications.""", ge=0, json_schema_extra = { "linkml_meta": {'aliases': ['deprecated'],
         'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '5: Deprecated elements'},
                         'xsd_type': {'tag': 'xsd_type',
                                      'value': 'xs:nonNegativeInteger'}},
         'domain_of': ['SbeVersionedMixin']} })

    @field_validator('symbolic_name')
    def pattern_symbolic_name(cls, v):
        pattern=re.compile(r"^[A-Za-z_][0-9A-Za-z_]{0,63}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid symbolic_name format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid symbolic_name format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('encoding_name')
    def pattern_encoding_name(cls, v):
        pattern=re.compile(r"^[A-Za-z_][0-9A-Za-z_]{0,63}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid encoding_name format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid encoding_name format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('value_ref')
    def pattern_value_ref(cls, v):
        pattern=re.compile(r"^[A-Za-z_][0-9A-Za-z_]*\.[A-Za-z_][0-9A-Za-z_]*$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid value_ref format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid value_ref format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('semantic_type')
    def pattern_semantic_type(cls, v):
        pattern=re.compile(r"^\S+( \S+)*$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid semantic_type format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid semantic_type format: {v}"
            raise ValueError(err_msg)
        return v


class SbeMessageSchemaV2(ConfiguredBaseModel):
    """
    One SBE 2.0 message schema, with its encodings and message templates.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'xml_element': {'tag': 'xml_element',
                                         'value': 'messageSchema'}},
         'close_mappings': ['fix_orchestra:OrchestraRepositoryV10'],
         'comments': ['It is not marked as a tree root because a merged schema can '
                      "have only one, and the final standard's class takes that place. "
                      'Name this class when validating a document.'],
         'from_schema': 'https://w3id.org/lmodel/fix-sbe/schema/fix_sbe_v2_0',
         'slot_usage': {'encoding_sets': {'name': 'encoding_sets',
                                          'range': 'SbeEncodingSetV2'},
                        'message_sets': {'name': 'message_sets',
                                         'range': 'SbeMessageSetV2'},
                        'sbe_id': {'description': 'The number that identifies this '
                                                  'schema between counterparties.',
                                   'name': 'sbe_id'}}})

    schema_package: Optional[str] = Field(default=None, description="""The name or category that a set of counterparties knows this schema or part of it by.""", json_schema_extra = { "linkml_meta": {'aliases': ['package'],
         'domain_of': ['SbeMessageSchemaV1',
                       'SbeMessageSchemaV2',
                       'SbeEncodingSetV2',
                       'SbeMessageSetV2']} })
    sbe_id: Optional[int] = Field(default=None, description="""The number that identifies this schema between counterparties.""", ge=0, le=65535, json_schema_extra = { "linkml_meta": {'aliases': ['id'],
         'annotations': {'xsd_type': {'tag': 'xsd_type', 'value': 'xs:unsignedShort'}},
         'domain_of': ['SbeMessageSchemaV1',
                       'SbeBlockV1Mixin',
                       'SbeFieldV1',
                       'SbeMessageSchemaV2',
                       'SbeBlockV2Mixin',
                       'SbeFieldV2']} })
    schema_version: int = Field(default=..., description="""The version of this message schema, starting at zero.""", ge=0, json_schema_extra = { "linkml_meta": {'aliases': ['version'],
         'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '4: Schema versioning'},
                         'xsd_type': {'tag': 'xsd_type',
                                      'value': 'xs:nonNegativeInteger'}},
         'domain_of': ['SbeMessageSchemaV1', 'SbeMessageSchemaV2']} })
    semantic_version: Optional[str] = Field(default=None, description="""The version of FIX whose meanings this schema uses.""", json_schema_extra = { "linkml_meta": {'aliases': ['semanticVersion'],
         'domain_of': ['SbeMessageSchemaV1', 'SbeMessageSchemaV2']} })
    description: Optional[str] = Field(default=None, description="""Free text about this element, for the people who read the schema.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'domain_of': ['SbeValidValue',
                       'SbeChoice',
                       'SbeMessageSchemaV1',
                       'SbeEncodingV1',
                       'SbeBlockV1Mixin',
                       'SbeFieldV1',
                       'SbeMessageSchemaV2',
                       'SbeEncodingSetV2',
                       'SbeMessageSetV2',
                       'SbeElementV2',
                       'SbeBlockV2Mixin',
                       'SbeFieldV2'],
         'slot_uri': 'schema:description'} })
    byte_order: Optional[SbeByteOrder] = Field(default=SbeByteOrder("littleEndian"), description="""How the octets of every number in this schema's messages are ordered.""", json_schema_extra = { "linkml_meta": {'aliases': ['byteOrder'],
         'domain_of': ['SbeMessageSchemaV1', 'SbeMessageSchemaV2'],
         'ifabsent': 'string(littleEndian)'} })
    header_type: Optional[str] = Field(default="messageHeader", description="""The composite, by name, that sends each message's header in this schema.""", json_schema_extra = { "linkml_meta": {'aliases': ['headerType'],
         'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '3: Message header schema'}},
         'domain_of': ['SbeMessageSchemaV1', 'SbeMessageSchemaV2'],
         'ifabsent': 'string(messageHeader)'} })
    encoding_sets: list[SbeEncodingSetV2] = Field(default=..., description="""The sets of encodings this schema's messages use.""", min_length=1, json_schema_extra = { "linkml_meta": {'aliases': ['types'],
         'domain_of': ['SbeMessageSchemaV1', 'SbeMessageSchemaV2']} })
    message_sets: list[SbeMessageSetV2] = Field(default=..., description="""The sets of message templates of this schema.""", min_length=1, json_schema_extra = { "linkml_meta": {'aliases': ['messages'], 'domain_of': ['SbeMessageSchemaV2']} })

    @field_validator('header_type')
    def pattern_header_type(cls, v):
        pattern=re.compile(r"^[A-Za-z_][0-9A-Za-z_]{0,63}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid header_type format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid header_type format: {v}"
            raise ValueError(err_msg)
        return v


class SbeEncodingSetV2(ConfiguredBaseModel):
    """
    A set of encodings, in any order, that may have its own package and may come from another file.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'xml_element': {'tag': 'xml_element', 'value': 'types'}},
         'from_schema': 'https://w3id.org/lmodel/fix-sbe/schema/fix_sbe_v2_0',
         'slot_usage': {'encodings': {'any_of': [{'range': 'SbeSimpleTypeV2'},
                                                 {'range': 'SbeCompositeV2'},
                                                 {'range': 'SbeEnumV2'},
                                                 {'range': 'SbeSetV2'}],
                                      'comments': ['A composite, an enumeration and a '
                                                   'set may appear here or inside a '
                                                   'composite, and a simple type has a '
                                                   'different shape in each place, so '
                                                   'no single class fits this list.'],
                                      'name': 'encodings',
                                      'range': 'SbeElementV2'},
                        'schema_package': {'description': 'A package for this set in '
                                                          "place of the schema's.",
                                           'name': 'schema_package'}}})

    description: Optional[str] = Field(default=None, description="""Free text about this element, for the people who read the schema.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'domain_of': ['SbeValidValue',
                       'SbeChoice',
                       'SbeMessageSchemaV1',
                       'SbeEncodingV1',
                       'SbeBlockV1Mixin',
                       'SbeFieldV1',
                       'SbeMessageSchemaV2',
                       'SbeEncodingSetV2',
                       'SbeMessageSetV2',
                       'SbeElementV2',
                       'SbeBlockV2Mixin',
                       'SbeFieldV2'],
         'slot_uri': 'schema:description'} })
    schema_package: Optional[str] = Field(default=None, description="""A package for this set in place of the schema's.""", json_schema_extra = { "linkml_meta": {'aliases': ['package'],
         'domain_of': ['SbeMessageSchemaV1',
                       'SbeMessageSchemaV2',
                       'SbeEncodingSetV2',
                       'SbeMessageSetV2']} })
    xml_base: Optional[str] = Field(default=None, description="""The base address that the XML Inclusion mechanism records on an element it brought in from another file.""", json_schema_extra = { "linkml_meta": {'aliases': ['xml:base'],
         'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '4: XInclude usage'}},
         'domain_of': ['SbeEncodingSetV2', 'SbeMessageSetV2']} })
    encodings: list[Union[SbeCompositeV2, SbeEnumV2, SbeSetV2, SbeSimpleTypeV2]] = Field(default=..., description="""The encodings of this set.""", min_length=1, json_schema_extra = { "linkml_meta": {'aliases': ['type', 'composite', 'enum', 'set'],
         'any_of': [{'range': 'SbeSimpleTypeV2'},
                    {'range': 'SbeCompositeV2'},
                    {'range': 'SbeEnumV2'},
                    {'range': 'SbeSetV2'}],
         'comments': ['A composite, an enumeration and a set may appear here or inside '
                      'a composite, and a simple type has a different shape in each '
                      'place, so no single class fits this list.'],
         'domain_of': ['SbeEncodingSetV1', 'SbeEncodingSetV2']} })


class SbeMessageSetV2(ConfiguredBaseModel):
    """
    Message templates held together, which may have their own package and may come from another file.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'xml_element': {'tag': 'xml_element', 'value': 'messages'}},
         'from_schema': 'https://w3id.org/lmodel/fix-sbe/schema/fix_sbe_v2_0',
         'slot_usage': {'messages': {'name': 'messages', 'range': 'SbeMessageV2'},
                        'schema_package': {'description': 'A package for this set in '
                                                          "place of the schema's.",
                                           'name': 'schema_package'}}})

    description: Optional[str] = Field(default=None, description="""Free text about this element, for the people who read the schema.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'domain_of': ['SbeValidValue',
                       'SbeChoice',
                       'SbeMessageSchemaV1',
                       'SbeEncodingV1',
                       'SbeBlockV1Mixin',
                       'SbeFieldV1',
                       'SbeMessageSchemaV2',
                       'SbeEncodingSetV2',
                       'SbeMessageSetV2',
                       'SbeElementV2',
                       'SbeBlockV2Mixin',
                       'SbeFieldV2'],
         'slot_uri': 'schema:description'} })
    schema_package: Optional[str] = Field(default=None, description="""A package for this set in place of the schema's.""", json_schema_extra = { "linkml_meta": {'aliases': ['package'],
         'domain_of': ['SbeMessageSchemaV1',
                       'SbeMessageSchemaV2',
                       'SbeEncodingSetV2',
                       'SbeMessageSetV2']} })
    xml_base: Optional[str] = Field(default=None, description="""The base address that the XML Inclusion mechanism records on an element it brought in from another file.""", json_schema_extra = { "linkml_meta": {'aliases': ['xml:base'],
         'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '4: XInclude usage'}},
         'domain_of': ['SbeEncodingSetV2', 'SbeMessageSetV2']} })
    messages: list[SbeMessageV2] = Field(default=..., description="""The message templates of this set.""", min_length=1, json_schema_extra = { "linkml_meta": {'aliases': ['message'], 'domain_of': ['SbeMessageSchemaV1', 'SbeMessageSetV2']} })


class SbeElementV2(ConfiguredBaseModel):
    """
    Anything that sets of encodings or composites hold, and the name and text they all have.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'abstract': True,
         'from_schema': 'https://w3id.org/lmodel/fix-sbe/schema/fix_sbe_v2_0'})

    encoding_kind: Literal["SbeElementV2"] = Field(default="SbeElementV2", description="""The class of this encoding or composite member, which stands for its XML element.""", json_schema_extra = { "linkml_meta": {'designates_type': True, 'domain_of': ['SbeMemberV1', 'SbeElementV2']} })
    symbolic_name: str = Field(default=..., description="""What the schema calls this element.""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['SbeValidValue',
                       'SbeChoice',
                       'SbeMemberV1',
                       'SbeBlockV1Mixin',
                       'SbeFieldV1',
                       'SbeElementV2',
                       'SbeBlockV2Mixin',
                       'SbeFieldV2']} })
    description: Optional[str] = Field(default=None, description="""Free text about this element, for the people who read the schema.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'domain_of': ['SbeValidValue',
                       'SbeChoice',
                       'SbeMessageSchemaV1',
                       'SbeEncodingV1',
                       'SbeBlockV1Mixin',
                       'SbeFieldV1',
                       'SbeMessageSchemaV2',
                       'SbeEncodingSetV2',
                       'SbeMessageSetV2',
                       'SbeElementV2',
                       'SbeBlockV2Mixin',
                       'SbeFieldV2'],
         'slot_uri': 'schema:description'} })

    @field_validator('symbolic_name')
    def pattern_symbolic_name(cls, v):
        pattern=re.compile(r"^[A-Za-z_][0-9A-Za-z_]{0,63}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid symbolic_name format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid symbolic_name format: {v}"
            raise ValueError(err_msg)
        return v


class SbeMemberV2(SbeElementV2):
    """
    Anything a composite may hold in the order it is sent.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'abstract': True,
         'from_schema': 'https://w3id.org/lmodel/fix-sbe/schema/fix_sbe_v2_0'})

    offset: Optional[int] = Field(default=None, description="""The octet this element starts at, counted from zero at the start of its block or composite.""", ge=0, le=4294967295, json_schema_extra = { "linkml_meta": {'aliases': ['offset'],
         'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '3: Field offset specified by '
                                                  'message schema'},
                         'xsd_type': {'tag': 'xsd_type', 'value': 'xs:unsignedInt'}},
         'domain_of': ['SbeMemberV1', 'SbeFieldV1', 'SbeMemberV2', 'SbeFieldV2']} })
    alignment: Optional[int] = Field(default=None, description="""The multiple of octets the start of this element is placed on.""", ge=1, json_schema_extra = { "linkml_meta": {'aliases': ['alignment'],
         'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '3: Field byte alignment'},
                         'xsd_type': {'tag': 'xsd_type',
                                      'value': 'xs:positiveInteger'}},
         'domain_of': ['SbeMemberV2', 'SbeBlockV2Mixin', 'SbeFieldV2']} })
    encoding_kind: Literal["SbeMemberV2"] = Field(default="SbeMemberV2", description="""The class of this encoding or composite member, which stands for its XML element.""", json_schema_extra = { "linkml_meta": {'designates_type': True, 'domain_of': ['SbeMemberV1', 'SbeElementV2']} })
    symbolic_name: str = Field(default=..., description="""What the schema calls this element.""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['SbeValidValue',
                       'SbeChoice',
                       'SbeMemberV1',
                       'SbeBlockV1Mixin',
                       'SbeFieldV1',
                       'SbeElementV2',
                       'SbeBlockV2Mixin',
                       'SbeFieldV2']} })
    description: Optional[str] = Field(default=None, description="""Free text about this element, for the people who read the schema.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'domain_of': ['SbeValidValue',
                       'SbeChoice',
                       'SbeMessageSchemaV1',
                       'SbeEncodingV1',
                       'SbeBlockV1Mixin',
                       'SbeFieldV1',
                       'SbeMessageSchemaV2',
                       'SbeEncodingSetV2',
                       'SbeMessageSetV2',
                       'SbeElementV2',
                       'SbeBlockV2Mixin',
                       'SbeFieldV2'],
         'slot_uri': 'schema:description'} })

    @field_validator('symbolic_name')
    def pattern_symbolic_name(cls, v):
        pattern=re.compile(r"^[A-Za-z_][0-9A-Za-z_]{0,63}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid symbolic_name format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid symbolic_name format: {v}"
            raise ValueError(err_msg)
        return v


class SbeSimpleTypeV2(SbeElementV2, SbeVersionedMixin):
    """
    A simple encoding that stands alone in a set, backed by one primitive value, or several in an array.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'xml_element': {'tag': 'xml_element', 'value': 'type'},
                         'xsd_type': {'tag': 'xsd_type', 'value': 'simpleDataType'}},
         'close_mappings': ['fix_orchestra:OrchestraDatatypeV10'],
         'from_schema': 'https://w3id.org/lmodel/fix-sbe/schema/fix_sbe_v2_0',
         'mixins': ['SbeVersionedMixin']})

    element_value: Optional[str] = Field(default=None, description="""The text of the XML element, which is the constant when presence is constant.""", json_schema_extra = { "linkml_meta": {'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '4: Constant value'},
                         'xsd_type': {'tag': 'xsd_type', 'value': 'xs:token'}},
         'domain_of': ['SbeSimpleTypeV1',
                       'SbeSimpleTypeV2',
                       'SbeMemberTypeV2',
                       'SbeFieldV2']} })
    primitive_type: SbePrimitiveType = Field(default=..., description="""The wire type under this encoding.""", json_schema_extra = { "linkml_meta": {'aliases': ['primitiveType'],
         'domain_of': ['SbeSimpleTypeV1', 'SbeSimpleTypeV2', 'SbeMemberTypeV2']} })
    array_length: Optional[int] = Field(default=1, description="""How many values of the primitive type the encoding holds, where zero means a variable number.""", ge=0, json_schema_extra = { "linkml_meta": {'aliases': ['length'],
         'annotations': {'xsd_type': {'tag': 'xsd_type',
                                      'value': 'xs:nonNegativeInteger'}},
         'domain_of': ['SbeSimpleTypeV1', 'SbeSimpleTypeV2', 'SbeMemberTypeV2'],
         'ifabsent': 'int(1)'} })
    character_encoding: Optional[str] = Field(default=None, description="""Which character set, or which Unicode scheme, character data follows.""", json_schema_extra = { "linkml_meta": {'aliases': ['characterEncoding'],
         'domain_of': ['SbeSimpleTypeV1', 'SbeSimpleTypeV2', 'SbeMemberTypeV2']} })
    since_version: Optional[int] = Field(default=0, description="""The schema version that added this element.""", ge=0, json_schema_extra = { "linkml_meta": {'aliases': ['sinceVersion'],
         'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '5: Since version'},
                         'xsd_type': {'tag': 'xsd_type',
                                      'value': 'xs:nonNegativeInteger'}},
         'domain_of': ['SbeVersionedMixin'],
         'ifabsent': 'int(0)'} })
    deprecated_since: Optional[int] = Field(default=None, description="""The schema version that retired this element, which stays only for older applications.""", ge=0, json_schema_extra = { "linkml_meta": {'aliases': ['deprecated'],
         'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '5: Deprecated elements'},
                         'xsd_type': {'tag': 'xsd_type',
                                      'value': 'xs:nonNegativeInteger'}},
         'domain_of': ['SbeVersionedMixin']} })
    encoding_kind: Literal["SbeSimpleTypeV2"] = Field(default="SbeSimpleTypeV2", description="""The class of this encoding or composite member, which stands for its XML element.""", json_schema_extra = { "linkml_meta": {'designates_type': True, 'domain_of': ['SbeMemberV1', 'SbeElementV2']} })
    symbolic_name: str = Field(default=..., description="""What the schema calls this element.""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['SbeValidValue',
                       'SbeChoice',
                       'SbeMemberV1',
                       'SbeBlockV1Mixin',
                       'SbeFieldV1',
                       'SbeElementV2',
                       'SbeBlockV2Mixin',
                       'SbeFieldV2']} })
    description: Optional[str] = Field(default=None, description="""Free text about this element, for the people who read the schema.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'domain_of': ['SbeValidValue',
                       'SbeChoice',
                       'SbeMessageSchemaV1',
                       'SbeEncodingV1',
                       'SbeBlockV1Mixin',
                       'SbeFieldV1',
                       'SbeMessageSchemaV2',
                       'SbeEncodingSetV2',
                       'SbeMessageSetV2',
                       'SbeElementV2',
                       'SbeBlockV2Mixin',
                       'SbeFieldV2'],
         'slot_uri': 'schema:description'} })

    @field_validator('element_value')
    def pattern_element_value(cls, v):
        pattern=re.compile(r"^\S+( \S+)*$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid element_value format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid element_value format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('symbolic_name')
    def pattern_symbolic_name(cls, v):
        pattern=re.compile(r"^[A-Za-z_][0-9A-Za-z_]{0,63}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid symbolic_name format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid symbolic_name format: {v}"
            raise ValueError(err_msg)
        return v


class SbeMemberTypeV2(SbeMemberV2):
    """
    A simple encoding inside a composite, which may say it is optional or constant.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'xml_element': {'tag': 'xml_element', 'value': 'type'},
                         'xsd_type': {'tag': 'xsd_type', 'value': 'memberDataType'}},
         'close_mappings': ['fix_orchestra:OrchestraDatatypeV10'],
         'from_schema': 'https://w3id.org/lmodel/fix-sbe/schema/fix_sbe_v2_0',
         'rules': [{'annotations': {'sbe_section': {'tag': 'sbe_section',
                                                    'value': '4: Field attributes'}},
                    'description': 'A value_ref is valid only on an element whose '
                                   'presence is constant.',
                    'postconditions': {'slot_conditions': {'presence': {'equals_string': 'constant',
                                                                        'name': 'presence'}}},
                    'preconditions': {'slot_conditions': {'value_ref': {'name': 'value_ref',
                                                                        'value_presence': 'PRESENT'}}},
                    'title': 'A reference to a value needs a constant'},
                   {'annotations': {'sbe_section': {'tag': 'sbe_section',
                                                    'value': '4: Schema validation'}},
                    'description': 'A null value cannot sit beside a presence of '
                                   'required.',
                    'postconditions': {'slot_conditions': {'null_value': {'name': 'null_value',
                                                                          'value_presence': 'ABSENT'}}},
                    'preconditions': {'slot_conditions': {'presence': {'equals_string': 'required',
                                                                       'name': 'presence'}}},
                    'title': 'A required value has no null'},
                   {'annotations': {'sbe_section': {'tag': 'sbe_section',
                                                    'value': '2: Common field schema '
                                                             'attributes'}},
                    'description': 'A null value cannot sit beside a presence of '
                                   'constant.',
                    'postconditions': {'slot_conditions': {'null_value': {'name': 'null_value',
                                                                          'value_presence': 'ABSENT'}}},
                    'preconditions': {'slot_conditions': {'presence': {'equals_string': 'constant',
                                                                       'name': 'presence'}}},
                    'title': 'A constant has no null'},
                   {'annotations': {'sbe_section': {'tag': 'sbe_section',
                                                    'value': '2: Common field schema '
                                                             'attributes'}},
                    'description': 'A lowest value cannot sit beside a presence of '
                                   'constant.',
                    'postconditions': {'slot_conditions': {'min_value': {'name': 'min_value',
                                                                         'value_presence': 'ABSENT'}}},
                    'preconditions': {'slot_conditions': {'presence': {'equals_string': 'constant',
                                                                       'name': 'presence'}}},
                    'title': 'A constant has no lowest value'},
                   {'annotations': {'sbe_section': {'tag': 'sbe_section',
                                                    'value': '2: Common field schema '
                                                             'attributes'}},
                    'description': 'A highest value cannot sit beside a presence of '
                                   'constant.',
                    'postconditions': {'slot_conditions': {'max_value': {'name': 'max_value',
                                                                         'value_presence': 'ABSENT'}}},
                    'preconditions': {'slot_conditions': {'presence': {'equals_string': 'constant',
                                                                       'name': 'presence'}}},
                    'title': 'A constant has no highest value'}]})

    element_value: Optional[str] = Field(default=None, description="""The text of the XML element, which is the constant when presence is constant.""", json_schema_extra = { "linkml_meta": {'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '4: Constant value'},
                         'xsd_type': {'tag': 'xsd_type', 'value': 'xs:token'}},
         'domain_of': ['SbeSimpleTypeV1',
                       'SbeSimpleTypeV2',
                       'SbeMemberTypeV2',
                       'SbeFieldV2']} })
    primitive_type: SbePrimitiveType = Field(default=..., description="""The wire type under this encoding.""", json_schema_extra = { "linkml_meta": {'aliases': ['primitiveType'],
         'domain_of': ['SbeSimpleTypeV1', 'SbeSimpleTypeV2', 'SbeMemberTypeV2']} })
    array_length: Optional[int] = Field(default=1, description="""How many values of the primitive type the encoding holds, where zero means a variable number.""", ge=0, json_schema_extra = { "linkml_meta": {'aliases': ['length'],
         'annotations': {'xsd_type': {'tag': 'xsd_type',
                                      'value': 'xs:nonNegativeInteger'}},
         'domain_of': ['SbeSimpleTypeV1', 'SbeSimpleTypeV2', 'SbeMemberTypeV2'],
         'ifabsent': 'int(1)'} })
    character_encoding: Optional[str] = Field(default=None, description="""Which character set, or which Unicode scheme, character data follows.""", json_schema_extra = { "linkml_meta": {'aliases': ['characterEncoding'],
         'domain_of': ['SbeSimpleTypeV1', 'SbeSimpleTypeV2', 'SbeMemberTypeV2']} })
    presence: Optional[SbePresence] = Field(default=SbePresence("required"), description="""Whether this element's value is required, optional or constant.""", json_schema_extra = { "linkml_meta": {'aliases': ['presence'],
         'domain_of': ['SbeSimpleTypeV1',
                       'SbeFieldV1',
                       'SbeMemberTypeV2',
                       'SbeFieldV2'],
         'ifabsent': 'string(required)'} })
    null_value: Optional[str] = Field(default=None, description="""The value that stands for null in place of the primitive type's default, written as text.""", json_schema_extra = { "linkml_meta": {'aliases': ['nullValue'],
         'domain_of': ['SbeSimpleTypeV1', 'SbeMemberTypeV2', 'SbeFieldV2']} })
    min_value: Optional[str] = Field(default=None, description="""The lowest value allowed, written as text.""", json_schema_extra = { "linkml_meta": {'aliases': ['minValue'],
         'domain_of': ['SbeSimpleTypeV1', 'SbeMemberTypeV2', 'SbeFieldV2']} })
    max_value: Optional[str] = Field(default=None, description="""The highest value allowed, written as text.""", json_schema_extra = { "linkml_meta": {'aliases': ['maxValue'],
         'domain_of': ['SbeSimpleTypeV1', 'SbeMemberTypeV2', 'SbeFieldV2']} })
    value_ref: Optional[str] = Field(default=None, description="""The valid value that gives a constant element its value.""", json_schema_extra = { "linkml_meta": {'aliases': ['valueRef'],
         'domain_of': ['SbeSimpleTypeV1',
                       'SbeFieldV1',
                       'SbeMemberTypeV2',
                       'SbeFieldV2']} })
    offset: Optional[int] = Field(default=None, description="""The octet this element starts at, counted from zero at the start of its block or composite.""", ge=0, le=4294967295, json_schema_extra = { "linkml_meta": {'aliases': ['offset'],
         'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '3: Field offset specified by '
                                                  'message schema'},
                         'xsd_type': {'tag': 'xsd_type', 'value': 'xs:unsignedInt'}},
         'domain_of': ['SbeMemberV1', 'SbeFieldV1', 'SbeMemberV2', 'SbeFieldV2']} })
    alignment: Optional[int] = Field(default=None, description="""The multiple of octets the start of this element is placed on.""", ge=1, json_schema_extra = { "linkml_meta": {'aliases': ['alignment'],
         'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '3: Field byte alignment'},
                         'xsd_type': {'tag': 'xsd_type',
                                      'value': 'xs:positiveInteger'}},
         'domain_of': ['SbeMemberV2', 'SbeBlockV2Mixin', 'SbeFieldV2']} })
    encoding_kind: Literal["SbeMemberTypeV2"] = Field(default="SbeMemberTypeV2", description="""The class of this encoding or composite member, which stands for its XML element.""", json_schema_extra = { "linkml_meta": {'designates_type': True, 'domain_of': ['SbeMemberV1', 'SbeElementV2']} })
    symbolic_name: str = Field(default=..., description="""What the schema calls this element.""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['SbeValidValue',
                       'SbeChoice',
                       'SbeMemberV1',
                       'SbeBlockV1Mixin',
                       'SbeFieldV1',
                       'SbeElementV2',
                       'SbeBlockV2Mixin',
                       'SbeFieldV2']} })
    description: Optional[str] = Field(default=None, description="""Free text about this element, for the people who read the schema.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'domain_of': ['SbeValidValue',
                       'SbeChoice',
                       'SbeMessageSchemaV1',
                       'SbeEncodingV1',
                       'SbeBlockV1Mixin',
                       'SbeFieldV1',
                       'SbeMessageSchemaV2',
                       'SbeEncodingSetV2',
                       'SbeMessageSetV2',
                       'SbeElementV2',
                       'SbeBlockV2Mixin',
                       'SbeFieldV2'],
         'slot_uri': 'schema:description'} })

    @field_validator('element_value')
    def pattern_element_value(cls, v):
        pattern=re.compile(r"^\S+( \S+)*$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid element_value format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid element_value format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('value_ref')
    def pattern_value_ref(cls, v):
        pattern=re.compile(r"^[A-Za-z_][0-9A-Za-z_]*\.[A-Za-z_][0-9A-Za-z_]*$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid value_ref format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid value_ref format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('symbolic_name')
    def pattern_symbolic_name(cls, v):
        pattern=re.compile(r"^[A-Za-z_][0-9A-Za-z_]{0,63}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid symbolic_name format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid symbolic_name format: {v}"
            raise ValueError(err_msg)
        return v


class SbeRefV2(SbeMemberV2):
    """
    A composite's member that reuses an encoding defined elsewhere in the schema.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'xml_element': {'tag': 'xml_element', 'value': 'ref'},
                         'xsd_type': {'tag': 'xsd_type', 'value': 'refType'}},
         'from_schema': 'https://w3id.org/lmodel/fix-sbe/schema/fix_sbe_v2_0'})

    encoding_name: str = Field(default=..., description="""Which encoding this element uses, by name.""", json_schema_extra = { "linkml_meta": {'aliases': ['type'],
         'comments': ['It holds a name and not a class reference, because a name is '
                      'unique only within one schema document, where several documents '
                      'may be listed side by side. tests/sbe_rules.py holds each to an '
                      'encoding of its document.'],
         'domain_of': ['SbeRefV1', 'SbeFieldV1', 'SbeRefV2', 'SbeFieldV2']} })
    offset: Optional[int] = Field(default=None, description="""The octet this element starts at, counted from zero at the start of its block or composite.""", ge=0, le=4294967295, json_schema_extra = { "linkml_meta": {'aliases': ['offset'],
         'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '3: Field offset specified by '
                                                  'message schema'},
                         'xsd_type': {'tag': 'xsd_type', 'value': 'xs:unsignedInt'}},
         'domain_of': ['SbeMemberV1', 'SbeFieldV1', 'SbeMemberV2', 'SbeFieldV2']} })
    alignment: Optional[int] = Field(default=None, description="""The multiple of octets the start of this element is placed on.""", ge=1, json_schema_extra = { "linkml_meta": {'aliases': ['alignment'],
         'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '3: Field byte alignment'},
                         'xsd_type': {'tag': 'xsd_type',
                                      'value': 'xs:positiveInteger'}},
         'domain_of': ['SbeMemberV2', 'SbeBlockV2Mixin', 'SbeFieldV2']} })
    encoding_kind: Literal["SbeRefV2"] = Field(default="SbeRefV2", description="""The class of this encoding or composite member, which stands for its XML element.""", json_schema_extra = { "linkml_meta": {'designates_type': True, 'domain_of': ['SbeMemberV1', 'SbeElementV2']} })
    symbolic_name: str = Field(default=..., description="""What the schema calls this element.""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['SbeValidValue',
                       'SbeChoice',
                       'SbeMemberV1',
                       'SbeBlockV1Mixin',
                       'SbeFieldV1',
                       'SbeElementV2',
                       'SbeBlockV2Mixin',
                       'SbeFieldV2']} })
    description: Optional[str] = Field(default=None, description="""Free text about this element, for the people who read the schema.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'domain_of': ['SbeValidValue',
                       'SbeChoice',
                       'SbeMessageSchemaV1',
                       'SbeEncodingV1',
                       'SbeBlockV1Mixin',
                       'SbeFieldV1',
                       'SbeMessageSchemaV2',
                       'SbeEncodingSetV2',
                       'SbeMessageSetV2',
                       'SbeElementV2',
                       'SbeBlockV2Mixin',
                       'SbeFieldV2'],
         'slot_uri': 'schema:description'} })

    @field_validator('encoding_name')
    def pattern_encoding_name(cls, v):
        pattern=re.compile(r"^[A-Za-z_][0-9A-Za-z_]{0,63}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid encoding_name format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid encoding_name format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('symbolic_name')
    def pattern_symbolic_name(cls, v):
        pattern=re.compile(r"^[A-Za-z_][0-9A-Za-z_]{0,63}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid symbolic_name format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid symbolic_name format: {v}"
            raise ValueError(err_msg)
        return v


class SbeCompositeV2(SbeMemberV2, SbeVersionedMixin):
    """
    An encoding built from members sent one after another, such as a decimal's mantissa and exponent.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'xml_element': {'tag': 'xml_element', 'value': 'composite'},
                         'xsd_type': {'tag': 'xsd_type', 'value': 'compositeDataType'}},
         'close_mappings': ['fix_orchestra:OrchestraComponentV10'],
         'comments': ['The members keep one list because their order is the order on '
                      'the wire. Separate lists per kind of member could not say that '
                      'an enum comes between two types.'],
         'from_schema': 'https://w3id.org/lmodel/fix-sbe/schema/fix_sbe_v2_0',
         'mixins': ['SbeVersionedMixin'],
         'slot_usage': {'composite_members': {'name': 'composite_members',
                                              'range': 'SbeMemberV2'}}})

    composite_members: list[Union[SbeMemberTypeV2,SbeRefV2,SbeCompositeV2,SbeEnumV2,SbeSetV2]] = Field(default=..., description="""The members of this composite, in the order they are sent.""", min_length=1, json_schema_extra = { "linkml_meta": {'aliases': ['type', 'enum', 'set', 'composite', 'ref'],
         'domain_of': ['SbeCompositeV1', 'SbeCompositeV2']} })
    since_version: Optional[int] = Field(default=0, description="""The schema version that added this element.""", ge=0, json_schema_extra = { "linkml_meta": {'aliases': ['sinceVersion'],
         'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '5: Since version'},
                         'xsd_type': {'tag': 'xsd_type',
                                      'value': 'xs:nonNegativeInteger'}},
         'domain_of': ['SbeVersionedMixin'],
         'ifabsent': 'int(0)'} })
    deprecated_since: Optional[int] = Field(default=None, description="""The schema version that retired this element, which stays only for older applications.""", ge=0, json_schema_extra = { "linkml_meta": {'aliases': ['deprecated'],
         'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '5: Deprecated elements'},
                         'xsd_type': {'tag': 'xsd_type',
                                      'value': 'xs:nonNegativeInteger'}},
         'domain_of': ['SbeVersionedMixin']} })
    offset: Optional[int] = Field(default=None, description="""The octet this element starts at, counted from zero at the start of its block or composite.""", ge=0, le=4294967295, json_schema_extra = { "linkml_meta": {'aliases': ['offset'],
         'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '3: Field offset specified by '
                                                  'message schema'},
                         'xsd_type': {'tag': 'xsd_type', 'value': 'xs:unsignedInt'}},
         'domain_of': ['SbeMemberV1', 'SbeFieldV1', 'SbeMemberV2', 'SbeFieldV2']} })
    alignment: Optional[int] = Field(default=None, description="""The multiple of octets the start of this element is placed on.""", ge=1, json_schema_extra = { "linkml_meta": {'aliases': ['alignment'],
         'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '3: Field byte alignment'},
                         'xsd_type': {'tag': 'xsd_type',
                                      'value': 'xs:positiveInteger'}},
         'domain_of': ['SbeMemberV2', 'SbeBlockV2Mixin', 'SbeFieldV2']} })
    encoding_kind: Literal["SbeCompositeV2"] = Field(default="SbeCompositeV2", description="""The class of this encoding or composite member, which stands for its XML element.""", json_schema_extra = { "linkml_meta": {'designates_type': True, 'domain_of': ['SbeMemberV1', 'SbeElementV2']} })
    symbolic_name: str = Field(default=..., description="""What the schema calls this element.""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['SbeValidValue',
                       'SbeChoice',
                       'SbeMemberV1',
                       'SbeBlockV1Mixin',
                       'SbeFieldV1',
                       'SbeElementV2',
                       'SbeBlockV2Mixin',
                       'SbeFieldV2']} })
    description: Optional[str] = Field(default=None, description="""Free text about this element, for the people who read the schema.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'domain_of': ['SbeValidValue',
                       'SbeChoice',
                       'SbeMessageSchemaV1',
                       'SbeEncodingV1',
                       'SbeBlockV1Mixin',
                       'SbeFieldV1',
                       'SbeMessageSchemaV2',
                       'SbeEncodingSetV2',
                       'SbeMessageSetV2',
                       'SbeElementV2',
                       'SbeBlockV2Mixin',
                       'SbeFieldV2'],
         'slot_uri': 'schema:description'} })

    @field_validator('symbolic_name')
    def pattern_symbolic_name(cls, v):
        pattern=re.compile(r"^[A-Za-z_][0-9A-Za-z_]{0,63}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid symbolic_name format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid symbolic_name format: {v}"
            raise ValueError(err_msg)
        return v


class SbeEnumV2(SbeMemberV2, SbeVersionedMixin):
    """
    An encoding whose value is one of a listed set of valid values.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'xml_element': {'tag': 'xml_element', 'value': 'enum'},
                         'xsd_type': {'tag': 'xsd_type', 'value': 'enumType'}},
         'close_mappings': ['fix_orchestra:OrchestraCodeSetV10'],
         'from_schema': 'https://w3id.org/lmodel/fix-sbe/schema/fix_sbe_v2_0',
         'mixins': ['SbeVersionedMixin']})

    encoding_type: str = Field(default=..., description="""The simple encoding or primitive type that an enumeration or set is sent as.""", json_schema_extra = { "linkml_meta": {'aliases': ['encodingType'],
         'domain_of': ['SbeEnumV1', 'SbeSetV1', 'SbeEnumV2', 'SbeSetV2']} })
    valid_values: list[SbeValidValue] = Field(default=..., description="""The values this enumeration allows.""", min_length=1, json_schema_extra = { "linkml_meta": {'aliases': ['validValue'], 'domain_of': ['SbeEnumV1', 'SbeEnumV2']} })
    since_version: Optional[int] = Field(default=0, description="""The schema version that added this element.""", ge=0, json_schema_extra = { "linkml_meta": {'aliases': ['sinceVersion'],
         'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '5: Since version'},
                         'xsd_type': {'tag': 'xsd_type',
                                      'value': 'xs:nonNegativeInteger'}},
         'domain_of': ['SbeVersionedMixin'],
         'ifabsent': 'int(0)'} })
    deprecated_since: Optional[int] = Field(default=None, description="""The schema version that retired this element, which stays only for older applications.""", ge=0, json_schema_extra = { "linkml_meta": {'aliases': ['deprecated'],
         'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '5: Deprecated elements'},
                         'xsd_type': {'tag': 'xsd_type',
                                      'value': 'xs:nonNegativeInteger'}},
         'domain_of': ['SbeVersionedMixin']} })
    offset: Optional[int] = Field(default=None, description="""The octet this element starts at, counted from zero at the start of its block or composite.""", ge=0, le=4294967295, json_schema_extra = { "linkml_meta": {'aliases': ['offset'],
         'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '3: Field offset specified by '
                                                  'message schema'},
                         'xsd_type': {'tag': 'xsd_type', 'value': 'xs:unsignedInt'}},
         'domain_of': ['SbeMemberV1', 'SbeFieldV1', 'SbeMemberV2', 'SbeFieldV2']} })
    alignment: Optional[int] = Field(default=None, description="""The multiple of octets the start of this element is placed on.""", ge=1, json_schema_extra = { "linkml_meta": {'aliases': ['alignment'],
         'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '3: Field byte alignment'},
                         'xsd_type': {'tag': 'xsd_type',
                                      'value': 'xs:positiveInteger'}},
         'domain_of': ['SbeMemberV2', 'SbeBlockV2Mixin', 'SbeFieldV2']} })
    encoding_kind: Literal["SbeEnumV2"] = Field(default="SbeEnumV2", description="""The class of this encoding or composite member, which stands for its XML element.""", json_schema_extra = { "linkml_meta": {'designates_type': True, 'domain_of': ['SbeMemberV1', 'SbeElementV2']} })
    symbolic_name: str = Field(default=..., description="""What the schema calls this element.""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['SbeValidValue',
                       'SbeChoice',
                       'SbeMemberV1',
                       'SbeBlockV1Mixin',
                       'SbeFieldV1',
                       'SbeElementV2',
                       'SbeBlockV2Mixin',
                       'SbeFieldV2']} })
    description: Optional[str] = Field(default=None, description="""Free text about this element, for the people who read the schema.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'domain_of': ['SbeValidValue',
                       'SbeChoice',
                       'SbeMessageSchemaV1',
                       'SbeEncodingV1',
                       'SbeBlockV1Mixin',
                       'SbeFieldV1',
                       'SbeMessageSchemaV2',
                       'SbeEncodingSetV2',
                       'SbeMessageSetV2',
                       'SbeElementV2',
                       'SbeBlockV2Mixin',
                       'SbeFieldV2'],
         'slot_uri': 'schema:description'} })

    @field_validator('encoding_type')
    def pattern_encoding_type(cls, v):
        pattern=re.compile(r"^[A-Za-z_][0-9A-Za-z_]{0,63}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid encoding_type format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid encoding_type format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('symbolic_name')
    def pattern_symbolic_name(cls, v):
        pattern=re.compile(r"^[A-Za-z_][0-9A-Za-z_]{0,63}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid symbolic_name format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid symbolic_name format: {v}"
            raise ValueError(err_msg)
        return v


class SbeSetV2(SbeMemberV2, SbeVersionedMixin):
    """
    An encoding whose value is any combination of up to 64 choices, sent as a bitset.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'xml_element': {'tag': 'xml_element', 'value': 'set'},
                         'xsd_type': {'tag': 'xsd_type', 'value': 'setType'}},
         'comments': ["FIX's transposer does not carry a set to Orchestra, so the "
                      "mapping is related. FIX's MultipleCharValue and "
                      'MultipleStringValue fields hold such choices in a code set.'],
         'from_schema': 'https://w3id.org/lmodel/fix-sbe/schema/fix_sbe_v2_0',
         'mixins': ['SbeVersionedMixin'],
         'related_mappings': ['fix_orchestra:OrchestraCodeSetV10']})

    encoding_type: str = Field(default=..., description="""The simple encoding or primitive type that an enumeration or set is sent as.""", json_schema_extra = { "linkml_meta": {'aliases': ['encodingType'],
         'domain_of': ['SbeEnumV1', 'SbeSetV1', 'SbeEnumV2', 'SbeSetV2']} })
    choices: list[SbeChoice] = Field(default=..., description="""The alternatives of this set.""", min_length=1, max_length=64, json_schema_extra = { "linkml_meta": {'aliases': ['choice'], 'domain_of': ['SbeSetV1', 'SbeSetV2']} })
    since_version: Optional[int] = Field(default=0, description="""The schema version that added this element.""", ge=0, json_schema_extra = { "linkml_meta": {'aliases': ['sinceVersion'],
         'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '5: Since version'},
                         'xsd_type': {'tag': 'xsd_type',
                                      'value': 'xs:nonNegativeInteger'}},
         'domain_of': ['SbeVersionedMixin'],
         'ifabsent': 'int(0)'} })
    deprecated_since: Optional[int] = Field(default=None, description="""The schema version that retired this element, which stays only for older applications.""", ge=0, json_schema_extra = { "linkml_meta": {'aliases': ['deprecated'],
         'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '5: Deprecated elements'},
                         'xsd_type': {'tag': 'xsd_type',
                                      'value': 'xs:nonNegativeInteger'}},
         'domain_of': ['SbeVersionedMixin']} })
    offset: Optional[int] = Field(default=None, description="""The octet this element starts at, counted from zero at the start of its block or composite.""", ge=0, le=4294967295, json_schema_extra = { "linkml_meta": {'aliases': ['offset'],
         'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '3: Field offset specified by '
                                                  'message schema'},
                         'xsd_type': {'tag': 'xsd_type', 'value': 'xs:unsignedInt'}},
         'domain_of': ['SbeMemberV1', 'SbeFieldV1', 'SbeMemberV2', 'SbeFieldV2']} })
    alignment: Optional[int] = Field(default=None, description="""The multiple of octets the start of this element is placed on.""", ge=1, json_schema_extra = { "linkml_meta": {'aliases': ['alignment'],
         'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '3: Field byte alignment'},
                         'xsd_type': {'tag': 'xsd_type',
                                      'value': 'xs:positiveInteger'}},
         'domain_of': ['SbeMemberV2', 'SbeBlockV2Mixin', 'SbeFieldV2']} })
    encoding_kind: Literal["SbeSetV2"] = Field(default="SbeSetV2", description="""The class of this encoding or composite member, which stands for its XML element.""", json_schema_extra = { "linkml_meta": {'designates_type': True, 'domain_of': ['SbeMemberV1', 'SbeElementV2']} })
    symbolic_name: str = Field(default=..., description="""What the schema calls this element.""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['SbeValidValue',
                       'SbeChoice',
                       'SbeMemberV1',
                       'SbeBlockV1Mixin',
                       'SbeFieldV1',
                       'SbeElementV2',
                       'SbeBlockV2Mixin',
                       'SbeFieldV2']} })
    description: Optional[str] = Field(default=None, description="""Free text about this element, for the people who read the schema.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'domain_of': ['SbeValidValue',
                       'SbeChoice',
                       'SbeMessageSchemaV1',
                       'SbeEncodingV1',
                       'SbeBlockV1Mixin',
                       'SbeFieldV1',
                       'SbeMessageSchemaV2',
                       'SbeEncodingSetV2',
                       'SbeMessageSetV2',
                       'SbeElementV2',
                       'SbeBlockV2Mixin',
                       'SbeFieldV2'],
         'slot_uri': 'schema:description'} })

    @field_validator('encoding_type')
    def pattern_encoding_type(cls, v):
        pattern=re.compile(r"^[A-Za-z_][0-9A-Za-z_]{0,63}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid encoding_type format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid encoding_type format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('symbolic_name')
    def pattern_symbolic_name(cls, v):
        pattern=re.compile(r"^[A-Za-z_][0-9A-Za-z_]{0,63}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid symbolic_name format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid symbolic_name format: {v}"
            raise ValueError(err_msg)
        return v


class SbeBlockV2Mixin(ConfiguredBaseModel):
    """
    The body shared by a message and a group entry, which holds its fixed-length fields first, then groups, then variable-length data.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/lmodel/fix-sbe/schema/fix_sbe_v2_0',
         'mixin': True,
         'slot_usage': {'alignment': {'description': 'The multiple of octets where a '
                                                     'message or each group entry '
                                                     'begins.',
                                      'name': 'alignment'},
                        'block_fields': {'name': 'block_fields', 'range': 'SbeFieldV2'},
                        'repeating_groups': {'name': 'repeating_groups',
                                             'range': 'SbeGroupV2'},
                        'sbe_id': {'name': 'sbe_id', 'required': True},
                        'var_data_fields': {'name': 'var_data_fields',
                                            'range': 'SbeFieldV2'}}})

    symbolic_name: str = Field(default=..., description="""What the schema calls this element.""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['SbeValidValue',
                       'SbeChoice',
                       'SbeMemberV1',
                       'SbeBlockV1Mixin',
                       'SbeFieldV1',
                       'SbeElementV2',
                       'SbeBlockV2Mixin',
                       'SbeFieldV2']} })
    sbe_id: int = Field(default=..., description="""The number that identifies this element.""", ge=0, le=65535, json_schema_extra = { "linkml_meta": {'aliases': ['id'],
         'annotations': {'xsd_type': {'tag': 'xsd_type', 'value': 'xs:unsignedShort'}},
         'domain_of': ['SbeMessageSchemaV1',
                       'SbeBlockV1Mixin',
                       'SbeFieldV1',
                       'SbeMessageSchemaV2',
                       'SbeBlockV2Mixin',
                       'SbeFieldV2']} })
    block_length: Optional[int] = Field(default=None, description="""The octets set aside for a message's fixed-length fields, or for those of each group entry.""", ge=0, json_schema_extra = { "linkml_meta": {'aliases': ['blockLength'],
         'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '3: Root block length'},
                         'xsd_type': {'tag': 'xsd_type',
                                      'value': 'xs:nonNegativeInteger'}},
         'domain_of': ['SbeBlockV1Mixin', 'SbeBlockV2Mixin']} })
    alignment: Optional[int] = Field(default=None, description="""The multiple of octets where a message or each group entry begins.""", ge=1, json_schema_extra = { "linkml_meta": {'aliases': ['alignment'],
         'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '3: Field byte alignment'},
                         'xsd_type': {'tag': 'xsd_type',
                                      'value': 'xs:positiveInteger'}},
         'domain_of': ['SbeMemberV2', 'SbeBlockV2Mixin', 'SbeFieldV2']} })
    semantic_type: Optional[str] = Field(default=None, description="""What this element means at the FIX application layer.""", json_schema_extra = { "linkml_meta": {'aliases': ['semanticType'],
         'annotations': {'xsd_type': {'tag': 'xsd_type', 'value': 'xs:token'}},
         'domain_of': ['SbeEncodingV1',
                       'SbeBlockV1Mixin',
                       'SbeFieldV1',
                       'SbeBlockV2Mixin',
                       'SbeFieldV2']} })
    description: Optional[str] = Field(default=None, description="""Free text about this element, for the people who read the schema.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'domain_of': ['SbeValidValue',
                       'SbeChoice',
                       'SbeMessageSchemaV1',
                       'SbeEncodingV1',
                       'SbeBlockV1Mixin',
                       'SbeFieldV1',
                       'SbeMessageSchemaV2',
                       'SbeEncodingSetV2',
                       'SbeMessageSetV2',
                       'SbeElementV2',
                       'SbeBlockV2Mixin',
                       'SbeFieldV2'],
         'slot_uri': 'schema:description'} })
    block_fields: Optional[list[SbeFieldV2]] = Field(default=None, description="""Fixed-length fields, listed in wire order.""", json_schema_extra = { "linkml_meta": {'aliases': ['field'], 'domain_of': ['SbeBlockV1Mixin', 'SbeBlockV2Mixin']} })
    repeating_groups: Optional[list[SbeGroupV2]] = Field(default=None, description="""Repeating groups, listed in wire order.""", json_schema_extra = { "linkml_meta": {'aliases': ['group'], 'domain_of': ['SbeBlockV1Mixin', 'SbeBlockV2Mixin']} })
    var_data_fields: Optional[list[SbeFieldV2]] = Field(default=None, description="""Variable-length fields, listed in wire order.""", json_schema_extra = { "linkml_meta": {'aliases': ['data'], 'domain_of': ['SbeBlockV1Mixin', 'SbeBlockV2Mixin']} })

    @field_validator('symbolic_name')
    def pattern_symbolic_name(cls, v):
        pattern=re.compile(r"^[A-Za-z_][0-9A-Za-z_]{0,63}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid symbolic_name format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid symbolic_name format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('semantic_type')
    def pattern_semantic_type(cls, v):
        pattern=re.compile(r"^\S+( \S+)*$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid semantic_type format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid semantic_type format: {v}"
            raise ValueError(err_msg)
        return v


class SbeMessageV2(SbeBlockV2Mixin, SbeVersionedMixin):
    """
    A message template, whose number and block length are sent in each message's header.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'xml_element': {'tag': 'xml_element', 'value': 'message'},
                         'xsd_type': {'tag': 'xsd_type', 'value': 'blockType'}},
         'close_mappings': ['fix_orchestra:OrchestraMessageV10'],
         'from_schema': 'https://w3id.org/lmodel/fix-sbe/schema/fix_sbe_v2_0',
         'mixins': ['SbeVersionedMixin', 'SbeBlockV2Mixin'],
         'slot_usage': {'sbe_id': {'description': "The template's number, which no "
                                                  'other template in the schema '
                                                  'shares.',
                                   'name': 'sbe_id'},
                        'semantic_type': {'description': 'The FIX MsgType(35) this '
                                                         'template stands for, where '
                                                         'several templates may share '
                                                         'one.',
                                          'name': 'semantic_type'}}})

    since_version: Optional[int] = Field(default=0, description="""The schema version that added this element.""", ge=0, json_schema_extra = { "linkml_meta": {'aliases': ['sinceVersion'],
         'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '5: Since version'},
                         'xsd_type': {'tag': 'xsd_type',
                                      'value': 'xs:nonNegativeInteger'}},
         'domain_of': ['SbeVersionedMixin'],
         'ifabsent': 'int(0)'} })
    deprecated_since: Optional[int] = Field(default=None, description="""The schema version that retired this element, which stays only for older applications.""", ge=0, json_schema_extra = { "linkml_meta": {'aliases': ['deprecated'],
         'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '5: Deprecated elements'},
                         'xsd_type': {'tag': 'xsd_type',
                                      'value': 'xs:nonNegativeInteger'}},
         'domain_of': ['SbeVersionedMixin']} })
    symbolic_name: str = Field(default=..., description="""What the schema calls this element.""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['SbeValidValue',
                       'SbeChoice',
                       'SbeMemberV1',
                       'SbeBlockV1Mixin',
                       'SbeFieldV1',
                       'SbeElementV2',
                       'SbeBlockV2Mixin',
                       'SbeFieldV2']} })
    sbe_id: int = Field(default=..., description="""The template's number, which no other template in the schema shares.""", ge=0, le=65535, json_schema_extra = { "linkml_meta": {'aliases': ['id'],
         'annotations': {'xsd_type': {'tag': 'xsd_type', 'value': 'xs:unsignedShort'}},
         'domain_of': ['SbeMessageSchemaV1',
                       'SbeBlockV1Mixin',
                       'SbeFieldV1',
                       'SbeMessageSchemaV2',
                       'SbeBlockV2Mixin',
                       'SbeFieldV2']} })
    block_length: Optional[int] = Field(default=None, description="""The octets set aside for a message's fixed-length fields, or for those of each group entry.""", ge=0, json_schema_extra = { "linkml_meta": {'aliases': ['blockLength'],
         'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '3: Root block length'},
                         'xsd_type': {'tag': 'xsd_type',
                                      'value': 'xs:nonNegativeInteger'}},
         'domain_of': ['SbeBlockV1Mixin', 'SbeBlockV2Mixin']} })
    alignment: Optional[int] = Field(default=None, description="""The multiple of octets where a message or each group entry begins.""", ge=1, json_schema_extra = { "linkml_meta": {'aliases': ['alignment'],
         'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '3: Field byte alignment'},
                         'xsd_type': {'tag': 'xsd_type',
                                      'value': 'xs:positiveInteger'}},
         'domain_of': ['SbeMemberV2', 'SbeBlockV2Mixin', 'SbeFieldV2']} })
    semantic_type: Optional[str] = Field(default=None, description="""The FIX MsgType(35) this template stands for, where several templates may share one.""", json_schema_extra = { "linkml_meta": {'aliases': ['semanticType'],
         'annotations': {'xsd_type': {'tag': 'xsd_type', 'value': 'xs:token'}},
         'domain_of': ['SbeEncodingV1',
                       'SbeBlockV1Mixin',
                       'SbeFieldV1',
                       'SbeBlockV2Mixin',
                       'SbeFieldV2']} })
    description: Optional[str] = Field(default=None, description="""Free text about this element, for the people who read the schema.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'domain_of': ['SbeValidValue',
                       'SbeChoice',
                       'SbeMessageSchemaV1',
                       'SbeEncodingV1',
                       'SbeBlockV1Mixin',
                       'SbeFieldV1',
                       'SbeMessageSchemaV2',
                       'SbeEncodingSetV2',
                       'SbeMessageSetV2',
                       'SbeElementV2',
                       'SbeBlockV2Mixin',
                       'SbeFieldV2'],
         'slot_uri': 'schema:description'} })
    block_fields: Optional[list[SbeFieldV2]] = Field(default=None, description="""Fixed-length fields, listed in wire order.""", json_schema_extra = { "linkml_meta": {'aliases': ['field'], 'domain_of': ['SbeBlockV1Mixin', 'SbeBlockV2Mixin']} })
    repeating_groups: Optional[list[SbeGroupV2]] = Field(default=None, description="""Repeating groups, listed in wire order.""", json_schema_extra = { "linkml_meta": {'aliases': ['group'], 'domain_of': ['SbeBlockV1Mixin', 'SbeBlockV2Mixin']} })
    var_data_fields: Optional[list[SbeFieldV2]] = Field(default=None, description="""Variable-length fields, listed in wire order.""", json_schema_extra = { "linkml_meta": {'aliases': ['data'], 'domain_of': ['SbeBlockV1Mixin', 'SbeBlockV2Mixin']} })

    @field_validator('symbolic_name')
    def pattern_symbolic_name(cls, v):
        pattern=re.compile(r"^[A-Za-z_][0-9A-Za-z_]{0,63}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid symbolic_name format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid symbolic_name format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('semantic_type')
    def pattern_semantic_type(cls, v):
        pattern=re.compile(r"^\S+( \S+)*$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid semantic_type format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid semantic_type format: {v}"
            raise ValueError(err_msg)
        return v


class SbeGroupV2(SbeBlockV2Mixin, SbeVersionedMixin):
    """
    A repeating group, whose entries each hold the same fields, and which cannot be without a field.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'xml_element': {'tag': 'xml_element', 'value': 'group'},
                         'xsd_type': {'tag': 'xsd_type', 'value': 'groupType'}},
         'close_mappings': ['fix_orchestra:OrchestraGroupV10'],
         'from_schema': 'https://w3id.org/lmodel/fix-sbe/schema/fix_sbe_v2_0',
         'mixins': ['SbeVersionedMixin', 'SbeBlockV2Mixin'],
         'slot_usage': {'block_fields': {'minimum_cardinality': 1,
                                         'name': 'block_fields',
                                         'required': True}}})

    dimension_type: Optional[str] = Field(default="groupSizeEncoding", description="""The composite, by name, that sends a repeating group's entry count and entry size.""", json_schema_extra = { "linkml_meta": {'aliases': ['dimensionType'],
         'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '3: Encoding of repeating group '
                                                  'dimensions'}},
         'domain_of': ['SbeGroupV1', 'SbeGroupV2'],
         'ifabsent': 'string(groupSizeEncoding)'} })
    since_version: Optional[int] = Field(default=0, description="""The schema version that added this element.""", ge=0, json_schema_extra = { "linkml_meta": {'aliases': ['sinceVersion'],
         'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '5: Since version'},
                         'xsd_type': {'tag': 'xsd_type',
                                      'value': 'xs:nonNegativeInteger'}},
         'domain_of': ['SbeVersionedMixin'],
         'ifabsent': 'int(0)'} })
    deprecated_since: Optional[int] = Field(default=None, description="""The schema version that retired this element, which stays only for older applications.""", ge=0, json_schema_extra = { "linkml_meta": {'aliases': ['deprecated'],
         'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '5: Deprecated elements'},
                         'xsd_type': {'tag': 'xsd_type',
                                      'value': 'xs:nonNegativeInteger'}},
         'domain_of': ['SbeVersionedMixin']} })
    symbolic_name: str = Field(default=..., description="""What the schema calls this element.""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['SbeValidValue',
                       'SbeChoice',
                       'SbeMemberV1',
                       'SbeBlockV1Mixin',
                       'SbeFieldV1',
                       'SbeElementV2',
                       'SbeBlockV2Mixin',
                       'SbeFieldV2']} })
    sbe_id: int = Field(default=..., description="""The number that identifies this element.""", ge=0, le=65535, json_schema_extra = { "linkml_meta": {'aliases': ['id'],
         'annotations': {'xsd_type': {'tag': 'xsd_type', 'value': 'xs:unsignedShort'}},
         'domain_of': ['SbeMessageSchemaV1',
                       'SbeBlockV1Mixin',
                       'SbeFieldV1',
                       'SbeMessageSchemaV2',
                       'SbeBlockV2Mixin',
                       'SbeFieldV2']} })
    block_length: Optional[int] = Field(default=None, description="""The octets set aside for a message's fixed-length fields, or for those of each group entry.""", ge=0, json_schema_extra = { "linkml_meta": {'aliases': ['blockLength'],
         'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '3: Root block length'},
                         'xsd_type': {'tag': 'xsd_type',
                                      'value': 'xs:nonNegativeInteger'}},
         'domain_of': ['SbeBlockV1Mixin', 'SbeBlockV2Mixin']} })
    alignment: Optional[int] = Field(default=None, description="""The multiple of octets where a message or each group entry begins.""", ge=1, json_schema_extra = { "linkml_meta": {'aliases': ['alignment'],
         'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '3: Field byte alignment'},
                         'xsd_type': {'tag': 'xsd_type',
                                      'value': 'xs:positiveInteger'}},
         'domain_of': ['SbeMemberV2', 'SbeBlockV2Mixin', 'SbeFieldV2']} })
    semantic_type: Optional[str] = Field(default=None, description="""What this element means at the FIX application layer.""", json_schema_extra = { "linkml_meta": {'aliases': ['semanticType'],
         'annotations': {'xsd_type': {'tag': 'xsd_type', 'value': 'xs:token'}},
         'domain_of': ['SbeEncodingV1',
                       'SbeBlockV1Mixin',
                       'SbeFieldV1',
                       'SbeBlockV2Mixin',
                       'SbeFieldV2']} })
    description: Optional[str] = Field(default=None, description="""Free text about this element, for the people who read the schema.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'domain_of': ['SbeValidValue',
                       'SbeChoice',
                       'SbeMessageSchemaV1',
                       'SbeEncodingV1',
                       'SbeBlockV1Mixin',
                       'SbeFieldV1',
                       'SbeMessageSchemaV2',
                       'SbeEncodingSetV2',
                       'SbeMessageSetV2',
                       'SbeElementV2',
                       'SbeBlockV2Mixin',
                       'SbeFieldV2'],
         'slot_uri': 'schema:description'} })
    block_fields: list[SbeFieldV2] = Field(default=..., description="""Fixed-length fields, listed in wire order.""", min_length=1, json_schema_extra = { "linkml_meta": {'aliases': ['field'], 'domain_of': ['SbeBlockV1Mixin', 'SbeBlockV2Mixin']} })
    repeating_groups: Optional[list[SbeGroupV2]] = Field(default=None, description="""Repeating groups, listed in wire order.""", json_schema_extra = { "linkml_meta": {'aliases': ['group'], 'domain_of': ['SbeBlockV1Mixin', 'SbeBlockV2Mixin']} })
    var_data_fields: Optional[list[SbeFieldV2]] = Field(default=None, description="""Variable-length fields, listed in wire order.""", json_schema_extra = { "linkml_meta": {'aliases': ['data'], 'domain_of': ['SbeBlockV1Mixin', 'SbeBlockV2Mixin']} })

    @field_validator('dimension_type')
    def pattern_dimension_type(cls, v):
        pattern=re.compile(r"^[A-Za-z_][0-9A-Za-z_]{0,63}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid dimension_type format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid dimension_type format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('symbolic_name')
    def pattern_symbolic_name(cls, v):
        pattern=re.compile(r"^[A-Za-z_][0-9A-Za-z_]{0,63}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid symbolic_name format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid symbolic_name format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('semantic_type')
    def pattern_semantic_type(cls, v):
        pattern=re.compile(r"^\S+( \S+)*$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid semantic_type format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid semantic_type format: {v}"
            raise ValueError(err_msg)
        return v


class SbeFieldV2(SbeVersionedMixin):
    """
    A message's or group entry's field, which uses an encoding at a place in its block and may state a constant.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'xml_element': {'tag': 'xml_element', 'value': 'field'},
                         'xsd_type': {'tag': 'xsd_type', 'value': 'fieldType'}},
         'close_mappings': ['fix_orchestra:OrchestraFieldV10'],
         'comments': ['The old mapping called this an exact match of an Orchestra '
                      'field, but the two differ. This one sits at a place in one '
                      "block, and FIX's transposer carries one with a composite "
                      'encoding to a component reference, not a field.'],
         'from_schema': 'https://w3id.org/lmodel/fix-sbe/schema/fix_sbe_v2_0',
         'mixins': ['SbeVersionedMixin'],
         'rules': [{'annotations': {'sbe_section': {'tag': 'sbe_section',
                                                    'value': '4: Field attributes'}},
                    'description': 'A value_ref is valid only on an element whose '
                                   'presence is constant.',
                    'postconditions': {'slot_conditions': {'presence': {'equals_string': 'constant',
                                                                        'name': 'presence'}}},
                    'preconditions': {'slot_conditions': {'value_ref': {'name': 'value_ref',
                                                                        'value_presence': 'PRESENT'}}},
                    'title': 'A reference to a value needs a constant'},
                   {'annotations': {'sbe_section': {'tag': 'sbe_section',
                                                    'value': '4: Schema validation'}},
                    'description': 'A null value cannot sit beside a presence of '
                                   'required.',
                    'postconditions': {'slot_conditions': {'null_value': {'name': 'null_value',
                                                                          'value_presence': 'ABSENT'}}},
                    'preconditions': {'slot_conditions': {'presence': {'equals_string': 'required',
                                                                       'name': 'presence'}}},
                    'title': 'A required value has no null'},
                   {'annotations': {'sbe_section': {'tag': 'sbe_section',
                                                    'value': '2: Common field schema '
                                                             'attributes'}},
                    'description': 'A null value cannot sit beside a presence of '
                                   'constant.',
                    'postconditions': {'slot_conditions': {'null_value': {'name': 'null_value',
                                                                          'value_presence': 'ABSENT'}}},
                    'preconditions': {'slot_conditions': {'presence': {'equals_string': 'constant',
                                                                       'name': 'presence'}}},
                    'title': 'A constant has no null'},
                   {'annotations': {'sbe_section': {'tag': 'sbe_section',
                                                    'value': '2: Common field schema '
                                                             'attributes'}},
                    'description': 'A lowest value cannot sit beside a presence of '
                                   'constant.',
                    'postconditions': {'slot_conditions': {'min_value': {'name': 'min_value',
                                                                         'value_presence': 'ABSENT'}}},
                    'preconditions': {'slot_conditions': {'presence': {'equals_string': 'constant',
                                                                       'name': 'presence'}}},
                    'title': 'A constant has no lowest value'},
                   {'annotations': {'sbe_section': {'tag': 'sbe_section',
                                                    'value': '2: Common field schema '
                                                             'attributes'}},
                    'description': 'A highest value cannot sit beside a presence of '
                                   'constant.',
                    'postconditions': {'slot_conditions': {'max_value': {'name': 'max_value',
                                                                         'value_presence': 'ABSENT'}}},
                    'preconditions': {'slot_conditions': {'presence': {'equals_string': 'constant',
                                                                       'name': 'presence'}}},
                    'title': 'A constant has no highest value'},
                   {'annotations': {'sbe_section': {'tag': 'sbe_section',
                                                    'value': '3: Field byte '
                                                             'alignment'}},
                    'description': 'A field places itself by an offset or by an '
                                   'alignment, never both.',
                    'postconditions': {'slot_conditions': {'offset': {'name': 'offset',
                                                                      'value_presence': 'ABSENT'}}},
                    'preconditions': {'slot_conditions': {'alignment': {'name': 'alignment',
                                                                        'value_presence': 'PRESENT'}}},
                    'title': 'An offset or an alignment, not both'}],
         'slot_usage': {'alignment': {'description': 'The multiple of octets the start '
                                                     'of this field is placed on, in '
                                                     'place of an offset.',
                                      'name': 'alignment'},
                        'sbe_id': {'description': "The field's FIX tag number.",
                                   'name': 'sbe_id',
                                   'required': True},
                        'semantic_type': {'description': 'The FIX datatype this field '
                                                         'carries.',
                                          'name': 'semantic_type'}}})

    symbolic_name: str = Field(default=..., description="""What the schema calls this element.""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['SbeValidValue',
                       'SbeChoice',
                       'SbeMemberV1',
                       'SbeBlockV1Mixin',
                       'SbeFieldV1',
                       'SbeElementV2',
                       'SbeBlockV2Mixin',
                       'SbeFieldV2']} })
    sbe_id: int = Field(default=..., description="""The field's FIX tag number.""", ge=0, le=65535, json_schema_extra = { "linkml_meta": {'aliases': ['id'],
         'annotations': {'xsd_type': {'tag': 'xsd_type', 'value': 'xs:unsignedShort'}},
         'domain_of': ['SbeMessageSchemaV1',
                       'SbeBlockV1Mixin',
                       'SbeFieldV1',
                       'SbeMessageSchemaV2',
                       'SbeBlockV2Mixin',
                       'SbeFieldV2']} })
    encoding_name: str = Field(default=..., description="""Which encoding this element uses, by name.""", json_schema_extra = { "linkml_meta": {'aliases': ['type'],
         'comments': ['It holds a name and not a class reference, because a name is '
                      'unique only within one schema document, where several documents '
                      'may be listed side by side. tests/sbe_rules.py holds each to an '
                      'encoding of its document.'],
         'domain_of': ['SbeRefV1', 'SbeFieldV1', 'SbeRefV2', 'SbeFieldV2']} })
    element_value: Optional[str] = Field(default=None, description="""The text of the XML element, which is the constant when presence is constant.""", json_schema_extra = { "linkml_meta": {'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '4: Constant value'},
                         'xsd_type': {'tag': 'xsd_type', 'value': 'xs:token'}},
         'domain_of': ['SbeSimpleTypeV1',
                       'SbeSimpleTypeV2',
                       'SbeMemberTypeV2',
                       'SbeFieldV2']} })
    offset: Optional[int] = Field(default=None, description="""The octet this element starts at, counted from zero at the start of its block or composite.""", ge=0, le=4294967295, json_schema_extra = { "linkml_meta": {'aliases': ['offset'],
         'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '3: Field offset specified by '
                                                  'message schema'},
                         'xsd_type': {'tag': 'xsd_type', 'value': 'xs:unsignedInt'}},
         'domain_of': ['SbeMemberV1', 'SbeFieldV1', 'SbeMemberV2', 'SbeFieldV2']} })
    alignment: Optional[int] = Field(default=None, description="""The multiple of octets the start of this field is placed on, in place of an offset.""", ge=1, json_schema_extra = { "linkml_meta": {'aliases': ['alignment'],
         'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '3: Field byte alignment'},
                         'xsd_type': {'tag': 'xsd_type',
                                      'value': 'xs:positiveInteger'}},
         'domain_of': ['SbeMemberV2', 'SbeBlockV2Mixin', 'SbeFieldV2']} })
    presence: Optional[SbePresence] = Field(default=SbePresence("required"), description="""Whether this element's value is required, optional or constant.""", json_schema_extra = { "linkml_meta": {'aliases': ['presence'],
         'domain_of': ['SbeSimpleTypeV1',
                       'SbeFieldV1',
                       'SbeMemberTypeV2',
                       'SbeFieldV2'],
         'ifabsent': 'string(required)'} })
    null_value: Optional[str] = Field(default=None, description="""The value that stands for null in place of the primitive type's default, written as text.""", json_schema_extra = { "linkml_meta": {'aliases': ['nullValue'],
         'domain_of': ['SbeSimpleTypeV1', 'SbeMemberTypeV2', 'SbeFieldV2']} })
    min_value: Optional[str] = Field(default=None, description="""The lowest value allowed, written as text.""", json_schema_extra = { "linkml_meta": {'aliases': ['minValue'],
         'domain_of': ['SbeSimpleTypeV1', 'SbeMemberTypeV2', 'SbeFieldV2']} })
    max_value: Optional[str] = Field(default=None, description="""The highest value allowed, written as text.""", json_schema_extra = { "linkml_meta": {'aliases': ['maxValue'],
         'domain_of': ['SbeSimpleTypeV1', 'SbeMemberTypeV2', 'SbeFieldV2']} })
    value_ref: Optional[str] = Field(default=None, description="""The valid value that gives a constant element its value.""", json_schema_extra = { "linkml_meta": {'aliases': ['valueRef'],
         'domain_of': ['SbeSimpleTypeV1',
                       'SbeFieldV1',
                       'SbeMemberTypeV2',
                       'SbeFieldV2']} })
    semantic_type: Optional[str] = Field(default=None, description="""The FIX datatype this field carries.""", json_schema_extra = { "linkml_meta": {'aliases': ['semanticType'],
         'annotations': {'xsd_type': {'tag': 'xsd_type', 'value': 'xs:token'}},
         'domain_of': ['SbeEncodingV1',
                       'SbeBlockV1Mixin',
                       'SbeFieldV1',
                       'SbeBlockV2Mixin',
                       'SbeFieldV2']} })
    description: Optional[str] = Field(default=None, description="""Free text about this element, for the people who read the schema.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'domain_of': ['SbeValidValue',
                       'SbeChoice',
                       'SbeMessageSchemaV1',
                       'SbeEncodingV1',
                       'SbeBlockV1Mixin',
                       'SbeFieldV1',
                       'SbeMessageSchemaV2',
                       'SbeEncodingSetV2',
                       'SbeMessageSetV2',
                       'SbeElementV2',
                       'SbeBlockV2Mixin',
                       'SbeFieldV2'],
         'slot_uri': 'schema:description'} })
    since_version: Optional[int] = Field(default=0, description="""The schema version that added this element.""", ge=0, json_schema_extra = { "linkml_meta": {'aliases': ['sinceVersion'],
         'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '5: Since version'},
                         'xsd_type': {'tag': 'xsd_type',
                                      'value': 'xs:nonNegativeInteger'}},
         'domain_of': ['SbeVersionedMixin'],
         'ifabsent': 'int(0)'} })
    deprecated_since: Optional[int] = Field(default=None, description="""The schema version that retired this element, which stays only for older applications.""", ge=0, json_schema_extra = { "linkml_meta": {'aliases': ['deprecated'],
         'annotations': {'sbe_section': {'tag': 'sbe_section',
                                         'value': '5: Deprecated elements'},
                         'xsd_type': {'tag': 'xsd_type',
                                      'value': 'xs:nonNegativeInteger'}},
         'domain_of': ['SbeVersionedMixin']} })

    @field_validator('symbolic_name')
    def pattern_symbolic_name(cls, v):
        pattern=re.compile(r"^[A-Za-z_][0-9A-Za-z_]{0,63}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid symbolic_name format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid symbolic_name format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('encoding_name')
    def pattern_encoding_name(cls, v):
        pattern=re.compile(r"^[A-Za-z_][0-9A-Za-z_]{0,63}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid encoding_name format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid encoding_name format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('element_value')
    def pattern_element_value(cls, v):
        pattern=re.compile(r"^\S+( \S+)*$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid element_value format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid element_value format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('value_ref')
    def pattern_value_ref(cls, v):
        pattern=re.compile(r"^[A-Za-z_][0-9A-Za-z_]*\.[A-Za-z_][0-9A-Za-z_]*$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid value_ref format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid value_ref format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('semantic_type')
    def pattern_semantic_type(cls, v):
        pattern=re.compile(r"^\S+( \S+)*$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid semantic_type format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid semantic_type format: {v}"
            raise ValueError(err_msg)
        return v


# Model rebuild
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model
SbeVersionedMixin.model_rebuild()
SbeValidValue.model_rebuild()
SbeChoice.model_rebuild()
SbeMessageSchemaV1.model_rebuild()
SbeEncodingSetV1.model_rebuild()
SbeMemberV1.model_rebuild()
SbeRefV1.model_rebuild()
SbeEncodingV1.model_rebuild()
SbeSimpleTypeV1.model_rebuild()
SbeCompositeV1.model_rebuild()
SbeEnumV1.model_rebuild()
SbeSetV1.model_rebuild()
SbeBlockV1Mixin.model_rebuild()
SbeMessageV1.model_rebuild()
SbeGroupV1.model_rebuild()
SbeFieldV1.model_rebuild()
SbeMessageSchemaV2.model_rebuild()
SbeEncodingSetV2.model_rebuild()
SbeMessageSetV2.model_rebuild()
SbeElementV2.model_rebuild()
SbeMemberV2.model_rebuild()
SbeSimpleTypeV2.model_rebuild()
SbeMemberTypeV2.model_rebuild()
SbeRefV2.model_rebuild()
SbeCompositeV2.model_rebuild()
SbeEnumV2.model_rebuild()
SbeSetV2.model_rebuild()
SbeBlockV2Mixin.model_rebuild()
SbeMessageV2.model_rebuild()
SbeGroupV2.model_rebuild()
SbeFieldV2.model_rebuild()
