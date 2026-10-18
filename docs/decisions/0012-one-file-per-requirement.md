# 12. One file per Baseline requirement, with level lists

- **Status:** superseded by [0013](0013-requirements-by-level-folder.md)
- **Date:** 2026-10-18
- **Amends:** [0007](0007-one-skill-two-layers.md)

## Context

[0007](0007-one-skill-two-layers.md) put the guidance for each Baseline category in one
file. To read one requirement, or only the requirements of one level, an agent had to load
a whole category, most of which it did not need. Users may also want to meet a few chosen
requirements from different levels and categories (for example "level 1 plus" in
`levels.md`).

## Decision

- Rename the skill's `references/controls/` folder to `references/osps/`.
- Store each assessment requirement in its own file, `osps/<category>/<requirement ID>.md`,
  in one folder per category named by its ID prefix (`AC`, `BR`, `DO`, `GV`, `LE`, `QA`,
  `SA`, `VM`).
- Add `osps/level1.md`, `level2.md` and `level3.md`, each a cumulative list of the
  requirements in that level, linking to their files.
- The file unit is the assessment requirement (`OSPS-AC-04.01`), not the control
  (`OSPS-AC-04`), because levels are assigned per requirement and one control can span
  levels.

The layout, and how to rebuild it for a new Baseline version, is documented in
[docs/maintenance/updating-the-baseline.md](../maintenance/updating-the-baseline.md#how-the-skill-stores-the-baseline).

## Consequences

- An agent loads one level list, then only the requirement files a task needs; a single
  requirement can be read alone.
- A requirement's path follows from its ID.
- 64 small files replace 8 larger ones, so a Baseline update touches more files; the
  maintainer doc lists every place to update and how to check the result.
