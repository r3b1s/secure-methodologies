# Moving a project to a newer Baseline version

> Facts about the Baseline were checked against its upstream repository on 2026-10-18.

Read this only when a project already meets, or claims to meet, an older OSPS Baseline
version and the user wants it audited against, or moved to, a newer one.

## Target version

By default, the target is the version in [baseline.md](baseline.md): the latest stable
release this skill is built around. If the user names a different version, target that
instead; its requirement text then comes from upstream, not from this skill's requirement
files.

## Default: nothing changes on its own

A newer Baseline version changes nothing for a project by default. The project keeps the
version and the results it has until the user deliberately asks for an audit against, or a
move to, a newer version.

## Where versions are published

- Release notes: [`docs/release_notes.md`](https://github.com/ossf/security-baseline/blob/main/docs/release_notes.md)
  in the upstream repository, listing new, modified and removed controls for each version.
- Each version's full text on the [website](https://baseline.openssf.org/), and its
  machine-readable controls as `baseline/OSPS-*.yaml` in the
  [upstream repository](https://github.com/ossf/security-baseline). Git tags exist for
  some versions, but upstream calls them "a convenience" that may not be updated; the
  website's version pages are the reference.

## Steps

1. **Establish where the project stands.** Find the version and level the project
   currently meets, wherever it records them (an earlier audit report, its security
   documentation, a badge entry). If nothing is recorded, ask the human; do not guess.
2. **List what changed between the two versions.** Read the release notes for every
   version between the project's and the target, then compare the requirements themselves.
   Release notes summarise; the requirement text is the source. Upstream's identifier
   rules matter here:
   - Retired identifiers are never reused and stay in the files, marked as retired.
   - A substantial change in meaning gets a new identifier.
   - A minor change, *including a change of level*, keeps the identifier. So compare each
     requirement's text and level, not only which identifiers are new.
3. **Narrow to the project's level.** Levels are cumulative, so keep the new and changed
   requirements at the project's level and below. Note any requirement that moved into or
   out of that range.
4. **Assess each one** against the project, with a status for each (ground rule 7): met,
   not met, not applicable, or not checked. Retired requirements simply stop applying.
5. **Check tool support.** Tools that assess the Baseline, such as the Best Practices Badge
   site, can trail the latest version. Note which version the project's tools support.
6. **Present the result and stop.** Report what the project would have to change to meet
   the target version. What to change, and whether to move at all, is the human's decision
   (ground rules 1 and 2).
7. **Record the new version** once the human has approved and the work is done, wherever
   the project keeps that record.
