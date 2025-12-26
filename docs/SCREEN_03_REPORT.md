# Screen 03: Report Screen

**Last Updated:** Dec 26, 2025  
**Status:** ✅ COMPLETE  
**Designer:** Builder 2  
**Phase:** Phase 0 - Design (Day 2)

---

## 📋 Overview

The Report screen displays a comprehensive player analysis after video processing. It features:
- **KRS Hero Section** with circular gauge
- **4B Framework Cards** (Brain, Body, Bat, Ball) with tinted backgrounds
- **11-Section Breakdown** with expandable details
- **Coach Rick Messages** with actionable insights

**User Flow:**
Upload → Processing → **Report** → Drills (optional)

---

## 🎨 Visual Hierarchy

### Priority Levels
1. **KRS Hero** - Primary focus, top of screen
2. **4B Cards** - Secondary focus, grid layout
3. **Section Breakdown** - Tertiary, scrollable list
4. **Actions** - Bottom sticky CTA

---

## 📐 Layout Structure

```
┌─────────────────────────────────────┐
│  Header                              │
│  "Your Swing Report"                 │
│  Player Name · Session Date          │
├─────────────────────────────────────┤
│                                      │
│  ┌───────────────────────────────┐  │
│  │   KRS HERO CARD               │  │
│  │   Circular Gauge · Score      │  │
│  │   ADVANCED                    │  │
│  │   Progress to ELITE           │  │
│  └───────────────────────────────┘  │
│                                      │
│  ┌─────────┐ ┌─────────┐           │
│  │ BRAIN   │ │ BODY    │           │
│  │ 88%     │ │ 82/50   │           │
│  └─────────┘ └─────────┘           │
│  ┌─────────┐ ┌─────────┐           │
│  │ BAT     │ │ BALL    │           │
│  │ 78/50   │ │ 75→85   │           │
│  └─────────┘ └─────────┘           │
│                                      │
│  11-Section Breakdown                │
│  ┌───────────────────────────────┐  │
│  │ 1. Brain (Motor Profile)      │  │
│  │ > Spinner · 88% confidence    │  │
│  └───────────────────────────────┘  │
│  ┌───────────────────────────────┐  │
│  │ 2. Body (Creation)            │  │
│  │ > Score: 82 · Good            │  │
│  └───────────────────────────────┘  │
│  [... 9 more sections ...]          │
│                                      │
│  [View Training Plan Button]        │
│                                      │
└─────────────────────────────────────┘
   Bottom Navigation (sticky)
```

---

## 🎯 Component Specifications

### 1. KRS Hero Card

**Dimensions:**
- Width: 100% (max 800px)
- Height: Auto (~300px)
- Padding: 32px
- Border radius: 24px

**Background:**
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

**Content:**
```
KRS Score: 80
Level: ADVANCED
Progress Bar: 80/90 (10 points to ELITE)
Creation: 82 (+2 from last)
Transfer: 78 (-1 from last)
```

**Typography:**
- Score: 72px bold, white
- Level: 24px semibold, white 80%
- Labels: 14px medium, white 70%
- Values: 20px semibold, white

**Interactive:**
- Tap to expand full KRS breakdown
- Smooth 300ms transition

---

### 2. 4B Framework Cards

**Grid Layout:**
```css
display: grid;
grid-template-columns: repeat(2, 1fr);
gap: 16px;
margin: 24px 0;
```

**Individual Card:**
- Aspect ratio: 1:1.2
- Border radius: 16px
- Padding: 20px
- Box shadow: 0 2px 8px rgba(0,0,0,0.04)

**Card Colors:**
```css
/* Brain Card */
background: linear-gradient(135deg, #10b981 0%, rgba(16, 185, 129, 0.1) 100%);
border-left: 4px solid #10b981;

/* Body Card */
background: linear-gradient(135deg, #3b82f6 0%, rgba(59, 130, 246, 0.1) 100%);
border-left: 4px solid #3b82f6;

/* Bat Card */
background: linear-gradient(135deg, #f59e0b 0%, rgba(245, 158, 11, 0.1) 100%);
border-left: 4px solid #f59e0b;

/* Ball Card */
background: linear-gradient(135deg, #ef4444 0%, rgba(239, 68, 68, 0.1) 100%);
border-left: 4px solid #ef4444;
```

