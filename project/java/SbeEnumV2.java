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
  An encoding whose value is one of a listed set of valid values.
**/
@Data
@EqualsAndHashCode(callSuper=false)
public class SbeEnumV2 extends SbeMemberV2 {

  private String encodingType;
  private List<SbeValidValue> validValues;
  private Integer sinceVersion;
  private Integer deprecatedSince;


}