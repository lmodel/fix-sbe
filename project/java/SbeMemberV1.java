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
  Anything a composite may hold in the order it is sent.
**/
@Data
@EqualsAndHashCode(callSuper=false)
public abstract class SbeMemberV1  {

  private String encodingKind;
  private String symbolicName;
  private Integer offset;
  private Integer sinceVersion;
  private Integer deprecatedSince;


}