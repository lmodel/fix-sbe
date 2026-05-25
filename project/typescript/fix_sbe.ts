/**
* Inline enumeration lifted from XSD attribute ``presence`` on ``presenceAttributes``.
*/
export enum Presence {
    
    /** The value must always be populated */
    required = "required",
    /** Value may be set to nullValue for its data type */
    optional = "optional",
    /** Value does not vary so it need not be serialized on the wire */
    constant = "constant",
};
/**
* Inline enumeration lifted from XSD attribute ``byteOrder`` on ``messageSchema``.
*/
export enum ByteOrder {
    
    bigEndian = "bigEndian",
    littleEndian = "littleEndian",
};
/**
* Inline enumeration lifted from XSD attribute ``primitiveType`` on ``encodedDataType``.
*/
export enum PrimitiveTypeV1 {
    
    char = "char",
    int8 = "int8",
    int16 = "int16",
    int32 = "int32",
    int64 = "int64",
    uint8 = "uint8",
    uint16 = "uint16",
    uint32 = "uint32",
    uint64 = "uint64",
    float = "float",
    double = "double",
};
/**
* Inline enumeration lifted from XSD attribute ``primitiveType`` on ``primitiveTypeAttributes``.
*/
export enum PrimitiveTypeV2 {
    
    /** A value of a single-byte character set */
    char = "char",
    int8 = "int8",
    int16 = "int16",
    int32 = "int32",
    int64 = "int64",
    uint8 = "uint8",
    uint16 = "uint16",
    uint32 = "uint32",
    uint64 = "uint64",
    float = "float",
    double = "double",
};


/**
 * Application layer class. Maps a field to a FIX data type or a template to a FIX message.
 */
export interface SemanticAttributes {
    semantic_type?: string,
    description?: string,
}


/**
 * Schema versioning supports message extension
 */
export interface VersionAttributes {
    /** The schema version in which an element was added */
    since_version?: number,
    /** The version of the schema in which an element was deprecated. It is retained for back compatibility but should no longer be used by updated applications. It may be removed in a later version. */
    deprecated?: number,
}


/**
 * Valid value as a string
 */
export interface ValidValue extends VersionAttributes {
    name: string,
    description?: string,
    /** Text content of the element. For SBE this carries the constant or default value (e.g. ``<type presence='constant'>-3</type>``). */
    value?: string,
}


/**
 * A choice within a multi value set. Value is the position within a bitset (zero-based index).
 */
export interface Choice extends VersionAttributes {
    name: string,
    description?: string,
    /** Text content of the element. For SBE this carries the constant or default value (e.g. ``<type presence='constant'>-3</type>``). */
    value?: string,
}



export interface AlignmentAttributesV1 {
    /** Offset from start of a composite type or block as a zero-based index. */
    offset?: number,
}



export interface PresenceAttributesV1 {
    presence?: string,
    /** A constant value as valid value of an enum in the form enum-name.valid-value-name */
    value_ref?: string,
}


/**
 * Base type of message and repeating group entry
 */
export interface BlockTypeV1 extends SemanticAttributes, VersionAttributes {
    /** Fixed-length fields */
    field?: FieldTypeV1[],
    group?: GroupTypeV1[],
    /** Variable-length fields */
    data?: FieldTypeV1[],
    name: string,
    /** Unique ID of a message template */
    id: number,
    /** Space reserved for root level of message, not include groups or variable-length data elements. */
    block_length?: number,
}


/**
 * A repeating group contains an array of entries
 */
export interface GroupTypeV1 extends BlockTypeV1 {
    dimension_type?: string,
}


/**
 * Simple wire encoding consisting of a primitive type or array of primitives
 */
export interface EncodedDataTypeV1 extends AlignmentAttributesV1, PresenceAttributesV1, SemanticAttributes, VersionAttributes {
    name: string,
    /** Override of default null indicator for the data type in SBE specification, as a string. */
    null_value?: string,
    min_value?: string,
    max_value?: string,
    length?: number,
    primitive_type: string,
    character_encoding?: string,
    /** Text content of the element. For SBE this carries the constant or default value (e.g. ``<type presence='constant'>-3</type>``). */
    value?: string,
}


/**
 * A wire encoding composed of multiple parts
 */
