# 📱 Screen 1: Home Dashboard

**Version:** 1.0  
**Date:** December 26, 2025  
**Device:** Mobile-first (375×812 iPhone 13 Pro)  
**Status:** Design Specification

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
│ Motor Profile Card (120px)          │ Current profile
├─────────────────────────────────────┤
│ KRS Hero Card (200px)               │ Main metric OR
│ OR KRS Prompt (160px)               │ Upload prompt
├─────────────────────────────────────┤
│ Quick Actions (200px)               │ 2×2 grid
├─────────────────────────────────────┤
│ Tips Card (80px)                    │ Daily tip
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
    
    <!-- Right: Streak + Avatar -->
    <div class="flex items-center gap-3">
      <!-- Streak Badge -->
      <div class="flex items-center gap-1 px-3 py-1.5 bg-orange-50 rounded-full">
        <span class="text-lg">🔥</span>
        <span class="text-sm font-semibold text-orange-600">7</span>
      </div>
      
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
- Streak badge: Orange accent (fire emoji + number)
- Avatar: Cyan circle with initial

**Interactions:**
- Tap avatar → Navigate to Settings
- Streak badge is static (shows current week streak)

---

### **2. Motor Profile Card (120px height)**

**Layout:**
```html
<div class="mx-4 mb-4 bg-white rounded-2xl p-4 shadow-md">
  <div class="flex items-center justify-between">
    <!-- Left: Profile Info -->
    <div class="flex items-center gap-3">
      <!-- Icon -->
      <div class="w-12 h-12 rounded-xl bg-purple-50 flex items-center justify-center">
        <span class="text-2xl">🏹</span>
      </div>
      
      <!-- Text -->
      <div>
        <p class="text-xs text-gray-600 mb-0.5">YOUR MOTOR PROFILE</p>
        <h3 class="text-lg font-bold text-gray-900">The Spinner</h3>
        <p class="text-sm text-gray-600">Quick hands, short path</p>
      </div>
    </div>
    
    <!-- Right: Confidence -->
    <div class="text-right">
      <div class="text-2xl font-bold text-purple-600">88%</div>
      <p class="text-xs text-gray-600">Confidence</p>
    </div>
  </div>
</div>
```

**Design Details:**
- Background: White card with shadow
- Border radius: 16px
- Padding: 16px
- Icon: Profile-specific (Spinner = 🏹, Whipper = ⚡, etc.)
- Color accent: Profile-specific (Spinner = purple)
- Confidence badge: Large number + label

**Interactions:**
- Tap card → Navigate to Motor Profile details
- Long press → Option to retake assessment

---

### **3A. KRS Hero Card (200px height) - WITH KRS**

**Shown when:** User has at least one session

**Layout:**
```html
<div class="mx-4 mb-4 bg-gradient-to-br from-cyan-500 to-cyan-600 rounded-2xl p-6 shadow-lg text-white">
  <!-- Header -->
  <div class="flex items-center justify-between mb-4">
    <h2 class="text-xl font-bold">Your KRS</h2>
    <span class="px-3 py-1 bg-white/20 rounded-full text-sm font-semibold">
      ADVANCED ⭐
    </span>
  </div>
  
  <!-- Score Display -->
  <div class="flex items-center justify-between mb-6">
    <!-- Left: Large Score -->
    <div>
      <div class="text-6xl font-bold mb-2">82</div>
      <div class="flex items-center gap-4">
        <div>
          <p class="text-xs opacity-80">Creation</p>
          <p class="text-2xl font-bold">41</p>
        </div>
        <div>
          <p class="text-xs opacity-80">Transfer</p>
          <p class="text-2xl font-bold">41</p>
        </div>
      </div>
    </div>
    
    <!-- Right: Circular Gauge -->
    <div class="relative w-24 h-24">
      <svg viewBox="0 0 100 100" class="transform -rotate-90">
        <circle cx="50" cy="50" r="45" fill="none" stroke="rgba(255,255,255,0.2)" stroke-width="10"/>
        <circle cx="50" cy="50" r="45" fill="none" stroke="white" stroke-width="10" 
                stroke-dasharray="283" stroke-dashoffset="51" stroke-linecap="round"/>
      </svg>
      <div class="absolute inset-0 flex items-center justify-center text-2xl font-bold">82</div>
    </div>
  </div>
  
  <!-- On Table Metrics -->
  <div class="flex items-center gap-6 text-sm">
    <div>
      <p class="opacity-80 mb-1">Bat Speed</p>
      <p class="font-bold text-lg">75 mph</p>
    </div>
    <div>
      <p class="opacity-80 mb-1">Exit Velo</p>
      <p class="font-bold text-lg">88 mph</p>
    </div>
  </div>
</div>
```

**Design Details:**
- Background: Cyan gradient (primary brand color)
- Text: All white
- Level badge: White/20 background, rounded pill
- Large score: 64px font size
- Sub-scores: 24px font size
- Circular gauge: SVG ring (white stroke)
- On-table metrics: 2 columns

**Interactions:**
- Tap card → Navigate to full Report screen
- No swipe actions

