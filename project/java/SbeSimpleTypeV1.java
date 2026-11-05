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
  An encoding backed by one primitive value, or several in an array.
**/
@Data
@EqualsAndHashCode(callSuper=false)
public class SbeSimpleTypeV1 extends SbeEncodingV1 {

  private String elementValue;
  private String primitiveType;
  private Integer arrayLength;
  private String characterEncoding;
  private String nullValue;
  private String minValue;
  private String maxValue;
  private String presence;
  private String valueRef;


}