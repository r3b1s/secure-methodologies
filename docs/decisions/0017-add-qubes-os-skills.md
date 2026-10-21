# 17. Widen the scope to include Qubes OS skills

- **Status:** accepted
- **Date:** 2026-10-21
- **Amends:** [0002](0002-scope-of-initial-version.md)
- **Amended by:** [0019](0019-add-qubes-admin-python-skill.md) (qubesadmin Python skill)

## Context

[0002](0002-scope-of-initial-version.md) scoped this repository to one methodology: making
a software repository safe to publish and easy to trust. It requires a new record to widen
that scope. The owner uses this repository to collect agent skills about working securely,
and has three skills for [Qubes OS](https://www.qubes-os.org/), an operating system built
around isolating work in separate virtual machines. They cover which command-line tools run
in dom0 and which inside other qubes, and how to build disposable qubes so that
configuration and secrets persist only where intended. The skills were first written in
the owner's Qubes OS dotfiles repository.

## Decision

- The repository also holds Qubes OS skills: `qubes-dom0-cli`, `qubes-vm-cli` and
  `qubes-disposable-vms`, in the `qubes-os` category (see
  [0018](0018-skill-categories.md)).
- The scope in the README applies to the `secure-repo` methodology. The Qubes OS skills
  have their own scope: using Qubes OS and building its qubes correctly. They are not part
  of the repository methodology, and it does not depend on them.
- The Qubes OS skills follow the same rules as every skill here: self-contained
  ([0010](0010-skills-self-contained.md)), MIT licensed
  ([0008](0008-mit-licence.md)), and grounded in primary sources: upstream Qubes OS
  documentation and the installed tools, with the release they were checked against
  stated in each skill.

## Consequences

- The README describes the repository as a collection of skills, with the repository
  methodology as one part of it.
- Further topics need their own record before they are added.
- The Qubes OS skills track Qubes OS releases rather than the OSPS Baseline, so their
  release checks happen on a different schedule.
