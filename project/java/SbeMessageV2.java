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
public class SbeMessageV2  {

  private Integer sinceVersion;
  private Integer deprecatedSince;
  private String symbolicName;
  private int sbeId;
  private Integer blockLength;
  private Integer alignment;
  private String semanticType;
  private String description;
  private List<SbeFieldV2> blockFields;
  private List<SbeGroupV2> repeatingGroups;
  private List<SbeFieldV2> varDataFields;


}