# Official Repositories, Multi-Stack Integration & Audit Checklist

This reference details where Material Design 3's official source code lives across platforms, how to share a single M3 design token foundation across a repository and its submodules, how to integrate M3/M3 Expressive into existing Web, Desktop, Android, and Flutter codebases, and what anti-patterns to avoid.

---

## 1. Official Upstream Repositories & Package Matrix

| Domain | GitHub Repository | Published Package(s) | Maintenance Status & Role |
|---|---|---|---|
| **Color & HCT Engine (All Platforms)** | https://github.com/material-foundation/material-color-utilities | • npm: `@material/material-color-utilities`<br>• Pub: `material_color_utilities`<br>• Maven/Java, C++, Swift in repo | **Active & Canonical.** The mathematical engine for HCT color space, tonal palettes, image quantization, contrast curves, and dynamic schemes (`SchemeTonalSpot`, `SchemeExpressive`, `SchemeVibrant`, `SchemeNeutral`, etc.). |
| **Material Symbols (Icons)** | https://github.com/google/material-design-icons | • npm: `@material-design-icons/font`, `material-symbols`<br>• Google Fonts: `Material Symbols Outlined` / `Rounded` / `Sharp` | **Active.** Variable icon fonts (`FILL`, `wght`, `GRAD`, `opsz`) and raw SVGs. Replaces legacy static "Material Icons". |
| **Theme Builder & Figma Tokens** | https://github.com/material-foundation/material-theme-builder<br>https://github.com/material-foundation/material-tokens | Figma Plugin: *Material Theme Builder* | **Active.** Exports JSON design tokens, CSS custom properties, Jetpack Compose `Color.kt`/`Theme.kt`, and Flutter `ThemeData`. |
| **Web Components (Lit)** | https://github.com/material-components/material-web | npm: `@material/web` (`<md-filled-button>`, `<md-dialog>`, `<md-slider>`, etc.) | **Maintenance Mode.** Framework-agnostic Custom Elements for standard M3. Does not yet include the newer M3 Expressive components (Button Groups, Split Button, Floating Toolbar, Loading Indicator), which should be authored with CSS tokens. |
| **Legacy Web (M2 — DO NOT USE)** | https://github.com/material-components/material-components-web | npm: `material-components-web`, `@material/mwc-*`, `@mui/material` (v5 default is M2) | **Archived / Legacy M2.** Do not install `material-components-web` for M3 projects. (Note: MUI v5/v6 is a third-party React library targeting M2 by default, not official M3.) |
| **Android (Jetpack Compose)** | https://github.com/androidx/androidx (`compose/material3/`) | Maven: `androidx.compose.material3:material3` (`1.4.0+` / `1.5.0+`), `androidx.graphics:graphics-shapes` | **Active Reference Implementation.** First-class support for all M3 and M3 Expressive APIs (`MaterialExpressiveTheme`, `MotionScheme`, `MaterialShapes`, `ButtonGroup`, `SplitButtonLayout`, `HorizontalFloatingToolbar`, `FloatingActionButtonMenu`, `LoadingIndicator`). |
| **Android Views (XML)** | https://github.com/material-components/material-components-android | Maven: `com.google.android.material:material` (`1.13.0+`) | **Active.** XML themes (`Theme.Material3.*`), spring motion tokens, and Views support. |
| **Flutter** | https://github.com/flutter/flutter (`packages/flutter/lib/src/material/`) | Built-in `package:flutter/material.dart` + community `package:material_3_expressive` | **Active.** M3 is enabled by default (`useMaterial3: true`). Pair with `material_3_expressive` on pub.dev for M3 Expressive spring physics and expressive widgets. |

---

## 2. Programmatic Token Generation (`@material/material-color-utilities`)

For any Web, TypeScript, Vite, Node, or Electron/Tauri GUI project, generate the complete Light and Dark `--md-sys-color-*` token set directly from a seed color using `@material/material-color-utilities`.

### Install
```sh
npm install @material/material-color-utilities
```

### Generate All 48 Semantic M3 Color Tokens (TypeScript)
This module generates every M3 surface container, accent, outline, inverse, and fixed color token for both Light and Dark mode, and either applies them to `:root` at runtime or emits a standalone `tokens.css` file at build time:

