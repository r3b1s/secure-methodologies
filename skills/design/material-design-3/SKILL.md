---
name: material-design-3
description: Designing, theming, and building user interfaces with Material Design 3 (M3) and Material 3 Expressive (https://m3.material.io/) across Web, Desktop/Studio GUIs, Android (Jetpack Compose), and Flutter. Covers the three-tier token architecture (reference, system, component), HCT color space and dynamic tonal palettes, surface-container elevation, adaptive window size classes and canonical layouts, M3 Expressive spring physics (spatial vs. effects), the 30-style baseline + emphasized type scale, the 10-step corner shape scale and shape morphing, component selection (including M3 Expressive button groups, split buttons, floating toolbars, FAB menus, and loading indicators), official upstream repositories, and incremental adoption in existing projects. Use when starting a UI, migrating an existing project to Material Design 3, building custom components that conform to M3/M3 Expressive, or auditing a UI against M3 guidelines.
license: MIT
metadata:
  verified-on: "m3.material.io specifications (M3 & M3 Expressive), @material/material-color-utilities, @material/web, and androidx.compose.material3 (checked 2026-10)"
---

# Material Design 3 & M3 Expressive

Material Design 3 (**M3**, also known as *Material You*) and its **M3 Expressive** evolution are Google's adaptive, token-driven design system. M3 replaces hardcoded colors, drop-shadow elevation, and fixed easing curves with **HCT perceptual color palettes**, **tonal surface containers**, **three-tier design tokens**, **spring-based motion physics**, **dynamic shape morphing**, and **emphasized editorial typography**.

When upstream specifications or installed library versions disagree with this skill, upstream wins. Primary sources of truth:

- **Specification & Guidelines:** https://m3.material.io/
- **Color & HCT Algorithms (TypeScript, Dart, Java, C++, Swift):** https://github.com/material-foundation/material-color-utilities (`@material/material-color-utilities` on npm)
- **Material Symbols & Icons (Variable Fonts & SVGs):** https://github.com/google/material-design-icons
- **Web Components (Lit / Custom Elements):** https://github.com/material-components/material-web (`@material/web` on npm — *maintenance mode*; see §2)
- **Jetpack Compose (Reference M3 Expressive Implementation):** `androidx.compose.material3:material3` and `androidx.graphics:graphics-shapes` in https://github.com/androidx/androidx
- **Android Views (XML):** https://github.com/material-components/material-components-android
- **Flutter:** `flutter/material.dart` (`useMaterial3: true`) in https://github.com/flutter/flutter and community package `material_3_expressive` on pub.dev

---

## 1. How to Approach Material Design 3 (Mental Model)

Do not treat M3 as a monolithic widget library that requires rewriting your DOM or UI tree at once. M3 is a **layered system** adopted from the bottom up:

```
Layer 5: Components & Patterns   Buttons, Floating Toolbars, Cards, Dialogs, Sheets, Lists
Layer 4: Adaptive Layout         Window Size Classes, Canonical Panes, Navigation Switching
Layer 3: Expressive Style        Spring Physics (Spatial/Effects), Shape Morphing, Emphasized Type
Layer 2: Semantic System Tokens  Color Roles (--md-sys-color-*), Surface Containers, State Layers
Layer 1: Reference Foundations   HCT Tonal Palettes (0–100), Typefaces, Raw Shape & Spacing Scales
```

### Standard M3 vs. M3 Expressive
M3 Expressive is not a separate design system—it is an expansion of M3 backed by Google UX research showing that **strategic expressiveness improves usability** (users locate key actions up to 4× faster when focal controls use distinct shapes, sizes, and vibrant container tokens).

| Dimension | Standard M3 Baseline | M3 Expressive Expansion |
|---|---|---|
| **Best suited for** | Dense data tables, utilitarian forms, secondary settings, enterprise administration | Hero moments, primary toolbars, creative/media studio controls, onboarding, focal actions |
| **Motion** | Low-bounce (`Standard`) springs or cubic-bezier curves | Playful, responsive overshoot on `Spatial` springs; critically damped `Effects` springs |
| **Typography** | 15 baseline styles (`Display`, `Headline`, `Title`, `Body`, `Label` × `L/M/S`) | +15 `Emphasized` styles (30 total) with heavier weights and variable font axes |
| **Shape** | 7 corner tokens (`0dp` to `28dp` + `full`) | 10 corner tokens (adds `20dp`, `32dp`, `48dp`), 35 polygon shapes, and interactive corner morphing |
| **Components** | Core M3 set (Buttons, Cards, Navigation Bar/Rail/Drawer, Dialogs, etc.) | Adds **Button Groups**, **Split Button**, **Floating/Docked Toolbars**, **FAB Menu**, **Loading Indicator**, **Flexible Nav Bar**, **Expanded Nav Rail**, **Wavy Progress**, and 5 button sizes (`XS`–`XL`) |

**Rule of thumb:** Combine both within the same application. Use **M3 Expressive** for primary navigation, floating canvas/viewport toolbars, primary action clusters, and empty/loading states; use **Standard M3** for dense inspector panels, property grids, and text-heavy forms.

---

## 2. Official Repositories & Ecosystem Status

Choosing the right upstream package prevents adopting deprecated Material 2 code:

| Target Platform | Official Package / Repo | Status & Recommended Strategy |
|---|---|---|
| **Any Web Stack (Vanilla TS, Vite, React, Vue, Svelte, Three.js GUIs)** | `@material/material-color-utilities` + CSS Custom Properties (`--md-sys-*`) | **Active & Recommended Foundation.** Generate HCT tonal schemes at build time or runtime into CSS variables. Style native HTML elements, custom studio panels, or headless UI primitives (Radix, Aria, etc.) directly with M3 tokens. |
| **Web Components (Lit / HTML)** | `@material/web` (`material-components/material-web`) | **Maintenance Mode.** Google placed `@material/web` in maintenance mode. Safe to use for standard M3 controls (`<md-filled-button>`, `<md-dialog>`, `<md-slider>`, etc.), but M3 Expressive components (Floating Toolbars, Split Buttons, Button Groups) must be authored with CSS tokens. |
| **Legacy Web (M2)** | `material-components-web` / `@material/mwc-*` | **Archived / Deprecated.** Material Design 2. **Never use in new or M3 projects.** |
| **Android (Jetpack Compose)** | `androidx.compose.material3:material3` (`1.4.0+` / `1.5.0+`) | **Active Flagship.** First-class support for `MaterialExpressiveTheme`, `MotionScheme.expressive()`, `ButtonGroup`, `SplitButtonLayout`, `HorizontalFloatingToolbar`, `FloatingActionButtonMenu`, `LoadingIndicator`, and `MaterialShapes`. |
| **Flutter** | `flutter/material.dart` + `material_color_utilities` (+ `material_3_expressive`) | **Active.** M3 is Flutter's default (`useMaterial3: true`). Use `ColorScheme.fromSeed()` for HCT palettes; add `material_3_expressive` for expressive components and spring tokens. |
| **Icons (All Platforms)** | `Material Symbols` (`google/material-design-icons`) | **Active.** Use the **Material Symbols** variable font (`Outlined`, `Rounded`, or `Sharp`), *not* the legacy static "Material Icons" font. |

See [references/ecosystem-and-integration.md](references/ecosystem-and-integration.md) for package setup, Vite/TypeScript/React/Compose code templates, and migration steps.

---

## 3. Core Pillar 1: Design Tokens & HCT Color System

Never hardcode hex values in components. Every visual property flows through three token tiers:

1. **Reference tokens (`--md-ref-*`):** Raw palette tones and measurements (e.g., `md.ref.palette.primary40`, `md.ref.typeface.brand`). Never referenced directly by UI components.
2. **System tokens (`--md-sys-*`):** Semantic roles that adapt across Light/Dark themes, contrast levels, and form factors (e.g., `--md-sys-color-primary`, `--md-sys-color-surface-container-high`, `--md-sys-shape-corner-large`). **Use these for all custom layouts and studio panels.**
3. **Component tokens (`--md-comp-*`):** Scoped overrides for individual component anatomy (e.g., `--md-filled-button-container-shape`), mapped to system tokens by default.

### Color Roles & Paired "On" Colors
Every container or surface role has a paired `on-*` role with guaranteed perceptual contrast in HCT space:

- **Accent roles:**
  - `primary` / `on-primary` and `primary-container` / `on-primary-container` (high-emphasis focal actions, active states)
  - `secondary` / `on-secondary` and `secondary-container` / `on-secondary-container` (tonal buttons, filter chips, less prominent controls)
  - `tertiary` / `on-tertiary` and `tertiary-container` / `on-tertiary-container` (complementary accents, badges, editorial highlights)
  - `error` / `on-error` and `error-container` / `on-error-container` (destructive states, validation errors)
- **Tonal Surface Container Hierarchy (Replaces Opacity-Overlay Elevation):**
  Instead of stacking white/black alpha overlays or heavy drop shadows to show depth, M3 steps through five neutral surface container tokens:

  | Surface Role | Light Tone | Dark Tone | Typical Use |
  |---|---:|---:|---|
  | `surface-dim` | 87 | 6 | Dimmed backdrop or recessed canvas area |
  | `surface-container-lowest` | 100 | 4 | Deepest background / inset canvas / code or 3D viewport surround |
  | `surface` | 98 | 6 | Default page / window background |
  | `surface-container-low` | 96 | 10 | Subtle cards, sidebars, secondary groupings |
  | `surface-container` | 94 | 12 | Default cards, navigation rails/bars, dock panels |
  | `surface-container-high` | 92 | 17 | Floating toolbars, elevated cards, bottom/side sheets |
  | `surface-container-highest` | 90 | 22 | Dialogs, menus, popovers, tooltips, input field fills |
  | `surface-bright` | 98 | 24 | Highlighted or spotlighted surface |

- **Text, Icons, and Borders on Surfaces:**
  - `on-surface` (Light Tone 10 / Dark Tone 90): Primary text and active icons on any `surface*` role.
  - `on-surface-variant` (Light Tone 30 / Dark Tone 80): Secondary text, labels, inactive icons.
  - `outline` (Light Tone 50 / Dark Tone 60): 3:1 accessible borders (outlined text fields, unselected checkboxes).
  - `outline-variant` (Light Tone 80 / Dark Tone 30): Decorative dividers and subtle panel borders.
- **Fixed Roles (`primary-fixed`, `primary-fixed-dim`, `on-primary-fixed`, `on-primary-fixed-variant`):** Maintain identical tones in both Light and Dark mode (Tone 90/80/10/30) for branded elements or media overlays that should not invert.

See [references/tokens-and-theming.md](references/tokens-and-theming.md) for the complete 48-role tone table, scheme variants (`TonalSpot`, `Expressive`, `Vibrant`, `Neutral`, `Monochrome`, `Fidelity`), contrast levels, state layer opacities, and `@material/material-color-utilities` code.

---

## 4. Core Pillar 2: M3 Expressive Style System

### Motion Physics (Springs over Duration/Easing)
M3 Expressive replaces fixed-duration easing curves with a **2 × 2 × 3 spring physics matrix**:

- **2 Schemes:** `Expressive` (noticeable bounce on spatial movement; default for M3 Expressive) vs. `Standard` (minimal bounce; utilitarian UIs).
- **2 Property Types:**
  - **`Spatial` (`md.sys.motion.spring.<speed>.spatial`):** Animates **position, size, width/height, scale, rotation, and corner radius**. Allows natural physical overshoot (`damping < 1.0`).
  - **`Effects` (`md.sys.motion.spring.<speed>.effects`):** Animates **color, background, opacity, and box-shadow**. Always **critically damped (`damping = 1.0`)**—never bounce opacity or color, as values oscillating past `0` or `1` clip and flash.
- **3 Speeds:** `fast` (switches, icon buttons, press morphs), `default` (cards, toolbars, button groups, drawers), `slow` (full-screen sheets, page transitions).

| Token (`Expressive` Scheme) | Stiffness | Damping | Web CSS Approximation (`duration` + `cubic-bezier`) |
|---|---:|---:|---|
| `spring.fast.spatial` | `800` | `0.6` | `350ms cubic-bezier(0.42, 1.67, 0.21, 0.90)` |
| `spring.default.spatial` | `380` | `0.8` | `500ms cubic-bezier(0.38, 1.21, 0.22, 1.00)` |
| `spring.slow.spatial` | `200` | `0.8` | `650ms cubic-bezier(0.39, 1.29, 0.35, 0.98)` |
| `spring.fast.effects` | `3800` | `1.0` | `150ms cubic-bezier(0.31, 0.94, 0.34, 1.00)` |
| `spring.default.effects` | `1600` | `1.0` | `200ms cubic-bezier(0.34, 0.80, 0.34, 1.00)` |
| `spring.slow.effects` | `800` | `1.0` | `300ms cubic-bezier(0.34, 0.88, 0.34, 1.00)` |

### Shape Scale, Corner Nesting & Interactive Shape Morphing
The 10-step corner scale runs from sharp to pill:
`none (0px)` · `extra-small (4px)` · `small (8px)` · `medium (12px)` · `large (16px)` · `large-increased (20px)` · `extra-large (28px)` · `extra-large-increased (32px)` · `extra-extra-large (48px)` · `full (9999px)`.

- **Optical Corner Nesting:** When nesting a rounded child inside a rounded parent with padding $P$, prevent awkward corner pinches via:
  $$R_{\text{inner}} = \max(0, R_{\text{outer}} - P)$$
- **Interactive Shape Morphing (Signature M3 Expressive Technique):**
  Interactive controls morph their `border-radius` on press, selection, or menu expansion using `spring.fast.spatial`:
  - **Rest (Unselected):** Pill (`--md-sys-shape-corner-full`) or small rounded corners inside a connected group (`--md-sys-shape-corner-small`).
  - **Pressed / Active:** Morphs toward a squarer corner (`--md-sys-shape-corner-small` or `medium`) to give tactile "squish" feedback.
  - **Selected (Toggleable Button / Icon Button / Button Group item):** Holds a distinct corner shape (e.g., `medium` `12px` or `large` `16px` square-ish pill) paired with `primary` or `secondary-container` fill so selection is communicated by **both shape and color** (improving accessibility).

### Typography: 15 Baseline + 15 Emphasized Styles
5 semantic roles (`display`, `headline`, `title`, `body`, `label`) × 3 sizes (`large`, `medium`, `small`). M3 Expressive adds an **Emphasized** counterpart for each of the 15 styles (shifting weight from `400` $\rightarrow$ `500`/`600` or `500` $\rightarrow$ `700`) for active states, focal numerals, and editorial hierarchy.

See [references/expressive-style-system.md](references/expressive-style-system.md) for the complete 30-style typography table, all 12 spring tokens, variable font axes, and Material Symbols icon axes.

---

## 5. Core Pillar 3: Adaptive Layout & Component Selection

### Window Size Classes (Breakpoints)
Design for responsive window dimensions, never device types:

| Size Class | Width Range | Primary Navigation Pattern | Canonical Pane Count |
|---|---|---|---|
| **Compact** | `< 600px` | Bottom `Navigation Bar` or `Floating Toolbar` | 1 pane |
| **Medium** | `600px – 839px` | Side `Navigation Rail` | 1–2 panes (collapsible supporting pane) |
| **Expanded** | `840px – 1199px` | `Navigation Rail` or `Expanded Navigation Rail` | 2 panes (List-Detail or Primary + Inspector) |
| **Large** | `1200px – 1599px` | `Expanded Navigation Rail` or persistent `Navigation Drawer` | 2–3 panes (`24px` inter-pane gap) |
| **Extra-large** | `>= 1600px` | Persistent `Navigation Drawer` + contextual `Floating Toolbars` | 3+ panes (e.g., Outliner + Viewport + Inspector) |

### Key M3 Expressive Components to Prefer
- **Button Groups (`Standard` & `Connected`):** Group related actions or segmented view/tool modes. On press or selection, the active button expands slightly in width while adjacent neighbors compress, animated with `spring.fast.spatial`.
- **Split Button:** Combines a primary action (leading pill segment) with a dropdown chevron (trailing segment) separated by a `2px` gap. When the menu opens, the trailing button's outer corner morphs toward a symmetric circle/squircle.
- **Floating Toolbar & Docked Toolbar:** Replaces rigid full-width bottom app bars. Float a pill-shaped `surface-container-high` or `primary-container` (vibrant) toolbar (`16px` margin from viewport edge) over canvases, 3D viewports, timelines, or scrolling content.
- **FAB Menu:** Replaces legacy speed-dials. Clicking a FAB morphs it into a close button (`tertiary` or `primary`) and staggers 2–6 labeled pill action items upward using `spring.fast.spatial`.
- **Loading Indicator:** For indeterminate waits under **5 seconds**, use the M3 Expressive shape-morphing polygon indicator instead of a plain circular spinner. Use `Linear` or `Circular` Progress Indicators (flat or wavy track) when progress is determinate or exceeds 5 seconds.

See [references/components-and-layout.md](references/components-and-layout.md) for the complete component decision matrix, anatomy specs, and patterns for desktop/creative GUI tools.

---

## 6. Integrating M3 into an Existing Project (Step-by-Step Workflow)

When introducing Material Design 3 into an existing codebase (or unifying UX/DX across a repository and its submodules):

1. **Establish the Shared Token Contract First (Zero Visual Breakage):**
   - Choose a primary seed color (and optional secondary/tertiary brand overrides) and a default scheme variant (`TonalSpot` for balanced tools, `Expressive` or `Vibrant` for creative apps, `Neutral` for color-critical media/3D viewports where UI chrome must not cast color bias onto the canvas).
   - Generate `--md-sys-color-*`, `--md-sys-typescale-*`, `--md-sys-shape-*`, and `--md-sys-motion-*` tokens into a shared CSS stylesheet or TS module.
2. **Migrate Backgrounds and Containment to Surface Containers:**
   - Replace ad-hoc background grays, semi-transparent borders, and drop shadows with the stepped surface hierarchy: `surface-container-lowest` (viewport/canvas recess) $\rightarrow$ `surface` (window) $\rightarrow$ `surface-container` (panels/sidebars) $\rightarrow$ `surface-container-high` (floating toolbars/inspector cards) $\rightarrow$ `surface-container-highest` (dialogs/menus).
3. **Adopt State Layers and Focus Rings:**
   - Replace custom `:hover` and `:active` color darkening/lightening with M3 state layers (`8%` hover, `10%` focus, `10%` press, `16%` drag of the `on-*` color token) and a `2px`/`3px` `--md-sys-color-secondary` or `primary` focus ring (`outline-offset: 2px`).
4. **Upgrade Focal Controls to M3 Expressive:**
   - Convert primary action clusters to **Filled / Tonal Buttons**, **Split Buttons**, **Connected Button Groups**, and **Floating Toolbars** with `spring.fast.spatial` corner morphing and `spring.fast.effects` color transitions.
5. **Verify Against the M3 Audit Checklist:**
   - Check contrast (all text uses paired `on-*` roles; minimum `4.5:1` for body text, `3:1` for large text and active UI boundaries).
   - Check motion separation (`spatial` springs never animate `opacity` or `background-color`; `prefers-reduced-motion: reduce` collapses spatial springs to instant/fade transitions).
   - Check component restraint (at most **one** `Filled` primary button or primary `FAB` per pane/group; never mix `Filled` and `Outlined` text fields in the same form).

---

## Reference Guides in This Skill

Load these files on demand when working on a specific layer:

- **[references/tokens-and-theming.md](references/tokens-and-theming.md)** — 3-tier token architecture, HCT color space, complete 48-role Light/Dark tone table, scheme variants, elevation, state layers, and `@material/material-color-utilities` generation.
- **[references/expressive-style-system.md](references/expressive-style-system.md)** — Full 12-token spring physics table (stiffness, damping, CSS curves), 30-style baseline + emphasized typography specs, 10-step shape scale, corner nesting math, shape morphing states, and Material Symbols variable icon axes.
- **[references/components-and-layout.md](references/components-and-layout.md)** — Window size classes, canonical layouts, all 6 component families, M3 Expressive components (Button Groups, Split Button, Floating Toolbars, FAB Menu, Loading Indicator), and desktop/studio GUI patterns (dark-mode viewports, density scales, property inspectors).
- **[references/ecosystem-and-integration.md](references/ecosystem-and-integration.md)** — Official GitHub repositories, npm/Gradle/Pub packages, multi-repo/submodule token sharing, framework integration patterns (Vanilla TS/Vite, Web Components, React/Vue, Compose, Flutter), and anti-pattern checklist.
