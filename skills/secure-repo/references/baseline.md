# The OSPS Baseline

> Facts about the Baseline were checked against its upstream repository on 2026-10-18.

## Version targeted

This skill targets [OSPS Baseline](https://baseline.openssf.org/) **v2026.08.28**, released
2026-08-28 ([release](https://github.com/ossf/security-baseline/releases/tag/v2026.08.28)),
developed at [github.com/ossf/security-baseline](https://github.com/ossf/security-baseline)
by the OpenSSF Security Baseline SIG. It is the latest stable release this skill is built
around, and the default target unless the user names another version.

For a project that meets an older version, see [baseline-upgrade.md](baseline-upgrade.md).

## Levels and categories

Guidance for each requirement is in its own file, named by its ID, in a folder for the
level where it first applies: [osps/level1/](osps/level1/), [osps/level2/](osps/level2/),
[osps/level3/](osps/level3/) (for example
[osps/level1/OSPS-AC-01.01.md](osps/level1/OSPS-AC-01.01.md)). Levels are cumulative, so
a project at level 2 needs the files in `level1/` and `level2/`; a single requirement can
be read on its own.

### Levels

Quoted from the Baseline's metadata:

| Level | Applies to | Requirements first appearing at this level | Cumulative total | Folder |
|---|---|---|---|---|
| 1 | "any code or non-code project with any number of maintainers or users" | 24 | 24 | [level1/](osps/level1/) |
| 2 | "any code project that has at least 2 maintainers and a small number of consistent users" | 19 | 43 | [level2/](osps/level2/) |
| 3 | "any code project that has a large number of consistent users" | 21 | 64 | [level3/](osps/level3/) |

Levels are cumulative: a project at level 2 meets every level 1 and level 2 requirement.
Which level a project should target, and how risk changes that, is covered in
[levels.md](levels.md).

### Categories

| Category | Covers | Requirements |
|---|---|---|
| Access Control (AC) | who can access the version control system and CI/CD pipelines | 6 |
| Build and Release (BR) | building, packaging and distributing the software | 12 |
| Documentation (DO) | information for users, contributors and maintainers | 8 |
| Governance (GV) | decision-making, roles and contribution | 6 |
| Legal (LE) | licensing and contributors' right to commit | 5 |
| Quality (QA) | source code, dependencies, tests and review | 13 |
| Security Assessment (SA) | design documentation, interfaces, security assessment and threat modelling | 4 |
| Vulnerability Management (VM) | reporting, disclosing and remediating vulnerabilities | 10 |

Counts exclude the retired requirement OSPS-BR-01.02.

## Gaps this skill fills

Places where the Baseline, read against this skill's goals (signals that let strangers
trust a project, software that does not harm the people who use it, nothing private
leaking on publication), either asks for an outcome without saying how, or says nothing.
Each was checked against the requirement text of v2026.08.28. Where a source is named, it
is a candidate, not yet chosen.

| Gap | What the Baseline says | Where this skill addresses it | Candidate source |
|---|---|---|---|
| **Nothing on showing conformance to strangers** | No requirement covers how a project demonstrates that it meets the Baseline: no badge, scan or machine-readable declaration is mentioned | [security-insights.md](security-insights.md) (offered, never required); [platforms/github.md](platforms/github.md) (tools offered on GitHub) | Security Insights; OSPS Baseline scanner; OpenSSF Scorecard |
| **No method for security assessment or threat modelling** | OSPS-SA-03.01 (level 2) requires a security assessment and OSPS-SA-03.02 (level 3) threat modelling and attack-surface analysis, without saying how | [threat-modeling.md](threat-modeling.md) | [Threat Modeling Manifesto](https://www.threatmodelingmanifesto.org/) |
| **Nothing on telling users what risks they accept** | OSPS-SA-03 requires the assessment to be *performed*; the recommendation says it is useful to downstream consumers, but nothing requires publishing it | [threat-modeling.md](threat-modeling.md) | none yet |
| **Security assessment applies only after a release** | OSPS-SA-01 to SA-03 apply "when the project has made a release" | [stages/pre-publication-audit.md](stages/pre-publication-audit.md), [stages/new-project.md](stages/new-project.md) | none needed |
| **Little on the security of the code itself** | Only a SAST remediation policy and blocking SAST check (OSPS-VM-06, level 3) and an SCA equivalent (OSPS-VM-05, level 3). Nothing on reviewing high-risk code, fuzzing or dynamic testing | stage guides; [tools/categories.md](tools/categories.md) | NIST SSDF (Produce Well-Secured Software); OWASP ASVS for web components |
| **Known-vulnerable dependencies are only checked at level 3** | Levels 1 and 2 require a dependency list (OSPS-QA-02.01), standard tooling to ingest dependencies (OSPS-BR-05.01) and a description of how dependencies are chosen and tracked (OSPS-DO-06.01). Automatic checks for known vulnerabilities and malicious dependencies arrive only at level 3 (OSPS-VM-05.03) | stage guides; [tools/categories.md](tools/categories.md) | none needed |
| **No requirement to pin what a build pulls in** | Nothing requires pinning dependencies or CI/CD components to exact versions or hashes; lock files appear only as an option in the recommendation for OSPS-BR-05.01 | stage guides; [tools/categories.md](tools/categories.md) | OpenSSF Scorecard (Pinned-Dependencies check) |
| **Nothing on secure defaults** | OSPS-DO-01.01 asks for highly visible warnings about dangerous or destructive actions, but nothing requires the software to be secure by default | [threat-modeling.md](threat-modeling.md) | CISA Secure by Design |
| **Leaks other than secrets** | OSPS-BR-07.01 requires preventing secrets and credentials being stored in version control. No requirement mentions personal information, or checking existing history before publishing | [stages/pre-publication-audit.md](stages/pre-publication-audit.md) | none yet |
| **Levels ignore what the software does** | Levels depend only on the number of maintainers and users, not on privilege, network exposure or what the software can reach | [levels.md](levels.md) | none yet |
| **Levels do not fit every project** | Level 2 requires at least 2 maintainers. A single-maintainer project with steady users has no obvious level between 1 and 3 | [levels.md](levels.md) | none yet |
| **No order of work** | Requirements are grouped by category, not by when in a project's life they apply | [stages/](stages/) | none needed |

Not listed: release provenance. The Baseline already requires signed releases or signed hashes (OSPS-BR-06.01) and
instructions for verifying them (OSPS-DO-03). SLSA can be added if deeper provenance is
wanted.
