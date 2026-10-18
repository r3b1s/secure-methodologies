# GitHub's built-in features and OSPS Baseline level 1

- **Date:** 2026-10-18
- **Purpose:** record how much of OSPS Baseline v2026.08.28 level 1 GitHub's own features
  cover, prompted by GitHub Security Lab's gh-secure tool.

Facts come from the sources linked, read on the date above. GitHub's settings and plans
change often; re-check before relying on a detail. The skill's
[GitHub guide](../../skills/secure-repo/references/platforms/github.md) holds the same
facts in usable form.

## gh-secure

[GitHubSecurityLab/gh-secure](https://github.com/GitHubSecurityLab/gh-secure) is a GitHub
CLI extension from GitHub Security Lab (MIT; first release v0.1.0 on 2026-09-16; checked
through the GitHub API). It enables five features on public repositories, following
GitHub Security Lab's recommendations: branch protection, private vulnerability reporting
(with a security policy), secret scanning with push protection, Dependabot, and CodeQL
code scanning. It has a status command, a dry-run mode, and enables features one by one or
all at once. It needs admin or maintain permission on the repository.

It shows that GitHub itself provides much of what level 1 needs, and some of what higher
levels and this skill's gaps need.

## Level 1 requirements and what GitHub provides

| Requirement | GitHub feature | Covered by GitHub alone? |
|---|---|---|
| OSPS-AC-01.01 MFA | two-factor authentication; organisations can require it | partly: required from selected contributors since 2023, enforceable for organisation members |
| OSPS-AC-02.01 collaborator permissions | repository roles | partly: personal-account collaborators always get write access |
| OSPS-AC-03.01, AC-03.02 primary branch | rulesets or branch protection (gh-secure: branch protection) | yes, once configured |
| OSPS-BR-01.01, BR-01.03 pipeline input and untrusted code | Actions hardening guidance; CodeQL can scan workflows (per gh-secure's template) | no: depends on how workflows are written |
| OSPS-BR-03.01, BR-03.02 encrypted channels | GitHub serves repositories and releases over HTTPS | for GitHub-hosted channels; others are the project's |
| OSPS-BR-07.01 secrets kept out | secret scanning (free on public repositories, full history) and push protection (gh-secure: secret scanning) | largely; a local check before commit still helps |
| OSPS-DO-01.01, DO-02.01 user guide, defect reporting | issues | the guides are the project's to write |
| OSPS-GV-02.01 public discussion | issues, discussions | yes |
| OSPS-GV-03.01 contribution process | community health files | the content is the project's |
| OSPS-LE-02.x, LE-03.x licences | a licence file in the repository | the choice and file are the project's |
| OSPS-QA-01.01, QA-01.02 public source and history | public repository | yes |
| OSPS-QA-02.01 dependency list | dependency manifest in the repository | the project's |
| OSPS-QA-04.01 codebases | — | the project's |
| OSPS-QA-05.01, QA-05.02 no binaries | — | the project's |
| OSPS-VM-02.01 security contacts | SECURITY.md as a community health file; private vulnerability reporting (gh-secure: vulnerability reporting) | the file is the project's; PVR gives the private channel that level 2 (VM-03.01) asks for |

Beyond level 1, two gh-secure features serve this skill's gaps and level 3: Dependabot
(known-vulnerable dependencies; OSPS-VM-05.03 if made a required check) and CodeQL code
scanning (OSPS-VM-06.02 if made a required check).

Sources: the GitHub documentation pages cited in the skill's GitHub guide, and the
[gh-secure README](https://github.com/GitHubSecurityLab/gh-secure/blob/main/README.md).
