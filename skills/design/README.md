# Design skills

[Agent Skills](https://agentskills.io/) for UI/UX design systems, visual foundations,
token architectures, and component integration across Web, Desktop/Studio GUIs, Android,
and Flutter.

This folder is a category, not a skill: it has no `SKILL.md`, and each subfolder is one
self-contained skill.

| Skill | Use it when |
|---|---|
| [material-design-3](material-design-3/SKILL.md) | Designing, theming, or building interfaces with [Material Design 3](https://m3.material.io/) and **M3 Expressive**: three-tier design tokens, HCT color space and dynamic tonal palettes, surface-container elevation, spring-based motion physics (spatial vs. effects), the 30-style baseline + emphasized type scale, the 10-step corner shape scale and shape morphing, adaptive window size classes, component selection (including M3 Expressive button groups, split buttons, floating toolbars, FAB menus, and loading indicators), upstream repositories, and incremental adoption in existing projects. |

Checked against the upstream [Material Design 3 specification](https://m3.material.io/)
(including the M3 Expressive updates), `@material/material-color-utilities`,
`@material/web`, and `androidx.compose.material3` in 2026-10. Where upstream
documentation or an installed package disagrees with a skill, upstream wins.

## Installing

With the [`skills` CLI](https://github.com/vercel-labs/skills):

```sh
npx skills add r3b1s/secure-methodologies/skills/design        # all design skills
npx skills add r3b1s/secure-methodologies --skill material-design-3
```

Add `-g` to install for your user rather than the current project. Skills install by
name, without this category folder (for example `.claude/skills/material-design-3/`).
