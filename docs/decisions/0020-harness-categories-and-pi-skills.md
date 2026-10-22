# 20. Group harness-specific skills in `harness-<name>` categories, starting with pi

- **Status:** accepted
- **Date:** 2026-10-22
- **Amends:** [0017](0017-add-qubes-os-skills.md), [0018](0018-skill-categories.md)

## Context

[0017](0017-add-qubes-os-skills.md) widened the repository from one methodology to a
collection of skills, and required a new record for further topics. The owner now uses the
repository as a catch-all for skills about best practices and secure methodologies, and
for the documentation that records them so they can be reused. Some of those skills are
about a particular agent harness: how it is built, and how to extend, embed or contribute
to it. They are not about a topic such as Qubes OS, and they go stale when the harness
changes, so they should be recognizable and installable as a group.

The harness in question first is [pi](https://github.com/earendil-works/pi), a minimal
coding-agent harness published as an npm-workspaces monorepo. It has two runtimes: the
regular harness (`pi-ai`, `pi-agent-core`, `pi-coding-agent` and supporting libraries) and
`pi-durable`, an experimental durable runtime that shares code with it but is not used by
the pi CLI. The owner studied the monorepo's source on 2026-10-22 (commit `74f468640`,
packages 1.4.0) and wants that knowledge kept as skills.

## Decision

- Skills tailored to one agent harness live in a category folder named
  `skills/harness-<name>/`, where `<name>` is the harness's lowercase name. This applies
  [0018](0018-skill-categories.md) unchanged: the folder has no `SKILL.md`, may have a
  `README.md`, skill names stay unique across the repository, and nesting stays within the
  `skills` CLI's three levels.
- Add `skills/harness-pi/` with three skills:
  - `pi-monorepo-info`: the monorepo's layout, packages, dependency graph, build and check
    scripts, contributor rules, release and packaging.
  - `pi-core`: the regular harness and its internals: the provider layer, the agent loop,
    the coding agent's sessions, tools and extension system, and the supporting libraries.
  - `pi-durable`: the durable runtime, how it differs from the regular harness, and its
    architecture and API.
- The skills follow the same rules as every skill here: self-contained
  ([0010](0010-skills-self-contained.md)), MIT licensed ([0008](0008-mit-licence.md)), and
  grounded in primary sources. Each states the commit and package version it was read
  against, and that it was read from source rather than run.
- The README scope applies to the `secure-repo` methodology; harness skills have their own
  scope, as the Qubes OS skills do.

## Consequences

- A whole harness category installs with one command, for example
  `npx skills add r3b1s/secure-methodologies/skills/harness-pi`.
- The pi skills describe a fast-moving, partly experimental project (`pi-durable` says its
  API changes without notice). They need re-checking against the pi repository at each
  release, and where a clone disagrees the clone wins; each skill says so.
- Claims were taken from source reading by several parallel readers with spot checks, not
  from running pi. Behavior such as crash recovery in the regular harness is stated from
  the absence of code, and the skills say that.
- Further harnesses get their own `harness-<name>` folder without a new record, as long as
  they stay within this scope; a different kind of topic still needs a record.