**Content Structure:**
```
Icon (24×24)
Label (12px uppercase, 60% opacity)
Primary Metric (32px bold)
Secondary Metric (16px regular)
Progress Bar (optional, 4px height)
Status Badge (12px, rounded)
```

**Example: BRAIN Card**
```
🧠 Icon
BRAIN
Spinner
88% confidence
[Status: ELITE badge, green]
```

**Example: BODY Card**
```
💪 Icon
BODY
82/50
Creation Score
[Progress bar: 82/100]
[Status: GOOD badge, blue]
```

---

### 3. Section Breakdown List

**Container:**
```css
margin-top: 32px;
display: flex;
flex-direction: column;
gap: 12px;
```

**Section Card:**
```css
background: white;
border: 1px solid #e5e7eb;
border-radius: 12px;
padding: 20px;
cursor: pointer;
transition: all 200ms ease;

&:hover {
  border-color: #06b6d4;
  box-shadow: 0 4px 12px rgba(6, 182, 212, 0.1);
}
```

**Header Row:**
```
┌────────────────────────────────────┐
│ [Icon] Section Name       [Arrow]  │
│        Status Badge                │
└────────────────────────────────────┘
```

**Typography:**
- Section number: 16px bold, #06b6d4
- Section name: 18px semibold, #111827
- Status badge: 12px medium, colored
- Summary: 14px regular, #6b7280

**Expanded State:**
```
┌────────────────────────────────────┐
│ [Icon] Section Name       [Arrow↓] │
│        Status Badge                │
├────────────────────────────────────┤
│ Key Metrics:                       │
│ • Metric 1: Value                  │
│ • Metric 2: Value                  │
│ • Metric 3: Value                  │
│                                    │
│ Insights:                          │
│ "Detailed analysis text..."        │
│                                    │
│ [View Full Details →]              │
└────────────────────────────────────┘
```

---

### 4. Sticky CTA Button

**Position:**
```css
position: sticky;
bottom: 80px; /* above bottom nav */
left: 16px;
right: 16px;
z-index: 10;
```

**Button Style:**
```css
width: calc(100% - 32px);
max-width: 400px;
margin: 0 auto;
height: 56px;
background: #06b6d4;
color: white;
border-radius: 16px;
font-size: 16px;
font-weight: 600;
box-shadow: 0 4px 20px rgba(6, 182, 212, 0.3);
```

**States:**
- Default: Primary blue
- Hover: Darken 10%
- Active: Scale 0.98
- Disabled: 40% opacity

**Text:**
- Primary CTA: "View Training Plan"
- Secondary: "Share Report" (ghost style)

---

## 📱 Responsive Behavior

### Mobile (375px)
- KRS Hero: Full width, 300px height
- 4B Cards: 2×2 grid, equal height
- Section list: Single column, 16px padding
- Sticky CTA: 16px margin, full width

### Tablet (768px)
- KRS Hero: Max 600px centered
- 4B Cards: 2×2 grid, larger cards
- Section list: Max 700px centered
- Sticky CTA: Max 400px centered

### Desktop (1024px+)
- KRS Hero: Max 800px centered
- 4B Cards: 4 in a row (optional)
- Section list: Max 800px centered
- Sticky CTA: Max 400px centered

---

## 🎬 Animations & Transitions

### Page Load
```css
/* Fade in from bottom */
@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.report-section {
  animation: slideUp 300ms ease-out;
  animation-fill-mode: both;
}

/* Stagger children */
.report-section:nth-child(1) { animation-delay: 0ms; }
.report-section:nth-child(2) { animation-delay: 50ms; }
.report-section:nth-child(3) { animation-delay: 100ms; }
```

### KRS Gauge Fill
```css
@keyframes gaugeFill {
  from {
    stroke-dashoffset: 283; /* full circumference */
  }
  to {
    stroke-dashoffset: calc(283 * (1 - var(--score) / 100));
  }
}

.gauge-progress {
  animation: gaugeFill 1000ms ease-out 300ms both;
}
```

### Section Expand
```css
.section-details {
  max-height: 0;
  overflow: hidden;
  transition: max-height 300ms ease;
}

.section-details.expanded {
  max-height: 500px;
}
```

### 4B Card Hover
```css
.four-b-card {
  transition: all 200ms ease;
}

.four-b-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
}
```

---

