# 7. Start with one methodology skill, in two layers

- **Status:** accepted
- **Date:** 2026-10-18
- **Amended by:** [0012](0012-one-file-per-requirement.md), superseded by [0013](0013-requirements-by-level-folder.md)

## Context

The methodology could be one skill or one per lifecycle stage. Its guidance could be
organised by Baseline control or by stage.

## Decision

Start with a single skill, `secure-repo`, and split it only if it grows too large.
Organise it in two layers: control guidance (how to meet and verify each Baseline control,
one file per category) and stage guides (what to do at each stage), where stage guides link
to controls instead of repeating them. A separate skill, `research-unfamiliar-stack`,
covers researching stacks that have no guidance yet.

## Consequences

- Each control is explained in one place.
- Loading the skill brings in only `SKILL.md`; references are read as needed.
