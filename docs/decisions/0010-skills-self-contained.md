# 10. Skills are self-contained and do not maintain themselves

- **Status:** accepted
- **Date:** 2026-10-18
- **Amends:** [0001](0001-record-decisions.md), [0006](0006-skills-are-canonical.md)

## Context

[0006](0006-skills-are-canonical.md) made the skills the canonical content, and
[0001](0001-record-decisions.md) allowed skills to refer to decision records by number.
A skill installed with `npx skills` carries only its own folder, so any reference to this
repository's other content (decision records, research, maintainer docs, the README) points
at something the user does not have. A first draft of the skill also included steps for
updating the skill's own content to a new Baseline version, which is not something a user
of the skill does.

## Decision

- Everything inside a skill's folder is self-contained. It references only files within
  that skill's own folder, and external sources (such as upstream Baseline pages). It does
  not reference this repository's decision records, research, maintainer docs or README,
  by link or by number.
- Skills contain no guidance on updating the skill itself. Maintainer guidance lives in
  `docs/` (for now, [docs/maintenance/](../maintenance/)).
- The skill targets the Baseline version it is built around by default, unless the user
  names another. Moving a *project* from an older Baseline version to a newer one is skill
  content, and does not suggest that the skill itself needs changing.

## Consequences

- 0001's note that skills "refer to records by number" no longer applies.
- Anything a skill needs from a decision (such as its goals) is stated in the skill itself.
