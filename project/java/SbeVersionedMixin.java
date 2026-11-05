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
  The two attributes that record when an element entered a schema and when it should leave.
**/
@Data
@EqualsAndHashCode(callSuper=false)
public class SbeVersionedMixin  {

  private Integer sinceVersion;
  private Integer deprecatedSince;


}