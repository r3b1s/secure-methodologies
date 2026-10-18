# Release and distribute

## When this applies

Preparing an official release, and especially the first one: many Baseline requirements
apply only once a project has made a release.

## Before you start

Read the [project record](../project-record.md). Publishing a release is outward-facing
and hard to reverse; it happens only on the human's decision (ground rule 1).

## Steps

### Before publishing

1. **Checks are clean.** Tests and required checks pass. At level 3, SCA findings are
   dealt with according to policy before release
   ([OSPS-VM-05.02](../osps/level3/OSPS-VM-05.02.md)).
2. **Identify it.** A unique version identifier for the release (level 2) and every asset
   tied to it (level 3)
   ([OSPS-BR-02.01](../osps/level2/OSPS-BR-02.01.md), [OSPS-BR-02.02](../osps/level3/OSPS-BR-02.02.md)).
3. **Describe it.** A change log covering functional and security changes (level 2,
   [OSPS-BR-04.01](../osps/level2/OSPS-BR-04.01.md)).
4. **Make it verifiable.** Signatures, or hashes in a signed manifest (level 2,
   [OSPS-BR-06.01](../osps/level2/OSPS-BR-06.01.md)); at level 3, an SBOM for
   compiled assets ([OSPS-QA-02.02](../osps/level3/OSPS-QA-02.02.md))
   and instructions for verifying integrity and author identity
   ([OSPS-DO-03.01](../osps/level3/OSPS-DO-03.01.md), [OSPS-DO-03.02](../osps/level3/OSPS-DO-03.02.md)).
5. **License it.** An open source licence included with the assets
   ([OSPS-LE-02.02](../osps/level1/OSPS-LE-02.02.md),
   [OSPS-LE-03.02](../osps/level1/OSPS-LE-03.02.md)).
6. **Distribute it safely.** Only through authenticated channels such as HTTPS, a trusted
   registry, or signed releases ([OSPS-BR-03.02](../osps/level1/OSPS-BR-03.02.md)).

### Requirements that start applying with the first release

Assess these before the first release, so they are met when it goes out:

- user guides, and a guide for reporting defects (level 1,
  [OSPS-DO-01.01](../osps/level1/OSPS-DO-01.01.md),
  [OSPS-DO-02.01](../osps/level1/OSPS-DO-02.01.md))
- dependency policy, design and interface descriptions, and a security assessment
  (level 2, [OSPS-DO-06.01](../osps/level2/OSPS-DO-06.01.md),
  [OSPS-SA-01.01](../osps/level2/OSPS-SA-01.01.md), [OSPS-SA-02.01](../osps/level2/OSPS-SA-02.01.md), [OSPS-SA-03.01](../osps/level2/OSPS-SA-03.01.md), [OSPS-SA-03.02](../osps/level3/OSPS-SA-03.02.md))
- support scope and security-update duration (level 3,
  [OSPS-DO-04.01](../osps/level3/OSPS-DO-04.01.md),
  [OSPS-DO-05.01](../osps/level3/OSPS-DO-05.01.md))

### After publishing

- If the release fixes a vulnerability, publish the advisory
  ([OSPS-VM-04.01](../osps/level2/OSPS-VM-04.01.md)).
- Update the release section of the Security Insights file, if the project has one.
- Record the release and the requirement results in the project record.

## Human decision points

- the decision to publish, and when
- signing mechanism, SBOM format and distribution channels
- advisory wording and timing

## Done when

The release is published through authenticated channels, every release requirement at
the level is met, and the project record is updated.
