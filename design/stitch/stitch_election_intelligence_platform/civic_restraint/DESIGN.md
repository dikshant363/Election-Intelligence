---
name: Civic Restraint
colors:
  surface: '#fcf8fb'
  surface-dim: '#dcd9dc'
  surface-bright: '#fcf8fb'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f6f3f5'
  surface-container: '#f0edef'
  surface-container-high: '#eae7ea'
  surface-container-highest: '#e4e2e4'
  on-surface: '#1b1b1d'
  on-surface-variant: '#444651'
  inverse-surface: '#303032'
  inverse-on-surface: '#f3f0f2'
  outline: '#757682'
  outline-variant: '#c5c5d3'
  surface-tint: '#4059aa'
  primary: '#00236f'
  on-primary: '#ffffff'
  primary-container: '#1e3a8a'
  on-primary-container: '#90a8ff'
  inverse-primary: '#b6c4ff'
  secondary: '#0051d5'
  on-secondary: '#ffffff'
  secondary-container: '#316bf3'
  on-secondary-container: '#fefcff'
  tertiary: '#1d2b3d'
  on-tertiary: '#ffffff'
  tertiary-container: '#334154'
  on-tertiary-container: '#9eadc4'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#dce1ff'
  primary-fixed-dim: '#b6c4ff'
  on-primary-fixed: '#00164e'
  on-primary-fixed-variant: '#264191'
  secondary-fixed: '#dbe1ff'
  secondary-fixed-dim: '#b4c5ff'
  on-secondary-fixed: '#00174b'
  on-secondary-fixed-variant: '#003ea8'
  tertiary-fixed: '#d5e3fc'
  tertiary-fixed-dim: '#b9c7df'
  on-tertiary-fixed: '#0d1c2e'
  on-tertiary-fixed-variant: '#3a485b'
  background: '#fcf8fb'
  on-background: '#1b1b1d'
  surface-variant: '#e4e2e4'
  surface-canvas: '#FBFBFD'
  surface-card: '#FFFFFF'
  surface-subtle: '#F5F5F7'
  border-subtle: '#E5E5EA'
  status-verified: '#15803D'
  status-verified-bg: '#ECFDF5'
  status-disputed: '#D97706'
  status-disputed-bg: '#FFFBEB'
  archive-slate: '#475569'
  archive-slate-bg: '#F1F5F9'
typography:
  display:
    fontFamily: Inter
    fontSize: 44px
    fontWeight: '600'
    lineHeight: 52px
    letterSpacing: -0.022em
  headline-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
    letterSpacing: -0.019em
  headline-lg-mobile:
    fontFamily: Inter
    fontSize: 26px
    fontWeight: '600'
    lineHeight: 34px
    letterSpacing: -0.015em
  headline-md:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
    letterSpacing: -0.015em
  headline-sm:
    fontFamily: Inter
    fontSize: 19px
    fontWeight: '600'
    lineHeight: 26px
    letterSpacing: -0.011em
  body-lg:
    fontFamily: Inter
    fontSize: 17px
    fontWeight: '400'
    lineHeight: 24px
    letterSpacing: -0.008em
  body-md:
    fontFamily: Inter
    fontSize: 15px
    fontWeight: '400'
    lineHeight: 22px
    letterSpacing: -0.005em
  body-sm:
    fontFamily: Inter
    fontSize: 13px
    fontWeight: '400'
    lineHeight: 18px
    letterSpacing: -0.002em
  label-md:
    fontFamily: Inter
    fontSize: 13px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.01em
  label-sm:
    fontFamily: Inter
    fontSize: 11px
    fontWeight: '600'
    lineHeight: 14px
    letterSpacing: 0.04em
  numeric-data:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
    letterSpacing: 0em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  gutter: 1.25rem
  gutter-mobile: 0.75rem
  margin: 2rem
  margin-mobile: 1rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2.5rem
---

## Brand & Style

This design system establishes a high-integrity, institutional research interface modeled on the core principles of human interface guidelines: spatial clarity, deference to content, and meticulous typographic hierarchy. The aesthetic is strictly non-partisan, authoritative, and analytical. Rather than sensationalizing democratic data, it recedes into the background to let facts, empirical models, and civic records speak with indisputable clarity.

The visual style blends refined modern minimalism with structured institutional precision. High legibility, nuanced surface depth, and quiet tactile feedback create an environment of academic rigor, accessible both to constitutional scholars and everyday voters navigating intricate multi-tier electoral datasets.

## Colors

The color system avoids any affiliation with partisan flags or political campaign palettes by anchoring on a deep civic navy (`#1E3A8A`) and an active interface blue (`#2563EB`). Backgrounds step away from stark, blinding cold whites in favor of an Apple-inspired warm studio canvas (`#FBFBFD`) complemented by segmented container cards (`#FFFFFF`) and elevated system fills (`#F5F5F7`).

Data veracity is conveyed via a dedicated tri-tier semantic spectrum:
- **Verified / Audited Data:** Deep forest green (`#15803D`) paired with an ultra-light tint (`#ECFDF5`) for validated affidavits and certified tallies.
- **Disputed / Unverified Claims:** Non-alarmist analytical amber (`#D97706`) over (`#FFFBEB`) for contested metrics, active litigation notes, or discrepancies.
- **Official Archive:** Neutral slate (`#475569`) with (`#F1F5F9`) denoting historical gazette entries and non-variable institutional transcripts.

