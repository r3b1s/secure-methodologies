# Design Tokens, HCT Color System, Elevation & State Layers

This reference covers Material Design 3's token architecture, the HCT perceptual color space, tonal palettes, all semantic color roles (including surface containers and fixed roles), contrast levels, elevation, and interaction state layers.

---

## 1. Three-Tier Design Token Architecture

Material Design 3 decouples raw values from semantic intent and component anatomy through three token tiers:

```
Reference Token (--md-ref-palette-primary40: #6750A4)
       ↓
System Token    (--md-sys-color-primary: var(--md-ref-palette-primary40))
       ↓
Component Token (--md-filled-button-container-color: var(--md-sys-color-primary))
```

| Tier | Naming Pattern | Role | Rules |
|---|---|---|---|
| **1. Reference** | `md.ref.<category>.<name>` (`--md-ref-*`) | Raw values: tonal palette stops (`0`–`100`), font families (`brand`, `plain`), font weights (`regular`, `medium`, `bold`). | Never use directly in application styles or component templates; they do not adapt to dark mode or contrast changes. |
| **2. System** | `md.sys.<category>.<role>` (`--md-sys-*`) | Semantic design decisions: color roles, type scale roles, corner shape steps, spring motion tokens, elevation levels, state layer opacities. | **Primary authoring layer.** All custom components, application layouts, and studio panels consume `--md-sys-*` tokens. |
| **3. Component** | `md.comp.<component>.<element>.<property>` | Scoped component tokens mapping anatomy elements (e.g., `container`, `label-text`, `leading-icon`) to system tokens. | Override only when customizing a specific component type without changing global system semantics. |

---

## 2. The HCT Color Space & Tonal Palettes

Unlike HSL or RGB (where a yellow and a blue with identical "50% lightness" have drastically different perceived brightness and WCAG contrast), M3 uses **HCT (Hue, Chroma, Tone)**:

- **Hue ($H$, $0^\circ\text{–}360^\circ$):** CAM16 perceptual hue angle.
- **Chroma ($C$, $0\text{–}\approx 120$):** Colorfulness/saturation relative to neutral gray.
- **Tone ($T$, $0\text{–}100$):** CIE $L^*$ perceptual lightness ($0$ = pure black, $100$ = pure white).

**Crucial property of HCT:** A Tone difference ($\Delta T$) guarantees a predictable WCAG contrast ratio **regardless of Hue or Chroma**:
- $\Delta T \ge 40 \implies$ contrast ratio $\ge 3.0:1$ (WCAG AA large text / active UI boundaries)
- $\Delta T \ge 50 \implies$ contrast ratio $\ge 4.5:1$ (WCAG AA normal text)
- $\Delta T \ge 70 \implies$ contrast ratio $\ge 7.0:1$ (WCAG AAA)

### The Six Key Tonal Palettes
From a single source seed color (or custom brand key colors), `@material/material-color-utilities` generates six tonal palettes, each evaluated at tones `0, 4, 6, 10, 12, 17, 20, 22, 24, 25, 30, 35, 40, 50, 60, 70, 80, 87, 90, 92, 94, 95, 96, 98, 99, 100`:

| Palette | Default Derivation (`SchemeTonalSpot`) | Purpose |
|---|---|---|
| **Primary (`a1`)** | Seed Hue, Chroma `36` | High-emphasis fills, active states, focal controls |
| **Secondary (`a2`)** | Seed Hue, Chroma `16` | Lower-emphasis fills, filter chips, tonal buttons |
| **Tertiary (`a3`)** | Seed Hue $+ 60^\circ$, Chroma `24` | Complementary accents, badges, editorial balance |
| **Neutral (`n1`)** | Seed Hue, Chroma `6` (`4` in baseline) | Surfaces, backgrounds, surface containers (`lowest` to `highest`) |
| **Neutral Variant (`n2`)** | Seed Hue, Chroma `8` | Outlines, dividers, `on-surface-variant`, subtle surface differentiation |
| **Error** | Hue `25`, Chroma `84` | Semantic error states and destructive confirmation |

### Dynamic Scheme Variants
Choose the scheme constructor in `@material/material-color-utilities` that fits your product:

| Scheme Variant | Character | Best For |
|---|---|---|
| **`SchemeTonalSpot`** | Balanced chroma (default M3) | General-purpose apps and standard productivity tools |
| **`SchemeExpressive`** | Hue-rotated primary, playful contrast with secondary/tertiary | **M3 Expressive** apps, consumer tools, creative & lifestyle UIs |
| **`SchemeVibrant`** | High chroma across primary, secondary, and tertiary | Media players, expressive dashboards, brand-forward experiences |
| **`SchemeNeutral`** | Near-achromatic (`Chroma ~2–4`) surfaces and subdued accents | **Color-critical GUI studios** (3D viewports, video grading, photo editing) where UI chrome must not visually tint the canvas |
| **`SchemeMonochrome`** | Zero chroma (`Chroma 0`) grayscale throughout | High-minimalism or e-ink / monochrome modes |
| **`SchemeFidelity`** / **`SchemeContent`** | Preserves exact source seed Hue & Chroma on `primaryContainer` / `primary` | Strict brand-color compliance or album-art/content-derived themes |

