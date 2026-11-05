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
  An encoding whose value is any combination of up to 64 choices, sent as a bitset.
**/
@Data
@EqualsAndHashCode(callSuper=false)
public class SbeSetV2 extends SbeMemberV2 {

  private String encodingType;
  private List<SbeChoice> choices;
  private Integer sinceVersion;
  private Integer deprecatedSince;


}