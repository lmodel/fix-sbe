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
  A simple encoding that stands alone in a set, backed by one primitive value, or several in an array.
**/
@Data
@EqualsAndHashCode(callSuper=false)
public class SbeSimpleTypeV2 extends SbeElementV2 {

  private String elementValue;
  private String primitiveType;
  private Integer arrayLength;
  private String characterEncoding;
  private Integer sinceVersion;
  private Integer deprecatedSince;


}