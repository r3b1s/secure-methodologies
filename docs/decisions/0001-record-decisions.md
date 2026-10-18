# 1. Record decisions as ADRs

- **Status:** accepted
- **Date:** 2026-10-18
- **Amended by:** [0010](0010-skills-self-contained.md)

## Context

This repository exists so that decisions about securing repositories are made once and
recorded, not re-derived per project. The decisions that shape the repository itself need
the same treatment, so that a later reader (person or agent) can see what was decided, when
and why, without relying on chat history.

## Decision

Record each significant decision as an Architecture Decision Record in `docs/decisions/`,
numbered in sequence, using Michael Nygard's format: title, status, date, context, decision,
consequences. A decision that changes an earlier one supersedes it with a new record; the
old record is kept and its status updated.

## Consequences

- Decisions are reviewable and dated.
- Decision records live outside the skills, so they are not included when a skill is
  installed on its own. Skills state what they need inline and refer to records by number.
