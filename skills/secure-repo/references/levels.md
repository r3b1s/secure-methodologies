# Choosing a maturity level

The level is the human's decision (ground rule 1). Gather the facts below, propose a level
with your reasons, and record the decision in the [project record](project-record.md).

## The Baseline's levels

The levels are cumulative and are defined by the project's people and audience, not by
what the software does (wording from the Baseline, summarised):

| Level | For | Requirements to meet |
|---|---|---|
| 1 | any project, whatever its number of maintainers or users | 24 |
| 2 | code projects with at least two maintainers and a small number of consistent users | 43 |
| 3 | code projects with a large number of consistent users | 64 |

Each requirement's guidance is in the folder for the level where it first applies:
[osps/level1/](osps/level1/), [osps/level2/](osps/level2/), [osps/level3/](osps/level3/).
A project at a given level needs that folder and every folder below it.

To propose a level, establish:

- how many people maintain the project (can merge, release or change settings)
- roughly how many people use it, and whether that use is steady
- whether it has released anything yet (many requirements apply only after a release)

## Adjusting for risk

The Baseline's levels ignore what the software can do. Two projects at level 1 can carry
very different risk. Before proposing, establish:

- **Privilege:** does it run as root or an administrator, install system components,
  change system trust, or ask for elevated rights?
- **Exposure:** does it listen on a network, handle input from untrusted parties, or
  process files from elsewhere?
- **Reach:** what can it read, change or delete, and whose data does it handle?
- **Distribution:** is it installed by others through a package registry, an installer or
  an image, or only built from source?

Risk changes the work in two ways; propose either, and let the human choose:

1. **More scrutiny at the same level.** For example, read privileged code in full and
   run more tool categories during an audit. This does not change the level claimed.
2. **Meet chosen requirements from a higher level.** For example, a level 1 project that
   distributes packages might also meet automatic checks for known-vulnerable
   dependencies ([OSPS-VM-05.03](osps/level3/OSPS-VM-05.03.md), level 3). Record these as
   "level 1 plus" with the chosen requirement IDs, not as a higher level. Each requirement
   is a single file, so only the chosen ones need reading.

## Projects the levels do not fit

Level 2 requires at least two maintainers. A project with one maintainer and steady users
cannot claim level 2, however mature it is. Propose level 1 plus the higher-level
requirements that fit, and record the reason in the project record.

## When to move up a level

Suggest a review of the level when the facts above change: a second maintainer joins, use
grows or becomes steady, the first release is made, or the software gains privilege or
network exposure. Moving up is the human's decision and starts a
[re-audit](stages/re-audit.md).
