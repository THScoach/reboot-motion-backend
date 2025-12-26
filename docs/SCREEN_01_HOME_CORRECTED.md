# 📱 Screen 01: Home Dashboard - CORRECTED VERSION

**Version:** 2.0 (Corrected)  
**Date:** December 26, 2025  
**Device:** Mobile-first (375×812)  
**Status:** Design Specification - VALIDATED

**⚠️ CRITICAL CORRECTIONS APPLIED:**
- KRS display: 0-100 scale with Creation/Transfer subscores
- On Table gain: mph format (available improvement)
- Complete data binding specification
- Responsive behavior defined
- Accessibility notes included

---

## 🎯 Overview

**Purpose:** Central hub for all user activity  
**Entry Point:** After login or from bottom navigation  
**Key Actions:** Upload swing, start Live Mode, view progress, access drills

---

## 📐 Layout Specification

### **Screen Dimensions**
```
Width: 375px (mobile base)
Height: 812px (iPhone 13 Pro)
Safe Area Top: 44px (status bar + notch)
Safe Area Bottom: 34px (home indicator)
Content Area: 375×734px
```

### **Viewport Structure**
```
┌─────────────────────────────────────┐
│ Status Bar (44px)                   │ System
├─────────────────────────────────────┤
│ Header (80px)                       │ Greeting + Profile
├─────────────────────────────────────┤
│ KRS Display Card (240px)            │ ✅ CORRECTED
├─────────────────────────────────────┤
│ Quick Actions (200px)               │ Upload + Live Mode
├─────────────────────────────────────┤
│ 30-Day Progress (180px)             │ ✅ CORRECTED
├─────────────────────────────────────┤
│ Recommended Drills (120px)          │ Personalized
├─────────────────────────────────────┤
│ Spacer (Auto)                       │ Push nav down
├─────────────────────────────────────┤
│ Bottom Navigation (64px)            │ 5 tabs
├─────────────────────────────────────┤
│ Safe Area (34px)                    │ System
└─────────────────────────────────────┘
```

---

## 🧱 Component Breakdown

### **1. Header Section (80px height)**

**Layout:**
```html
<header class="px-4 py-6 bg-gray-50">
  <div class="flex items-center justify-between">
    <!-- Left: Greeting + Name -->
    <div>
      <p class="text-sm text-gray-600">Good morning,</p>
      <h1 class="text-2xl font-bold text-gray-900">Alex</h1>
    </div>
    
    <!-- Right: Notifications + Avatar -->
    <div class="flex items-center gap-3">
      <!-- Notifications -->
      <button class="w-10 h-10 rounded-full bg-white flex items-center justify-center relative">
        <IconBell class="w-5 h-5 text-gray-600" />
        <span class="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
      </button>
      
      <!-- Avatar -->
      <button class="w-10 h-10 rounded-full bg-cyan-500 flex items-center justify-center text-white font-semibold">
        A
      </button>
    </div>
  </div>
</header>
```

**Design Details:**
- Background: `#FAFAFA` (light gray)
- Greeting text: 14px, gray-600
- Name text: 24px, bold, gray-900
- Notification bell: White circle, red dot if unread
- Avatar: Cyan circle with initial

**Interactions:**
- Tap bell → Navigate to Notifications
- Tap avatar → Navigate to Settings

---

## 2. KRS Display Card ✅ CORRECTED

┌─────────────────────────────────────────────────────────┐
│  📊 YOUR LATEST KRS                                     │
│                                                          │
│                    75                                    │  ← 72px (desktop), 56px (mobile), Inter Bold, #06B6D4
│                 ADVANCED                                 │  ← 20px, badge style, white text on #0891B2 bg, 8px radius
│                                                          │
│         Creation: 74.8    Transfer: 69.5                │  ← 16px, #475569 gray
│         +3.1 mph bat speed available                    │  ← 14px, #10B981 green, bold
│                                                          │
│  📅 Dec 25, 2025  •  Session #12  •  15 swings         │  ← 14px, #6B7280 gray
│                                                          │
│  [View Full Report →]                                   │  ← Button, 48px height, cyan accent
└─────────────────────────────────────────────────────────┘

