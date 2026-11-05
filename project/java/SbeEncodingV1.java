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
  An encoding of SBE 1.0, which says how a value is laid out on the wire.
**/
@Data
@EqualsAndHashCode(callSuper=false)
public abstract class SbeEncodingV1 extends SbeMemberV1 {

  private String semanticType;
  private String description;


}