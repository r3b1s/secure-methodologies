---
name: pi-monorepo-info
description: Overview of the official pi monorepo (github.com/earendil-works/pi) that holds the pi coding agent and every package around it — pi-ai, pi-agent-core, pi-coding-agent, pi-tui, pi-mcp, pi-codemode, pi-telemetry, chord, pi-durable, pi-env, pi-evals. Covers the layout, what each package is for, how they depend on each other, the build order, root npm scripts and check scripts, the contributor rules in AGENTS.md and CONTRIBUTING.md, versioning and releases, Nix packaging, and how to run pi or its tests from source. Use when working in a clone of the pi repository, deciding which package a change belongs in, running its build, check or tests, or preparing a contribution. For how the pi harness works inside, use pi-core; for the durable runtime, use pi-durable.
license: MIT
metadata:
  verified-on: "pi monorepo commit 74f468640 (2026-10-22), all packages 1.4.0"
---

# The pi monorepo

Pi is a minimal, extensible coding-agent harness. Its source lives in one npm-workspaces
monorepo, `earendil-works/pi`, which also holds the libraries pi is built from and a
second, separate runtime (`pi-durable`). This skill is the map. The other two skills in
this category go inside: `pi-core` (the normal harness) and `pi-durable`.

Read from source at the commit above (2026-10-22), not by running the build. Where a clone
disagrees with this file, the clone wins. Paths below are relative to the repository root.

## 1. Packages

All packages are in `packages/`, share the npm scope `@earendil-works`, and have the same
version (1.4.0 at the commit above; they are released in lockstep). Node `>=22.19.0`.

| Directory | npm name | Purpose |
|---|---|---|
| `ai` | `pi-ai` | Unified LLM API: ~42 providers, model catalog, streaming, auth/OAuth, tool schemas (typebox), usage and cost, overflow and retry helpers. |
| `agent` | `pi-agent-core` | The in-memory agent loop: `Agent`, tool calling, steering and follow-up queues, events, hooks. No persistence. |
| `coding-agent` | `pi-coding-agent` | The `pi` CLI and SDK: tools, JSONL sessions, compaction, extensions, skills, packages, interactive/print/json/rpc modes. |
| `tui` | `pi-tui` | Terminal UI library with differential rendering, kitty keyboard protocol, overlays. |
| `mcp` | `pi-mcp` | Standalone MCP client (stdio and streamable HTTP, OAuth). No official SDK dependency. |
| `codemode` | `pi-codemode` | Model-written JavaScript in a QuickJS sandbox whose only capability is calling injected tools. |
| `telemetry` | `pi-telemetry` | Vendor-neutral telemetry contracts (spans, metrics, propagation), reference adapter, conformance tests. |
| `chord` | `chord` | Typed host runtime for hot-reloadable objects, replicated JSON state and RPC. Plumbing for durable. |
| `durable` | `pi-durable` | Experimental durable runtime: conversations, tasks and documents committed to storage, resumable after a crash. |
| `env` | `pi-env` | Remote execution environments for durable: a Rust daemon deployed over SSH plus a TypeScript `ExecutionEnv` client. |
| `evals` | `pi-evals` | Private evaluation harness (not published). |

Everything is TypeScript except the Rust daemon in `packages/env/daemon/`. The root
README lists only seven of these as packages (chord, telemetry, ai, durable, agent-core,
coding-agent, tui); codemode, mcp, env and evals are in the workspace and the build too.
Slack and chat automation live in a separate repository, `earendil-works/pi-chat`.

## 2. Dependency graph

Internal dependencies only:

```
telemetry   (leaf)
tui, codemode, mcp   (leaves)
chord   -> telemetry
ai      -> telemetry
agent   -> ai
durable -> chord, ai, codemode, telemetry
env     -> chord, durable
coding-agent -> agent, ai, codemode, mcp, tui
evals   (dev) -> ai, coding-agent
```

Consequences worth knowing:

- `coding-agent` does **not** import `durable`, `chord` or `env`. The two runtimes are
  siblings that share `ai` and `codemode`. A few things are duplicated by hand, with a
  "keep in sync" comment (for example shell resolution in
  `packages/coding-agent/src/utils/shell.ts` and `packages/durable/src/env/node.ts`).
- `durable` does not use `pi-agent-core`. It has its own loop.
- `agent` has no persistence, retry or overflow handling; the host (coding-agent) applies
  the helpers that `ai` exports.

## 3. Root layout

