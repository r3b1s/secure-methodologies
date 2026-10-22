---
name: pi-durable
description: Architecture and API guide for pi-durable (@earendil-works/pi-durable), the experimental durable agent runtime in the pi monorepo — conversations, tasks, documents and extensions committed atomically to storage so a crashed process resumes where it stopped. Explains how it differs from the regular pi harness, the Harness/Conversation/Submission/Task/Document model, the effect-sandwich and replay rules, restart and parking, abort and ownership, compaction, forks, watching and multi-client attach, hot reload, storage backends (memory, JSONL, SQLite, IndexedDB, Cloudflare Durable Objects), execution environments, testing, and a minimal working example. Use when building an agent or service on pi-durable, reading its source, or deciding between pi-durable and the regular pi harness. For the regular harness use pi-core; for the repository layout use pi-monorepo-info.
license: MIT
metadata:
  verified-on: "pi monorepo commit 74f468640 (2026-10-22), pi-durable 1.4.0, read from source; not run"
---

# pi-durable

An **experimental** durable agent harness (the package README says the API changes without
notice). Conversations, model turns, tool calls and your own state are committed to storage
before anything is shown; if the process dies mid-turn, reopening the storage picks the
work up where it stopped. It lives in `packages/durable` of the pi monorepo and was
announced by Earendil as a framework for long-running agents that run anywhere a
JavaScript runtime exists. Source paths below are relative to `packages/durable` unless
noted. The version is 1.4.0; read from source at the commit above, nothing was executed.
When a clone disagrees, the clone wins.

## 1. Relationship to the regular pi harness

pi-durable is a **sibling runtime, not a backend for the pi CLI**.

- `packages/coding-agent` does not import `pi-durable`, `chord` or `pi-env`. The pi CLI
  runs on `pi-agent-core` and its own JSONL sessions.
- pi-durable does not import `pi-agent-core`. It reimplements the loop as durable tasks
  (`GenerationTask`, `ToolTask`) and reuses `pi-ai` (models, messages, tool schemas,
  validation, retry, overflow) and `pi-codemode`. It uses `@earendil-works/chord` for
  context, deltas and SQLite adapters.
- The `pi-agent-core` changelog records that the earlier experimental harness and
  sessions were removed from that package in favor of pi-durable. Upstream says lessons
  from pi-durable are meant to flow back into pi once proven; no code or doc found shows a
  plan to run the pi CLI on it.

| | regular pi (`pi-core`) | pi-durable |
|---|---|---|
| Loop | `runLoop` in memory, no checkpoints | State-machine tasks; every phase commits a checkpoint |
| Persistence | JSONL appended per message, no fsync or lock | One atomic `commit()` of entries, documents and task records; memory, JSONL, SQLite, IndexedDB, Durable Objects |
| Crash | Partial text lost; interrupted tool calls not re-run | Reopen finds live tasks and continues from the last checkpoint |
| Tool replay | Not handled | Intent committed before the effect; re-run only if marked `replay: "safe"` |
| Retried submit | None | `requestId` makes it exactly-once |
| Compaction | Blocking, inline | Background task; waits only near the limit or on overflow |
| System prompt | Built-in sections from files (preamble, tools, rules, `AGENTS.md`, skills, cwd), diffed into the session as patches | No built-in text; host-defined sections, same patch format, replayed from `pi.system` entries (§7) |
| Extensions | Loaded at runtime by jiti from disk | Named bundles in a registry; conversations store names; swap while running |
| Clients | One process; RPC is one client over pipes | Any client attaches to any conversation, gets the current view then changes |
| Branching | Entry `parentId` tree in one file | `fork(at)` shares history up to a point; documents choose inherit/current/fresh |
| Tools run | In the agent process via operations interfaces | In an `ExecutionEnv` your host builds (local Node, remote daemon, sandbox) |

Use pi-durable when the work must survive crashes, run for a long time, be steered from
several places, or run on a server or Durable Object. Use the regular harness for a
single-user terminal session.

## 2. Vocabulary

- **Harness**: storage plus the machinery to run many conversations in parallel.
  `Harness.open(storage, options, context)`.
- **Conversation**: a transcript plus its own agent configuration (model, thinking level,
  extension names, cwd). A handle has no state; compare handles by id. Entries are
  `pi.user`, `pi.assistant`, `pi.tool-result`, `pi.system`, `pi.reset`, `pi.compaction`
  and your own kinds.
- **Submission**: input offered to a conversation (`conversation.submit`); `await
  submission.wait(context)` for the outcome. A `requestId` makes it idempotent.
