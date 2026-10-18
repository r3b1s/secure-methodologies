# Periodic re-audit

## When this applies

Only when the human asks for one. Nothing in this skill starts a re-audit on its own; a
new Baseline version, a passing date or a level change is a reason to suggest one, not to
begin.

## Before you start

- Read the [project record](../project-record.md): the version, level, constraints and
  previous results are the starting point.
- Keep the Baseline version the project was assessed against, unless the human asks to
  move to a newer one; then follow [baseline-upgrade.md](../baseline-upgrade.md).

## Steps

1. **Check the level still fits.** Re-establish maintainers, users, releases, privilege
   and exposure ([levels.md](../levels.md)). Propose a change if the facts changed.
2. **See what changed.** Review the changes since the last assessment: code, pipelines,
   dependencies, people with access, and platform settings.
3. **Re-run the tool baseline** with the tools the project uses, and compare with the
   previous results.
4. **Re-read high-risk code that changed**, with the same priorities as in the
   [pre-publication audit](pre-publication-audit.md) (step 3).
5. **Update the threat model** and the README's security model section
   ([threat-modeling.md](../threat-modeling.md)).
6. **Reassess every requirement at the level** (the files in
   `../osps/level1/` up to the project's level), not only the ones touched by changes; settings and documents
   drift.
7. **Report the differences** from the previous assessment alongside the current status
   (ground rule 7), and propose fixes.
8. **Update the project record** once the human approves.

## Human decision points

- whether to change level or Baseline version
- each fix and each accepted risk

## Done when

Every requirement at the level has a current status with evidence, the differences from
the last assessment are reported, and the project record is updated.
