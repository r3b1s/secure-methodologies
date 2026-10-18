# Showing Baseline conformance

- **Date:** 2026-10-18
- **Purpose:** find ways a project can demonstrate, with tools it runs itself, that it
  meets the OSPS Baseline, serving the top goal in the [scope](../../README.md#scope):
  signals that let strangers trust a project.
- **Outcome:** [ADR 0011](../decisions/0011-conformance-signals-offered.md).

Facts come from each project's own pages or repository, read on the date above, unless
marked *(secondary)*.

## OpenSSF Best Practices Badge

- Not an external audit. OpenSSF describes badge claims as mostly self-assertions; answers
  are public, and automation checks some criteria and can override false claims
  ([OpenSSF, 2026-02-25](https://openssf.org/?p=9630)).
- Has a "baseline" series (baseline-1/2/3) next to the older "metal" series. As of February
  2026 it supported Baseline v2025.10.10.
- It is a form completed on the badge site, not something a project runs.

## Security Insights

- [Specification](https://security-insights.openssf.org/), maintained under OpenSSF in
  [ossf/security-insights-spec](https://github.com/ossf/security-insights-spec). Latest
  release **v2.2.0**, 2026-01-31 (earlier: v2.1.0 2025-05-09, v2.0.0 2025-01-01; checked
  through the GitHub API).
- One YAML file, `security-insights.yml` or `.yaml`, at the repository root or in the
  forge directory (`.github/`, `.gitlab/`). Two files in one place is an error.
- Sections: `header` (required), `project` and `repository` (required in a single-repository
  file). Required content includes administrators, vulnerability reporting, the licence,
  repository status, core team and a self-assessment comment. Optional content covers
  policy and documentation links, release details and attestations, and security tools by
  type (fuzzing, container, secret, SCA, SAST, other). Taken from
  [`spec/schema.cue`](https://github.com/ossf/security-insights-spec/blob/v2.2.0/spec/schema.cue)
  at v2.2.0.
- Self-declared; the site says to treat it as a snapshot of the commit it ships with.
- Validation, from the [get-started guide](https://security-insights.openssf.org/get-started.html):
  `cue vet -d '#SecurityInsights' schema.cue security-insights.yml`.
- Consumers named by the site: LFX Insights (assesses projects against the Baseline),
  CLOMonitor, the OSPS Baseline scanner, and si-tooling.
- The minimum example in the v2.2.0 release declares `schema-version: 2.0.0`.

## OSPS Baseline scanner

- GitHub Action [`revanite-io/osps-baseline-action`](https://github.com/revanite-io/osps-baseline-action)
  (v1.5.x, Apache-2.0). The Security Insights site's Marketplace link for it returned 404;
  the repository was found through the Baseline repository's own CI
  (`.github/workflows/baseline-scanner.yaml`, which pins v1.5.2 and catalog
  `osps-baseline-2026-02`).
- Wraps Privateer with the [`ossf/pvtr-github-repo-scanner`](https://github.com/ossf/pvtr-github-repo-scanner)
  plugin (Apache-2.0), which also runs locally (`pvtr` CLI) or in Docker.
- Action: level 1 only (hardcoded); default catalog `osps-baseline-2026-02`; output YAML,
  JSON or SARIF, optional upload to code scanning; needs a personal access token; GitHub
  only; no badge mentioned.
- Plugin: catalog `osps-baseline` tracks the latest bundled catalog (2026-08 per its
  README); level 1 checks are the most tested, levels 2 and 3 still in development;
  unverifiable checks return "Needs Review"; many checks depend on a Security Insights file;
  optional AI review of SA-01.01 to SA-03.02 evidence needs a model provider.

## OpenSSF Scorecard

- [Repository](https://github.com/ossf/scorecard), Apache-2.0. 19 checks, each 0–10,
  combined into a risk-weighted score.
- Runs as a GitHub Action, or a CLI (binary, Docker, Nix, Homebrew) that needs a GitHub
  token. A `--local` mode is shown by a secondary source
  ([Context7](https://context7.com/ossf/scorecard)); which checks work there is not
  verified.
- Badge: requires the Action with `publish_results: true`, which also publishes results to
  the REST API and the scorecard.dev viewer.
- GitHub fully supported; GitLab partly (several checks unsupported).
- Does not assess the Baseline; the Baseline maps to Scorecard 5.0. A Scorecard version
  grading against Baseline controls appears only as a proposal in a third-party post
  ([safeguard.sh](https://www.safeguard.sh/resources/blog/openssf-scorecard-v6-roadmap-osps-baseline),
  not verified).

## Observations

- All three runnable options centre on GitHub today, at odds with the goal of a
  forge-neutral core. Security Insights is a plain file and forge-neutral in itself; its
  consumers are not.
- The scanner Action's default catalog trails the Baseline version the skill targets.

## Not verified

- Which Scorecard checks work in `--local` mode.
- The token scopes the Baseline scanner plugin needs.