```ts
import {
  argbFromHex,
  hexFromArgb,
  Hct,
  MaterialDynamicColors,
  SchemeExpressive,
  SchemeNeutral,
  SchemeTonalSpot,
  SchemeVibrant,
  type DynamicScheme,
} from '@material/material-color-utilities';

export type M3SchemeVariant = 'tonal-spot' | 'expressive' | 'vibrant' | 'neutral';

const COLOR_TOKENS = {
  'primary': MaterialDynamicColors.primary,
  'on-primary': MaterialDynamicColors.onPrimary,
  'primary-container': MaterialDynamicColors.primaryContainer,
  'on-primary-container': MaterialDynamicColors.onPrimaryContainer,
  'primary-fixed': MaterialDynamicColors.primaryFixed,
  'primary-fixed-dim': MaterialDynamicColors.primaryFixedDim,
  'on-primary-fixed': MaterialDynamicColors.onPrimaryFixed,
  'on-primary-fixed-variant': MaterialDynamicColors.onPrimaryFixedVariant,
  'secondary': MaterialDynamicColors.secondary,
  'on-secondary': MaterialDynamicColors.onSecondary,
  'secondary-container': MaterialDynamicColors.secondaryContainer,
  'on-secondary-container': MaterialDynamicColors.onSecondaryContainer,
  'secondary-fixed': MaterialDynamicColors.secondaryFixed,
  'secondary-fixed-dim': MaterialDynamicColors.secondaryFixedDim,
  'on-secondary-fixed': MaterialDynamicColors.onSecondaryFixed,
  'on-secondary-fixed-variant': MaterialDynamicColors.onSecondaryFixedVariant,
  'tertiary': MaterialDynamicColors.tertiary,
  'on-tertiary': MaterialDynamicColors.onTertiary,
  'tertiary-container': MaterialDynamicColors.tertiaryContainer,
  'on-tertiary-container': MaterialDynamicColors.onTertiaryContainer,
  'tertiary-fixed': MaterialDynamicColors.tertiaryFixed,
  'tertiary-fixed-dim': MaterialDynamicColors.tertiaryFixedDim,
  'on-tertiary-fixed': MaterialDynamicColors.onTertiaryFixed,
  'on-tertiary-fixed-variant': MaterialDynamicColors.onTertiaryFixedVariant,
  'error': MaterialDynamicColors.error,
  'on-error': MaterialDynamicColors.onError,
  'error-container': MaterialDynamicColors.errorContainer,
  'on-error-container': MaterialDynamicColors.onErrorContainer,
  'surface-dim': MaterialDynamicColors.surfaceDim,
  'surface': MaterialDynamicColors.surface,
  'surface-bright': MaterialDynamicColors.surfaceBright,
  'surface-container-lowest': MaterialDynamicColors.surfaceContainerLowest,
  'surface-container-low': MaterialDynamicColors.surfaceContainerLow,
  'surface-container': MaterialDynamicColors.surfaceContainer,
  'surface-container-high': MaterialDynamicColors.surfaceContainerHigh,
  'surface-container-highest': MaterialDynamicColors.surfaceContainerHighest,
  'on-surface': MaterialDynamicColors.onSurface,
  'on-surface-variant': MaterialDynamicColors.onSurfaceVariant,
  'outline': MaterialDynamicColors.outline,
  'outline-variant': MaterialDynamicColors.outlineVariant,
  'inverse-surface': MaterialDynamicColors.inverseSurface,
  'inverse-on-surface': MaterialDynamicColors.inverseOnSurface,
  'inverse-primary': MaterialDynamicColors.inversePrimary,
  'scrim': MaterialDynamicColors.scrim,
  'shadow': MaterialDynamicColors.shadow,
} as const;

export function createM3Scheme(
  seedHex: string,
  isDark: boolean,
  variant: M3SchemeVariant = 'expressive',
  contrastLevel = 0.0, // 0.0 = standard, 0.5 = medium, 1.0 = high
): DynamicScheme {
  const sourceHct = Hct.fromInt(argbFromHex(seedHex));
  switch (variant) {
    case 'expressive':
      return new SchemeExpressive(sourceHct, isDark, contrastLevel);
    case 'vibrant':
      return new SchemeVibrant(sourceHct, isDark, contrastLevel);
    case 'neutral':
      return new SchemeNeutral(sourceHct, isDark, contrastLevel);
    case 'tonal-spot':
    default:
      return new SchemeTonalSpot(sourceHct, isDark, contrastLevel);
  }
}

export function schemeToCssVariables(scheme: DynamicScheme): Record<string, string> {
  const vars: Record<string, string> = {};
  for (const [name, dynamicColor] of Object.entries(COLOR_TOKENS)) {
    vars[`--md-sys-color-${name}`] = hexFromArgb(dynamicColor.getArgb(scheme));
  }
  return vars;
}

export function applyM3Theme(
  seedHex: string,
  options: { isDark?: boolean; variant?: M3SchemeVariant; contrastLevel?: number; target?: HTMLElement } = {},
): void {
  const { isDark = true, variant = 'expressive', contrastLevel = 0.0, target = document.documentElement } = options;
  const scheme = createM3Scheme(seedHex, isDark, variant, contrastLevel);
  const vars = schemeToCssVariables(scheme);
  for (const [prop, value] of Object.entries(vars)) {
    target.style.setProperty(prop, value);
  }
  target.dataset.theme = isDark ? 'dark' : 'light';
}
```

