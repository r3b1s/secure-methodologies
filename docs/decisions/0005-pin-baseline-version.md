# 5. Pin the Baseline version and review upstream before upgrading

- **Status:** accepted
- **Date:** 2026-10-18

## Context

The Baseline released several versions within a year (v2025.10.10, v2026.02.19 and
v2026.08.28 were all seen during the survey), and tools that implement it, such as the Best
Practices Badge site, can trail the latest version.

## Decision

Follow OSPS Baseline **v2026.08.28**, the latest release on 2026-10-18. Record the upstream
repository, [github.com/ossf/security-baseline](https://github.com/ossf/security-baseline),
where the controls are developed and published in machine-readable form, so new releases
can be reviewed, and checked for proactively, before they are adopted. Adopting a new
version is a deliberate change with its own record.

## Consequences

- Control IDs and titles in the skill come from the pinned release.
- The procedure for reviewing a new version is to be written in the skill's Baseline
  reference.
