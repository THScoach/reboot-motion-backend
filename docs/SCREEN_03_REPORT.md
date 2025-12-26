# Screen 03: Report (Player Report)

**Screen Name**: Player Report  
**Route**: `/report/[sessionId]`  
**Complexity**: HIGH (Most complex screen - 11 sections)  
**Priority**: P0 (Critical Path)

---

## 📐 Layout Overview

```
┌─────────────────────────────────────┐
│  ← Back                    Share 🔗 │ ← Header
├─────────────────────────────────────┤
│                                     │
│  ┌─────────────────────────────┐   │
│  │   KRS HERO CARD             │   │ ← Section 1: KRS Hero
│  │   [Circular Gauge 80]       │   │
│  │   ADVANCED                  │   │
│  └─────────────────────────────┘   │
│                                     │
│  🎯 The 4B Framework               │ ← Section Header
│  ┌──────┬──────┬──────┬──────┐    │
│  │BRAIN │ BODY │ BAT  │ BALL │    │ ← Section 2-5: 4B Cards
│  └──────┴──────┴──────┴──────┘    │
│                                     │
│  🎯 Quick Wins                     │ ← Section 6: Wins
│  [Actionable insights cards]       │
│                                     │
│  🎯 Your Mission                   │ ← Section 7: Mission
│  [Phase-specific goals]            │
│                                     │
│  💪 Drill Library                  │ ← Section 8: Drills
│  [Personalized drill cards]        │
│                                     │
│  📊 Your Progress                  │ ← Section 9: Progress
│  [Week streak, total swings]       │
│                                     │
│  🎙️ Coach Rick Says               │ ← Section 10: Coach Rick
│  [Motivational message]            │
│                                     │
│  🚩 Flags & Insights              │ ← Section 11: Flags
│  [Special insights, paradoxes]     │
│                                     │
└─────────────────────────────────────┘
```

---

## 🎨 Section Breakdown

### Section 1: KRS Hero Card
**Component**: `KRSHeroCard`  
**Height**: 240px  
**Background**: Purple gradient (`gradient-primary`)

```
┌─────────────────────────────────────┐
│  Kinetic Readiness Score (KRS)     │ ← Caption-01 • Gray-300
│                                     │
│        ┌───────────────┐           │
│        │   Circular    │           │
│        │   Gauge       │           │ ← 140px diameter
│        │      80       │           │   Electric Cyan ring
│        │  ADVANCED     │           │
│        └───────────────┘           │
│                                     │
│  ┌──────────────┬──────────────┐   │
│  │ Creation: 82 │ Transfer: 78 │   │ ← Split metrics
│  │   +2 ↑       │   +1 ↑       │   │   Green arrows
│  └──────────────┴──────────────┘   │
│                                     │
│  10 points to ELITE                │ ← Progress indicator
│  ■■■■■■■■■□ 89%                    │
└─────────────────────────────────────┘
```