export interface CompositeDataTypeV1 extends AlignmentAttributesV1, SemanticAttributes, VersionAttributes {
    type?: EncodedDataTypeV1[],
    enum?: EnumTypeV1[],
    set?: SetTypeV1[],
    composite?: CompositeDataTypeV1[],
    ref?: RefTypeV1[],
    name: string,
    /** Text content of the element. For SBE this carries the constant or default value (e.g. ``<type presence='constant'>-3</type>``). */
    value?: string,
}


/**
 * An enumeration of valid values
 */
export interface EnumTypeV1 extends AlignmentAttributesV1, SemanticAttributes, VersionAttributes {
    valid_value: ValidValue[],
    name: string,
    encoding_type: string,
    /** Text content of the element. For SBE this carries the constant or default value (e.g. ``<type presence='constant'>-3</type>``). */
    value?: string,
}


/**
 * A reference to any existing encoding type (simple type, enum or set) to reuse as a member of a composite type
 */
export interface RefTypeV1 extends AlignmentAttributesV1, VersionAttributes {
    name: string,
    type: string,
    /** Text content of the element. For SBE this carries the constant or default value (e.g. ``<type presence='constant'>-3</type>``). */
    value?: string,
}


/**
 * A multi value choice (encoded as a bitset)
 */
export interface SetTypeV1 extends AlignmentAttributesV1, SemanticAttributes, VersionAttributes {
    choice: Choice[],
    name: string,
    encoding_type: string,
    /** Text content of the element. For SBE this carries the constant or default value (e.g. ``<type presence='constant'>-3</type>``). */
    value?: string,
}


/**
 * A field of a message of a specified dataType
 */
export interface FieldTypeV1 extends AlignmentAttributesV1, PresenceAttributesV1, SemanticAttributes, VersionAttributes {
    name: string,
    id: number,
    /** Must match the name of an encoding contained by 'types' element */
    type: string,
    epoch?: string,
    /** Deprecated - only for back compatibility with RC2 */
    time_unit?: string,
}


/**
 * Root of XML document, holds all message templates and their elements
 */
export interface MessageSchemaV1 {
    /** More than one set of types may be provided. Names must be unique across all encoding types. Encoding types may appear in any order. */
    types: string[],
    message: MessageV1[],
    package?: string,
    /** Unique ID of a message schema */
    id?: number,
    /** The version of a message schema. Initial version is 0. */
    version: number,
    /** Application layer specification version, such as FIX version 'FIX.5.0SP2' */
    semantic_version?: string,
    description?: string,
    byte_order?: string,
    /** Name of the encoding type of the message header, which is the same for all messages in a schema. The name has a default, but an encoding of that name must be present under a 'types' element. */
    header_type?: string,
}


/**
 * A message type, also known as a message template
 */
export interface MessageV1 extends BlockTypeV1 {
}



export interface AlignmentAttributesV2 {
    /** Byte alignment of the start of a block (message root or repeating group instance). */
    alignment?: number,
}



export interface OffsetAttributesV2 {
    /** Offset from start of a composite type or block as a zero-based index. */
    offset?: number,
    /** Byte alignment of the start of a block (message root or repeating group instance). */
    alignment?: number,
}



export interface PresenceAttributesV2 {
    presence?: string,
    /** Override of default null indicator for the data type in SBE specification, as a string. */
    null_value?: string,
    /** Lower bound of a range */
    min_value?: string,
    /** Upper bound of a range */
    max_value?: string,
    /** A constant value as valid value of an enum in the form enum-name.valid-value-name. Only valid if presence='constant'. */
    value_ref?: string,
}



export interface PrimitiveTypeAttributesV2 {
    primitive_type: string,
    length?: number,
    /** Character set or Unicode encoding scheme */
    character_encoding?: string,
}


/**
 * Base type of message and repeating group entry
 */
export interface BlockTypeV2 extends AlignmentAttributesV2, SemanticAttributes, VersionAttributes {
    /** Fixed-length fields */
    field?: FieldTypeV2[],
    group?: GroupTypeV2[],
    /** Variable-length fields */
    data?: FieldTypeV2[],
    name: string,
    /** Unique ID of a message template */
    id: number,
    /** Space reserved for root level of message or repeating group, not including nested groups or variable-length data elements. */
    block_length?: number,
}


