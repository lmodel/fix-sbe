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
  A message's or group entry's field, which uses an encoding at a place in its block.
**/
@Data
@EqualsAndHashCode(callSuper=false)
public class SbeFieldV1  {

  private String symbolicName;
  private int sbeId;
  private String encodingName;
  private Integer offset;
  private String presence;
  private String valueRef;
  private String semanticType;
  private String description;
  private String timeEpoch;
  private String timeUnit;
  private Integer sinceVersion;
  private Integer deprecatedSince;


}