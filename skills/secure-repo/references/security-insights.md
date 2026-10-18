# Creating a Security Insights file

> Facts about the specification were checked against its upstream repository on
> 2026-10-18.

Read this only when the user wants to create a Security Insights file, or agrees to one
when it is offered.

## What it is

A [Security Insights](https://security-insights.openssf.org/) file is one YAML file in
which a project's maintainers declare security facts that tools cannot discover on their
own: contacts, how vulnerabilities are reported, policies, release details and the
security tools in use. Tools such as LFX Insights and the OSPS Baseline scanner read it.
It is self-declared, and it describes the commit it ships with, not necessarily the
project's current state.

This workflow targets **schema v2.2.0**
([release](https://github.com/ossf/security-insights-spec/releases/tag/v2.2.0),
[schema](https://github.com/ossf/security-insights-spec/blob/v2.2.0/spec/schema.cue),
[minimum example](https://github.com/ossf/security-insights-spec/blob/v2.2.0/examples/example-minimum.yml),
[full example](https://github.com/ossf/security-insights-spec/blob/v2.2.0/examples/example-full.yml)).

## Steps

1. **Check for an existing file.** Look for `security-insights.yml` or
   `security-insights.yaml` at the repository root and in the forge directory (`.github/`,
   `.gitlab/` and so on). If one exists, stop and ask whether to review it instead. Two
   files in the same place is an error under the specification; report it.
2. **Settle the layout.** A single repository holds both a `project` and a `repository`
   section. A project spread over several repositories keeps `project` in a parent file
   that each repository's file points to with `header.project-si-source`. If it is unclear
   which applies, ask.
3. **Fill in what the repository shows.** Work through the [field table](#field-table).
   Record where each value came from.
4. **Ask for the rest, in one go.** Put every remaining question to the user together,
   grouped by section, with any value you found offered as a proposal to confirm. Never
   invent a value: contacts, booleans such as `bug-bounty-available`, and the repository's
   status all come from the repository or from the user.
5. **Validate the draft**, if the [CUE](https://cuelang.org/) tool is available:

   ```sh
   curl -O https://raw.githubusercontent.com/ossf/security-insights-spec/v2.2.0/spec/schema.cue
   cue vet -d '#SecurityInsights' schema.cue security-insights.yml
   ```

   A passing run prints nothing. If CUE is not installed, ask whether to install it or to
   skip validation; if skipped, say so in the preview.
6. **Preview and wait for approval.** Show the user:
   - the complete YAML exactly as it would be written
   - for each value, where it came from: found in the repository (and where), given by the
     user, or a fixed value such as the schema version
   - optional fields left out, and the validation result

   Write nothing until the user approves (ground rule 2). If they change anything, show
   the preview again.
7. **Write the file** where the user chooses: the repository root or the forge directory.
   The OSPS Baseline scanner looks at the root and at `.github/security-insights.yml`.
8. **Report** what was written, whether it was validated, and which values are still
   unconfirmed (ground rule 7). Remind the user that `header.last-updated` should change
   whenever contacts, tools or policies change, and that the specification's guide
   suggests reviewing the file every one to six months. Validating it in CI is a pipeline
   change: offer it, do not add it.

## Field table

Required fields are in **bold**. "Ask" means: ask the user, offering anything found as a
proposal. Every URL must be absolute (`http://` or `https://`), so files in the repository
are referenced by their public URL. If the repository is not public yet, say that those
URLs will not resolve until it is.

### `header`

| Field | Value |
|---|---|
| **`schema-version`** | `2.2.0` |
| **`last-updated`**, **`last-reviewed`** | today's date, `YYYY-MM-DD` |
| **`url`** | the public raw URL the file will have once committed: derive it from the remote, the default branch and the chosen location, then confirm |
| `project-si-source` | multi-repository layouts only: the parent file's raw URL |

### `project`

| Field | Where to look |
|---|---|
| **`name`** | README title, package metadata; confirm |
| **`administrators`** | `MAINTAINERS`, `CODEOWNERS`, `SECURITY.md`; ask. Each contact needs `name` and `primary` (exactly one primary); `affiliation`, `email`, `social` are optional. Do not take e-mail addresses from commit metadata without asking |
| **`repositories`** | this repository: `name`, `url` (from the remote) and `comment` (from the README's description) |
| **`vulnerability-reporting.reports-accepted`** | `SECURITY.md`; ask if absent |
| **`vulnerability-reporting.bug-bounty-available`** | `SECURITY.md`; otherwise ask |
| `vulnerability-reporting.policy`, `contact`, `pgp-key`, `in-scope`, `out-of-scope`, `bug-bounty-program` | `SECURITY.md` |
| `homepage`, `roadmap`, `funding`, `steward` | README, package metadata, `FUNDING.yml` |
| `documentation.*` (`quickstart-guide`, `detailed-guide`, `design`, `code-of-conduct`, `release-process`, `support-policy`, `signature-verification`) | matching files or links in the repository |

### `repository`

| Field | Where to look |
|---|---|
| **`url`** | the remote |
| **`status`** | ask; one of `active`, `abandoned`, `concept`, `inactive`, `moved`, `suspended`, `unsupported`, `WIP` |
| **`accepts-change-request`** | `CONTRIBUTING.md`, README; confirm |
| **`accepts-automated-change-request`** | a dependency update tool's configuration suggests `true`; confirm |
| **`core-team`** | as for `administrators` |
| **`license.expression`**, **`license.url`** | the licence file and package metadata; an SPDX expression |
| **`security.assessments.self.comment`** | a summary of any security assessment done, with `evidence` (for example a link to the README's security model section), `date` and `name` if available; otherwise ask. The specification's minimum example uses "Self assessment has not yet been completed." |
| `security.assessments.third-party` | ask |
| `security.champions` | ask |
| `security.tools` | security tools configured in the repository (CI configuration, pre-commit hooks). For each: `name`, `type` (`fuzzing`, `container`, `secret`, `SCA`, `SAST` or `other`), `rulesets` (`["default"]` unless customised), `integration` (`adhoc`, `ci`, `release`, each true or false) and `results` (may be empty). List only tools actually configured |
| `documentation.*` (`contributing-guide`, `security-policy`, `governance`, `review-policy`, `dependency-management-policy`) | matching files in the repository |
| `bug-fixes-only`, `no-third-party-packages` | ask, or leave out |
| `release` | only if the project makes releases. Needs **`automated-pipeline`** (is there a release workflow?) and **`distribution-points`** (where releases are published, each with `uri` and `comment`); optional `changelog`, `license`, `attestations` |
