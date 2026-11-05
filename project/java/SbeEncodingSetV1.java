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
  A set of encodings, listed in any order, whose names are unique across the whole schema.
**/
@Data
@EqualsAndHashCode(callSuper=false)
public class SbeEncodingSetV1  {

  private List<SbeEncodingV1> encodings;


}