## Typography

The typography mirrors Apple's San Francisco system through **Inter**, optimized for optical balance, precise numerals, and seamless cross-rendering alongside bilingual Devanagari system fonts (such as Kohinoor Devanagari or Noto Sans Devanagari). 

Key rules:
- Tabular figures (`tnum`, `cv01`, `zero`) must be enforced on all electoral tallies, vote margins, and census percentages to preserve vertical decimal alignment.
- When rendering Devanagari conjuncts or transliterated candidate profiles, vertical line-height rules require an automatic 4px buffer over standard Latin baselines to prevent vowel diacritic clipping (`matras`).
- Labels and audit badges use small, tight tracking with medium-to-semibold weights to preserve clarity at compact sizes.

## Layout & Spacing

The platform follows a responsive 12-column adaptive fluid grid structured for multi-panel civic dashboards, legislative overviews, and granular constituency tables.

- **Desktop (1024px and up):** 12-column layout with `2rem` outer margins and `1.25rem` column gutters. Max content container is capped at 1280px for standard research dossiers and 1440px for complex geographic mapping matrices.
- **Tablet (768px - 1023px):** 8-column layout with `1.5rem` margins and `1rem` gutters. Sidebars fold into standard sliding inspector sheets.
- **Mobile (below 768px):** 4-column layout with `1rem` edge margins and `0.75rem` gutters. Deep data tables convert to vertically stacked comparison cards or horizontally pinned-scroll cells with a persistent lead column.

## Elevation & Depth

In alignment with modern human interface standards, depth is produced via translucent materials, tonal layer nesting, and hair-thin border definitions rather than heavy, dramatic dropshadows.

- **Base Layer:** `#FBFBFD` background canvas.
- **Card Tier 1:** Solid `#FFFFFF` elevated via a 1px composite outline (`#000000` at 6% alpha) and an ambient sub-surface diffuse shadow (`0 2px 8px rgba(0, 0, 0, 0.04)`).
- **Floating Modals & Flyouts:** Crisp `#FFFFFF` resting upon a dual-tier shadow (`0 8px 24px rgba(0, 0, 0, 0.08)`, `0 1px 2px rgba(0, 0, 0, 0.04)`).
- **Navigation Bars & Sticky Filters:** Ultra-thin frosted materials utilizing `backdrop-filter: blur(20px) saturate(180%)` over `#FFFFFF` at 85% opacity, demarcated from the canvas by a bottom border of `#000000` at 8% alpha.

## Shapes

The design uses a refined geometric scale (`roundedness: 2`), reflecting the continuous curvature (`squircle`) aesthetic of modern operating systems. 

- Interactive controls, audit pills, and source citations use micro-radii (6px to 8px) to remain compact and analytical.
- Data containers, constituency briefing cards, and search inputs apply `rounded-lg` (16px).
- Modals, large analytical panes, and slide-in panels adopt `rounded-xl` (24px).
- Status tokens and inline tags adopt full pill geometry (`9999px`) to distinguish categorical metadata from rectangular data panels.

## Components

### Buttons & Interactive Controls
- **Primary Action:** Solid `#1E3A8A` filled background, white Inter 14px Semibold text, 8px corner radius. Subtle scale down (0.98) on click.
- **Secondary Action:** Translucent fill (`#F5F5F7`), `#1D1D1F` text, hovering to `#E5E5EA`.
- **Text / Citation Trigger:** No background, `#2563EB` link text with an integrated external link icon.

### Evidence & Verification Badges
- **Verified:** 6px vertical pill containing `#15803D` text, `#ECFDF5` background, and an enclosed 12px checkmark icon. Used strictly for Election Commission of India (ECI) certified reports.
- **Disputed / Pending:** `#D97706` text over `#FFFBEB` with a subtle amber border (`#FDE68A`). Accompanied by a tooltip trigger showing competing affidavit links.
- **Official Archive:** `#475569` text over `#F1F5F9`.

### Source Citation Pills
- Compact inline components (`font-size: 11px`, `height: 22px`, `border-radius: 9999px`, padding `0 8px`). Built with a light slate border (`#E2E8F0`), displaying source abbreviation (e.g., `[ECI-2024]`, `[ADR]`, `[Delimitation-2008]`) which opens a citation popover containing the unedited gazette link and timestamp.

### Civic Data Tables
- Strict grid alignment with `#F5F5F7` column headers in 11px uppercase tracking.
- Row division using `#E5E5EA` hair-lines (0.5px to 1px). Alternating row hover state set to `#FBFBFD`.
- Right-aligned tabular numeric values for vote counts, booth turnouts, and demographic percentages.
- Fixed left column on mobile views for candidate/constituency names.

### Form Inputs & Constituency Search
- Bordered text boxes using `#FFFFFF` interior with a 1px border of `#D1D5DB`.
- Active focus state: `#2563EB` continuous hairline ring with an outer 3px blue glow at 15% opacity (`rgba(37, 99, 235, 0.15)`).
- Clear integrated search icon left-aligned and keyboard shortcut badge (`⌘K` / `Ctrl+K`) right-aligned.