---

## 3. Sharing UX/DX Across a Parent Repository and Git Submodules

When developing multiple standalone GUI tools across a parent repository and Git submodules (for example, a main production repo with standalone web/Three.js submodules that must also build and run independently):

1. **Zero-Dependency Token Contract (`--md-sys-*`):**
   - Because M3 standardizes every token name (`--md-sys-color-surface-container`, `--md-sys-shape-corner-large`, `--md-sys-motion-expressive-fast-spatial`), submodules do **not** need a tight runtime dependency on the parent repo to share identical UX/DX.
   - Define a self-contained `m3-tokens.css` (containing the Light/Dark color variables, 10 corner radius tokens, 12 spring motion curves, and type scale classes) that can either be imported directly or generated from the same seed hex (`seedHex` + `variant` + `contrastLevel`).
2. **Submodule Independence with Parent Override:**
   - In each submodule, declare token defaults on `:root` using CSS custom properties so the submodule works standalone (`vite dev` inside the submodule).
   - When the parent repo embeds or frames the submodule, or when multiple tools run side-by-side on the desktop, all tools read the same `--md-sys-*` custom properties and automatically match theme, contrast, shape, and motion physics.
3. **Lightweight Shared Primitives:**
   - For zero-framework TypeScript/Vite GUIs (such as Three.js viewports and studio tools), prefer **semantic HTML + M3 CSS classes/Web Components** over heavy framework-locked widget trees. A `<button class="m3-btn m3-btn--filled">` or `<div class="m3-floating-toolbar">` works identically in Vanilla TS, Lit, React, Vue, or Svelte.

---

## 4. Platform-Specific Integration Guides

### A. Web: Combining `@material/web` with M3 Expressive CSS
If you want ready-made accessible primitives for complex controls (dialogs, menus, sliders, switches, text fields) alongside custom M3 Expressive controls:

```sh
npm install @material/web
```

```ts
// Import only the components you use (tree-shakeable):
import '@material/web/button/filled-button.js';
import '@material/web/button/filled-tonal-button.js';
import '@material/web/iconbutton/icon-button.js';
import '@material/web/slider/slider.js';
import '@material/web/switch/switch.js';
import '@material/web/dialog/dialog.js';
import '@material/web/textfield/filled-text-field.js';
```

`@material/web` components automatically consume the `--md-sys-color-*` and `--md-sys-shape-*` CSS custom properties set on `:root` by `applyM3Theme()` above. To add M3 Expressive spring physics and shape morphing to `@material/web` or native elements, apply the `--md-sys-motion-expressive-*` transitions from [references/expressive-style-system.md](expressive-style-system.md).

