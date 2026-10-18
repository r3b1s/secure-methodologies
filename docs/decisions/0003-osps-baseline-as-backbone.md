# 3. Use the OSPS Baseline as the backbone

- **Status:** accepted
- **Date:** 2026-10-18

## Context

The owner wanted the method to rest on a real, external framework, partly to align with
outside organisations, rather than on a structure invented here. Ten candidates were
surveyed ([research record](../research/2026-10-18-framework-survey.md)). Three options
were considered: the OSPS Baseline as backbone, NIST SSDF as backbone, or a home-made
structure mapped to several frameworks.

## Decision

Use the [OpenSSF OSPS Baseline](https://baseline.openssf.org/) as the backbone. The Baseline
defines *what* a project must meet at each maturity level. This repository supplies *how*:
the process for each lifecycle stage, the tool catalog, and the skills. Where the Baseline
asks for an outcome without saying how, or does not cover something in scope, named
external sources fill the gap. Candidates noted so far: the Threat Modeling Manifesto for
threat modelling, NIST SSDF or OWASP ASVS for code-level practice, SLSA for releases.
OpenSSF Scorecard and the Best Practices Badge (baseline series) serve as measures.

## Consequences

- Fits the scope's priorities: it targets individual projects, its levels scale with the
  project's audience, it is worded without depending on a forge, and the Best Practices
  Badge gives a public signal for it.
- The Baseline publishes mappings to other frameworks (SSDF, CRA, SLSA, Scorecard, SAMM and
  others). The Baseline itself warns these are not exact; no conformance to those
  frameworks is claimed here unless separately checked.
- The Baseline is thin on how to review code and on leaks other than secrets; this
  repository must fill those gaps explicitly.
- The Baseline changes often, so the version followed must be pinned (see 0005).
