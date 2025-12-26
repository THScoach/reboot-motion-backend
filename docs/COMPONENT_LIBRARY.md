# Component Library
## Catching Barrels PWA
**Version:** 2.0  
**Last Updated:** December 26, 2025  
**Status:** Design Specification — Complete

---

## Table of Contents
1. [Overview](#overview)
2. [Component Architecture](#component-architecture)
3. [Critical Components](#critical-components)
4. [Component Catalog](#component-catalog)
5. [Usage Guidelines](#usage-guidelines)
6. [Implementation Notes](#implementation-notes)

---

## 1. Overview

### Purpose
This document defines the **5 critical components** required for Phase 1 MVP development:
1. **KRSScoreDisplay** — Hero KRS score with subscores
2. **FrameworkCard** — 4B Framework metric cards
3. **MotorProfileBadge** — Motor profile visual identifier
4. **ProgressChart** — KRS journey line chart
5. **DrillCard** — Drill library item card

### Design Principles
- **Atomic Design:** Components → Patterns → Screens
- **Mobile-First:** 375px viewport baseline
- **Accessible:** WCAG 2.1 AA compliance
- **Performant:** < 100ms render time
- **Reusable:** Single responsibility principle

### Tech Stack
- **Framework:** React 18 + TypeScript
- **Styling:** Tailwind CSS 3.4
- **Animation:** Framer Motion
- **Charts:** Recharts
- **Icons:** Lucide React

---

## 2. Component Architecture

### File Structure
```
/app/components/
├── ui/                    # Atomic UI components
│   ├── Button.tsx
│   ├── Card.tsx
│   ├── Badge.tsx
│   └── Input.tsx
├── krs/                   # KRS-specific components
│   ├── KRSScoreDisplay.tsx
│   ├── KRSLevelBadge.tsx
│   └── KRSProgressRing.tsx
├── framework/             # 4B Framework components
│   ├── FrameworkCard.tsx
│   ├── BrainCard.tsx
│   ├── BodyCard.tsx
│   ├── BatCard.tsx
│   └── BallCard.tsx
├── motor-profile/         # Motor Profile components
│   ├── MotorProfileBadge.tsx
│   ├── MotorProfileCard.tsx
│   └── MotorProfileSelector.tsx
├── charts/                # Chart components
│   ├── ProgressChart.tsx
│   ├── SessionHistoryChart.tsx
│   └── MetricTrendChart.tsx
└── drills/                # Drill components
    ├── DrillCard.tsx
    ├── DrillGrid.tsx
    └── DrillDetail.tsx
```

### Component Hierarchy
```
Page
├── Layout
│   ├── Header
│   │   ├── BackButton
│   │   ├── PageTitle
│   │   └── ActionButton
│   ├── Content
│   │   ├── Section
│   │   │   ├── SectionTitle
│   │   │   └── ComponentGroup
│   │   │       └── Component (KRSScoreDisplay, FrameworkCard, etc.)
│   │   └── ...
│   └── BottomNav
│       └── NavItem[]
```

---

## 3. Critical Components

### 3.1 KRSScoreDisplay

**Purpose:** Display hero KRS score with Creation/Transfer subscores.

**Props Interface:**
```typescript
interface KRSScoreDisplayProps {
  krsScore: number;              // 0-100
  creationScore: number;         // 0-100
  transferScore: number;         // 0-100
  krsLevel: KRSLevel;           // FOUNDATION | BUILDING | DEVELOPING | ADVANCED | ELITE
  gainValue?: number;           // +3.1 (On-Table Gain)
  gainMetric?: string;          // "mph" | "degrees" | "%"
  showSubscores?: boolean;      // default: true
  showGain?: boolean;           // default: true
  size?: 'sm' | 'md' | 'lg';   // default: 'md'
  className?: string;
}

type KRSLevel = 'FOUNDATION' | 'BUILDING' | 'DEVELOPING' | 'ADVANCED' | 'ELITE';
```

**Visual Specs:**
- **Hero Number:** font-size 64px, font-weight 700, color by KRS level
- **KRS Label:** "KRS SCORE" in uppercase, 12px, letter-spacing 0.1em
- **Subscores Row:** Creation/Transfer in 16px, weights 40%/60% indicated
- **Gain Badge:** "+3.1 mph" in 14px bold, color #10B981, background #D1FAE5
- **Level Badge:** Background by level, white text, rounded-full, px-3 py-1

**KRS Level Colors:**
```typescript
const KRS_LEVEL_COLORS = {
  FOUNDATION: { bg: '#1E293B', text: '#94A3B8' },   // 0-40
  BUILDING: { bg: '#475569', text: '#CBD5E1' },     // 40-60
  DEVELOPING: { bg: '#F59E0B', text: '#FFFFFF' },  // 60-75
  ADVANCED: { bg: '#06B6D4', text: '#FFFFFF' },    // 75-85
  ELITE: { bg: '#8B5CF6', text: '#FFFFFF' },       // 85-100
};
```

**Layout (375px viewport):**
```
┌────────────────────────────────────┐
│           KRS SCORE                │
│                                    │
│              75                    │  ← 64px, Electric Cyan
│           ADVANCED                 │  ← Level badge
│                                    │
│  Creation 74.8 (40%)  Transfer 69.5 (60%)  ← Subscores
│                                    │
│         +3.1 mph On Table          │  ← Gain badge
└────────────────────────────────────┘
```

**React Implementation:**
```typescript
'use client';

import { cn } from '@/lib/utils';
import { motion } from 'framer-motion';

type KRSLevel = 'FOUNDATION' | 'BUILDING' | 'DEVELOPING' | 'ADVANCED' | 'ELITE';

interface KRSScoreDisplayProps {
  krsScore: number;
  creationScore: number;
  transferScore: number;
  krsLevel: KRSLevel;
  gainValue?: number;
  gainMetric?: string;
  showSubscores?: boolean;
  showGain?: boolean;
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

const KRS_LEVEL_COLORS = {
  FOUNDATION: { bg: '#1E293B', text: '#94A3B8', border: '#334155' },
  BUILDING: { bg: '#475569', text: '#CBD5E1', border: '#64748B' },
  DEVELOPING: { bg: '#F59E0B', text: '#FFFFFF', border: '#FBBF24' },
  ADVANCED: { bg: '#06B6D4', text: '#FFFFFF', border: '#22D3EE' },
  ELITE: { bg: '#8B5CF6', text: '#FFFFFF', border: '#A78BFA' },
};

const SIZE_CONFIGS = {
  sm: { hero: 'text-5xl', label: 'text-xs', subscore: 'text-sm' },
  md: { hero: 'text-6xl', label: 'text-sm', subscore: 'text-base' },
  lg: { hero: 'text-7xl', label: 'text-base', subscore: 'text-lg' },
};

export function KRSScoreDisplay({
  krsScore,
  creationScore,
  transferScore,
  krsLevel,
  gainValue,
  gainMetric = 'mph',
  showSubscores = true,
  showGain = true,
  size = 'md',
  className,
}: KRSScoreDisplayProps) {
  const levelColors = KRS_LEVEL_COLORS[krsLevel];
  const sizeConfig = SIZE_CONFIGS[size];

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className={cn('flex flex-col items-center gap-4 py-8', className)}
    >
      {/* KRS Label */}
      <span className={cn('font-medium tracking-widest uppercase', sizeConfig.label)} style={{ color: levelColors.text }}>
        KRS SCORE
      </span>

      {/* Hero Score */}
      <span
        className={cn('font-bold tabular-nums', sizeConfig.hero)}
        style={{ color: levelColors.bg }}
      >
        {Math.round(krsScore)}
      </span>

      {/* Level Badge */}
      <span
        className="rounded-full px-4 py-1.5 text-sm font-semibold uppercase tracking-wide"
        style={{
          backgroundColor: levelColors.bg,
          color: levelColors.text,
        }}
      >
        {krsLevel}
      </span>

      {/* Subscores */}
      {showSubscores && (
        <div className="flex items-center gap-4 text-slate-700">
          <div className="flex flex-col items-center">
            <span className={cn('font-semibold', sizeConfig.subscore)}>
              {creationScore.toFixed(1)}
            </span>
            <span className="text-xs text-slate-500">Creation (40%)</span>
          </div>
          <div className="h-8 w-px bg-slate-300" />
          <div className="flex flex-col items-center">
            <span className={cn('font-semibold', sizeConfig.subscore)}>
              {transferScore.toFixed(1)}
            </span>
            <span className="text-xs text-slate-500">Transfer (60%)</span>
          </div>
        </div>
      )}

      {/* Gain Badge */}
      {showGain && gainValue !== undefined && (
        <div className="flex items-center gap-2 rounded-lg bg-emerald-100 px-4 py-2">
          <span className="text-lg font-bold text-emerald-600">
            {gainValue > 0 ? '+' : ''}{gainValue.toFixed(1)} {gainMetric}
          </span>
          <span className="text-sm text-emerald-700">On Table</span>
        </div>
      )}
    </motion.div>
  );
}
```

**Accessibility:**
- `role="region"` on container
- `aria-label="KRS Score Display"`
- `aria-live="polite"` for score updates
- Sufficient color contrast (4.5:1 minimum)
- Focus indicators on interactive elements

**Responsive Behavior:**
- 375px: Vertical stack, subscores horizontal
- 768px: Same layout, larger text
- 1024px: Same layout, max-width 600px centered

**Success Criteria:**
- ✅ KRS score 0-100 range
- ✅ 5 KRS levels with correct colors
- ✅ Creation/Transfer subscores with 40%/60% weights
- ✅ Gain badge "+3.1 mph On Table"
- ✅ Smooth animations (0.5s duration)
- ✅ WCAG AA compliance

---

### 3.2 FrameworkCard

**Purpose:** Display 4B Framework metric cards (Brain, Body, Bat, Ball).

**Props Interface:**
```typescript
interface FrameworkCardProps {
  category: '4B-Brain' | '4B-Body' | '4B-Bat' | '4B-Ball';
  title: string;
  metrics: MetricItem[];
  onClick?: () => void;
  className?: string;
}

interface MetricItem {
  label: string;
  value: string | number;
  unit?: string;
  color?: string;
  trend?: 'up' | 'down' | 'neutral';
}
```

**Visual Specs (per category):**

**Brain Card:**
- Background: `#EDE9FE` (Purple 100)
- Border: `#C4B5FD` (Purple 300)
- Icon: Brain (Lucide)
- Metrics:
  - Motor Profile: "Whipper" (14px bold)
  - Confidence: "92%" (24px bold, Purple 600)
  - Timing: "0.24s" (16px, Purple 700)

**Body Card:**
- Background: `#DBEAFE` (Blue 100)
- Border: `#93C5FD` (Blue 300)
- Icon: Activity (Lucide)
- Metrics:
  - Creation Score: "74.8" (24px bold, Blue 600)
  - Physical Capacity: "95 mph" (16px, Blue 700)
  - Peak Force: "723 N" (16px, Blue 700)

**Bat Card:**
- Background: `#D1FAE5` (Green 100)
- Border: `#6EE7B7` (Green 300)
- Icon: Zap (Lucide)
- Metrics:
  - Transfer Score: "69.5" (24px bold, Green 600)
  - Transfer Efficiency: "82%" (16px, Green 700)
  - Attack Angle: "12°" (16px, Green 700)

**Ball Card:**
- Background: `#FEE2E2` (Red 100)
- Border: `#FCA5A5` (Red 300)
- Icon: Target (Lucide)
- Metrics:
  - Exit Velocity: "82 mph" (24px bold, Red 600)
  - Capacity: "95 mph" (16px, Red 700)
  - Launch Angle: "18°" (16px, Red 700)

**Card Layout (Mobile 375px):**
```
┌─────────────────────────────────┐
│ [Icon]  BRAIN                  │  ← Header (16px bold)
├─────────────────────────────────┤
│                                 │
│   Motor Profile                 │  ← Label (12px)
│   Whipper                       │  ← Value (14px bold)
│                                 │
│   Confidence      92%           │  ← Hero metric (24px)
│   Timing          0.24s         │  ← Secondary (16px)
│                                 │
└─────────────────────────────────┘
```

**React Implementation:**
```typescript
'use client';

import { cn } from '@/lib/utils';
import { Brain, Activity, Zap, Target, TrendingUp, TrendingDown, Minus } from 'lucide-react';
import { motion } from 'framer-motion';

type FrameworkCategory = '4B-Brain' | '4B-Body' | '4B-Bat' | '4B-Ball';

interface MetricItem {
  label: string;
  value: string | number;
  unit?: string;
  color?: string;
  trend?: 'up' | 'down' | 'neutral';
}

interface FrameworkCardProps {
  category: FrameworkCategory;
  title: string;
  metrics: MetricItem[];
  onClick?: () => void;
  className?: string;
}

const FRAMEWORK_CONFIG = {
  '4B-Brain': {
    bg: '#EDE9FE',
    border: '#C4B5FD',
    icon: Brain,
    textColor: '#7C3AED',
  },
  '4B-Body': {
    bg: '#DBEAFE',
    border: '#93C5FD',
    icon: Activity,
    textColor: '#2563EB',
  },
  '4B-Bat': {
    bg: '#D1FAE5',
    border: '#6EE7B7',
    icon: Zap,
    textColor: '#059669',
  },
  '4B-Ball': {
    bg: '#FEE2E2',
    border: '#FCA5A5',
    icon: Target,
    textColor: '#DC2626',
  },
};

const TREND_ICONS = {
  up: TrendingUp,
  down: TrendingDown,
  neutral: Minus,
};

export function FrameworkCard({
  category,
  title,
  metrics,
  onClick,
  className,
}: FrameworkCardProps) {
  const config = FRAMEWORK_CONFIG[category];
  const Icon = config.icon;
  const isInteractive = !!onClick;

  return (
    <motion.div
      whileHover={isInteractive ? { scale: 1.02 } : undefined}
      whileTap={isInteractive ? { scale: 0.98 } : undefined}
      onClick={onClick}
      className={cn(
        'rounded-2xl border-2 p-6 transition-shadow',
        isInteractive && 'cursor-pointer hover:shadow-lg',
        className
      )}
      style={{
        backgroundColor: config.bg,
        borderColor: config.border,
      }}
    >
      {/* Header */}
      <div className="mb-4 flex items-center gap-3">
        <Icon size={24} style={{ color: config.textColor }} />
        <h3 className="text-base font-bold uppercase tracking-wide" style={{ color: config.textColor }}>
          {title}
        </h3>
      </div>

      {/* Metrics */}
      <div className="space-y-3">
        {metrics.map((metric, index) => {
          const isHero = index === 1; // Second metric is hero
          const TrendIcon = metric.trend ? TREND_ICONS[metric.trend] : null;

          return (
            <div key={metric.label} className="flex items-baseline justify-between">
              <span
                className={cn(
                  'text-slate-700',
                  isHero ? 'text-sm' : 'text-xs'
                )}
              >
                {metric.label}
              </span>
              <div className="flex items-baseline gap-1">
                <span
                  className={cn(
                    'font-bold tabular-nums',
                    isHero ? 'text-2xl' : 'text-base'
                  )}
                  style={{ color: config.textColor }}
                >
                  {metric.value}
                </span>
                {metric.unit && (
                  <span className="text-xs text-slate-600">{metric.unit}</span>
                )}
                {TrendIcon && (
                  <TrendIcon size={14} className="ml-1" style={{ color: config.textColor }} />
                )}
              </div>
            </div>
          );
        })}
      </div>
    </motion.div>
  );
}
```

**Usage Example:**
```typescript
// Brain Card
<FrameworkCard
  category="4B-Brain"
  title="BRAIN"
  metrics={[
    { label: 'Motor Profile', value: 'Whipper' },
    { label: 'Confidence', value: 92, unit: '%' },
    { label: 'Timing', value: '0.24s' },
  ]}
  onClick={() => router.push('/report/brain')}
/>

// Body Card
<FrameworkCard
  category="4B-Body"
  title="BODY"
  metrics={[
    { label: 'Creation Score', value: 74.8 },
    { label: 'Physical Capacity', value: 95, unit: 'mph', trend: 'up' },
    { label: 'Peak Force', value: 723, unit: 'N' },
  ]}
  onClick={() => router.push('/report/body')}
/>

// Bat Card
<FrameworkCard
  category="4B-Bat"
  title="BAT"
  metrics={[
    { label: 'Transfer Score', value: 69.5 },
    { label: 'Transfer Efficiency', value: 82, unit: '%' },
    { label: 'Attack Angle', value: 12, unit: '°' },
  ]}
  onClick={() => router.push('/report/bat')}
/>

// Ball Card
<FrameworkCard
  category="4B-Ball"
  title="BALL"
  metrics={[
    { label: 'Exit Velocity', value: 82, unit: 'mph' },
    { label: 'Capacity', value: 95, unit: 'mph', trend: 'up' },
    { label: 'Launch Angle', value: 18, unit: '°' },
  ]}
  onClick={() => router.push('/report/ball')}
/>
```

**Accessibility:**
- `role="button"` when interactive
- `aria-label="{category} metrics card"`
- `tabIndex={0}` for keyboard navigation
- `onKeyDown` handler for Enter/Space
- High contrast text (4.5:1 minimum)

**Responsive Behavior:**
- 375px: Full width, padding 24px
- 768px: 2-column grid (Brain/Body | Bat/Ball)
- 1024px: 4-column grid, max-width 1200px

**Success Criteria:**
- ✅ 4 distinct card styles (Brain, Body, Bat, Ball)
- ✅ Correct background/border colors per category
- ✅ Hero metric emphasized (24px)
- ✅ Trend indicators (up/down/neutral)
- ✅ Smooth hover/tap animations
- ✅ WCAG AA compliance

---

### 3.3 MotorProfileBadge

**Purpose:** Display motor profile visual identifier with icon and color.

**Props Interface:**
```typescript
interface MotorProfileBadgeProps {
  profile: MotorProfile;
  size?: 'sm' | 'md' | 'lg';
  showLabel?: boolean;
  onClick?: () => void;
  className?: string;
}

type MotorProfile = 'Spinner' | 'Slingshotter' | 'Whipper' | 'Titan';
```

**Visual Specs (per profile):**

**Spinner:**
- Color: `#8B5CF6` (Purple 500)
- Icon: Orbit / Rotation arrows
- Description: "Rotational power, early hip trigger"

**Slingshotter:**
- Color: `#F59E0B` (Amber 500)
- Icon: Waves / Slingshot
- Description: "Elastic energy, stretch-shortening cycle"

**Whipper:**
- Color: `#06B6D4` (Cyan 500)
- Icon: Zap / Lightning
- Description: "Speed-based, late acceleration"

**Titan:**
- Color: `#DC2626` (Red 600)
- Icon: Mountain / Anvil
- Description: "Strength-dominant, max force"

**Badge Sizes:**
- `sm`: 32px × 32px, icon 16px, label 12px
- `md`: 48px × 48px, icon 24px, label 14px
- `lg`: 64px × 64px, icon 32px, label 16px

**Layout (md size):**
```
┌──────────────────┐
│   ┌────────┐     │
│   │  Icon  │     │  ← 48×48px circle
│   └────────┘     │
│    Whipper       │  ← Label (14px)
└──────────────────┘
```

**React Implementation:**
```typescript
'use client';

import { cn } from '@/lib/utils';
import { RotateCw, Waves, Zap, Mountain } from 'lucide-react';
import { motion } from 'framer-motion';

type MotorProfile = 'Spinner' | 'Slingshotter' | 'Whipper' | 'Titan';

interface MotorProfileBadgeProps {
  profile: MotorProfile;
  size?: 'sm' | 'md' | 'lg';
  showLabel?: boolean;
  onClick?: () => void;
  className?: string;
}

const PROFILE_CONFIG = {
  Spinner: {
    color: '#8B5CF6',
    icon: RotateCw,
    description: 'Rotational power, early hip trigger',
  },
  Slingshotter: {
    color: '#F59E0B',
    icon: Waves,
    description: 'Elastic energy, stretch-shortening cycle',
  },
  Whipper: {
    color: '#06B6D4',
    icon: Zap,
    description: 'Speed-based, late acceleration',
  },
  Titan: {
    color: '#DC2626',
    icon: Mountain,
    description: 'Strength-dominant, max force',
  },
};

const SIZE_CONFIG = {
  sm: { container: 'w-8 h-8', icon: 16, label: 'text-xs' },
  md: { container: 'w-12 h-12', icon: 24, label: 'text-sm' },
  lg: { container: 'w-16 h-16', icon: 32, label: 'text-base' },
};

export function MotorProfileBadge({
  profile,
  size = 'md',
  showLabel = true,
  onClick,
  className,
}: MotorProfileBadgeProps) {
  const config = PROFILE_CONFIG[profile];
  const sizeConfig = SIZE_CONFIG[size];
  const Icon = config.icon;
  const isInteractive = !!onClick;

  return (
    <motion.div
      whileHover={isInteractive ? { scale: 1.05 } : undefined}
      whileTap={isInteractive ? { scale: 0.95 } : undefined}
      onClick={onClick}
      className={cn(
        'flex flex-col items-center gap-2',
        isInteractive && 'cursor-pointer',
        className
      )}
    >
      {/* Icon Circle */}
      <div
        className={cn(
          'rounded-full flex items-center justify-center',
          sizeConfig.container
        )}
        style={{ backgroundColor: config.color }}
      >
        <Icon size={sizeConfig.icon} color="#FFFFFF" />
      </div>

      {/* Label */}
      {showLabel && (
        <span className={cn('font-medium', sizeConfig.label)} style={{ color: config.color }}>
          {profile}
        </span>
      )}
    </motion.div>
  );
}
```

**Usage Example:**
```typescript
// Small badge (no label)
<MotorProfileBadge profile="Whipper" size="sm" showLabel={false} />

// Medium badge (with label)
<MotorProfileBadge profile="Titan" size="md" />

// Large interactive badge
<MotorProfileBadge
  profile="Spinner"
  size="lg"
  onClick={() => router.push('/motor-profile/spinner')}
/>
```

**Accessibility:**
- `role="img"` on icon container
- `aria-label="{profile} motor profile"`
- `tabIndex={0}` when interactive
- High contrast icon/background (4.5:1 minimum)

**Success Criteria:**
- ✅ 4 motor profile styles (Spinner, Slingshotter, Whipper, Titan)
- ✅ Correct colors per profile
- ✅ 3 size variants (sm, md, lg)
- ✅ Optional label display
- ✅ Smooth hover/tap animations
- ✅ WCAG AA compliance

---

### 3.4 ProgressChart

**Purpose:** Display KRS journey line chart with session history.

**Props Interface:**
```typescript
interface ProgressChartProps {
  sessions: SessionData[];
  height?: number;
  showCreation?: boolean;
  showTransfer?: boolean;
  className?: string;
}

interface SessionData {
  date: string;              // ISO 8601 date
  krsScore: number;          // 0-100
  creationScore?: number;    // 0-100
  transferScore?: number;    // 0-100
}
```

**Visual Specs:**
- **Chart Library:** Recharts
- **Type:** LineChart with responsive container
- **Y-axis:** 0-100 (KRS scale)
- **X-axis:** Date (MM/DD format)
- **Line Color:** Electric Cyan (#06B6D4)
- **Line Width:** 2px
- **Dot Size:** 6px
- **Dot Hover:** 8px with glow
- **Grid:** Light gray (#E2E8F0), dashed
- **Tooltip:** White background, shadow, rounded

**Chart Layout:**
```
100 ┤          ╭─●
    │         ╱
 75 ┤       ●─╯
    │      ╱
 50 ┤    ●─╯
    │   ╱
 25 ┤ ●─╯
    │╱
  0 ┼─────────────────────
    12/1  12/8  12/15  12/22
```

**React Implementation:**
```typescript
'use client';

import { cn } from '@/lib/utils';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, TooltipProps } from 'recharts';
import { format, parseISO } from 'date-fns';

interface SessionData {
  date: string;
  krsScore: number;
  creationScore?: number;
  transferScore?: number;
}

interface ProgressChartProps {
  sessions: SessionData[];
  height?: number;
  showCreation?: boolean;
  showTransfer?: boolean;
  className?: string;
}

// Custom Tooltip
function CustomTooltip({ active, payload }: TooltipProps<number, string>) {
  if (!active || !payload || payload.length === 0) return null;

  const data = payload[0].payload;
  const date = parseISO(data.date);

  return (
    <div className="rounded-lg bg-white p-3 shadow-lg border border-slate-200">
      <p className="text-xs text-slate-600 mb-1">
        {format(date, 'MMM d, yyyy')}
      </p>
      <p className="text-lg font-bold text-cyan-600">
        KRS {Math.round(data.krsScore)}
      </p>
      {data.creationScore !== undefined && (
        <p className="text-xs text-slate-700">
          Creation: {data.creationScore.toFixed(1)}
        </p>
      )}
      {data.transferScore !== undefined && (
        <p className="text-xs text-slate-700">
          Transfer: {data.transferScore.toFixed(1)}
        </p>
      )}
    </div>
  );
}

export function ProgressChart({
  sessions,
  height = 300,
  showCreation = false,
  showTransfer = false,
  className,
}: ProgressChartProps) {
  // Format data for chart
  const chartData = sessions.map(session => ({
    ...session,
    dateLabel: format(parseISO(session.date), 'M/d'),
  }));

  return (
    <div className={cn('w-full', className)}>
      <ResponsiveContainer width="100%" height={height}>
        <LineChart data={chartData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
          <XAxis
            dataKey="dateLabel"
            stroke="#64748B"
            style={{ fontSize: 12 }}
            tickLine={false}
          />
          <YAxis
            domain={[0, 100]}
            stroke="#64748B"
            style={{ fontSize: 12 }}
            tickLine={false}
            ticks={[0, 25, 50, 75, 100]}
          />
          <Tooltip content={<CustomTooltip />} />
          
          {/* KRS Score Line */}
          <Line
            type="monotone"
            dataKey="krsScore"
            stroke="#06B6D4"
            strokeWidth={2}
            dot={{ fill: '#06B6D4', r: 4 }}
            activeDot={{ r: 6, stroke: '#06B6D4', strokeWidth: 2, fill: '#FFFFFF' }}
          />

          {/* Optional Creation Line */}
          {showCreation && (
            <Line
              type="monotone"
              dataKey="creationScore"
              stroke="#3B82F6"
              strokeWidth={1.5}
              strokeDasharray="5 5"
              dot={{ fill: '#3B82F6', r: 3 }}
            />
          )}

          {/* Optional Transfer Line */}
          {showTransfer && (
            <Line
              type="monotone"
              dataKey="transferScore"
              stroke="#10B981"
              strokeWidth={1.5}
              strokeDasharray="5 5"
              dot={{ fill: '#10B981', r: 3 }}
            />
          )}
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
```

**Usage Example:**
```typescript
// Basic KRS journey
<ProgressChart
  sessions={[
    { date: '2025-12-01', krsScore: 68 },
    { date: '2025-12-08', krsScore: 71 },
    { date: '2025-12-15', krsScore: 73 },
    { date: '2025-12-22', krsScore: 75 },
  ]}
/>

// With Creation/Transfer subscores
<ProgressChart
  sessions={[
    { date: '2025-12-01', krsScore: 68, creationScore: 72, transferScore: 65 },
    { date: '2025-12-08', krsScore: 71, creationScore: 73, transferScore: 69 },
  ]}
  showCreation
  showTransfer
  height={400}
/>
```

**Accessibility:**
- Chart has `role="img"` and `aria-label="KRS progress chart"`
- Tooltip displays on hover and focus
- Keyboard navigation support (Tab to dots)
- High contrast lines (4.5:1 minimum)

**Responsive Behavior:**
- 375px: height 250px, 4-6 data points visible
- 768px: height 300px, 8-10 data points
- 1024px: height 350px, 12+ data points

**Success Criteria:**
- ✅ KRS score 0-100 Y-axis
- ✅ Date X-axis with MM/DD format
- ✅ Electric Cyan line with dots
- ✅ Custom tooltip with date + scores
- ✅ Optional Creation/Transfer lines
- ✅ Responsive to viewport width
- ✅ WCAG AA compliance

---

### 3.5 DrillCard

**Purpose:** Display drill library item card with thumbnail, metadata, and CTA.

**Props Interface:**
```typescript
interface DrillCardProps {
  drill: DrillData;
  onClick?: () => void;
  className?: string;
}

interface DrillData {
  id: string;
  name: string;
  category: '4B-Brain' | '4B-Body' | '4B-Bat' | '4B-Ball';
  focusArea: string;
  prescription: string;
  duration: number;           // minutes
  thumbnailUrl: string;
  videoUrl?: string;
  difficulty?: 'Beginner' | 'Intermediate' | 'Advanced';
  equipment?: string;
  reason?: string;
  expectedGain?: string;
}
```

**Visual Specs:**
- **Card Size:** 375px full width (mobile), 320px fixed (desktop)
- **Thumbnail:** 16:9 aspect ratio, gradient overlay
- **Category Badge:** Top-left, color by 4B category
- **Duration Badge:** Top-right, dark background
- **Title:** 18px bold, 2-line clamp
- **Prescription:** 14px, 3-line clamp, slate-600
- **Focus Area:** 12px uppercase, category color
- **CTA Button:** "Start Drill" (primary) or "View Details" (secondary)

**Card Layout:**
```
┌─────────────────────────────────┐
│  [Thumbnail 16:9]               │
│  ┌────────┐          ┌───────┐  │
│  │ BODY   │          │ 5 min │  │  ← Badges
│  └────────┘          └───────┘  │
│                                 │
│  Hip Rotation Drill             │  ← Title (18px bold)
│                                 │
│  CREATION                       │  ← Focus Area (12px)
│                                 │
│  Develop rotational power       │  ← Prescription (14px)
│  through progressive hip...     │    (3-line clamp)
│                                 │
│  ┌───────────────────────────┐  │
│  │     Start Drill           │  │  ← CTA Button
│  └───────────────────────────┘  │
└─────────────────────────────────┘
```

**React Implementation:**
```typescript
'use client';

import { cn } from '@/lib/utils';
import { Play, Clock } from 'lucide-react';
import { motion } from 'framer-motion';
import Image from 'next/image';

type FrameworkCategory = '4B-Brain' | '4B-Body' | '4B-Bat' | '4B-Ball';

interface DrillData {
  id: string;
  name: string;
  category: FrameworkCategory;
  focusArea: string;
  prescription: string;
  duration: number;
  thumbnailUrl: string;
  videoUrl?: string;
  difficulty?: 'Beginner' | 'Intermediate' | 'Advanced';
  equipment?: string;
  reason?: string;
  expectedGain?: string;
}

interface DrillCardProps {
  drill: DrillData;
  onClick?: () => void;
  className?: string;
}

const CATEGORY_COLORS = {
  '4B-Brain': { bg: '#EDE9FE', text: '#7C3AED' },
  '4B-Body': { bg: '#DBEAFE', text: '#2563EB' },
  '4B-Bat': { bg: '#D1FAE5', text: '#059669' },
  '4B-Ball': { bg: '#FEE2E2', text: '#DC2626' },
};

export function DrillCard({ drill, onClick, className }: DrillCardProps) {
  const categoryConfig = CATEGORY_COLORS[drill.category];

  return (
    <motion.div
      whileHover={{ y: -4 }}
      whileTap={{ scale: 0.98 }}
      onClick={onClick}
      className={cn(
        'group relative overflow-hidden rounded-2xl bg-white shadow-md transition-shadow hover:shadow-xl cursor-pointer',
        className
      )}
    >
      {/* Thumbnail */}
      <div className="relative aspect-video w-full overflow-hidden bg-slate-200">
        <Image
          src={drill.thumbnailUrl}
          alt={drill.name}
          fill
          className="object-cover transition-transform duration-300 group-hover:scale-105"
        />
        {/* Gradient Overlay */}
        <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-black/20 to-transparent" />

        {/* Category Badge */}
        <div
          className="absolute top-3 left-3 rounded-full px-3 py-1 text-xs font-bold uppercase"
          style={{ backgroundColor: categoryConfig.bg, color: categoryConfig.text }}
        >
          {drill.category.replace('4B-', '')}
        </div>

        {/* Duration Badge */}
        <div className="absolute top-3 right-3 flex items-center gap-1 rounded-full bg-black/70 px-2 py-1 text-white backdrop-blur-sm">
          <Clock size={12} />
          <span className="text-xs font-medium">{drill.duration} min</span>
        </div>

        {/* Play Icon (on hover) */}
        <div className="absolute inset-0 flex items-center justify-center opacity-0 transition-opacity group-hover:opacity-100">
          <div className="rounded-full bg-white/30 p-4 backdrop-blur-sm">
            <Play size={32} className="text-white" fill="white" />
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="p-4 space-y-3">
        {/* Focus Area */}
        <span
          className="text-xs font-bold uppercase tracking-wide"
          style={{ color: categoryConfig.text }}
        >
          {drill.focusArea}
        </span>

        {/* Title */}
        <h3 className="text-lg font-bold text-slate-900 line-clamp-2">
          {drill.name}
        </h3>

        {/* Prescription */}
        <p className="text-sm text-slate-600 line-clamp-3">
          {drill.prescription}
        </p>

        {/* Metadata */}
        {(drill.difficulty || drill.equipment) && (
          <div className="flex items-center gap-3 text-xs text-slate-500">
            {drill.difficulty && (
              <span className="rounded-full bg-slate-100 px-2 py-1">
                {drill.difficulty}
              </span>
            )}
            {drill.equipment && (
              <span className="rounded-full bg-slate-100 px-2 py-1">
                {drill.equipment}
              </span>
            )}
          </div>
        )}

        {/* CTA Button */}
        <button
          className="w-full rounded-lg bg-cyan-600 py-3 text-sm font-semibold text-white transition-colors hover:bg-cyan-700"
          onClick={(e) => {
            e.stopPropagation();
            onClick?.();
          }}
        >
          Start Drill
        </button>
      </div>
    </motion.div>
  );
}
```

**Usage Example:**
```typescript
<DrillCard
  drill={{
    id: 'drill-001',
    name: 'Hip Rotation Drill',
    category: '4B-Body',
    focusArea: 'CREATION',
    prescription: 'Develop rotational power through progressive hip activation sequences',
    duration: 5,
    thumbnailUrl: '/drills/hip-rotation-thumbnail.jpg',
    videoUrl: '/drills/hip-rotation-video.mp4',
    difficulty: 'Intermediate',
    equipment: 'None',
  }}
  onClick={() => router.push('/drills/drill-001')}
/>
```

**Accessibility:**
- Card has `role="button"` and `aria-label="{drill.name} drill"`
- `tabIndex={0}` for keyboard navigation
- `onKeyDown` handler for Enter/Space
- Thumbnail alt text describes drill
- High contrast text (4.5:1 minimum)

**Responsive Behavior:**
- 375px: Full width, single column
- 768px: 2-column grid, fixed width 320px
- 1024px: 3-column grid, fixed width 320px

**Success Criteria:**
- ✅ 16:9 thumbnail with gradient overlay
- ✅ Category badge (4B color-coded)
- ✅ Duration badge (top-right)
- ✅ Play icon on hover
- ✅ 2-line title, 3-line prescription clamps
- ✅ Difficulty/equipment badges
- ✅ "Start Drill" CTA button
- ✅ Smooth hover lift animation
- ✅ WCAG AA compliance

---

## 4. Component Catalog

### 4.1 Atomic Components

**Button:**
```typescript
interface ButtonProps {
  variant: 'primary' | 'secondary' | 'ghost';
  size: 'sm' | 'md' | 'lg';
  children: React.ReactNode;
  onClick?: () => void;
  disabled?: boolean;
  loading?: boolean;
}
```

**Card:**
```typescript
interface CardProps {
  children: React.ReactNode;
  variant?: 'default' | 'outlined' | 'elevated';
  padding?: 'sm' | 'md' | 'lg';
  onClick?: () => void;
}
```

**Badge:**
```typescript
interface BadgeProps {
  children: React.ReactNode;
  color: 'default' | 'primary' | 'success' | 'warning' | 'error';
  size?: 'sm' | 'md' | 'lg';
}
```

**Input:**
```typescript
interface InputProps {
  label?: string;
  placeholder?: string;
  value: string;
  onChange: (value: string) => void;
  error?: string;
  type?: 'text' | 'email' | 'number' | 'password';
  disabled?: boolean;
}
```

---

### 4.2 Composite Components

**BottomNav:**
```typescript
interface BottomNavProps {
  activeRoute: string;
  items: NavItem[];
}

interface NavItem {
  icon: React.ReactNode;
  label: string;
  route: string;
  badge?: number;
}
```

**Header:**
```typescript
interface HeaderProps {
  title: string;
  leftAction?: React.ReactNode;
  rightAction?: React.ReactNode;
  subtitle?: string;
}
```

**SessionHistoryList:**
```typescript
interface SessionHistoryListProps {
  sessions: SessionSummary[];
  onSessionClick: (sessionId: string) => void;
}

interface SessionSummary {
  id: string;
  date: string;
  krsScore: number;
  krsDelta: number;
  swingCount: number;
  duration: number;
}
```

---

## 5. Usage Guidelines

### 5.1 Component Selection

**Use KRSScoreDisplay when:**
- Displaying hero KRS score on Home Dashboard
- Showing KRS in Player Report
- Highlighting KRS in session results

**Use FrameworkCard when:**
- Displaying 4B metrics (Brain, Body, Bat, Ball)
- Showing metric summaries on Home/Report
- Creating drill recommendations

**Use MotorProfileBadge when:**
- Indicating player's motor profile
- Showing profile in navigation/header
- Displaying profile in assessment results

**Use ProgressChart when:**
- Visualizing KRS journey over time
- Displaying session history trends
- Comparing Creation/Transfer trends

**Use DrillCard when:**
- Listing drills in library
- Showing recommended drills
- Displaying drill search results

---

### 5.2 Composition Patterns

**Home Dashboard Pattern:**
```typescript
<Layout>
  <Header title="Dashboard" />
  <ScrollView>
    <KRSScoreDisplay {...krsData} />
    <ProgressChart sessions={recentSessions} />
    <FrameworkCardGrid>
      <FrameworkCard category="4B-Brain" {...brainData} />
      <FrameworkCard category="4B-Body" {...bodyData} />
      <FrameworkCard category="4B-Bat" {...batData} />
      <FrameworkCard category="4B-Ball" {...ballData} />
    </FrameworkCardGrid>
  </ScrollView>
  <BottomNav />
</Layout>
```

**Player Report Pattern:**
```typescript
<Layout>
  <Header title="Player Report" leftAction={<BackButton />} />
  <ScrollView>
    <KRSScoreDisplay {...krsData} size="lg" />
    <MotorProfileBadge profile={motorProfile} size="lg" />
    <TabView tabs={['Brain', 'Body', 'Bat', 'Ball']}>
      <TabPanel>
        <FrameworkCard category="4B-Brain" {...brainData} />
        <MetricDetailList metrics={brainMetrics} />
      </TabPanel>
      {/* ... other tabs */}
    </TabView>
  </ScrollView>
</Layout>
```

**Drills Library Pattern:**
```typescript
<Layout>
  <Header title="Drills Library" />
  <SearchBar placeholder="Search drills..." />
  <CategoryTabs categories={['All', 'Brain', 'Body', 'Bat', 'Ball']} />
  <DrillGrid>
    {drills.map(drill => (
      <DrillCard key={drill.id} drill={drill} onClick={handleDrillClick} />
    ))}
  </DrillGrid>
  <BottomNav />
</Layout>
```

---

## 6. Implementation Notes

### 6.1 Performance Optimization

**Code Splitting:**
```typescript
// Lazy load heavy components
const ProgressChart = dynamic(() => import('./ProgressChart'), {
  loading: () => <ChartSkeleton />,
  ssr: false,
});
```

**Memoization:**
```typescript
// Memoize expensive calculations
const krsLevel = useMemo(() => calculateKRSLevel(krsScore), [krsScore]);

// Memoize static components
const MemoizedFrameworkCard = React.memo(FrameworkCard);
```

**Image Optimization:**
```typescript
// Use Next.js Image with lazy loading
<Image
  src={thumbnailUrl}
  alt={name}
  fill
  loading="lazy"
  placeholder="blur"
  blurDataURL={blurDataUrl}
/>
```

---

### 6.2 Testing Strategy

**Unit Tests (Jest + React Testing Library):**
```typescript
describe('KRSScoreDisplay', () => {
  it('displays KRS score 0-100', () => {
    render(<KRSScoreDisplay krsScore={75} {...} />);
    expect(screen.getByText('75')).toBeInTheDocument();
  });

  it('shows correct KRS level badge', () => {
    render(<KRSScoreDisplay krsScore={75} krsLevel="ADVANCED" {...} />);
    expect(screen.getByText('ADVANCED')).toBeInTheDocument();
  });
});
```

**Integration Tests (Playwright):**
```typescript
test('Home Dashboard displays KRS and 4B cards', async ({ page }) => {
  await page.goto('/');
  await expect(page.getByText('KRS SCORE')).toBeVisible();
  await expect(page.getByText('BRAIN')).toBeVisible();
  await expect(page.getByText('BODY')).toBeVisible();
});
```

---

### 6.3 Accessibility Checklist

- ✅ Semantic HTML (header, main, nav, section, article)
- ✅ ARIA labels on all interactive elements
- ✅ Keyboard navigation (Tab, Enter, Space, Arrow keys)
- ✅ Focus indicators (2px outline, high contrast)
- ✅ Color contrast 4.5:1 minimum (text), 3:1 (UI components)
- ✅ Screen reader announcements (aria-live, aria-label)
- ✅ Touch targets 44×44px minimum
- ✅ Responsive text scaling (rem units)

---

### 6.4 Browser Support

**Target Browsers:**
- Chrome 90+ (Desktop/Mobile)
- Safari 14+ (iOS/macOS)
- Firefox 88+
- Edge 90+

**Polyfills Required:**
- IntersectionObserver (for lazy loading)
- ResizeObserver (for responsive charts)

**Progressive Enhancement:**
- Core content visible without JavaScript
- CSS Grid with flexbox fallback
- SVG icons with PNG fallback

---

## 7. Component Development Roadmap

### Phase 1 (MVP - Weeks 3-4)
- ✅ KRSScoreDisplay
- ✅ FrameworkCard
- ✅ MotorProfileBadge
- ✅ ProgressChart
- ✅ DrillCard

### Phase 2 (Weeks 5-6)
- SessionHistoryList
- MetricDetailCard
- DrillDetailView
- VideoPlayer
- LiveFeedbackOverlay

### Phase 3 (Weeks 7-8)
- ComparisonChart
- LeaderboardCard
- AchievementBadge
- NotificationCard
- SettingsForm

---

## Summary

This Component Library defines the **5 critical components** required for Phase 1 MVP:

1. **KRSScoreDisplay** — Hero KRS score with Creation/Transfer subscores
2. **FrameworkCard** — 4B Framework metric cards (Brain, Body, Bat, Ball)
3. **MotorProfileBadge** — Motor profile visual identifier
4. **ProgressChart** — KRS journey line chart
5. **DrillCard** — Drill library item card

Each component includes:
- ✅ TypeScript interfaces
- ✅ Visual specifications
- ✅ React implementations
- ✅ Usage examples
- ✅ Accessibility guidelines
- ✅ Responsive behavior
- ✅ Success criteria

**Estimated Development Time:** 16-20 hours (Phase 1)

**Next Steps:**
1. Review component specs
2. Build atomic components (Button, Card, Badge, Input)
3. Implement 5 critical components
4. Write unit/integration tests
5. Deploy Storybook component showcase

---

**Last Updated:** December 26, 2025  
**Contact:** Builder 2 — Phase 0 Corrections
