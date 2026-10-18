# Updating the skill to a new Baseline version

Maintainer guidance for this repository: how to move the `secure-repo` skill itself to a
newer OSPS Baseline version. It is not part of any skill. (Moving a *project* to a newer
version is covered inside the skill, in `references/baseline-upgrade.md`.)

Facts about the Baseline were checked against its upstream repository on 2026-10-18.

## Default: nothing changes on its own

A new Baseline version changes nothing by default. The skill keeps targeting its current
version until a maintainer deliberately decides to adopt the new one.

## Where updates are published

- Release notes: [`docs/release_notes.md`](https://github.com/ossf/security-baseline/blob/main/docs/release_notes.md)
  in the upstream repository, listing new, modified and removed controls and new framework
  mappings for each version.
- Maintenance process: [`docs/maintenance.md`](https://github.com/ossf/security-baseline/blob/main/docs/maintenance.md).
  It says a new version is considered at least once a year, versions are identified by
  date, previous versions stay available and stable, and changes are announced on the
  [SIG mailing list](https://lists.openssf.org/g/openssf-sig-security-baseline).
- Versions on the [website](https://baseline.openssf.org/). Git tags exist (`v2026.02.19`,
  `v2026.08.28`), but the maintenance process calls them "a convenience" that may not be
  updated, so the website's version pages are the reference.

## Adopting a new version

1. **Notice it.** Check the release notes, the website or the mailing list for a version
   newer than the one the skill targets (`baseline-version` in
   [SKILL.md](../../skills/secure-repo/SKILL.md)).
2. **Read the release notes.** List the new, modified and removed controls, and the
   changes to framework mappings.
3. **Compare the controls themselves.** Compare the `baseline/OSPS-*.yaml` files of the two
   versions (for example `git diff <old-tag> <new-tag> -- baseline/` in a clone, if both are
   tagged). Release notes summarise; the files are the source. A schema migration can make
   the diff noisy (v2026.08.28 moved to Gemara v1), so compare requirement by requirement.
4. **Apply the identifier rules** from the maintenance process:
   - Retired identifiers are never reused and stay in the files, marked as retired.
   - A substantial change in meaning gets a new identifier.
   - A minor change, *including a change of level*, keeps the identifier. So check each
     requirement's text and level, not only which identifiers are new.
5. **Check tool support.** Tools that assess the Baseline can trail it. The Best Practices
   Badge site, for example, supported v2025.10.10 in February 2026.
6. **Decide, and record it.** Record the adoption in a decision that supersedes
   [ADR 0005](../decisions/0005-pin-baseline-version.md).
7. **Update the skill.** Work through the [layout below](#how-the-skill-stores-the-baseline):
   - **Requirement files.** For each new requirement, add `osps/level<N>/<requirement
     ID>.md`, where N is the level at which it first applies. For each modified one,
     update its file, including the level line and the "after a release" marker; if its
     level changed, move the file to the matching folder. For each retired or removed one,
     delete its file. Each file's "Exact text" link carries the version in its URL; update
     every link to the new version.
   - **Everything that links to requirements.** Search the skill for links to requirement
     files that were added, removed or moved: the stage guides, `levels.md`,
     `threat-modeling.md`, `baseline.md` (its gap table cites requirement IDs) and
     `platforms/github.md` (its mapping table).
   - **Counts and version.** The counts per level and per category in `baseline.md` and
     `levels.md`, the `baseline-version` field and the description in `SKILL.md`, and the
     [README](../../README.md).
8. **Check the result.** Every link and anchor resolves; every requirement in the new
   version has exactly one file, in the folder for the level where it first applies, and
   its level line agrees; and no file inside a skill links outside that skill (see
   [ADR 0010](../decisions/0010-skills-self-contained.md)).

## How the skill stores the Baseline

Decided in [ADR 0013](../decisions/0013-requirements-by-level-folder.md). Inside
`skills/secure-repo/references/osps/`:

```
osps/
  level1/   requirements that first apply at level 1
  level2/   requirements that first apply at level 2 (level 1's are not repeated)
  level3/   requirements that first apply at level 3
    OSPS-AC-01.01.md   one file per assessment requirement, named by its ID
```

- **The Baseline has three levels** (its metadata defines `maturity-1` to `maturity-3`).
  They are cumulative, so each folder holds only the requirements that first apply at
  that level; a project at level N reads `level1/` up to `levelN/`.
- **The unit is the assessment requirement** (for example `OSPS-AC-04.01`), not the
  control (`OSPS-AC-04`). Levels are assigned per requirement, and one control can hold
  requirements at different levels (`OSPS-AC-04.01` is level 2, `OSPS-AC-04.02` level 3),
  so its requirements can sit in different folders.
- **There are no index files.** A folder's listing is the list of its requirements.
- **Retired requirements have no file.** `baseline.md` notes them where counts are given.
- **Each requirement file** holds: the requirement ID as title; its control ID, control
  title and category; its level, with "after a release" where the requirement applies
  only after a release; a link to the exact upstream text; a status line; any
  category-wide note (for example "not legal advice" in LE, "also before first
  publication" in SA); then **Requires**, **Meet it** and **Verify**. Requirements are
  summarised in the skill's own words; the upstream text is the authority.
- **Links inside requirement files** to other skill files are relative to
  `osps/level<N>/`, so they start with `../../`.

The data for levels, control titles and release applicability comes from the upstream
`baseline/OSPS-*.yaml` files of the version being adopted (`applicability` lists the
levels, and the lowest is where a requirement first applies; a requirement whose text
begins "When the project has made a release" applies only after a release).