---

## 3. Complete Semantic Color Roles & Tone Mapping Table

Never pair arbitrary colors. Always pair a container/surface token with its corresponding `on-*` token.

### Accent & Status Roles

| CSS Custom Property (`--md-sys-color-*`) | Palette | Light Tone (Std) | Dark Tone (Std) | Usage |
|---|---|---:|---:|---|
| `primary` | Primary | `40` | `80` | Filled buttons, active states, switches, active indicators |
| `on-primary` | Primary | `100` | `20` | Text and icons directly on `primary` |
| `primary-container` | Primary | `90` | `30` | FABs, vibrant floating toolbars, selected navigation pills |
| `on-primary-container` | Primary | `10` (or `30`) | `90` | Text and icons on `primary-container` |
| `secondary` | Secondary | `40` | `80` | Less prominent accents |
| `on-secondary` | Secondary | `100` | `20` | Text and icons on `secondary` |
| `secondary-container` | Secondary | `90` | `30` | Filled tonal buttons, selected filter chips, navigation rail indicator |
| `on-secondary-container` | Secondary | `10` (or `30`) | `90` | Text and icons on `secondary-container` |
| `tertiary` | Tertiary | `40` | `80` | Complementary highlights, FAB menu close button |
| `on-tertiary` | Tertiary | `100` | `20` | Text and icons on `tertiary` |
| `tertiary-container` | Tertiary | `90` | `30` | Input overlays, badge callouts, contrasting cards |
| `on-tertiary-container` | Tertiary | `10` (or `30`) | `90` | Text and icons on `tertiary-container` |
| `error` | Error | `40` | `80` | Invalid input borders, destructive button fills, error icons |
| `on-error` | Error | `100` | `20` | Text and icons on `error` |
| `error-container` | Error | `90` | `30` | Error banners, warning callouts |
| `on-error-container` | Error | `10` | `90` | Text and icons on `error-container` |

### Surface, Container, Outline & Utility Roles

| CSS Custom Property (`--md-sys-color-*`) | Palette | Light Tone | Dark Tone | Usage |
|---|---|---:|---:|---|
| `surface-dim` | Neutral | `87` | `6` | Dimmed canvas backdrop |
| `surface` | Neutral | `98` | `6` | Default root background |
| `surface-bright` | Neutral | `98` | `24` | Highlighted or elevated dark-mode surface |
| `surface-container-lowest` | Neutral | `100` | `4` | Recessed wells, 3D/video viewport surrounds, code blocks |
| `surface-container-low` | Neutral | `96` | `10` | Low-emphasis cards, secondary side panes |
| `surface-container` | Neutral | `94` | `12` | Default panels, navigation bars/rails, standard cards |
| `surface-container-high` | Neutral | `92` | `17` | Floating toolbars, elevated cards, side/bottom sheets |
| `surface-container-highest` | Neutral | `90` | `22` | Dialogs, menus, popovers, filled text-field backgrounds |
| `on-surface` | Neutral | `10` | `90` | Primary body text, headlines, active icons on any `surface*` |
| `on-surface-variant` | Neutral Variant | `30` | `80` | Secondary text, captions, supporting text, inactive icons |
| `outline` | Neutral Variant | `50` | `60` | 3:1 accessible control borders (inputs, outlined buttons) |
| `outline-variant` | Neutral Variant | `80` | `30` | Decorative dividers, subtle panel hairlines, outlined cards |
| `inverse-surface` | Neutral | `20` | `90` | Snackbars and plain tooltips (high contrast against canvas) |
| `inverse-on-surface` | Neutral | `95` | `20` | Text inside snackbars and plain tooltips |
| `inverse-primary` | Primary | `80` | `40` | Action button text inside `inverse-surface` snackbars |
| `scrim` | Neutral | `0` | `0` | Modal backdrop (`opacity: 0.32` to `0.5`) |
| `shadow` | Neutral | `0` | `0` | Elevation ambient/key shadow base color |

### Fixed Color Roles (Theme-Invariant)
Fixed roles keep the **exact same tone in both Light and Dark mode**:

| Role | Palette | Light & Dark Tone | Usage |
|---|---|---:|---|
| `primary-fixed` / `secondary-fixed` / `tertiary-fixed` | Primary / Sec / Tert | `90` | Branded containers or media overlays that never invert |
| `primary-fixed-dim` / `secondary-fixed-dim` / `tertiary-fixed-dim` | Primary / Sec / Tert | `80` | Pressed/emphasized sub-containers inside fixed containers |
| `on-primary-fixed` / `on-secondary-fixed` / `on-tertiary-fixed` | Primary / Sec / Tert | `10` | Primary text on fixed containers |
| `on-primary-fixed-variant` / `on-secondary-fixed-variant` / `on-tertiary-fixed-variant` | Primary / Sec / Tert | `30` | Secondary text/icons on fixed containers |

