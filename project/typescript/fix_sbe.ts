/**
* Whether a value is on the wire, and whether it may be null.
*/
export enum SbePresence {
    
    /** A value is always sent, and it is never tested for null. */
    required = "required",
    /** A value is sent, and a null marker says that none is set. */
    optional = "optional",
    /** The schema states the value, so nothing is sent. */
    constant = "constant",
};
/**
* The order of the octets in every multi-octet number of a message.
*/
export enum SbeByteOrder {
    
    /** The most significant octet comes first. */
    bigEndian = "bigEndian",
    /** The least significant octet comes first. */
    littleEndian = "littleEndian",
};
/**
* The wire types every encoding is finally built from.
*/
export enum SbePrimitiveType {
    
    /** One character of one octet. */
    char = "char",
    /** A signed integer of one octet. */
    int8 = "int8",
    /** A signed integer of two octets. */
    int16 = "int16",
    /** A signed integer of four octets. */
    int32 = "int32",
    /** A signed integer of eight octets. */
    int64 = "int64",
    /** An unsigned integer of one octet. */
    uint8 = "uint8",
    /** An unsigned integer of two octets. */
    uint16 = "uint16",
    /** An unsigned integer of four octets. */
    uint32 = "uint32",
    /** An unsigned integer of eight octets. */
    uint64 = "uint64",
    /** A four-octet number in binary floating point. */
    float = "float",
    /** An eight-octet number in binary floating point. */
    double = "double",
};
/**
* The FIX datatypes the specification's summary table lists as a field's or an encoding's semantic type.
*/
export enum SbeFixDatatype {
    
    int = "int",
    Length = "Length",
    TagNum = "TagNum",
    SeqNum = "SeqNum",
    NumInGroup = "NumInGroup",
    DayOfMonth = "DayOfMonth",
    Qty = "Qty",
    float = "float",
    Price = "Price",
    PriceOffset = "PriceOffset",
    Amt = "Amt",
    Percentage = "Percentage",
    char = "char",
    String = "String",
    EncodedText = "EncodedText",
    XMLData = "XMLData",
    data = "data",
    Country = "Country",
    Currency = "Currency",
    Exchange = "Exchange",
    Language = "Language",
    Boolean = "Boolean",
    MultipleCharValue = "MultipleCharValue",
    MultipleStringValue = "MultipleStringValue",
    MonthYear = "MonthYear",
    UTCTimestamp = "UTCTimestamp",
    UTCTimeOnly = "UTCTimeOnly",
    UTCDateOnly = "UTCDateOnly",
    LocalMktDate = "LocalMktDate",
    TZTimeOnly = "TZTimeOnly",
    TZTimestamp = "TZTimestamp",
};


/**
 * The two attributes that record when an element entered a schema and when it should leave.
 */
export interface SbeVersionedMixin {
    /** The schema version that added this element. */
    since_version?: number,
    /** The schema version that retired this element, which stays only for older applications. */
    deprecated_since?: number,
}


/**
 * One of the values an enumeration allows.
 */
export interface SbeValidValue extends SbeVersionedMixin {
    /** What the schema calls this element. */
    symbolic_name: string,
    /** Free text about this element, for the people who read the schema. */
    description?: string,
    /** The value as it is written in the schema, which must convert to the enumeration's encoding. */
    valid_value: string,
}


/**
 * One of the alternatives of a set, which is one bit of its encoding.
 */
export interface SbeChoice extends SbeVersionedMixin {
    /** What the schema calls this element. */
    symbolic_name: string,
    /** Free text about this element, for the people who read the schema. */
    description?: string,
    /** Which bit stands for this choice, counted from zero at the least significant. */
    bit_position: number,
}


/**
 * One SBE 1.0 message schema, with its encodings and message templates.
 */
export interface SbeMessageSchemaV1 {
    /** The name or category that a set of counterparties knows this schema or part of it by. */
    schema_package?: string,
    /** The number that identifies this schema between counterparties. */
    sbe_id?: number,
    /** The version of this message schema, starting at zero. */
    schema_version: number,
    /** The version of FIX whose meanings this schema uses. */
    semantic_version?: string,
    /** Free text about this element, for the people who read the schema. */
    description?: string,
    /** How the octets of every number in this schema's messages are ordered. */
    byte_order?: string,
    /** The composite, by name, that sends each message's header in this schema. */
    header_type?: string,
    /** The sets of encodings this schema's messages use. */
    encoding_sets: SbeEncodingSetV1[],
    /** The message templates of this set. */
    messages: SbeMessageV1[],
}


