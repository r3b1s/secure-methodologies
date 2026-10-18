# Start a new project

## When this applies

A new repository, before or soon after its first commit. Meeting requirements from the
start is far cheaper than retrofitting them.

## Before you start

- Start the [project record](../project-record.md), including constraints such as what CI
  will be able to run.
- Agree a level with the human ([levels.md](../levels.md)). Most new projects start at
  level 1; consider which higher-level requirements are worth meeting from day one.

## Steps

Propose each item; set it up only with approval. Links go to the guidance for each
requirement.

1. **Licence and legal.** A licence the human chooses, in a well-known location
   ([OSPS-LE-02.01](../osps/level1/OSPS-LE-02.01.md), [OSPS-LE-03.01](../osps/level1/OSPS-LE-03.01.md)). At level 2, a contributor assertion mechanism
   ([OSPS-LE-01.01](../osps/level2/OSPS-LE-01.01.md)).
2. **Repository protection.** MFA for maintainers, lowest default permissions for
   collaborators, and a primary branch that cannot be pushed to directly or deleted
   ([OSPS-AC-01.01](../osps/level1/OSPS-AC-01.01.md), [OSPS-AC-02.01](../osps/level1/OSPS-AC-02.01.md), [OSPS-AC-03.01](../osps/level1/OSPS-AC-03.01.md), [OSPS-AC-03.02](../osps/level1/OSPS-AC-03.02.md)).
3. **Keeping secrets out.** Ignore rules and automated secret detection before commits
   land ([OSPS-BR-07.01](../osps/level1/OSPS-BR-07.01.md)).
4. **Dependencies.** A manifest, and a lock file where the ecosystem supports one
   ([OSPS-QA-02.01](../osps/level1/OSPS-QA-02.01.md),
   [OSPS-BR-05.01](../osps/level2/OSPS-BR-05.01.md)). Offer pinning and
   checks for known-vulnerable dependencies (gaps in [baseline.md](../baseline.md#gaps-this-skill-fills)).
5. **No binaries.** Ignore rules for build outputs
   ([OSPS-QA-05.01](../osps/level1/OSPS-QA-05.01.md), [OSPS-QA-05.02](../osps/level1/OSPS-QA-05.02.md)).
6. **Pipelines, if any.** Read-only default permissions, permissions granted per job,
   untrusted input never interpolated into scripts, untrusted code kept away from secrets
   ([OSPS-AC-04.01](../osps/level2/OSPS-AC-04.01.md), [OSPS-AC-04.02](../osps/level3/OSPS-AC-04.02.md),
   [OSPS-BR-01.01](../osps/level1/OSPS-BR-01.01.md), [OSPS-BR-01.03](../osps/level1/OSPS-BR-01.03.md), [OSPS-BR-01.04](../osps/level3/OSPS-BR-01.04.md)).
   At level 2, tests run on every change and required checks must pass
   ([OSPS-QA-06.01](../osps/level2/OSPS-QA-06.01.md),
   [OSPS-QA-03.01](../osps/level2/OSPS-QA-03.01.md)).
7. **Community and reporting.** A public discussion channel, a contribution guide (or a
   statement that contributions are not accepted), and security contacts
   ([OSPS-GV-02.01](../osps/level1/OSPS-GV-02.01.md),
   [OSPS-GV-03.01](../osps/level1/OSPS-GV-03.01.md),
   [OSPS-VM-02.01](../osps/level1/OSPS-VM-02.01.md)); the
   [SECURITY.md template](../../assets/SECURITY.md.template) covers contacts and reporting. At level 2, a disclosure
   policy and private reporting ([OSPS-VM-01.01](../osps/level2/OSPS-VM-01.01.md), [OSPS-VM-03.01](../osps/level2/OSPS-VM-03.01.md)).
8. **An early threat sketch.** A short model of what the software will do and where its
   trust boundaries are ([threat-modeling.md](../threat-modeling.md)), so design choices
   such as secure defaults are made deliberately.
9. **Signals.** Offer a [Security Insights file](../security-insights.md) once the basics
   exist, and on GitHub the [tools to offer](../platforms/github.md#tools-to-offer).

## Human decision points

- the level; the licence; contributor terms
- every tool, dependency and pipeline structure
- platform settings

## Done when

Every requirement at the level that applies before a release is met or has an agreed
plan, and the project record says so. The rest is picked up at the first
[release](release.md).
