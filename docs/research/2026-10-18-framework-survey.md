# Framework survey

- **Date:** 2026-10-18
- **Purpose:** choose an external framework to build the methodology on
  ([scope](../../README.md#scope)).
- **Outcome:** [ADR 0003](../decisions/0003-osps-baseline-as-backbone.md), OSPS Baseline as
  backbone.

Facts come from each framework's own site, read on the date above, unless marked
*(secondary)*. "Not verified" means no primary source was found for the claim.

## Candidates

| Framework | Maintained by | Aimed at | Levels | Fit |
|---|---|---|---|---|
| [OSPS Baseline](https://baseline.openssf.org/versions/2026-08-28) v2026.08.28 | OpenSSF Security Baseline SIG | Individual open source projects | 3, defined by users and maintainers | Closest overall |
| [Best Practices Badge](https://www.bestpractices.dev/en/criteria) | OpenSSF | Projects, self-assessed with some automated checks | "Metal" series (passing, silver, gold) and "baseline" series (Baseline levels 1–3) | Public signal; implements the Baseline |
| [Scorecard](https://github.com/ossf/scorecard) | OpenSSF | Automated scan of a repository | 0–10 per check, weighted by risk | A measure, not a method; full support on GitHub, partial on GitLab |
| [SLSA](https://slsa.dev/spec/) v1.2 | Linux Foundation community | Build and source integrity | Build L0–L3; Source track reintroduced in v1.2 | Narrow: releases and provenance |
| [NIST SSDF](https://csrc.nist.gov/projects/ssdf) SP 800-218 v1.1 (2022-02-03) | NIST | Organisations that produce software | None; outcome-based | Widely cited, not checkable per project; v1.2 (SP 800-218 Rev. 1) in draft since 2025-12-17 |
| [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/) 5.0.0 | OWASP | Web applications | L1–L3 *(secondary)* | Detailed, web components only |
| [OWASP SAMM](https://owaspsamm.org/model/) v2.0 | OWASP | Organisations' security programmes | Maturity levels (not described on the page read) | Organisation-level; poor fit |
| [S2C2F](https://github.com/ossf/s2c2f) | OpenSSF Supply Chain Integrity WG | Organisations consuming open source dependencies | Maturity model | Narrow: dependency intake |
| [CISA Secure by Design](https://www.cisa.gov/securebydesign) | CISA | Software manufacturers, at executive level | None (pledge) | Principles only; poor fit |
| [Threat Modeling Manifesto](https://www.threatmodelingmanifesto.org/) | 15 practitioners | Anyone | None | Values and four questions; methodology-agnostic |

## OSPS Baseline in detail

- 64 active requirements (one more, OSPS-BR-01.02, is retired) in 8 categories: Access
  Control (AC), Build and Release (BR), Documentation (DO), Governance (GV), Legal (LE),
  Quality (QA), Security Assessment (SA), Vulnerability Management (VM). MUST statements
  only.
- Levels: 1 applies to any project; 2 to code projects with at least 2 maintainers and a
  small number of consistent users; 3 to code projects with a large number of consistent
  users. Requirements are cumulative.
- Lists mappings to: Best Practices Badge (2024), Scorecard 5.0, NIST CSF 2.0, EU Cyber
  Resilience Act (Regulation (EU) 2024/2847), NIST SSDF 1.1, ISO/IEC 18974, OpenCRE, SLSA,
  P-SSCRM, OWASP SAMM 2, PCI DSS 4.0.1, NIST SP 800-161r1, UK Software Security Code of
  Practice, BSI TR-03185-2. The Baseline states mappings "are not guaranteed to be 100%
  matches".
- Worded generically ("version control system", "CI/CD pipeline"), with GitHub, GitLab and
  Bitbucket as examples.
- Upstream: [github.com/ossf/security-baseline](https://github.com/ossf/security-baseline),
  Apache-2.0, controls as YAML in `baseline/OSPS-*.yaml`, release `v2026.08.28` published
  2026-08-28 (checked through the GitHub API).
- The Best Practices Badge site awards baseline-1/2/3 badges and checks some controls
  automatically; it supported v2025.10.10 as of February 2026
  ([OpenSSF, 2026-02-25](https://openssf.org/?p=9630)).

### Gaps against the scope

- Code-level security: only static analysis and dependency scanning thresholds, at level 3.
- Threat modelling: required (SA-03) but no method given.
- Leaks: secrets in version control (BR-07.01) only; nothing found on personal information
  in history.
- Includes Legal controls, which the initial scope excluded (resolved by
  [ADR 0004](../decisions/0004-include-baseline-legal-controls.md)).
- Changes often: v2025.10.10, v2026.02.19 and v2026.08.28 seen within a year.

### Conflicting source

An OpenSSF brochure ([PDF, 2026-01](https://openssf.org/wp-content/uploads/2026/01/OpenSSF-OSPS-Baseline.pdf),
seen only through a search summary) describes "41 requirements across six lifecycle
stages". Probably an earlier version; the v2026.08.28 page shows 64 requirements by
category.

## Options considered

- **A. OSPS Baseline as backbone**, gaps filled from named sources, Scorecard and the badge
  as measures. Chosen.
- **B. NIST SSDF as backbone.** Lifecycle-shaped and widely cited, but aimed at
  organisations, without levels or a public signal, and its next version is in draft.
- **C. A home-made structure mapped to several frameworks.** Most flexible; repeats the
  problem of invented structure and requires maintaining every mapping.

## Not verified

- ASVS level definitions and requirement counts (secondary sources only).
- Any specific threat modelling technique, such as STRIDE (not researched).
- Which Baseline controls tools such as Minder or Privateer assess (named in an OpenSSF
  brochure, details not found).

## Sources

- https://baseline.openssf.org/ and https://baseline.openssf.org/versions/2026-08-28
- https://github.com/ossf/security-baseline
- https://www.bestpractices.dev/en/criteria
- https://openssf.org/?p=9630
- https://github.com/ossf/scorecard
- https://slsa.dev/spec/ and https://slsa.dev/spec/v1.2/build-track-basics
- https://csrc.nist.gov/projects/ssdf and https://csrc.nist.gov/projects/ssdf/publications
- https://owasp.org/www-project-application-security-verification-standard/
- https://softwaremill.com/whats-new-in-asvs-5-0/ *(secondary)*
- https://owaspsamm.org/model/
- https://github.com/ossf/s2c2f
- https://www.cisa.gov/securebydesign
- https://www.threatmodelingmanifesto.org/