- **Task**: a durable state machine with named phases. Every unit of work (a model
  request, a tool call, compaction, your own) is one. Built-ins: `pi.generation`,
  `pi.tool`, `pi.compaction`.
- **Document**: typed JSON stored beside the transcript and changed in the same commits
  (todos, plans, usage). Scopes: session, conversation, task.
- **Extension**: a named bundle of tools, system-prompt sections, hooks, task definitions
  and wrappers, installed into a **registry**. Conversations store only names.
- **Context**: the cancellation/telemetry context passed as the last argument of nearly
  every call (`BACKGROUND_CONTEXT` from `@earendil-works/chord/context` for a plain one).

## 3. Minimal example

```ts
import { BACKGROUND_CONTEXT as context } from "@earendil-works/chord/context";
import { createModels } from "@earendil-works/pi-ai/models";
import { openaiProvider } from "@earendil-works/pi-ai/providers/openai";
import { AssistantEntry, createRegistry, Harness, MemoryStorage } from "@earendil-works/pi-durable";

const models = createModels();
models.setProvider(openaiProvider());
const harness = await Harness.open(new MemoryStorage(), { models, registry: createRegistry() }, context);
const root = await harness.root(context, { agent: { model: { provider: "openai", modelId: "<model id>" } } });
const submission = await root.submit({ type: "input", content: "What is the capital of France?" }, context);
const settled = await submission.wait(context);
await harness.close(context);
```

For a real agent, pass a persistent storage (§8), an `env` builder and an extension with
tools. An offline run using the faux provider is in `test/examples/13-chat.ts`. In the
README the answer is committed back with `root.commit((tx) => tx.entry(AssistantEntry,
settled.answer), context)`. Other `Harness` methods: `resume()`, `wake()`, `inspect()`,
`submission(id)`, `abortTask`, `retryTask`, `usage`, `watchTaskGraph`, `createConversation`,
`closed`. Conversation methods: `submit`, `configure`, `commit`, `abort`, `compact`,
`reset`, `fork`, `watch`, `waitForIdle`. `watchEvents(harness, conversationId, context)` is
a free function exported from the package root.

Package `exports`: `.`, `./env`, `./env/node`, `./codemode`, `./tool-search`, `./tools`,
`./images(/node|/cloudflare)`, `./storage/memory`, `./storage/indexeddb`,
`./storage/jsonl(/node)`, `./storage/sqlite(/node|/cloudflare)`, `./testing`. Node
`>=22.19.0`; the portable SQLite and JSONL cores avoid Node APIs and run on Bun or
Cloudflare.

## 4. Architecture

```
src/session/   SessionImpl: the one mutation line, Transaction staging, commit + publish
src/harness/   HarnessImpl (extends SessionImpl), TaskScheduler, Submissions, inbox,
               generation / tool / compaction tasks, views, events, registry, prompt
src/storage/   Storage interface and memory, jsonl, sqlite, indexeddb backends
src/env/       FileSystem, Shell, ExecutionEnv interfaces; NodeExecutionEnv
src/tools/     read, write, edit, bash, powershell        src/codemode/, src/tool-search/
```

Rules that shape everything (spec §1):

1. One Session commit is atomic across entries, documents and task records. Documents
   publish only after the storage commit. Everything visible is already durable.
2. External effects never run inside the mutation transaction.
3. Entries and ids are immutable and never reused. A storage error is fatal: the Harness
   ends and must be reopened.
4. One process owns a storage at a time; there is no cross-process locking. Other clients
   attach to that process (§9). `Harness.open(..., { readOnly: true })` gives a
   read-only session.

### One user message, end to end

1. `Conversation.submit` calls `Submissions.submit`, which dedupes by `requestId` and runs
   `admitSubmission` in a commit. An idle conversation appends the input and starts a
   conversation-owned `pi.generation` task. A busy one stores the input in the `pi.inbox`
   document, placed later at a tool boundary (`postTools`) or at the end (`final`).
2. The commit publishes. The scheduler observes it, reserves all eligible tasks in one
   commit, and runs each task's next phase.
3. `pi.generation` phases: `prepare` (render sections, diff the system prompt into system
   entries, possibly wait on a compaction), `request` (stream the model response,
   `beforeRequest` hook), then a classify step that routes to `poll` (deferred),
   `retry` (retryable error, back to `prepare`), a compaction child (overflow), `answer`
   (stop), or a tool round (toolUse). After tools, `afterTools` runs and the task either
   ends or hands over to a fresh generation.
