# Glossary

* [Adapt copy](adapt-copy.md) - An adapt copy: the form of a schema `lokf adapt` writes so that it can sit beside LOKF's, in which concept classes descend from `Concept`. Here it is `.lokf/schema/fix_sbe.yaml`.
* [Message schema](message-schema.md) - Message schema: the XML document SBE defines, which lists the encodings and message templates two counterparties share. `SbeMessageSchemaV1` and `SbeMessageSchemaV2` describe one.
* [Message template](message-template.md) - A message template: one kind of message in a schema, with a number that each message's header sends. `SbeMessageV1` and `SbeMessageV2` describe one.
* [Encoding](encoding.md) - An encoding: how a value is laid out on the wire. SBE has a simple type, a composite, an enumeration and a set, and a field names one by `encoding_name`.
* [Composite](composite.md) - A composite: an encoding built from members sent one after another, such as a decimal's mantissa and exponent. `SbeCompositeV1` and `SbeCompositeV2` describe one.
* [Block](block.md) - Block: the body a message and a group entry share, with its fixed-length fields first, then groups, then variable-length data. `SbeBlockV1Mixin` and `SbeBlockV2Mixin` hold it.
* [Semantic type](semantic-type.md) - A semantic type: what an element means at the FIX application layer. On an encoding or a field it names a FIX datatype, and on a message it holds a FIX MsgType value.
* [Presence](presence.md) - Presence: whether a value is required, optional or constant. `SbePresence` lists the three, and a value left out counts as required.