## 🎨 Color System

### KRS Hero
```css
--krs-gradient-start: #667eea;
--krs-gradient-end: #764ba2;
--krs-text-primary: #ffffff;
--krs-text-secondary: rgba(255, 255, 255, 0.8);
--krs-accent: #fbbf24;
```

### 4B Cards
```css
--brain-primary: #10b981;
--brain-bg: rgba(16, 185, 129, 0.08);

--body-primary: #3b82f6;
--body-bg: rgba(59, 130, 246, 0.08);

--bat-primary: #f59e0b;
--bat-bg: rgba(245, 158, 11, 0.08);

--ball-primary: #ef4444;
--ball-bg: rgba(239, 68, 68, 0.08);
```

### Status Badges
```css
--status-elite: #10b981;
--status-good: #3b82f6;
--status-needs-work: #f59e0b;
--status-critical: #ef4444;
```

---

## 🔢 Data Display Rules

### Score Formatting
```javascript
// KRS Total Score
const formatKRS = (score) => {
  return Math.round(score * 10) / 10; // 79.9
};

// Percentage
const formatPercent = (value) => {
  return `${Math.round(value)}%`; // 88%
};

// Ratio
const formatRatio = (current, max) => {
  return `${current}/${max}`; // 82/50
};

// Velocity
const formatVelocity = (value) => {
  return `${Math.round(value)} mph`; // 75 mph
};

// Change Indicator
const formatChange = (change) => {
  if (change > 0) return `+${change}`;
  if (change < 0) return `${change}`;
  return '—';
};
```

### Status Determination
```javascript
const getStatus = (score) => {
  if (score >= 85) return 'ELITE';
  if (score >= 70) return 'GOOD';
  if (score >= 50) return 'NEEDS_WORK';
  return 'CRITICAL';
};

const getStatusColor = (status) => {
  return {
    'ELITE': '#10b981',
    'GOOD': '#3b82f6',
    'NEEDS_WORK': '#f59e0b',
    'CRITICAL': '#ef4444'
  }[status];
};
```

---

## ♿ Accessibility

### Semantic HTML
```html
<main role="main" aria-label="Player Report">
  <section aria-labelledby="krs-heading">
    <h2 id="krs-heading">KRS Score</h2>
    <!-- KRS Hero content -->
  </section>
  
  <section aria-labelledby="framework-heading">
    <h2 id="framework-heading">4B Framework</h2>
    <div role="list">
      <article role="listitem" aria-label="Brain Score">
        <!-- Brain card -->
      </article>
      <!-- ... other cards -->
    </div>
  </section>
  
  <section aria-labelledby="breakdown-heading">
    <h2 id="breakdown-heading">Complete Analysis</h2>
    <!-- Section list -->
  </section>
</main>
```

### Screen Reader Support
```html
<!-- KRS Gauge -->
<div role="img" aria-label="KRS Score: 80 out of 100, Advanced level">
  <svg><!-- gauge visual --></svg>
</div>

<!-- Progress Bars -->
<div role="progressbar" 
     aria-valuenow="82" 
     aria-valuemin="0" 
     aria-valuemax="100"
     aria-label="Body creation score">
  <div class="progress-fill"></div>
</div>

<!-- Expandable Sections -->
<button aria-expanded="false" 
        aria-controls="section-brain-details">
  Brain (Motor Profile)
</button>
<div id="section-brain-details" hidden>
  <!-- Details content -->
</div>
```

### Keyboard Navigation
- Tab order: Header → KRS Hero → 4B Cards → Sections → CTA
- Enter/Space: Expand/collapse sections
- Esc: Collapse all sections
- Arrow keys: Navigate between 4B cards

---

## 📊 Data Schema Integration

### PlayerReport API Response
```typescript
interface PlayerReport {
  session_id: string;
  player_info: {
    player_id: string;
    name: string;
    age: number;
    height_inches: number;
    weight_lbs: number;
  };
  krs: {
    total: number;
    level: 'BEGINNER' | 'INTERMEDIATE' | 'ADVANCED' | 'ELITE';
    creation_score: number;
    transfer_score: number;
    creation_change?: number;
    transfer_change?: number;
  };
  brain: {
    motor_profile: {
      primary: string;
      confidence: number;
      display_name: string;
      tagline: string;
      color: string;
    };
    timing: {
      tempo_rating: string;
    };
  };
  body: {
    creation_score: number;
    capacity: {
      estimated_bat_speed_mph: number;
    };
    ground_flow: {
      score: number;
    };
    engine_flow: {
      score: number;
    };
  };
  bat: {
    transfer_score: number;
    flow: {
      you_create_mph: number;
      you_transfer_mph: number;
    };
  };
  ball: {
    exit_velocity: {
      bat_speed_mph: number;
      exit_velo_mph: number;
    };
  };
  // ... additional sections
}
```

