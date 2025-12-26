# Screen 05: Onboarding

**Screen Name**: Onboarding Flow (3 screens)  
**Route**: `/onboarding/[step]`  
**Complexity**: MEDIUM (Multi-step flow)  
**Priority**: P0 (Critical Path)

---

## 📐 Flow Overview

```
Onboarding Step 1: Welcome
    ↓
Onboarding Step 2: How It Works
    ↓
Onboarding Step 3: Get Started
    ↓
Create Profile (Screen 06)
```

---

## 🎯 Step 1: Welcome

### Layout
```
┌───────────────────────────────┐
│                     Skip →    │ ← Skip button
├───────────────────────────────┤
│                               │
│                               │
│       [Illustration]          │ ← Icon/Illustration
│         96×96                  │   (Baseball bat)
│                               │
│                               │
│   Welcome to                  │ ← Heading-01
│   Catching Barrels            │
│                               │
│   The most advanced swing     │ ← Body-01
│   analysis platform for       │   (Gray-500)
│   baseball players.           │
│                               │
│                               │
│                               │
│   ○ ● ○                       │ ← Progress dots
│                               │
│   [Next]                      │ ← Primary button
│                               │
└───────────────────────────────┘
```

### Content
- **Icon**: Baseball bat (96×96, Electric Cyan)
- **Heading**: "Welcome to Catching Barrels"
- **Body**: "The most advanced swing analysis platform for baseball players."
- **Progress**: Dot 1 of 3 (active)
- **Button**: "Next" (Primary, full width)

---

## 🎯 Step 2: How It Works

### Layout
```
┌───────────────────────────────┐
│        ← Back       Skip →    │ ← Navigation
├───────────────────────────────┤
│                               │
│                               │
│       [Illustration]          │ ← Icon/Illustration
│         96×96                  │   (Camera + AI)
│                               │
│                               │
│   How It Works                │ ← Heading-01
│                               │
│   1. Record your swing        │ ← Feature list
│   2. AI analyzes your motion  │   with icons
│   3. Get personalized drills  │
│                               │
│   KRS Score • Motor Profile   │ ← Feature badges
│   4B Breakdown • Live Coaching│
│                               │
│   ○ ○ ●                       │ ← Progress dots
│                               │
│   [Next]                      │ ← Primary button
│                               │
└───────────────────────────────┘
```

### Content
- **Icon**: Camera with AI sparkles (96×96, Electric Cyan)
- **Heading**: "How It Works"
- **Features**:
  1. "Record your swing" (with camera icon)
  2. "AI analyzes your motion" (with brain icon)
  3. "Get personalized drills" (with target icon)
- **Badges**: KRS Score, Motor Profile, 4B Breakdown, Live Coaching
- **Progress**: Dot 2 of 3 (active)
- **Buttons**: "Back" (Ghost) + "Next" (Primary)

---

## 🎯 Step 3: Get Started

### Layout
```
┌───────────────────────────────┐
│        ← Back                 │ ← Back button only
├───────────────────────────────┤
│                               │
│                               │
│       [Illustration]          │ ← Icon/Illustration
│         96×96                  │   (Trophy/Star)
│                               │
│                               │
│   Ready to Optimize           │ ← Heading-01
│   Your Swing?                 │
│                               │
│   Join thousands of players   │ ← Body-01
│   improving their game with   │
│   data-driven insights.       │
│                               │
│   ✓ Free to start             │ ← Benefit list
│   ✓ No credit card required   │
│   ✓ Unlimited swing analysis  │
│                               │
│   ○ ○ ○                       │ ← Progress dots
│                               │
│   [Create Your Profile]       │ ← Primary button
│                               │
│   By continuing, you agree to │ ← Legal text
│   our Terms & Privacy Policy  │   (Caption, links)
│                               │
└───────────────────────────────┘
```

### Content
- **Icon**: Trophy or star (96×96, Electric Cyan)
- **Heading**: "Ready to Optimize Your Swing?"
- **Body**: "Join thousands of players improving their game with data-driven insights."
- **Benefits**:
  - ✓ Free to start
  - ✓ No credit card required
  - ✓ Unlimited swing analysis
- **Progress**: Dot 3 of 3 (active)
- **Button**: "Create Your Profile" (Primary, full width)
- **Legal**: "By continuing, you agree to our Terms & Privacy Policy"

---

## 🎨 Visual Specifications

### Layout Container
```css
max-width: 400px;
margin: 0 auto;
padding: 24px;
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
margin-bottom: 32px;
```

**Back Button** (Ghost):
```css
color: #6B7280; /* Gray-500 */
font-size: 16px;
padding: 8px 0;
```

**Skip Button** (Ghost):
```css
color: #6B7280; /* Gray-500 */
font-size: 16px;
padding: 8px 0;
```

