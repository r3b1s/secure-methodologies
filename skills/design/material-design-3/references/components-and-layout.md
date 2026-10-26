# Adaptive Layout, Component Catalog & Studio GUI Patterns

This reference covers M3's responsive window size classes, canonical multi-pane layouts, the complete component catalog (including **M3 Expressive** components), and specialized guidance for desktop/creative/developer GUI tools.

---

## 1. Adaptive Layout & Window Size Classes

M3 layouts adapt to the application's **current window viewport**, never a static device detection check.

### Width & Height Breakpoints

| Size Class | Width Breakpoint | Height Breakpoint | Layout Margin | Inter-Pane Gap | Recommended Navigation |
|---|---|---|---|---|---|
| **Compact** | `< 600px` | `< 480px` | `16px` | — (1 pane) | Bottom `Navigation Bar` (3–5 destinations) or `Floating Toolbar` |
| **Medium** | `600px – 839px` | `480px – 899px` | `24px` | `16px` | Side `Navigation Rail` (3–7 destinations + optional FAB) |
| **Expanded** | `840px – 1199px` | `>= 900px` | `24px` | `24px` | `Navigation Rail` or `Expanded Navigation Rail` |
| **Large** | `1200px – 1599px` | — | `24px` | `24px` | `Expanded Navigation Rail` or persistent `Navigation Drawer` |
| **Extra-large** | `>= 1600px` | — | `24px` | `24px` | Persistent `Navigation Drawer` + contextual `Floating Toolbars` |

### Canonical Multi-Pane Layouts
Instead of stretching a single column past `840px`, split the workspace into **rounded, elevated/tonal panes** (`border-radius: var(--md-sys-shape-corner-large)` or `extra-large`) sitting on a `surface-container-lowest` or `surface-dim` background:

1. **List–Detail:** Fixed-width primary list pane (`360px–412px`) alongside a flexible detail pane (`flex: 1`). On `Compact`, the detail view pushes over the list.
2. **Supporting Pane (Primary Canvas + Inspector):** Primary workspace/canvas (`flex: 1`, minimum `60%` width) paired with a docked `surface-container` supporting pane (`320px–400px` wide) for properties, comments, or outliners. On `Compact`/`Medium`, the supporting pane converts into a modal `Side Sheet` or `Bottom Sheet`.
3. **Feed:** Responsive grid of cards (`grid-template-columns: repeat(auto-fill, minmax(280px, 1fr))`, `gap: 16px`).

---

## 2. Complete Component Catalog & Selection Rules

### Category A: Actions

| Component | Variants / Sizes | When to Use & Key Rules |
|---|---|---|
| **Common Buttons** | **Emphasis (high $\rightarrow$ low):**<br>1. `Filled` (`primary`)<br>2. `Filled Tonal` (`secondary-container`)<br>3. `Elevated` (`surface-container-low` + shadow)<br>4. `Outlined` (`outline` border)<br>5. `Text` (no container)<br><br>**M3 Expressive Sizes:**<br>`XS` (`32px` h), `S` (`40px` h, default), `M` (`56px` h), `L` (`96px` h), `XL` (`136px` h) | • Use **at most one `Filled` button** per card, dialog, or toolbar group to anchor the primary action.<br>• Pair `Filled` with `Filled Tonal` or `Text` for secondary actions (never place two `Filled` buttons side-by-side unless in a segmented/connected group).<br>• **Toggleable buttons:** M3 Expressive allows buttons to toggle between unselected (`full` pill shape, tonal/surface fill) and selected (`medium`/`large` rounded-rect shape, `primary` fill). |
| **Button Groups** *(M3 Expressive)* | • `Standard` (`8px–12px` gap)<br>• `Connected` (`2px` gap, pill outer ends, `4px–8px` inner seam corners) | • Replaces older `Segmented Buttons` for 2–5 closely related actions, view switchers, or tool modes.<br>• On press (`:active`), the pressed button widens slightly (`flex-grow` or horizontal padding boost) and morphs its corners while adjacent siblings subtly compress using `spring.fast.spatial`. |
| **Split Button** *(M3 Expressive)* | Leading primary action button + `2px` gap + trailing menu trigger button (`chevron_down`) | • Use when a common default action (e.g., *Render*, *Export*, *Save*, *Run*) has 2–6 secondary variants in a dropdown menu.<br>• Outer corners are `full` (`9999px`); inner seam corners are `extra-small` (`4px`). When the menu is open, the trailing button's corners morph to symmetric `full` or `medium` and the chevron rotates `180deg`. |
| **Icon Buttons** | `Standard`, `Filled`, `Filled Tonal`, `Outlined`<br>Sizes: `XS` (`32px`), `S` (`40px`), `M` (`56px`), `L` (`96px`), `XL` (`136px`) | • Minimum touch target is always `48×48px` on touchscreens (even when the visual container is `32px` or `40px`).<br>• Toggleable icon buttons animate `FILL` axis `0` $\rightarrow$ `1` and morph from circle (`full`) to squircle (`medium` `12px`) when selected. |
| **FAB & Extended FAB** | `Small` (`40px`), `Default` (`56px`, `16px` radius), `Large` (`96px`, `28px` radius), `Extended` (icon + label) | • Reserved for the **single most constructive primary action** on a screen (e.g., *Create*, *Compose*, *Add Keyframe*). Do not put a FAB on every panel. |
| **FAB Menu** *(M3 Expressive)* | Trigger FAB + 2–6 stacked pill menu items (`56px` height) | • Replaces legacy speed-dials. Activating the FAB morphs its icon to `close` and staggers 2–6 labeled `primary-container` or `secondary-container` pill buttons upward with `spring.fast.spatial`. |

