# 21. Add a `design` skill category, starting with Material Design 3

- **Status:** accepted
- **Date:** 2026-10-25
- **Amends:** [0017](0017-add-qubes-os-skills.md), [0018](0018-skill-categories.md)

## Context

[0017](0017-add-qubes-os-skills.md) and [0020](0020-harness-categories-and-pi-skills.md)
established that this repository collects reusable Agent Skills organized into category
folders under `skills/<category>/<skill>/` ([0018](0018-skill-categories.md)), and that a
new topic area gets its own decision record.

The owner wants contiguous UX and developer experience across GUI tools in their projects
and submodules, built around [Material Design 3](https://m3.material.io/) and its
**Material 3 Expressive** evolution, and needs a reusable, project-independent skill
covering how the design system works, where its official source repositories live across
platforms, and how to adopt its tokens, styles, and components cleanly in existing
codebases.

## Decision

- Add a `skills/design/` category folder (following [0018](0018-skill-categories.md): no
  `SKILL.md` in the category folder, a human-facing `README.md`, and unique skill names
  across the repository).
- Add `skills/design/material-design-3/` covering Material Design 3 and M3 Expressive:
  - `SKILL.md`: the mental model, Standard M3 vs. M3 Expressive, upstream repository and
    package matrix, core pillars (3-tier tokens and HCT color roles, M3 Expressive motion
    physics, shape scale and morphing, 30-style typography, adaptive window size classes
    and components), and the step-by-step workflow for adopting M3 in existing projects.
  - `references/tokens-and-theming.md`: token tiers, HCT color math, all 48 semantic color
    roles and Light/Dark tone mappings, scheme variants, elevation, and state layers.
  - `references/expressive-style-system.md`: the 12-token spring physics matrix (stiffness,
    damping, CSS curves), 30-style baseline + emphasized type scale, 10-step corner shape
    scale, optical corner nesting, polygon morphing, and Material Symbols variable axes.
  - `references/components-and-layout.md`: window size classes, canonical layouts, all six
    component families including M3 Expressive additions (Button Groups, Split Button,
    Floating/Docked Toolbars, FAB Menu, Loading Indicator), and adaptations for desktop and
    creative studio GUIs.
  - `references/ecosystem-and-integration.md`: upstream repositories and maintenance status,
    `@material/material-color-utilities` token generation, sharing tokens across parent
    repositories and submodules, platform integration (Web, Compose, Flutter), and an
    audit checklist.
- Like the other non-methodology skills here, `material-design-3` is self-contained
  ([0010](0010-skills-self-contained.md)), MIT licensed ([0008](0008-mit-licence.md)), and
  grounded in primary sources (`m3.material.io`, `material-foundation/*`,
  `material-components/*`, and `androidx.compose.material3`).

## Consequences

- All design skills install together with
  `npx skills add r3b1s/secure-methodologies/skills/design`, or individually with
  `npx skills add r3b1s/secure-methodologies --skill material-design-3`.
- Further design-system or UI/UX skills can be added under `skills/design/` without a new
  category record as long as they stay within this scope.
