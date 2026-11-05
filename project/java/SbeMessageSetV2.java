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
  Message templates held together, which may have their own package and may come from another file.
**/
@Data
@EqualsAndHashCode(callSuper=false)
public class SbeMessageSetV2  {

  private String description;
  private String schemaPackage;
  private URI xmlBase;
  private List<SbeMessageV2> messages;


}