#### Reference CSS Pattern: M3 Expressive Connected Button Group & Split Button

```css
/* Connected Button Group */
.m3e-button-group-connected {
  display: inline-flex;
  align-items: center;
  gap: 2px;
}
.m3e-button-group-connected > button {
  height: 40px;
  padding-inline: 16px;
  border: none;
  background: var(--md-sys-color-secondary-container);
  color: var(--md-sys-color-on-secondary-container);
  font: 500 0.875rem/1.25rem var(--md-ref-typeface-plain, sans-serif);
  border-radius: var(--md-sys-shape-corner-extra-small, 4px);
  transition:
    border-radius var(--md-sys-motion-expressive-fast-spatial),
    padding-inline var(--md-sys-motion-expressive-fast-spatial),
    background-color var(--md-sys-motion-expressive-fast-effects),
    color var(--md-sys-motion-expressive-fast-effects);
}
.m3e-button-group-connected > button:first-child {
  border-top-left-radius: var(--md-sys-shape-corner-full, 9999px);
  border-bottom-left-radius: var(--md-sys-shape-corner-full, 9999px);
}
.m3e-button-group-connected > button:last-child {
  border-top-right-radius: var(--md-sys-shape-corner-full, 9999px);
  border-bottom-right-radius: var(--md-sys-shape-corner-full, 9999px);
}
.m3e-button-group-connected > button:active {
  padding-inline: 22px; /* Expressive width expansion */
  border-radius: var(--md-sys-shape-corner-small, 8px);
}
.m3e-button-group-connected > button[aria-pressed="true"] {
  background: var(--md-sys-color-primary);
  color: var(--md-sys-color-on-primary);
  font-weight: 600; /* Emphasized label */
  border-radius: var(--md-sys-shape-corner-medium, 12px);
}
```

---

### Category B: Navigation & Toolbars

| Component | Variants | When to Use & Key Rules |
|---|---|---|
| **Floating Toolbar** *(M3 Expressive)* | • `Horizontal` (`64px` height, pill shape `9999px`) or `Vertical` (`64px` width)<br>• Color: `Standard` (`surface-container-high`) or `Vibrant` (`primary-container`) | • **Preferred over legacy Bottom App Bars.** Floats `16px` or `24px` inset from the viewport edge with Level 3 elevation.<br>• Ideal for canvas/viewport tools, playback controls, text formatting bars, and contextual actions.<br>• Can sit alongside an adjacent FAB (`8px–12px` gap). |
| **Docked Toolbar** *(M3 Expressive)* | Full-width bottom bar (`64px` height, `surface-container`) | • Use when a floating toolbar would obscure critical edge-to-edge bottom content. |
| **Flexible Navigation Bar** *(M3 Expressive)* | Bottom bar for `Compact` windows; supports stacked icon+label or inline horizontal icon+label | • Use for 3–5 top-level destinations on `Compact` screens. Active item displays a pill indicator (`secondary-container`) and switches its label to `Emphasized`. |
| **Navigation Rail & Expanded Navigation Rail** *(M3 Expressive)* | Collapsed (`80px` wide) $\leftrightarrow$ Expanded (`220px–360px` wide) | • Primary left navigation for `Medium`, `Expanded`, and `Large` windows. M3 Expressive merges the Rail and Drawer into a single **Expanded Navigation Rail** that smoothly animates open/closed with `spring.default.spatial`. |
| **Tabs** | `Primary` (under top app bar, 3dp active indicator bar) vs. `Secondary` (inside panes/cards, full-width indicator) | • Use `Primary` tabs to switch top-level sub-views of a category; use `Secondary` tabs inside an inspector panel or card. |
| **Search Bar & Search View** | Pill-shaped `Search Bar` (`56px` h, `surface-container-high`) expanding into full/modal `Search View` | • Also serves as the pattern for command palettes (`Ctrl+K` / `Cmd+K`) in desktop/studio apps. |

