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
  One of the values an enumeration allows.
**/
@Data
@EqualsAndHashCode(callSuper=false)
public class SbeValidValue  {

  private String symbolicName;
  private String description;
  private String validValue;
  private Integer sinceVersion;
  private Integer deprecatedSince;


}