# pi harness skills

[Agent Skills](https://agentskills.io/) for developing with and on
[pi](https://github.com/earendil-works/pi), the minimal coding-agent harness, and its
experimental durable runtime, `pi-durable`.

This folder is a category, not a skill: it has no `SKILL.md`, and each subfolder is one
self-contained skill. Skills specific to one agent harness go in a `harness-<name>`
folder like this one.

| Skill | Use it when |
|---|---|
| [pi-monorepo-info](pi-monorepo-info/SKILL.md) | Working in a clone of the pi repository: which package a change belongs in, the dependency graph, build order, check scripts, tests, contributor rules, releases and Nix packaging. |
| [pi-core](pi-core/SKILL.md) | Writing a pi extension, embedding pi through its SDK or RPC, or changing the regular harness: provider layer, agent loop, sessions, tools, compaction, extensions, skills, and the supporting libraries. |
| [pi-durable](pi-durable/SKILL.md) | Building on `pi-durable`, or deciding between it and the regular harness: tasks and checkpoints, crash resume, replay rules, submissions, documents, forks, storage, execution environments and multi-client attach. |

They were read from the pi source at commit `74f468640` (2026-10-22, all packages 1.4.0),
not by running pi. Where a clone of pi disagrees with a skill, the clone wins.

## Installing

With the [`skills` CLI](https://github.com/vercel-labs/skills):

```sh
npx skills add r3b1s/secure-methodologies/skills/harness-pi    # all three
npx skills add r3b1s/secure-methodologies --skill pi-core       # one skill
```

Add `-g` to install for your user rather than the current project. Skills install by
name, without this category folder (for example `.claude/skills/pi-core/`).
