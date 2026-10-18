# secure-methodologies

Guidance for making a software repository safe to publish and easy to trust, written so
that a person, an LLM agent, or both together can follow it through most of a project's
life.

## Scope

**Purpose.** This repository is context: guidance a person or an agent follows to make a
repository safe to publish and easy to trust. Checklists, templates, reports and other
artifacts are produced from that context and are secondary to it.

**Audience.** Anyone who wants to adopt it. It assumes no knowledge of its author or of any
particular project.

**Who carries it out.** People and agents, on equal footing. Every part must work when read
by a person alone. Where an agent carries it out, the points that need a human decision are
marked.

**Applies to.** Any repository containing software: code that is built, run, deployed or
distributed. Repositories without such code (for example, documentation only) are mostly
out of scope, unless they include something that is itself run, such as a platform that
hosts the documentation. Where the line is unclear, the guidance says how to decide
whether, and how much, it applies.

**Languages and tools.** The core is language-neutral and names categories of practice and
tooling, not products. Guidance for specific stacks is added as stacks are encountered. It
is offered as suggestions and never imposed. Where no guidance exists for a stack, the
repository explains how to research one safely and reliably.

**Platforms.** The core does not depend on any one git forge. GitHub is the only platform
covered concretely for now. Platform-specific guidance is kept apart from the core.

**Stages of a project's life covered:**

- auditing an existing repository before making it public
- starting a new project
- ongoing maintenance
- releases and distribution
- periodic re-audits

**Goals, in priority order:**

1. signals that let strangers trust the project
2. the code not harming the people who use it
3. nothing private leaking when it is published

**Effort scales with risk.** A small personal tool needs less scrutiny than a widely used or
privileged one. A project's level can rise as adoption grows.

**Constraints are decided per project.** Each project records its own limits, for example
what its CI can and cannot run, or which tools are acceptable. The guidance does not assume
one environment.

**In scope:**

- security
- code quality, where it affects security or trust
- the threat model a project adopts, and the risks a person accepts by using the software
  (installing, deploying or running it), including whether those risks are reasonable
- the legal controls of the OSPS Baseline (see below)

**Out of scope for this version:** licensing and legal questions beyond the Baseline's
legal controls, compliance with privacy regulation, and archiving a project.

## Foundation

The requirements come from the
[OpenSSF Open Source Project Security Baseline](https://baseline.openssf.org/) (OSPS
Baseline), version **v2026.08.28**. The Baseline defines *what* a project should meet at
each maturity level. This repository supplies *how*: the process to follow at each stage, a
catalog of tool categories, and guidance for filling the Baseline's gaps. See
[the Baseline reference](skills/secure-repo/references/baseline.md) and
[the decision records](docs/decisions/).

## Contents

| Path | What it is |
|---|---|
| [skills/secure-repo/](skills/secure-repo/) | The methodology, packaged as an [Agent Skill](https://agentskills.io/). This is the canonical content, for people and agents alike. |
| [docs/glossary.md](docs/glossary.md) | Terms as this repository uses them, with their sources. |
| [docs/decisions/](docs/decisions/) | Decision records: what was decided, when and why. |
| [docs/research/](docs/research/) | Dated research behind the decisions. |

## Using it as a person

Start with [skills/secure-repo/SKILL.md](skills/secure-repo/SKILL.md): its scope, the
route through the material, and the ground rules the work is held to. Then open the
stage guide for where your project is (for example the pre-publication audit), and follow
its links to the guidance for each Baseline requirement as you need it.

## Using it as an agent

The skill follows the [Agent Skills](https://agentskills.io/specification) format and
is found by the [`skills` CLI](https://github.com/vercel-labs/skills) in the top-level
`skills/` folder. To install it:

```sh
npx skills add r3b1s/secure-methodologies --skill secure-repo
```

Add `-g` to install for your user rather than the current project, or `--list` to see the
available skills first. The skill is self-contained: it needs nothing else from this
repository.

## Licence

[MIT](LICENSE).
