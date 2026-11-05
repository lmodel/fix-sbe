-- # Class: SbeVersionedMixin Description: The two attributes that record when an element entered a schema and when it should leave.
--     * Slot: id
--     * Slot: since_version Description: The schema version that added this element.
--     * Slot: deprecated_since Description: The schema version that retired this element, which stays only for older applications.
-- # Class: SbeValidValue Description: One of the values an enumeration allows.
--     * Slot: id
--     * Slot: symbolic_name Description: What the schema calls this element.
--     * Slot: description Description: Free text about this element, for the people who read the schema.
--     * Slot: valid_value Description: The value as it is written in the schema, which must convert to the enumeration's encoding.
--     * Slot: since_version Description: The schema version that added this element.
--     * Slot: deprecated_since Description: The schema version that retired this element, which stays only for older applications.
--     * Slot: SbeEnumV1_id Description: Autocreated FK slot
--     * Slot: SbeEnumV2_id Description: Autocreated FK slot
-- # Class: SbeChoice Description: One of the alternatives of a set, which is one bit of its encoding.
--     * Slot: id
--     * Slot: symbolic_name Description: What the schema calls this element.
--     * Slot: description Description: Free text about this element, for the people who read the schema.
--     * Slot: bit_position Description: Which bit stands for this choice, counted from zero at the least significant.
--     * Slot: since_version Description: The schema version that added this element.
--     * Slot: deprecated_since Description: The schema version that retired this element, which stays only for older applications.
--     * Slot: SbeSetV1_id Description: Autocreated FK slot
--     * Slot: SbeSetV2_id Description: Autocreated FK slot
-- # Class: SbeMessageSchemaV1 Description: One SBE 1.0 message schema, with its encodings and message templates.
--     * Slot: id
--     * Slot: schema_package Description: The name or category that a set of counterparties knows this schema or part of it by.
--     * Slot: sbe_id Description: The number that identifies this schema between counterparties.
--     * Slot: schema_version Description: The version of this message schema, starting at zero.
--     * Slot: semantic_version Description: The version of FIX whose meanings this schema uses.
--     * Slot: description Description: Free text about this element, for the people who read the schema.
--     * Slot: byte_order Description: How the octets of every number in this schema's messages are ordered.
--     * Slot: header_type Description: The composite, by name, that sends each message's header in this schema.
-- # Class: SbeEncodingSetV1 Description: A set of encodings, listed in any order, whose names are unique across the whole schema.
--     * Slot: id
--     * Slot: SbeMessageSchemaV1_id Description: Autocreated FK slot
-- # Abstract Class: SbeMemberV1 Description: Anything a composite may hold in the order it is sent.
--     * Slot: id
--     * Slot: encoding_kind Description: The class of this encoding or composite member, which stands for its XML element.
--     * Slot: symbolic_name Description: What the schema calls this element.
--     * Slot: offset Description: The octet this element starts at, counted from zero at the start of its block or composite.
--     * Slot: since_version Description: The schema version that added this element.
--     * Slot: deprecated_since Description: The schema version that retired this element, which stays only for older applications.
--     * Slot: SbeCompositeV1_id Description: Autocreated FK slot
-- # Class: SbeRefV1 Description: A composite's member that reuses an encoding defined elsewhere in the schema.
--     * Slot: id
--     * Slot: encoding_name Description: Which encoding this element uses, by name.
--     * Slot: encoding_kind Description: The class of this encoding or composite member, which stands for its XML element.
--     * Slot: symbolic_name Description: What the schema calls this element.
--     * Slot: offset Description: The octet this element starts at, counted from zero at the start of its block or composite.
--     * Slot: since_version Description: The schema version that added this element.
--     * Slot: deprecated_since Description: The schema version that retired this element, which stays only for older applications.
-- # Abstract Class: SbeEncodingV1 Description: An encoding of SBE 1.0, which says how a value is laid out on the wire.
--     * Slot: id
--     * Slot: semantic_type Description: The FIX datatype this encoding carries.
--     * Slot: description Description: Free text about this element, for the people who read the schema.
--     * Slot: encoding_kind Description: The class of this encoding or composite member, which stands for its XML element.
--     * Slot: symbolic_name Description: What the schema calls this element.
--     * Slot: offset Description: The octet this element starts at, counted from zero at the start of its block or composite.
--     * Slot: since_version Description: The schema version that added this element.
--     * Slot: deprecated_since Description: The schema version that retired this element, which stays only for older applications.
--     * Slot: SbeEncodingSetV1_id Description: Autocreated FK slot
-- # Class: SbeSimpleTypeV1 Description: An encoding backed by one primitive value, or several in an array.
--     * Slot: id
--     * Slot: element_value Description: The text of the XML element, which is the constant when presence is constant.
--     * Slot: primitive_type Description: The wire type under this encoding.
--     * Slot: array_length Description: How many values of the primitive type the encoding holds, where zero means a variable number.
--     * Slot: character_encoding Description: Which character set, or which Unicode scheme, character data follows.
--     * Slot: null_value Description: The value that stands for null in place of the primitive type's default, written as text.
--     * Slot: min_value Description: The lowest value allowed, written as text.
--     * Slot: max_value Description: The highest value allowed, written as text.
--     * Slot: presence Description: Whether this element's value is required, optional or constant.
--     * Slot: value_ref Description: The valid value that gives a constant element its value.
--     * Slot: semantic_type Description: The FIX datatype this encoding carries.
--     * Slot: description Description: Free text about this element, for the people who read the schema.
--     * Slot: encoding_kind Description: The class of this encoding or composite member, which stands for its XML element.
--     * Slot: symbolic_name Description: What the schema calls this element.
--     * Slot: offset Description: The octet this element starts at, counted from zero at the start of its block or composite.
--     * Slot: since_version Description: The schema version that added this element.
--     * Slot: deprecated_since Description: The schema version that retired this element, which stays only for older applications.
-- # Class: SbeCompositeV1 Description: An encoding built from members sent one after another, such as a decimal's mantissa and exponent.
--     * Slot: id
--     * Slot: semantic_type Description: The FIX datatype this encoding carries.
--     * Slot: description Description: Free text about this element, for the people who read the schema.
--     * Slot: encoding_kind Description: The class of this encoding or composite member, which stands for its XML element.
--     * Slot: symbolic_name Description: What the schema calls this element.
--     * Slot: offset Description: The octet this element starts at, counted from zero at the start of its block or composite.
--     * Slot: since_version Description: The schema version that added this element.
--     * Slot: deprecated_since Description: The schema version that retired this element, which stays only for older applications.
-- # Class: SbeEnumV1 Description: An encoding whose value is one of a listed set of valid values.
--     * Slot: id
--     * Slot: encoding_type Description: The simple encoding or primitive type that an enumeration or set is sent as.
--     * Slot: semantic_type Description: The FIX datatype this encoding carries.
--     * Slot: description Description: Free text about this element, for the people who read the schema.
--     * Slot: encoding_kind Description: The class of this encoding or composite member, which stands for its XML element.
--     * Slot: symbolic_name Description: What the schema calls this element.
--     * Slot: offset Description: The octet this element starts at, counted from zero at the start of its block or composite.
--     * Slot: since_version Description: The schema version that added this element.
--     * Slot: deprecated_since Description: The schema version that retired this element, which stays only for older applications.
-- # Class: SbeSetV1 Description: An encoding whose value is any combination of up to 64 choices, sent as a bitset.
--     * Slot: id
--     * Slot: encoding_type Description: The simple encoding or primitive type that an enumeration or set is sent as.
--     * Slot: semantic_type Description: The FIX datatype this encoding carries.
--     * Slot: description Description: Free text about this element, for the people who read the schema.
--     * Slot: encoding_kind Description: The class of this encoding or composite member, which stands for its XML element.
--     * Slot: symbolic_name Description: What the schema calls this element.
--     * Slot: offset Description: The octet this element starts at, counted from zero at the start of its block or composite.
--     * Slot: since_version Description: The schema version that added this element.
--     * Slot: deprecated_since Description: The schema version that retired this element, which stays only for older applications.
-- # Class: SbeBlockV1Mixin Description: The body shared by a message and a group entry, which holds its fixed-length fields first, then groups, then variable-length data.
--     * Slot: id
--     * Slot: symbolic_name Description: What the schema calls this element.
--     * Slot: sbe_id Description: The number that identifies this element.
--     * Slot: block_length Description: The octets set aside for a message's fixed-length fields, or for those of each group entry.
--     * Slot: semantic_type Description: What this element means at the FIX application layer.
--     * Slot: description Description: Free text about this element, for the people who read the schema.
-- # Class: SbeMessageV1 Description: A message template, whose number and block length are sent in each message's header.
--     * Slot: id
--     * Slot: since_version Description: The schema version that added this element.
--     * Slot: deprecated_since Description: The schema version that retired this element, which stays only for older applications.
--     * Slot: symbolic_name Description: What the schema calls this element.
--     * Slot: sbe_id Description: The template's number, which no other template in the schema shares.
--     * Slot: block_length Description: The octets set aside for a message's fixed-length fields, or for those of each group entry.
--     * Slot: semantic_type Description: The FIX MsgType(35) this template stands for, where several templates may share one.
--     * Slot: description Description: Free text about this element, for the people who read the schema.
--     * Slot: SbeMessageSchemaV1_id Description: Autocreated FK slot
-- # Class: SbeGroupV1 Description: A repeating group, whose entries each hold the same fields, and which must have at least one field.
--     * Slot: id
--     * Slot: dimension_type Description: The composite, by name, that sends a repeating group's entry count and entry size.
--     * Slot: since_version Description: The schema version that added this element.
--     * Slot: deprecated_since Description: The schema version that retired this element, which stays only for older applications.
--     * Slot: symbolic_name Description: What the schema calls this element.
--     * Slot: sbe_id Description: The number that identifies this element.
--     * Slot: block_length Description: The octets set aside for a message's fixed-length fields, or for those of each group entry.
--     * Slot: semantic_type Description: What this element means at the FIX application layer.
--     * Slot: description Description: Free text about this element, for the people who read the schema.
--     * Slot: SbeBlockV1Mixin_id Description: Autocreated FK slot
--     * Slot: SbeMessageV1_id Description: Autocreated FK slot
--     * Slot: SbeGroupV1_id Description: Autocreated FK slot
-- # Class: SbeFieldV1 Description: A message's or group entry's field, which uses an encoding at a place in its block.
--     * Slot: id
--     * Slot: symbolic_name Description: What the schema calls this element.
--     * Slot: sbe_id Description: The field's FIX tag number.
--     * Slot: encoding_name Description: Which encoding this element uses, by name.
--     * Slot: offset Description: The octet this element starts at, counted from zero at the start of its block or composite.
--     * Slot: presence Description: Whether this element's value is required, optional or constant.
--     * Slot: value_ref Description: The valid value that gives a constant element its value.
--     * Slot: semantic_type Description: The FIX datatype this field carries.
--     * Slot: description Description: Free text about this element, for the people who read the schema.
--     * Slot: time_epoch Description: Where the period a time value counts from begins.
--     * Slot: time_unit Description: The unit of a time value.
--     * Slot: since_version Description: The schema version that added this element.
--     * Slot: deprecated_since Description: The schema version that retired this element, which stays only for older applications.
--     * Slot: SbeBlockV1Mixin_id Description: Autocreated FK slot
--     * Slot: SbeMessageV1_id Description: Autocreated FK slot
--     * Slot: SbeGroupV1_id Description: Autocreated FK slot
-- # Class: SbeMessageSchemaV2 Description: One SBE 2.0 message schema, with its encodings and message templates.
--     * Slot: id
--     * Slot: schema_package Description: The name or category that a set of counterparties knows this schema or part of it by.
--     * Slot: sbe_id Description: The number that identifies this schema between counterparties.
--     * Slot: schema_version Description: The version of this message schema, starting at zero.
--     * Slot: semantic_version Description: The version of FIX whose meanings this schema uses.
--     * Slot: description Description: Free text about this element, for the people who read the schema.
--     * Slot: byte_order Description: How the octets of every number in this schema's messages are ordered.
--     * Slot: header_type Description: The composite, by name, that sends each message's header in this schema.
-- # Class: SbeEncodingSetV2 Description: A set of encodings, in any order, that may have its own package and may come from another file.
--     * Slot: id
--     * Slot: description Description: Free text about this element, for the people who read the schema.
--     * Slot: schema_package Description: A package for this set in place of the schema's.
--     * Slot: sbe_xml_base Description: The base address that the XML Inclusion mechanism records on an element it brought in from another file.
--     * Slot: SbeMessageSchemaV2_id Description: Autocreated FK slot
-- # Class: SbeMessageSetV2 Description: Message templates held together, which may have their own package and may come from another file.
--     * Slot: id
--     * Slot: description Description: Free text about this element, for the people who read the schema.
--     * Slot: schema_package Description: A package for this set in place of the schema's.
--     * Slot: sbe_xml_base Description: The base address that the XML Inclusion mechanism records on an element it brought in from another file.
--     * Slot: SbeMessageSchemaV2_id Description: Autocreated FK slot
-- # Abstract Class: SbeElementV2 Description: Anything that sets of encodings or composites hold, and the name and text they all have.
--     * Slot: id
--     * Slot: encoding_kind Description: The class of this encoding or composite member, which stands for its XML element.
--     * Slot: symbolic_name Description: What the schema calls this element.
--     * Slot: description Description: Free text about this element, for the people who read the schema.
--     * Slot: SbeEncodingSetV2_id Description: Autocreated FK slot
-- # Abstract Class: SbeMemberV2 Description: Anything a composite may hold in the order it is sent.
--     * Slot: id
--     * Slot: offset Description: The octet this element starts at, counted from zero at the start of its block or composite.
--     * Slot: alignment Description: The multiple of octets the start of this element is placed on.
--     * Slot: encoding_kind Description: The class of this encoding or composite member, which stands for its XML element.
--     * Slot: symbolic_name Description: What the schema calls this element.
--     * Slot: description Description: Free text about this element, for the people who read the schema.
--     * Slot: SbeCompositeV2_id Description: Autocreated FK slot
-- # Class: SbeSimpleTypeV2 Description: A simple encoding that stands alone in a set, backed by one primitive value, or several in an array.
--     * Slot: id
--     * Slot: element_value Description: The text of the XML element, which is the constant when presence is constant.
--     * Slot: primitive_type Description: The wire type under this encoding.
--     * Slot: array_length Description: How many values of the primitive type the encoding holds, where zero means a variable number.
--     * Slot: character_encoding Description: Which character set, or which Unicode scheme, character data follows.
--     * Slot: since_version Description: The schema version that added this element.
--     * Slot: deprecated_since Description: The schema version that retired this element, which stays only for older applications.
--     * Slot: encoding_kind Description: The class of this encoding or composite member, which stands for its XML element.
--     * Slot: symbolic_name Description: What the schema calls this element.
--     * Slot: description Description: Free text about this element, for the people who read the schema.
-- # Class: SbeMemberTypeV2 Description: A simple encoding inside a composite, which may say it is optional or constant.
--     * Slot: id
--     * Slot: element_value Description: The text of the XML element, which is the constant when presence is constant.
--     * Slot: primitive_type Description: The wire type under this encoding.
--     * Slot: array_length Description: How many values of the primitive type the encoding holds, where zero means a variable number.
--     * Slot: character_encoding Description: Which character set, or which Unicode scheme, character data follows.
--     * Slot: presence Description: Whether this element's value is required, optional or constant.
--     * Slot: null_value Description: The value that stands for null in place of the primitive type's default, written as text.
--     * Slot: min_value Description: The lowest value allowed, written as text.
--     * Slot: max_value Description: The highest value allowed, written as text.
--     * Slot: value_ref Description: The valid value that gives a constant element its value.
--     * Slot: offset Description: The octet this element starts at, counted from zero at the start of its block or composite.
--     * Slot: alignment Description: The multiple of octets the start of this element is placed on.
--     * Slot: encoding_kind Description: The class of this encoding or composite member, which stands for its XML element.
--     * Slot: symbolic_name Description: What the schema calls this element.
--     * Slot: description Description: Free text about this element, for the people who read the schema.
-- # Class: SbeRefV2 Description: A composite's member that reuses an encoding defined elsewhere in the schema.
--     * Slot: id
--     * Slot: encoding_name Description: Which encoding this element uses, by name.
--     * Slot: offset Description: The octet this element starts at, counted from zero at the start of its block or composite.
--     * Slot: alignment Description: The multiple of octets the start of this element is placed on.
--     * Slot: encoding_kind Description: The class of this encoding or composite member, which stands for its XML element.
--     * Slot: symbolic_name Description: What the schema calls this element.
--     * Slot: description Description: Free text about this element, for the people who read the schema.
-- # Class: SbeCompositeV2 Description: An encoding built from members sent one after another, such as a decimal's mantissa and exponent.
--     * Slot: id
--     * Slot: since_version Description: The schema version that added this element.
--     * Slot: deprecated_since Description: The schema version that retired this element, which stays only for older applications.
--     * Slot: offset Description: The octet this element starts at, counted from zero at the start of its block or composite.
--     * Slot: alignment Description: The multiple of octets the start of this element is placed on.
--     * Slot: encoding_kind Description: The class of this encoding or composite member, which stands for its XML element.
--     * Slot: symbolic_name Description: What the schema calls this element.
--     * Slot: description Description: Free text about this element, for the people who read the schema.
-- # Class: SbeEnumV2 Description: An encoding whose value is one of a listed set of valid values.
--     * Slot: id
--     * Slot: encoding_type Description: The simple encoding or primitive type that an enumeration or set is sent as.
--     * Slot: since_version Description: The schema version that added this element.
--     * Slot: deprecated_since Description: The schema version that retired this element, which stays only for older applications.
--     * Slot: offset Description: The octet this element starts at, counted from zero at the start of its block or composite.
--     * Slot: alignment Description: The multiple of octets the start of this element is placed on.
--     * Slot: encoding_kind Description: The class of this encoding or composite member, which stands for its XML element.
--     * Slot: symbolic_name Description: What the schema calls this element.
--     * Slot: description Description: Free text about this element, for the people who read the schema.
-- # Class: SbeSetV2 Description: An encoding whose value is any combination of up to 64 choices, sent as a bitset.
--     * Slot: id
--     * Slot: encoding_type Description: The simple encoding or primitive type that an enumeration or set is sent as.
--     * Slot: since_version Description: The schema version that added this element.
--     * Slot: deprecated_since Description: The schema version that retired this element, which stays only for older applications.
--     * Slot: offset Description: The octet this element starts at, counted from zero at the start of its block or composite.
--     * Slot: alignment Description: The multiple of octets the start of this element is placed on.
--     * Slot: encoding_kind Description: The class of this encoding or composite member, which stands for its XML element.
--     * Slot: symbolic_name Description: What the schema calls this element.
--     * Slot: description Description: Free text about this element, for the people who read the schema.
-- # Class: SbeBlockV2Mixin Description: The body shared by a message and a group entry, which holds its fixed-length fields first, then groups, then variable-length data.
--     * Slot: id
--     * Slot: symbolic_name Description: What the schema calls this element.
--     * Slot: sbe_id Description: The number that identifies this element.
--     * Slot: block_length Description: The octets set aside for a message's fixed-length fields, or for those of each group entry.
--     * Slot: alignment Description: The multiple of octets where a message or each group entry begins.
--     * Slot: semantic_type Description: What this element means at the FIX application layer.
--     * Slot: description Description: Free text about this element, for the people who read the schema.
-- # Class: SbeMessageV2 Description: A message template, whose number and block length are sent in each message's header.
--     * Slot: id
--     * Slot: since_version Description: The schema version that added this element.
--     * Slot: deprecated_since Description: The schema version that retired this element, which stays only for older applications.
--     * Slot: symbolic_name Description: What the schema calls this element.
--     * Slot: sbe_id Description: The template's number, which no other template in the schema shares.
--     * Slot: block_length Description: The octets set aside for a message's fixed-length fields, or for those of each group entry.
--     * Slot: alignment Description: The multiple of octets where a message or each group entry begins.
--     * Slot: semantic_type Description: The FIX MsgType(35) this template stands for, where several templates may share one.
--     * Slot: description Description: Free text about this element, for the people who read the schema.
--     * Slot: SbeMessageSetV2_id Description: Autocreated FK slot
-- # Class: SbeGroupV2 Description: A repeating group, whose entries each hold the same fields, and which must have at least one field.
--     * Slot: id
--     * Slot: dimension_type Description: The composite, by name, that sends a repeating group's entry count and entry size.
--     * Slot: since_version Description: The schema version that added this element.
--     * Slot: deprecated_since Description: The schema version that retired this element, which stays only for older applications.
--     * Slot: symbolic_name Description: What the schema calls this element.
--     * Slot: sbe_id Description: The number that identifies this element.
--     * Slot: block_length Description: The octets set aside for a message's fixed-length fields, or for those of each group entry.
--     * Slot: alignment Description: The multiple of octets where a message or each group entry begins.
--     * Slot: semantic_type Description: What this element means at the FIX application layer.
--     * Slot: description Description: Free text about this element, for the people who read the schema.
--     * Slot: SbeBlockV2Mixin_id Description: Autocreated FK slot
--     * Slot: SbeMessageV2_id Description: Autocreated FK slot
--     * Slot: SbeGroupV2_id Description: Autocreated FK slot
-- # Class: SbeFieldV2 Description: A message's or group entry's field, which uses an encoding at a place in its block and may state a constant.
--     * Slot: id
--     * Slot: symbolic_name Description: What the schema calls this element.
--     * Slot: sbe_id Description: The field's FIX tag number.
--     * Slot: encoding_name Description: Which encoding this element uses, by name.
--     * Slot: element_value Description: The text of the XML element, which is the constant when presence is constant.
--     * Slot: offset Description: The octet this element starts at, counted from zero at the start of its block or composite.
--     * Slot: alignment Description: The multiple of octets the start of this field is placed on, in place of an offset.
--     * Slot: presence Description: Whether this element's value is required, optional or constant.
--     * Slot: null_value Description: The value that stands for null in place of the primitive type's default, written as text.
--     * Slot: min_value Description: The lowest value allowed, written as text.
--     * Slot: max_value Description: The highest value allowed, written as text.
--     * Slot: value_ref Description: The valid value that gives a constant element its value.
--     * Slot: semantic_type Description: The FIX datatype this field carries.
--     * Slot: description Description: Free text about this element, for the people who read the schema.
--     * Slot: since_version Description: The schema version that added this element.
--     * Slot: deprecated_since Description: The schema version that retired this element, which stays only for older applications.
--     * Slot: SbeBlockV2Mixin_id Description: Autocreated FK slot
--     * Slot: SbeMessageV2_id Description: Autocreated FK slot
--     * Slot: SbeGroupV2_id Description: Autocreated FK slot