### Illustration Area
```css
display: flex;
justify-content: center;
align-items: center;
margin-bottom: 40px;
```

**Icon**:
- Size: 96px × 96px
- Color: Electric Cyan (#06B6D4)
- Style: Outlined (Lucide React)
- Background: White circle with subtle shadow

### Heading
```css
font-family: 'Inter', sans-serif;
font-weight: 600; /* Semibold */
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
color: #6B7280; /* Gray-500 */
text-align: center;
margin-bottom: 32px;
```

### Feature List (Step 2)
```css
list-style: none;
padding: 0;
margin-bottom: 24px;
```

**Each Feature**:
```css
display: flex;
align-items: center;
gap: 12px;
padding: 12px 0;
font-size: 16px;
color: #374151; /* Gray-700 */
```

**Icon** (24px, Electric Cyan):
- Camera: `<Camera size={24} />`
- Brain: `<Brain size={24} />`
- Target: `<Target size={24} />`

### Feature Badges (Step 2)
```css
display: flex;
flex-wrap: wrap;
gap: 8px;
justify-content: center;
margin-bottom: 32px;
```

**Each Badge**:
```css
background: #FFFFFF;
border: 1px solid #E5E7EB; /* Gray-200 */
border-radius: 6px;
padding: 8px 12px;
font-size: 14px;
color: #374151; /* Gray-700 */
```

### Benefit List (Step 3)
```css
list-style: none;
padding: 0;
margin-bottom: 32px;
text-align: left;
max-width: 280px;
margin-left: auto;
margin-right: auto;
```

**Each Benefit**:
```css
display: flex;
align-items: center;
gap: 12px;
padding: 8px 0;
font-size: 16px;
color: #374151; /* Gray-700 */
```

**Checkmark**:
- Icon: `<Check size={20} />`
- Color: Success Green (#10B981)
- Background: Light green circle (16px)

### Progress Dots
```css
display: flex;
gap: 8px;
justify-content: center;
margin-bottom: 24px;
```

**Each Dot**:
```css
width: 8px;
height: 8px;
border-radius: 50%;
background: #D1D5DB; /* Gray-300, inactive */
transition: all 200ms ease;
```

**Active Dot**:
```css
background: #06B6D4; /* Electric Cyan */
width: 24px;
border-radius: 4px; /* Pill shape */
```

### Primary Button
```css
width: 100%;
height: 48px;
background: #06B6D4; /* Electric Cyan */
color: #FFFFFF;
border-radius: 8px;
font-size: 16px;
font-weight: 600;
border: none;
cursor: pointer;
transition: background 200ms ease;
```

**Hover**:
```css
background: #0284C7; /* Darker cyan */
```

**Active**:
```css
background: #0369A1; /* Even darker */
transform: scale(0.98);
```

### Legal Text
```css
font-size: 12px;
line-height: 18px;
color: #9CA3AF; /* Gray-400 */
text-align: center;
margin-top: 16px;
```

**Links**:
```css
color: #06B6D4; /* Electric Cyan */
text-decoration: underline;
```

---

## 🎬 Animations

### Page Transitions
```css
/* Slide in from right */
@keyframes slideInRight {
  from {
    opacity: 0;
    transform: translateX(20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

/* Slide out to left */
@keyframes slideOutLeft {
  from {
    opacity: 1;
    transform: translateX(0);
  }
  to {
    opacity: 0;
    transform: translateX(-20px);
  }
}
```

### Element Entrance
- **Icon**: Fade in + Scale (500ms, delay 100ms)
- **Heading**: Fade in + Slide up (300ms, delay 200ms)
- **Body**: Fade in (300ms, delay 300ms)
- **Features**: Fade in + Slide up (300ms, stagger 100ms)
- **Button**: Fade in (300ms, delay 500ms)

---

## 🔄 Navigation Logic

### Next Button
```typescript
const handleNext = () => {
  if (currentStep < 3) {
    // Go to next step
    router.push(`/onboarding/${currentStep + 1}`);
  } else {
    // Go to Create Profile
    router.push('/profile/create');
  }
};
```

### Back Button
```typescript
const handleBack = () => {
  if (currentStep > 1) {
    // Go to previous step
    router.push(`/onboarding/${currentStep - 1}`);
  } else {
    // Go to splash (shouldn't happen)
    router.push('/');
  }
};
```

### Skip Button
```typescript
const handleSkip = () => {
  // Skip onboarding, go directly to Create Profile
  router.push('/profile/create');
  
  // Track analytics
  analytics.track('Onboarding Skipped', {
    step: currentStep,
  });
};
```

---

## 📱 Responsive Behavior

### Mobile (< 768px)
- Icon: 96px
- Heading: 32px
- Body: 16px
- Padding: 24px
- Button: Full width

### Tablet (768px - 1023px)
- Icon: 112px
- Heading: 36px
- Body: 18px
- Padding: 32px
- Button: Full width

### Desktop (1024px+)
- Max width: 480px (centered)
- Icon: 128px
- Heading: 40px
- Body: 20px
- Padding: 40px
- Button: Max 400px

---

## ♿ Accessibility

### Keyboard Navigation
- **Tab**: Navigate through interactive elements (Skip, Back, Next)
- **Enter/Space**: Activate buttons
- **Arrow keys**: Navigate between steps (optional)

### Screen Reader
```html
<!-- Step 1 -->
<div role="region" aria-label="Onboarding Step 1 of 3">
  <h1>Welcome to Catching Barrels</h1>
  <p>The most advanced swing analysis platform for baseball players.</p>
  <nav aria-label="Onboarding progress">
    <span aria-current="step">Step 1</span>
    <span>Step 2</span>
    <span>Step 3</span>
  </nav>
  <button aria-label="Go to next step">Next</button>
  <button aria-label="Skip onboarding">Skip</button>
</div>
```

### Focus Management
- When navigating between steps, focus moves to heading
- Skip button always visible and focusable
- Clear focus indicators (2px Electric Cyan outline)

---

## 📊 Analytics Events

```typescript
// Step viewed
analytics.track('Onboarding Step Viewed', {
  step: number,
  stepName: string,
});

// Next clicked
analytics.track('Onboarding Next Clicked', {
  step: number,
});

// Back clicked
analytics.track('Onboarding Back Clicked', {
  step: number,
});

// Skip clicked
analytics.track('Onboarding Skipped', {
  step: number,
});

// Completed
analytics.track('Onboarding Completed', {
  duration: number, // ms
});
```

---

## 🎯 Success Metrics

### Completion Rate
- **Target**: > 80% complete all 3 steps
- **Benchmark**: < 20% skip onboarding

### Time on Onboarding
- **Target**: 30-60 seconds total
- **Per Step**: 10-20 seconds

### Drop-off Points
- Monitor which step has highest drop-off
- Optimize content/design accordingly

---

## 🎨 Icon Assets

### Step 1: Baseball Bat
- Lucide Icon: `<Activity />` or custom SVG
- Size: 96×96
- Color: Electric Cyan (#06B6D4)
- Style: Outlined

### Step 2: Camera + AI
- Lucide Icon: `<Camera />` + `<Sparkles />`
- Size: 96×96
- Color: Electric Cyan (#06B6D4)
- Style: Outlined

### Step 3: Trophy
- Lucide Icon: `<Trophy />` or `<Star />`
- Size: 96×96
- Color: Electric Cyan (#06B6D4)
- Style: Outlined

---

## 📝 Copy Variations

### Alternative Headlines

**Step 1**:
- "Welcome to Catching Barrels"
- "Your Swing Journey Starts Here"
- "Train Like the Pros"

**Step 2**:
- "How It Works"
- "Your Personal Swing Coach"
- "Science-Backed Training"

**Step 3**:
- "Ready to Optimize Your Swing?"
- "Join the Catching Barrels Community"
- "Start Your Free Analysis"

---

## 🔍 Testing Checklist

- [ ] All 3 steps render correctly
- [ ] Navigation works (Next, Back, Skip)
- [ ] Progress dots update correctly
- [ ] Animations smooth (60 FPS)
- [ ] Skip button works
- [ ] Legal text links work
- [ ] Responsive on mobile
- [ ] Responsive on tablet
- [ ] Responsive on desktop
- [ ] Keyboard navigation works
- [ ] Screen reader announces correctly
- [ ] Focus indicators visible
- [ ] Analytics events fire
- [ ] No console errors

---

## 📱 Device Testing

- iPhone SE (375×667)
- iPhone 14 Pro (393×852)
- Android (Pixel 5) (393×851)
- iPad (768×1024)
- Desktop (1440×900)

---

## ✅ Definition of Done

- [ ] All 3 steps implemented
- [ ] Navigation works (Next, Back, Skip)
- [ ] Progress indicators update
- [ ] Animations implemented
- [ ] Icons/illustrations added
- [ ] Copy finalized
- [ ] Legal text + links
- [ ] Responsive design works
- [ ] Keyboard accessible
- [ ] Screen reader accessible
- [ ] Analytics integrated
- [ ] 60 FPS on mobile
- [ ] Lighthouse score > 90

---

**Priority**: P0 (Critical Path)  
**Complexity**: MEDIUM (Multi-step flow)  
**Estimated Dev Time**: 6-8 hours (Phase 1)

**Dependencies**:
- Icon assets (baseball bat, camera, trophy)
- Inter font loaded
- Routing configured
- Analytics setup

---

*Last Updated: December 27, 2025*  
*Screen Specification v1.0*
