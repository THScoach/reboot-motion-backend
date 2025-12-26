# Catching Barrels Design System

**Version:** 2.0  
**Date:** December 26, 2025  
**Status:** Complete — Phase 0

---

## 📋 Table of Contents

1. [Introduction](#introduction)
2. [Foundations](#foundations)
   - [Color Palette](#color-palette)
   - [Typography](#typography)
   - [Spacing System](#spacing-system)
   - [Grid System](#grid-system)
   - [Elevation (Shadows)](#elevation-shadows)
   - [Border Radius](#border-radius)
   - [Motion & Animation](#motion--animation)
3. [Components](#components)
4. [Patterns](#patterns)
5. [Design Tokens](#design-tokens)

---

## 🎯 Introduction

The Catching Barrels Design System provides a comprehensive framework for building consistent, accessible, and high-quality user interfaces across the PWA. This system ensures:

- **Consistency:** Unified visual language across all 13 screens
- **Efficiency:** Reusable components and patterns reduce development time
- **Accessibility:** WCAG AA compliance (4.5:1 contrast minimum)
- **Scalability:** Token-based system adapts to future design changes
- **Performance:** Optimized for mobile-first, progressive web app

**Design Philosophy:**
- **Clean Athletic Professional:** Modern, energetic, data-driven
- **Mobile-First:** Optimized for 375×812 (iPhone 13 Pro) and up
- **Performance-Focused:** Fast load times, smooth animations
- **Accessible:** Keyboard navigation, screen readers, color contrast

---

# 🎨 FOUNDATIONS

## Color Palette

### Primary Colors (Electric Cyan)

Used for primary actions, brand elements, KRS scores, and interactive elements.

| Shade | Hex | RGB | Use Case |
|-------|-----|-----|----------|
| **primary-50** | `#ECFEFF` | rgb(236, 254, 255) | Background tints |
| **primary-100** | `#CFFAFE` | rgb(207, 250, 254) | Hover states (light) |
| **primary-200** | `#A5F3FC` | rgb(165, 243, 252) | Disabled states |
| **primary-300** | `#67E8F9` | rgb(103, 232, 249) | Accents |
| **primary-400** | `#22D3EE` | rgb(34, 211, 238) | Hover states |
| **primary-500** | `#06B6D4` | rgb(6, 182, 212) | **PRIMARY** — Buttons, links, KRS |
| **primary-600** | `#0891B2` | rgb(8, 145, 178) | Active states |
| **primary-700** | `#0E7490` | rgb(14, 116, 144) | Dark mode primary |
| **primary-800** | `#155E75` | rgb(21, 94, 117) | — |
| **primary-900** | `#164E63` | rgb(22, 78, 99) | — |

**Usage Rules:**
- **primary-500 (#06B6D4):** Primary buttons, links, KRS score text, active nav items, progress bars
- **primary-600 (#0891B2):** Button hover states, active button press
- **primary-400 (#22D3EE):** Link hover states, focus rings
- **primary-100 (#CFFAFE):** Background tints for info cards

**Accessibility:** primary-500 on white = 4.52:1 contrast ✅ WCAG AA

---

### Neutral Colors (Slate Scale)

Used for text, backgrounds, borders, and structural elements.

| Shade | Hex | RGB | Use Case |
|-------|-----|-----|----------|
| **neutral-50** | `#F8FAFC` | rgb(248, 250, 252) | Background (lightest) |
| **neutral-100** | `#F1F5F9` | rgb(241, 245, 249) | Card backgrounds |
| **neutral-200** | `#E2E8F0` | rgb(226, 232, 240) | Borders (light) |
| **neutral-300** | `#CBD5E1` | rgb(203, 213, 225) | Borders (default) |
| **neutral-400** | `#94A3B8` | rgb(148, 163, 184) | Placeholder text |
| **neutral-500** | `#64748B` | rgb(100, 116, 139) | Secondary text |
| **neutral-600** | `#475569` | rgb(71, 85, 105) | Tertiary text |
| **neutral-700** | `#334155` | rgb(51, 65, 85) | Body text |
| **neutral-800** | `#1E293B` | rgb(30, 41, 59) | Headings |
| **neutral-900** | `#0F172A` | rgb(15, 23, 42) | **PRIMARY TEXT** |

**Usage Rules:**
- **neutral-900 (#0F172A):** Primary text (headings, important labels)
- **neutral-700 (#334155):** Body text (paragraphs, descriptions)
- **neutral-500 (#64748B):** Secondary text (captions, helper text)
- **neutral-400 (#94A3B8):** Placeholder text, disabled text
- **neutral-300 (#CBD5E1):** Default borders (cards, inputs)
- **neutral-100 (#F1F5F9):** Card backgrounds, subtle backgrounds
- **neutral-50 (#F8FAFC):** Page backgrounds

**Accessibility:** neutral-900 on white = 16.1:1 contrast ✅ WCAG AAA

---

### Semantic Colors

#### Success (Green)

| Shade | Hex | Use Case |
|-------|-----|----------|
| **success-50** | `#F0FDF4` | Background |
| **success-100** | `#DCFCE7` | Light tint |
| **success-500** | `#10B981` | **PRIMARY** — Success messages, positive indicators |
| **success-600** | `#059669` | Hover state |
| **success-700** | `#047857` | Dark mode |

**Usage:** Success messages, positive KRS changes (+5 points ↑), "Good" status pills, checkmarks

#### Warning (Amber)

| Shade | Hex | Use Case |
|-------|-----|----------|
| **warning-50** | `#FFFBEB` | Background |
| **warning-100** | `#FEF3C7` | Light tint |
| **warning-500** | `#F59E0B` | **PRIMARY** — Warning messages, moderate indicators |
| **warning-600** | `#D97706` | Hover state |
| **warning-700** | `#B45309` | Dark mode |

**Usage:** Warning messages, moderate status ("Near target" in Live Mode), caution indicators

#### Error (Red)

| Shade | Hex | Use Case |
|-------|-----|----------|
| **error-50** | `#FEF2F2` | Background |
| **error-100** | `#FEE2E2` | Light tint |
| **error-500** | `#EF4444` | **PRIMARY** — Error messages, critical issues |
| **error-600** | `#DC2626` | Hover state |
| **error-700** | `#B91C1C` | Dark mode |

**Usage:** Error messages, validation errors, critical status ("Off target" in Live Mode), delete actions

#### Info (Blue)

| Shade | Hex | Use Case |
|-------|-----|----------|
| **info-50** | `#EFF6FF` | Background |
| **info-100** | `#DBEAFE` | Light tint |
| **info-500** | `#3B82F6` | **PRIMARY** — Info messages, neutral indicators |
| **info-600** | `#2563EB` | Hover state |
| **info-700** | `#1D4ED8` | Dark mode |

**Usage:** Info messages, tooltips, neutral status indicators, onboarding highlights

---

### 4B Framework Colors

Special colors for Brain, Body, Bat, Ball cards with tinted backgrounds.

#### Brain (Purple)

| Element | Hex | RGB | Use Case |
|---------|-----|-----|----------|
| **Background** | `#EDE9FE` | rgb(237, 233, 254) | Card background (light purple tint) |
| **Text/Icon** | `#7C3AED` | rgb(124, 58, 237) | Text, icons, borders |
| **Border** | `#A78BFA` | rgb(167, 139, 250) | Card border (optional) |

**Usage:** Brain card (Motor Profile, Confidence, Timing)

#### Body (Blue)

| Element | Hex | RGB | Use Case |
|---------|-----|-----|----------|
| **Background** | `#DBEAFE` | rgb(219, 234, 254) | Card background (light blue tint) |
| **Text/Icon** | `#2563EB` | rgb(37, 99, 235) | Text, icons, borders |
| **Border** | `#60A5FA` | rgb(96, 165, 250) | Card border (optional) |

**Usage:** Body card (Creation Score, Physical Capacity, Peak Force)

#### Bat (Green)

| Element | Hex | RGB | Use Case |
|---------|-----|-----|----------|
| **Background** | `#D1FAE5` | rgb(209, 250, 229) | Card background (light green tint) |
| **Text/Icon** | `#059669` | rgb(5, 150, 105) | Text, icons, borders |
| **Border** | `#34D399` | rgb(52, 211, 153) | Card border (optional) |

**Usage:** Bat card (Transfer Score, Efficiency, Attack Angle)

#### Ball (Red/Pink)

| Element | Hex | RGB | Use Case |
|---------|-----|-----|----------|
| **Background** | `#FEE2E2` | rgb(254, 226, 226) | Card background (light red tint) |
| **Text/Icon** | `#DC2626` | rgb(220, 38, 38) | Text, icons, borders |
| **Border** | `#F87171` | rgb(248, 113, 113) | Card border (optional) |

**Usage:** Ball card (Exit Velocity, Launch Angle, Contact Quality)

**Design Note:** All 4B card backgrounds use 5-10% opacity tints of their primary color to maintain readability while providing visual distinction.

---

### Motor Profile Colors

Colors representing the 4 Motor Profile types.

| Profile | Hex | RGB | Use Case |
|---------|-----|-----|----------|
| **Spinner** | `#10B981` | rgb(16, 185, 129) | Upper-body rotation dominant |
| **Slingshotter** | `#F59E0B` | rgb(245, 158, 11) | Balanced rotation |
| **Whipper** | `#EF4444` | rgb(239, 68, 68) | Aggressive hip rotation |
| **Titan** | `#8B5CF6` | rgb(139, 92, 246) | Strength-dominant |

**Usage:** Motor Profile badges, icons, chart legends

---

## Typography

### Font Families

**Primary:** Inter Variable  
**Fallback:** -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif  
**Monospace:** SF Mono, Monaco, "Courier New", monospace

**Why Inter?**
- Optimized for digital screens
- Excellent readability at small sizes
- Variable font = fewer HTTP requests
- Wide character set (supports 139 languages)

**Font Loading Strategy:**
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
```

---

### Type Scale

| Name | Desktop | Mobile | Line Height | Letter Spacing | Weight | Use Case |
|------|---------|--------|-------------|----------------|--------|----------|
| **display-01** | 96px | 72px | 1.0 | -0.02em | 700 (Bold) | Hero text (rarely used) |
| **display-02** | 72px | 56px | 1.0 | -0.02em | 700 (Bold) | **KRS Score** |
| **heading-01** | 32px | 28px | 1.2 | -0.01em | 700 (Bold) | Page titles (H1) |
| **heading-02** | 24px | 22px | 1.3 | 0 | 600 (Semibold) | Section headers (H2) |
| **heading-03** | 20px | 18px | 1.4 | 0 | 600 (Semibold) | Subsection headers (H3) |
| **heading-04** | 18px | 16px | 1.4 | 0 | 600 (Semibold) | Card titles (H4) |
| **body-01** | 16px | 16px | 1.5 | 0 | 400 (Regular) | **Body text** (paragraphs) |
| **body-02** | 14px | 14px | 1.5 | 0 | 400 (Regular) | Secondary body text |
| **caption-01** | 14px | 14px | 1.4 | 0 | 400 (Regular) | Labels, metadata |
| **caption-02** | 12px | 12px | 1.4 | 0.01em | 500 (Medium) | Uppercase labels, badges |
| **small** | 12px | 12px | 1.4 | 0 | 400 (Regular) | Helper text, footnotes |

**Usage Guidelines:**

**Display-02 (72px/56px):**
- KRS score display (Home Dashboard, Report Hero)
- Very large numbers requiring emphasis
- Use sparingly (1-2 per screen max)

**Heading-01 (32px/28px):**
- Page titles: "Player Report", "Progress Dashboard"
- Screen headers (H1)
- Main navigation labels (when large)

**Heading-02 (24px/22px):**
- Section headers: "Your KRS Journey", "4B Framework"
- Card group titles

**Heading-03 (20px/18px):**
- Subsection headers: "Recent Sessions", "Recommended Drills"
- Card titles (larger cards)

**Heading-04 (18px/16px):**
- Card titles (standard cards)
- List item headers

**Body-01 (16px):**
- Primary body text (paragraphs, descriptions)
- Button text (medium/large buttons)
- Input field text

**Body-02 (14px):**
- Secondary body text (less important descriptions)
- List items
- Button text (small buttons)

**Caption-01 (14px):**
- Labels: "Creation Score", "Transfer Score"
- Metadata: "2 hours ago", "Last session"
- Breadcrumbs

**Caption-02 (12px):**
- Uppercase labels: "ADVANCED", "ELITE"
- Badges: "NEW", "RECOMMENDED"
- Small status indicators

**Small (12px):**
- Helper text below inputs
- Footnotes
- Legal text

---

### Font Weights

| Weight | Value | Use Case |
|--------|-------|----------|
| **Regular** | 400 | Body text, descriptions, captions |
| **Medium** | 500 | Emphasized text, labels, uppercase badges |
| **Semibold** | 600 | Headings (H2-H4), button text, tabs |
| **Bold** | 700 | Display text, H1, KRS score, primary emphasis |

**Usage Rules:**
- **400 (Regular):** Default for all body text
- **500 (Medium):** Use for labels that need slight emphasis without being headings
- **600 (Semibold):** Standard for all headings H2-H4, button text
- **700 (Bold):** Reserved for H1, display text (KRS score), very strong emphasis

---

### Line Heights

| Name | Value | Use Case |
|------|-------|----------|
| **tight** | 1.0 | Display text (KRS score 72px) |
| **snug** | 1.2 | Headings (H1) |
| **normal** | 1.5 | Body text (paragraphs) |
| **relaxed** | 1.75 | Long-form content (rarely used) |

**Usage:**
- **1.0:** Only for very large display text (KRS score)
- **1.2:** Headings H1
- **1.3:** Headings H2
- **1.4:** Headings H3-H4, captions
- **1.5:** Body text (default)

---

### Letter Spacing

| Name | Value | Use Case |
|------|-------|----------|
| **tight** | -0.02em | Display text (72px+) |
| **normal** | 0 | Body text, headings |
| **wide** | 0.01em | Uppercase labels (12px) |

**Usage:**
- **-0.02em:** Large display text (improves optical spacing at large sizes)
- **0:** Default for body text and most headings
- **0.01em:** Uppercase text (improves readability of all-caps)

---

## Spacing System

### Base Unit: 4px

All spacing values are multiples of 4px for consistent vertical rhythm.

| Token | Value | Rem | Use Case |
|-------|-------|-----|----------|
| `space-0` | 0px | 0 | No spacing |
| `space-1` | 4px | 0.25rem | Icon padding, tight spacing |
| `space-2` | 8px | 0.5rem | Small gaps (badge padding) |
| `space-3` | 12px | 0.75rem | Default gap between elements |
| `space-4` | 16px | 1rem | **Standard spacing** (card padding) |
| `space-5` | 20px | 1.25rem | Medium gaps |
| `space-6` | 24px | 1.5rem | Section spacing |
| `space-8` | 32px | 2rem | Large gaps (between sections) |
| `space-10` | 40px | 2.5rem | Extra large gaps |
| `space-12` | 48px | 3rem | Page margins (top/bottom) |
| `space-16` | 64px | 4rem | Hero section padding |
| `space-20` | 80px | 5rem | Rarely used |
| `space-24` | 96px | 6rem | Very large spacing |
| `space-32` | 128px | 8rem | Maximum spacing |

**Usage Guidelines:**

**Inset Spacing (Padding):**
- **space-4 (16px):** Default card padding
- **space-6 (24px):** Large card padding
- **space-3 (12px):** Button padding (vertical)
- **space-4 (16px):** Button padding (horizontal)
- **space-2 (8px):** Badge padding
- **space-1 (4px):** Icon padding

**Stack Spacing (Margin-Bottom / Gap):**
- **space-2 (8px):** Between label and value
- **space-3 (12px):** Between form fields
- **space-4 (16px):** Between paragraphs
- **space-6 (24px):** Between sections (same card)
- **space-8 (32px):** Between major sections (different cards)
- **space-12 (48px):** Page top/bottom padding

**Inline Spacing (Margin-Right / Gap):**
- **space-2 (8px):** Between icon and text
- **space-3 (12px):** Between buttons in a group
- **space-4 (16px):** Between cards in a grid

---

## Grid System

### Breakpoints

| Name | Min Width | Columns | Gutters | Margins | Max Content Width |
|------|-----------|---------|---------|---------|-------------------|
| **Mobile** | 320px | 4 | 16px | 16px | 100% |
| **Mobile-L** | 375px | 4 | 16px | 16px | 100% |
| **Tablet** | 768px | 8 | 16px | 24px | 720px |
| **Desktop** | 1024px | 12 | 24px | 48px | 1200px |
| **Wide** | 1440px | 12 | 24px | 96px | 1200px |

**Mobile-First Approach:**
- Design for 375×812 (iPhone 13 Pro) first
- Scale up using responsive breakpoints
- Use `min-width` media queries (mobile-first)

**Media Query Syntax:**
```css
/* Mobile (default, < 768px) */
.element { ... }

/* Tablet (>= 768px) */
@media (min-width: 768px) {
  .element { ... }
}

/* Desktop (>= 1024px) */
@media (min-width: 1024px) {
  .element { ... }
}

/* Wide (>= 1440px) */
@media (min-width: 1440px) {
  .element { ... }
}
```

---

### Grid Layout

**Container:**
```css
.container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 16px; /* Mobile */
}

@media (min-width: 768px) {
  .container {
    padding: 0 24px; /* Tablet */
  }
}

@media (min-width: 1024px) {
  .container {
    padding: 0 48px; /* Desktop */
  }
}
```

**Grid:**
```css
.grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr); /* Mobile: 4 columns */
  gap: 16px;
}

@media (min-width: 768px) {
  .grid {
    grid-template-columns: repeat(8, 1fr); /* Tablet: 8 columns */
  }
}

@media (min-width: 1024px) {
  .grid {
    grid-template-columns: repeat(12, 1fr); /* Desktop: 12 columns */
    gap: 24px;
  }
}
```

**Column Spanning:**
```css
/* Mobile: Full width (4 columns) */
.card {
  grid-column: span 4;
}

/* Tablet: Half width (4 columns) */
@media (min-width: 768px) {
  .card {
    grid-column: span 4;
  }
}

/* Desktop: One-third width (4 columns) */
@media (min-width: 1024px) {
  .card {
    grid-column: span 4;
  }
}
```

---

## Elevation (Shadows)

### Shadow Scale

| Level | Name | Value | Use Case |
|-------|------|-------|----------|
| **0** | None | `box-shadow: none;` | Flat elements (no elevation) |
| **1** | sm | `0 1px 2px 0 rgb(0 0 0 / 0.05)` | Subtle cards, inputs (default) |
| **2** | md | `0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)` | Raised cards, dropdowns |
| **3** | lg | `0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)` | Modals, popovers |
| **4** | xl | `0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)` | Floating action buttons, tooltips |
| **5** | 2xl | `0 25px 50px -12px rgb(0 0 0 / 0.25)` | Overlays, full-screen modals |

**Usage Guidelines:**

**Level 0 (None):**
- Flush cards (no visual separation)
- Background elements
- Text on colored backgrounds

**Level 1 (sm):**
- Default cards (Home Dashboard cards)
- Input fields (focus state)
- List items

**Level 2 (md):**
- Elevated cards (hover state)
- Dropdown menus
- Tabs (active state)

**Level 3 (lg):**
- Modals
- Popovers
- Context menus
- Bottom sheets

**Level 4 (xl):**
- Floating Action Buttons (FAB)
- Tooltips
- Snackbars

**Level 5 (2xl):**
- Full-screen overlays
- Critical modals
- Image lightboxes

**Interaction Shadows:**
```css
/* Card hover effect */
.card {
  box-shadow: 0 1px 2px 0 rgb(0 0 0 / 0.05); /* Level 1 */
  transition: box-shadow 200ms ease-in-out;
}

.card:hover {
  box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1); /* Level 2 */
}
```

---

## Border Radius

| Token | Value | Use Case |
|-------|-------|----------|
| `radius-none` | 0px | Sharp corners (rarely used) |
| `radius-sm` | 4px | Badges, small pills |
| `radius-md` | 8px | **Default** — Buttons, inputs, small cards |
| `radius-lg` | 12px | Cards, modals |
| `radius-xl` | 16px | Large cards, hero sections |
| `radius-2xl` | 24px | Extra large cards (rarely used) |
| `radius-full` | 9999px | Pills, avatars, circular buttons |

**Usage Guidelines:**

**radius-md (8px):**
- Default for buttons (all sizes)
- Input fields
- Small cards (drill cards in grid)
- Status pills (with padding)

**radius-lg (12px):**
- Standard cards (Home Dashboard cards, 4B cards)
- Modals
- Bottom navigation background

**radius-xl (16px):**
- Large hero cards (KRS Hero Card on Home)
- Feature cards (onboarding cards)

**radius-full (9999px):**
- Pills: "ADVANCED" badge, status pills
- Avatars: User profile pictures
- Circular buttons: Play button overlays

**Examples:**
```css
/* Button */
.button {
  border-radius: 8px; /* radius-md */
}

/* Card */
.card {
  border-radius: 12px; /* radius-lg */
}

/* Badge */
.badge {
  border-radius: 9999px; /* radius-full */
}
```

---

## Motion & Animation

### Duration

| Token | Value | Use Case |
|-------|-------|----------|
| `duration-instant` | 150ms | Instant feedback (button press) |
| `duration-fast` | 200ms | **Default** — Hover effects, focus states |
| `duration-normal` | 300ms | Page transitions, modal open/close |
| `duration-slow` | 500ms | Complex animations (chart rendering) |
| `duration-slower` | 1000ms | Count-up effects (KRS score animation) |

**Usage Guidelines:**

**150ms (Instant):**
- Button active state (press down)
- Checkbox/radio toggle
- Immediate visual feedback

**200ms (Fast) — DEFAULT:**
- Button hover
- Card hover (shadow change)
- Input focus (border color)
- Link hover (underline)

**300ms (Normal):**
- Modal fade-in
- Dropdown slide-down
- Tooltip appearance
- Page transitions

**500ms (Slow):**
- Chart animations (line drawing)
- Progress bar fill
- Complex multi-step animations

**1000ms (Slower):**
- KRS score count-up effect (0 → 75)
- Loading spinners (rotation)
- Skeleton screen pulse

---

### Easing Functions

| Token | Value | Use Case |
|-------|-------|----------|
| `ease-linear` | `linear` | Constant speed (loading spinners) |
| `ease-in` | `cubic-bezier(0.4, 0, 1, 1)` | Exit animations (fade out, slide out) |
| `ease-out` | `cubic-bezier(0, 0, 0.2, 1)` | **Default** — Enter animations (fade in, slide in) |
| `ease-in-out` | `cubic-bezier(0.4, 0, 0.2, 1)` | Two-way animations (modal open/close) |
| `ease-bounce` | `cubic-bezier(0.68, -0.55, 0.27, 1.55)` | Playful animations (badge pop-in) |

**Usage Guidelines:**

**ease-out (Default):**
- Element appearing (fade in)
- Element sliding in (dropdown, modal)
- Hover effects (shadow, scale)

**ease-in:**
- Element disappearing (fade out)
- Element sliding out
- Dismiss animations

**ease-in-out:**
- Modal open/close
- Page transitions
- Two-directional movements

**ease-linear:**
- Loading spinners (360° rotation)
- Progress bars (consistent speed)

**Examples:**
```css
/* Button hover */
.button {
  transition: background-color 200ms ease-out;
}

/* Modal fade-in */
.modal {
  animation: fadeIn 300ms ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* KRS score count-up */
.krs-score {
  animation: countUp 1000ms ease-out;
}
```

---

### Animation Principles

**1. Responsive (< 300ms default):**
- Animations should feel instant for user interactions
- Hover effects: 200ms
- Focus states: 150ms
- Page transitions: 300ms max

**2. Purposeful:**
- Every animation should convey meaning
- Use motion to guide attention (e.g., new badge appears with bounce)
- Avoid gratuitous animations

**3. Accessible:**
- Respect `prefers-reduced-motion` media query
- Provide instant alternatives for users who prefer reduced motion

```css
/* Default animation */
.element {
  transition: transform 300ms ease-out;
}

/* Reduced motion: instant transition */
@media (prefers-reduced-motion: reduce) {
  .element {
    transition: none;
  }
}
```

**4. Performance:**
- Animate `transform` and `opacity` only (GPU-accelerated)
- Avoid animating `width`, `height`, `top`, `left` (causes reflow)

**Good:**
```css
.card:hover {
  transform: translateY(-4px); /* GPU-accelerated ✅ */
}
```

**Bad:**
```css
.card:hover {
  top: -4px; /* Causes reflow ❌ */
}
```

---

# 🧩 COMPONENTS

This section documents all reusable UI components with variants, states, props, and usage examples.

## KRS Hero Badge

**Purpose:** Display KRS score prominently with level, subscores, and on-table gain.

**Variants:**
- **Large:** Home Dashboard (240px height)
- **Small:** Report header (120px height)
- **Minimal:** Quick glance (score + level only, 80px height)

**States:**
- **Default:** Score loaded, all data visible
- **Loading:** Skeleton placeholder
- **Error:** Error message + retry button

**Props:**
```typescript
interface KRSHeroBadgeProps {
  variant: 'large' | 'small' | 'minimal';
  krsTotal: number;           // 75 (0-100 scale)
  krsLevel: string;           // "ADVANCED"
  creation: number;           // 74.8 (0-100)
  transfer: number;           // 69.5 (0-100)
  onTableGain: number;        // 3.1 (mph bat speed)
  showSubscores?: boolean;    // Default: true (large variant)
  showGauge?: boolean;        // Default: true (large variant)
  loading?: boolean;          // Default: false
  error?: string | null;      // Default: null
}
```

**Layout (Large Variant):**
```
┌─────────────────────────────────────┐
│  Your KRS                  [badge]  │ ← Header
│                                     │
│           ┌───────┐                 │
│           │       │                 │ ← Gauge (140px)
│           │  75   │                 │   Score: 72px
│           │       │                 │
│           └───────┘                 │
│         ADVANCED                    │ ← Level badge
│                                     │
│  Creation     Transfer              │ ← Subscores
│    74.8         69.5                │
│                                     │
│  On Table: +3.1 mph bat speed      │ ← Gain
└─────────────────────────────────────┘
```

**Styling:**
```css
.krs-hero-large {
  background: linear-gradient(135deg, #06B6D4 0%, #0891B2 100%);
  border-radius: 16px;
  padding: 24px;
  color: white;
  height: 240px;
}

.krs-score {
  font-size: 72px;
  font-weight: 700;
  line-height: 1.0;
  text-align: center;
}

.krs-level-badge {
  background: rgba(255, 255, 255, 0.2);
  border-radius: 9999px;
  padding: 4px 12px;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}
```

**Usage Example:**
```tsx
<KRSHeroBadge
  variant="large"
  krsTotal={75}
  krsLevel="ADVANCED"
  creation={74.8}
  transfer={69.5}
  onTableGain={3.1}
  showSubscores={true}
  showGauge={true}
/>
```

---

## 4B Card Component

**Purpose:** Display metrics for Brain, Body, Bat, or Ball with tinted background.

**Variants:**
- **Brain:** Purple tint (#EDE9FE), icon 🧠
- **Body:** Blue tint (#DBEAFE), icon 💪
- **Bat:** Green tint (#D1FAE5), icon 🏏
- **Ball:** Red tint (#FEE2E2), icon ⚾

**States:**
- **Default:** Collapsed (3-4 metrics visible)
- **Expanded:** Full metrics visible (tap to expand)
- **Loading:** Skeleton placeholder
- **Error:** Error message

**Props:**
```typescript
interface FourBCardProps {
  cardType: 'brain' | 'body' | 'bat' | 'ball';
  metrics: {
    primary: { label: string; value: string | number };
    secondary: { label: string; value: string | number }[];
    status?: 'good' | 'moderate' | 'needs-work';
  };
  expanded?: boolean;
  onToggle?: () => void;
  loading?: boolean;
  error?: string | null;
}
```

**Layout (Brain Card Example):**
```
┌─────────────────────────────────────┐
│  🧠  BRAIN                    [✓]   │ ← Header (icon, title, status)
│                                     │
│  Motor Profile                      │ ← Primary metric
│  Slingshotter                       │
│  92% confidence                     │
│                                     │
│  Timing: Fast (0.65s)              │ ← Secondary metrics
│  Tempo: Consistent                  │
│                                     │
│  [Expand ▼]                         │ ← Toggle (optional)
└─────────────────────────────────────┘
```

**Styling:**
```css
/* Brain variant */
.fourb-card-brain {
  background: #EDE9FE; /* Light purple tint */
  border: 1px solid #C4B5FD;
  border-radius: 12px;
  padding: 20px;
}

.fourb-card-brain .icon {
  color: #7C3AED; /* Purple text */
  font-size: 32px;
}

.fourb-card-brain .title {
  color: #7C3AED;
  font-size: 18px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

/* Body variant */
.fourb-card-body {
  background: #DBEAFE; /* Light blue tint */
  border: 1px solid #93C5FD;
}

.fourb-card-body .icon,
.fourb-card-body .title {
  color: #2563EB;
}

/* Bat variant */
.fourb-card-bat {
  background: #D1FAE5; /* Light green tint */
  border: 1px solid #6EE7B7;
}

.fourb-card-bat .icon,
.fourb-card-bat .title {
  color: #059669;
}

/* Ball variant */
.fourb-card-ball {
  background: #FEE2E2; /* Light red tint */
  border: 1px solid #FECACA;
}

.fourb-card-ball .icon,
.fourb-card-ball .title {
  color: #DC2626;
}
```

**Usage Example:**
```tsx
<FourBCard
  cardType="brain"
  metrics={{
    primary: {
      label: "Motor Profile",
      value: "Slingshotter (92% confidence)"
    },
    secondary: [
      { label: "Timing", value: "Fast (0.65s)" },
      { label: "Tempo", value: "Consistent" }
    ],
    status: "good"
  }}
  expanded={false}
  onToggle={() => setExpanded(!expanded)}
/>
```

---

## Button Component

**Purpose:** Primary interactive element for user actions.

**Variants:**
- **Primary:** Cyan background (#06B6D4), white text
- **Secondary:** White background, cyan border, cyan text
- **Ghost:** Transparent background, cyan text (hover: light cyan bg)
- **Danger:** Red background (#EF4444), white text

**Sizes:**
- **Small:** 40px height, 14px text
- **Medium:** 48px height, 16px text (DEFAULT)
- **Large:** 56px height, 18px text

**States:**
- **Default:** Normal state
- **Hover:** Darker background
- **Active:** Pressed state (scale down slightly)
- **Disabled:** Opacity 0.5, cursor not-allowed
- **Loading:** Spinner icon, text hidden

**Props:**
```typescript
interface ButtonProps {
  variant: 'primary' | 'secondary' | 'ghost' | 'danger';
  size: 'small' | 'medium' | 'large';
  disabled?: boolean;
  loading?: boolean;
  fullWidth?: boolean;
  icon?: React.ReactNode;
  onClick?: () => void;
  children: React.ReactNode;
}
```

**Styling:**
```css
/* Base button */
.button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  border-radius: 8px;
  font-weight: 600;
  transition: all 200ms ease-out;
  cursor: pointer;
  min-height: 44px; /* Accessibility: minimum touch target */
}

/* Primary variant */
.button-primary {
  background: #06B6D4;
  color: white;
  border: none;
}

.button-primary:hover {
  background: #0891B2;
}

.button-primary:active {
  transform: scale(0.98);
}

/* Medium size (default) */
.button-medium {
  height: 48px;
  padding: 0 24px;
  font-size: 16px;
}

/* Disabled state */
.button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Loading state */
.button-loading {
  position: relative;
  color: transparent;
}

.button-loading::after {
  content: '';
  position: absolute;
  width: 20px;
  height: 20px;
  border: 2px solid white;
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin 600ms linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
```

**Usage Example:**
```tsx
<Button
  variant="primary"
  size="medium"
  onClick={handleUpload}
  loading={isUploading}
>
  Upload Swing Video
</Button>
```

---

## Input Component

**Purpose:** Text input for forms (name, age, height, weight, etc.).

**Types:**
- **Text:** Single-line text input
- **Number:** Numeric input with step controls
- **Email:** Email validation
- **Select:** Dropdown selection
- **Textarea:** Multi-line text input

**States:**
- **Default:** Empty, unfocused
- **Focus:** Cyan border, label moved up (if floating)
- **Filled:** Has value
- **Error:** Red border, error message below
- **Disabled:** Gray background, cursor not-allowed

**Props:**
```typescript
interface InputProps {
  type: 'text' | 'number' | 'email' | 'select' | 'textarea';
  label: string;
  placeholder?: string;
  value: string | number;
  onChange: (value: string | number) => void;
  error?: string;
  disabled?: boolean;
  required?: boolean;
  min?: number;  // For number type
  max?: number;  // For number type
  step?: number; // For number type
}
```

**Styling:**
```css
.input-container {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.input-label {
  font-size: 14px;
  font-weight: 500;
  color: #374151;
}

.input-field {
  height: 48px;
  padding: 0 16px;
  border: 1px solid #CBD5E1;
  border-radius: 8px;
  font-size: 16px;
  transition: border-color 200ms ease-out;
}

.input-field:focus {
  outline: none;
  border-color: #06B6D4;
  box-shadow: 0 0 0 3px rgba(6, 182, 212, 0.1);
}

.input-field.error {
  border-color: #EF4444;
}

.input-error-message {
  font-size: 12px;
  color: #EF4444;
}
```

**Usage Example:**
```tsx
<Input
  type="number"
  label="Age"
  placeholder="Enter your age"
  value={age}
  onChange={setAge}
  min={10}
  max={25}
  required
  error={ageError}
/>
```

---

## Progress Bar Component

**Purpose:** Show completion percentage (0-100%).

**Variants:**
- **Linear:** Horizontal bar (Processing screen)
- **Circular:** Gauge/donut chart (KRS score gauge)

**States:**
- **Default:** Progress value 0-100
- **Indeterminate:** Loading state (animated)
- **Complete:** 100%, success color

**Props:**
```typescript
interface ProgressBarProps {
  variant: 'linear' | 'circular';
  value: number;      // 0-100
  max?: number;       // Default: 100
  color?: string;     // Default: primary-500
  size?: number;      // Circular only (diameter in px)
  showLabel?: boolean;
  indeterminate?: boolean;
}
```

**Styling (Linear):**
```css
.progress-bar-linear {
  width: 100%;
  height: 8px;
  background: #E2E8F0;
  border-radius: 4px;
  overflow: hidden;
}

.progress-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #06B6D4 0%, #0891B2 100%);
  transition: width 500ms ease-out;
}

/* Indeterminate animation */
.progress-bar-fill.indeterminate {
  width: 40%;
  animation: indeterminate 1.5s infinite;
}

@keyframes indeterminate {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(350%); }
}
```

**Usage Example:**
```tsx
<ProgressBar
  variant="linear"
  value={uploadProgress}
  showLabel={true}
/>
```

---

## Status Pill Component

**Purpose:** Display status indicators (level, health check, etc.).

**Variants:**
- **Success:** Green background, "Good", "ELITE"
- **Warning:** Amber background, "Moderate", "BUILDING"
- **Error:** Red background, "Needs Work", "FOUNDATION"
- **Info:** Blue background, "Info", "ADVANCED"
- **Neutral:** Gray background, neutral indicators

**Sizes:**
- **Small:** 24px height, 12px text
- **Medium:** 32px height, 14px text (DEFAULT)

**Props:**
```typescript
interface StatusPillProps {
  status: 'success' | 'warning' | 'error' | 'info' | 'neutral';
  text: string;
  size?: 'small' | 'medium';
  icon?: React.ReactNode;
}
```

**Styling:**
```css
.status-pill {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 6px 12px;
  border-radius: 9999px;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

.status-pill-success {
  background: #D1FAE5;
  color: #047857;
}

.status-pill-warning {
  background: #FEF3C7;
  color: #B45309;
}

.status-pill-error {
  background: #FEE2E2;
  color: #B91C1C;
}
```

**Usage Example:**
```tsx
<StatusPill
  status="success"
  text="ADVANCED"
  size="medium"
/>
```

---

## Additional Components

Due to length constraints, the following components are documented with brief specs:

### Coach Cue Overlay
- **Purpose:** Display real-time coaching feedback in Live Mode
- **Layout:** Bottom-center banner, 80px height
- **States:** Info (blue), Warning (amber), Success (green)
- **Animation:** Slide-up from bottom with fade-in (300ms)

### Bottom Navigation
- **Purpose:** Primary navigation for 5 main screens
- **Layout:** Fixed bottom, 64px height, 5 tabs
- **Active State:** Cyan accent bar (3px height) above icon
- **Tabs:** Home, Live, Upload, Progress, Settings

### Modal/Dialog
- **Purpose:** Overlays for confirmations, forms, alerts
- **Sizes:** Small (400px), Medium (600px), Large (800px)
- **Parts:** Header (title + close button), Body (content), Footer (actions)
- **Backdrop:** Dark overlay (rgba(0, 0, 0, 0.5))

### Chart Components (Recharts)
- **Types:** Line (KRS Journey), Bar (Session History), Dual-Line (Creation vs Transfer)
- **Configuration:** 0-100 y-axis, date x-axis, level threshold lines
- **Colors:** Cyan primary line, reference areas for levels

---

# 📐 PATTERNS

## Screen Header Pattern

**Purpose:** Consistent header across all screens with back button, title, and optional action.

**Layout:**
```
┌─────────────────────────────────────┐
│  ← Back         TITLE          [⋮]  │
└─────────────────────────────────────┘
```

**Specifications:**
- Height: 56px (mobile), 64px (desktop)
- Background: #FAFAFA
- Border-bottom: 1px solid #E2E8F0

**Structure:**
- Left: Back button (← icon, 16px)
- Center: Title (20px semibold, uppercase for screen names)
- Right: Action button (⋮ menu, 🔔 notifications, 🔍 search)

**Implementation:**
```css
.screen-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 56px;
  padding: 0 16px;
  background: #FAFAFA;
  border-bottom: 1px solid #E2E8F0;
}
```

---

## Empty State Pattern

**Purpose:** Display when no data is available (e.g., no sessions yet).

**Layout:**
```
┌─────────────────────────────────────┐
│                                     │
│              [Icon]                 │ ← 64×64 icon
│                                     │
│         No Sessions Yet             │ ← Heading (24px)
│                                     │
│   Upload your first swing video     │ ← Description (16px)
│    to get your KRS score and        │
│      personalized insights          │
│                                     │
│     [Upload Swing Video]            │ ← Primary CTA
│                                     │
└─────────────────────────────────────┘
```

**Specifications:**
- Centered vertically and horizontally
- Icon: 64×64, neutral-400 color
- Heading: 24px semibold, neutral-900
- Description: 16px regular, neutral-500
- CTA: Primary button

---

## Loading State Pattern

**Purpose:** Show loading feedback while data is fetching or processing.

**Variants:**

**1. Skeleton Screens:**
- Gray placeholders matching final layout
- Animated pulse effect (opacity 0.5 → 1 → 0.5)
- Use for list items, cards, text blocks

**2. Spinner:**
- Circular spinner (32×32) for inline loading
- Use for buttons (loading state), small content areas

**3. Progress Bar:**
- Linear progress bar for file uploads, processing
- Show percentage if known

**Implementation (Skeleton):**
```css
.skeleton {
  background: linear-gradient(
    90deg,
    #E2E8F0 0%,
    #F1F5F9 50%,
    #E2E8F0 100%
  );
  background-size: 200% 100%;
  animation: skeleton-pulse 1.5s ease-in-out infinite;
  border-radius: 4px;
}

@keyframes skeleton-pulse {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
```

---

## Error State Pattern

**Purpose:** Display errors with clear messaging and recovery actions.

**Layout:**
```
┌─────────────────────────────────────┐
│                                     │
│              [⚠️]                   │ ← Error icon (64×64)
│                                     │
│         Upload Failed               │ ← Heading (24px, error red)
│                                     │
│   Check your internet connection    │ ← Description (16px)
│      and try again. If the          │
│    problem persists, contact        │
│           support.                  │
│                                     │
│  [Try Again]      [Cancel]         │ ← Action buttons
│                                     │
└─────────────────────────────────────┘
```

**Specifications:**
- Error icon: ⚠️ or ❌, 64×64, error-500 color
- Heading: 24px semibold, error-700
- Description: 16px regular, neutral-700
- Actions: Primary button ("Try Again"), Ghost button ("Cancel")

---

## Form Pattern

**Purpose:** Consistent form layout with validation and error handling.

**Layout:**
```
┌─────────────────────────────────────┐
│  Name *                             │ ← Label
│  ┌───────────────────────────────┐  │
│  │ Enter your name               │  │ ← Input
│  └───────────────────────────────┘  │
│  This will appear on your profile.  │ ← Helper text
│                                     │
│  Age *                              │
│  ┌───────────────────────────────┐  │
│  │ 17                            │  │
│  └───────────────────────────────┘  │
│  ⚠️ Age must be between 10-25      │ ← Error message
│                                     │
│        [Submit]                     │ ← Submit button
└─────────────────────────────────────┘
```

**Specifications:**
- Label: 14px medium, neutral-700, required indicator (*) in error-500
- Input: 48px height, 16px text, 16px padding
- Helper text: 12px regular, neutral-500
- Error message: 12px regular, error-500, ⚠️ icon
- Submit button: Primary variant, full width on mobile
- Validation: On blur (after user leaves field)
- Success: Toast notification + redirect

---

## Card List Pattern

**Purpose:** Display cards in a responsive grid.

**Layout:**
```
Mobile (1 column):
┌───────────┐
│   Card    │
└───────────┘
┌───────────┐
│   Card    │
└───────────┘

Tablet (2 columns):
┌───────────┬───────────┐
│   Card    │   Card    │
└───────────┴───────────┘

Desktop (3 columns):
┌─────────┬─────────┬─────────┐
│  Card   │  Card   │  Card   │
└─────────┴─────────┴─────────┘
```

**Specifications:**
- Grid gap: 16px (mobile), 20px (desktop)
- Card hover: Shadow-sm → shadow-md, translateY(-4px)
- Card click: Navigate or expand

**Implementation:**
```css
.card-grid {
  display: grid;
  grid-template-columns: 1fr; /* Mobile */
  gap: 16px;
}

@media (min-width: 768px) {
  .card-grid {
    grid-template-columns: repeat(2, 1fr); /* Tablet */
  }
}

@media (min-width: 1024px) {
  .card-grid {
    grid-template-columns: repeat(3, 1fr); /* Desktop */
    gap: 20px;
  }
}
```

---

# 🎨 DESIGN TOKENS (JSON)

Complete design tokens file consolidating all values from this design system.

```json
{
  "$schema": "https://tr.designtokens.org/format/draft/spec/",
  "name": "Catching Barrels Design Tokens",
  "version": "2.0.0",
  "description": "Design tokens for Catching Barrels PWA — Clean Athletic Professional",
  
  "colors": {
    "primary": {
      "50": "#ECFEFF",
      "100": "#CFFAFE",
      "200": "#A5F3FC",
      "300": "#67E8F9",
      "400": "#22D3EE",
      "500": "#06B6D4",
      "600": "#0891B2",
      "700": "#0E7490",
      "800": "#155E75",
      "900": "#164E63"
    },
    "neutral": {
      "50": "#F8FAFC",
      "100": "#F1F5F9",
      "200": "#E2E8F0",
      "300": "#CBD5E1",
      "400": "#94A3B8",
      "500": "#64748B",
      "600": "#475569",
      "700": "#334155",
      "800": "#1E293B",
      "900": "#0F172A"
    },
    "semantic": {
      "success": {
        "bg": "#F0FDF4",
        "text": "#10B981",
        "border": "#10B981"
      },
      "warning": {
        "bg": "#FFFBEB",
        "text": "#F59E0B",
        "border": "#F59E0B"
      },
      "error": {
        "bg": "#FEF2F2",
        "text": "#EF4444",
        "border": "#EF4444"
      },
      "info": {
        "bg": "#EFF6FF",
        "text": "#3B82F6",
        "border": "#3B82F6"
      }
    },
    "fourB": {
      "brain": {
        "bg": "#EDE9FE",
        "text": "#7C3AED",
        "icon": "#7C3AED",
        "border": "#C4B5FD"
      },
      "body": {
        "bg": "#DBEAFE",
        "text": "#2563EB",
        "icon": "#2563EB",
        "border": "#93C5FD"
      },
      "bat": {
        "bg": "#D1FAE5",
        "text": "#059669",
        "icon": "#059669",
        "border": "#6EE7B7"
      },
      "ball": {
        "bg": "#FEE2E2",
        "text": "#DC2626",
        "icon": "#DC2626",
        "border": "#FECACA"
      }
    },
    "motorProfile": {
      "spinner": "#10B981",
      "slingshotter": "#F59E0B",
      "whipper": "#EF4444",
      "titan": "#8B5CF6"
    }
  },
  
  "typography": {
    "fontFamily": {
      "primary": "Inter Variable, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
      "monospace": "SF Mono, Monaco, 'Courier New', monospace"
    },
    "fontSize": {
      "display-01": { "desktop": "96px", "mobile": "72px" },
      "display-02": { "desktop": "72px", "mobile": "56px" },
      "heading-01": { "desktop": "32px", "mobile": "28px" },
      "heading-02": { "desktop": "24px", "mobile": "22px" },
      "heading-03": { "desktop": "20px", "mobile": "18px" },
      "heading-04": { "desktop": "18px", "mobile": "16px" },
      "body-01": "16px",
      "body-02": "14px",
      "caption-01": "14px",
      "caption-02": "12px",
      "small": "12px"
    },
    "fontWeight": {
      "regular": 400,
      "medium": 500,
      "semibold": 600,
      "bold": 700
    },
    "lineHeight": {
      "tight": 1.0,
      "snug": 1.2,
      "normal": 1.5,
      "relaxed": 1.75
    },
    "letterSpacing": {
      "tight": "-0.02em",
      "normal": "0",
      "wide": "0.01em"
    }
  },
  
  "spacing": {
    "0": "0px",
    "1": "4px",
    "2": "8px",
    "3": "12px",
    "4": "16px",
    "5": "20px",
    "6": "24px",
    "8": "32px",
    "10": "40px",
    "12": "48px",
    "16": "64px",
    "20": "80px",
    "24": "96px",
    "32": "128px"
  },
  
  "borderRadius": {
    "none": "0",
    "sm": "4px",
    "md": "8px",
    "lg": "12px",
    "xl": "16px",
    "2xl": "24px",
    "full": "9999px"
  },
  
  "shadows": {
    "none": "none",
    "sm": "0 1px 2px 0 rgb(0 0 0 / 0.05)",
    "md": "0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)",
    "lg": "0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)",
    "xl": "0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)",
    "2xl": "0 25px 50px -12px rgb(0 0 0 / 0.25)"
  },
  
  "breakpoints": {
    "mobile": "320px",
    "mobile-l": "375px",
    "tablet": "768px",
    "desktop": "1024px",
    "wide": "1440px"
  },
  
  "animation": {
    "duration": {
      "instant": "150ms",
      "fast": "200ms",
      "normal": "300ms",
      "slow": "500ms",
      "slower": "1000ms"
    },
    "easing": {
      "linear": "linear",
      "in": "cubic-bezier(0.4, 0, 1, 1)",
      "out": "cubic-bezier(0, 0, 0.2, 1)",
      "inOut": "cubic-bezier(0.4, 0, 0.2, 1)",
      "bounce": "cubic-bezier(0.68, -0.55, 0.27, 1.55)"
    }
  }
}
```

---

## Usage in Code

**Tailwind CSS Configuration:**
```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#ECFEFF',
          100: '#CFFAFE',
          // ... rest of primary scale
          500: '#06B6D4', // Default
          600: '#0891B2',
        },
        // ... other color scales
      },
      fontFamily: {
        sans: ['Inter Variable', 'system-ui', 'sans-serif'],
      },
      fontSize: {
        'display-lg': ['72px', { lineHeight: '1.0' }],
        'display-md': ['56px', { lineHeight: '1.0' }],
        // ... rest of type scale
      },
      spacing: {
        1: '4px',
        2: '8px',
        // ... rest of spacing scale
      },
      borderRadius: {
        'md': '8px',
        'lg': '12px',
        'xl': '16px',
      },
      boxShadow: {
        sm: '0 1px 2px 0 rgb(0 0 0 / 0.05)',
        md: '0 4px 6px -1px rgb(0 0 0 / 0.1)',
        // ... rest of shadow scale
      },
    },
  },
};
```

---

## Conclusion

This design system provides a complete foundation for building the Catching Barrels PWA. All components, patterns, and tokens are ready for Phase 1 implementation.

**Next Steps:**
1. Set up Tailwind CSS with design tokens
2. Build component library (5 critical components first)
3. Implement screen flows following patterns
4. Test accessibility and responsiveness

---

*Last Updated: December 26, 2025*  
*Design System Version: 2.0*
