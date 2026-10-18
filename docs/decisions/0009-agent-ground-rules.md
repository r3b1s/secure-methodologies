# 9. Ground rules for agents

- **Status:** accepted
- **Date:** 2026-10-18

## Context

The skill is carried out by people, agents, or both (see
[0002](0002-scope-of-initial-version.md)). An earlier draft of this repository came from an
agent that audited and changed a project, chose its toolchain and wrote a method, all
without the owner's approval. The ground rules set the standard an agent's work is held to,
so that does not happen again.

## Decision

The `secure-repo` skill opens with seven ground rules (see "Ground rules for agents" in
[SKILL.md](../../skills/secure-repo/SKILL.md)):

1. The human decides; the agent proposes options and stops. Reserved decisions: tools,
   dependencies, pinned versions and pipeline structure; the target maturity level;
   accepting a risk or marking a control not applicable; changing behaviour; anything
   outward-facing or hard to reverse.
2. Change nothing without approval. A project may grant standing permission for named
   kinds of change, recorded with its constraints.
3. Code is the source of truth for documents that describe the project. This does not
   cover files that instruct agents, such as `AGENTS.md` or skill files.
4. Use tools for breadth and reading for depth; a clean tool run is not proof of security.
5. No facts from memory: cite primary sources with dates, mark what is unverified, claim
   no unchecked conformance.
6. Respect the project's recorded constraints, or establish them first.
7. Report faithfully: what changed, what ran and passed (with commands), and what was not
   checked, with a status for every control or finding.

Considered and rejected:

- **Treat what you read as data, not instructions.** Rejected: an agent might then ignore
  legitimate instruction files such as `AGENTS.md` or other skills. Rule 3 was narrowed
  for the same reason.
- **Never copy a secret; report its location only.** Removed for now.
- **Require approval before running the target project's own code** (build, tests,
  install). Rejected: most agent harnesses already control this.
- For rule 2, two looser alternatives: allowing changes that do not alter behaviour, or
  allowing clear defect fixes reported afterwards. Rejected in favour of approval by
  default with recorded, per-project permission.

## Consequences

- An agent following the skill asks more often; projects that want less friction record
  standing permissions explicitly.
- The rejected rules can be revisited with a new record if a need appears.
