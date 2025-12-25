# CATCHING BARRELS - MASTER BUILD SPECIFICATION
## Complete Frontend + Backend Integration
## FOR BUILDER 2 - DO NOT DEVIATE FROM THIS STRUCTURE

---

## 🚨 **CRITICAL: READ THIS FIRST**

### **Your Job:**
Build the **Catching Barrels player experience** exactly as specified below.

### **What You CANNOT Change:**
- ✋ The data schema (use exactly as provided)
- ✋ The UI section order (Brain → Body → Bat → Ball → Mission → Drills)
- ✋ The KRS calculation approach (Creation + Transfer)
- ✋ The branding (Catching Barrels, Coach Rick AI, KRS™)

### **What You CAN Customize:**
- ✅ Visual styling (colors, fonts, spacing) to match brand
- ✅ Animations/transitions
- ✅ Mobile responsiveness details
- ✅ Loading states and error handling UX

---

## 📊 **SYSTEM ARCHITECTURE OVERVIEW**

```
┌─────────────────────────────────────────────────────────────┐
│  PLAYER UPLOADS VIDEO                                       │
│  (Phone camera, hitting session)                            │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  CATCHING BARRELS BACKEND                                   │
│                                                             │
│  Step 1: Video Processing                                  │
│  ├─ Gemini AI analysis (Motor Profile, Ground/Engine/Weapon)│
│  └─ Returns: coach_rick_analysis.json                       │
│                                                             │
│  Step 2: Biomechanics Processing (if available)            │
│  ├─ Reboot Motion API call                                  │
│  ├─ Returns: inverse_kinematics.csv + momentum_energy.csv   │
│  └─ Store in YOUR database                                  │
│                                                             │
│  Step 3: KRS Calculation                                   │
│  ├─ Input: Player info + Reboot data OR Gemini scores      │
│  ├─ Calculate: Creation Score + Transfer Score             │
│  └─ Returns: krs_report.json                                │
│                                                             │
│  Step 4: Generate Player Report                            │
│  └─ Combine all data into unified report JSON              │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  PLAYER UI (What Builder 2 Builds)                          │
│  Displays: KRS + 4B Breakdown + Mission + Drills            │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔑 **BACKEND API ENDPOINTS (What Builder 2 Calls)**

### **Endpoint 1: Upload & Analyze Session**
```
POST /api/sessions/analyze

Request:
{
  "player_id": "string",
  "video_url": "string",
  "player_info": {
    "name": "string",
    "age": number,
    "height_inches": number,
    "weight_lbs": number,
    "wingspan_inches": number (optional)
  }
}

Response:
{
  "session_id": "string",
  "status": "processing" | "complete" | "error",
  "estimated_time_seconds": number
}
```

### **Endpoint 2: Get Session Report**
```
GET /api/sessions/{session_id}/report

Response: PlayerReport (see schema below)
```

### **Endpoint 3: Get Player Progress**
```
GET /api/players/{player_id}/progress

Response:
{
  "total_sessions": number,
  "total_swings": number,
  "krs_history": Array<{date, krs, creation, transfer}>,
  "current_streak_weeks": number,
  "milestones": Array<{type, date, value}>
}
```

---

## 📋 **COMPLETE DATA SCHEMA: PlayerReport**

### **This is THE contract between backend and frontend.**
### **Builder 2: Use this EXACT schema. Do not modify.**

```typescript
interface PlayerReport {
  // ========================================
  // METADATA
  // ========================================
  session_id: string;
  player_id: string;
  session_date: string;              // ISO 8601
  session_number: number;            // Lifetime session count
  
  // ========================================
  // PLAYER INFO
  // ========================================
  player: {
    name: string;
    age: number;
    height_inches: number;
    weight_lbs: number;
    wingspan_inches: number | null;
    ape_index: number | null;        // wingspan - height
  };
  
  // ========================================
  // PROGRESS TRACKING
  // ========================================
  progress: {
    total_swings: number;            // Lifetime total
    session_number: number;          // Current session
    last_session_date: string;
    week_streak: number;             // Consecutive weeks
    days_since_last: number;
    
    // Unlock status
    report_unlocked: boolean;        // true if >= 50 swings
    swings_to_unlock: number;        // Remaining until 50
  };
  
