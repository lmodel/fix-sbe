-- # Class: SemanticAttributes Description: Application layer class. Maps a field to a FIX data type or a template to a FIX message.
--     * Slot: id
--     * Slot: semantic_type
--     * Slot: description
-- # Class: VersionAttributes Description: Schema versioning supports message extension
--     * Slot: id
--     * Slot: since_version Description: The schema version in which an element was added
--     * Slot: deprecated Description: The version of the schema in which an element was deprecated. It is retained for back compatibility but should no longer be used by updated applications. It may be removed in a later version.
-- # Class: ValidValue Description: Valid value as a string
--     * Slot: id
--     * Slot: name
--     * Slot: description
--     * Slot: value Description: Text content of the element. For SBE this carries the constant or default value (e.g. ``<type presence='constant'>-3</type>``).
--     * Slot: since_version Description: The schema version in which an element was added
--     * Slot: deprecated Description: The version of the schema in which an element was deprecated. It is retained for back compatibility but should no longer be used by updated applications. It may be removed in a later version.
--     * Slot: EnumTypeV1_id Description: Autocreated FK slot
--     * Slot: EnumTypeV2_id Description: Autocreated FK slot
-- # Class: Choice Description: A choice within a multi value set. Value is the position within a bitset (zero-based index).
--     * Slot: id
--     * Slot: name
--     * Slot: description
--     * Slot: value Description: Text content of the element. For SBE this carries the constant or default value (e.g. ``<type presence='constant'>-3</type>``).
--     * Slot: since_version Description: The schema version in which an element was added
--     * Slot: deprecated Description: The version of the schema in which an element was deprecated. It is retained for back compatibility but should no longer be used by updated applications. It may be removed in a later version.
--     * Slot: SetTypeV1_id Description: Autocreated FK slot
--     * Slot: SetTypeV2_id Description: Autocreated FK slot
-- # Class: AlignmentAttributesV1
--     * Slot: id
--     * Slot: offset Description: Offset from start of a composite type or block as a zero-based index.
-- # Class: PresenceAttributesV1
--     * Slot: id
--     * Slot: presence
--     * Slot: value_ref Description: A constant value as valid value of an enum in the form enum-name.valid-value-name
-- # Class: BlockTypeV1 Description: Base type of message and repeating group entry
--     * Slot: uid
--     * Slot: name
--     * Slot: id Description: Unique ID of a message template
--     * Slot: block_length Description: Space reserved for root level of message, not include groups or variable-length data elements.
--     * Slot: semantic_type
--     * Slot: description
--     * Slot: since_version Description: The schema version in which an element was added
--     * Slot: deprecated Description: The version of the schema in which an element was deprecated. It is retained for back compatibility but should no longer be used by updated applications. It may be removed in a later version.
-- # Class: GroupTypeV1 Description: A repeating group contains an array of entries
--     * Slot: uid
--     * Slot: dimension_type
--     * Slot: name
--     * Slot: id Description: Unique ID of a message template
--     * Slot: block_length Description: Space reserved for root level of message, not include groups or variable-length data elements.
--     * Slot: semantic_type
--     * Slot: description
--     * Slot: since_version Description: The schema version in which an element was added
--     * Slot: deprecated Description: The version of the schema in which an element was deprecated. It is retained for back compatibility but should no longer be used by updated applications. It may be removed in a later version.
--     * Slot: BlockTypeV1_uid Description: Autocreated FK slot
--     * Slot: GroupTypeV1_uid Description: Autocreated FK slot
--     * Slot: MessageV1_uid Description: Autocreated FK slot
-- # Class: EncodedDataTypeV1 Description: Simple wire encoding consisting of a primitive type or array of primitives
--     * Slot: id
--     * Slot: name
--     * Slot: null_value Description: Override of default null indicator for the data type in SBE specification, as a string.
--     * Slot: min_value
--     * Slot: max_value
--     * Slot: length
--     * Slot: primitive_type
--     * Slot: character_encoding
--     * Slot: value Description: Text content of the element. For SBE this carries the constant or default value (e.g. ``<type presence='constant'>-3</type>``).
--     * Slot: offset Description: Offset from start of a composite type or block as a zero-based index.
--     * Slot: presence
--     * Slot: value_ref Description: A constant value as valid value of an enum in the form enum-name.valid-value-name
--     * Slot: semantic_type
--     * Slot: description
--     * Slot: since_version Description: The schema version in which an element was added
--     * Slot: deprecated Description: The version of the schema in which an element was deprecated. It is retained for back compatibility but should no longer be used by updated applications. It may be removed in a later version.
--     * Slot: CompositeDataTypeV1_id Description: Autocreated FK slot
-- # Class: CompositeDataTypeV1 Description: A wire encoding composed of multiple parts
--     * Slot: id
--     * Slot: name
--     * Slot: value Description: Text content of the element. For SBE this carries the constant or default value (e.g. ``<type presence='constant'>-3</type>``).
--     * Slot: offset Description: Offset from start of a composite type or block as a zero-based index.
--     * Slot: semantic_type
--     * Slot: description
--     * Slot: since_version Description: The schema version in which an element was added
--     * Slot: deprecated Description: The version of the schema in which an element was deprecated. It is retained for back compatibility but should no longer be used by updated applications. It may be removed in a later version.
--     * Slot: CompositeDataTypeV1_id Description: Autocreated FK slot
-- # Class: EnumTypeV1 Description: An enumeration of valid values
--     * Slot: id
--     * Slot: name
--     * Slot: encoding_type
--     * Slot: value Description: Text content of the element. For SBE this carries the constant or default value (e.g. ``<type presence='constant'>-3</type>``).
--     * Slot: offset Description: Offset from start of a composite type or block as a zero-based index.
--     * Slot: semantic_type
--     * Slot: description
--     * Slot: since_version Description: The schema version in which an element was added
--     * Slot: deprecated Description: The version of the schema in which an element was deprecated. It is retained for back compatibility but should no longer be used by updated applications. It may be removed in a later version.
--     * Slot: CompositeDataTypeV1_id Description: Autocreated FK slot
-- # Class: RefTypeV1 Description: A reference to any existing encoding type (simple type, enum or set) to reuse as a member of a composite type
--     * Slot: id
--     * Slot: name
--     * Slot: type
--     * Slot: value Description: Text content of the element. For SBE this carries the constant or default value (e.g. ``<type presence='constant'>-3</type>``).
--     * Slot: offset Description: Offset from start of a composite type or block as a zero-based index.
--     * Slot: since_version Description: The schema version in which an element was added
--     * Slot: deprecated Description: The version of the schema in which an element was deprecated. It is retained for back compatibility but should no longer be used by updated applications. It may be removed in a later version.
--     * Slot: CompositeDataTypeV1_id Description: Autocreated FK slot
-- # Class: SetTypeV1 Description: A multi value choice (encoded as a bitset)
--     * Slot: id
--     * Slot: name
--     * Slot: encoding_type
--     * Slot: value Description: Text content of the element. For SBE this carries the constant or default value (e.g. ``<type presence='constant'>-3</type>``).
--     * Slot: offset Description: Offset from start of a composite type or block as a zero-based index.
--     * Slot: semantic_type
--     * Slot: description
--     * Slot: since_version Description: The schema version in which an element was added
--     * Slot: deprecated Description: The version of the schema in which an element was deprecated. It is retained for back compatibility but should no longer be used by updated applications. It may be removed in a later version.
--     * Slot: CompositeDataTypeV1_id Description: Autocreated FK slot
-- # Class: FieldTypeV1 Description: A field of a message of a specified dataType
--     * Slot: uid
--     * Slot: name
--     * Slot: id
--     * Slot: type Description: Must match the name of an encoding contained by 'types' element
--     * Slot: epoch
--     * Slot: time_unit Description: Deprecated - only for back compatibility with RC2
--     * Slot: offset Description: Offset from start of a composite type or block as a zero-based index.
--     * Slot: presence
--     * Slot: value_ref Description: A constant value as valid value of an enum in the form enum-name.valid-value-name
--     * Slot: semantic_type
--     * Slot: description
--     * Slot: since_version Description: The schema version in which an element was added
--     * Slot: deprecated Description: The version of the schema in which an element was deprecated. It is retained for back compatibility but should no longer be used by updated applications. It may be removed in a later version.
--     * Slot: BlockTypeV1_uid Description: Autocreated FK slot
--     * Slot: GroupTypeV1_uid Description: Autocreated FK slot
--     * Slot: MessageV1_uid Description: Autocreated FK slot
-- # Class: MessageSchemaV1 Description: Root of XML document, holds all message templates and their elements
--     * Slot: uid
--     * Slot: package
--     * Slot: id Description: Unique ID of a message schema
--     * Slot: version Description: The version of a message schema. Initial version is 0.
--     * Slot: semantic_version Description: Application layer specification version, such as FIX version 'FIX.5.0SP2'
--     * Slot: description
--     * Slot: byte_order
--     * Slot: header_type Description: Name of the encoding type of the message header, which is the same for all messages in a schema. The name has a default, but an encoding of that name must be present under a 'types' element.
-- # Class: MessageV1 Description: A message type, also known as a message template
--     * Slot: uid
--     * Slot: name
--     * Slot: id Description: Unique ID of a message template
--     * Slot: block_length Description: Space reserved for root level of message, not include groups or variable-length data elements.
--     * Slot: semantic_type
--     * Slot: description
--     * Slot: since_version Description: The schema version in which an element was added
--     * Slot: deprecated Description: The version of the schema in which an element was deprecated. It is retained for back compatibility but should no longer be used by updated applications. It may be removed in a later version.
--     * Slot: MessageSchemaV1_uid Description: Autocreated FK slot
-- # Class: AlignmentAttributesV2
--     * Slot: id
--     * Slot: alignment Description: Byte alignment of the start of a block (message root or repeating group instance).
-- # Class: OffsetAttributesV2
--     * Slot: id
--     * Slot: offset Description: Offset from start of a composite type or block as a zero-based index.
--     * Slot: alignment Description: Byte alignment of the start of a block (message root or repeating group instance).
-- # Class: PresenceAttributesV2
--     * Slot: id
--     * Slot: presence
--     * Slot: null_value Description: Override of default null indicator for the data type in SBE specification, as a string.
--     * Slot: min_value Description: Lower bound of a range
--     * Slot: max_value Description: Upper bound of a range
--     * Slot: value_ref Description: A constant value as valid value of an enum in the form enum-name.valid-value-name. Only valid if presence='constant'.
-- # Class: PrimitiveTypeAttributesV2
--     * Slot: id
--     * Slot: primitive_type
--     * Slot: length
--     * Slot: character_encoding Description: Character set or Unicode encoding scheme
-- # Class: BlockTypeV2 Description: Base type of message and repeating group entry
--     * Slot: uid
--     * Slot: name
--     * Slot: id Description: Unique ID of a message template
--     * Slot: block_length Description: Space reserved for root level of message or repeating group, not including nested groups or variable-length data elements.
--     * Slot: alignment Description: Byte alignment of the start of a block (message root or repeating group instance).
--     * Slot: semantic_type
--     * Slot: description
--     * Slot: since_version Description: The schema version in which an element was added
--     * Slot: deprecated Description: The version of the schema in which an element was deprecated. It is retained for back compatibility but should no longer be used by updated applications. It may be removed in a later version.
--     * Slot: MessagesV2_id Description: Autocreated FK slot
-- # Class: GroupTypeV2 Description: A repeating group contains an array of entries
--     * Slot: uid
--     * Slot: dimension_type
--     * Slot: name
--     * Slot: id Description: Unique ID of a message template
--     * Slot: block_length Description: Space reserved for root level of message or repeating group, not including nested groups or variable-length data elements.
--     * Slot: alignment Description: Byte alignment of the start of a block (message root or repeating group instance).
--     * Slot: semantic_type
--     * Slot: description
--     * Slot: since_version Description: The schema version in which an element was added
--     * Slot: deprecated Description: The version of the schema in which an element was deprecated. It is retained for back compatibility but should no longer be used by updated applications. It may be removed in a later version.
--     * Slot: BlockTypeV2_uid Description: Autocreated FK slot
--     * Slot: GroupTypeV2_uid Description: Autocreated FK slot
-- # Class: SimpleDataTypeV2 Description: Simple wire encoding consisting of a primitive type or array of primitives
--     * Slot: id
--     * Slot: name
--     * Slot: description
--     * Slot: value Description: Text content of the element. For SBE this carries the constant or default value (e.g. ``<type presence='constant'>-3</type>``).
--     * Slot: primitive_type
--     * Slot: length
--     * Slot: character_encoding Description: Character set or Unicode encoding scheme
--     * Slot: since_version Description: The schema version in which an element was added
--     * Slot: deprecated Description: The version of the schema in which an element was deprecated. It is retained for back compatibility but should no longer be used by updated applications. It may be removed in a later version.
--     * Slot: TypesV2_id Description: Autocreated FK slot
-- # Class: MemberDataTypeV2 Description: A simple type used as a member of a composite type
--     * Slot: id
--     * Slot: name
--     * Slot: description
--     * Slot: value Description: Text content of the element. For SBE this carries the constant or default value (e.g. ``<type presence='constant'>-3</type>``).
--     * Slot: primitive_type
--     * Slot: length
--     * Slot: character_encoding Description: Character set or Unicode encoding scheme
--     * Slot: offset Description: Offset from start of a composite type or block as a zero-based index.
--     * Slot: alignment Description: Byte alignment of the start of a block (message root or repeating group instance).
--     * Slot: presence
--     * Slot: null_value Description: Override of default null indicator for the data type in SBE specification, as a string.
--     * Slot: min_value Description: Lower bound of a range
--     * Slot: max_value Description: Upper bound of a range
--     * Slot: value_ref Description: A constant value as valid value of an enum in the form enum-name.valid-value-name. Only valid if presence='constant'.
--     * Slot: CompositeDataTypeV2_id Description: Autocreated FK slot
-- # Class: CompositeDataTypeV2 Description: A wire encoding composed of multiple parts
--     * Slot: id
--     * Slot: name
--     * Slot: description
--     * Slot: value Description: Text content of the element. For SBE this carries the constant or default value (e.g. ``<type presence='constant'>-3</type>``).
--     * Slot: offset Description: Offset from start of a composite type or block as a zero-based index.
--     * Slot: alignment Description: Byte alignment of the start of a block (message root or repeating group instance).
--     * Slot: since_version Description: The schema version in which an element was added
--     * Slot: deprecated Description: The version of the schema in which an element was deprecated. It is retained for back compatibility but should no longer be used by updated applications. It may be removed in a later version.
--     * Slot: CompositeDataTypeV2_id Description: Autocreated FK slot
--     * Slot: TypesV2_id Description: Autocreated FK slot
-- # Class: EnumTypeV2 Description: An enumeration of valid values
--     * Slot: id
--     * Slot: name
--     * Slot: encoding_type
--     * Slot: description
--     * Slot: value Description: Text content of the element. For SBE this carries the constant or default value (e.g. ``<type presence='constant'>-3</type>``).
--     * Slot: offset Description: Offset from start of a composite type or block as a zero-based index.
--     * Slot: alignment Description: Byte alignment of the start of a block (message root or repeating group instance).
--     * Slot: since_version Description: The schema version in which an element was added
--     * Slot: deprecated Description: The version of the schema in which an element was deprecated. It is retained for back compatibility but should no longer be used by updated applications. It may be removed in a later version.
--     * Slot: CompositeDataTypeV2_id Description: Autocreated FK slot
--     * Slot: TypesV2_id Description: Autocreated FK slot
-- # Class: RefTypeV2 Description: A reference to any existing encoding type (simple type, enum or set) to reuse as a member of a composite type
--     * Slot: id
--     * Slot: name
--     * Slot: type
--     * Slot: description Description: How the referenced type is used
--     * Slot: value Description: Text content of the element. For SBE this carries the constant or default value (e.g. ``<type presence='constant'>-3</type>``).
--     * Slot: offset Description: Offset from start of a composite type or block as a zero-based index.
--     * Slot: alignment Description: Byte alignment of the start of a block (message root or repeating group instance).
--     * Slot: CompositeDataTypeV2_id Description: Autocreated FK slot
-- # Class: SetTypeV2 Description: A multi value choice (encoded as a bitset)
--     * Slot: id
--     * Slot: name
--     * Slot: encoding_type
--     * Slot: description
--     * Slot: value Description: Text content of the element. For SBE this carries the constant or default value (e.g. ``<type presence='constant'>-3</type>``).
--     * Slot: offset Description: Offset from start of a composite type or block as a zero-based index.
--     * Slot: alignment Description: Byte alignment of the start of a block (message root or repeating group instance).
--     * Slot: since_version Description: The schema version in which an element was added
--     * Slot: deprecated Description: The version of the schema in which an element was deprecated. It is retained for back compatibility but should no longer be used by updated applications. It may be removed in a later version.
--     * Slot: CompositeDataTypeV2_id Description: Autocreated FK slot
--     * Slot: TypesV2_id Description: Autocreated FK slot
-- # Class: FieldTypeV2 Description: A field of a message of a specified dataType
--     * Slot: uid
--     * Slot: name
--     * Slot: id
--     * Slot: type Description: Must match the name of an encoding contained by 'types' element
--     * Slot: value Description: Text content of the element. For SBE this carries the constant or default value (e.g. ``<type presence='constant'>-3</type>``).
--     * Slot: offset Description: Offset from start of a composite type or block as a zero-based index.
--     * Slot: alignment Description: Byte alignment of the start of a block (message root or repeating group instance).
--     * Slot: presence
--     * Slot: null_value Description: Override of default null indicator for the data type in SBE specification, as a string.
--     * Slot: min_value Description: Lower bound of a range
--     * Slot: max_value Description: Upper bound of a range
--     * Slot: value_ref Description: A constant value as valid value of an enum in the form enum-name.valid-value-name. Only valid if presence='constant'.
--     * Slot: semantic_type
--     * Slot: description
--     * Slot: since_version Description: The schema version in which an element was added
--     * Slot: deprecated Description: The version of the schema in which an element was deprecated. It is retained for back compatibility but should no longer be used by updated applications. It may be removed in a later version.
--     * Slot: BlockTypeV2_uid Description: Autocreated FK slot
--     * Slot: GroupTypeV2_uid Description: Autocreated FK slot
-- # Class: MessageSchemaV2 Description: Root of XML document, holds all message templates and their elements
--     * Slot: uid
--     * Slot: package
--     * Slot: id Description: Unique ID of a message schema
--     * Slot: version Description: The version of a message schema. Initial version is 0.
--     * Slot: semantic_version Description: Application layer specification version, such as FIX version 'FIX.5.0SP2'
--     * Slot: description
--     * Slot: byte_order
--     * Slot: header_type Description: Name of the encoding type of the message header, which is the same for all messages in a schema. The name has a default, but an encoding of that name must be present under a 'types' element.
-- # Class: MessagesV2
--     * Slot: id
--     * Slot: description
--     * Slot: package Description: Overrides the messageSchema package
--     * Slot: MessageSchemaV2_uid Description: Autocreated FK slot
-- # Class: TypesV2 Description: More than one set of types may be provided. Names must be unique across all encoding types. Encoding types may appear in any order.
--     * Slot: id
--     * Slot: description
--     * Slot: package Description: Overrides the messageSchema package
--     * Slot: MessageSchemaV2_uid Description: Autocreated FK slot
-- # Class: MessageSchemaV1_types
--     * Slot: MessageSchemaV1_uid Description: Autocreated FK slot
--     * Slot: types Description: More than one set of types may be provided. Names must be unique across all encoding types. Encoding types may appear in any order.

