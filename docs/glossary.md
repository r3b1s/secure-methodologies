# Glossary

Terms as this repository uses them, with the sources each definition rests on.

## Security model

A short, easily visible section of a project's README that explains the project's threat
model and what using the software means for the user: what it protects and from whom,
what it does with privilege and why, what it trusts and does not protect against, each
accepted risk with its reason, and how a cautious user can reduce their exposure. It is
the published result of the threat modelling in the skill's `threat-modeling.md`.

Not the same as [SECURITY.md](#securitymd), which tells people how to report a
vulnerability. `SECURITY.md` may link to the security model to explain what counts as a
vulnerability, and a Security Insights file may link to it as evidence of its
self-assessment. Decided in [ADR 0016](decisions/0016-security-model-in-readme.md).

## SECURITY.md

A repository's **vulnerability disclosure policy**: the file that tells someone who has
found a security problem in the project how to report it privately, and what will happen
when they do. Conventionally it covers:

- who to contact, and the private channel to use (not a public issue)
- what to include in a report
- how quickly the project will respond, and what it does with a confirmed vulnerability
- when and how vulnerabilities are disclosed
- which versions receive security fixes

Projects often add **scope**: what does and does not count as a vulnerability in this
project. Larger projects keep the file short and link to a fuller policy elsewhere. It is
not a general description of the project's security practices.

GitHub recognises the file in the repository root, `.github/` or `docs/`, and an account
can provide a default for all its repositories from its public `.github` repository.

The OSPS Baseline recommends it for security contacts (OSPS-VM-02.01), a coordinated
disclosure policy with a response timeframe (OSPS-VM-01.01) and private reporting
(OSPS-VM-03.01).

Sources, read 2026-10-18: [GitHub: adding a security policy](https://docs.github.com/en/code-security/getting-started/adding-a-security-policy-to-your-repository),
[GitHub: community health files](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file),
[OpenSSF CVD guide for maintainers](https://github.com/ossf/oss-vulnerability-guide/blob/main/maintainer-guide.md),
[OpenSSF Scorecard: Security-Policy check](https://github.com/ossf/scorecard/blob/main/docs/checks.md).
Research: [2026-10-18-security-md.md](research/2026-10-18-security-md.md).