  // ========================================
  // KRS™ (HERO METRIC)
  // ========================================
  krs: {
    total: number;                   // 0-100
    level: 'FOUNDATION' | 'BUILDING' | 'DEVELOPING' | 'ADVANCED' | 'ELITE';
    emoji: string;                   // 🌱, 🔧, 📈, ⭐, 🏆
    points_to_next_level: number;
    
    // Components
    creation_score: number;          // 0-100
    transfer_score: number;          // 0-100
    
    // Trends (vs last session)
    krs_change: number;              // +/- points
    creation_change: number;
    transfer_change: number;
    
    // Data source
    data_source: 'Video Analysis' | 'Advanced Biomechanics' | 'Elite Lab Session';
    confidence: 'Standard' | 'Advanced' | 'Elite';
  };
  
  // ========================================
  // 🧠 BRAIN (MOTOR PROFILE)
  // ========================================
  brain: {
    motor_profile: {
      primary: 'Twister' | 'Tilter' | 'Hybrid' | 'Spinner';
      primary_confidence: number;    // 0-100
      secondary: string | null;
      
      // Display
      display_name: string;          // "THE TWISTER"
      tagline: string;               // "Rotational power. Stay tight, spin fast."
      color: string;                 // Hex color for theming
      icon: string;                  // Emoji
    };
    
    tempo: {
      ratio: number;                 // e.g., 2.8
      category: 'Fast' | 'Balanced' | 'Slow';
      message: string;
    };
    
    pitch_watch: string | null;      // "Breaking balls down"
  };
  
  // ========================================
  // 🏋️ BODY (CREATION - POWER ENGINE)
  // ========================================
  body: {
    creation_score: number;          // 0-100
    
    capacity: {
      capacity_ke_joules: number;    // Physical capacity
      capacity_bat_speed_mph: number;// Theoretical max
    };
    
    actual: {
      peak_ke_joules: number;        // What you generated
      estimated_bat_speed_mph: number;
    };
    
    on_table: {
      ke_gap_joules: number;         // Capacity - Actual
      bat_speed_gap_mph: number;
    };
    
    // Sub-components
    ground_flow: {
      score: number;                 // 0-10
      status: 'elite' | 'good' | 'needs_work' | 'critical';
    };
    
    engine_flow: {
      score: number;                 // 0-10
      status: 'elite' | 'good' | 'needs_work' | 'critical';
    };
    
    // Gap source (what's limiting creation)
    gap_source: string;              // "Early hip rotation"
  };
  
  // ========================================
  // ⚔️ BAT (TRANSFER - POWER DELIVERY)
  // ========================================
  bat: {
    transfer_score: number;          // 0-100
    
    flow: {
      you_create_mph: number;        // From body
      reaches_barrel_mph: number;    // Output
      on_table_mph: number;          // Lost in transfer
    };
    
    // Sub-components
    kinetic_chain: {
      score: number;                 // 0-100
      status: 'elite' | 'good' | 'needs_work' | 'critical';
      
      // Details (if available)
      hip_momentum: number | null;
      shoulder_momentum: number | null;
      sh_ratio: number | null;
      sequence: 'proper' | 'reversed' | 'compressed' | null;
    };
    
    lead_leg: {
      score: number;                 // 0-100
      status: 'elite' | 'good' | 'needs_work' | 'critical';
      
      // Details (if available)
      knee_extension_deg: number | null;
      target_extension_deg: number | null;
      gap_deg: number | null;
    };
    
    timing: {
      score: number;                 // 0-100
      status: 'elite' | 'good' | 'needs_work' | 'critical';
    };
    
    // Attack angle
    attack_angle: {
      current_deg: number;
      capacity_deg: number;          // Optimal range
    };
    
    // Gap source (what's limiting transfer)
    gap_source: string;              // "Pelvis-torso timing"
  };
  
  // ========================================
  // ⚾ BALL (PROJECTIONS)
  // ========================================
  ball: {
    current: {
      exit_velo_mph: number;
      launch_angle_deg: number;
      contact_quality: string;       // "Ground ball tendency"
    };
    
    capacity: {
      exit_velo_mph: number;
      launch_angle_deg: number;
      contact_quality: string;       // "Line drive machine"
    };
    
    total_on_table_mph: number;      // Body gap + Bat gap
  };
  
