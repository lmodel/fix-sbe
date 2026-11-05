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
  Anything that sets of encodings or composites hold, and the name and text they all have.
**/
@Data
@EqualsAndHashCode(callSuper=false)
public abstract class SbeElementV2  {

  private String encodingKind;
  private String symbolicName;
  private String description;


}