# Screen 12: Progress Dashboard

**Screen Name:** Progress Dashboard  
**Route:** `/progress`  
**Complexity:** MEDIUM  
**Priority:** P0

**Version:** 2.0  
**Date:** 2025-12-26  
**Status:** Design Specification — Corrected

---

## 📋 Overview

The Progress Dashboard displays the player's KRS journey over time with historical trends, session history, and growth metrics. All KRS values use the **0-100 scale** with **5 levels** (FOUNDATION/BUILDING/DEVELOPING/ADVANCED/ELITE).

**Key Features:**
- KRS Journey Chart (0-100 scale, last 30 days)
- Session History table with KRS scores and subscores
- Growth indicators ("+5 points" format, not percentages)
- Level progression tracking (FOUNDATION → ELITE)
- Creation/Transfer subscore trends (0-100 each)

---

## 🎨 Layout (Mobile-First: 375×812)

```
┌─────────────────────────────────────┐
│  ← Back          Progress       🔔   │  ← Header (64px)
├─────────────────────────────────────┤
│                                     │
│  Your KRS Journey                   │  ← Section Title
│                                     │
│  ┌─────────────────────────────┐    │
│  │ [KRS Line Chart]            │    │  ← KRS Journey Chart (300px)
│  │                             │    │
│  │  100 ┄┄┄┄┄┄┄┄┄┄┄┄┄┄ ELITE  │    │
│  │   85 ┄┄┄┄┄┄┄┄┄┄┄ ADVANCED   │    │
│  │   75 ┄┄┄┄┄┄┄ DEVELOPING     │    │
│  │   60 ┄┄┄ BUILDING           │    │
│  │   40 ┄ FOUNDATION           │    │
│  │    0 ┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄  │    │
│  │     Dec 1   Dec 15  Dec 26  │    │
│  │                             │    │
│  │  Current: 75 (ADVANCED)     │    │
│  │  30-Day Gain: +5 points     │    │
│  └─────────────────────────────┘    │
│                                     │
│  Session History                    │  ← Section Title
│                                     │
│  ┌─────────────────────────────┐    │
│  │ Dec 26, 2024 • 2:30 PM      │    │  ← Session Card (120px)
│  │ KRS: 75 (ADVANCED) +3 ↑     │    │
│  │ Creation: 74.8              │    │
│  │ Transfer: 69.5              │    │
│  │ [View Report →]             │    │
│  └─────────────────────────────┘    │
│                                     │
│  ┌─────────────────────────────┐    │
│  │ Dec 24, 2024 • 10:15 AM     │    │  ← Session Card
│  │ KRS: 72 (DEVELOPING) +2 ↑   │    │
│  │ Creation: 72.5              │    │
│  │ Transfer: 68.0              │    │
│  │ [View Report →]             │    │
│  └─────────────────────────────┘    │
│                                     │
│  ┌─────────────────────────────┐    │
│  │ Dec 20, 2024 • 4:00 PM      │    │  ← Session Card
│  │ KRS: 70 (DEVELOPING) +1 ↑   │    │
│  │ Creation: 70.2              │    │
│  │ Transfer: 66.8              │    │
│  │ [View Report →]             │    │
│  └─────────────────────────────┘    │
│                                     │
│  Stats Summary                      │  ← Section Title
│                                     │
│  ┌──────────┬──────────┬──────────┐ │
│  │ Total    │ Current  │ 30-Day   │ │  ← Stats Grid (100px)
│  │ Swings   │ Level    │ Gain     │ │
│  │          │          │          │ │
│  │   12     │ ADVANCED │  +5      │ │
│  │ sessions │          │ points   │ │
│  └──────────┴──────────┴──────────┘ │
│                                     │
│  Level Progression                  │  ← Section Title
│                                     │
│  ┌─────────────────────────────┐    │
│  │ Current: ADVANCED (75/100)  │    │  ← Progress Card (140px)
│  │                             │    │
│  │ ████████████████████░░░░    │    │  ← Progress Bar (75%)
│  │                             │    │
│  │ Next: ELITE (85/100)        │    │
│  │ Gap: 10 points              │    │
│  │                             │    │
│  │ Keep going! 10 more points  │    │
│  │ to reach ELITE level.       │    │
│  └─────────────────────────────┘    │
│                                     │
│  Creation vs Transfer Trends        │  ← Section Title
│                                     │
│  ┌─────────────────────────────┐    │
│  │ [Dual Line Chart]           │    │  ← Dual Line Chart (250px)
│  │                             │    │
│  │ 100 ┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄   │    │
│  │  75 ─── Creation (74.8)     │    │
│  │  50 ─── Transfer (69.5)     │    │
│  │  25 ┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄   │    │
│  │   0 ┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄   │    │
│  │     Dec 1   Dec 15  Dec 26  │    │
│  │                             │    │
│  │ Creation: +4.5 (30 days)    │    │
│  │ Transfer: +3.2 (30 days)    │    │
│  └─────────────────────────────┘    │
│                                     │
└─────────────────────────────────────┘
│  Home  Upload  Report  More        │  ← Bottom Nav (64px)
└─────────────────────────────────────┘
```