/**
 * A set of encodings, listed in any order, whose names are unique across the whole schema.
 */
export interface SbeEncodingSetV1 {
    /** The encodings of this set. */
    encodings: SbeEncodingV1[],
}


/**
 * Anything a composite may hold in the order it is sent.
 */
export interface SbeMemberV1 extends SbeVersionedMixin {
    /** The class of this encoding or composite member, which stands for its XML element. */
    encoding_kind: string,
    /** What the schema calls this element. */
    symbolic_name: string,
    /** The octet this element starts at, counted from zero at the start of its block or composite. */
    offset?: number,
}


/**
 * A composite's member that reuses an encoding defined elsewhere in the schema.
 */
export interface SbeRefV1 extends SbeMemberV1 {
    /** Which encoding this element uses, by name. */
    encoding_name: string,
}


/**
 * An encoding of SBE 1.0, which says how a value is laid out on the wire.
 */
export interface SbeEncodingV1 extends SbeMemberV1 {
    /** The FIX datatype this encoding carries. */
    semantic_type?: string,
    /** Free text about this element, for the people who read the schema. */
    description?: string,
}


/**
 * An encoding backed by one primitive value, or several in an array.
 */
export interface SbeSimpleTypeV1 extends SbeEncodingV1 {
    /** The text of the XML element, which is the constant when presence is constant. */
    element_value?: string,
    /** The wire type under this encoding. */
    primitive_type: string,
    /** How many values of the primitive type the encoding holds, where zero means a variable number. */
    array_length?: number,
    /** Which character set, or which Unicode scheme, character data follows. */
    character_encoding?: string,
    /** The value that stands for null in place of the primitive type's default, written as text. */
    null_value?: string,
    /** The lowest value allowed, written as text. */
    min_value?: string,
    /** The highest value allowed, written as text. */
    max_value?: string,
    /** Whether this element's value is required, optional or constant. */
    presence?: string,
    /** The valid value that gives a constant element its value. */
    value_ref?: string,
}


/**
 * An encoding built from members sent one after another, such as a decimal's mantissa and exponent.
 */
export interface SbeCompositeV1 extends SbeEncodingV1 {
    /** The members of this composite, in the order they are sent. */
    composite_members: SbeMemberV1[],
}


/**
 * An encoding whose value is one of a listed set of valid values.
 */
export interface SbeEnumV1 extends SbeEncodingV1 {
    /** The simple encoding or primitive type that an enumeration or set is sent as. */
    encoding_type: string,
    /** The values this enumeration allows. */
    valid_values: SbeValidValue[],
}


/**
 * An encoding whose value is any combination of up to 64 choices, sent as a bitset.
 */
export interface SbeSetV1 extends SbeEncodingV1 {
    /** The simple encoding or primitive type that an enumeration or set is sent as. */
    encoding_type: string,
    /** The alternatives of this set. */
    choices: SbeChoice[],
}


/**
 * The body shared by a message and a group entry, which holds its fixed-length fields first, then groups, then variable-length data.
 */
export interface SbeBlockV1Mixin {
    /** What the schema calls this element. */
    symbolic_name: string,
    /** The number that identifies this element. */
    sbe_id: number,
    /** The octets set aside for a message's fixed-length fields, or for those of each group entry. */
    block_length?: number,
    /** What this element means at the FIX application layer. */
    semantic_type?: string,
    /** Free text about this element, for the people who read the schema. */
    description?: string,
    /** Fixed-length fields, listed in wire order. */
    block_fields?: SbeFieldV1[],
    /** Repeating groups, listed in wire order. */
    repeating_groups?: SbeGroupV1[],
    /** Variable-length fields, listed in wire order. */
    var_data_fields?: SbeFieldV1[],
}


/**
 * A message template, whose number and block length are sent in each message's header.
 */
export interface SbeMessageV1 extends SbeVersionedMixin, SbeBlockV1Mixin {
}


/**
 * A repeating group, whose entries each hold the same fields, and which cannot be without a field.
 */