4. Each tool call is a `pi.tool` task: `call` (resolve, validate, `beforeTool` hooks,
   commit the `execute` intent), `run` (the tool's `execute` with `api.env`), `settle`
   (append the tool result). If reopened in `execute`, the replay rule (§6) decides.
5. Each phase commit is one decision commit; a phase that returns an unchanged checkpoint
   without progress faults. Watches and views read the committed state (§9).

## 5. Tasks

`defineTask({ name, version, initial(input), phases, abort(task, runtime, ctx),
migrate? })`. A phase handler `(task, runtime, context)` must commit a changed
checkpoint or a terminal outcome through `runtime`. Runtime operations include `commit`,
`memo`, `sleepUntil`, `waitForTask`, `abortOwned`, `ownedTasks`, `outcomes`, `entry`,
`env(context)`, `setTimer`, `report`.

States: `pending`, `running`, `waiting`, `sleeping`, `completing` (outcome decided, owned
live work remains), `terminal`.

- **Effect sandwich.** Commit the intent, perform the effect, commit the outcome or next
  phase. Reopening in an intent phase means the effect may already have happened; the
  handler must retry safely, poll, or record the interruption. Work before a sleep is not
  exactly-once.
- **Waiting.** A phase can return `{ status: "waiting", checkpoint, on: [taskIds], policy }`
  with policy `allSettled` or `failFast`; wait cycles are rejected. The README example is
  a checkout that charges four cards and refunds the rest when one fails
  (`test/examples/23-child-tasks.ts`).
- **Memo.** `api.memo(name, candidate?, ctx)` is a first-writer-wins value stored with the
  live task. Hooks that decide something use it so a rerun does not decide again.
- **Versions.** Persisted meaning changed? Bump `version` and provide `migrate`. Stored
  version equal: used; older: `migrate`; newer, or older with no `migrate`: the task
  blocks (`task_too_old`, `migration_failed`).

### Restart and parking

On open, the scheduler turns every surviving `running` task into `pending` and bumps its
`restarts` count. A clean close does not count; a new checkpoint, wait, sleep or outcome
resets the count. When `restarts` reaches `settings.restartLimit` (default 5, `Infinity`
never parks) the task is **parked** as blocked (`restart_limit`) until
`harness.retryTask`. Other block reasons: `missing_task`, `task_too_old`,
`migration_failed`. Tasks marked `abandonOnRestart` are aborted instead of resumed (the
children of a non-replay-safe caller are). Call `harness.resume()` to enable scheduling
after open.

## 6. Tools, replay and hooks

```ts
defineTool({ name, description, parameters /* typebox */,
  execute(args, api, context) { return { output, structuredOutput?, details?, usage?, control? }; },
  replay: "safe" | "unsafe", // default unsafe
  callers?: ("model" | "tools")[], deferred?: true, executionMode?, outputLimits? })
```

- **Replay.** If a crash interrupts a call, it is re-run only when both the stored intent
  and the tool say `replay: "safe"`. Otherwise the model receives an error saying the call
  was interrupted and may have partly run, and decides what to do. Mark a tool safe only
  if running it twice is harmless.
- **Nested calls** (a tool or codemode script calling tools) are keyed by position or an
  explicit key and are **not** exactly-once.
- **`control`** on a result: `addTools`, `terminate`, `handoff` (start a fresh context from
  a note).
- **Extension shape**: `defineExtension({ name, tools?, sections?, hooks?, wraps?, tasks? })`.
  `section(key, render, { tag? })` adds a system-prompt section. `hook(TaskClass, handlers)`
  with ToolTask hooks `beforeTool`, `afterTool` and GenerationTask hooks `beforeRequest`,
  `afterResponse`, `onYield`, `afterTools`. `wrapTool(tool, fn)` and `wrapSection(key, fn)`
  decorate whichever same-named definition won. A later extension's same-named tool
  replaces an earlier one.
- **Built-in tools** (`./tools`): `read`, `write`, `edit`, `bash`, `powershell`; also
  `codemode` (script over tools, results journaled for replay) and `tool_search` (BM25 over
  deferred tools). `createCodingTools` bundles read, write, edit, bash.
- **Subagents**: a tool creates a conversation it owns, configures a smaller model and no
  tools, submits and waits. They survive crashes like any conversation
  (`test/examples/21-subagent-foreground.ts`, `22-subagent-background.ts`).

## 7. Abort, ownership, submissions, compaction

- **Ownership tree.** Conversations and tasks form a tree (`ownership` is `conversation` or
  `task`). Aborting a task aborts what it owns, bottom-up; a task finishing with owned live
  work is `completing`. **Foreground** tasks belong to the current work and stop on
  `conversation.abort()`; **background** tasks (`background: true`, for example threshold
  compaction) keep running when the conversation goes idle and are left alone by ordinary
  aborts.
- **Busy conversations.** `submit({ type: "input", content, whenBusy })` where `whenBusy`
  is `"steer"` (placed after the current tool round), `"followUp"` (the default, after
  the current work) or `"reject"` (throws `ConversationBusy`). Queued inputs survive a
  crash.
- **Compaction** is its own `pi.compaction` task. When context nears the model limit,
  older messages are summarized and the summary placed at the next turn boundary; generation
  waits only if the next request would not fit, and a provider "too long" rejection
  compacts and retries once. Settings: `compaction.enabled`, `reserveTokens`,
  `keepRecentTokens`, `backgroundTokens`, `modelOverrides`. Old entries stay in storage.
  `conversation.reset(handoff?)` starts a fresh context.

### System prompt construction

pi-durable has **no built-in prompt text**: no preamble, no tool guidelines, no
`AGENTS.md` or skills loading. The host installs extensions whose sections produce every
word. (The "You are a concise coding assistant" preamble in the examples is written by the
example host.) The only built-in section is `codemode`, which lists callable, non-deferred
tools and appears only when that extension is installed. The `read`, `write`, `edit` and
`bash` tools carry their model-facing guidance in their descriptions, and nothing installs
them automatically (`createCodingTools`).

**Representation.** A section is `section(key, render, { tag? })`. `render(input, context)`
receives the conversation id, the resolved agent (tools, cwd), the `env`, `shown` (what the
transcript currently shows) and a `read` helper; returning `undefined` omits the section.
Tagged sections become `<key>...</key>`. Keys match `/^[a-z][a-z0-9_-]*$/` and are unique
per extension; `instructions` is reserved and renders last. Order follows extension install
order, and a later extension's same-key section replaces the earlier one in place.
`wrapSection(key, fn)` decorates whichever definition won. Tools are not prompt text: they
are declarations carried on the same system messages as `toolsAdded`/`toolsRemoved`.

**Per request (`pi.generation` `prepare` phase).**

1. Replay the transcript's `pi.system` entries to get what is currently *shown* (a value
   sets a section, `null` deletes it).
