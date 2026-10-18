# 14. Fold stack research into the secure-repo skill

- **Status:** accepted
- **Date:** 2026-10-18
- **Amends:** [0007](0007-one-skill-two-layers.md)

## Context

[0007](0007-one-skill-two-layers.md) created a second skill, `research-unfamiliar-stack`,
for researching stacks that have no guidance yet. It is only ever needed while using
`secure-repo`, and as a separate skill it could be missing when `secure-repo` was
installed on its own.

## Decision

Remove the `research-unfamiliar-stack` skill. Its guidance moves into `secure-repo` as
`references/tools/stacks/stack-research.md`, read only when a project's stack has no file
in that folder.

## Consequences

- The repository ships one skill, so installing it brings everything it refers to.
- The guidance loads only when needed, like the skill's other references.
