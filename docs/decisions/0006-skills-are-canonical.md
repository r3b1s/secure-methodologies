# 6. Skills hold the canonical content

- **Status:** accepted
- **Date:** 2026-10-18
- **Amended by:** [0010](0010-skills-self-contained.md)

## Context

Agent guidance is to be packaged as [Agent Skills](https://agentskills.io/specification),
installable with [`npx skills`](https://github.com/vercel-labs/skills). That CLI finds
skills in a top-level `skills/` folder and installs each skill folder on its own, and the
specification expects a skill to reference files relative to its own root. So content an
agent needs must be inside the skill or fetched from elsewhere. Three options were
considered: docs canonical with thin skills that fetch by URL; skills canonical; docs
canonical, copied into skills by a script.

## Decision

The methodology lives inside the skills (`skills/<name>/SKILL.md` and `references/`). The
README indexes it for people. Nothing is placed under agent-specific folders such as
`.claude/`.

## Consequences

- One copy of the content; it works offline once installed; people and agents read the
  same text.
- The skill format shapes the layout: `SKILL.md` stays short (the specification recommends
  under 500 lines) and detail goes in `references/`.
- Files inside a skill must not link outside it. Material that is not needed at run time
  (decision records, research) stays in `docs/`.
