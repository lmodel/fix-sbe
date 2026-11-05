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
  An encoding built from members sent one after another, such as a decimal's mantissa and exponent.
**/
@Data
@EqualsAndHashCode(callSuper=false)
public class SbeCompositeV1 extends SbeEncodingV1 {

  private List<SbeMemberV1> compositeMembers;


}