**Viewport Dimensions:**
- **Width:** 375px (mobile), 768px (tablet), 1024px (desktop)
- **Height:** Variable scroll (est. 1800-2200px)
- **Safe Areas:** Top 44px, Bottom 34px
- **Content Area:** 375×734px (mobile)

---

## 🎨 Component Specifications

### **1. Header (64px)**

**Layout:**
```
┌─────────────────────────────────────┐
│  ← Back          Progress       🔔   │
└─────────────────────────────────────┘
```

**Elements:**
- **Back Button:** `<` icon, tap to return to Home
- **Title:** "Progress" (center, 20px semibold, #111827)
- **Notifications Bell:** 🔔 icon (24×24, tap to notifications)

**Styling:**
```css
.header {
  height: 64px;
  background: #FAFAFA;
  border-bottom: 1px solid #E5E7EB;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 16px;
}

.back-button {
  font-size: 16px;
  color: #6B7280;
  cursor: pointer;
}

.title {
  font-size: 20px;
  font-weight: 600;
  color: #111827;
}

.notifications-icon {
  width: 24px;
  height: 24px;
  color: #6B7280;
  cursor: pointer;
}
```

---

### **2. KRS Journey Chart (300px)**

**Purpose:** Display KRS score trend over last 30 days with level thresholds.

**Chart Type:** Line chart with area fill (Recharts)

**Data Points:**
- X-axis: Date (e.g., "Dec 1", "Dec 15", "Dec 26")
- Y-axis: KRS score (0-100)
- Line: Player's KRS progression
- Reference Lines: Level thresholds (40, 60, 75, 85, 100)

**Level Thresholds:**
```
100 ┄┄┄┄┄┄┄┄┄┄┄┄┄┄ ELITE (85-100)
 85 ┄┄┄┄┄┄┄┄┄┄┄ ADVANCED (75-85)
 75 ┄┄┄┄┄┄┄ DEVELOPING (60-75)
 60 ┄┄┄ BUILDING (40-60)
 40 ┄ FOUNDATION (0-40)
  0 ┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄
```

**Chart Summary:**
- **Current KRS:** 75 (ADVANCED)
- **30-Day Gain:** +5 points

**Recharts Configuration:**
```tsx
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine, Area, AreaChart } from 'recharts';

interface KRSDataPoint {
  date: string;          // "Dec 1", "Dec 15", "Dec 26"
  krs: number;           // 70, 72, 75 (0-100 scale)
  creation: number;      // 70.2, 72.5, 74.8
  transfer: number;      // 66.8, 68.0, 69.5
}

const chartData: KRSDataPoint[] = [
  { date: 'Dec 1', krs: 70, creation: 70.2, transfer: 66.8 },
  { date: 'Dec 10', krs: 71, creation: 71.0, transfer: 67.5 },
  { date: 'Dec 20', krs: 72, creation: 72.5, transfer: 68.0 },
  { date: 'Dec 26', krs: 75, creation: 74.8, transfer: 69.5 },
];

<ResponsiveContainer width="100%" height={300}>
  <AreaChart data={chartData}>
    <defs>
      <linearGradient id="krsGradient" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stopColor="#06B6D4" stopOpacity={0.4} />
        <stop offset="100%" stopColor="#06B6D4" stopOpacity={0.1} />
      </linearGradient>
    </defs>
    
    <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
    
    {/* Y-axis: 0-100 */}
    <YAxis 
      domain={[0, 100]} 
      ticks={[0, 40, 60, 75, 85, 100]}
      tickFormatter={(value) => `${value}`}
      stroke="#6B7280"
      style={{ fontSize: '12px' }}
    />
    
    {/* X-axis: Dates */}
    <XAxis 
      dataKey="date" 
      stroke="#6B7280"
      style={{ fontSize: '12px' }}
    />
    
    {/* Level Threshold Lines */}
    <ReferenceLine y={40} stroke="#9CA3AF" strokeDasharray="3 3" label="FOUNDATION" />
    <ReferenceLine y={60} stroke="#9CA3AF" strokeDasharray="3 3" label="BUILDING" />
    <ReferenceLine y={75} stroke="#9CA3AF" strokeDasharray="3 3" label="DEVELOPING" />
    <ReferenceLine y={85} stroke="#9CA3AF" strokeDasharray="3 3" label="ADVANCED" />
    <ReferenceLine y={100} stroke="#9CA3AF" strokeDasharray="3 3" label="ELITE" />
    
    {/* KRS Line */}
    <Area 
      type="monotone" 
      dataKey="krs" 
      stroke="#06B6D4" 
      strokeWidth={3}
      fill="url(#krsGradient)"
    />
    
    {/* Tooltip */}
    <Tooltip 
      contentStyle={{ 
        backgroundColor: '#FFFFFF', 
        border: '1px solid #E5E7EB',
        borderRadius: '8px',
        padding: '8px'
      }}
      formatter={(value: number) => [`${value} KRS`, 'Score']}
    />
  </AreaChart>
</ResponsiveContainer>
```

**Chart Summary Card:**
```tsx
<div className="chart-summary">
  <div className="summary-item">
    <span className="label">Current:</span>
    <span className="value">75 (ADVANCED)</span>
  </div>
  <div className="summary-item">
    <span className="label">30-Day Gain:</span>
    <span className="value success">+5 points ↑</span>
  </div>
</div>
```

**Styling:**
```css
.krs-journey-chart {
  background: #FFFFFF;
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  margin-bottom: 24px;
}

.chart-summary {
  display: flex;
  justify-content: space-around;
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #E5E7EB;
}

.summary-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.summary-item .label {
  font-size: 12px;
  color: #6B7280;
}

.summary-item .value {
  font-size: 18px;
  font-weight: 600;
  color: #111827;
}

.summary-item .value.success {
  color: #10B981;
}
```

---

### **3. Session History (Variable Height)**

**Purpose:** Display recent sessions with KRS scores and subscores.

**Session Card Layout:**
```
┌─────────────────────────────┐
│ Dec 26, 2024 • 2:30 PM      │  ← Date/Time (14px, #6B7280)
│ KRS: 75 (ADVANCED) +3 ↑     │  ← KRS Score (18px semibold, #111827) + Level + Change
│ Creation: 74.8              │  ← Creation subscore (14px, #374151)
│ Transfer: 69.5              │  ← Transfer subscore (14px, #374151)
│ [View Report →]             │  ← Link (14px, #06B6D4)
└─────────────────────────────┘
```

**Data Structure:**
```typescript
interface SessionHistoryItem {
  id: string;                    // "session_abc123"
  date: string;                  // "2024-12-26T14:30:00Z" (ISO 8601)
  krs_total: number;             // 75 (0-100 scale)
  krs_level: string;             // "ADVANCED"
  krs_change: number;            // +3 (points gained since previous session)
  creation_score: number;        // 74.8 (0-100 scale)
  transfer_score: number;        // 69.5 (0-100 scale)
}
```

**React Component:**
```tsx
interface SessionHistoryProps {
  sessions: SessionHistoryItem[];
}

const SessionHistory: React.FC<SessionHistoryProps> = ({ sessions }) => {
  return (
    <div className="session-history">
      <h2 className="section-title">Session History</h2>
      
      {sessions.map((session) => (
        <div key={session.id} className="session-card">
          {/* Date/Time */}
          <div className="session-date">
            {new Date(session.date).toLocaleDateString('en-US', {
              month: 'short',
              day: 'numeric',
              year: 'numeric',
            })} • {new Date(session.date).toLocaleTimeString('en-US', {
              hour: 'numeric',
              minute: '2-digit',
            })}
          </div>
          
          {/* KRS Score */}
          <div className="session-krs">
            <span className="krs-label">KRS:</span>
            <span className="krs-value">{session.krs_total}</span>
            <span className="krs-level">({session.krs_level})</span>
            {session.krs_change > 0 && (
              <span className="krs-change positive">
                +{session.krs_change} ↑
              </span>
            )}
            {session.krs_change < 0 && (
              <span className="krs-change negative">
                {session.krs_change} ↓
              </span>
            )}
            {session.krs_change === 0 && (
              <span className="krs-change neutral">
                —
              </span>
            )}
          </div>
          
          {/* Subscores */}
          <div className="session-subscores">
            <div className="subscore-item">
              <span className="subscore-label">Creation:</span>
              <span className="subscore-value">{session.creation_score.toFixed(1)}</span>
            </div>
            <div className="subscore-item">
              <span className="subscore-label">Transfer:</span>
              <span className="subscore-value">{session.transfer_score.toFixed(1)}</span>
            </div>
          </div>
          
          {/* View Report Link */}
          <a href={`/report/${session.id}`} className="view-report-link">
            View Report →
          </a>
        </div>
      ))}
    </div>
  );
};
```

**Styling:**
```css
.session-history {
  margin-bottom: 32px;
}

.section-title {
  font-size: 20px;
  font-weight: 600;
  color: #111827;
  margin-bottom: 16px;
}

.session-card {
  background: #FFFFFF;
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  margin-bottom: 12px;
}

.session-date {
  font-size: 14px;
  color: #6B7280;
  margin-bottom: 8px;
}

.session-krs {
  font-size: 18px;
  font-weight: 600;
  color: #111827;
  margin-bottom: 8px;
  display: flex;
  align-items: center;
  gap: 6px;
}

.krs-label {
  color: #374151;
}

.krs-value {
  color: #06B6D4;
}

.krs-level {
  font-size: 14px;
  color: #6B7280;
}

.krs-change {
  font-size: 14px;
  margin-left: 4px;
}

.krs-change.positive {
  color: #10B981;
}

.krs-change.negative {
  color: #EF4444;
}

.krs-change.neutral {
  color: #6B7280;
}

.session-subscores {
  display: flex;
  gap: 16px;
  margin-bottom: 12px;
}

.subscore-item {
  font-size: 14px;
  color: #374151;
}

.subscore-label {
  margin-right: 4px;
}

.subscore-value {
  font-weight: 500;
}

.view-report-link {
  font-size: 14px;
  color: #06B6D4;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.view-report-link:hover {
  text-decoration: underline;
}
```

---

### **4. Stats Summary (100px)**

**Purpose:** Display aggregate statistics at a glance.

**Layout:**
```
┌──────────┬──────────┬──────────┐
│ Total    │ Current  │ 30-Day   │
│ Swings   │ Level    │ Gain     │
│          │          │          │
│   12     │ ADVANCED │  +5      │
│ sessions │          │ points   │
└──────────┴──────────┴──────────┘
```

**Data Structure:**
```typescript
interface StatsData {
  total_sessions: number;        // 12
  current_krs: number;           // 75
  current_level: string;         // "ADVANCED"
  thirty_day_gain: number;       // +5 (points gained in last 30 days)
}
```

**React Component:**
```tsx
interface StatsSummaryProps {
  stats: StatsData;
}

const StatsSummary: React.FC<StatsSummaryProps> = ({ stats }) => {
  return (
    <div className="stats-summary">
      <div className="stat-card">
        <div className="stat-label">Total Swings</div>
        <div className="stat-value">{stats.total_sessions}</div>
        <div className="stat-unit">sessions</div>
      </div>
      
      <div className="stat-card">
        <div className="stat-label">Current Level</div>
        <div className="stat-value level">{stats.current_level}</div>
      </div>
      
      <div className="stat-card">
        <div className="stat-label">30-Day Gain</div>
        <div className="stat-value gain">
          {stats.thirty_day_gain > 0 ? '+' : ''}{stats.thirty_day_gain}
        </div>
        <div className="stat-unit">points</div>
      </div>
    </div>
  );
};
```

**Styling:**
```css
.stats-summary {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  margin-bottom: 32px;
}

.stat-card {
  background: #FFFFFF;
  border-radius: 12px;
  padding: 16px;
  text-align: center;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.stat-label {
  font-size: 12px;
  color: #6B7280;
  margin-bottom: 8px;
}

.stat-value {
  font-size: 32px;
  font-weight: 700;
  color: #06B6D4;
  line-height: 1;
}

.stat-value.level {
  font-size: 16px;
  color: #10B981;
}

.stat-value.gain {
  color: #10B981;
}

.stat-unit {
  font-size: 12px;
  color: #6B7280;
  margin-top: 4px;
}
```

---

### **5. Level Progression (140px)**

**Purpose:** Show current KRS level and progress toward next level.

**Layout:**
```
┌─────────────────────────────┐
│ Current: ADVANCED (75/100)  │
│                             │
│ ████████████████████░░░░    │  ← Progress bar (75%)
│                             │
│ Next: ELITE (85/100)        │
│ Gap: 10 points              │
│                             │
│ Keep going! 10 more points  │
│ to reach ELITE level.       │
└─────────────────────────────┘
```

**Data Structure:**
```typescript
interface LevelProgressionData {
  current_krs: number;           // 75
  current_level: string;         // "ADVANCED"
  next_level: string;            // "ELITE"
  next_level_threshold: number;  // 85
  gap: number;                   // 10 (points to next level)
}
```

**React Component:**
```tsx
interface LevelProgressionProps {
  progression: LevelProgressionData;
}

const LevelProgression: React.FC<LevelProgressionProps> = ({ progression }) => {
  const progressPercent = (progression.current_krs / progression.next_level_threshold) * 100;
  
  return (
    <div className="level-progression">
      <h2 className="section-title">Level Progression</h2>
      
      <div className="progression-card">
        {/* Current Level */}
        <div className="current-level">
          <span className="label">Current:</span>
          <span className="value">
            {progression.current_level} ({progression.current_krs}/100)
          </span>
        </div>
        
        {/* Progress Bar */}
        <div className="progress-bar">
          <div 
            className="progress-fill" 
            style={{ width: `${progressPercent}%` }}
          ></div>
        </div>
        
        {/* Next Level */}
        <div className="next-level">
          <div className="next-level-info">
            <span className="label">Next:</span>
            <span className="value">
              {progression.next_level} ({progression.next_level_threshold}/100)
            </span>
          </div>
          <div className="gap-info">
            <span className="label">Gap:</span>
            <span className="value">{progression.gap} points</span>
          </div>
        </div>
        
        {/* Encouragement Message */}
        <div className="encouragement">
          Keep going! {progression.gap} more points to reach {progression.next_level} level.
        </div>
      </div>
    </div>
  );
};
```

**Styling:**
```css
.level-progression {
  margin-bottom: 32px;
}

.progression-card {
  background: #FFFFFF;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.current-level,
.next-level-info,
.gap-info {
  display: flex;
  justify-content: space-between;
  margin-bottom: 12px;
}

.current-level .label,
.next-level-info .label,
.gap-info .label {
  font-size: 14px;
  color: #6B7280;
}

.current-level .value,
.next-level-info .value,
.gap-info .value {
  font-size: 16px;
  font-weight: 600;
  color: #111827;
}

.progress-bar {
  width: 100%;
  height: 12px;
  background: #F3F4F6;
  border-radius: 6px;
  overflow: hidden;
  margin: 16px 0;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #06B6D4 0%, #0284C7 100%);
  transition: width 0.5s ease-in-out;
}

.next-level {
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #E5E7EB;
}

.encouragement {
  font-size: 14px;
  color: #10B981;
  text-align: center;
  margin-top: 16px;
  padding: 12px;
  background: #D1FAE5;
  border-radius: 8px;
}
```

---

### **6. Creation vs Transfer Trends (250px)**

**Purpose:** Display dual line chart comparing Creation and Transfer subscores over time.

**Chart Type:** Dual line chart (Recharts)

**Data Points:**
- X-axis: Date
- Y-axis: Score (0-100)
- Line 1: Creation score (blue)
- Line 2: Transfer score (green)

**Recharts Configuration:**
```tsx
interface TrendsDataPoint {
  date: string;          // "Dec 1", "Dec 15", "Dec 26"
  creation: number;      // 70.2, 72.5, 74.8 (0-100 scale)
  transfer: number;      // 66.8, 68.0, 69.5 (0-100 scale)
}

const trendsData: TrendsDataPoint[] = [
  { date: 'Dec 1', creation: 70.2, transfer: 66.8 },
  { date: 'Dec 10', creation: 71.0, transfer: 67.5 },
  { date: 'Dec 20', creation: 72.5, transfer: 68.0 },
  { date: 'Dec 26', creation: 74.8, transfer: 69.5 },
];

<ResponsiveContainer width="100%" height={250}>
  <LineChart data={trendsData}>
    <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
    
    {/* Y-axis: 0-100 */}
    <YAxis 
      domain={[0, 100]} 
      ticks={[0, 25, 50, 75, 100]}
      stroke="#6B7280"
      style={{ fontSize: '12px' }}
    />
    
    {/* X-axis: Dates */}
    <XAxis 
      dataKey="date" 
      stroke="#6B7280"
      style={{ fontSize: '12px' }}
    />
    
    {/* Creation Line (Blue) */}
    <Line 
      type="monotone" 
      dataKey="creation" 
      stroke="#2563EB" 
      strokeWidth={2}
      dot={{ fill: '#2563EB', r: 4 }}
      name="Creation"
    />
    
    {/* Transfer Line (Green) */}
    <Line 
      type="monotone" 
      dataKey="transfer" 
      stroke="#059669" 
      strokeWidth={2}
      dot={{ fill: '#059669', r: 4 }}
      name="Transfer"
    />
    
    {/* Tooltip */}
    <Tooltip 
      contentStyle={{ 
        backgroundColor: '#FFFFFF', 
        border: '1px solid #E5E7EB',
        borderRadius: '8px',
        padding: '8px'
      }}
    />
    
    {/* Legend */}
    <Legend 
      wrapperStyle={{ paddingTop: '16px' }}
      iconType="line"
    />
  </LineChart>
</ResponsiveContainer>
```

**Chart Summary Card:**
```tsx
<div className="trends-summary">
  <div className="trend-item">
    <span className="trend-label">Creation:</span>
    <span className="trend-value creation">+4.5 (30 days)</span>
  </div>
  <div className="trend-item">
    <span className="trend-label">Transfer:</span>
    <span className="trend-value transfer">+3.2 (30 days)</span>
  </div>
</div>
```

**Styling:**
```css
.creation-transfer-trends {
  background: #FFFFFF;
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  margin-bottom: 24px;
}

.trends-summary {
  display: flex;
  justify-content: space-around;
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #E5E7EB;
}

.trend-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.trend-label {
  font-size: 12px;
  color: #6B7280;
}

.trend-value {
  font-size: 16px;
  font-weight: 600;
}

.trend-value.creation {
  color: #2563EB;
}

.trend-value.transfer {
  color: #059669;
}
```

---

## 🔌 Data Binding & API Specifications

### **API Endpoint**

**GET /api/players/{playerId}/progress**

**Query Parameters:**
- `days` (optional, default: 30): Number of days to include in history (7, 30, 90, 365)

**Request Example:**
```http
GET /api/players/player_abc123/progress?days=30
Authorization: Bearer <token>
```

**Response Schema:**
```typescript
interface ProgressResponse {
  player_id: string;                     // "player_abc123"
  current_krs: number;                   // 75 (0-100 scale)
  current_level: string;                 // "ADVANCED"
  thirty_day_gain: number;               // +5 (points gained in last 30 days)
  
  // KRS Journey Data (for line chart)
  krs_history: KRSDataPoint[];           // Array of KRS scores over time
  
  // Session History
  sessions: SessionHistoryItem[];        // Array of recent sessions
  
  // Stats Summary
  stats: {
    total_sessions: number;              // 12
    current_level: string;               // "ADVANCED"
    thirty_day_gain: number;             // +5
  };
  
  // Level Progression
  progression: {
    current_krs: number;                 // 75
    current_level: string;               // "ADVANCED"
    next_level: string;                  // "ELITE"
    next_level_threshold: number;        // 85
    gap: number;                         // 10
  };
  
  // Trends Data
  trends: {
    creation_history: TrendsDataPoint[]; // Creation scores over time
    transfer_history: TrendsDataPoint[]; // Transfer scores over time
    creation_gain: number;               // +4.5 (30 days)
    transfer_gain: number;               // +3.2 (30 days)
  };
}
```

**Response Example:**
```json
{
  "player_id": "player_abc123",
  "current_krs": 75,
  "current_level": "ADVANCED",
  "thirty_day_gain": 5,
  
  "krs_history": [
    { "date": "Dec 1", "krs": 70, "creation": 70.2, "transfer": 66.8 },
    { "date": "Dec 10", "krs": 71, "creation": 71.0, "transfer": 67.5 },
    { "date": "Dec 20", "krs": 72, "creation": 72.5, "transfer": 68.0 },
    { "date": "Dec 26", "krs": 75, "creation": 74.8, "transfer": 69.5 }
  ],
  
  "sessions": [
    {
      "id": "session_001",
      "date": "2024-12-26T14:30:00Z",
      "krs_total": 75,
      "krs_level": "ADVANCED",
      "krs_change": 3,
      "creation_score": 74.8,
      "transfer_score": 69.5
    },
    {
      "id": "session_002",
      "date": "2024-12-24T10:15:00Z",
      "krs_total": 72,
      "krs_level": "DEVELOPING",
      "krs_change": 2,
      "creation_score": 72.5,
      "transfer_score": 68.0
    },
    {
      "id": "session_003",
      "date": "2024-12-20T16:00:00Z",
      "krs_total": 70,
      "krs_level": "DEVELOPING",
      "krs_change": 1,
      "creation_score": 70.2,
      "transfer_score": 66.8
    }
  ],
  
  "stats": {
    "total_sessions": 12,
    "current_level": "ADVANCED",
    "thirty_day_gain": 5
  },
  
  "progression": {
    "current_krs": 75,
    "current_level": "ADVANCED",
    "next_level": "ELITE",
    "next_level_threshold": 85,
    "gap": 10
  },
  
  "trends": {
    "creation_history": [
      { "date": "Dec 1", "creation": 70.2, "transfer": 66.8 },
      { "date": "Dec 10", "creation": 71.0, "transfer": 67.5 },
      { "date": "Dec 20", "creation": 72.5, "transfer": 68.0 },
      { "date": "Dec 26", "creation": 74.8, "transfer": 69.5 }
    ],
    "creation_gain": 4.5,
    "transfer_gain": 3.2
  }
}
```

---

### **React/TypeScript Implementation**

```tsx
'use client';

import { useEffect, useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine, Area, AreaChart, Legend } from 'recharts';

interface ProgressPageProps {
  playerId: string;
}

const ProgressPage: React.FC<ProgressPageProps> = ({ playerId }) => {
  const [progressData, setProgressData] = useState<ProgressResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchProgress() {
      try {
        setLoading(true);
        
        const response = await fetch(`/api/players/${playerId}/progress?days=30`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('auth_token')}`,
          },
        });

        if (!response.ok) {
          throw new Error(`Failed to fetch progress: ${response.status}`);
        }

        const data = await response.json();
        setProgressData(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error');
      } finally {
        setLoading(false);
      }
    }

    fetchProgress();
  }, [playerId]);

  if (loading) return <div className="loading">Loading progress...</div>;
  if (error) return <div className="error">Error: {error}</div>;
  if (!progressData) return <div className="no-data">No progress data available</div>;

  return (
    <div className="progress-page">
      {/* Header */}
      <header className="header">
        <button className="back-button">← Back</button>
        <h1 className="title">Progress</h1>
        <button className="notifications-icon">🔔</button>
      </header>

      {/* KRS Journey Chart */}
      <section className="krs-journey-chart">
        <h2 className="section-title">Your KRS Journey</h2>
        
        <ResponsiveContainer width="100%" height={300}>
          <AreaChart data={progressData.krs_history}>
            <defs>
              <linearGradient id="krsGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#06B6D4" stopOpacity={0.4} />
                <stop offset="100%" stopColor="#06B6D4" stopOpacity={0.1} />
              </linearGradient>
            </defs>
            
            <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
            <YAxis domain={[0, 100]} ticks={[0, 40, 60, 75, 85, 100]} />
            <XAxis dataKey="date" />
            
            <ReferenceLine y={40} stroke="#9CA3AF" strokeDasharray="3 3" label="FOUNDATION" />
            <ReferenceLine y={60} stroke="#9CA3AF" strokeDasharray="3 3" label="BUILDING" />
            <ReferenceLine y={75} stroke="#9CA3AF" strokeDasharray="3 3" label="DEVELOPING" />
            <ReferenceLine y={85} stroke="#9CA3AF" strokeDasharray="3 3" label="ADVANCED" />
            
            <Area type="monotone" dataKey="krs" stroke="#06B6D4" strokeWidth={3} fill="url(#krsGradient)" />
            <Tooltip />
          </AreaChart>
        </ResponsiveContainer>
        
        <div className="chart-summary">
          <div className="summary-item">
            <span className="label">Current:</span>
            <span className="value">{progressData.current_krs} ({progressData.current_level})</span>
          </div>
          <div className="summary-item">
            <span className="label">30-Day Gain:</span>
            <span className="value success">+{progressData.thirty_day_gain} points ↑</span>
          </div>
        </div>
      </section>

      {/* Session History */}
      <SessionHistory sessions={progressData.sessions} />

      {/* Stats Summary */}
      <StatsSummary stats={progressData.stats} />

      {/* Level Progression */}
      <LevelProgression progression={progressData.progression} />

      {/* Creation vs Transfer Trends */}
      <section className="creation-transfer-trends">
        <h2 className="section-title">Creation vs Transfer Trends</h2>
        
        <ResponsiveContainer width="100%" height={250}>
          <LineChart data={progressData.trends.creation_history}>
            <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
            <YAxis domain={[0, 100]} ticks={[0, 25, 50, 75, 100]} />
            <XAxis dataKey="date" />
            
            <Line type="monotone" dataKey="creation" stroke="#2563EB" strokeWidth={2} name="Creation" />
            <Line type="monotone" dataKey="transfer" stroke="#059669" strokeWidth={2} name="Transfer" />
            
            <Tooltip />
            <Legend />
          </LineChart>
        </ResponsiveContainer>
        
        <div className="trends-summary">
          <div className="trend-item">
            <span className="trend-label">Creation:</span>
            <span className="trend-value creation">+{progressData.trends.creation_gain} (30 days)</span>
          </div>
          <div className="trend-item">
            <span className="trend-label">Transfer:</span>
            <span className="trend-value transfer">+{progressData.trends.transfer_gain} (30 days)</span>
          </div>
        </div>
      </section>

      {/* Bottom Navigation */}
      <nav className="bottom-nav">
        <button className="nav-item">Home</button>
        <button className="nav-item">Upload</button>
        <button className="nav-item">Report</button>
        <button className="nav-item active">More</button>
      </nav>
    </div>
  );
};

