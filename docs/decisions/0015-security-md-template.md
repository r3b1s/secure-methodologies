# 15. SECURITY.md is the vulnerability disclosure policy, with a simple template

- **Status:** accepted
- **Date:** 2026-10-18

## Context

The skill needed a view of what a SECURITY.md is for before offering a template. Research
([record](../research/2026-10-18-security-md.md)) found that GitHub, the OpenSSF
vulnerability disclosure guide, Scorecard, the Best Practices Badge and real projects all
treat it as the place to learn how to report a vulnerability privately and what happens
next; scope (what counts as a vulnerability) is the common extension.

## Decision

- Define SECURITY.md in a repository [glossary](../glossary.md#securitymd) as the
  project's vulnerability disclosure policy.
- For the first iteration, ship one simple template in the skill
  (`skills/secure-repo/assets/SECURITY.md.template`), following the structure of the GitHub
  security policy template in the OpenSSF Vulnerability Disclosure Guide (the OpenSSF
  also stewards the OSPS Baseline), credited in the template. It covers the private
  channel, what to include, response time, handling of confirmed reports, disclosure
  timeline and supported versions, all as placeholders for the maintainers to decide.

## Consequences

- The template meets the reporting side of OSPS-VM-02.01, and with a private channel and
  a timeframe filled in, VM-01.01 and VM-03.01.
- Richer content (scope, supported-version policy, links to a security model) can be added
  in a later iteration.
