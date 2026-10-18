# Ongoing maintenance

## When this applies

Day-to-day work on a project that already meets its level: changes, dependency updates,
vulnerability reports and changes of people.

## Before you start

Read the [project record](../project-record.md) for the level, constraints and standing
permissions. Work only within those (ground rules 2 and 6).

## Steps

### On each change

- Required checks pass, or are bypassed deliberately and visibly
  ([OSPS-QA-03.01](../osps/level2/OSPS-QA-03.01.md)); tests run
  ([OSPS-QA-06.01](../osps/level2/OSPS-QA-06.01.md), [OSPS-QA-06.02](../osps/level3/OSPS-QA-06.02.md), [OSPS-QA-06.03](../osps/level3/OSPS-QA-06.03.md));
  at level 3, a non-author approves
  ([OSPS-QA-07.01](../osps/level3/OSPS-QA-07.01.md)).
- Changes to pipelines get the same scrutiny as code: permissions and untrusted input
  ([OSPS-AC-04.01](../osps/level2/OSPS-AC-04.01.md), [OSPS-AC-04.02](../osps/level3/OSPS-AC-04.02.md),
  [OSPS-BR-01.01](../osps/level1/OSPS-BR-01.01.md), [OSPS-BR-01.03](../osps/level1/OSPS-BR-01.03.md), [OSPS-BR-01.04](../osps/level3/OSPS-BR-01.04.md)).
- New features or breaking changes update the user guides, design description, interface
  descriptions and threat model where they exist
  ([OSPS-DO-01.01](../osps/level1/OSPS-DO-01.01.md),
  [OSPS-SA-01.01](../osps/level2/OSPS-SA-01.01.md), [OSPS-SA-02.01](../osps/level2/OSPS-SA-02.01.md), [OSPS-SA-03.01](../osps/level2/OSPS-SA-03.01.md), [OSPS-SA-03.02](../osps/level3/OSPS-SA-03.02.md)).

### Dependencies

- Review dependency updates before accepting them; an update bot proposes, a person
  decides.
- Act on SCA findings according to the project's policy (at level 3,
  [OSPS-VM-05.01](../osps/level3/OSPS-VM-05.01.md), [OSPS-VM-05.02](../osps/level3/OSPS-VM-05.02.md), [OSPS-VM-05.03](../osps/level3/OSPS-VM-05.03.md)).
- Keep the dependency policy true to practice
  ([OSPS-DO-06.01](../osps/level2/OSPS-DO-06.01.md)).

### Vulnerability reports

- Handle reports through the documented private channel and within the stated timeframe
  ([OSPS-VM-01.01](../osps/level2/OSPS-VM-01.01.md),
  [OSPS-VM-03.01](../osps/level2/OSPS-VM-03.01.md)).
- Publish discovered vulnerabilities once fixed
  ([OSPS-VM-04.01](../osps/level2/OSPS-VM-04.01.md)). Disclosure timing and
  wording are the human's decision.

### People and access

- New collaborators start with the lowest permissions
  ([OSPS-AC-02.01](../osps/level1/OSPS-AC-02.01.md)); at level 3, escalations
  follow the review policy ([OSPS-GV-04.01](../osps/level3/OSPS-GV-04.01.md)).
- Keep the list of members with sensitive access current
  ([OSPS-GV-01.01](../osps/level2/OSPS-GV-01.01.md)); remove access that is no
  longer needed.

### Records

- Update the Security Insights file's `last-updated` when contacts, tools or policies
  change, if the project has one.
- Note significant changes in the project record, and suggest a level review when the
  facts in [levels.md](../levels.md#when-to-move-up-a-level) change.

## Human decision points

- accepting dependency updates and acting on findings
- disclosure of vulnerabilities
- granting and removing access

## Done when

Maintenance is continuous; each change leaves every requirement at the level as met as it
was before.