2. Render every section from the live agent configuration to get what is *desired*. A
   section that throws keeps its shown text and the error is reported.
3. `planSystemEntries` diffs desired against shown and appends a **minimal patch**, for
   example `{ role: "system", content: "", sections: { cwd: "/repo/packages" } }`. Tool
   changes ride on the last section entry or get their own entry. With no change, nothing is
   appended.
4. Two fallbacks: if the change would alter the *order* of sections or tools, it removes all
   and re-adds all; and after a head marker (`pi.reset` or a compaction) with no later
   `pi.system`, it writes a fresh baseline containing every section and tool, plus `omit`
   edits for the older `pi.system` entries.

**Storage and audit.** Only `pi.system` entries are persisted, holding the already-rendered,
already-tagged text and tool declarations. Render functions, the agent and the env are not
stored; shown state is recomputed by replay. So the transcript records exactly what the
model saw, and renderers must be deterministic.

**Provider side.** The request carries only `{ messages }`; the baseline system message in
the transcript is the prompt, and `leadWithSystem` keeps the first one at the front. In
`pi-ai`, a provider that supports mid-conversation system messages gets the deltas
(Anthropic: leading `system` block plus native tool add/remove blocks; OpenAI-style APIs:
`Updated system prompt section "name":` messages). Providers without delta support (Google,
Bedrock, Codex) get one collapsed message with the full replayed text on every request. An
unchanged prefix adds no bytes, which keeps prompt caches warm.

**Versus the regular harness.** Both store the same `SystemMessage` patch format from
`pi-ai`. pi builds a fixed set of sections from files on disk (preamble, tools, rules, docs,
`AGENTS.md`, skills, cwd) and offers `SYSTEM.md` and extension events to override them;
pi-durable has no defaults and lets the host define all sections, with no whole-prompt
override.

## 8. Documents, forks, storage, environments

**Documents.** `defineDoc({ kind, version, scope, history, fork, initial, migrate?,
checkpointWhen })`. `scope` is `session`, `conversation` or `task`. For conversation
documents `history` is `latest` or `rewindable`, and `fork` is `initial` (fresh),
`current` (parent's current value) or, for rewindable ones, `asOf` (parent's value at the
fork point). `defineDocFamily` adds a key. Built-ins: `pi.agent`, `pi.provider`,
`pi.live`, `pi.inbox`, `pi.usage`. `fork(at)` creates a conversation that sees the
parent's history up to that point without copying it, with a fresh provider session id.