/**
 * A repeating group contains an array of entries
 */
export interface GroupTypeV2 extends BlockTypeV2 {
    dimension_type?: string,
}


/**
 * Simple wire encoding consisting of a primitive type or array of primitives
 */
export interface SimpleDataTypeV2 extends PrimitiveTypeAttributesV2, VersionAttributes {
    name: string,
    description?: string,
    /** Text content of the element. For SBE this carries the constant or default value (e.g. ``<type presence='constant'>-3</type>``). */
    value?: string,
}


/**
 * A simple type used as a member of a composite type
 */
export interface MemberDataTypeV2 extends PrimitiveTypeAttributesV2, OffsetAttributesV2, PresenceAttributesV2 {
    name: string,
    description?: string,
    /** Text content of the element. For SBE this carries the constant or default value (e.g. ``<type presence='constant'>-3</type>``). */
    value?: string,
}


/**
 * A wire encoding composed of multiple parts
 */
export interface CompositeDataTypeV2 extends OffsetAttributesV2, VersionAttributes {
    type?: MemberDataTypeV2[],
    enum?: EnumTypeV2[],
    set?: SetTypeV2[],
    composite?: CompositeDataTypeV2[],
    ref?: RefTypeV2[],
    name: string,
    description?: string,
    /** Text content of the element. For SBE this carries the constant or default value (e.g. ``<type presence='constant'>-3</type>``). */
    value?: string,
}


/**
 * An enumeration of valid values
 */
export interface EnumTypeV2 extends OffsetAttributesV2, VersionAttributes {
    valid_value: ValidValue[],
    name: string,
    encoding_type: string,
    description?: string,
    /** Text content of the element. For SBE this carries the constant or default value (e.g. ``<type presence='constant'>-3</type>``). */
    value?: string,
}


/**
 * A reference to any existing encoding type (simple type, enum or set) to reuse as a member of a composite type
 */
export interface RefTypeV2 extends OffsetAttributesV2 {
    name: string,
    type: string,
    /** How the referenced type is used */
    description?: string,
    /** Text content of the element. For SBE this carries the constant or default value (e.g. ``<type presence='constant'>-3</type>``). */
    value?: string,
}


/**
 * A multi value choice (encoded as a bitset)
 */
export interface SetTypeV2 extends OffsetAttributesV2, VersionAttributes {
    choice: Choice[],
    name: string,
    encoding_type: string,
    description?: string,
    /** Text content of the element. For SBE this carries the constant or default value (e.g. ``<type presence='constant'>-3</type>``). */
    value?: string,
}


/**
 * A field of a message of a specified dataType
 */
export interface FieldTypeV2 extends OffsetAttributesV2, PresenceAttributesV2, SemanticAttributes, VersionAttributes {
    name: string,
    id: number,
    /** Must match the name of an encoding contained by 'types' element */
    type: string,
    /** Text content of the element. For SBE this carries the constant or default value (e.g. ``<type presence='constant'>-3</type>``). */
    value?: string,
}


/**
 * Root of XML document, holds all message templates and their elements
 */
export interface MessageSchemaV2 {
    types: TypesV2[],
    messages: MessagesV2[],
    package?: string,
    /** Unique ID of a message schema */
    id?: number,
    /** The version of a message schema. Initial version is 0. */
    version: number,
    /** Application layer specification version, such as FIX version 'FIX.5.0SP2' */
    semantic_version?: string,
    description?: string,
    byte_order?: string,
    /** Name of the encoding type of the message header, which is the same for all messages in a schema. The name has a default, but an encoding of that name must be present under a 'types' element. */
    header_type?: string,
}



export interface MessagesV2 {
    /** A message type, also known as a message template */
    message: BlockTypeV2[],
    description?: string,
    /** Overrides the messageSchema package */
    package?: string,
}


/**
 * More than one set of types may be provided. Names must be unique across all encoding types. Encoding types may appear in any order.
 */
export interface TypesV2 {
    type?: SimpleDataTypeV2[],
    composite?: CompositeDataTypeV2[],
    enum?: EnumTypeV2[],
    set?: SetTypeV2[],
    description?: string,
    /** Overrides the messageSchema package */
    package?: string,
}



