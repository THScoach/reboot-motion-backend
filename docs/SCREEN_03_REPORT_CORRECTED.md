# Screen 03: Report (Player Report) - CORRECTED VERSION

**Screen Name**: Player Report  
**Route**: `/report/[sessionId]`  
**Complexity**: HIGH (Most complex screen - 11 sections)  
**Priority**: P0 (Critical Path)

**⚠️ CRITICAL CORRECTIONS APPLIED:**
- KRS scale: 0-100 (NOT 0-1000)
- KRS levels: FOUNDATION/BUILDING/DEVELOPING/ADVANCED/ELITE
- 4B Framework: Brain (Motor Profile), Body (Creation), Bat (Transfer), Ball (Outcomes)
- All metrics verified against product specification

---

## 📐 Layout Overview

```
┌─────────────────────────────────────┐
│  ← Back                    Share 🔗 │ ← Header
├─────────────────────────────────────┤
│                                     │
│  ┌─────────────────────────────┐   │
│  │   KRS HERO CARD             │   │ ← Section 1: KRS Hero
│  │   [Score: 75]               │   │   0-100 scale
│  │   ADVANCED                  │   │   5 levels
│  └─────────────────────────────┘   │
│                                     │
│  🎯 The 4B Framework               │ ← Section Header
│  ┌──────┬──────┬──────┬──────┐    │
│  │BRAIN │ BODY │ BAT  │ BALL │    │ ← Section 2-5: 4B Cards
│  └──────┴──────┴──────┴──────┘    │   Corrected metrics
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

## 🎨 Section 1: KRS Hero Card ✅ CORRECTED

**Component**: `KRSHeroCard`  
**Height**: 280px (increased from 240px)  
**Background**: Gradient (Electric Cyan to Purple)

```
┌─────────────────────────────────────────┐
│  Kinetic Readiness Score (KRS)         │ ← Caption-01 • White/80%
│                                         │
│             75                          │ ← KRS Score
│        Your KRS Total                   │   72px bold (96px desktop)
│                                         │   White text
│          ADVANCED                       │ ← Level badge
│                                         │   24px medium
│  ┌─────────────────────────────────┐   │
│  │  [━━━━━━━━━░░░░] 75%           │   │ ← Progress scale
│  │   FOUND  BUILD  DEV  ADV  ELITE │   │   0-100 markers
│  │     0    40    60   75   85    100 │
│  └─────────────────────────────────┘   │
│                                         │
│  ┌──────────────┬─────────────────┐    │
│  │ Creation: 74.8│ Transfer: 69.5 │    │ ← Subscores
│  │   Flow        │   Efficiency    │    │   out of 100
│  └──────────────┴─────────────────┘    │
│                                         │
│  💡 ON TABLE: +3.1 mph bat speed       │ ← Available gain
│     5 points from ELITE (85)           │ ← Progress to next level
└─────────────────────────────────────────┘
```

### KRS Hero Specifications

**KRS Total Score (Primary)**:
- **Value**: 75 (example) - Range: 0-100
- **Formula**: `(Creation × 0.4) + (Transfer × 0.6)`
- **Example**: `(74.8 × 0.4) + (69.5 × 0.6) = 29.92 + 41.7 = 71.62 → 72`
- **Font Size**: 72px (mobile: 56px)
- **Font Weight**: 700 (bold)
- **Color**: White on gradient background

**KRS Level Badge**:
- **FOUNDATION**: 0-40 (Gray #6B7280)
- **BUILDING**: 40-60 (Blue #3B82F6)
- **DEVELOPING**: 60-75 (Green #10B981)
- **ADVANCED**: 75-85 (Amber #F59E0B)
- **ELITE**: 85-100 (Purple #8B5CF6)

**Progress Scale**:
- Visual bar showing position on 0-100 scale
- Markers at: 0, 40, 60, 75, 85, 100
- Current score indicated with dot/arrow

**Subscores (Creation & Transfer)**:
- **Creation Score**: 74.8 / 100
  - Label: "Flow" or "Power Creation"
  - Formula: `Peak momentum / Physical capacity × 100`
  - Color: Blue tint
- **Transfer Score**: 69.5 / 100
  - Label: "Efficiency" or "Power Transfer"
  - Formula: `Output bat speed / Peak momentum × 100`
  - Color: Green tint

**"On Table" Indicator**:
- Shows available improvement potential
- Example: "+3.1 mph bat speed" or "+30 KE available"
- Calculation: Physical capacity minus current output
- Color: Electric Cyan highlight

**Progress to Next Level**:
- "5 points from ELITE (85)"
- Shows gap to next milestone
- Motivational context

---

## 🎨 Section 2: Brain Card (4B Framework) ✅ CORRECTED

**Component**: `BrainCard`  
**Background**: Light Purple (#EDE9FE)  
**Icon/Text Color**: Dark Purple (#7C3AED)

```
┌─────────────────────────────────────┐
│  🧠 BRAIN                          │ ← Heading-03 • Purple
│  Decision Making & Timing           │ ← Caption-01 • Purple/60%
├─────────────────────────────────────┤
│                                     │
│  SLINGSHOTTER                       │ ← Motor Profile (primary)
│  92% confidence                     │   Heading-04 • Gray-900
│                                     │
│  "Generates power through           │ ← Profile description
│   aggressive hip rotation"          │   Body-02 • Gray-700
│                                     │
│  ━━━━━━━━━━━━━━━━━━━━ 92%         │ ← Confidence bar
│                                     │
│  ⏱️ Timing                          │
│  • Tempo: Fast (0.65s)             │ ← Load-to-contact time
│  • Load Phase: 0.28s               │   Body-02 • Gray-700
│  • Launch: Quick trigger           │
│                                     │
│  🎯 Similar Athletes:               │
│  Fernando Tatis Jr., Mookie Betts  │ ← Example players
│                                     │
└─────────────────────────────────────┘
```

### Brain Card Data Structure

**Motor Profile (Primary Metric)**:
- **4 Types**: Spinner, Slingshotter, Whipper, Titan
- **Example**: "SLINGSHOTTER"
- **Confidence**: 92% (0-100%)
- **Description**: Brief biomechanical summary
- **Display**: Large heading, color-coded badge

**Timing Metrics**:
- **Tempo**: Fast/Medium/Slow
- **Load-to-Contact Time**: e.g., 0.65 seconds
- **Load Phase Duration**: e.g., 0.28 seconds
- **Launch Trigger**: Quick/Moderate/Delayed

**Context**:
- **Similar Athletes**: 2-3 example MLB/professional players
- **Characteristics**: Key traits of this motor profile

**Data Sources**:
- Motor Profile: Classification from Movement Assessment
- Timing: Video analysis (240 FPS required)
- Confidence: Model certainty from pose estimation

---

## 🎨 Section 3: Body Card (4B Framework) ✅ CORRECTED

**Component**: `BodyCard`  
**Background**: Light Blue (#DBEAFE)  
**Icon/Text Color**: Dark Blue (#2563EB)

```
┌─────────────────────────────────────┐
│  💪 BODY                           │ ← Heading-03 • Blue
│  Power Creation & Flow              │ ← Caption-01 • Blue/60%
├─────────────────────────────────────┤
│                                     │
│  Creation Score                     │ ← Primary metric
│  74.8 / 100                         │   Display-01 • Gray-900
│                                     │
│  ━━━━━━━━━━━━━━━□□□□ 75%          │ ← Visual progress bar
│                                     │
│  ⚡ Physical Capacity               │
│  • Bat Speed Capacity: 85 mph      │ ← Theoretical max
│  • Kinetic Energy: 125 J           │   Body-02 • Gray-700
│                                     │
│  📊 Peak Performance                │
│  • Peak Ground Force: 723 N        │ ← Force generation
│  • Peak Momentum: 2.8 kg·m/s       │   Peak values
│                                     │
│  🔥 Ground Flow Score: 7.5/10      │ ← Quality metric
│                                     │
│  Status: ✅ GOOD                    │ ← Overall status
│  Room for improvement in load phase │
└─────────────────────────────────────┘
```

### Body Card Data Structure

**Creation Score (Primary)**:
- **Value**: 74.8 / 100
- **Formula**: `Peak momentum / Physical capacity × 100`
- **Interpretation**: How well player generates kinetic energy
- **Display**: Large number (48px) with "/100" context

**Physical Capacity**:
- **Bat Speed Capacity**: e.g., 85 mph
  - Theoretical maximum based on body metrics (height, weight, age)
  - Calculated from anthropometric data
- **Kinetic Energy**: e.g., 125 Joules
  - Total energy created during swing
  - Measured from biomechanics

**Peak Performance Metrics**:
- **Peak Ground Force**: e.g., 723 Newtons
  - Maximum force applied to ground
  - Indicates power generation capacity
- **Peak Momentum**: e.g., 2.8 kg·m/s
  - Maximum momentum achieved
  - Key input for Creation score

**Ground Flow Score**:
- **Range**: 0-10
- **Assessment**: Quality of weight transfer and sequencing
- **Color**: Green (8-10), Amber (5-7), Red (<5)

**Status Badge**:
- ✅ GOOD (75-100)
- ⚠️ DEVELOPING (50-74)
- 🔴 NEEDS WORK (<50)

**Data Sources**:
- Creation Score: Calculated from video analysis
- Physical Capacity: Estimated from profile (height, weight, age)
- Peak Force/Momentum: Pose estimation + physics model
- Ground Flow: Kinematic sequence analysis

---

## 🎨 Section 4: Bat Card (4B Framework) ✅ CORRECTED

**Component**: `BatCard`  
**Background**: Light Green (#D1FAE5)  
**Icon/Text Color**: Dark Green (#059669)

```
┌─────────────────────────────────────┐
│  🏏 BAT                            │ ← Heading-03 • Green
│  Power Transfer & Efficiency        │ ← Caption-01 • Green/60%
├─────────────────────────────────────┤
│                                     │
│  Transfer Score                     │ ← Primary metric
│  69.5 / 100                         │   Display-01 • Gray-900
│                                     │
│  ━━━━━━━━━━━━━□□□□□□ 70%          │ ← Visual progress bar
│                                     │
│  ⚙️ Transfer Efficiency             │
│  • Current: 82%                    │ ← Efficiency ratio
│  • Target: 90% (ELITE)             │   Body-02 • Gray-700
│  • Gap: -8%                        │
│                                     │
│  🎯 Swing Plane                     │
│  • Attack Angle: 18°               │ ← Bat path metrics
│  • Connection: Early separation    │   Quality notes
│  • Path Quality: 8.5/10            │
│                                     │
│  📐 Kinetic Chain                   │
│  • Hip-Shoulder Sep: 45°           │ ← Separation angle
│  • Sequence Score: 7/10            │   Timing quality
│                                     │
│  Status: ✅ GOOD                    │ ← Overall status
│  Work on connection timing          │
└─────────────────────────────────────┘
```

### Bat Card Data Structure

**Transfer Score (Primary)**:
- **Value**: 69.5 / 100
- **Formula**: `Output bat speed / Peak momentum × 100`
- **Interpretation**: Efficiency of converting body power to bat speed
- **Display**: Large number (48px) with "/100" context

**Transfer Efficiency**:
- **Current %**: e.g., 82%
- **Calculation**: How much of created energy reaches the bat
- **Target**: 90%+ for ELITE level
- **Gap**: Shows room for improvement

**Swing Plane Metrics**:
- **Attack Angle**: e.g., 18 degrees
  - Bat path relative to ground at contact
  - Optimal: 15-25° for most hitters
- **Connection**: Quality descriptor
  - Examples: "Early separation", "Good connection", "Late load"
- **Path Quality**: 0-10 scale
  - Assessment of bat path efficiency

**Kinetic Chain**:
- **Hip-Shoulder Separation**: e.g., 45 degrees
  - Angular separation at max load
  - Optimal: 40-60° depending on profile
- **Sequence Score**: 0-10
  - Quality of energy transfer through body segments
  - Ground → Hips → Torso → Arms → Bat

**Status Badge**:
- ✅ GOOD (75-100)
- ⚠️ DEVELOPING (50-74)
- 🔴 NEEDS WORK (<50)

**Data Sources**:
- Transfer Score: Calculated from video analysis
- Efficiency: Ratio of output/input energy
- Attack Angle: 3D bat trajectory from video
- Hip-Shoulder Sep: Pose estimation
- Sequence Score: Timing analysis of body segments

---

## 🎨 Section 5: Ball Card (4B Framework) ✅ CORRECTED

**Component**: `BallCard`  
**Background**: Light Red (#FEE2E2)  
**Icon/Text Color**: Dark Red (#DC2626)

```
┌─────────────────────────────────────┐
│  ⚾ BALL                           │ ← Heading-03 • Red
│  Contact Quality & Outcomes         │ ← Caption-01 • Red/60%
├─────────────────────────────────────┤
│                                     │
│  Exit Velocity                      │
│  82 mph (Current)                   │ ← Display-01 • Gray-900
│  95 mph (Capacity)                  │   Target/potential
│                                     │
│  ━━━━━━━━━━━━━━━━━━ 86%           │ ← % of capacity
│  +13 mph available                  │   Gap to potential
│                                     │
│  🎯 Contact Quality                 │
│  • Overall: 8.2 / 10               │ ← Quality metric
│  • Sweet Spot %: 65%               │   Body-02 • Gray-700
│  • Hard Hit %: 45%                 │
│                                     │
│  📊 Launch Angle                    │
│  • Current Range: 12-18°           │ ← Angle distribution
│  • Optimal: Line drives            │   Contact type
│  • Profile: Gap-to-gap power       │
│                                     │
│  📈 Trajectory                      │
│  • Spray Chart: Balanced           │ ← Direction analysis
│  • Pull %: 35% | Center: 40%      │   Distribution
│  • Oppo %: 25%                     │
│                                     │
│  Status: ⭐ CONSISTENT              │ ← Overall status
│  Great contact quality              │
└─────────────────────────────────────┘
```

### Ball Card Data Structure

**Exit Velocity (Primary)**:
- **Current**: e.g., 82 mph
  - Average exit velocity from session
  - Measured output
- **Capacity**: e.g., 95 mph
  - Theoretical maximum based on Creation score
  - What player COULD achieve with perfect transfer
- **Gap**: e.g., +13 mph available
  - Difference between current and capacity
  - Shows improvement potential

**Contact Quality**:
- **Overall Score**: 0-10 scale
  - Comprehensive contact assessment
  - Considers exit velo, launch angle, barrel control
- **Sweet Spot %**: e.g., 65%
  - Percentage of swings hitting barrel sweet spot
  - Target: 60%+ for good hitters
- **Hard Hit %**: e.g., 45%
  - Percentage of swings >90 mph exit velo
  - Indicator of power consistency

**Launch Angle**:
- **Current Range**: e.g., 12-18 degrees
  - Typical launch angle distribution
- **Optimal**: Contact type descriptor
  - Examples: "Line drives", "Fly balls", "Ground balls"
- **Profile**: Style descriptor
  - Examples: "Gap-to-gap power", "Pull-side power", "Contact hitter"

**Trajectory/Spray Chart**:
- **Spray Pattern**: Balanced/Pull-heavy/Oppo-heavy
- **Pull %**: Percentage of hits to pull side
- **Center %**: Percentage up the middle
- **Oppo %**: Percentage to opposite field
- **Target**: 30-40-30 is balanced

**Status Badge**:
- ⭐ CONSISTENT (85-100)
- ✅ GOOD (70-84)
- ⚠️ DEVELOPING (50-69)
- 🔴 INCONSISTENT (<50)

**Data Sources**:
- Exit Velocity: Calculated from video (240 FPS)
  - OR from radar device if available
  - OR estimated from bat speed + contact quality
- Capacity: Derived from Creation score + Transfer efficiency
- Launch Angle: 3D trajectory analysis
- Contact Quality: Barrel tracking + exit velo
- Spray Chart: Direction analysis from multiple swings

**⚠️ NOTE**: Exit velocity and launch angle require either:
1. 240 FPS high-speed video for accurate calculation
2. External measurement device (radar, TrackMan, etc.)
3. If unavailable, show "Not Available - Upgrade to KRS Analysis"

---

## 🎨 Sections 6-11: Supporting Content

### Section 6: Quick Wins
**Component**: `QuickWinsSection`  
**Layout**: Vertical stack of action cards

```
┌─────────────────────────────────────┐
│  🎯 Quick Wins                     │ ← Heading-02
│  Top 3 things to work on today     │ ← Body-02 • Gray-500
│                                     │
│  ┌─────────────────────────────┐   │
│  │ 1. Improve Ground Flow      │   │ ← Action card
│  │    +5 Creation points       │   │
│  │    [View Drills →]          │   │
│  └─────────────────────────────┘   │
│                                     │
│  ┌─────────────────────────────┐   │
│  │ 2. Optimize Kinetic Chain   │   │
│  │    +3 Transfer points       │   │
│  │    [View Drills →]          │   │
│  └─────────────────────────────┘   │
│                                     │
│  ┌─────────────────────────────┐   │
│  │ 3. Increase Exit Velocity   │   │
│  │    Close +13 mph gap        │   │
│  │    [View Drills →]          │   │
│  └─────────────────────────────┘   │
└─────────────────────────────────────┘
```

### Section 7: Your Mission
**Component**: `MissionSection`

```
┌─────────────────────────────────────┐
│  🎯 Your Mission                   │
│  Current Phase: Foundation         │
│                                     │
│  Goal: Reach ADVANCED level (75+)  │
│  Progress: 72/75 (96%)             │
│  ━━━━━━━━━━━━━━━━━━━□ 96%         │
│                                     │
│  [Continue Training →]              │
└─────────────────────────────────────┘
```

### Sections 8-11 (unchanged)
- **Section 8**: Drill Library (personalized recommendations)
- **Section 9**: Progress tracking (swings, streaks)
- **Section 10**: Coach Rick motivational message
- **Section 11**: Flags & insights (paradoxes, special notes)

---

## 📊 Component Library References

**Components Used**:
1. `KRSHeroCard` - Primary score display with subscores
2. `BrainCard` - Motor profile & timing
3. `BodyCard` - Creation score & physical capacity
4. `BatCard` - Transfer score & efficiency
5. `BallCard` - Exit velocity & contact quality
6. `QuickWinsSection` - Action items
7. `MissionSection` - Progress goals
8. `DrillLibrarySection` - Recommended drills
9. `ProgressSection` - Stats & streaks
10. `CoachRickSection` - Motivational message
11. `FlagsSection` - Insights & paradoxes

---

## 🎨 Design Specifications

**Colors (from design-tokens.json)**:
- Brain Card: bg=#EDE9FE, text=#7C3AED (purple)
- Body Card: bg=#DBEAFE, text=#2563EB (blue)
- Bat Card: bg=#D1FAE5, text=#059669 (green)
- Ball Card: bg=#FEE2E2, text=#DC2626 (red)

**Typography**:
- KRS Score: 72px (mobile: 56px), weight 700
- Subscores: 48px, weight 600
- Card Headings: 20px, weight 600
- Body Text: 16px, weight 400
- Captions: 14px, weight 400

**Spacing**:
- Section gaps: 32px
- Card padding: 24px
- Card gaps (4B grid): 16px

**Shadows**:
- Cards: shadow-01 (subtle)
- Hero card: shadow-02 (medium)

---

## ✅ VALIDATION CHECKLIST

- [x] KRS scale is 0-100 (not 0-1000)
- [x] KRS levels: FOUNDATION/BUILDING/DEVELOPING/ADVANCED/ELITE
- [x] Creation and Transfer subscores shown
- [x] "On Table" gain displayed
- [x] Brain card shows Motor Profile (4 types)
- [x] Body card shows Creation Score (/100)
- [x] Bat card shows Transfer Score (/100)
- [x] Ball card shows Current + Capacity Exit Velocity
- [x] 4B cards use correct color tints (purple/blue/green/red)
- [x] All metrics match product specification
- [x] No invented metrics (removed "Decision", "Recognition", etc.)

---

**STATUS**: ✅ CORRECTED - Ready for Figma implementation