### Layout Specifications
- **Container:** White background (#FFFFFF), 16px padding, 12px border radius, shadow-md
- **KRS Number:** 72px desktop / 56px mobile, font-weight: 700, color: #06B6D4, text-align: center
- **Level Badge:** Inline-block, 20px text, 8px padding horizontal, 4px padding vertical, border-radius: 8px
  - FOUNDATION: #6B7280 bg
  - BUILDING: #F59E0B bg
  - DEVELOPING: #3B82F6 bg
  - ADVANCED: #0891B2 bg
  - ELITE: #7C3AED bg
- **Subscores:** Display flex, justify-content: space-around, 16px text, margin-top: 16px
- **On Table Gain:** 14px text, #10B981 green, font-weight: 600, margin-top: 8px
- **Metadata:** 14px, #6B7280, margin-top: 16px
- **CTA Button:** Full-width, 48px height, #06B6D4 bg, white text, 12px radius, margin-top: 16px

### Data Binding Specification

**API Endpoint:** `GET /api/sessions/latest`

**Response Schema:**
```json
{
  "session_id": "abc123",
  "player_id": "player_001",
  "session_number": 12,
  "date": "2025-12-25",
  "total_swings": 15,
  "krs": {
    "total": 75,
    "level": "ADVANCED",
    "creation": 74.8,
    "transfer": 69.5
  },
  "on_table": {
    "bat_speed_gain": 3.1,
    "exit_velo_gain": 8.5
  }
}
```

**UI Mapping:**
- `krs.total` → "75" (large display number)
- `krs.level` → "ADVANCED" (badge)
- `krs.creation` → "Creation: 74.8"
- `krs.transfer` → "Transfer: 69.5"
- `on_table.bat_speed_gain` → "+3.1 mph bat speed available"
- `date` → "Dec 25, 2025"
- `session_number` → "Session #12"
- `total_swings` → "15 swings"
- `session_id` → Used in "View Full Report" link: `/report/${session_id}`

### HTML/React Implementation

```tsx
<div className="mx-4 mb-4 bg-white rounded-xl p-6 shadow-md">
  {/* Header */}
  <div className="flex items-center gap-2 mb-4">
    <span className="text-lg">📊</span>
    <h2 className="text-sm font-semibold text-gray-600 uppercase tracking-wide">
      YOUR LATEST KRS
    </h2>
  </div>
  
  {/* KRS Score */}
  <div className="text-center mb-4">
    <div 
      className="text-6xl md:text-7xl font-bold text-cyan-500 mb-2"
      aria-label={`Your KRS score is ${krs.total} out of 100, ${krs.level} level`}
    >
      {krs.total}
    </div>
    
    {/* Level Badge */}
    <div 
      className={`inline-block px-3 py-1 rounded-lg text-sm font-semibold text-white ${getLevelBadgeColor(krs.level)}`}
      role="status"
    >
      {krs.level}
    </div>
  </div>
  
  {/* Subscores */}
  <div className="flex justify-around mb-3">
    <div className="text-center">
      <p className="text-xs text-gray-500 mb-1">Creation</p>
      <p className="text-base font-semibold text-gray-700">{krs.creation}</p>
    </div>
    <div className="text-center">
      <p className="text-xs text-gray-500 mb-1">Transfer</p>
      <p className="text-base font-semibold text-gray-700">{krs.transfer}</p>
    </div>
  </div>
  
  {/* On Table Gain */}
  <div 
    className="text-center mb-4"
    aria-label={`You have ${on_table.bat_speed_gain} miles per hour of bat speed improvement available`}
  >
    <p className="text-sm font-semibold text-green-500">
      +{on_table.bat_speed_gain} mph bat speed available
    </p>
  </div>
  
  {/* Metadata */}
  <div className="flex items-center justify-center gap-2 text-sm text-gray-500 mb-4">
    <span>📅 {formatDate(date)}</span>
    <span>•</span>
    <span>Session #{session_number}</span>
    <span>•</span>
    <span>{total_swings} swings</span>
  </div>
  
  {/* CTA Button */}
  <button 
    onClick={() => navigate(`/report/${session_id}`)}
    className="w-full py-3 bg-cyan-500 text-white font-semibold rounded-xl hover:bg-cyan-600 transition"
    aria-label={`View full report for session ${session_number}`}
  >
    View Full Report →
  </button>
</div>
```

### Helper Functions

```typescript
// Level badge color mapping
function getLevelBadgeColor(level: string): string {
  const colors = {
    'FOUNDATION': 'bg-gray-500',
    'BUILDING': 'bg-amber-500',
    'DEVELOPING': 'bg-blue-500',
    'ADVANCED': 'bg-cyan-600',
    'ELITE': 'bg-purple-600'
  };
  return colors[level] || 'bg-gray-500';
}

// Date formatting
function formatDate(dateString: string): string {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', { 
    month: 'short', 
    day: 'numeric', 
    year: 'numeric' 
  });
}
```

### Responsive Behavior
- **Mobile (320-767px):** Single column, KRS number 56px, button full-width
- **Tablet (768-1023px):** Single column, KRS number 64px, max-width: 600px centered
- **Desktop (1024px+):** Single column, KRS number 72px, max-width: 600px centered

### Accessibility
- KRS number: `aria-label="Your KRS score is 75 out of 100, Advanced level"`
- Level badge: `role="status"`
- On Table gain: `aria-label="You have 3.1 miles per hour of bat speed improvement available"`
- View Report button: `aria-label="View full report for session 12"`

---

## 3. 30-Day Progress Card ✅ CORRECTED

┌─────────────────────────────────────────────────────────┐
│  📈 YOUR 30-DAY PROGRESS                                │
│                                                          │
│  KRS Journey: 70 → 75 (+5 points) 📈                   │  ← 18px, bold
│                                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │                                                    │ │
│  │  70   71   72   73   74   75                      │ │  ← Chart x-axis labels
│  │  ▃▄▅▆▇█                                           │ │  ← Bar chart visualization
│  │                                                    │ │
│  │  Dec 1        Dec 15        Dec 25                │ │  ← Date markers
│  └────────────────────────────────────────────────────┘ │
│                                                          │
│  🎯 On track: +0.5 points per week                     │  ← 14px, gray
│                                                          │
│  [View Progress Dashboard →]                            │  ← Button
└─────────────────────────────────────────────────────────┘

### Data Binding Specification

**API Endpoint:** `GET /api/players/{player_id}/progress?days=30`

**Response Schema:**
```json
{
  "player_id": "player_001",
  "date_range": {
    "start": "2025-11-26",
    "end": "2025-12-25"
  },
  "krs_history": [
    { "date": "2025-11-26", "krs": 70 },
    { "date": "2025-12-03", "krs": 71 },
    { "date": "2025-12-10", "krs": 72 },
    { "date": "2025-12-17", "krs": 74 },
    { "date": "2025-12-25", "krs": 75 }
  ],
  "trend": {
    "start_krs": 70,
    "end_krs": 75,
    "change": 5,
    "weekly_average": 0.5
  }
}
```

**UI Mapping:**
- `trend.start_krs` → "70" (start)
- `trend.end_krs` → "75" (end)
- `trend.change` → "+5 points"
- `krs_history[]` → Chart data points (bar chart or line chart)
- `trend.weekly_average` → "+0.5 points per week"

### Chart Specifications
- **Type:** Vertical bar chart or line chart
- **X-axis:** Dates (formatted as "Dec 1", "Dec 15", etc.)
- **Y-axis:** KRS values (0-100 scale, show 60-80 range for zoom)
- **Colors:** 
  - Bars/line: #06B6D4 (cyan)
  - Grid lines: #E2E8F0 (light gray)
  - Latest bar: #0891B2 (darker cyan, highlighted)
- **Height:** 120px
- **Library:** Recharts (React) or Chart.js

### HTML/React Implementation

```tsx
<div className="mx-4 mb-4 bg-white rounded-xl p-6 shadow-md">
  {/* Header */}
  <div className="flex items-center gap-2 mb-4">
    <span className="text-lg">📈</span>
    <h2 className="text-sm font-semibold text-gray-600 uppercase tracking-wide">
      YOUR 30-DAY PROGRESS
    </h2>
  </div>
  
  {/* Journey Summary */}
  <div className="mb-4">
    <p className="text-lg font-bold text-gray-900">
      KRS Journey: {trend.start_krs} → {trend.end_krs} 
      <span className="text-green-500"> (+{trend.change} points)</span> 📈
    </p>
  </div>
  
  {/* Chart */}
  <div className="mb-4">
    <LineChart width={320} height={120} data={krs_history}>
      <XAxis 
        dataKey="date" 
        tickFormatter={(date) => formatChartDate(date)}
        stroke="#9CA3AF"
        style={{ fontSize: '12px' }}
      />
      <YAxis 
        domain={[60, 80]} 
        stroke="#9CA3AF"
        style={{ fontSize: '12px' }}
      />
      <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
      <Line 
        type="monotone" 
        dataKey="krs" 
        stroke="#06B6D4" 
        strokeWidth={3}
        dot={{ fill: '#06B6D4', r: 4 }}
        activeDot={{ r: 6 }}
      />
      <Tooltip />
    </LineChart>
  </div>
  
  {/* Trend Indicator */}
  <div className="mb-4">
    <p className="text-sm text-gray-600">
      🎯 On track: <span className="font-semibold">+{trend.weekly_average} points per week</span>
    </p>
  </div>
  
  {/* CTA Button */}
  <button 
    onClick={() => navigate('/progress')}
    className="w-full py-2.5 bg-gray-100 text-gray-700 font-semibold rounded-lg hover:bg-gray-200 transition"
  >
    View Progress Dashboard →
  </button>
</div>
```

### Helper Functions

```typescript
function formatChartDate(dateString: string): string {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
}
```

---

## 4. Quick Actions

┌─────────────────────────────────────────────────────────┐
│  🎯 QUICK ACTIONS                                       │
│                                                          │
│  ┌──────────────────────┐  ┌──────────────────────┐   │
│  │   📹 UPLOAD          │  │   🎮 LIVE            │   │
│  │   NEW VIDEO          │  │   MODE               │   │
│  │                      │  │                      │   │
│  │   Analyze your       │  │   Real-time          │   │
│  │   swing (240 FPS)    │  │   feedback           │   │
│  └──────────────────────┘  └──────────────────────┘   │
└─────────────────────────────────────────────────────────┘

### Layout Specifications
- **Grid:** 2 columns (mobile: 1 column stacked)
- **Card:** White bg, 16px padding, 12px radius, shadow-sm, hover: shadow-md
- **Icon:** 48px, cyan color
- **Title:** 18px, bold, #0F172A
- **Description:** 14px, #6B7280
- **Touch Target:** Minimum 120px height, full card clickable

### HTML/React Implementation

```tsx
<div className="mx-4 mb-4">
  {/* Header */}
  <div className="flex items-center gap-2 mb-3">
    <span className="text-lg">🎯</span>
    <h2 className="text-sm font-semibold text-gray-600 uppercase tracking-wide">
      QUICK ACTIONS
    </h2>
  </div>
  
  {/* Grid */}
  <div className="grid grid-cols-2 gap-3">
    {/* Upload Card */}
    <button 
      onClick={() => navigate('/upload')}
      className="bg-white rounded-xl p-4 shadow-sm hover:shadow-md transition text-left"
    >
      <div className="text-4xl mb-2">📹</div>
      <h3 className="text-base font-bold text-gray-900 mb-1">UPLOAD</h3>
      <p className="text-xs text-gray-600 mb-2">NEW VIDEO</p>
      <p className="text-xs text-gray-500">Analyze your swing (240 FPS)</p>
    </button>
    
    {/* Live Mode Card */}
    <button 
      onClick={() => navigate('/live')}
      className="bg-white rounded-xl p-4 shadow-sm hover:shadow-md transition text-left"
    >
      <div className="text-4xl mb-2">🎮</div>
      <h3 className="text-base font-bold text-gray-900 mb-1">LIVE</h3>
      <p className="text-xs text-gray-600 mb-2">MODE</p>
      <p className="text-xs text-gray-500">Real-time feedback</p>
    </button>
  </div>
</div>
```

### Actions
- Upload card → Navigate to `/upload`
- Live Mode card → Navigate to `/live`

---

## 5. Recommended Drills

┌─────────────────────────────────────────────────────────┐
│  💪 RECOMMENDED DRILLS                                  │
│                                                          │
│  Based on your Creation gap (74.8/100):                │
│                                                          │
│  • Hip Load Sequence Drill                             │
│    Focus: Body - Creation | 10 reps, 3 sets            │
│                                                          │
│  • Connection Timing Drill                              │
│    Focus: Bat - Transfer | 15 swings                   │
│                                                          │
│  [View All Drills →]                                   │
└─────────────────────────────────────────────────────────┘

### Data Binding Specification

**API Endpoint:** `GET /api/players/{player_id}/recommended-drills`

**Response Schema:**
```json
{
  "player_id": "player_001",
  "drills": [
    {
      "drill_id": "drill_001",
      "name": "Hip Load Sequence Drill",
      "focus_area": "Body - Creation",
      "prescription": "10 reps, 3 sets",
      "reason": "Creation gap (74.8/100)"
    },
    {
      "drill_id": "drill_002",
      "name": "Connection Timing Drill",
      "focus_area": "Bat - Transfer",
      "prescription": "15 swings",
      "reason": "Transfer efficiency below 85%"
    }
  ]
}
```

**UI Mapping:**
- `drills[].name` → Drill title
- `drills[].focus_area` → "Focus: Body - Creation"
- `drills[].prescription` → "10 reps, 3 sets"
- Click → Navigate to `/drills/${drill_id}`

### HTML/React Implementation

```tsx
<div className="mx-4 mb-4 bg-white rounded-xl p-6 shadow-md">
  {/* Header */}
  <div className="flex items-center gap-2 mb-3">
    <span className="text-lg">💪</span>
    <h2 className="text-sm font-semibold text-gray-600 uppercase tracking-wide">
      RECOMMENDED DRILLS
    </h2>
  </div>
  
  {/* Context */}
  <p className="text-sm text-gray-600 mb-4">
    Based on your Creation gap (74.8/100):
  </p>
  
  {/* Drills List */}
  <div className="space-y-3 mb-4">
    {drills.map(drill => (
      <button
        key={drill.drill_id}
        onClick={() => navigate(`/drills/${drill.drill_id}`)}
        className="w-full text-left p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition"
      >
        <h3 className="text-sm font-semibold text-gray-900 mb-1">
          • {drill.name}
        </h3>
        <p className="text-xs text-gray-600">
          Focus: {drill.focus_area} | {drill.prescription}
        </p>
      </button>
    ))}
  </div>
  
  {/* View All Button */}
  <button 
    onClick={() => navigate('/drills')}
    className="w-full py-2.5 bg-gray-100 text-gray-700 font-semibold rounded-lg hover:bg-gray-200 transition"
  >
    View All Drills →
  </button>
</div>
```

---

## 📱 Responsive Behavior Summary

### Mobile (320-767px)
- Single column layout throughout
- KRS number: 56px
- Quick Actions: Stacked (1 column)
- Chart: 320px width max
- Buttons: Full-width

### Tablet (768-1023px)
- Single column, max-width: 600px, centered
- KRS number: 64px
- Quick Actions: 2 columns
- Chart: 520px width max

### Desktop (1024px+)
- Single column, max-width: 600px, centered
- KRS number: 72px
- Quick Actions: 2 columns
- Chart: 560px width max

---

## ♿ Accessibility Summary

- All headings use proper heading tags (`<h1>`, `<h2>`, `<h3>`)
- KRS score has descriptive `aria-label`
- Level badge has `role="status"`
- On Table gain has descriptive `aria-label`
- All buttons have descriptive `aria-label` or clear text content
- Keyboard navigation: Tab through all interactive elements
- Focus indicators: Visible outline on all focusable elements
- Touch targets: Minimum 44×44px (iOS) / 48×48px (Android)

---

## 🎨 Design Token References

**Colors (from design-tokens.json):**
- Primary Cyan: `#06B6D4`
- Cyan Dark: `#0891B2`
- Success Green: `#10B981`
- Warning Amber: `#F59E0B`
- Gray Scale: `#0F172A` (900), `#475569` (600), `#6B7280` (500), `#E2E8F0` (200)

**Typography:**
- KRS Score: 72px (desktop) / 56px (mobile), Inter Bold
- Headings: 18-24px, Inter Semibold/Bold
- Body: 14-16px, Inter Regular
- Captions: 12-14px, Inter Regular

**Spacing:**
- Section gaps: 16px (mobile) / 24px (desktop)
- Card padding: 24px
- Button height: 48px
- Touch target minimum: 44px

**Shadows:**
- Card: shadow-md
- Button hover: shadow-lg

---

## ✅ VALIDATION CHECKLIST

- [x] KRS scale: 0-100 (not 0-1000)
- [x] KRS subscores: Creation 74.8, Transfer 69.5
- [x] On Table gain: +3.1 mph format
- [x] Level badge: ADVANCED (5 levels defined)
- [x] 30-Day Progress: Chart with 0-100 y-axis
- [x] Data binding: Complete API specs
- [x] Responsive: Mobile/tablet/desktop defined
- [x] Accessibility: ARIA labels, keyboard nav
- [x] Color tokens: Match design-tokens.json
- [x] Typography: Match design-tokens.json

---

**STATUS**: ✅ CORRECTED - Ready for Phase 1 implementation
