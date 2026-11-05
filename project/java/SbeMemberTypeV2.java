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
  A simple encoding inside a composite, which may say it is optional or constant.
**/
@Data
@EqualsAndHashCode(callSuper=false)
public class SbeMemberTypeV2 extends SbeMemberV2 {

  private String elementValue;
  private String primitiveType;
  private Integer arrayLength;
  private String characterEncoding;
  private String presence;
  private String nullValue;
  private String minValue;
  private String maxValue;
  private String valueRef;


}