### Mapping to UI
```javascript
// KRS Hero
<KRSHero
  score={report.krs.total}
  level={report.krs.level}
  creation={report.krs.creation_score}
  transfer={report.krs.transfer_score}
  creationChange={report.krs.creation_change}
  transferChange={report.krs.transfer_change}
/>

// 4B Cards
<BrainCard
  motorProfile={report.brain.motor_profile.primary}
  confidence={report.brain.motor_profile.confidence}
  displayName={report.brain.motor_profile.display_name}
  color={report.brain.motor_profile.color}
/>

<BodyCard
  score={report.body.creation_score}
  capacity={report.body.capacity.estimated_bat_speed_mph}
  groundFlow={report.body.ground_flow.score}
  engineFlow={report.body.engine_flow.score}
/>

<BatCard
  score={report.bat.transfer_score}
  created={report.bat.flow.you_create_mph}
  transferred={report.bat.flow.you_transfer_mph}
/>

<BallCard
  batSpeed={report.ball.exit_velocity.bat_speed_mph}
  exitVelo={report.ball.exit_velocity.exit_velo_mph}
/>
```

---

## 🎯 Success Metrics

### Performance
- Initial render: <200ms
- KRS gauge animation: 1000ms
- Section expand: <300ms
- Smooth 60fps scrolling

### User Engagement
- Time on Report: >2 minutes
- Section expansions: ≥3 per session
- CTA clicks: >40%
- Share rate: >15%

### Accessibility
- Lighthouse Accessibility: >95
- Keyboard navigable: ✅
- Screen reader compatible: ✅
- Color contrast: AAA

---

## 🚀 Implementation Priority

1. **Phase 1: Core Structure**
   - Layout scaffold
   - KRS Hero card
   - 4B card grid
   - Section list

2. **Phase 2: Interactions**
   - Section expand/collapse
   - KRS gauge animation
   - Progress bar fills
   - Hover states

3. **Phase 3: Data Integration**
   - API connection
   - Data mapping
   - Error states
   - Loading states

4. **Phase 4: Polish**
   - Micro-interactions
   - Stagger animations
   - Share functionality
   - Analytics tracking

---

## 📝 Implementation Notes

### Component Hierarchy
```
<ReportScreen>
  <ReportHeader />
  <KRSHeroCard />
  <FourBFramework>
    <BrainCard />
    <BodyCard />
    <BatCard />
    <BallCard />
  </FourBFramework>
  <SectionBreakdown>
    <SectionCard /> × 11
  </SectionBreakdown>
  <StickyCTA />
  <BottomNav />
</ReportScreen>
```

### State Management
```javascript
const [report, setReport] = useState(null);
const [expandedSections, setExpandedSections] = useState([]);
const [loading, setLoading] = useState(true);
const [error, setError] = useState(null);
```

### Error Handling
- Network error: Retry button
- Invalid session: Redirect to upload
- Missing data: Show defaults with warning
- Timeout: Show partial report with notice

---

## ✅ Definition of Done

- [ ] KRS Hero displays correctly with animation
- [ ] 4B cards render with proper colors/data
- [ ] 11 sections expandable/collapsible
- [ ] Responsive on 375px, 768px, 1024px
- [ ] Smooth animations (60fps)
- [ ] Keyboard accessible
- [ ] Screen reader tested
- [ ] Error states handled
- [ ] Loading states implemented
- [ ] CTA button sticky and functional
- [ ] Share functionality working

---

**Next Steps:**
1. Create Figma mockup with all specifications
2. Export design tokens for KRS Hero & 4B cards
3. Build interactive prototype for user testing
4. Handoff to development with component specs

---

**Status:** ✅ SPECIFICATION COMPLETE  
**Ready for:** Figma Design Phase  
**Review Date:** Friday 4pm