**Details**:
- Circular gauge: 140px diameter
- Electric Cyan ring (#06B6D4) with opacity gradient
- Score: Display-02 (96px bold)
- Level: Heading-02 (24px medium)
- Metrics: split 2-column layout
- Change indicators: +2 ↑ in success-green
- Progress bar: 8px height, rounded

---

### Section 2-5: 4B Framework Cards
**Component**: `FourBGrid`  
**Layout**: 4 columns on desktop, 2 on tablet, 1 on mobile

#### Brain Card
```
┌─────────────────────────┐
│ 🧠 BRAIN               │ ← Heading-03 • Brand Cyan
│ Motor & Timing         │ ← Caption-01 • Gray-400
├─────────────────────────┤
│                         │
│ THE SPINNER            │ ← Heading-04 • Gray-900
│ Quick hands, short path│ ← Body-02 • Gray-500
│                         │
│ Confidence: 88%        │ ← Body-02 with progress bar
│ ■■■■■■■■■□             │   8px height
│                         │
│ Tempo: FAST (3.2:1)    │ ← Metric badge
│ Status: ⭐ ELITE       │ ← Status badge green
└─────────────────────────┘
```

**Tint**: Soft cyan background (#06B6D4 at 5% opacity)

#### Body Card
```
┌─────────────────────────┐
│ 💪 BODY                │ ← Heading-03 • Success Green
│ Power Creation         │ ← Caption-01 • Gray-400
├─────────────────────────┤
│                         │
│ Creation Score: 82/100 │ ← Heading-04 • Gray-900
│ ■■■■■■■■□□             │   Progress bar
│                         │
│ ⚡ Capacity             │
│   150 KE (75 mph)      │ ← Body-02 • Gray-700
│                         │
│ 📊 On Table            │
│   Gap: +30 KE          │ ← Body-02 • Gray-700
│                         │
│ Ground Flow: 7.5/10    │ ← Metric with badge
│ Status: ✓ GOOD         │
└─────────────────────────┘
```

**Tint**: Soft green background (#10B981 at 5% opacity)

#### Bat Card
```
┌─────────────────────────┐
│ ⚾ BAT                  │ ← Heading-03 • Warning Orange
│ Power Transfer         │ ← Caption-01 • Gray-400
├─────────────────────────┤
│                         │
│ Transfer Score: 78/100 │ ← Heading-04 • Gray-900
│ ■■■■■■■■□□             │   Progress bar
│                         │
│ You Create: 75.6 mph   │ ← Body-02 • Gray-700
│ You Transfer: 58.9 mph │
│ Efficiency: 77.9%      │
│                         │
│ Weapon Path: ELITE     │ ← Status badge green
│ Kinetic Chain: GOOD    │ ← Status badge amber
└─────────────────────────┘
```

**Tint**: Soft orange background (#FF6B35 at 5% opacity)

#### Ball Card
```
┌─────────────────────────┐
│ ⚡ BALL                 │ ← Heading-03 • Electric Cyan
│ Exit Outcomes          │ ← Caption-01 • Gray-400
├─────────────────────────┤
│                         │
│ Bat Speed: 75 mph      │ ← Heading-04 • Gray-900
│ Exit Velo: 85 mph      │
│                         │
│ 📊 MLB Comparison      │
│   Bat Speed: 50th %ile │ ← Body-02 • Gray-700
│   Exit Velo: 45th %ile │
│                         │
│ Status: ✓ GOOD         │ ← Status badge amber
└─────────────────────────┘
```

**Tint**: Soft cyan background (#06B6D4 at 5% opacity)

---

### Section 6: Quick Wins
**Component**: `QuickWinsSection`  
**Layout**: Vertical stack of action cards

```
┌─────────────────────────────────────┐
│  🎯 Quick Wins                     │ ← Heading-02
│  Top 3 things to work on today     │ ← Body-02 • Gray-500
│                                     │
│  ┌─────────────────────────────┐   │
│  │ 1. Improve Ground Contact   │   │ ← Action card
│  │    +5 points to Creation    │   │
│  │    [View Drills →]          │   │
│  └─────────────────────────────┘   │
│                                     │
│  ┌─────────────────────────────┐   │
│  │ 2. Optimize Kinetic Chain   │   │
│  │    +3 points to Transfer    │   │
│  │    [View Drills →]          │   │
│  └─────────────────────────────┘   │
│                                     │
│  ┌─────────────────────────────┐   │
│  │ 3. Maintain Tempo Control   │   │
│  │    Lock in Fast tempo       │   │
│  │    [View Drills →]          │   │
│  └─────────────────────────────┘   │
└─────────────────────────────────────┘
```

**Card Specs**:
- White background with shadow-01
- Left border: 4px solid Electric Cyan
- Padding: 16px
- Gap between cards: 12px

---

### Section 7: Your Mission
**Component**: `MissionSection`  
**Layout**: Single card with progress tracking

```
┌─────────────────────────────────────┐
│  🎯 Your Mission                   │ ← Heading-02
│  Phase 1: Foundation Building      │ ← Body-02 • Gray-500
│                                     │
│  ┌─────────────────────────────┐   │
│  │                             │   │
│  │  Current Phase: FOUNDATION  │   │ ← Heading-03
│  │  40 swings remaining        │   │ ← Body-02
│  │                             │   │
│  │  ■■■■■□□□□□ 20%            │   │ ← Progress bar
│  │                             │   │
│  │  📊 Goals:                  │   │
│  │  • 50 total swings          │   │
│  │  • Establish motor profile  │   │
│  │  • Unlock detailed report   │   │
│  │                             │   │
│  │  [Continue Training →]      │   │ ← Primary button
│  └─────────────────────────────┘   │
└─────────────────────────────────────┘
```

---

### Section 8: Drill Library
**Component**: `DrillLibrarySection`  
**Layout**: Horizontal scroll (mobile), grid (desktop)

```
┌─────────────────────────────────────┐
│  💪 Drill Library                  │ ← Heading-02
│  Personalized for your profile     │ ← Body-02 • Gray-500
│                                     │
│  ┌──────┐ ┌──────┐ ┌──────┐       │
│  │Drill │ │Drill │ │Drill │       │ ← Drill cards
│  │  1   │ │  2   │ │  3   │       │   160px × 200px
│  │      │ │      │ │      │       │
│  │[View]│ │[View]│ │[View]│       │
│  └──────┘ └──────┘ └──────┘       │
└─────────────────────────────────────┘
```

**Drill Card Specs**:
- 160px × 200px
- White background with shadow-01
- Thumbnail: 160px × 100px (16:10)
- Title: Body-01 semibold
- Duration: Caption-01
- Difficulty badge: Caption-01 in pill

---

### Section 9: Your Progress
**Component**: `ProgressSection`  
**Layout**: Stats grid

```
┌─────────────────────────────────────┐
│  📊 Your Progress                  │ ← Heading-02
│  Keep the momentum going           │ ← Body-02 • Gray-500
│                                     │
│  ┌──────────┬──────────┬──────────┐│
│  │   10     │    1     │    0     ││ ← Stats grid
│  │  swings  │   week   │   days   ││   3 columns
│  │  total   │  streak  │   since  ││
│  └──────────┴──────────┴──────────┘│
│                                     │
│  Week 1: ●●●○○○○                   │ ← Week dots
│  Last swing: 2 hours ago           │ ← Timestamp
└─────────────────────────────────────┘
```

---

### Section 10: Coach Rick Says
**Component**: `CoachRickSection`  
**Layout**: Message card with avatar

```
┌─────────────────────────────────────┐
│  🎙️ Coach Rick Says               │ ← Heading-02
│                                     │
│  ┌─────────────────────────────┐   │
│  │  [👤 Avatar]                │   │ ← 48px avatar
│  │                             │   │
│  │  "Great work today! Your    │   │ ← Body-01
│  │   tempo control is locked   │   │   Message text
│  │   in. Focus on maintaining  │   │
│  │   that ground connection."  │   │
│  │                             │   │
│  │  - Coach Rick              │   │ ← Caption-01 • Gray-400
│  └─────────────────────────────┘   │
└─────────────────────────────────────┘
```

**Card Specs**:
- Light cyan background (#06B6D4 at 3% opacity)
- Left border: 4px solid Electric Cyan
- Avatar: 48px circle
- Padding: 20px

---

### Section 11: Flags & Insights
**Component**: `FlagsSection`  
**Layout**: Vertical stack of insight cards

```
┌─────────────────────────────────────┐
│  🚩 Flags & Special Insights       │ ← Heading-02
│                                     │
│  ┌─────────────────────────────┐   │
│  │ ⚠️ Power Paradox Detected   │   │ ← Warning card
│  │                             │   │
│  │ You're creating 150 KE but  │   │ ← Body-02
│  │ only using 120 KE. Focus on │   │
│  │ transfer efficiency.        │   │
│  │                             │   │
│  │ Potential gain: +5 mph EV   │   │ ← Highlight
│  └─────────────────────────────┘   │
│                                     │
│  ┌─────────────────────────────┐   │
│  │ ✨ Special Insight          │   │ ← Info card
│  │                             │   │
│  │ Your Fast tempo puts you in │   │
│  │ the top 20% of players.     │   │
│  │ Elite comp: Teoscar, JRod.  │   │
│  └─────────────────────────────┘   │
└─────────────────────────────────────┘
```

**Card Types**:
- Warning: Amber background, amber left border
- Info: Cyan background, cyan left border
- Success: Green background, green left border

---

## 🎨 Visual Specifications

### Colors
- **Background**: Gray-50 (#FAFAFA)
- **Cards**: White (#FFFFFF) with shadow-01
- **Primary**: Electric Cyan (#06B6D4)
- **Section headers**: Gray-900 (#111827)

### Spacing
- **Section gap**: 32px
- **Card gap**: 16px
- **Card padding**: 20px
- **Grid gap**: 12px

### Shadows
- **Cards**: `shadow-01` (0 1px 3px rgba(0,0,0,0.1))
- **Elevated**: `shadow-02` (0 4px 6px rgba(0,0,0,0.1))

### Border Radius
- **Cards**: 12px
- **Badges**: 6px
- **Buttons**: 8px

---

## 📱 Responsive Behavior

### Desktop (1024px+)
- 4B Grid: 4 columns (1fr 1fr 1fr 1fr)
- Drill Library: 4 columns
- Stats Grid: 3 columns
- Max width: 1200px centered

### Tablet (768px - 1023px)
- 4B Grid: 2 columns (1fr 1fr)
- Drill Library: 3 columns
- Stats Grid: 3 columns
- Max width: 768px

### Mobile (< 768px)
- 4B Grid: 1 column (stack)
- Drill Library: Horizontal scroll
- Stats Grid: 3 columns (compact)
- Full width with 16px padding

---

## 🔄 Interactions

### Scroll Behavior
- **Sticky header**: Back button and Share remain visible
- **Lazy load**: Sections load as user scrolls
- **Scroll to top**: FAB appears after 500px scroll

### Actions
- **Share button**: Opens native share sheet
- **Drill cards**: Navigate to drill detail page
- **View Drills CTA**: Navigate to drills library filtered by recommendation
- **Continue Training**: Navigate to Live Mode or Upload

### Loading States
- **Initial load**: Skeleton for all sections
- **Section load**: Individual skeletons per section
- **Error state**: Retry button per section

---

## ♿ Accessibility

### Focus Management
- **Skip to content**: Jump to first section
- **Section navigation**: Jump links to each section
- **Keyboard nav**: Tab through all interactive elements

### Screen Reader
- **Section landmarks**: `<section>` with `aria-label`
- **Heading hierarchy**: H1 (page title) → H2 (sections) → H3 (subsections)
- **Progress bars**: `aria-valuenow`, `aria-valuemin`, `aria-valuemax`
- **Status badges**: `aria-label` with full status text

### Visual
- **Contrast**: All text meets WCAG AA (4.5:1)
- **Focus visible**: 2px Electric Cyan outline
- **Color not sole indicator**: Icons + text for status

---

## 📊 Data Requirements

### API Endpoint
```
GET /api/sessions/{sessionId}/report
```

### Response Schema
```typescript
interface PlayerReport {
  session_id: string;
  player_info: PlayerInfo;
  progress: Progress;
  krs: KRSScore;
  brain: Brain;
  body: Body;
  bat: Bat;
  ball: Ball;
  wins: QuickWin[];
  mission: Mission;
  drills: Drill[];
  coach_rick: CoachMessage;
  flags: Flags;
}
```

---

## 🎯 Success Metrics

### Performance
- **Initial load**: < 2s
- **Section render**: < 100ms per section
- **Smooth scroll**: 60 FPS

### User Engagement
- **Time on page**: > 2 minutes
- **Scroll depth**: > 70%
- **CTA clicks**: > 40% (View Drills, Continue Training)

---

## 🚀 Implementation Notes

### Component Hierarchy
```
ReportPage
├── ReportHeader
├── KRSHeroCard
├── FourBGrid
│   ├── BrainCard
│   ├── BodyCard
│   ├── BatCard
│   └── BallCard
├── QuickWinsSection
├── MissionSection
├── DrillLibrarySection
├── ProgressSection
├── CoachRickSection
└── FlagsSection
```

### State Management
- **Zustand store**: `useReportStore`
- **API call**: `fetchPlayerReport(sessionId)`
- **Caching**: Cache report for 5 minutes
- **Optimistic updates**: Show cached data while fetching

### Performance Optimizations
- **Lazy load images**: Use `next/image` with `loading="lazy"`
- **Virtual scroll**: For drill library (if > 20 drills)
- **Code splitting**: Lazy load non-critical sections
- **Memoization**: Memoize expensive calculations (KRS gauge)

---

## 📝 Notes for Builder 2

1. **4B Cards**: Already implemented in `/templates/coach_rick_analysis.html`. Copy HTML structure and adapt to React/Next.js components.

2. **KRS Circular Gauge**: Existing implementation uses SVG. Consider using canvas for 60 FPS animation.

3. **Data Transformer**: `/app/services/data_transformer.py` transforms Coach Rick API response to PlayerReport schema. Frontend should expect this exact structure.

4. **Mobile-first**: Design starts with mobile (375px), then scales up. Test on iPhone SE (375×667) and iPhone 14 Pro (393×852).

5. **Accessibility**: This is the most complex screen. Ensure all sections have proper landmarks and headings.

6. **Error Handling**: If API call fails, show error state per section (not full page error). Allow retry per section.

---

## ✅ Definition of Done

- [ ] All 11 sections render correctly
- [ ] 4B cards match design system colors and spacing
- [ ] Responsive behavior works on mobile, tablet, desktop
- [ ] KRS circular gauge animates smoothly (60 FPS)
- [ ] All interactive elements keyboard accessible
- [ ] Loading states for all sections
- [ ] Error states with retry functionality
- [ ] Share button opens native share sheet
- [ ] Drill cards navigate to drill detail
- [ ] CTAs navigate to correct pages
- [ ] Lighthouse score > 90
- [ ] No console errors or warnings

---

**Priority**: P0 (Critical Path)  
**Complexity**: HIGH (Most complex screen)  
**Estimated Dev Time**: 12-16 hours (Phase 1)

**Dependencies**:
- Design System components
- API integration (PlayerReport endpoint)
- Supabase session storage
- Backend data transformer

---

*Last Updated: December 26, 2025*  
*Screen Specification v1.0*
