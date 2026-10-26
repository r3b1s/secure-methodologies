# 18. Group related skills in category folders

- **Status:** accepted
- **Date:** 2026-10-21
- **Amends:** [0006](0006-skills-are-canonical.md)
- **Amended by:** [0020](0020-harness-categories-and-pi-skills.md) (harness categories),
  [0021](0021-add-design-category-and-material-design-3-skill.md) (design category)

## Context

[0006](0006-skills-are-canonical.md) placed each skill at `skills/<name>/`. With Qubes OS
skills added ([0017](0017-add-qubes-os-skills.md)), related skills should sit together
without a category folder being mistaken for a skill. The
[`skills` CLI](https://github.com/vercel-labs/skills) treats `skills/` as a container and
searches it up to three levels deep. A folder counts as a skill only if it contains
`SKILL.md`, and the search does not descend below a skill. This was read in the CLI source
(`src/skills.ts`, `src/blob.ts`, commit a80e4c9, 2026-10-19) and tested on 2026-10-21 by
listing and installing a copy of this repository with the layout below.

## Decision

- Related skills may be grouped as `skills/<category>/<skill>/SKILL.md`. A category folder
  never contains a `SKILL.md`. It may contain a `README.md` that lists its skills for
  people.
- Skills that stand alone stay at `skills/<skill>/`. `secure-repo` stays where it is.
- Skill names are unique across the whole repository, because installed skills are placed
  by name without their category (for example `.claude/skills/qubes-dom0-cli/`).
- Nesting stays within the CLI's limit: `skills/<category>/<skill>/` uses two of the three
  levels it searches.

## Consequences

- A whole category installs with one command, by pointing the CLI at its folder:
  `npx skills add r3b1s/secure-methodologies/skills/qubes-os`.
- Single skills still install by name with `--skill <name>`, wherever they sit.
- If the CLI's discovery rules change, the layout must be re-checked against them.
