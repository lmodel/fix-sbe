package example;

/* metamodel_version: 1.12.0 */
/* version: 1.0 and 2.0-rc3 */
import java.net.URI;
import java.time.LocalDate;
import java.time.LocalTime;
import java.time.ZonedDateTime;
import java.util.List;
import lombok.*;

/**
  One SBE 1.0 message schema, with its encodings and message templates.
**/
@Data
@EqualsAndHashCode(callSuper=false)
public class SbeMessageSchemaV1  {

  private String schemaPackage;
  private Integer sbeId;
  private int schemaVersion;
  private String semanticVersion;
  private String description;
  private String byteOrder;
  private String headerType;
  private List<SbeEncodingSetV1> encodingSets;
  private List<SbeMessageV1> messages;


}