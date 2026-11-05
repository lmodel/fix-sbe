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
  A repeating group, whose entries each hold the same fields, and which cannot be without a field.
**/
@Data
@EqualsAndHashCode(callSuper=false)
public class SbeGroupV2 extends SbeBlockV2 {

  private String dimensionType;


}