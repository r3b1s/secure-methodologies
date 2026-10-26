# M3 Expressive Style System: Motion Physics, Typography, Shape & Icons

This reference provides the exact specification tables and implementation rules for the four stylistic pillars of Material Design 3 and **M3 Expressive**: spring-based motion physics, the 30-style baseline + emphasized type scale, the 10-step shape scale and polygon morphing system, and Material Symbols variable icons.

---

## 1. M3 Expressive Motion Physics (Spring System)

M3 Expressive replaces fixed duration-and-bezier transitions with a **spring physics model** defined by **stiffness** and **damping ratio ($\zeta$)**. Springs respond naturally to interruption, velocity changes, and mid-flight redirection.

### The Golden Rule: Spatial vs. Effects Springs
Every animated property belongs to one of two categories:

1. **`Spatial` Springs (`--md-sys-motion-spring-<speed>-spatial`):**
   - **Properties:** `transform` (`translate`, `scale`, `rotate`), `width`, `height`, `top`/`left`/`inset`, `padding`, `margin`, `gap`, `border-radius`, SVG path morphing.
   - **Behavior:** Under-damped ($\zeta < 1.0$). Produces a subtle physical overshoot/bounce in the `Expressive` scheme and near-critical damping ($\zeta = 0.9$) in the `Standard` scheme.
2. **`Effects` Springs (`--md-sys-motion-spring-<speed>-effects`):**
   - **Properties:** `opacity`, `background-color`, `color`, `border-color`, `fill`, `stroke`, `box-shadow`, `filter`.
   - **Behavior:** **Critically damped ($\zeta = 1.0$).** Never use a `spatial` spring on opacity or color—overshooting `1.0` or `0.0` causes hard clamping, premature flashes, or inverted color artifacts.

### Complete 12-Token Spring Specification Table

| Scheme | Speed | Type | Token (`md.sys.motion.spring.*`) | Stiffness | Damping ($\zeta$) | Approx. Duration | CSS `cubic-bezier()` Equivalent | Typical Use |
|---|---|---|---|---:|---:|---:|---|---|
| **Expressive** | **Fast** | **Spatial** | `expressive.fast.spatial` | `800` | `0.6` | `350ms` | `cubic-bezier(0.42, 1.67, 0.21, 0.90)` | Button press corner morph, switch thumb, icon toggle, tooltip pop, FAB menu items |
| **Expressive** | **Default** | **Spatial** | `expressive.default.spatial` | `380` | `0.8` | `500ms` | `cubic-bezier(0.38, 1.21, 0.22, 1.00)` | Connected button group width flex, card expansion, navigation drawer/rail toggle, floating toolbar entrance |
| **Expressive** | **Slow** | **Spatial** | `expressive.slow.spatial` | `200` | `0.8` | `650ms` | `cubic-bezier(0.39, 1.29, 0.35, 0.98)` | Full-screen dialog/sheet transition, hero carousel layout shift |
| **Expressive** | **Fast** | **Effects** | `expressive.fast.effects` | `3800` | `1.0` | `150ms` | `cubic-bezier(0.31, 0.94, 0.34, 1.00)` | Hover/press state layer fade, button color shift, ripple opacity |
| **Expressive** | **Default** | **Effects** | `expressive.default.effects` | `1600` | `1.0` | `200ms` | `cubic-bezier(0.34, 0.80, 0.34, 1.00)` | Container color crossfade, dialog scrim fade-in |
| **Expressive** | **Slow** | **Effects** | `expressive.slow.effects` | `800` | `1.0` | `300ms` | `cubic-bezier(0.34, 0.88, 0.34, 1.00)` | Ambient theme switch, full-page crossfade |
| **Standard** | **Fast** | **Spatial** | `standard.fast.spatial` | `1400` | `0.9` | `350ms` | `cubic-bezier(0.27, 1.06, 0.18, 1.00)` | Utilitarian toggles, dense inspector controls |
| **Standard** | **Default** | **Spatial** | `standard.default.spatial` | `700` | `0.9` | `500ms` | `cubic-bezier(0.27, 1.06, 0.18, 1.00)` | Standard panel resize, accordion collapse/expand |
| **Standard** | **Slow** | **Spatial** | `standard.slow.spatial` | `300` | `0.9` | `750ms` | `cubic-bezier(0.27, 1.06, 0.18, 1.00)` | Large layout pane transitions |
| **Standard** | **Fast** | **Effects** | `standard.fast.effects` | `3800` | `1.0` | `150ms` | `cubic-bezier(0.31, 0.94, 0.34, 1.00)` | Micro-interaction color/opacity fades |
| **Standard** | **Default** | **Effects** | `standard.default.effects` | `1600` | `1.0` | `200ms` | `cubic-bezier(0.34, 0.80, 0.34, 1.00)` | Standard fade transitions |
| **Standard** | **Slow** | **Effects** | `standard.slow.effects` | `800` | `1.0` | `300ms` | `cubic-bezier(0.34, 0.88, 0.34, 1.00)` | Large container opacity changes |

