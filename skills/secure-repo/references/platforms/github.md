# GitHub

> Facts checked against GitHub's documentation on 2026-10-18; GitHub changes its settings
> and plans often, so re-check before relying on a detail. Platform-specific steps only;
> the core guidance does not depend on GitHub. Every setting change here is the human's
> decision (ground rule 1).

## Tools to offer

Two automated tools give a GitHub project a public, repeatable signal that strangers can
check. Neither is required by this skill. When the repository is hosted on GitHub, ask the
user whether they would like each one; add it only if they say yes (ground rule 1). On any
other host, do not offer them.

### OSPS Baseline scanner

- **What it does:** assesses the repository against the OSPS Baseline and reports a
  verdict per requirement (passed, failed, or needs review when it cannot verify one).
  Output is YAML, JSON or SARIF, optionally uploaded to the repository's Security tab.
- **Forms:** the GitHub Action
  [`revanite-io/osps-baseline-action`](https://github.com/revanite-io/osps-baseline-action),
  or the scanner it wraps,
  [`ossf/pvtr-github-repo-scanner`](https://github.com/ossf/pvtr-github-repo-scanner), a
  plugin for the Privateer (`pvtr`) CLI that can also run locally or in Docker.
- **Worth telling the user:**
  - The Action assesses level 1 only (fixed in the Action). Higher levels need the plugin
    directly, and its authors say its level 2 and 3 checks are still in development.
  - The Action's default catalog is `osps-baseline-2026-02`, older than the version this
    skill targets (see [baseline.md](../baseline.md)); the plugin's README says its bundled
    catalog tracks 2026-08.
  - Many checks read the project's Security Insights file (see
    [security-insights.md](../security-insights.md)); without one, more results need review.
  - It needs a personal access token; the workflow's built-in token is not enough.
  - It is GitHub-only.

### OpenSSF Scorecard

- **What it does:** runs a set of automated checks (for example Pinned-Dependencies,
  Token-Permissions, Branch-Protection, SAST, Security-Policy, Vulnerabilities), scores
  each from 0 to 10 and combines them into a score weighted by risk
  ([repository](https://github.com/ossf/scorecard)).
- **Forms:** a GitHub Action, or a CLI (binary, Docker, Nix, Homebrew) that needs a GitHub
  token.
- **Worth telling the user:**
  - A public badge requires running the Action with `publish_results: true`, which also
    publishes the results to the public API and viewer at scorecard.dev.
  - It does not assess the Baseline itself, though the Baseline maps to Scorecard 5.0.
  - GitHub is fully supported; GitLab only partly.

## Repository settings

| Need | GitHub feature | Notes |
|---|---|---|
| MFA for maintainers (OSPS-AC-01.01) | two-factor authentication; an organisation can require it for all members | GitHub required 2FA from selected groups of contributors from March 2023, not from everyone ([docs](https://docs.github.com/en/authentication/securing-your-account-with-two-factor-authentication-2fa/about-mandatory-two-factor-authentication)). For a personal-account repository, ask each maintainer. The Best Practices Badge site treats GitHub-hosted projects as meeting this automatically. |
| Lowest default permissions (OSPS-AC-02.01) | repository roles | On a personal-account repository, collaborators get read and write access; GitHub's documentation says owners can only grant write access to collaborators ([docs](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-personal-account-on-github/managing-personal-account-settings/permission-levels-for-a-personal-account-repository)). An organisation offers finer roles. |
| No direct commits; no deletion of the primary branch (OSPS-AC-03.01, 03.02) | rulesets (or branch protection rules): "Require a pull request before merging", "Restrict deletions", "Block force pushes" | Check who has bypass permissions ([docs](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets)). |
| Required checks (OSPS-QA-03.01) | ruleset rule "Require status checks to pass before merging" | |
| Non-author approval (OSPS-QA-07.01) | the required approvals setting of "Require a pull request before merging"; optionally "Require approval of the most recent reviewable push" and "Dismiss stale pull request approvals when new commits are pushed" | A single-maintainer project cannot meet this without a second reviewer. |
| Private vulnerability reporting (OSPS-VM-03.01) | Settings, Advanced Security, "Private vulnerability reporting" | Reporters then see a "Report a vulnerability" button on the Advisories page ([docs](https://docs.github.com/en/code-security/security-advisories/working-with-repository-security-advisories/configuring-private-vulnerability-reporting-for-a-repository)). |
| Publishing vulnerabilities (OSPS-VM-04.01) | repository security advisories | |
| Secrets kept out of history (OSPS-BR-07.01) | secret scanning and push protection | Secret scanning runs automatically and free on public repositories, across the entire history ([docs](https://docs.github.com/en/code-security/secret-scanning/introduction/about-secret-scanning)). Push protection for users is on by default and stops your account pushing secrets to public repositories; push protection for a repository is off by default and needs GitHub Secret Protection ([docs](https://docs.github.com/en/code-security/secret-scanning/introduction/about-push-protection)). These are platform checks after the fact or at push time; a local check before commit is still worth offering. |
| Contributor sign-off (OSPS-LE-01.01) | "Require contributors to sign off on web-based commits" | Covers only commits made in the web interface ([docs](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/managing-repository-settings/managing-the-commit-signoff-policy-for-your-repository)). Commits from the command line need a status check that verifies sign-off. |

## CI/CD (GitHub Actions)

Guidance from GitHub's [security hardening guide for Actions](https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions)
and [Actions settings](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository):

- **Default token permissions (OSPS-AC-04.01).** Under the repository's Actions settings,
  "Workflow permissions" can give `GITHUB_TOKEN` write access to all scopes, or read access
  to `contents` and `packages` only. New personal-account repositories default to the
  read-only option; organisation repositories inherit the organisation's setting. Check it
  rather than assume it.
- **Per-job permissions (OSPS-AC-04.02).** Grant what each job needs with the
  `permissions` key, starting from read-only.
- **Untrusted input (OSPS-BR-01.01, 01.04).** Do not place event data such as
  `github.event.pull_request.title` directly in `run:` scripts. GitHub recommends passing
  it through an intermediate environment variable (and quoting it), or to an action as an
  argument.
- **Untrusted code (OSPS-BR-01.03).** `pull_request_target` and `workflow_run` run with
  the base repository's privileges; GitHub says such workflows must not check out
  untrusted code, such as code from forks. Treat artifacts from other workflows with
  caution.
- **Fork contributions.** By default, workflows from first-time contributors need approval
  from someone with write access before they run; stricter options exist.
- **Pinning (the pinning gap).** GitHub advises pinning third-party actions to a
  full-length commit SHA from the action's own repository, since tags can move. It
  describes a workflow dependency lock file, where available, as stronger still.
- **Pull requests created by workflows.** "Allow GitHub Actions to create and approve pull
  requests" is off by default for personal-account repositories; leaving it off keeps
  approvals human (OSPS-QA-07.01).
- **Provenance (OSPS-BR-06.01, OSPS-DO-03).** Artifact attestations record where and how
  an artifact was built: generated with the `actions/attest` action (needing `id-token:
  write`, `contents: read` and `attestations: write`) and verified with
  `gh attestation verify` ([docs](https://docs.github.com/en/actions/security-for-github-actions/using-artifact-attestations/using-artifact-attestations-to-establish-provenance-for-builds)).
  Which plans and repository types can use them was not checked.

## Mapping to Baseline controls

Where GitHub features help meet a requirement. Requirements not listed are met by the
project's own files and practices rather than a platform feature.

| Requirement | GitHub feature |
|---|---|
| OSPS-AC-01.01 | two-factor authentication (organisation requirement) |
| OSPS-AC-02.01 | repository roles; organisation for finer roles |
| OSPS-AC-03.01, AC-03.02 | rulesets or branch protection |
| OSPS-AC-04.01, AC-04.02 | workflow permissions setting; `permissions` key |
| OSPS-BR-01.01, BR-01.03, BR-01.04 | workflow design per the hardening guide |
| OSPS-BR-06.01, DO-03.01, DO-03.02 | artifact attestations, or signatures of the human's choosing |
| OSPS-BR-07.01 | secret scanning, push protection |
| OSPS-DO-02.01, GV-02.01 | issues, discussions |
| OSPS-LE-01.01 | web sign-off setting plus a sign-off status check |
| OSPS-QA-01.01, QA-01.02 | public repository and commit history |
| OSPS-QA-03.01 | ruleset: required status checks |
| OSPS-QA-07.01 | ruleset: required approvals |
| OSPS-VM-03.01 | private vulnerability reporting |
| OSPS-VM-04.01 | repository security advisories |
