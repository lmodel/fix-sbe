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
  A message's or group entry's field, which uses an encoding at a place in its block and may state a constant.
**/
@Data
@EqualsAndHashCode(callSuper=false)
public class SbeFieldV2  {

  private String symbolicName;
  private int sbeId;
  private String encodingName;
  private String elementValue;
  private Integer offset;
  private Integer alignment;
  private String presence;
  private String nullValue;
  private String minValue;
  private String maxValue;
  private String valueRef;
  private String semanticType;
  private String description;
  private Integer sinceVersion;
  private Integer deprecatedSince;


}