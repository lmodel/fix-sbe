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
  One of the alternatives of a set, which is one bit of its encoding.
**/
@Data
@EqualsAndHashCode(callSuper=false)
public class SbeChoice  {

  private String symbolicName;
  private String description;
  private int bitPosition;
  private Integer sinceVersion;
  private Integer deprecatedSince;


}