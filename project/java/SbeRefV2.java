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
  A composite's member that reuses an encoding defined elsewhere in the schema.
**/
@Data
@EqualsAndHashCode(callSuper=false)
public class SbeRefV2 extends SbeMemberV2 {

  private String encodingName;


}