---

### Category C: Containment

| Component | Variants | When to Use & Key Rules |
|---|---|---|
| **Cards** | 1. `Filled` (`surface-container-highest`)<br>2. `Elevated` (`surface-container-low` + Level 1 shadow)<br>3. `Outlined` (`surface` + `outline-variant` border) | • Default corner radius is `medium` (`12px`) or `large-increased` (`20px`) in M3 Expressive.<br>• Do not overload cards with borders *and* shadows unless highlighting selection (`2px solid var(--md-sys-color-primary)`). |
| **Dialogs** | `Basic` (`280px–560px` w, `28px` corner radius, `surface-container-high`) & `Full-screen` | • Reserve for critical interruptions or focused tasks. Action buttons sit bottom-right (`Text` button for Cancel, `Filled` or `Text` button for Confirm). |
| **Bottom Sheets & Side Sheets** | `Standard` (co-planar, non-blocking, no scrim) vs. `Modal` (blocks background with `scrim`) | • Use `Standard Side Sheets` (`320px–400px` wide) for persistent property inspectors, history logs, or AI/chat sidebars on `Expanded`/`Large` screens. Include a `32×4px` `on-surface-variant` (`opacity: 0.4`) drag handle on bottom sheets. |
| **Carousel** | `Multi-browse`, `Uncontained`, `Hero`, `Full-screen` | • Items dynamically clip and morph width (`spring.default.spatial`) as they scroll near the leading/trailing edges of the container. |
| **Lists & Dividers** | 1-line, 2-line, 3-line list items; `1px` `outline-variant` dividers | • **Prefer tonal containment (`surface-container-*` groupings with `2px–4px` gaps) over heavy full-bleed dividers.** When using dividers, prefer inset dividers (`margin-inline: 16px`). |

---

### Category D: Communication

| Component | Variants | When to Use & Key Rules |
|---|---|---|
| **Loading Indicator** *(M3 Expressive)* | Uncontained (`on-primary-container` / `primary`) or Contained (`48×48px` `primary-container` circle) | • **Use for indeterminate waits under 5 seconds** (e.g., fetching data, refreshing a view). Smoothly morphs across a sequence of 7 M3 Expressive polygons while rotating. |
| **Progress Indicators** | `Linear` & `Circular`; `Flat` track or **M3 Expressive `Wavy` active indicator** (`4px` or `8px` thickness) | • Use for determinate progress (`0%–100%`, rendering frames, file exports, uploads) or waits exceeding 5 seconds. Include a `4px` stop gap between the active indicator and the remaining track (`secondary-container`). |
| **Snackbar** | Single-line or two-line (`inverse-surface` background, `inverse-on-surface` text, `inverse-primary` action) | • Floats at the bottom (`4px` corner radius), auto-dismisses after `4s–10s`, never stacks more than one at a time, and must not cover a `Floating Toolbar` or `FAB`. |
| **Tooltips** | `Plain` (`inverse-surface`, brief label) vs. `Rich` (`surface-container`, title + body + optional action) | • Every icon-only button (`Icon Button`, `Floating Toolbar` action, `Navigation Rail` item without label) **must** have an accessible label and tooltip. |
| **Badges** | Small dot (`6×6px`) or large count pill (`16px` height, `error` container with `on-error` label) | • Anchor to the top-right quadrant of an icon inside navigation items or icon buttons. |

---

### Category E: Selection & Category F: Text Inputs