**Storage** (`./storage/*`). One interface: `commit(writes, adopt, context)` persists a
batch atomically and calls `adopt(seq)` once, synchronously, after it is durable;
`mintId()` is monotonic across reopen. Backends:

| Backend | Open with | Notes |
|---|---|---|
| Memory | `new MemoryStorage()` | Not persisted. |
| JSONL | `openNodeJsonlStorage(dir, context, { fsync? })` | Keeps the whole history in memory; a failed write poisons the instance. |
| SQLite | `openNodeSqliteStorage(path, options?)` | `node:sqlite`, WAL; table `prefix` option. |
| Cloudflare DO | `openDurableObjectSqliteStorage(ctx.storage, options?)` | SQLite-backed Durable Objects only. |
| IndexedDB | `IndexedDbStorage.open(name, options?)` | Browser; wrap its lifetime in a Web Lock. |

A custom backend (key-value store, Postgres) implements `Storage` and must pass
`registerStorageConformance` from `./testing`.

**Execution environments.** `ExecutionEnv` = `FileSystem` + `Shell` (`./env`). The host
supplies `HarnessOptions.env`, a builder such as
`({ cwd }) => new NodeExecutionEnv({ cwd: cwd ?? process.cwd() })`, called for a
conversation's generation phases and tool attempts; tools reach it as `api.env`. The
builder, not the tool, decides where commands run, so different conversations can run
in different places, but a single tool cannot pick another environment itself.
`pi-env`'s `RemoteExecutionEnv` runs commands on a remote host through a Rust daemon
started over SSH; return it from the builder. `pi-env` depends on `pi-durable`, not the
reverse.

## 9. Watching and many clients

Any client can attach to any conversation. A new client first receives the current view
(transcript, streaming answer, running tools, queued messages, agent, usage), then only
changes. `conversation.watch()` streams exact committed chord ops (at most 100 pending
frames, then coalesced to the newest view); `watchEvents(harness, id, context)` converts
them into pi-style agent events. Late join: `test/examples/20-late-join.ts`. Telemetry goes through
`pi-telemetry` (`pi.durable.*` schema) when you pass a `telemetry` option.

## 10. Hot reload

`registry.install(extension)` under an existing name replaces it in place. Running tool
calls finish on the old code; the next phase or call uses the new. Conversations store
names, so they pick up new code after a restart too. Replacing a **task** definition whose
persisted state changed needs a version bump and `migrate`. Example:
`test/examples/30-reload-and-restart.ts`.

## 11. Errors

`ConversationBusy`, `ReadAfterWrite`, `ReadOnlySession`, `SessionFailed`,
`StorageRequestError` (`src/errors.ts`). Three rules: a storage error ends the Harness
(`harness.closed` resolves with `{reason: "failed", error}`); an invalid read fails only
that call; your code fails only its own unit (a task, a tool).

## 12. Testing and learning more

- `./testing` exports `registerStorageConformance` and `registerEnvConformance`;
  `test/harness-support.ts` (`openHarness`, `addTool`, `addTask`, `addHooks`,
  `addSection`) and `test/session-support.ts` (`ControlledStorage` for injected failures)
  are the patterns to copy. Use the faux provider from `@earendil-works/pi-ai/providers/faux`
  to avoid real models.
- Run an example: `node --conditions=source --experimental-strip-types
  test/examples/NN-name.ts` (00-conversation through 30-reload-and-restart: documents,
  forks, owned conversations, watches, tasks, recovery, system prompt, coding tools,
  inbox, late join, subagents, child tasks, compaction, plan mode, reviewer,
  per-conversation sandbox, tool override, reload and restart). There is no `examples/`
  folder; they are under `test/examples/`.
- `docs/spec.md` (about 5,600 lines) is normative: terms and invariants (§1), core records
  (§2), documents (§3), transactions and storage ownership (§4), tasks (§5: effect
  sandwich, scheduler, ownership, restarts), submissions and inbox (§6), extensions, hooks,
  tools and prompt (§7), built-in tasks (§8), observation (§9), storage contract and
  backends (§10, §11), API footguns (§12), non-goals (§13).

## 13. Pitfalls

- A tool defaults to `replay: "unsafe"`: after a crash the model sees an interruption
  error rather than a re-run. Opt in deliberately.
- Reads inside a `commit` callback must go through `tx`; the commit may be async but the
  mutation line stays held until storage settles.
- Do not open the same storage from two processes. Attach clients to the owner instead.
- `whenBusy` is `steer | followUp | reject`, not "queue".
- Work in a handler between a sleep or wait and the next checkpoint can repeat; design
  phases around the effect sandwich.
- The API is explicitly unstable; re-check signatures against the clone you depend on.
