# 2. Scope of the initial version

- **Status:** accepted
- **Date:** 2026-10-18
- **Amended by:** [0004](0004-include-baseline-legal-controls.md) (legal controls),
  [0017](0017-add-qubes-os-skills.md) (Qubes OS skills)

## Context

An earlier draft of this repository generalised a single audit of one project into a
method, with tool choices and structure decided without the owner. It was discarded so the
scope could be set first, deliberately.

## Decision

The scope is the one stated in the [README](../../README.md#scope). In summary:

- The primary product is context that people and agents follow; other artifacts derive
  from it.
- It is for anyone to adopt, and is carried out by people, agents, or both.
- It applies to repositories containing software; documentation-only repositories are
  mostly out.
- The core is language-neutral and forge-neutral. Stack guidance is added as stacks are
  encountered and is never imposed. GitHub is the only platform covered for now.
- Stages covered: audit before publishing, new project, maintenance, release and
  distribution, periodic re-audit. Archiving is out.
- Goals, in priority order: trust signals for strangers, not harming users, no leaks.
- Effort scales with risk. Constraints are decided per project.
- Code quality is in scope only where it affects security or trust. The threat model a
  project adopts, and the risks of using it, are in scope.
- Out of scope for now: licensing and legal questions (amended by 0004), and privacy
  regulation compliance.

## Consequences

- Everything added to the repository should be checkable against this scope.
- Widening the scope (for example general code quality) needs a new record.