  // ========================================
  // 💪 WINS (WHAT'S WORKING)
  // ========================================
  wins: Array<{
    metric: string;                  // "Hip Angular Momentum"
    score: number | string;
    percentile: number | null;       // Age-normalized
    message: string;
    icon: string;
  }>;
  
  // ========================================
  // 🎯 MISSION (PRIMARY FOCUS)
  // ========================================
  mission: {
    title: string;                   // "Fix Lead Knee Extension"
    category: 'body' | 'bat' | 'timing' | 'power';
    priority: 'CRITICAL' | 'HIGH' | 'MEDIUM';
    
    unlock: string;                  // "Unlock +20 mph bat speed"
    explanation: string;             // 2-3 sentences
    
    current_value: number | null;
    target_value: number | null;
    unit: string | null;
    gap: number | null;
    
    expected_fix_weeks: number;
  };
  
  // Secondary issues (collapsed by default)
  secondary_issues: Array<{
    title: string;
    priority: 'MEDIUM' | 'LOW';
    brief: string;
  }>;
  
  // ========================================
  // 🏋️ DRILLS (TRAINING PLAN)
  // ========================================
  drills: Array<{
    name: string;
    category: string;
    
    volume: string;                  // "3 sets × 30 seconds"
    frequency: string;               // "Daily"
    
    why_it_works: string;
    key_cues: string[];              // Max 3
    
    video_url: string | null;
    thumbnail_url: string | null;
    
    addresses_issue: string;         // Links to mission
  }>;
  
  // Projection if drills followed
  projection: {
    timeframe: string;               // "4-6 weeks"
    gains: {
      bat_speed: string;             // "+15-20 mph"
      exit_velocity: string;
      transfer_efficiency: string;
      krs_points: string;            // "+23 points"
    };
  };
  
  // ========================================
  // 💬 COACH RICK MESSAGE
  // ========================================
  coach_message: {
    what_i_see: string;              // One sentence
    your_mission: string;            // One sentence
    signature: string;               // "Trust the work."
  };
  
  // ========================================
  // 🚩 SPECIAL FLAGS
  // ========================================
  flags: {
    power_paradox: boolean;
    cricket_background: boolean;
    anthropometric_advantage: boolean;
    rapid_improver: boolean;
  };
  