---

### **3B. KRS Prompt Card (160px height) - NO KRS YET**

**Shown when:** User has no sessions yet

**Layout:**
```html
<div class="mx-4 mb-4 bg-white border-2 border-dashed border-gray-300 rounded-2xl p-6">
  <!-- Icon -->
  <div class="w-16 h-16 mx-auto mb-4 rounded-full bg-cyan-50 flex items-center justify-center">
    <span class="text-3xl">📊</span>
  </div>
  
  <!-- Text -->
  <h3 class="text-lg font-bold text-gray-900 text-center mb-2">
    Discover Your KRS
  </h3>
  <p class="text-sm text-gray-600 text-center mb-4">
    Upload your first swing to unlock your Kinetic Rotational Score
  </p>
  
  <!-- CTA -->
  <button class="w-full py-3 bg-cyan-500 text-white font-semibold rounded-xl hover:bg-cyan-600">
    Upload Swing Video
  </button>
</div>
```

**Design Details:**
- Background: White
- Border: Dashed, gray
- Icon: Large emoji in circle
- Text: Centered, encouraging
- CTA: Full-width primary button

**Interactions:**
- Tap button → Navigate to Upload screen

---

### **4. Quick Actions Grid (200px height)**

**Layout:**
```html
<div class="mx-4 mb-4">
  <h2 class="text-lg font-bold text-gray-900 mb-3">Quick Actions</h2>
  
  <div class="grid grid-cols-2 gap-3">
    <!-- Live Mode -->
    <button class="bg-white rounded-2xl p-4 shadow-md hover:shadow-lg transition-shadow">
      <div class="w-12 h-12 mb-3 rounded-xl bg-purple-50 flex items-center justify-center">
        <IconCamera class="w-6 h-6 text-purple-600" />
      </div>
      <h3 class="font-semibold text-gray-900 mb-1">Live Mode</h3>
      <p class="text-xs text-gray-600">Real-time feedback</p>
    </button>
    
    <!-- Upload -->
    <button class="bg-white rounded-2xl p-4 shadow-md hover:shadow-lg transition-shadow">
      <div class="w-12 h-12 mb-3 rounded-xl bg-cyan-50 flex items-center justify-center">
        <IconUpload class="w-6 h-6 text-cyan-600" />
      </div>
      <h3 class="font-semibold text-gray-900 mb-1">Upload</h3>
      <p class="text-xs text-gray-600">Analyze a swing</p>
    </button>
    
    <!-- Drills -->
    <button class="bg-white rounded-2xl p-4 shadow-md hover:shadow-lg transition-shadow">
      <div class="w-12 h-12 mb-3 rounded-xl bg-green-50 flex items-center justify-center">
        <IconTarget class="w-6 h-6 text-green-600" />
      </div>
      <h3 class="font-semibold text-gray-900 mb-1">Drills</h3>
      <p class="text-xs text-gray-600">Training plan</p>
    </button>
    
    <!-- Progress -->
    <button class="bg-white rounded-2xl p-4 shadow-md hover:shadow-lg transition-shadow">
      <div class="w-12 h-12 mb-3 rounded-xl bg-orange-50 flex items-center justify-center">
        <IconTrendingUp class="w-6 h-6 text-orange-600" />
      </div>
      <h3 class="font-semibold text-gray-900 mb-1">Progress</h3>
      <p class="text-xs text-gray-600">Your journey</p>
    </button>
  </div>
</div>
```

**Design Details:**
- Grid: 2 columns, 16px gap
- Cards: White background, shadow
- Icons: Colored backgrounds matching action type
- Text: Title + subtitle
- Hover: Elevated shadow

**Interactions:**
- Tap Live Mode → Navigate to Live Mode screen (camera)
- Tap Upload → Navigate to Upload screen
- Tap Drills → Navigate to Drills screen
- Tap Progress → Navigate to Progress screen

---

### **5. Tips Card (80px height)**

**Layout:**
```html
<div class="mx-4 mb-4 bg-blue-50 border border-blue-200 rounded-2xl p-4">
  <div class="flex items-start gap-3">
    <div class="w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center flex-shrink-0">
      <IconLightbulb class="w-4 h-4 text-white" />
    </div>
    <div>
      <h4 class="text-sm font-semibold text-blue-900 mb-1">Daily Tip</h4>
      <p class="text-sm text-blue-700">
        Upload swings from multiple angles to get the best analysis
      </p>
    </div>
  </div>
</div>
```

**Design Details:**
- Background: Light blue tint
- Border: Blue
- Icon: Blue circle with lightbulb
- Text: Blue tones

**Interactions:**
- Static card (no tap action)
- Tip rotates daily

---

### **6. Bottom Navigation (64px height)**

