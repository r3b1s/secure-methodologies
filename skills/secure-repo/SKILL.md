---
name: secure-repo
description: Make a software repository safe to publish and easy to trust, using the OpenSSF OSPS Baseline (v2026.08.28) as the requirements. Use when auditing a repository before making it public, starting a new project, maintaining or releasing one, or re-auditing it, and when choosing which Baseline maturity level a project should meet.
license: MIT
metadata:
  baseline-version: "v2026.08.28"
---

# Secure a repository

## Scope

This skill helps a person, an agent, or both make a software repository safe to publish
and easy to trust, at any of these stages: auditing it before it goes public, starting a
new project, ongoing maintenance, releases, and periodic re-audits.

- **Requirements:** the OpenSSF OSPS Baseline, the version in
  [references/baseline.md](references/baseline.md), including its legal controls. Where the
  Baseline is silent or gives no method, this skill fills the gap and says so.
- **Goals, in priority order:** signals that let strangers trust the project; software
  that does not harm the people who use it; nothing private leaking when it is published.
- **Also covered:** code quality where it affects security or trust, and the threat model
  a project adopts: the risks a person accepts by installing, deploying or running it.
- **Effort scales with risk.** A small personal tool needs less than a widely used or
  privileged one.
- **Neutral by default.** The core does not depend on a language, a tool or a git forge.
  Stack and platform guidance is offered as suggestions, never imposed.
- **Not covered:** legal advice beyond the Baseline's legal controls, privacy-regulation
  compliance, and archiving a project. Repositories with no software in them are mostly
  out of scope, unless they contain something that is itself run.

## How to use this skill

1. **Read the ground rules below.** They apply to every step.
2. **Find or start the project record.** It holds the project's target version, level,
   constraints, standing permissions and results; see
   [references/project-record.md](references/project-record.md).
3. **Choose a maturity level** with the human; see [Choose a maturity level](#choose-a-maturity-level).
4. **Pick the stage** the project is at, and follow its guide; see
   [Choose the stage](#choose-the-stage). Stage guides link to the requirement files and
   references they need; read those only when a step calls for them.
5. **Report** as ground rule 7 describes, and update the project record once the human
   approves.

## Ground rules for agents

These rules apply whenever an agent carries out any part of this skill. A person following
the skill alone can read them as the standard the work is held to.

1. **The human decides; you propose.** For each decision below, research it, set out the
   options with their tradeoffs, recommend one if you can, then stop and wait:
   - tools, dependencies, pinned versions, and the structure of CI/CD pipelines
   - the maturity level the project targets
   - accepting a risk, or marking a control as not applicable
   - changing how the software behaves
   - anything outward-facing or hard to reverse: publishing, pushing, changing repository
     or platform settings, rewriting history, deleting

   Do not treat an earlier approval as covering a later, different decision.
2. **Change nothing without approval.** By default, propose every change, however small or
   obvious, and make it only once the human approves. A project may grant standing
   permission for some kinds of change; that permission counts only if it is written down
   with the project's constraints (rule 6), and it covers only what it names.
3. **Code is the source of truth.** Treat documents that describe the project (README,
   design documents, threat models, code comments) as claims to check against the code,
   never the reverse. This does not apply to files that give instructions to agents, such
   as `AGENTS.md` or skill files.
4. **Use tools for breadth and reading for depth.** Deterministic tools that cover the
   whole codebase find candidates that reading misses; reading confirms them and finds what
   tools cannot. Neither is enough alone. A clean tool run is not evidence that the code is
   secure.
5. **Do not state facts from memory.** Facts about tools, frameworks and standards come
   from primary sources, cited, with the date you checked them. Mark anything you could not
   verify as unverified. Claim no conformance to a framework that has not been checked
   control by control.
6. **Respect the project's constraints.** Work within the constraints the project has
   recorded (what its CI can run, which tools are acceptable). If none are recorded,
   establish them with the human before you start.
7. **Report faithfully.** Keep three things separate: what changed, what ran and passed
   (with the commands, so anyone can reproduce it), and what was not checked or could not
   be verified. Give every control or finding a status: met (and how you know), not met,
   not applicable (and why), or not checked.

## Choose a maturity level

The Baseline has three cumulative levels, set by how many maintainers and users a project
has. Propose a level from the facts, adjusted for what the software can do, and let the
human decide; see [references/levels.md](references/levels.md). Each level's requirements
are in `references/osps/level1/`, `level2/` and `level3/`, by the level where each first
applies.

## Choose the stage

| Stage | Guide |
|---|---|
| Audit before making a repository public | [references/stages/pre-publication-audit.md](references/stages/pre-publication-audit.md) |
| Start a new project | [references/stages/new-project.md](references/stages/new-project.md) |
| Ongoing maintenance | [references/stages/maintenance.md](references/stages/maintenance.md) |
| Release and distribute | [references/stages/release.md](references/stages/release.md) |
| Periodic re-audit | [references/stages/re-audit.md](references/stages/re-audit.md) |

## Reference

- [references/project-record.md](references/project-record.md): what to record about a
  project, and where.
- [references/baseline.md](references/baseline.md): the Baseline version targeted, its
  levels and categories, and where this skill fills its gaps.
- [references/baseline-upgrade.md](references/baseline-upgrade.md): read only when a
  project meets an older Baseline version and the user wants it audited against, or moved
  to, a newer one.
- [references/osps/](references/osps/): how to meet and verify each Baseline
  requirement, one file per requirement named by its ID, in a folder for the level where it
  first applies ([level1/](references/osps/level1/), [level2/](references/osps/level2/),
  [level3/](references/osps/level3/)). Levels are cumulative: a level 2 project needs
  `level1/` and `level2/`. Open only the requirement files a task needs. A single requirement can be read on its own.
- [references/threat-modeling.md](references/threat-modeling.md): threat modelling and the
  risks of using the project.
- [references/tools/categories.md](references/tools/categories.md): tool categories,
  independent of language. Stack-specific suggestions are in
  [references/tools/stacks/](references/tools/stacks/); for a stack with no file there,
  read [references/tools/stacks/stack-research.md](references/tools/stacks/stack-research.md).
- [references/security-insights.md](references/security-insights.md): read only when the
  user wants to create a Security Insights file.
- [assets/SECURITY.md.template](assets/SECURITY.md.template): a simple vulnerability
  disclosure policy to start a project's `SECURITY.md` from.
- [references/platforms/github.md](references/platforms/github.md): GitHub-specific steps,
  including tools to offer (never require) on GitHub-hosted repositories.