| Path | What it is |
|---|---|
| `AGENTS.md` | Rules for contributors and for agents working in the repo (§6). |
| `CONTRIBUTING.md` | The contribution gate and PR rules (§6). |
| `package.json` | Workspace root (private). Workspaces: `packages/*`, `apps/*` (absent in the public repo) and five example extensions under `packages/coding-agent/examples/extensions/`. |
| `biome.json` | Biome lint and format: tabs, indent width 3, line width 120. |
| `tsconfig.base.json`, `tsconfig.json` | Strict TypeScript, `erasableSyntaxOnly`, `verbatimModuleSyntax`, `module NodeNext`, `noEmit`; root `paths` alias every package to its source. |
| `vitest.base.ts` | Shared vitest aliases mapping `@earendil-works/*` to each package's `src`. |
| `scripts/` | About 75 build, check, release and test helpers. |
| `test.sh` | Runs the non-e2e test suite in an isolated environment (§5). |
| `pi-test.sh` (`.ps1`, `.bat`) | Runs pi from source (§5). |
| `flake.nix`, `nix/` | Nix packaging (§7). |
| `.github/` | `APPROVED_CONTRIBUTORS`, issue templates, 14 workflows (CI, binaries, nix, env daemons, audit, model catalog, contribution gates). |
| `.husky/pre-commit` | Blocks lockfile commits, then runs `npm run check`. |
| `.pi/` | The repository's own agent assets: skills (`release`, `interactive-testing`, `add-llm-provider`, `github-work`), prompt templates and four extensions. |

The README's list of docs lives in each package: `packages/coding-agent/docs/` (about 47
files), `packages/durable/docs/spec.md`, `packages/chord/docs/`, `packages/env/docs/`.

## 4. Build order and root scripts

The root `build` script builds in dependency order: telemetry, chord, tui, codemode, mcp,
ai, durable, env, agent, coding-agent. `build:offline` is the same but skips the network
step that refreshes model data in `ai`.

| Script | What it does |
|---|---|
| `npm run check` | Biome with `--write`, then pinned-deps, runtime-deps, ts-imports, entry-graphs, install-lock and browser-smoke checks, then `tsc --noEmit`. Does not run tests. |
| `npm test` | `test:scripts` (node `--test` on `scripts/*.test.*`) then each workspace's `test`. Includes e2e tests that activate when provider env vars are present, which is why contributors use `./test.sh`. |
| `npm run generate:models`, `hydrate:model-data`, `check:model-data`, `generate:model-catalog`, `diff:model-catalog`, `update:model-catalog-pin`, `check:model-catalog(-compat)` | Model catalog tooling for `ai` and the Nix pin. |
| `npm run eval` | Runs `pi-evals`. |
| `npm run profile:tui`, `profile:rpc` | Profile the coding agent. |
| `version:*`, `release:*`, `publish`, `pack:packages` | Lockstep versioning and release (§7). |

What the `check` scripts enforce:

- `check-pinned-deps`: direct dependencies must be exact versions (workspace, file, git and
  http specifiers are skipped). `.npmrc` sets `save-exact=true` and `min-release-age=2`.
- `check-runtime-deps`: public packages may not import undeclared runtime dependencies
  (TypeScript AST scan).
- `check-ts-relative-imports`: no relative `.js` imports in non-declaration `.ts`.
- `check-entry-graphs`: per-export module-graph file budgets, so an entry point cannot
  silently pull in a large graph.
- `generate-coding-agent-install-lock --check`: the coding-agent install lock must match
  what the script generates. New dependencies with lifecycle scripts need an explicit
  allowlist entry in that script.
- `check-browser-smoke`: esbuild bundles of browser entries, failing on forbidden Node
  adapters.
- Pre-commit `check-lockfile-commit`: refuses lockfile changes unless
  `PI_ALLOW_LOCKFILE_CHANGE=1`.

## 5. Running pi and the tests from source

```sh
./pi-test.sh [--no-env] [args]   # runs packages/coding-agent/src/cli.ts through a source resolver
./test.sh                        # non-e2e tests, isolated env: no API keys, temp HOME
```

`--no-env` unsets provider API keys. `test.sh` runs under `env -i` with a temporary
`HOME` and `PI_NO_LOCAL_LLM=1`.

One test file, from the package's own directory:

```sh
node "$(git rev-parse --show-toplevel)/node_modules/vitest/dist/cli.js" --run test/specific.test.ts
node --test test/specific.test.ts   # packages/tui uses node:test
```

Coding-agent tests under `test/suite/` use `test/suite/harness.ts` and the faux provider:
never a real provider, key or paid token. Durable examples run with
`node --conditions=source --experimental-strip-types test/examples/NN-name.ts`.

Install with `npm install --ignore-scripts` (or `npm ci --ignore-scripts`); refresh the
lockfile with `npm install --package-lock-only --ignore-scripts`.

## 6. Contributor and agent rules

Summarized from `AGENTS.md` and `CONTRIBUTING.md`; read them before contributing, they
change.

**Code**

- No `any` unless unavoidable; inline single-use helpers; top-level imports only (no
  `await import()` or `import("pkg").Type`).
