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
  A set of encodings, in any order, that may have its own package and may come from another file.
**/
@Data
@EqualsAndHashCode(callSuper=false)
public class SbeEncodingSetV2  {

  private String description;
  private String schemaPackage;
  private String xmlBase;
  private List<SbeElementV2> encodings;


}