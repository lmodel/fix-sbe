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
  The body shared by a message and a group entry, which holds its fixed-length fields first, then groups, then variable-length data.
**/
@Data
@EqualsAndHashCode(callSuper=false)
public abstract class SbeBlockV2  {

  private String symbolicName;
  private int sbeId;
  private Integer blockLength;
  private Integer alignment;
  private String semanticType;
  private String description;
  private List<SbeFieldV2> blockFields;
  private List<SbeGroupV2> repeatingGroups;
  private List<SbeFieldV2> varDataFields;
  private Integer sinceVersion;
  private Integer deprecatedSince;


}