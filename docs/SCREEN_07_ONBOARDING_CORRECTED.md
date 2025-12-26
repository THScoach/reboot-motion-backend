# Screen 07: Onboarding - CORRECTED VERSION

**Version:** 2.0 (Corrected)  
**Date:** December 26, 2025  
**Route**: `/onboarding/[step]` (steps 1-4)  
**Complexity**: MEDIUM (4-screen flow)  
**Priority**: P0 (Critical Path)

**⚠️ CRITICAL CORRECTIONS APPLIED:**
- 4 screens (was 3): "What is KRS?", "Motor Profiles", "Two Modes", "Track Progress"
- KRS scale: 0-100 explained in Screen 1
- Motor Profiles: 4 types only (Spinner/Slingshotter/Whipper/Titan) in Screen 2
- Live Mode limitations: Positional feedback only (Screen 3)
- Progress chart: 0-100 KRS scale (Screen 4)

---

## 📐 Flow Overview

```
Onboarding Screen 1: "What is KRS?"
    ↓
Onboarding Screen 2: "Motor Profiles"
    ↓
Onboarding Screen 3: "Two Modes"
    ↓
Onboarding Screen 4: "Track Progress"
    ↓
Create Profile (Screen 08)
```

---

## 🎯 Screen 1: "What is KRS?"

### Purpose
Explain the KRS scoring system (0-100 scale) with Creation and Transfer subscores.

### Layout
```
┌───────────────────────────────────────────┐
│                          Skip →           │ ← Skip button
├───────────────────────────────────────────┤
│                                           │
│            [Icon: 📊]                     │ ← 96px icon
│                                           │
│        What is KRS?                       │ ← Heading-01 (32px)
│                                           │
│    Your Kinetic Readiness Score          │ ← Body-01 (16px)
│    measures how efficiently you           │   Gray-600
│    generate and transfer power            │
│    through your swing.                    │
│                                           │
│  ┌─────────────────────────────────────┐ │
│  │                                     │ │
│  │      [━━━━━━━━━░░░░] 75%           │ │ ← Visual scale
│  │       0   40   60   75   85   100  │ │   0-100 markers
│  │    FOUND BUILD DEV  ADV  ELITE     │ │   5 levels
│  │                                     │ │
│  └─────────────────────────────────────┘ │
│                                           │
│    ✓ Creation Score (0-100)              │ ← Key components
│      How well you generate power          │
│                                           │
│    ✓ Transfer Score (0-100)              │
│      How efficiently you use it           │
│                                           │
│    ✓ "On Table" Gain                     │
│      Your untapped potential              │
│                                           │
│            ● ○ ○ ○                        │ ← Progress dots (1 of 4)
│                                           │
│          [Next]                           │ ← Primary button
│                                           │
└───────────────────────────────────────────┘
```

### Content Specifications