- Only erasable TypeScript syntax in `packages/*/src`, `packages/*/test` and coding-agent
  examples: no `enum`, `namespace`, parameter properties, `import =`, `export =`.
- In coding-agent, resolve package assets through `src/config.ts`, never `__dirname`.
- Never hardcode a key check; add defaults to `DEFAULT_EDITOR_KEYBINDINGS` or
  `DEFAULT_APP_KEYBINDINGS` so they stay configurable.
- Never edit `packages/ai/src/models.generated.ts` by hand: change
  `packages/ai/scripts/generate-models.ts` and regenerate. Generated data in
  `packages/ai/src/providers/data/` is gitignored.
- Ask before removing code that looks intentional. No backward compatibility unless asked.

**Commands**

- After code changes run `npm run check` and fix everything it reports.
- Do not run `npm run build` or `npm test` unless asked. Never run the full vitest suite
  directly; use `./test.sh`.
- A new or changed test file must be run and made to pass. A regression test for a GitHub
  issue carries a comment with the issue number.

**Git**

- Several pi sessions may share one working directory, so stage explicit paths only (no
  `git add -A` or `git add .`), and commit only files you changed.
- Commit subject format `{feat,fix,docs}[(ai,tui,agent,coding-agent)]: message`. No emojis.
- Never `reset --hard`, `checkout .`, `clean -fd`, `stash`, `--no-verify` or force-push.
  Never commit unless asked.

**Changelogs**: `packages/*/CHANGELOG.md`, entries under `## [Unreleased]` with the
subsections Breaking Changes, Added, Changed, Fixed, Removed. Released sections are
immutable. Note the two documents disagree: `AGENTS.md` tells agents to add entries while
`CONTRIBUTING.md` tells outside contributors not to edit `CHANGELOG.md`; follow
`CONTRIBUTING.md` unless you are a maintainer.

**Contribution gate (outside contributors)**

- New contributors' issues and PRs are closed automatically until a maintainer approves
  them: a maintainer replies `lgtmi` (issues allowed) or `lgtm` (issues and PRs allowed).
  `lgtmi` does not allow PRs.
- Use one of the two issue templates. Write it yourself and keep it short; unreviewed
  AI-generated text is not accepted.
- A PR needs prior approval, and both `npm run check` and `./test.sh` must pass.

## 7. Versioning, releases and packaging

- **Lockstep versions.** `scripts/sync-versions.js` fails if non-private packages differ;
  `version:patch|minor|major|set` runs `npm version --workspaces`, syncs, and refreshes the
  lockfile. The repository's release skill (`.pi/skills/release.md`) says patch for fixes
  and additions, minor for breaking changes, and no major releases, though
  `scripts/release.mjs` still accepts `major`.
- **Release** (`scripts/release.mjs`): clean-tree check, verify packages exist on npm, pin
  the newest model catalog, bump, date the changelogs, run checks, commit `Release vX.Y.Z`,
  tag, add a fresh `[Unreleased]`, push. Publishing uses
  `npm publish --provenance --access public --ignore-scripts` through npm trusted
  publishing (OIDC) in `build-binaries.yml`.
- **CI** (`.github/workflows/ci.yml`): `npm ci --ignore-scripts`, build, check, build the
  env daemon, test, and an MCP conformance job. Binaries for darwin-arm64, darwin-x64,
  linux-x64, linux-arm64, windows-x64 and windows-arm64 are built on `v*` tags.
- **Nix.** `nix profile add github:earendil-works/pi/stable` installs the latest release;
  `stable` is fast-forwarded on tags. Nix builds are offline, so bundled model data comes
  from a pi.dev model-catalog revision pinned in `nix/model-catalog.json`; refresh it with
  `npm run update:model-catalog-pin`. At runtime pi still overlays newer catalog data.

## 8. Which package does a change belong in?

| The change is about | Package |
|---|---|
| A provider, model, streaming event, auth flow, token or cost accounting | `ai` |
| The agent loop, tool-call scheduling, steering/follow-up semantics, loop hooks | `agent` |
| CLI behavior, built-in tools, sessions, compaction, extensions API, settings, modes | `coding-agent` |
| Rendering, input handling, keybinding or component behavior | `tui` |
| MCP protocol or OAuth for MCP | `mcp` |
| The script sandbox | `codemode` |
| Durable tasks, storage, resume, multi-client conversations | `durable` (storage backends in `durable/src/storage`) |
| Remote command or file execution for durable | `env` |
| Cross-process hot-reloadable state or RPC plumbing | `chord` |

## 9. Where to read next

- `pi-core` (this category): the harness internals.
- `pi-durable` (this category): the durable runtime and how it differs.
- Upstream: the repository README, `packages/coding-agent/docs/how-pi-works.md`,
  `packages/durable/README.md` and `docs/spec.md`, and the design RFCs linked from the
  README (https://rfc.earendil.com/keyword/pi/).
