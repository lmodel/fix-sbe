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
  A message template, whose number and block length are sent in each message's header.
**/
@Data
@EqualsAndHashCode(callSuper=false)
public class SbeMessageV1 extends SbeBlockV1 {



}