export default ProgressPage;
```

---

## 📱 Responsive Behavior

### **Mobile (375px)**
- Single column layout
- Charts: Full width (343px with 16px padding)
- Session cards: Stack vertically
- Stats grid: 3 columns (tight spacing)

### **Tablet (768px)**
- Charts: 720px width
- Session cards: 2 columns
- Stats grid: 3 columns (more spacing)

### **Desktop (1024px+)**
- Max-width: 1200px (centered)
- Charts: 600px width
- Session cards: 3 columns
- Stats grid: 4 columns

**Media Queries:**
```css
/* Mobile-first (default) */
.progress-page {
  padding: 16px;
  max-width: 100%;
}

/* Tablet */
@media (min-width: 768px) {
  .progress-page {
    padding: 24px;
    max-width: 768px;
    margin: 0 auto;
  }
  
  .session-history {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 16px;
  }
  
  .stats-summary {
    grid-template-columns: repeat(4, 1fr);
  }
}

/* Desktop */
@media (min-width: 1024px) {
  .progress-page {
    padding: 32px;
    max-width: 1200px;
  }
  
  .session-history {
    grid-template-columns: repeat(3, 1fr);
  }
  
  .krs-journey-chart,
  .creation-transfer-trends {
    max-width: 800px;
    margin-left: auto;
    margin-right: auto;
  }
}
```

---

## ♿ Accessibility

### **Screen Reader Support**

**Chart Descriptions:**
```tsx
<div 
  role="img" 
  aria-label={`KRS Journey Chart showing progress from ${firstKRS} to ${currentKRS} over ${days} days`}
