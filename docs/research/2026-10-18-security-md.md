# What SECURITY.md is for

- **Date:** 2026-10-18
- **Purpose:** establish what a SECURITY.md file is conventionally for before the skill
  offers a template for one.
- **Outcome:** the definition in the [glossary](../glossary.md#securitymd), and a simple
  template in the skill ([ADR 0015](../decisions/0015-security-md-template.md)).

Facts come from the sources linked, read on the date above.

## Authoritative sources

| Source | What it says the file is for |
|---|---|
| [GitHub: adding a security policy](https://docs.github.com/en/code-security/getting-started/adding-a-security-policy-to-your-repository) | A "security policy" with instructions for reporting a vulnerability; the setup step says to describe supported versions and how to report |
| [GitHub: community health files](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file) | Recognised in `.github/`, the root or `docs/` (checked in that order); an account's public `.github` repository can supply a default |
| [OpenSSF CVD guide for maintainers](https://github.com/ossf/oss-vulnerability-guide/blob/main/maintainer-guide.md) (CC-BY-4.0) | How to contact the team, that reports can stay private until the project discloses, and what the reporter can expect; suggests publishing any disclosure deadline. Its [GitHub template](https://github.com/ossf/oss-vulnerability-guide/blob/main/templates/security_policies/github_security_policy.md) is one paragraph: where to report, what to include, response time, advisory on confirmation, a 90-day disclosure timeline |
| [OpenSSF Scorecard: Security-Policy](https://github.com/ossf/scorecard/blob/main/docs/checks.md) | Scores a reporting link or e-mail (6 points), free text (3) and wording on vulnerabilities, disclosure and time frames (1); advises explaining what counts as a vulnerability and placing the file at the root |
| [OpenSSF Best Practices Badge, passing](https://www.bestpractices.dev/en/criteria/0) | A published reporting process, a private channel if private reports are accepted, first response within 14 days; no passing criterion asks for a wider security document |
| OSPS Baseline v2026.08.28 | Recommends SECURITY.md for security contacts (VM-02.01), a coordinated disclosure policy with a response timeframe (VM-01.01), private reporting (VM-03.01), and optionally support and security-update scope (DO-04.01, DO-05.01) |
| [RFC 9116 (security.txt)](https://www.rfc-editor.org/rfc/rfc9116.html) | A different file: a machine-readable contact file for websites and organisations at `/.well-known/security.txt` (informational RFC, April 2022); does not address source repositories |

## Real SECURITY.md files

| Project | Lines | Contents |
|---|---|---|
| [django/django](https://github.com/django/django/blob/main/.github/SECURITY.md) | 3 | a link to the project's security page |
| [golang/go](https://github.com/golang/go/blob/master/SECURITY.md) | 13 | supported versions; link to the reporting policy |
| [kubernetes/kubernetes](https://github.com/kubernetes/kubernetes/blob/master/.github/SECURITY.md) | 14 | links to the supported-versions policy and the reporting process |
| [astral-sh/uv](https://github.com/astral-sh/uv/blob/main/SECURITY.md) | 15 | what is *not* a vulnerability (uv runs code by design); link to an organisation-wide policy |
| [python/cpython](https://github.com/python/cpython/blob/main/.github/SECURITY.md) | 24 | links to a [full policy](https://devguide.python.org/security/policy/) covering what counts as a vulnerability (a threat model), supported versions, backports, credit and CVE issuance |
| [curl/curl](https://github.com/curl/curl/blob/master/SECURITY.md) | 30 | link to the disclosure policy; reporting link; its Best Practices Gold badge |
| [nodejs/node](https://github.com/nodejs/node/blob/main/SECURITY.md) | 738 | reporting and disclosure, a full threat model with examples of vulnerabilities and non-vulnerabilities, CVE publication, incident response, team membership |

Every file is about vulnerabilities: how to report them and, often, what qualifies. Larger
projects spell out scope in more detail, up to a full threat model, or link to a fuller
policy. None uses the file as a general list of security practices.

## gh-secure's template

[GitHubSecurityLab/gh-secure](https://github.com/GitHubSecurityLab/gh-secure) (MIT, v0.1.0,
2026-09-16) ships a [SECURITY.md template](https://github.com/GitHubSecurityLab/gh-secure/blob/main/SECURITY.md.template).
Its reporting section matches the sources above (no public issues; private reporting or
e-mail; what to include; response times of 48 hours and 7 days; credit; supported
versions). It adds "Security Features" (GitHub features enabled on the repository) and
"Security Best Practices" for contributors. Against this repository's principles: the
reporting instructions and feature list are GitHub-specific; the response times are fixed
in advance, though they are the maintainer's commitment to choose; the feature list is a
claim that can drift from the repository's real settings; contributor practices fit
better in a contribution guide. What gh-secure shows about GitHub's own features is
recorded in [2026-10-18-github-osps-level1.md](2026-10-18-github-osps-level1.md).

## Conclusion

SECURITY.md is the project's vulnerability disclosure policy. Scope (what counts as a
vulnerability) is the one widely used extension. Wider security practices, settings and
trust signals belong elsewhere.