CREATE TABLE "SemanticAttributes" (
	id INTEGER NOT NULL,
	semantic_type TEXT,
	description TEXT,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_SemanticAttributes_id" ON "SemanticAttributes" (id);

CREATE TABLE "VersionAttributes" (
	id INTEGER NOT NULL,
	since_version INTEGER,
	deprecated INTEGER,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_VersionAttributes_id" ON "VersionAttributes" (id);

CREATE TABLE "AlignmentAttributesV1" (
	id INTEGER NOT NULL,
	"offset" INTEGER,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_AlignmentAttributesV1_id" ON "AlignmentAttributesV1" (id);

CREATE TABLE "PresenceAttributesV1" (
	id INTEGER NOT NULL,
	presence VARCHAR(8),
	value_ref TEXT,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_PresenceAttributesV1_id" ON "PresenceAttributesV1" (id);

CREATE TABLE "BlockTypeV1" (
	uid INTEGER NOT NULL,
	name TEXT NOT NULL,
	id INTEGER NOT NULL,
	block_length INTEGER,
	semantic_type TEXT,
	description TEXT,
	since_version INTEGER,
	deprecated INTEGER,
	PRIMARY KEY (uid)
);
CREATE INDEX "ix_BlockTypeV1_uid" ON "BlockTypeV1" (uid);

CREATE TABLE "CompositeDataTypeV1" (
	id INTEGER NOT NULL,
	name TEXT NOT NULL,
	value TEXT,
	"offset" INTEGER,
	semantic_type TEXT,
	description TEXT,
	since_version INTEGER,
	deprecated INTEGER,
	"CompositeDataTypeV1_id" INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY("CompositeDataTypeV1_id") REFERENCES "CompositeDataTypeV1" (id)
);
CREATE INDEX "ix_CompositeDataTypeV1_id" ON "CompositeDataTypeV1" (id);

CREATE TABLE "MessageSchemaV1" (
	uid INTEGER NOT NULL,
	package TEXT,
	id INTEGER,
	version INTEGER NOT NULL,
	semantic_version TEXT,
	description TEXT,
	byte_order VARCHAR(12),
	header_type TEXT,
	PRIMARY KEY (uid)
);
CREATE INDEX "ix_MessageSchemaV1_uid" ON "MessageSchemaV1" (uid);

CREATE TABLE "AlignmentAttributesV2" (
	id INTEGER NOT NULL,
	alignment INTEGER,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_AlignmentAttributesV2_id" ON "AlignmentAttributesV2" (id);

CREATE TABLE "OffsetAttributesV2" (
	id INTEGER NOT NULL,
	"offset" INTEGER,
	alignment INTEGER,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_OffsetAttributesV2_id" ON "OffsetAttributesV2" (id);

CREATE TABLE "PresenceAttributesV2" (
	id INTEGER NOT NULL,
	presence VARCHAR(8),
	null_value TEXT,
	min_value TEXT,
	max_value TEXT,
	value_ref TEXT,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_PresenceAttributesV2_id" ON "PresenceAttributesV2" (id);

CREATE TABLE "PrimitiveTypeAttributesV2" (
	id INTEGER NOT NULL,
	primitive_type VARCHAR(6) NOT NULL,
	length INTEGER,
	character_encoding TEXT,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_PrimitiveTypeAttributesV2_id" ON "PrimitiveTypeAttributesV2" (id);

CREATE TABLE "MessageSchemaV2" (
	uid INTEGER NOT NULL,
	package TEXT,
	id INTEGER,
	version INTEGER NOT NULL,
	semantic_version TEXT,
	description TEXT,
	byte_order VARCHAR(12),
	header_type TEXT,
	PRIMARY KEY (uid)
);
CREATE INDEX "ix_MessageSchemaV2_uid" ON "MessageSchemaV2" (uid);

CREATE TABLE "EncodedDataTypeV1" (
	id INTEGER NOT NULL,
	name TEXT NOT NULL,
	null_value TEXT,
	min_value TEXT,
	max_value TEXT,
	length INTEGER,
	primitive_type VARCHAR(6) NOT NULL,
	character_encoding TEXT,
	value TEXT,
	"offset" INTEGER,
	presence VARCHAR(8),
	value_ref TEXT,
	semantic_type TEXT,
	description TEXT,
	since_version INTEGER,
	deprecated INTEGER,
	"CompositeDataTypeV1_id" INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY("CompositeDataTypeV1_id") REFERENCES "CompositeDataTypeV1" (id)
);
CREATE INDEX "ix_EncodedDataTypeV1_id" ON "EncodedDataTypeV1" (id);

CREATE TABLE "EnumTypeV1" (
	id INTEGER NOT NULL,
	name TEXT NOT NULL,
	encoding_type TEXT NOT NULL,
	value TEXT,
	"offset" INTEGER,
	semantic_type TEXT,
	description TEXT,
	since_version INTEGER,
	deprecated INTEGER,
	"CompositeDataTypeV1_id" INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY("CompositeDataTypeV1_id") REFERENCES "CompositeDataTypeV1" (id)
);
CREATE INDEX "ix_EnumTypeV1_id" ON "EnumTypeV1" (id);

CREATE TABLE "RefTypeV1" (
	id INTEGER NOT NULL,
	name TEXT NOT NULL,
	type TEXT NOT NULL,
	value TEXT,
	"offset" INTEGER,
	since_version INTEGER,
	deprecated INTEGER,
	"CompositeDataTypeV1_id" INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY("CompositeDataTypeV1_id") REFERENCES "CompositeDataTypeV1" (id)
);
CREATE INDEX "ix_RefTypeV1_id" ON "RefTypeV1" (id);

CREATE TABLE "SetTypeV1" (
	id INTEGER NOT NULL,
	name TEXT NOT NULL,
	encoding_type TEXT NOT NULL,
	value TEXT,
	"offset" INTEGER,
	semantic_type TEXT,
	description TEXT,
	since_version INTEGER,
	deprecated INTEGER,
	"CompositeDataTypeV1_id" INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY("CompositeDataTypeV1_id") REFERENCES "CompositeDataTypeV1" (id)
);
CREATE INDEX "ix_SetTypeV1_id" ON "SetTypeV1" (id);

CREATE TABLE "MessageV1" (
	uid INTEGER NOT NULL,
	name TEXT NOT NULL,
	id INTEGER NOT NULL,
	block_length INTEGER,
	semantic_type TEXT,
	description TEXT,
	since_version INTEGER,
	deprecated INTEGER,
	"MessageSchemaV1_uid" INTEGER,
	PRIMARY KEY (uid),
	FOREIGN KEY("MessageSchemaV1_uid") REFERENCES "MessageSchemaV1" (uid)
);
CREATE INDEX "ix_MessageV1_uid" ON "MessageV1" (uid);

CREATE TABLE "MessagesV2" (
	id INTEGER NOT NULL,
	description TEXT,
	package TEXT,
	"MessageSchemaV2_uid" INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY("MessageSchemaV2_uid") REFERENCES "MessageSchemaV2" (uid)
);
CREATE INDEX "ix_MessagesV2_id" ON "MessagesV2" (id);

CREATE TABLE "TypesV2" (
	id INTEGER NOT NULL,
	description TEXT,
	package TEXT,
	"MessageSchemaV2_uid" INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY("MessageSchemaV2_uid") REFERENCES "MessageSchemaV2" (uid)
);
CREATE INDEX "ix_TypesV2_id" ON "TypesV2" (id);

CREATE TABLE "MessageSchemaV1_types" (
	"MessageSchemaV1_uid" INTEGER,
	types TEXT NOT NULL,
	PRIMARY KEY ("MessageSchemaV1_uid", types),
	FOREIGN KEY("MessageSchemaV1_uid") REFERENCES "MessageSchemaV1" (uid)
);
CREATE INDEX "ix_MessageSchemaV1_types_types" ON "MessageSchemaV1_types" (types);
CREATE INDEX "ix_MessageSchemaV1_types_MessageSchemaV1_uid" ON "MessageSchemaV1_types" ("MessageSchemaV1_uid");

CREATE TABLE "GroupTypeV1" (
	uid INTEGER NOT NULL,
	dimension_type TEXT,
	name TEXT NOT NULL,
	id INTEGER NOT NULL,
	block_length INTEGER,
	semantic_type TEXT,
	description TEXT,
	since_version INTEGER,
	deprecated INTEGER,
	"BlockTypeV1_uid" INTEGER,
	"GroupTypeV1_uid" INTEGER,
	"MessageV1_uid" INTEGER,
	PRIMARY KEY (uid),
	FOREIGN KEY("BlockTypeV1_uid") REFERENCES "BlockTypeV1" (uid),
	FOREIGN KEY("GroupTypeV1_uid") REFERENCES "GroupTypeV1" (uid),
	FOREIGN KEY("MessageV1_uid") REFERENCES "MessageV1" (uid)
);
CREATE INDEX "ix_GroupTypeV1_uid" ON "GroupTypeV1" (uid);

CREATE TABLE "BlockTypeV2" (
	uid INTEGER NOT NULL,
	name TEXT NOT NULL,
	id INTEGER NOT NULL,
	block_length INTEGER,
	alignment INTEGER,
	semantic_type TEXT,
	description TEXT,
	since_version INTEGER,
	deprecated INTEGER,
	"MessagesV2_id" INTEGER,
	PRIMARY KEY (uid),
	FOREIGN KEY("MessagesV2_id") REFERENCES "MessagesV2" (id)
);
CREATE INDEX "ix_BlockTypeV2_uid" ON "BlockTypeV2" (uid);

CREATE TABLE "SimpleDataTypeV2" (
	id INTEGER NOT NULL,
	name TEXT NOT NULL,
	description TEXT,
	value TEXT,
	primitive_type VARCHAR(6) NOT NULL,
	length INTEGER,
	character_encoding TEXT,
	since_version INTEGER,
	deprecated INTEGER,
	"TypesV2_id" INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY("TypesV2_id") REFERENCES "TypesV2" (id)
);
CREATE INDEX "ix_SimpleDataTypeV2_id" ON "SimpleDataTypeV2" (id);

CREATE TABLE "CompositeDataTypeV2" (
	id INTEGER NOT NULL,
	name TEXT NOT NULL,
	description TEXT,
	value TEXT,
	"offset" INTEGER,
	alignment INTEGER,
	since_version INTEGER,
	deprecated INTEGER,
	"CompositeDataTypeV2_id" INTEGER,
	"TypesV2_id" INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY("CompositeDataTypeV2_id") REFERENCES "CompositeDataTypeV2" (id),
	FOREIGN KEY("TypesV2_id") REFERENCES "TypesV2" (id)
);
CREATE INDEX "ix_CompositeDataTypeV2_id" ON "CompositeDataTypeV2" (id);

CREATE TABLE "FieldTypeV1" (
	uid INTEGER NOT NULL,
	name TEXT NOT NULL,
	id INTEGER NOT NULL,
	type TEXT NOT NULL,
	epoch TEXT,
	time_unit TEXT,
	"offset" INTEGER,
	presence VARCHAR(8),
	value_ref TEXT,
	semantic_type TEXT,
	description TEXT,
	since_version INTEGER,
	deprecated INTEGER,
	"BlockTypeV1_uid" INTEGER,
	"GroupTypeV1_uid" INTEGER,
	"MessageV1_uid" INTEGER,
	PRIMARY KEY (uid),
	FOREIGN KEY("BlockTypeV1_uid") REFERENCES "BlockTypeV1" (uid),
	FOREIGN KEY("GroupTypeV1_uid") REFERENCES "GroupTypeV1" (uid),
	FOREIGN KEY("MessageV1_uid") REFERENCES "MessageV1" (uid)
);
CREATE INDEX "ix_FieldTypeV1_uid" ON "FieldTypeV1" (uid);

CREATE TABLE "GroupTypeV2" (
	uid INTEGER NOT NULL,
	dimension_type TEXT,
	name TEXT NOT NULL,
	id INTEGER NOT NULL,
	block_length INTEGER,
	alignment INTEGER,
	semantic_type TEXT,
	description TEXT,
	since_version INTEGER,
	deprecated INTEGER,
	"BlockTypeV2_uid" INTEGER,
	"GroupTypeV2_uid" INTEGER,
	PRIMARY KEY (uid),
	FOREIGN KEY("BlockTypeV2_uid") REFERENCES "BlockTypeV2" (uid),
	FOREIGN KEY("GroupTypeV2_uid") REFERENCES "GroupTypeV2" (uid)
);
CREATE INDEX "ix_GroupTypeV2_uid" ON "GroupTypeV2" (uid);

CREATE TABLE "MemberDataTypeV2" (
	id INTEGER NOT NULL,
	name TEXT NOT NULL,
	description TEXT,
	value TEXT,
	primitive_type VARCHAR(6) NOT NULL,
	length INTEGER,
	character_encoding TEXT,
	"offset" INTEGER,
	alignment INTEGER,
	presence VARCHAR(8),
	null_value TEXT,
	min_value TEXT,
	max_value TEXT,
	value_ref TEXT,
	"CompositeDataTypeV2_id" INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY("CompositeDataTypeV2_id") REFERENCES "CompositeDataTypeV2" (id)
);
CREATE INDEX "ix_MemberDataTypeV2_id" ON "MemberDataTypeV2" (id);

CREATE TABLE "EnumTypeV2" (
	id INTEGER NOT NULL,
	name TEXT NOT NULL,
	encoding_type TEXT NOT NULL,
	description TEXT,
	value TEXT,
	"offset" INTEGER,
	alignment INTEGER,
	since_version INTEGER,
	deprecated INTEGER,
	"CompositeDataTypeV2_id" INTEGER,
	"TypesV2_id" INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY("CompositeDataTypeV2_id") REFERENCES "CompositeDataTypeV2" (id),
	FOREIGN KEY("TypesV2_id") REFERENCES "TypesV2" (id)
);
CREATE INDEX "ix_EnumTypeV2_id" ON "EnumTypeV2" (id);

CREATE TABLE "RefTypeV2" (
	id INTEGER NOT NULL,
	name TEXT NOT NULL,
	type TEXT NOT NULL,
	description TEXT,
	value TEXT,
	"offset" INTEGER,
	alignment INTEGER,
	"CompositeDataTypeV2_id" INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY("CompositeDataTypeV2_id") REFERENCES "CompositeDataTypeV2" (id)
);
CREATE INDEX "ix_RefTypeV2_id" ON "RefTypeV2" (id);

CREATE TABLE "SetTypeV2" (
	id INTEGER NOT NULL,
	name TEXT NOT NULL,
	encoding_type TEXT NOT NULL,
	description TEXT,
	value TEXT,
	"offset" INTEGER,
	alignment INTEGER,
	since_version INTEGER,
	deprecated INTEGER,
	"CompositeDataTypeV2_id" INTEGER,
	"TypesV2_id" INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY("CompositeDataTypeV2_id") REFERENCES "CompositeDataTypeV2" (id),
	FOREIGN KEY("TypesV2_id") REFERENCES "TypesV2" (id)
);
CREATE INDEX "ix_SetTypeV2_id" ON "SetTypeV2" (id);

CREATE TABLE "ValidValue" (
	id INTEGER NOT NULL,
	name TEXT NOT NULL,
	description TEXT,
	value TEXT,
	since_version INTEGER,
	deprecated INTEGER,
	"EnumTypeV1_id" INTEGER,
	"EnumTypeV2_id" INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY("EnumTypeV1_id") REFERENCES "EnumTypeV1" (id),
	FOREIGN KEY("EnumTypeV2_id") REFERENCES "EnumTypeV2" (id)
);
CREATE INDEX "ix_ValidValue_id" ON "ValidValue" (id);

CREATE TABLE "Choice" (
	id INTEGER NOT NULL,
	name TEXT NOT NULL,
	description TEXT,
	value TEXT,
	since_version INTEGER,
	deprecated INTEGER,
	"SetTypeV1_id" INTEGER,
	"SetTypeV2_id" INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY("SetTypeV1_id") REFERENCES "SetTypeV1" (id),
	FOREIGN KEY("SetTypeV2_id") REFERENCES "SetTypeV2" (id)
);
CREATE INDEX "ix_Choice_id" ON "Choice" (id);

CREATE TABLE "FieldTypeV2" (
	uid INTEGER NOT NULL,
	name TEXT NOT NULL,
	id INTEGER NOT NULL,
	type TEXT NOT NULL,
	value TEXT,
	"offset" INTEGER,
	alignment INTEGER,
	presence VARCHAR(8),
	null_value TEXT,
	min_value TEXT,
	max_value TEXT,
	value_ref TEXT,
	semantic_type TEXT,
	description TEXT,
	since_version INTEGER,
	deprecated INTEGER,
	"BlockTypeV2_uid" INTEGER,
	"GroupTypeV2_uid" INTEGER,
	PRIMARY KEY (uid),
	FOREIGN KEY("BlockTypeV2_uid") REFERENCES "BlockTypeV2" (uid),
	FOREIGN KEY("GroupTypeV2_uid") REFERENCES "GroupTypeV2" (uid)
);
CREATE INDEX "ix_FieldTypeV2_uid" ON "FieldTypeV2" (uid);