### Combining Spatial and Effects Transitions in CSS
Always split `transition` declarations so spatial properties use the spatial curve and color/opacity properties use the effects curve:

```css
:root {
  --md-sys-motion-expressive-fast-spatial: 350ms cubic-bezier(0.42, 1.67, 0.21, 0.90);
  --md-sys-motion-expressive-default-spatial: 500ms cubic-bezier(0.38, 1.21, 0.22, 1.00);
  --md-sys-motion-expressive-fast-effects: 150ms cubic-bezier(0.31, 0.94, 0.34, 1.00);
}

.m3e-interactive-control {
  transition:
    border-radius var(--md-sys-motion-expressive-fast-spatial),
    transform var(--md-sys-motion-expressive-fast-spatial),
    flex-grow var(--md-sys-motion-expressive-default-spatial),
    background-color var(--md-sys-motion-expressive-fast-effects),
    color var(--md-sys-motion-expressive-fast-effects);
}

@media (prefers-reduced-motion: reduce) {
  .m3e-interactive-control {
    transition:
      background-color 150ms linear,
      color 150ms linear;
  }
}
```

### Legacy M3 Easing & Duration Tokens (Fallback Reference)
When interfacing with older M3 codebases:
- **Emphasized:** `cubic-bezier(0.2, 0.0, 0, 1.0)` (decelerate: `cubic-bezier(0.05, 0.7, 0.1, 1.0)`, accelerate: `cubic-bezier(0.3, 0.0, 0.8, 0.15)`)
- **Standard:** `cubic-bezier(0.2, 0.0, 0, 1.0)` (decelerate: `cubic-bezier(0, 0, 0, 1)`, accelerate: `cubic-bezier(0.3, 0, 1, 1)`)
- **Durations:** `short1` (`50ms`), `short2` (`100ms`), `short3` (`150ms`), `short4` (`200ms`), `medium1` (`250ms`), `medium2` (`300ms`), `medium3` (`350ms`), `medium4` (`400ms`), `long1` (`450ms`), `long2` (`500ms`), `long3` (`550ms`), `long4` (`600ms`).

---

## 2. Typography: 15 Baseline + 15 M3 Expressive Emphasized Styles

M3 organizes typography into two font family tokens:
- `--md-ref-typeface-brand`: Used for `Display`, `Headline`, and `Title` roles (can be an expressive variable font such as *Roboto Flex*, *Plus Jakarta Sans*, *Inter*, or a custom brand display font).
- `--md-ref-typeface-plain`: Used for `Body` and `Label` roles (optimized for high legibility at small sizes, e.g., *Roboto*, *Inter*, or system UI sans).
- For developer/studio GUIs, add `--md-ref-typeface-mono` (e.g., *JetBrains Mono*, *Roboto Mono*) for numeric scrubbers, timecodes, coordinates, and shader/code editors, using `font-variant-numeric: tabular-nums`.

### Complete 30-Style Type Scale Table (`rem` / `px` at `16px` root)