### B. Android / Jetpack Compose (`MaterialExpressiveTheme`)
In Jetpack Compose (`androidx.compose.material3:material3:1.4.0+`):

```kotlin
import androidx.compose.material3.ExperimentalMaterial3ExpressiveApi
import androidx.compose.material3.MaterialExpressiveTheme
import androidx.compose.material3.MotionScheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.dynamicDarkColorScheme

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun AppTheme(
    darkTheme: Boolean = true,
    content: @Composable () -> Unit,
) {
    MaterialExpressiveTheme(
        colorScheme = darkColorScheme(), // or dynamicDarkColorScheme(LocalContext.current)
        motionScheme = MotionScheme.expressive(), // or MotionScheme.standard()
        content = content,
    )
}
```
Access spring tokens directly anywhere in Compose via `MaterialTheme.motionScheme.fastSpatialSpec()`, `defaultSpatialSpec()`, `slowSpatialSpec()`, `fastEffectsSpec()`, `defaultEffectsSpec()`, `slowEffectsSpec()`.

### C. Flutter (`useMaterial3` + `ColorScheme.fromSeed`)
```dart
final ThemeData studioTheme = ThemeData(
  useMaterial3: true,
  colorScheme: ColorScheme.fromSeed(
    seedColor: const Color(0xFF6750A4),
    brightness: Brightness.dark,
    dynamicSchemeVariant: DynamicSchemeVariant.expressive, // or .tonalSpot, .neutral, .vibrant
    contrastLevel: 0.0,
  ),
);
```

---

## 5. Verification & Anti-Pattern Checklist

Run through this checklist whenever authoring or reviewing an M3 / M3 Expressive UI:

### Color & Surface Anti-Patterns
- [ ] **No hardcoded hex/RGB colors in components:** Every background, text, icon, and border references `--md-sys-color-*` (or `MaterialTheme.colorScheme.*`).
- [ ] **No mismatched `on-*` pairings:** Text on `primary` uses `on-primary` (never hardcoded `#ffffff`, which fails in dark mode where `primary` is Tone 80 and `on-primary` is Tone 20!).
- [ ] **No white-opacity elevation overlays:** Depth in dark and light mode is built with `surface-container-lowest` $\rightarrow$ `low` $\rightarrow$ `default` $\rightarrow$ `high` $\rightarrow$ `highest`, not `rgba(255, 255, 255, 0.05)` hacks.
- [ ] **No legacy `surface-variant` overuse:** Prefer the 5-step `surface-container-*` hierarchy over the older single `surface-variant` token for cards and panels.

### Motion & Shape Anti-Patterns
- [ ] **Never apply a bouncy (`spatial`) spring to opacity or color (`effects`):** Spatial springs overshoot `1.0`, causing opacity/color clipping and flicker. Always pair `spring.*.spatial` (for `transform`, `width`, `border-radius`) with `spring.*.effects` (for `background-color`, `color`, `opacity`).
- [ ] **Respect `prefers-reduced-motion: reduce`:** Collapse spatial spring animations and polygon morphs when reduced motion is requested while keeping fast opacity/color state transitions intact.
- [ ] **Optical corner nesting:** Nested rounded elements reduce their inner radius by the parent's padding ($R_{\text{inner}} = \max(0, R_{\text{outer}} - P)$).

### Component & Layout Anti-Patterns
- [ ] **Button emphasis discipline:** At most **one** high-emphasis `Filled` button (or `FAB`) per logical view/group; secondary actions use `Filled Tonal`, `Outlined`, or `Text`.
- [ ] **Text field consistency:** Never mix `Filled` and `Outlined` text fields in the same form or inspector panel.
- [ ] **Accessible icon-only controls:** Every `Icon Button`, `Floating Toolbar` icon, and collapsed `Navigation Rail` item has an `aria-label` / tooltip and a minimum `48×48px` touch target (`32px–36px` only in explicit desktop compact density `-2`/`-3` with visible `:focus-visible` outline).
- [ ] **Material Symbols variable axes:** Icons use **Material Symbols** (not legacy Material Icons), set `GRAD -25` in dark mode, and animate `FILL 0 -> 1` when selected.