export interface SbeGroupV1 extends SbeVersionedMixin, SbeBlockV1Mixin {
    /** The composite, by name, that sends a repeating group's entry count and entry size. */
    dimension_type?: string,
}


/**
 * A message's or group entry's field, which uses an encoding at a place in its block.
 */
export interface SbeFieldV1 extends SbeVersionedMixin {
    /** What the schema calls this element. */
    symbolic_name: string,
    /** The field's FIX tag number. */
    sbe_id: number,
    /** Which encoding this element uses, by name. */
    encoding_name: string,
    /** The octet this element starts at, counted from zero at the start of its block or composite. */
    offset?: number,
    /** Whether this element's value is required, optional or constant. */
    presence?: string,
    /** The valid value that gives a constant element its value. */
    value_ref?: string,
    /** The FIX datatype this field carries. */
    semantic_type?: string,
    /** Free text about this element, for the people who read the schema. */
    description?: string,
    /** Where the period a time value counts from begins. */
    time_epoch?: string,
    /** The unit of a time value. */
    time_unit?: string,
}


/**
 * One SBE 2.0 message schema, with its encodings and message templates.
 */
export interface SbeMessageSchemaV2 {
    /** The name or category that a set of counterparties knows this schema or part of it by. */
    schema_package?: string,
    /** The number that identifies this schema between counterparties. */
    sbe_id?: number,
    /** The version of this message schema, starting at zero. */
    schema_version: number,
    /** The version of FIX whose meanings this schema uses. */
    semantic_version?: string,
    /** Free text about this element, for the people who read the schema. */
    description?: string,
    /** How the octets of every number in this schema's messages are ordered. */
    byte_order?: string,
    /** The composite, by name, that sends each message's header in this schema. */
    header_type?: string,
    /** The sets of encodings this schema's messages use. */
    encoding_sets: SbeEncodingSetV2[],
    /** The sets of message templates of this schema. */
    message_sets: SbeMessageSetV2[],
}


/**
 * A set of encodings, in any order, that may have its own package and may come from another file.
 */
export interface SbeEncodingSetV2 {
    /** Free text about this element, for the people who read the schema. */
    description?: string,
    /** A package for this set in place of the schema's. */
    schema_package?: string,
    /** The base address that the XML Inclusion mechanism records on an element it brought in from another file. */
    xml_base?: string,
    /** The encodings of this set. */
    encodings: SbeElementV2[],
}


/**
 * Message templates held together, which may have their own package and may come from another file.
 */
export interface SbeMessageSetV2 {
    /** Free text about this element, for the people who read the schema. */
    description?: string,
    /** A package for this set in place of the schema's. */
    schema_package?: string,
    /** The base address that the XML Inclusion mechanism records on an element it brought in from another file. */
    xml_base?: string,
    /** The message templates of this set. */
    messages: SbeMessageV2[],
}


/**
 * Anything that sets of encodings or composites hold, and the name and text they all have.
 */
export interface SbeElementV2 {
    /** The class of this encoding or composite member, which stands for its XML element. */
    encoding_kind: string,
    /** What the schema calls this element. */
    symbolic_name: string,
    /** Free text about this element, for the people who read the schema. */
    description?: string,
}


/**
 * Anything a composite may hold in the order it is sent.
 */
export interface SbeMemberV2 extends SbeElementV2 {
    /** The octet this element starts at, counted from zero at the start of its block or composite. */
    offset?: number,
    /** The multiple of octets the start of this element is placed on. */
    alignment?: number,
}


/**
 * A simple encoding that stands alone in a set, backed by one primitive value, or several in an array.
 */
export interface SbeSimpleTypeV2 extends SbeElementV2, SbeVersionedMixin {
    /** The text of the XML element, which is the constant when presence is constant. */
    element_value?: string,
    /** The wire type under this encoding. */
    primitive_type: string,
    /** How many values of the primitive type the encoding holds, where zero means a variable number. */
    array_length?: number,
    /** Which character set, or which Unicode scheme, character data follows. */
    character_encoding?: string,
}


/**
 * A simple encoding inside a composite, which may say it is optional or constant.
 */