| Role & Size | Token Prefix (`--md-sys-typescale-*`) | Font Size | Line Height | Tracking (Letter Spacing) | Baseline Weight | **M3 Expressive Emphasized Weight** | Typical Usage |
|---|---|---:|---:|---:|---:|---:|---|
| **Display Large** | `display-large` | `57px` (`3.5625rem`) | `64px` (`4rem`) | `-0.25px` | `400` | **`500`** | Hero numerals, splash titles |
| **Display Medium** | `display-medium` | `45px` (`2.8125rem`) | `52px` (`3.25rem`) | `0px` | `400` | **`500`** | Large editorial callouts |
| **Display Small** | `display-small` | `36px` (`2.25rem`) | `44px` (`2.75rem`) | `0px` | `400` | **`500`** | Section hero headers |
| **Headline Large** | `headline-large` | `32px` (`2rem`) | `40px` (`2.5rem`) | `0px` | `400` | **`500`** | Primary screen headings |
| **Headline Medium** | `headline-medium` | `28px` (`1.75rem`) | `36px` (`2.25rem`) | `0px` | `400` | **`500`** | Dialog/sheet hero titles |
| **Headline Small** | `headline-small` | `24px` (`1.5rem`) | `32px` (`2rem`) | `0px` | `400` | **`500`** | Standard dialog titles, card hero headers |
| **Title Large** | `title-large` | `22px` (`1.375rem`) | `28px` (`1.75rem`) | `0px` | `400` | **`500`** | Top app bar title, primary panel headers |
| **Title Medium** | `title-medium` | `16px` (`1rem`) | `24px` (`1.5rem`) | `+0.15px` | `500` | **`600` / `700`** | Card titles, subsection headers, L/XL button labels |
| **Title Small** | `title-small` | `14px` (`0.875rem`) | `20px` (`1.25rem`) | `+0.1px` | `500` | **`600` / `700`** | Inspector group headers, dense tabs |
| **Body Large** | `body-large` | `16px` (`1rem`) | `24px` (`1.5rem`) | `+0.5px` | `400` | **`500`** | Long-form reading, text field input values |
| **Body Medium** | `body-medium` | `14px` (`0.875rem`) | `20px` (`1.25rem`) | `+0.25px` | `400` | **`500`** | Default UI copy, list item supporting text, menus |
| **Body Small** | `body-small` | `12px` (`0.75rem`) | `16px` (`1rem`) | `+0.4px` | `400` | **`500`** | Helper text, captions, footnotes, timestamps |
| **Label Large** | `label-large` | `14px` (`0.875rem`) | `20px` (`1.25rem`) | `+0.1px` | `500` | **`600` / `700`** | Standard (`S`/`M`) button labels, chips, active navigation labels |
| **Label Medium** | `label-medium` | `12px` (`0.75rem`) | `16px` (`1rem`) | `+0.5px` | `500` | **`600` / `700`** | Navigation bar/rail labels, `XS` buttons, badges, studio property labels |
| **Label Small** | `label-small` | `11px` (`0.6875rem`) | `16px` (`1rem`) | `+0.5px` | `500` | **`600` / `700`** | Dense annotations, keyboard shortcut hints, micro-badges |

### When to Use Emphasized Typography
- **Selected states:** When a navigation tab, rail item, filter chip, or toggle button becomes selected, switch its label from `Baseline` to `Emphasized` (or animate variable font `GRAD` / `wght`) so active state is legible without relying solely on color.
- **Focal metrics & scrubbers:** Use `Emphasized` styles for active timecodes, frame counters, key KPIs, or primary card headers.
- **Layout stability tip:** When toggling between Baseline and Emphasized on hover/selection, if a standard `font-weight` change shifts text width and causes layout jitter, use the variable font `GRAD` (Grade) axis (`font-variation-settings: 'GRAD' 150`) which thickens strokes **without changing glyph advance widths**.

---

## 3. Shape Scale, Corner Nesting & Dynamic Shape Morphing

### Complete 10-Step Shape Scale (`--md-sys-shape-corner-*`)

| Token | Radius | Typical Components |
|---|---:|---|
| `--md-sys-shape-corner-none` | `0px` | Full-screen views, flush docked bars, sharp dividers |
| `--md-sys-shape-corner-extra-small` | `4px` | Menus, Snackbars, Plain Tooltips, Filled Text Field top corners (`4px 4px 0 0`), connected button inner corners |
| `--md-sys-shape-corner-small` | `8px` | Chips, Rich Tooltips, pressed button corners, compact studio inputs |
| `--md-sys-shape-corner-medium` | `12px` | Standard Cards, small FABs, selected toggleable buttons |
| `--md-sys-shape-corner-large` | `16px` | Standard FAB, Navigation Drawer, Extended FAB, large Cards |
| `--md-sys-shape-corner-large-increased` | `20px` | M3 Expressive medium/large cards, prominent panels |
| `--md-sys-shape-corner-extra-large` | `28px` | Dialogs, Bottom/Side Sheets (top/leading corners), Search View, Large FAB |
| `--md-sys-shape-corner-extra-large-increased` | `32px` | M3 Expressive large sheets and hero containers |
| `--md-sys-shape-corner-extra-extra-large` | `48px` | Extra-large M3 Expressive hero cards and XL buttons |
| `--md-sys-shape-corner-full` | `9999px` | Standard Buttons, Icon Buttons, Floating Toolbars, Search Bars, Sliders, Badges, Switches |