  // Special insights (if flags true)
  special_insights: {
    power_paradox?: {
      capacity_percentile: number;
      delivery_percentile: number;
      potential_gain_mph: number;
      bottleneck: string;
    };
    
    cricket_background?: {
      detected_patterns: string[];
      conversion_timeline: string;
      priority_focus: string;
    };
    
    anthropometric_advantage?: {
      ape_index: number;
      leverage_advantage: string;
      ceiling_estimate: string;
    };
  };
}
```

---

## 🎨 **UI STRUCTURE (EXACT ORDER - DO NOT REORDER)**

### **Builder 2: Build these sections IN THIS ORDER, TOP TO BOTTOM:**

```
┌─────────────────────────────────────────────────────────────┐
│  HEADER                                                     │
│  - Catching Barrels logo                                   │
│  - Streak counter (🔥 {week_streak})                       │
│  - Session number                                          │
│  - [Upload Next Session] CTA                               │
├─────────────────────────────────────────────────────────────┤
│  PROGRESS GATE (if total_swings < 50)                      │
│  - Progress bar                                            │
│  - "X swings until full report"                            │
│  - What's unlocked at current level                        │
│  - [Upload Next Session] CTA                               │
│                                                            │
│  STOP HERE IF < 50 SWINGS. Show limited content below.    │
├─────────────────────────────────────────────────────────────┤
│  KRS HERO SECTION                                          │
│  - Big circular display or gauge                           │
│  - KRS total (0-100)                                       │
│  - Level badge (emoji + name)                              │
│  - "Kinetic Realization Score™"                            │
│  - Creation Score | Transfer Score (side by side)          │
│  - Trend arrows (↑↓→ vs last session)                      │
│  - Progress bar to next level                              │
│  - Data source badge (confidence level)                    │
├─────────────────────────────────────────────────────────────┤
│  🧠 BRAIN (MOTOR PROFILE)                                   │
│  - Profile icon + name (THE TWISTER)                       │
│  - Tagline in quotes                                       │
│  - Confidence badge (if < 100%)                            │
│  - Tempo ratio + category                                  │
│  - Pitch watch (if available)                              │
├─────────────────────────────────────────────────────────────┤
│  🏋️ BODY (CREATION SCORE - POWER ENGINE)                    │
│  - Creation Score (0-100) with trend                       │
│  - Capacity vs Actual comparison                           │
│    • Capacity: X mph / Y Joules                            │
│    • You Create: X mph / Y Joules                          │
│    • On The Table: X mph / Y Joules                        │
│  - Ground Flow score + status                              │
│  - Engine Flow score + status                              │
│  - Gap Source (what's limiting creation)                   │
├─────────────────────────────────────────────────────────────┤
│  ⚔️ BAT (TRANSFER SCORE - POWER DELIVERY)                   │
│  - Transfer Score (0-100) with trend                       │
│  - Flow visualization                                      │
│    • You Create: X mph                                     │
│    • Reaches Barrel: X mph                                 │
│    • On The Table: X mph                                   │
│  - Kinetic Chain score + status                            │
│    └─ Details if available (hip/shoulder, ratio, sequence) │
│  - Lead Leg score + status                                 │
│    └─ Details if available (knee angle, gap)               │
│  - Timing score + status                                   │
│  - Attack Angle (current vs capacity)                      │
│  - Gap Source (what's limiting transfer)                   │
├─────────────────────────────────────────────────────────────┤
│  ⚾ BALL (PROJECTIONS)                                      │
│  - Current Performance                                     │
│    • Exit Velo: X mph                                      │
│    • Launch Angle: X°                                      │
│    • Contact Quality: "Ground ball tendency"               │
│  - Capacity (if fixed)                                     │
│    • Exit Velo: X mph                                      │
│    • Launch Angle: X°                                      │
│    • Contact Quality: "Line drive machine"                 │
│  - Total On Table: X mph bat speed                         │
├─────────────────────────────────────────────────────────────┤
│  🚨 SPECIAL INSIGHTS (if flags true)                       │
│  - Power Paradox card (if power_paradox = true)            │
│    • Capacity vs Delivery bar chart                        │
│    • Percentiles, bottleneck, potential gain               │
│  - Cricket Background card (if cricket_background = true)  │
│    • Detected patterns, timeline, priority                 │
│  - Anthropometric Advantage (if ape index significant)     │
│    • Ape index, leverage advantage, ceiling                │
├─────────────────────────────────────────────────────────────┤
│  💪 YOUR WINS (WHAT'S WORKING)                              │
│  - 1-3 win cards (green theme)                             │
│  - Each shows: metric, score, percentile, message, icon    │
│  - Always positive, celebratory tone                       │
├─────────────────────────────────────────────────────────────┤
│  🎯 YOUR MISSION (PRIMARY FOCUS)                            │
│  - Priority badge (CRITICAL/HIGH/MEDIUM)                   │
│  - Mission title                                           │
│  - Current vs Target visualization                         │
│  - Unlock callout (big, bold)                              │
│  - Explanation (3-4 sentences max)                         │
│  - Expected timeline                                       │
│  - [▼ Other areas to monitor] (expandable)                 │
│    └─ Secondary issues list                                │
├─────────────────────────────────────────────────────────────┤
│  🏋️ YOUR DRILLS (TRAINING PLAN)                             │
│  - Header: "Fix {mission} in {timeframe}"                  │
│  - 2-3 drill cards                                         │
│    • Name                                                  │
│    • Volume | Frequency                                    │
│    • [▼ Why it works] (expandable)                         │
│    • [▼ Key cues (3)] (expandable)                         │
│    • [📹 Watch Demo] (if video available)                  │
│  - Projection box (green theme)                            │
│    • "Expected in {timeframe}:"                            │
│    • Bat Speed: +X mph                                     │
│    • Exit Velocity: +X mph                                 │
│    • Transfer Efficiency: +X%                              │
│    • KRS: +X points                                        │
├─────────────────────────────────────────────────────────────┤
│  📈 YOUR PROGRESS (SESSION HISTORY)                         │
│  - Session count + total swings                            │
│  - KRS trend line chart                                    │
│  - All-time KRS change                                     │
│  - Current streak                                          │
│  - Milestones achieved                                     │
│  - [View Full History] button                              │
├─────────────────────────────────────────────────────────────┤
│  💬 COACH RICK SAYS                                         │
│  - Avatar + name                                           │
│  - What I see (1 sentence)                                 │
│  - Your mission (1 sentence)                               │
│  - Signature closer (1 sentence)                           │
├─────────────────────────────────────────────────────────────┤
│  FOOTER CTA                                                │
│  - [📹 Upload Next Session] (full-width button)            │
│  - Instruction text                                        │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎨 **VISUAL DESIGN REQUIREMENTS**

### **Color Palette:**
```css
/* Dark Mode Base */
--bg-primary: #030712;      /* gray-950 */
--bg-secondary: #111827;    /* gray-900 */
--bg-card: #1F2937;         /* gray-800 */

/* Text */
--text-primary: #F9FAFB;    /* gray-50 */
--text-secondary: #D1D5DB;  /* gray-300 */

/* Status Colors */
--elite: #10B981;    /* green-500 */
--good: #3B82F6;     /* blue-500 */
--warning: #F59E0B;  /* amber-500 */
--critical: #EF4444; /* red-500 */

/* Motor Profile Colors (dynamic) */
--profile-color: {motor_profile.color}; /* Use from data */
```

### **Typography:**
```css
font-family: 'DM Sans', 'Inter', system-ui, sans-serif;

/* Hierarchy */
h1: 2.25rem (36px), bold
h2: 1.875rem (30px), semibold
h3: 1.5rem (24px), semibold
h4: 1.25rem (20px), medium
body: 1rem (16px), normal
small: 0.875rem (14px), normal
```

### **Spacing:**
```css
--space-unit: 8px;
--space-xs: 4px;
--space-sm: 8px;
--space-md: 16px;
--space-lg: 24px;
--space-xl: 32px;
--space-2xl: 48px;
```

### **Border Radius:**
```css
--radius-sm: 4px;
--radius-md: 8px;
--radius-lg: 12px;
--radius-xl: 16px;
```

### **Cards:**
```css
.card {
  background: var(--bg-card);
  border: 1px solid rgba(55, 65, 81, 0.5);
  border-radius: var(--radius-xl);
  padding: var(--space-lg);
}

.card-hero {
  border-top: 3px solid var(--profile-color);
  background: linear-gradient(135deg, var(--bg-secondary), var(--bg-card));
}
```

---

## 📱 **MOBILE-FIRST REQUIREMENTS**

### **Max Width:**
```css
.container {
  max-width: 480px;
  margin: 0 auto;
  padding: 0 var(--space-md);
}
```

### **Touch Targets:**
```css
/* Minimum 44px × 44px for all tappable elements */
button, a.button {
  min-height: 44px;
  min-width: 44px;
  padding: var(--space-sm) var(--space-lg);
}
```

### **Breakpoints:**
```css
/* Mobile first - default styles for < 640px */

@media (min-width: 640px) {
  /* Tablet adjustments */
}

@media (min-width: 1024px) {
  /* Desktop adjustments */
  .container {
    max-width: 640px;  /* Slightly wider on desktop */
  }
}
```

---

## 🔄 **STATE MANAGEMENT**

### **Loading States:**
```typescript
// Show skeleton screens while data loads
<LoadingState>
  <SkeletonKRSHero />
  <SkeletonMotorProfile />
  <SkeletonBodyCard />
  <SkeletonBatCard />
  ...
</LoadingState>
```

### **Error States:**
```typescript
// If session fails to load
<ErrorState 
  message="Couldn't load your report. Let's try again."
  onRetry={() => refetchSession()}
/>
```

### **Empty States:**
```typescript
// If player has 0 sessions
<EmptyState
  icon="📹"
  message="Ready to unlock your Swing DNA?"
  cta="Upload First Session"
/>
```

---

## 🚀 **BACKEND INTEGRATION QUESTIONS FOR BUILDER**

### **Question 1: Reboot Motion API Access**
```
Can you access the Reboot Motion API from your backend?

If YES:
- What endpoints are available?
- What's the request/response format?
- Can you process the CSV data and store in your database?

If NO:
- Do you need API credentials?
- Do you need documentation?
- Should we start with video-only (Gemini) first?
```

### **Question 2: Data Storage**
```
Where are you storing session data?

- PostgreSQL?
- MongoDB?
- Firebase?
- Other?

Do you need help designing the database schema?
```

### **Question 3: KRS Calculation**
```
Who's writing the KRS calculation logic?

Option A: You write it (I provide formulas)
Option B: We write it (Python module you call)
Option C: Separate microservice (API endpoint)

Preference?
```

### **Question 4: Video Processing**
```
How is video analysis currently working?

- You call Gemini API directly?
- Existing endpoint returns Motor Profile scores?
- What's the current flow?

Can you share:
- Sample Gemini API response
- Current video upload endpoint
- Processing time estimates
```

---

## ✅ **ACCEPTANCE CRITERIA**

### **Before marking this task complete, verify:**

**UI Checklist:**
- [ ] All 11 sections render in correct order
- [ ] KRS hero section prominent at top
- [ ] Motor Profile theming applied (color from data)
- [ ] Progress gate shows for < 50 swings
- [ ] Trend arrows show correctly (↑↓→)
- [ ] Special insights conditionally render based on flags
- [ ] Drills expandable for details
- [ ] Coach Rick message at bottom
- [ ] Upload CTA sticky/always visible
- [ ] Mobile responsive (test on iPhone)
- [ ] Loading skeletons during data fetch
- [ ] Error handling with retry

**Data Integration Checklist:**
- [ ] API endpoint called correctly
- [ ] PlayerReport schema matches exactly
- [ ] All fields mapped to UI components
- [ ] Null/undefined values handled gracefully
- [ ] Confidence badges show correct tier
- [ ] Percentile calculations display (if available)
- [ ] Session history chart renders
- [ ] Milestone detection works

**Branding Checklist:**
- [ ] "Catching Barrels" branding only
- [ ] "Coach Rick AI" messaging
- [ ] "KRS™" (Kinetic Realization Score)
- [ ] NO mention of "Reboot Motion" anywhere
- [ ] Logo/colors match brand guidelines

---

## 🎯 **PHASED ROLLOUT**

### **Phase 1: Video-Only MVP (Week 1-2)**
```
Build UI with mock data first
└─ Test all sections render correctly
└─ Test responsive design
└─ Test loading/error states

Then integrate:
└─ Video upload endpoint
└─ Gemini AI analysis (Motor Profile)
└─ Basic KRS from Coach Rick scores
└─ NO Reboot biomechanics yet (simplified)
```

### **Phase 2: Reboot Integration (Week 3-4)**
```
Add backend processing:
└─ Reboot Motion API integration
└─ CSV data storage
└─ Full KRS calculation (Creation + Transfer)
└─ Detailed biomechanics sections

Frontend updates:
└─ Show detailed kinetic chain scores
└─ Show lead leg measurements
└─ Show capacity vs actual comparisons
```

### **Phase 3: Progress Tracking (Week 5-6)**
```
Add features:
└─ Session-over-session comparison
└─ KRS trend charts
└─ Milestone celebrations
└─ Streak tracking
└─ Level-up animations
```

---

## 📞 **SUPPORT & QUESTIONS**

### **If you need clarification:**

**About UI/UX:**
- Reference the complete UI structure above
- Check visual design requirements
- Review acceptance criteria

**About Data:**
- Reference PlayerReport schema
- All fields documented with types
- Examples provided in schema comments

**About Backend:**
- Ask the 4 integration questions above
- We'll help with KRS calculation
- We'll provide formulas/algorithms

**About Branding:**
- Catching Barrels (company)
- Coach Rick AI (analysis engine)
- KRS™ (the score)
- 4B Framework (Brain, Body, Bat, Ball)

---

## 🚨 **FINAL REMINDERS**

### **DO:**
✅ Follow the schema exactly
✅ Build sections in specified order
✅ Use Catching Barrels branding
✅ Make it mobile-first
✅ Handle loading/error states
✅ Test with real data when available

### **DON'T:**
❌ Reorder sections
❌ Change the KRS calculation approach
❌ Modify the data schema
❌ Show "Reboot Motion" branding
❌ Add extra sections without approval
❌ Deviate from visual design specs

---

## 📋 **NEXT STEPS**

1. **Review this entire document**
2. **Answer the 4 backend integration questions**
3. **Start with Phase 1 (Video-Only MVP)**
4. **Build UI with mock data first**
5. **Test thoroughly before connecting backend**
6. **Integrate real API calls**
7. **Test with real player data**
8. **Deploy Phase 1**
9. **Iterate to Phase 2 & 3**

---

**This is your MASTER SPEC. Refer back to it constantly. Don't deviate.**

**Questions? Ask before implementing, not after.** 🎯