| Component | Key Specifications & Best Practices |
|---|---|
| **Chips** | Four semantic types: **Assist** (smart actions), **Filter** (multi-select toggles, morphs leading checkmark in and switches to `secondary-container` fill), **Input** (user-entered tags with trailing `×` remove icon), **Suggestion** (dynamic query completions). Corner radius: `8px` (`small`). |
| **Sliders** | M3 Expressive updates sliders with a **thicker track (`16px`–`40px` tall)**, rounded outer ends, a **vertical bar thumb (`4px` wide × `44px` tall)** flanked by a `6px` transparent gap, and optional inset icon/value indicators. Great for timeline scrubbers, audio gain, and camera FOV/exposure controls. |
| **Switch** | `52×32px` pill track (`outline` border + `surface-container-highest` when off; `primary` fill when on). Thumb morphs size (`16px` off $\rightarrow$ `24px` on, or `24px` with icon) and expands to `28px` while pressed (`spring.fast.spatial`). |
| **Checkbox & Radio** | Checkbox uses `2px` border, `18×18px` box (`2px–4px` radius), `40px` state layer, `48px` touch target. Supports `checked`, `unchecked`, and `indeterminate`. |
| **Menus** | `surface-container` background, Level 2 elevation, `4px` (`extra-small`) or `12px` (`medium`) corner radius, `48px` standard item height (`36px` in compact desktop density). |
| **Text Fields** | Two variants: **`Filled`** (`surface-container-highest` background, `4px 4px 0 0` top corners, bottom `1px` $\rightarrow$ `2px` active indicator bar) and **`Outlined`** (`4px` all-around `outline` border with floating cut-out label). **Never mix `Filled` and `Outlined` text fields within the same form or panel.** |

---

## 3. Applying M3 Expressive to Desktop, Creative & Studio GUI Tools

Many developer, video production, and 3D tools (such as Three.js studios, timeline editors, and node-graph tools) have denser requirements than mobile apps. Apply M3 Expressive to studio GUIs using these four adaptations:

### 1. Dark-First Neutral Canvas + Expressive Focal Controls
- **Canvas Surround:** Use `--md-sys-color-surface-container-lowest` (Dark Tone `4`) behind 3D viewports, video previews, and timelines so the UI recedes and never competes with viewport luminance.
- **Color Scheme Choice:** If the user is grading color or inspecting lighting, generate the theme with **`SchemeNeutral`** (or low-chroma `SchemeTonalSpot`) so panels (`surface-container` Tone `12`) remain near-neutral gray while primary focal buttons and playheads still use clear semantic `primary` / `tertiary` accents.
- **Floating Viewport Overlays:** Place camera presets, gizmo mode toggles (Translate / Rotate / Scale), and playback transport inside an **M3 Expressive Horizontal or Vertical Floating Toolbar** (`surface-container-high` with `backdrop-filter: blur(12px)` or solid Tone `17`, `border-radius: 9999px`) inset `16px` from the viewport edge.

### 2. M3 Density Scale for Inspector Panels (`-1`, `-2`, `-3`)
Standard M3 targets `48px` touch targets (`Density 0`). For mouse/keyboard desktop inspector panels, apply M3's systematic density scale (`-4px` height per step):

| Density Level | Button / Chip / Input Height | List / Menu Item Height | Where to Apply |
|---|---:|---:|---|
| **Default (`0`)** | `40px` (`56px` text field) | `48px–56px` | Primary Floating Toolbars, Dialogs, Welcome screens, Touch devices |
| **Compact (`-1`)** | `36px` (`48px` text field) | `40px` | Top bars, secondary toolbars, standard desktop forms |
| **Dense (`-2`)** | `32px` (`40px` text field) | `36px` | Scene outliners, asset browsers, timeline track headers |
| **Ultra-Dense (`-3`)** | `28px` (`32px` scrubber/input) | `28px–32px` | XYZ transform scrubbers, shader uniform tables, keyframe dope sheets |

### 3. Numeric Scrubbers & Sliders
- Use `--md-ref-typeface-mono` with `font-variant-numeric: tabular-nums` inside numeric inputs so live scrubbing at 60fps never causes horizontal layout jitter.
- Pair M3 Expressive thick-track **Sliders** (`16px–24px` tall track with `4px` vertical bar thumb gap) for bounded parameters (`0.0–1.0` roughness, FOV, opacity) with compact `Filled` (`surface-container-highest`) scrubbers for unbounded XYZ coordinates.

### 4. Keyboard-First Focus & Command Palette
- Maintain visible `:focus-visible` rings (`2px solid var(--md-sys-color-primary)`, `outline-offset: 2px`) on every toolbar button, tree node, and timeline track.
- Style the studio's `Ctrl+K` / `Cmd+K` command palette as an M3 **Search View** (`surface-container-high`, `28px` corner radius, Level 3 shadow) with keyboard shortcut chips styled using `label-small` in `surface-container-highest`.