**Layout:**
```html
<nav class="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 px-4 pb-safe">
  <div class="flex items-center justify-around h-16">
    <!-- Home (Active) -->
    <button class="flex flex-col items-center gap-1 text-cyan-500">
      <IconHome class="w-6 h-6" />
      <span class="text-xs font-medium">Home</span>
    </button>
    
    <!-- Live -->
    <button class="flex flex-col items-center gap-1 text-gray-400">
      <IconCamera class="w-6 h-6" />
      <span class="text-xs font-medium">Live</span>
    </button>
    
    <!-- Upload (Center, Larger) -->
    <button class="flex flex-col items-center -mt-4">
      <div class="w-14 h-14 rounded-full bg-cyan-500 flex items-center justify-center shadow-lg">
        <IconPlus class="w-8 h-8 text-white" />
      </div>
      <span class="text-xs font-medium text-gray-600 mt-1">Upload</span>
    </button>
    
    <!-- Progress -->
    <button class="flex flex-col items-center gap-1 text-gray-400">
      <IconTrendingUp class="w-6 h-6" />
      <span class="text-xs font-medium">Progress</span>
    </button>
    
    <!-- Settings -->
    <button class="flex flex-col items-center gap-1 text-gray-400">
      <IconSettings class="w-6 h-6" />
      <span class="text-xs font-medium">Settings</span>
    </button>
  </div>
</nav>
```

**Design Details:**
- Position: Fixed bottom
- Background: White
- Border: Top border, gray
- Active tab: Cyan color
- Inactive tabs: Gray
- Center button: Larger, raised, cyan circle
- Icons: 24px
- Labels: 12px

**Interactions:**
- Tap any tab → Navigate to that screen
- Active tab: Cyan highlight
- Center upload button: Primary action

---

## 📱 Responsive Behavior

### **Tablet (768px+)**
```
Changes:
- Max width: 480px centered
- Larger text sizes
- More padding
- 4-column quick actions (optional)
```

### **Desktop (1024px+)**
```
Changes:
- Max width: 600px centered
- Side navigation instead of bottom
- Larger cards
```

---

## 🎬 Animations & Transitions

### **Page Load**
```css
/* Fade in from bottom */
.card {
  animation: slideUp 300ms ease-out;
}

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
```

### **Quick Action Tap**
```css
.action-card:active {
  transform: scale(0.95);
  transition: transform 100ms ease-out;
}
```

---

## ♿ Accessibility

### **Requirements:**
- [ ] All tap targets minimum 44×44px
- [ ] Color contrast ratio 4.5:1+ for text
- [ ] Focus states visible (2px cyan ring)
- [ ] Screen reader labels on all buttons
- [ ] Semantic HTML structure

### **ARIA Labels:**
```html
<button aria-label="Navigate to Live Mode">
  <IconCamera />
  <span>Live</span>
</button>
```

---

## 🧪 States

### **Loading State**
- Show skeleton loaders for cards
- Header loads first, then cards stagger

### **Empty State**
- No KRS: Show KRS Prompt card
- No Motor Profile: Show assessment prompt

### **Error State**
- Failed to load data: Show retry button
- Network offline: Show offline indicator

---

## 📐 Spacing Specifications

```
Screen padding: 16px (left/right)
Card gap: 16px (vertical)
Section gap: 24px
Component padding: 16-24px
Icon sizes: 20-24px
Touch targets: Minimum 44×44px
```

---

## 🎨 Color Usage

```
Backgrounds:
- Screen: #FAFAFA
- Cards: #FFFFFF
- KRS Hero: Gradient (#06B6D4 to #0891B2)

Text:
- Primary: #1F2937
- Secondary: #6B7280
- On Cyan: #FFFFFF

Accents:
- Primary: #06B6D4 (Cyan)
- Motor Profile: #7C3AED (Purple - if Spinner)
- Streak: #F59E0B (Orange)
```

---

## 🔧 Implementation Notes

### **React Component Structure:**
```typescript
<HomeScreen>
  <Header greeting={greeting} name={name} streak={streak} avatar={avatar} />
  <MotorProfileCard profile={profile} />
  {hasKRS ? (
    <KRSHeroCard krs={krs} />
  ) : (
    <KRSPromptCard onUpload={handleUpload} />
  )}
  <QuickActions />
  <TipsCard tip={dailyTip} />
  <BottomNav activeTab="home" />
</HomeScreen>
```

### **Data Requirements:**
```typescript
interface HomeScreenData {
  user: {
    name: string;
    avatar: string;
    streak: number;
  };
  motorProfile: {
    type: 'Spinner' | 'Whipper' | 'Torquer' | 'Twister';
    confidence: number;
    tagline: string;
  };
  krs?: {
    total: number;
    level: 'Foundation' | 'Building' | 'Developing' | 'Advanced' | 'Elite';
    creationScore: number;
    transferScore: number;
    batSpeed: number;
    exitVelo: number;
  };
  dailyTip: string;
}
```

---

## ✅ Acceptance Criteria

- [ ] All components render correctly
- [ ] Responsive on mobile (375-768px)
- [ ] Smooth animations (60 FPS)
- [ ] Tap targets meet accessibility standards
- [ ] Data loads from API
- [ ] Empty states handled
- [ ] Error states handled
- [ ] Navigation works between screens

---

**Status:** DESIGN COMPLETE  
**Next:** Live Mode Screen

---

*End of Home Dashboard Specification*
