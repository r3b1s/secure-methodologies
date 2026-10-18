# 13. Store requirements in one folder per level

- **Status:** accepted
- **Date:** 2026-10-18
- **Supersedes:** [0012](0012-one-file-per-requirement.md)

## Context

[0012](0012-one-file-per-requirement.md) stored one file per requirement in a folder per
category, plus a cumulative list file per level. The owner preferred the files themselves
to be grouped by level, with no separate lists to keep in step.

## Decision

- Keep one file per assessment requirement, named by its ID, in the skill's
  `references/osps/` folder.
- Put each file in `level1/`, `level2/` or `level3/`: the folder for the level at which
  the requirement first applies. The Baseline has exactly three levels.
- Because levels are cumulative, a requirement appears only once, in its lowest level's
  folder. A project at level N reads `level1/` up to `levelN/`.
- Drop the category folders and the `level1.md`, `level2.md`, `level3.md` lists. Each
  file still names its category.

The layout, and how to rebuild it for a new Baseline version, is documented in
[docs/maintenance/updating-the-baseline.md](../maintenance/updating-the-baseline.md#how-the-skill-stores-the-baseline).

## Consequences

- The files for a target level are found by folder, with nothing to keep in sync.
- A requirement's level can be read from its path; its category is in its ID.
- If the Baseline changes a requirement's level, its file moves folder.