>
  {/* Chart component */}
</div>
```

**Data Tables:**
```tsx
<table role="table" aria-label="Session History">
  <thead>
    <tr>
      <th scope="col">Date</th>
      <th scope="col">KRS Score</th>
      <th scope="col">Creation</th>
      <th scope="col">Transfer</th>
    </tr>
  </thead>
  <tbody>
    {sessions.map(session => (
      <tr key={session.id}>
        <td>{session.date}</td>
        <td>{session.krs_total}</td>
        <td>{session.creation_score}</td>
        <td>{session.transfer_score}</td>
      </tr>
    ))}
  </tbody>
</table>
```

### **Keyboard Navigation**

- Tab order: Header → Chart → Session cards → Stats → Progression → Trends → Bottom nav
- Focus indicators: 2px solid #06B6D4 outline
- Escape key: Close modals, return to previous view

### **Color Contrast**

- Text on white: #111827 (21:1 contrast ratio) ✅
- Links: #06B6D4 (4.5:1 contrast ratio) ✅
- Success indicators: #10B981 (3:1 contrast ratio) ✅

---

## 🎯 Success Criteria

**Progress Dashboard passes when:**

1. ✅ KRS Journey Chart uses 0-100 scale with level thresholds
2. ✅ Session History shows KRS scores (0-100), levels, and subscores
3. ✅ Growth indicators format: "+5 points" (not "+50 points")
4. ✅ Level progression shows current level and gap to next level
5. ✅ Creation/Transfer trends chart uses 0-100 scale
6. ✅ Complete API spec with GET /api/players/{id}/progress endpoint
7. ✅ React/TypeScript implementation with Recharts
8. ✅ Responsive behavior (mobile/tablet/desktop)
9. ✅ Accessibility (ARIA labels, keyboard nav, screen reader support)

---

## 📊 Implementation Notes

**Libraries Required:**
- Recharts: `npm install recharts`
- Date formatting: `date-fns` (optional, can use native Date)

**API Integration:**
- Polling interval: None (load on page mount)
- Caching: Cache progress data for 5 minutes (reduce API calls)
- Error handling: Show error message if API fails

**Performance:**
- Chart rendering: Use `ResponsiveContainer` for responsive charts
- Session list: Virtual scrolling for 100+ sessions (use `react-window`)
- Image optimization: Lazy load session thumbnails (if added)

---

**Priority:** P0 — High Priority  
**Complexity:** MEDIUM  
**Est. Time:** 6-8 hours (Phase 1)

---

*Last Updated: December 26, 2025*