### Asymmetric Shapes & Optical Corner Nesting
- **Asymmetric modifiers:** Bottom sheets use `extra-large` top corners (`28px 28px 0 0`); side sheets and navigation drawers docked to the left use `0 16px 16px 0` (or `0 28px 28px 0`).
- **Concentric / Optical Nesting Rule:** Whenever a rounded element with radius $R_{\text{inner}}$ sits inside a container with radius $R_{\text{outer}}$ and padding $P$, set:
  $$R_{\text{inner}} = \max(0, R_{\text{outer}} - P)$$
  *Example:* A floating toolbar (`border-radius: 28px`, `padding: 8px`) containing a square-morphed active button should give that inner button `border-radius: 20px` when squarer, or `9999px` when pill-shaped.

### Interactive Shape Morphing (Buttons, Icon Buttons & Groups)
In M3 Expressive, interactive elements communicate state transitions by morphing their corner radius using `spring.fast.spatial`:

| Component State | Corner Shape | Visual Rationale |
|---|---|---|
| **Unselected / Rest** | `--md-sys-shape-corner-full` (Pill/Circle) | Friendly, approachable resting target |
| **Pressed (`:active`)** | `--md-sys-shape-corner-small` (`8px`) or `medium` (`12px`) | Immediate physical compression feedback |
| **Selected (`[aria-pressed="true"]` / `[aria-checked="true"]`)** | `--md-sys-shape-corner-medium` (`12px`) or `large` (`16px`) | Distinguishes toggled-on controls from resting pill controls by geometry as well as color |
| **Connected Button Group — Outer Ends** | `--md-sys-shape-corner-full` (`9999px`) on outer edges | Cohesive outer capsule silhouette |
| **Connected Button Group — Inner Seam** | `--md-sys-shape-corner-extra-small` (`4px`) or `small` (`8px`) (`2px` gap between siblings) | Crisp internal separation; morphs to `full` or `medium` when selected/pressed |

### The 35-Shape Polygon Library (`MaterialShapes`)
M3 Expressive includes 35 canonical geometric polygons (Circle, Square, Slanted, Arch, SemiCircle, Oval, Pill, Triangle, Arrow, Fan, Diamond, ClamShell, Pentagon, Gem, Sunny, VerySunny, Cookie4/6/7/9/12Sided, Ghostish, Clover4/8Leaf, Burst, SoftBurst, Boom, SoftBoom, Flower, Puffy, PuffyDiamond, PixelCircle, PixelTriangle, Bun, Heart).
- **Where to use:** Avatars, decorative media masks, badge frames, empty-state illustrations, and the indeterminate **Loading Indicator** (which cycles smoothly through a sequence of `MaterialShapes` polygons).
- **Platform support:** Native in Jetpack Compose via `androidx.graphics:graphics-shapes` (`RoundedPolygon`, `Morph`); on Web/SVG, implement via normalized SVG `<path>` or `<clip-path>` definitions with matching vertex counts for smooth interpolation.

---

## 4. Material Symbols (Variable Font Icons)

Always use **Material Symbols** (`Material Symbols Outlined`, `Material Symbols Rounded`, or `Material Symbols Sharp`), never the legacy static `Material Icons` font.

### The Four Variable Axes
Material Symbols expose four continuous CSS `font-variation-settings` axes:

| Axis Tag | Range | Default | M3 Best Practice |
|---|---|---|---|
| **`FILL`** | `0` (outlined) to `1` (filled) | `0` | **Animate `0` $\rightarrow$ `1` when a control becomes selected/active** (e.g., Navigation Bar/Rail item, toggle Icon Button, bookmark/favorite button). |
| **`wght`** | `100` to `700` | `400` | Match adjacent typography weight (`400` for baseline labels, `500`–`600` for emphasized labels). |
| **`GRAD`** | `-25` to `200` | `0` | Use `-25` for light icons on dark surfaces (prevents halation/bleed in dark mode!); use `200` for high-emphasis/hovered states without changing icon box size. |
| **`opsz`** | `20` to `48` | `24` | Set to match the rendered pixel size (`20` for `18px–20px` compact icons, `24` for standard `24px`, `40` or `48` for large/XL hero buttons). |

```css
.m3-icon {
  font-family: 'Material Symbols Rounded', 'Material Symbols Outlined';
  font-size: 24px;
  line-height: 1;
  font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
  transition: font-variation-settings var(--md-sys-motion-expressive-fast-effects);
}
[data-theme="dark"] .m3-icon {
  font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' -25, 'opsz' 24;
}
.is-selected .m3-icon,
[aria-pressed="true"] .m3-icon,
[aria-selected="true"] .m3-icon {
  font-variation-settings: 'FILL' 1, 'wght' 500, 'GRAD' 0, 'opsz' 24;
}
```