CREATE TABLE "SbeVersionedMixin" (
	id INTEGER NOT NULL,
	since_version INTEGER,
	deprecated_since INTEGER,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_SbeVersionedMixin_id" ON "SbeVersionedMixin" (id);

CREATE TABLE "SbeMessageSchemaV1" (
	id INTEGER NOT NULL,
	schema_package TEXT,
	sbe_id INTEGER,
	schema_version INTEGER NOT NULL,
	semantic_version TEXT,
	description TEXT,
	byte_order VARCHAR(12),
	header_type TEXT,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_SbeMessageSchemaV1_id" ON "SbeMessageSchemaV1" (id);

CREATE TABLE "SbeRefV1" (
	id INTEGER NOT NULL,
	encoding_name TEXT NOT NULL,
	encoding_kind TEXT NOT NULL,
	symbolic_name TEXT NOT NULL,
	"offset" INTEGER,
	since_version INTEGER,
	deprecated_since INTEGER,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_SbeRefV1_id" ON "SbeRefV1" (id);

CREATE TABLE "SbeSimpleTypeV1" (
	id INTEGER NOT NULL,
	element_value TEXT,
	primitive_type VARCHAR(6) NOT NULL,
	array_length INTEGER,
	character_encoding TEXT,
	null_value TEXT,
	min_value TEXT,
	max_value TEXT,
	presence VARCHAR(8),
	value_ref TEXT,
	semantic_type TEXT,
	description TEXT,
	encoding_kind TEXT NOT NULL,
	symbolic_name TEXT NOT NULL,
	"offset" INTEGER,
	since_version INTEGER,
	deprecated_since INTEGER,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_SbeSimpleTypeV1_id" ON "SbeSimpleTypeV1" (id);

CREATE TABLE "SbeCompositeV1" (
	id INTEGER NOT NULL,
	semantic_type TEXT,
	description TEXT,
	encoding_kind TEXT NOT NULL,
	symbolic_name TEXT NOT NULL,
	"offset" INTEGER,
	since_version INTEGER,
	deprecated_since INTEGER,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_SbeCompositeV1_id" ON "SbeCompositeV1" (id);

CREATE TABLE "SbeEnumV1" (
	id INTEGER NOT NULL,
	encoding_type TEXT NOT NULL,
	semantic_type TEXT,
	description TEXT,
	encoding_kind TEXT NOT NULL,
	symbolic_name TEXT NOT NULL,
	"offset" INTEGER,
	since_version INTEGER,
	deprecated_since INTEGER,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_SbeEnumV1_id" ON "SbeEnumV1" (id);

CREATE TABLE "SbeSetV1" (
	id INTEGER NOT NULL,
	encoding_type TEXT NOT NULL,
	semantic_type TEXT,
	description TEXT,
	encoding_kind TEXT NOT NULL,
	symbolic_name TEXT NOT NULL,
	"offset" INTEGER,
	since_version INTEGER,
	deprecated_since INTEGER,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_SbeSetV1_id" ON "SbeSetV1" (id);

CREATE TABLE "SbeBlockV1Mixin" (
	id INTEGER NOT NULL,
	symbolic_name TEXT NOT NULL,
	sbe_id INTEGER NOT NULL,
	block_length INTEGER,
	semantic_type TEXT,
	description TEXT,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_SbeBlockV1Mixin_id" ON "SbeBlockV1Mixin" (id);

CREATE TABLE "SbeMessageSchemaV2" (
	id INTEGER NOT NULL,
	schema_package TEXT,
	sbe_id INTEGER,
	schema_version INTEGER NOT NULL,
	semantic_version TEXT,
	description TEXT,
	byte_order VARCHAR(12),
	header_type TEXT,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_SbeMessageSchemaV2_id" ON "SbeMessageSchemaV2" (id);

CREATE TABLE "SbeSimpleTypeV2" (
	id INTEGER NOT NULL,
	element_value TEXT,
	primitive_type VARCHAR(6) NOT NULL,
	array_length INTEGER,
	character_encoding TEXT,
	since_version INTEGER,
	deprecated_since INTEGER,
	encoding_kind TEXT NOT NULL,
	symbolic_name TEXT NOT NULL,
	description TEXT,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_SbeSimpleTypeV2_id" ON "SbeSimpleTypeV2" (id);

CREATE TABLE "SbeMemberTypeV2" (
	id INTEGER NOT NULL,
	element_value TEXT,
	primitive_type VARCHAR(6) NOT NULL,
	array_length INTEGER,
	character_encoding TEXT,
	presence VARCHAR(8),
	null_value TEXT,
	min_value TEXT,
	max_value TEXT,
	value_ref TEXT,
	"offset" INTEGER,
	alignment INTEGER,
	encoding_kind TEXT NOT NULL,
	symbolic_name TEXT NOT NULL,
	description TEXT,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_SbeMemberTypeV2_id" ON "SbeMemberTypeV2" (id);

CREATE TABLE "SbeRefV2" (
	id INTEGER NOT NULL,
	encoding_name TEXT NOT NULL,
	"offset" INTEGER,
	alignment INTEGER,
	encoding_kind TEXT NOT NULL,
	symbolic_name TEXT NOT NULL,
	description TEXT,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_SbeRefV2_id" ON "SbeRefV2" (id);

CREATE TABLE "SbeCompositeV2" (
	id INTEGER NOT NULL,
	since_version INTEGER,
	deprecated_since INTEGER,
	"offset" INTEGER,
	alignment INTEGER,
	encoding_kind TEXT NOT NULL,
	symbolic_name TEXT NOT NULL,
	description TEXT,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_SbeCompositeV2_id" ON "SbeCompositeV2" (id);

CREATE TABLE "SbeEnumV2" (
	id INTEGER NOT NULL,
	encoding_type TEXT NOT NULL,
	since_version INTEGER,
	deprecated_since INTEGER,
	"offset" INTEGER,
	alignment INTEGER,
	encoding_kind TEXT NOT NULL,
	symbolic_name TEXT NOT NULL,
	description TEXT,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_SbeEnumV2_id" ON "SbeEnumV2" (id);

CREATE TABLE "SbeSetV2" (
	id INTEGER NOT NULL,
	encoding_type TEXT NOT NULL,
	since_version INTEGER,
	deprecated_since INTEGER,
	"offset" INTEGER,
	alignment INTEGER,
	encoding_kind TEXT NOT NULL,
	symbolic_name TEXT NOT NULL,
	description TEXT,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_SbeSetV2_id" ON "SbeSetV2" (id);

CREATE TABLE "SbeBlockV2Mixin" (
	id INTEGER NOT NULL,
	symbolic_name TEXT NOT NULL,
	sbe_id INTEGER NOT NULL,
	block_length INTEGER,
	alignment INTEGER,
	semantic_type TEXT,
	description TEXT,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_SbeBlockV2Mixin_id" ON "SbeBlockV2Mixin" (id);

CREATE TABLE "SbeValidValue" (
	id INTEGER NOT NULL,
	symbolic_name TEXT NOT NULL,
	description TEXT,
	valid_value TEXT NOT NULL,
	since_version INTEGER,
	deprecated_since INTEGER,
	"SbeEnumV1_id" INTEGER,
	"SbeEnumV2_id" INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY("SbeEnumV1_id") REFERENCES "SbeEnumV1" (id),
	FOREIGN KEY("SbeEnumV2_id") REFERENCES "SbeEnumV2" (id)
);
CREATE INDEX "ix_SbeValidValue_id" ON "SbeValidValue" (id);

CREATE TABLE "SbeChoice" (
	id INTEGER NOT NULL,
	symbolic_name TEXT NOT NULL,
	description TEXT,
	bit_position INTEGER NOT NULL,
	since_version INTEGER,
	deprecated_since INTEGER,
	"SbeSetV1_id" INTEGER,
	"SbeSetV2_id" INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY("SbeSetV1_id") REFERENCES "SbeSetV1" (id),
	FOREIGN KEY("SbeSetV2_id") REFERENCES "SbeSetV2" (id)
);
CREATE INDEX "ix_SbeChoice_id" ON "SbeChoice" (id);

CREATE TABLE "SbeEncodingSetV1" (
	id INTEGER NOT NULL,
	"SbeMessageSchemaV1_id" INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY("SbeMessageSchemaV1_id") REFERENCES "SbeMessageSchemaV1" (id)
);
CREATE INDEX "ix_SbeEncodingSetV1_id" ON "SbeEncodingSetV1" (id);

CREATE TABLE "SbeMemberV1" (
	id INTEGER NOT NULL,
	encoding_kind TEXT NOT NULL,
	symbolic_name TEXT NOT NULL,
	"offset" INTEGER,
	since_version INTEGER,
	deprecated_since INTEGER,
	"SbeCompositeV1_id" INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY("SbeCompositeV1_id") REFERENCES "SbeCompositeV1" (id)
);
CREATE INDEX "ix_SbeMemberV1_id" ON "SbeMemberV1" (id);

CREATE TABLE "SbeMessageV1" (
	id INTEGER NOT NULL,
	since_version INTEGER,
	deprecated_since INTEGER,
	symbolic_name TEXT NOT NULL,
	sbe_id INTEGER NOT NULL,
	block_length INTEGER,
	semantic_type TEXT,
	description TEXT,
	"SbeMessageSchemaV1_id" INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY("SbeMessageSchemaV1_id") REFERENCES "SbeMessageSchemaV1" (id)
);
CREATE INDEX "ix_SbeMessageV1_id" ON "SbeMessageV1" (id);

CREATE TABLE "SbeEncodingSetV2" (
	id INTEGER NOT NULL,
	description TEXT,
	schema_package TEXT,
	sbe_xml_base TEXT,
	"SbeMessageSchemaV2_id" INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY("SbeMessageSchemaV2_id") REFERENCES "SbeMessageSchemaV2" (id)
);
CREATE INDEX "ix_SbeEncodingSetV2_id" ON "SbeEncodingSetV2" (id);

CREATE TABLE "SbeMessageSetV2" (
	id INTEGER NOT NULL,
	description TEXT,
	schema_package TEXT,
	sbe_xml_base TEXT,
	"SbeMessageSchemaV2_id" INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY("SbeMessageSchemaV2_id") REFERENCES "SbeMessageSchemaV2" (id)
);
CREATE INDEX "ix_SbeMessageSetV2_id" ON "SbeMessageSetV2" (id);

CREATE TABLE "SbeMemberV2" (
	id INTEGER NOT NULL,
	"offset" INTEGER,
	alignment INTEGER,
	encoding_kind TEXT NOT NULL,
	symbolic_name TEXT NOT NULL,
	description TEXT,
	"SbeCompositeV2_id" INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY("SbeCompositeV2_id") REFERENCES "SbeCompositeV2" (id)
);
CREATE INDEX "ix_SbeMemberV2_id" ON "SbeMemberV2" (id);

CREATE TABLE "SbeEncodingV1" (
	id INTEGER NOT NULL,
	semantic_type TEXT,
	description TEXT,
	encoding_kind TEXT NOT NULL,
	symbolic_name TEXT NOT NULL,
	"offset" INTEGER,
	since_version INTEGER,
	deprecated_since INTEGER,
	"SbeEncodingSetV1_id" INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY("SbeEncodingSetV1_id") REFERENCES "SbeEncodingSetV1" (id)
);
CREATE INDEX "ix_SbeEncodingV1_id" ON "SbeEncodingV1" (id);

CREATE TABLE "SbeGroupV1" (
	id INTEGER NOT NULL,
	dimension_type TEXT,
	since_version INTEGER,
	deprecated_since INTEGER,
	symbolic_name TEXT NOT NULL,
	sbe_id INTEGER NOT NULL,
	block_length INTEGER,
	semantic_type TEXT,
	description TEXT,
	"SbeBlockV1Mixin_id" INTEGER,
	"SbeMessageV1_id" INTEGER,
	"SbeGroupV1_id" INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY("SbeBlockV1Mixin_id") REFERENCES "SbeBlockV1Mixin" (id),
	FOREIGN KEY("SbeMessageV1_id") REFERENCES "SbeMessageV1" (id),
	FOREIGN KEY("SbeGroupV1_id") REFERENCES "SbeGroupV1" (id)
);
CREATE INDEX "ix_SbeGroupV1_id" ON "SbeGroupV1" (id);

CREATE TABLE "SbeElementV2" (
	id INTEGER NOT NULL,
	encoding_kind TEXT NOT NULL,
	symbolic_name TEXT NOT NULL,
	description TEXT,
	"SbeEncodingSetV2_id" INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY("SbeEncodingSetV2_id") REFERENCES "SbeEncodingSetV2" (id)
);
CREATE INDEX "ix_SbeElementV2_id" ON "SbeElementV2" (id);

CREATE TABLE "SbeMessageV2" (
	id INTEGER NOT NULL,
	since_version INTEGER,
	deprecated_since INTEGER,
	symbolic_name TEXT NOT NULL,
	sbe_id INTEGER NOT NULL,
	block_length INTEGER,
	alignment INTEGER,
	semantic_type TEXT,
	description TEXT,
	"SbeMessageSetV2_id" INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY("SbeMessageSetV2_id") REFERENCES "SbeMessageSetV2" (id)
);
CREATE INDEX "ix_SbeMessageV2_id" ON "SbeMessageV2" (id);

CREATE TABLE "SbeFieldV1" (
	id INTEGER NOT NULL,
	symbolic_name TEXT NOT NULL,
	sbe_id INTEGER NOT NULL,
	encoding_name TEXT NOT NULL,
	"offset" INTEGER,
	presence VARCHAR(8),
	value_ref TEXT,
	semantic_type TEXT,
	description TEXT,
	time_epoch TEXT,
	time_unit TEXT,
	since_version INTEGER,
	deprecated_since INTEGER,
	"SbeBlockV1Mixin_id" INTEGER,
	"SbeMessageV1_id" INTEGER,
	"SbeGroupV1_id" INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY("SbeBlockV1Mixin_id") REFERENCES "SbeBlockV1Mixin" (id),
	FOREIGN KEY("SbeMessageV1_id") REFERENCES "SbeMessageV1" (id),
	FOREIGN KEY("SbeGroupV1_id") REFERENCES "SbeGroupV1" (id)
);
CREATE INDEX "ix_SbeFieldV1_id" ON "SbeFieldV1" (id);

CREATE TABLE "SbeGroupV2" (
	id INTEGER NOT NULL,
	dimension_type TEXT,
	since_version INTEGER,
	deprecated_since INTEGER,
	symbolic_name TEXT NOT NULL,
	sbe_id INTEGER NOT NULL,
	block_length INTEGER,
	alignment INTEGER,
	semantic_type TEXT,
	description TEXT,
	"SbeBlockV2Mixin_id" INTEGER,
	"SbeMessageV2_id" INTEGER,
	"SbeGroupV2_id" INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY("SbeBlockV2Mixin_id") REFERENCES "SbeBlockV2Mixin" (id),
	FOREIGN KEY("SbeMessageV2_id") REFERENCES "SbeMessageV2" (id),
	FOREIGN KEY("SbeGroupV2_id") REFERENCES "SbeGroupV2" (id)
);
CREATE INDEX "ix_SbeGroupV2_id" ON "SbeGroupV2" (id);

CREATE TABLE "SbeFieldV2" (
	id INTEGER NOT NULL,
	symbolic_name TEXT NOT NULL,
	sbe_id INTEGER NOT NULL,
	encoding_name TEXT NOT NULL,
	element_value TEXT,
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
	deprecated_since INTEGER,
	"SbeBlockV2Mixin_id" INTEGER,
	"SbeMessageV2_id" INTEGER,
	"SbeGroupV2_id" INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY("SbeBlockV2Mixin_id") REFERENCES "SbeBlockV2Mixin" (id),
	FOREIGN KEY("SbeMessageV2_id") REFERENCES "SbeMessageV2" (id),
	FOREIGN KEY("SbeGroupV2_id") REFERENCES "SbeGroupV2" (id)
);
CREATE INDEX "ix_SbeFieldV2_id" ON "SbeFieldV2" (id);