### Contrast Levels
M3 supports three user/system contrast levels passed into dynamic scheme constructors (`0.0` Standard, `0.5` Medium, `1.0` High). In Medium and High contrast, container tones and `on-*` tones pull further apart (e.g., $\Delta T \ge 70$), and subtle borders become higher-contrast outlines automatically.

---

## 4. Elevation & Surface Hierarchy

In M3, **depth is communicated primarily through `surface-container-*` tone steps**, not drop shadows. Shadows are added only when a component floats physically above scrolling or variable content (e.g., a Floating Toolbar over a 3D canvas, a FAB, or a Menu popover).

| Elevation Level | Token | Resting Shadow (Web CSS Approximation) | Typical Components |
|---|---|---|---|
| **Level 0** (`0dp`) | `--md-sys-elevation-level0` | `none` | Filled/Outlined cards, Navigation Bar/Rail, Docked panels |
| **Level 1** (`1dp`) | `--md-sys-elevation-level1` | `0 1px 2px rgba(0,0,0,0.3), 0 1px 3px 1px rgba(0,0,0,0.15)` | Elevated cards, Elevated buttons, Bottom sheets |
| **Level 2** (`3dp`) | `--md-sys-elevation-level2` | `0 1px 2px rgba(0,0,0,0.3), 0 2px 6px 2px rgba(0,0,0,0.15)` | Menus, Rich tooltips, Scrolled Top App Bar |
| **Level 3** (`6dp`) | `--md-sys-elevation-level3` | `0 4px 8px 3px rgba(0,0,0,0.15), 0 1px 3px rgba(0,0,0,0.3)` | **FAB**, **Floating Toolbar**, **Dialogs**, Date/Time Pickers |
| **Level 4** (`8dp`) | `--md-sys-elevation-level4` | `0 6px 10px 4px rgba(0,0,0,0.15), 0 2px 3px rgba(0,0,0,0.3)` | Hovered FAB / Dragged card |
| **Level 5** (`12dp`) | `--md-sys-elevation-level5` | `0 8px 12px 6px rgba(0,0,0,0.15), 0 4px 4px rgba(0,0,0,0.3)` | High-altitude modal overlays |

---

## 5. Interaction State Layers & Focus Rings

M3 never darkens or lightens a button's container color directly via arbitrary math on `:hover` or `:active`. Instead, it renders a **State Layer**—an overlay between the container background and its content (text/icon) whose color matches the content (`on-*` role) at a fixed opacity:

| Interaction State | State Layer Opacity Token | Value | Notes |
|---|---|---:|---|
| **Enabled (Rest)** | — | `0%` | Base container color only |
| **Hovered** | `--md-sys-state-hover-state-layer-opacity` | `8%` (`0.08`) | Uses `on-*` color (e.g., `on-primary` on a Filled button) |
| **Focused** | `--md-sys-state-focus-state-layer-opacity` | `10%` (`0.10`) | Paired with a `2px`–`3px` `--md-sys-color-secondary` outline (`outline-offset: 2px`) on `:focus-visible` |
| **Pressed (Active)** | `--md-sys-state-pressed-state-layer-opacity` | `10%` (`0.10`) | Plus optional ripple and M3 Expressive corner shape morph |
| **Dragged** | `--md-sys-state-dragged-state-layer-opacity` | `16%` (`0.16`) | Elevates component by +1 or +2 levels |
| **Disabled Container** | — | `12%` (`0.12`) | Always uses `on-surface` at `12%` opacity (never the accent color) |
| **Disabled Content** | — | `38%` (`0.38`) | Always uses `on-surface` at `38%` opacity for text and icons |

### Modern CSS State Layer Implementation (`color-mix`)
In modern browsers, you can compute state layers cleanly without extra DOM wrapper elements using CSS `color-mix(in srgb, ...)`:

```css
.m3-filled-button {
  --_bg: var(--md-sys-color-primary);
  --_fg: var(--md-sys-color-on-primary);
  background-color: var(--_bg);
  color: var(--_fg);
}
.m3-filled-button:hover {
  background-color: color-mix(in srgb, var(--_fg) 8%, var(--_bg));
}
.m3-filled-button:focus-visible {
  background-color: color-mix(in srgb, var(--_fg) 10%, var(--_bg));
  outline: 3px solid var(--md-sys-color-secondary);
  outline-offset: 2px;
}
.m3-filled-button:active {
  background-color: color-mix(in srgb, var(--_fg) 10%, var(--_bg));
}
.m3-filled-button:disabled {
  background-color: color-mix(in srgb, var(--md-sys-color-on-surface) 12%, transparent);
  color: color-mix(in srgb, var(--md-sys-color-on-surface) 38%, transparent);
  pointer-events: none;
}
```