export interface SbeMemberTypeV2 extends SbeMemberV2 {
    /** The text of the XML element, which is the constant when presence is constant. */
    element_value?: string,
    /** The wire type under this encoding. */
    primitive_type: string,
    /** How many values of the primitive type the encoding holds, where zero means a variable number. */
    array_length?: number,
    /** Which character set, or which Unicode scheme, character data follows. */
    character_encoding?: string,
    /** Whether this element's value is required, optional or constant. */
    presence?: string,
    /** The value that stands for null in place of the primitive type's default, written as text. */
    null_value?: string,
    /** The lowest value allowed, written as text. */
    min_value?: string,
    /** The highest value allowed, written as text. */
    max_value?: string,
    /** The valid value that gives a constant element its value. */
    value_ref?: string,
}


/**
 * A composite's member that reuses an encoding defined elsewhere in the schema.
 */
export interface SbeRefV2 extends SbeMemberV2 {
    /** Which encoding this element uses, by name. */
    encoding_name: string,
}


/**
 * An encoding built from members sent one after another, such as a decimal's mantissa and exponent.
 */
export interface SbeCompositeV2 extends SbeMemberV2, SbeVersionedMixin {
    /** The members of this composite, in the order they are sent. */
    composite_members: SbeMemberV2[],
}


/**
 * An encoding whose value is one of a listed set of valid values.
 */
export interface SbeEnumV2 extends SbeMemberV2, SbeVersionedMixin {
    /** The simple encoding or primitive type that an enumeration or set is sent as. */
    encoding_type: string,
    /** The values this enumeration allows. */
    valid_values: SbeValidValue[],
}


/**
 * An encoding whose value is any combination of up to 64 choices, sent as a bitset.
 */
export interface SbeSetV2 extends SbeMemberV2, SbeVersionedMixin {
    /** The simple encoding or primitive type that an enumeration or set is sent as. */
    encoding_type: string,
    /** The alternatives of this set. */
    choices: SbeChoice[],
}


/**
 * The body shared by a message and a group entry, which holds its fixed-length fields first, then groups, then variable-length data.
 */
export interface SbeBlockV2Mixin {
    /** What the schema calls this element. */
    symbolic_name: string,
    /** The number that identifies this element. */
    sbe_id: number,
    /** The octets set aside for a message's fixed-length fields, or for those of each group entry. */
    block_length?: number,
    /** The multiple of octets where a message or each group entry begins. */
    alignment?: number,
    /** What this element means at the FIX application layer. */
    semantic_type?: string,
    /** Free text about this element, for the people who read the schema. */
    description?: string,
    /** Fixed-length fields, listed in wire order. */
    block_fields?: SbeFieldV2[],
    /** Repeating groups, listed in wire order. */
    repeating_groups?: SbeGroupV2[],
    /** Variable-length fields, listed in wire order. */
    var_data_fields?: SbeFieldV2[],
}


/**
 * A message template, whose number and block length are sent in each message's header.
 */
export interface SbeMessageV2 extends SbeVersionedMixin, SbeBlockV2Mixin {
}


/**
 * A repeating group, whose entries each hold the same fields, and which cannot be without a field.
 */
export interface SbeGroupV2 extends SbeVersionedMixin, SbeBlockV2Mixin {
    /** The composite, by name, that sends a repeating group's entry count and entry size. */
    dimension_type?: string,
}


/**
 * A message's or group entry's field, which uses an encoding at a place in its block and may state a constant.
 */
export interface SbeFieldV2 extends SbeVersionedMixin {
    /** What the schema calls this element. */
    symbolic_name: string,
    /** The field's FIX tag number. */
    sbe_id: number,
    /** Which encoding this element uses, by name. */
    encoding_name: string,
    /** The text of the XML element, which is the constant when presence is constant. */
    element_value?: string,
    /** The octet this element starts at, counted from zero at the start of its block or composite. */
    offset?: number,
    /** The multiple of octets the start of this field is placed on, in place of an offset. */
    alignment?: number,
    /** Whether this element's value is required, optional or constant. */
    presence?: string,
    /** The value that stands for null in place of the primitive type's default, written as text. */
    null_value?: string,
    /** The lowest value allowed, written as text. */
    min_value?: string,
    /** The highest value allowed, written as text. */
    max_value?: string,
    /** The valid value that gives a constant element its value. */
    value_ref?: string,
    /** The FIX datatype this field carries. */
    semantic_type?: string,
    /** Free text about this element, for the people who read the schema. */
    description?: string,
}