**Icon**: 📊 (96×96px, Electric Cyan #06B6D4)

**Heading**: "What is KRS?"  
- Font: Inter, 32px, bold (700)
- Color: Gray-900 (#111827)
- Alignment: Center

**Body Text**: 
"Your Kinetic Readiness Score measures how efficiently you generate and transfer power through your swing."
- Font: Inter, 16px, regular (400)
- Color: Gray-600 (#6B7280)
- Line height: 24px
- Alignment: Center

**KRS Scale Visual**:
- Progress bar showing 0-100 scale
- Example score: 75 (marker on bar)
- Labels at: 0, 40, 60, 75, 85, 100
- Level names: FOUND (Foundation), BUILD (Building), DEV (Developing), ADV (Advanced), ELITE
- Colors: Gray (0-40), Blue (40-60), Green (60-75), Amber (75-85), Purple (85-100)

**Key Components** (3 bullets with checkmarks):
1. **Creation Score (0-100)**  
   "How well you generate power"  
   - Checkmark: Green (#10B981)
   - Text: 14px, Gray-700
   
2. **Transfer Score (0-100)**  
   "How efficiently you use it"  
   - Checkmark: Green (#10B981)
   - Text: 14px, Gray-700
   
3. **"On Table" Gain**  
   "Your untapped potential"  
   - Checkmark: Green (#10B981)
   - Text: 14px, Gray-700

**Progress Dots**: ● ○ ○ ○ (Step 1 of 4 active)

**Button**: "Next" (Primary, Cyan #06B6D4, full-width, 48px height)

---

## 🎯 Screen 2: "Motor Profiles"

### Purpose
Introduce the 4 Motor Profile types with characteristics.

### Layout
```
┌───────────────────────────────────────────┐
│      ← Back                  Skip →       │ ← Navigation
├───────────────────────────────────────────┤
│                                           │
│            [Icon: 🏹]                     │ ← 96px icon
│                                           │
│        Motor Profiles                     │ ← Heading-01 (32px)
│                                           │
│    Discover your unique swing DNA.        │ ← Body-01 (16px)
│    There are 4 primary profiles:          │
│                                           │
│  ┌───────────────────────────────────┐   │
│  │  🏹 Spinner                       │   │ ← Profile 1
│  │  Upper body rotation specialist   │   │
│  │  Examples: Mookie Betts           │   │
│  └───────────────────────────────────┘   │
│                                           │
│  ┌───────────────────────────────────┐   │
│  │  🎯 Slingshotter                  │   │ ← Profile 2
│  │  Balanced power + contact         │   │
│  │  Examples: Fernando Tatis Jr.     │   │
│  └───────────────────────────────────┘   │
│                                           │
│  ┌───────────────────────────────────┐   │
│  │  ⚡ Whipper                        │   │ ← Profile 3
│  │  Explosive hip rotation           │   │
│  │  Examples: Aaron Judge            │   │
│  └───────────────────────────────────┘   │
│                                           │
│  ┌───────────────────────────────────┐   │
│  │  💪 Titan                         │   │ ← Profile 4
│  │  Strength-dominant                │   │
│  │  Examples: Giancarlo Stanton      │   │
│  └───────────────────────────────────┘   │
│                                           │
│    You'll discover yours after           │ ← Note
│    completing the Movement Assessment.    │
│                                           │
│            ○ ● ○ ○                        │ ← Progress dots (2 of 4)
│                                           │
│          [Next]                           │ ← Primary button
│                                           │
└───────────────────────────────────────────┘
```

### Content Specifications

**Icon**: 🏹 (96×96px, Electric Cyan #06B6D4)

**Heading**: "Motor Profiles"  
- Font: Inter, 32px, bold (700)
- Color: Gray-900 (#111827)

**Body Text**: "Discover your unique swing DNA. There are 4 primary profiles:"

**4 Profile Cards** (verify only 4, not 6):

1. **Spinner** 🏹
   - Title: "Spinner" (16px, bold, Gray-900)
   - Description: "Upper body rotation specialist"
   - Example: "Examples: Mookie Betts, José Altuve"
   - Background: White, border Gray-200, 12px radius
   - Padding: 16px

2. **Slingshotter** 🎯
   - Title: "Slingshotter" (16px, bold, Gray-900)
   - Description: "Balanced power + contact"
   - Example: "Examples: Fernando Tatis Jr., Ronald Acuña Jr."
   - Background: White, border Gray-200, 12px radius
   - Padding: 16px

3. **Whipper** ⚡
   - Title: "Whipper" (16px, bold, Gray-900)
   - Description: "Explosive hip rotation"
   - Example: "Examples: Aaron Judge, Juan Soto"
   - Background: White, border Gray-200, 12px radius
   - Padding: 16px

4. **Titan** 💪
   - Title: "Titan" (16px, bold, Gray-900)
   - Description: "Strength-dominant"
   - Example: "Examples: Giancarlo Stanton, Pete Alonso"
   - Background: White, border Gray-200, 12px radius
   - Padding: 16px

**Note**: "You'll discover yours after completing the Movement Assessment."  
- Font: 14px, Gray-600, center-aligned

**Progress Dots**: ○ ● ○ ○ (Step 2 of 4 active)

**Buttons**: "Back" (Ghost, left) + "Next" (Primary, right)

---

## 🎯 Screen 3: "Two Modes"

### Purpose
Explain Live Mode (60 FPS, positional feedback) vs KRS Mode (240 FPS, full analysis).

### Layout
```
┌───────────────────────────────────────────┐
│      ← Back                  Skip →       │
├───────────────────────────────────────────┤
│                                           │
│            [Icon: 🎮]                     │ ← 96px icon
│                                           │
│          Two Ways to Train                │ ← Heading-01 (32px)
│                                           │
│    Choose the right mode for your         │ ← Body-01
│    training session.                      │
│                                           │
│  ┌───────────────────────────────────┐   │
│  │  🎮 Live Mode                     │   │ ← Mode 1
│  │                                   │   │
│  │  Daily Practice Feedback          │   │
│  │  • 60 FPS camera (standard)       │   │
│  │  • Real-time positional feedback  │   │
│  │  • Hip rotation, knee bend, etc.  │   │
│  │  • ⚠️ No exit velo or launch angle│   │
│  │                                   │   │
│  │  Perfect for: Daily reps          │   │
│  └───────────────────────────────────┘   │
│                                           │
│  ┌───────────────────────────────────┐   │
│  │  📊 KRS Analysis Mode             │   │ ← Mode 2
│  │                                   │   │
│  │  Full Biomechanical Analysis      │   │
│  │  • 240 FPS video required         │   │
│  │  • Complete KRS calculation       │   │
│  │  • Exit velo, bat speed, angles   │   │
│  │  • 4B Framework breakdown         │   │
│  │                                   │   │
│  │  Perfect for: Performance tracking│   │
│  └───────────────────────────────────┘   │
│                                           │
│            ○ ○ ● ○                        │ ← Progress dots (3 of 4)
│                                           │
│          [Next]                           │ ← Primary button
│                                           │
└───────────────────────────────────────────┘
```

### Content Specifications

**Icon**: 🎮 (96×96px, Electric Cyan #06B6D4)

**Heading**: "Two Ways to Train"  
- Font: Inter, 32px, bold (700)

**Body Text**: "Choose the right mode for your training session."

**Mode 1: Live Mode** 🎮
- **Title**: "Live Mode" (18px, bold, Gray-900)
- **Subtitle**: "Daily Practice Feedback" (14px, Cyan-600)
- **Features** (14px, Gray-700, bullet list):
  - 60 FPS camera (standard)
  - Real-time positional feedback
  - Hip rotation, knee bend, posture
  - ⚠️ **No exit velo or launch angle** (Warning text, Amber-600)
- **Use Case**: "Perfect for: Daily reps" (14px, Gray-600, italic)
- **Background**: Light Cyan tint (#DBEAFE)
- **Border**: Cyan-200
- **Padding**: 20px

**Mode 2: KRS Analysis Mode** 📊
- **Title**: "KRS Analysis Mode" (18px, bold, Gray-900)
- **Subtitle**: "Full Biomechanical Analysis" (14px, Purple-600)
- **Features** (14px, Gray-700, bullet list):
  - 240 FPS video required
  - Complete KRS calculation (0-100)
  - Exit velo, bat speed, angles
  - 4B Framework breakdown
- **Use Case**: "Perfect for: Performance tracking" (14px, Gray-600, italic)
- **Background**: Light Purple tint (#EDE9FE)
- **Border**: Purple-200
- **Padding**: 20px

**Progress Dots**: ○ ○ ● ○ (Step 3 of 4 active)

**Buttons**: "Back" (Ghost) + "Next" (Primary)

---

## 🎯 Screen 4: "Track Progress"

### Purpose
Show KRS journey visualization and 5 levels.

### Layout
```
┌───────────────────────────────────────────┐
│      ← Back                               │
├───────────────────────────────────────────┤
│                                           │
│            [Icon: 📈]                     │ ← 96px icon
│                                           │
│        Track Your Journey                 │ ← Heading-01 (32px)
│                                           │
│    Watch your KRS grow over time          │ ← Body-01
│    as you train and improve.              │
│                                           │
│  ┌───────────────────────────────────┐   │
│  │                                   │   │
│  │  85  ┌─────────────────────────┐ │   │ ← Chart visualization
│  │      │                   ┌─────┤ │   │   Y-axis: 0-100 KRS
│  │  80  │             ┌─────┘     │ │   │
│  │      │       ┌─────┘           │ │   │
│  │  75  │ ┌─────┘                 │ │   │
│  │      └─┘                       │ │   │
│  │  70  Week 1   Week 2   Week 3  │   │   X-axis: Time
│  │                                   │   │
│  └───────────────────────────────────┘   │
│                                           │
│  Your KRS Journey: 70 → 85 (+15) 📈      │ ← Progress summary
│                                           │
│  ┌──────────┬──────────┬──────────┐      │
│  │   FOUND  │   BUILD  │   DEV    │      │ ← 5 Levels
│  │   0-40   │   40-60  │   60-75  │      │
│  └──────────┴──────────┴──────────┘      │
│  ┌──────────┬──────────┐                 │
│  │    ADV   │   ELITE  │                 │
│  │   75-85  │  85-100  │                 │
│  └──────────┴──────────┘                 │
│                                           │
│    Every swing brings you closer          │ ← Motivational text
│    to your potential. Let's start!        │
│                                           │
│            ○ ○ ○ ●                        │ ← Progress dots (4 of 4)
│                                           │
│      [Start Movement Assessment]          │ ← Primary button (CTA)
│                                           │
└───────────────────────────────────────────┘
```

### Content Specifications

**Icon**: 📈 (96×96px, Electric Cyan #06B6D4)

**Heading**: "Track Your Journey"  
- Font: Inter, 32px, bold (700)

**Body Text**: "Watch your KRS grow over time as you train and improve."

**Chart Visualization**:
- **Type**: Line chart showing KRS progression
- **Y-Axis**: 0-100 KRS scale (show range 65-90 for zoom)
  - Labels: 70, 75, 80, 85 (example)
  - **⚠️ Verify NOT 0-1000 scale**
- **X-Axis**: Time periods (Week 1, Week 2, Week 3)
- **Line**: Cyan (#06B6D4), 3px width
- **Data Points**: Dots at each week
- **Example trend**: 70 → 75 → 82 → 85 (gradual improvement)
- **Size**: 320px width × 120px height
- **Background**: White with light grid lines

**Progress Summary**:
"Your KRS Journey: 70 → 85 (+15) 📈"
- Font: 16px, bold, Gray-900
- Highlight change in Green (#10B981)
- Center-aligned

**5 Levels Table**:
```
┌──────────┬──────────┬──────────┐
│ FOUNDATION│ BUILDING │ DEVELOPING│
│   0-40    │  40-60   │  60-75   │
│  Gray-500 │ Blue-500 │ Green-500│
└──────────┴──────────┴──────────┘
┌──────────┬──────────┐
│ ADVANCED │  ELITE   │
│  75-85   │ 85-100   │
│ Amber-500│Purple-500│
└──────────┴──────────┘
```
- Each cell: 14px, bold, center-aligned
- Level name: Uppercase
- Range: Below name
- Color-coded borders

**Motivational Text**:
"Every swing brings you closer to your potential. Let's start!"
- Font: 16px, Gray-600
- Center-aligned

**Progress Dots**: ○ ○ ○ ● (Step 4 of 4 active)

**Button**: "Start Movement Assessment" (Primary, Cyan, full-width, 48px height)
- Action: Navigate to `/assessment` (Movement Assessment screen)

---

## 🎨 Visual Specifications

### Layout Container
```css
max-width: 480px;
margin: 0 auto;
padding: 32px 24px;
min-height: 100vh;
display: flex;
flex-direction: column;
justify-content: space-between;
background: #FAFAFA; /* Gray-50 */
```

### Top Navigation
```css
display: flex;
justify-content: space-between;
align-items: center;
height: 44px;
margin-bottom: 40px;
```

**Back Button** (Ghost):
```css
color: #6B7280; /* Gray-500 */
font-size: 16px;
padding: 8px 12px;
border-radius: 8px;
transition: background 0.2s;
```
```css
&:hover {
  background: #F3F4F6; /* Gray-100 */
}
```

**Skip Button** (Ghost):
```css
color: #06B6D4; /* Cyan-500 */
font-size: 16px;
padding: 8px 12px;
border-radius: 8px;
```

### Icon Area
```css
display: flex;
justify-content: center;
align-items: center;
margin-bottom: 32px;
```

**Icon Container**:
- Size: 96px × 96px
- Background: White circle
- Border: 2px solid Gray-200
- Box shadow: shadow-md
- Padding: 20px
- Icon size: 56px, Cyan-500

### Heading
```css
font-family: 'Inter', sans-serif;
font-weight: 700; /* Bold */
font-size: 32px;
line-height: 40px;
color: #111827; /* Gray-900 */
text-align: center;
margin-bottom: 16px;
```

### Body Text
```css
font-family: 'Inter', sans-serif;
font-weight: 400; /* Regular */
font-size: 16px;
line-height: 24px;
color: #6B7280; /* Gray-600 */
text-align: center;
margin-bottom: 32px;
max-width: 400px;
margin-left: auto;
margin-right: auto;
```

### KRS Scale Visual (Screen 1)
```css
background: #FFFFFF;
border: 1px solid #E5E7EB; /* Gray-200 */
border-radius: 12px;
padding: 24px;
margin-bottom: 24px;
```

**Progress Bar**:
- Height: 12px
- Border radius: 6px
- Background: Gray-200
- Fill: Gradient (Gray → Blue → Green → Amber → Purple based on score position)
- Marker: Small dot indicating current score (e.g., 75)

**Labels**:
- Font: 12px, Gray-600
- Position: Below bar
- Values: 0, 40, 60, 75, 85, 100
- Level names: FOUND, BUILD, DEV, ADV, ELITE (uppercase, 10px)

### Component List (Screens 1, 2)
```css
list-style: none;
padding: 0;
margin-bottom: 32px;
```

**Each Item**:
```css
display: flex;
align-items: flex-start;
gap: 12px;
padding: 12px 0;
font-size: 14px;
line-height: 20px;
```

**Checkmark Icon**:
- Size: 20px circle
- Background: Green-100
- Icon: Green-500 check (16px)

**Text**:
- Title: 14px, bold, Gray-900
- Description: 14px, regular, Gray-600

### Profile Cards (Screen 2)
```css
background: #FFFFFF;
border: 1px solid #E5E7EB; /* Gray-200 */
border-radius: 12px;
padding: 16px;
margin-bottom: 12px;
transition: all 0.2s;
```

```css
&:hover {
  border-color: #06B6D4; /* Cyan-500 */
  box-shadow: 0 4px 12px rgba(6, 182, 212, 0.1);
}
```

**Icon + Title**:
- Display: Flex, gap 12px
- Icon: 24px emoji
- Title: 16px, bold, Gray-900

**Description**:
- Font: 14px, Gray-600
- Margin-top: 4px

**Example Athletes**:
- Font: 12px, Gray-500
- Margin-top: 8px
- Italic

### Mode Cards (Screen 3)
```css
background: #FFFFFF; /* or tinted */
border: 2px solid transparent;
border-radius: 12px;
padding: 20px;
margin-bottom: 16px;
transition: all 0.2s;
```

**Live Mode Card**:
```css
background: #DBEAFE; /* Light blue tint */
border-color: #93C5FD; /* Blue-300 */
```

**KRS Analysis Card**:
```css
background: #EDE9FE; /* Light purple tint */
border-color: #C4B5FD; /* Purple-300 */
```

**Title**: 18px, bold, Gray-900  
**Subtitle**: 14px, medium, Cyan-600 or Purple-600  
**Feature List**: 14px bullets, Gray-700, 24px line height  
**Use Case**: 14px, italic, Gray-600, margin-top 12px

### Chart (Screen 4)
- SVG or Canvas-based line chart
- Width: 100% (max 360px)
- Height: 120px
- Margin: 24px 0

### Progress Dots
```css
display: flex;
gap: 8px;
justify-content: center;
margin: 32px 0 24px;
```

**Each Dot**:
```css
width: 10px;
height: 10px;
border-radius: 50%;
background: #D1D5DB; /* Gray-300, inactive */
transition: all 0.3s;
```

**Active Dot**:
```css
background: #06B6D4; /* Cyan-500 */
width: 28px; /* Pill shape */
border-radius: 5px;
```

### Primary Button
```css
width: 100%;
height: 48px;
background: #06B6D4; /* Cyan-500 */
color: #FFFFFF;
font-size: 16px;
font-weight: 600;
border: none;
border-radius: 12px;
box-shadow: 0 2px 8px rgba(6, 182, 212, 0.2);
transition: all 0.2s;
cursor: pointer;
```

```css
&:hover {
  background: #0891B2; /* Cyan-600 */
  box-shadow: 0 4px 12px rgba(6, 182, 212, 0.3);
  transform: translateY(-1px);
}

&:active {
  transform: translateY(0);
}
```

---

## 📱 Responsive Behavior

**Mobile (320-767px)**:
- Single column layout
- Full-width cards
- Heading: 28px
- Body: 14px
- Profile cards: Stack vertically
- Chart width: 100% of container

**Tablet (768-1023px)**:
- Max-width: 480px, centered
- Heading: 32px
- Body: 16px
- Mode cards: Can show side-by-side if space allows

**Desktop (1024px+)**:
- Max-width: 480px, centered
- All text sizes as specified
- Hover effects on cards and buttons

---

## ♿ Accessibility

**Keyboard Navigation**:
- Tab through all interactive elements (Back, Skip, Next buttons)
- Enter/Space to activate buttons
- Focus indicators visible on all elements

**Screen Reader**:
- Heading hierarchy: h1 for screen title, h2 for sections, h3 for card titles
- Progress dots: `aria-label="Step 2 of 4"`
- Skip button: `aria-label="Skip onboarding and go to profile creation"`
- Chart: Alternative text description of KRS trend

**ARIA Labels**:
```html
<div role="progressbar" aria-valuenow="2" aria-valuemin="1" aria-valuemax="4" aria-label="Onboarding progress: Step 2 of 4">
```

**Color Contrast**:
- All text meets WCAG AA (4.5:1 ratio)
- Interactive elements have 3:1 contrast with background

---

## 🎬 Animations

**Page Transition** (between steps):
```css
@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.onboarding-screen {
  animation: slideIn 0.3s ease;
}
```

**Card Hover** (Profile cards, Mode cards):
```css
transition: all 0.2s ease;
```

**Button Press**:
```css
&:active {
  transform: scale(0.98);
}
```

---

## 🔄 User Flow

**Entry Points**:
1. First-time user (after app launch)
2. Manual trigger (Settings → "Retake Onboarding")

**Navigation**:
- **Next Button**: Advance to next step (1 → 2 → 3 → 4)
- **Back Button**: Return to previous step (2 → 1, 3 → 2, 4 → 3)
- **Skip Button**: Jump directly to Create Profile (any step → Profile creation)

**Exit**:
- Complete Step 4 → Navigate to `/assessment` (Movement Assessment)
- Skip → Navigate to `/profile/create` (Create Profile)

**State Persistence**:
- If user closes app mid-onboarding, resume at last completed step
- Once completed, don't show onboarding again (unless manually triggered)

---

## 📊 Data Tracking

**Analytics Events**:
```javascript
// User views onboarding step
analytics.track('onboarding_step_viewed', {
  step: 2,
  step_name: 'Motor Profiles'
});

// User advances to next step
analytics.track('onboarding_step_completed', {
  step: 2,
  time_on_step: 15 // seconds
});

// User skips onboarding
analytics.track('onboarding_skipped', {
  from_step: 2
});

// User completes onboarding
analytics.track('onboarding_completed', {
  total_time: 120, // seconds
  skipped_steps: []
});
```

---

## ✅ VALIDATION CHECKLIST

- [x] 4 screens defined (not 3)
- [x] Screen 1: "What is KRS?" - KRS scale 0-100 explained
- [x] Screen 1: Creation and Transfer subscores mentioned
- [x] Screen 1: "On Table" gain concept introduced
- [x] Screen 2: "Motor Profiles" - 4 types only (Spinner, Slingshotter, Whipper, Titan)
- [x] Screen 2: No extra profiles (no Rotator, Power Hitter, Torquer, Tilter, Hybrid)
- [x] Screen 2: MLB athlete examples per profile
- [x] Screen 3: "Two Modes" - Live Mode vs KRS Analysis Mode
- [x] Screen 3: Live Mode limitations clearly stated (60 FPS, positional feedback only, no exit velo)
- [x] Screen 3: KRS Mode requirements stated (240 FPS video)
- [x] Screen 4: "Track Progress" - Chart shows 0-100 KRS scale (not 0-1000)
- [x] Screen 4: 5 levels shown (FOUNDATION/BUILDING/DEVELOPING/ADVANCED/ELITE)
- [x] Screen 4: Motivational messaging
- [x] All screens: Color tokens match design-tokens.json
- [x] All screens: Responsive behavior defined
- [x] All screens: Accessibility notes included
- [x] Progress dots: 4 dots (one per screen)
- [x] Navigation: Back, Skip, Next buttons functional

---

**STATUS**: ✅ CORRECTED - Ready for Phase 1 implementation

**Issues Found and Fixed**:
1. **Screen count**: Was 3 screens, corrected to 4 screens
2. **Screen content**: Generic content replaced with KRS-specific education
3. **KRS scale**: 0-100 scale explicitly shown in Screens 1 and 4
4. **Motor Profiles**: Verified only 4 types (no extras)
5. **Live Mode**: Limitations clearly stated in Screen 3 (no exit velo overpromise)
6. **Chart scale**: Screen 4 chart verified as 0-100 scale (not 0-1000)
