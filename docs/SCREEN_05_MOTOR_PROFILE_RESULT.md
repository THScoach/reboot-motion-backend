# Screen 05: Motor Profile Result

**Version:** 1.0  
**Date:** December 26, 2025  
**Status:** Design Specification - Phase 0 Corrections

---

## Overview

**Purpose:** Display determined Motor Profile with confidence, characteristics, strengths, and example MLB athletes.

**User arrives here from:** Movement Assessment (after completing 5 movements)

**Next step:** Navigate to Home Dashboard (first-time user setup complete)

---

## Screen Layout

```
┌─────────────────────────────────────────────────────────┐
│                  MOTOR PROFILE RESULT                    │
├─────────────────────────────────────────────────────────┤
│                                                          │
│                                                          │
│              🎯 YOU'RE A SLINGSHOTTER!                   │  ← 32px, bold, cyan
│                                                          │
│                  92% Confidence                          │  ← 18px, badge, green bg
│                                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │                                                    │ │
│  │        [Illustration or icon placeholder]         │ │  ← 200px, cyan/gray
│  │         Slingshotter silhouette                   │ │
│  │                                                    │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
│  CHARACTERISTICS:                                        │  ← 16px, bold
│  ✓ Balanced rotation (hip + upper body)                 │
│  ✓ Explosive power generation                           │
│  ✓ Good timing and rhythm                               │
│  ✓ Strong weight transfer                               │
│                                                          │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│                                                          │
│  SIMILAR TO:                                             │  ← 16px, bold
│  • Fernando Tatis Jr. (Padres)                          │
│  • Ronald Acuña Jr. (Braves)                            │
│  • Francisco Lindor (Mets)                              │
│                                                          │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│                                                          │
│  YOUR STRENGTHS:                                         │  ← 16px, bold
│  💪 Hip rotation: 85° (Excellent)                       │
│  ⚡ Explosive power: 26" vertical jump                  │
│  ⚖️ Balance: 9.0 seconds (Strong)                       │
│                                                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │        [CONTINUE TO DASHBOARD →]                 │  │  ← 56px button, cyan
│  └──────────────────────────────────────────────────┘  │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## The 4 Motor Profiles

### Profile 1: Spinner

**Power Source:** Upper body rotation (torso twist)

**Characteristics:**
- Generates bat speed primarily through torso rotation
- Less hip involvement in swing initiation
- Quick, compact swing path
- High hand speed
- Strong top-hand dominance

**Physical Traits:**
- High T-spine rotation (>70°)
- Moderate hip rotation (60-75°)
- Good balance and control
- Fast-twitch muscle fiber dominance

**Strengths:**
- Contact hitting
- Quick adjustments
- Bat control
- Handles inside pitches well

**Areas to Develop:**
- Power generation from lower body
- Hip-shoulder separation
- Driving through contact

**Example MLB Athletes:**
- Mookie Betts (Dodgers)
- José Altuve (Astros)
- Freddie Freeman (Dodgers)
- Luis Arraez (Marlins)

**Typical KRS Range:** 65-80 (contact-focused, moderate power)

---

### Profile 2: Slingshotter

**Power Source:** Balanced rotation (hip + upper body coordination)

**Characteristics:**
- Balanced use of hip and torso rotation
- Explosive power through coordinated sequencing
- Good timing and rhythm
- Strong weight transfer from back to front leg
- Generates power through "elastic" loading

**Physical Traits:**
- Balanced hip rotation (75-85°)
- Good T-spine rotation (65-75°)
- High vertical jump (>22")
- Excellent single-leg balance (>8s)

**Strengths:**
- Power + contact balance
- Consistent hard contact
- Handles all pitch locations
- Adaptable swing

**Areas to Develop:**
- Maintaining timing under pressure
- Optimizing transfer efficiency

**Example MLB Athletes:**
- Fernando Tatis Jr. (Padres)
- Ronald Acuña Jr. (Braves)
- Mookie Betts (Dodgers)
- Francisco Lindor (Mets)

**Typical KRS Range:** 70-90 (balanced power + contact)

---

### Profile 3: Whipper

**Power Source:** Aggressive hip rotation (lower body dominant)

**Characteristics:**
- Initiates swing with explosive hip turn
- High rotational velocity
- Fast tempo (quick from load to contact)
- Generates leverage through hip-shoulder separation
- Power through speed, not just strength

**Physical Traits:**
- Very high hip rotation (>85°)
- High vertical jump (>24")
- Fast movement tempo
- Strong ground force production

**Strengths:**
- Elite exit velocity potential
- Extra-base hit power
- Generates bat speed efficiently
- Handles velocity well

**Areas to Develop:**
- Bat control on offspeed
- Timing/discipline
- Managing aggressive rotation

**Example MLB Athletes:**
- Juan Soto (Yankees)
- Aaron Judge (Yankees)
- Yordan Alvarez (Astros)
- Kyle Schwarber (Phillies)

**Typical KRS Range:** 75-95 (high power, elite exit velocity)

---

### Profile 4: Titan

**Power Source:** Strength-dominant (force > speed)

**Characteristics:**
- Generates power through raw strength
- Slower tempo, longer swing
- Less mobility, more force production
- Strong through contact ("hitting through the ball")
- Relies on physicality over sequencing

**Physical Traits:**
- Moderate hip rotation (65-75°)
- Strong squat performance
- High ground force (>800 N)
- Lower vertical jump (<20")
- Larger, more muscular build

**Strengths:**
- Power to all fields
- Driving the ball (not slapping)
- Handles inside pitches
- Strong contact

**Areas to Develop:**
- Mobility and flexibility
- Swing tempo/timing
- Rotational efficiency
- Transfer optimization

**Example MLB Athletes:**
- Giancarlo Stanton (Yankees)
- Pete Alonso (Mets)
- Matt Olson (Braves)
- Kyle Schwarber (Phillies)

**Typical KRS Range:** 60-75 (high force, moderate efficiency)

---

## Data Binding Specification

### API Endpoint
```
GET /api/motor-profile/assessments/{assessment_id}/result
```

### Response Schema
```json
{
  "assessment_id": "assess_001",
  "player_id": "player_001",
  "motor_profile": {
    "profile": "Slingshotter",
    "confidence": 0.92,
    "reasoning": "Balanced rotation (hip 85°, T-spine 70°) + explosive power (26\" vertical) + excellent balance (9.0s)"
  },
  "characteristics": [
    "Balanced rotation (hip + upper body)",
    "Explosive power generation",
    "Good timing and rhythm",
    "Strong weight transfer"
  ],
  "similar_athletes": [
    { "name": "Fernando Tatis Jr.", "team": "Padres" },
    { "name": "Ronald Acuña Jr.", "team": "Braves" },
    { "name": "Francisco Lindor", "team": "Mets" }
  ],
  "strengths": [
    { "category": "Hip rotation", "value": "85°", "rating": "Excellent" },
    { "category": "Explosive power", "value": "26\" vertical", "rating": null },
    { "category": "Balance", "value": "9.0 seconds", "rating": "Strong" }
  ],
  "typical_krs_range": {
    "min": 70,
    "max": 90,
    "description": "Balanced power + contact"
  }
}
```

### UI Mapping
- `motor_profile.profile` → "YOU'RE A SLINGSHOTTER!"
- `motor_profile.confidence` → "92% Confidence" badge
- `characteristics[]` → Bullet list with checkmarks
- `similar_athletes[]` → "Similar to:" list with names and teams
- `strengths[]` → "YOUR STRENGTHS:" with icons and values

---

## Layout Specifications

### Profile Title
- **Font Size:** 32px (mobile: 28px)
- **Font Weight:** 700 (bold)
- **Color:** #06B6D4 (cyan)
- **Text Transform:** Uppercase
- **Margin:** 32px top, 16px bottom

### Confidence Badge
- **Background:** #10B981 (green) if >85%, #F59E0B (yellow) if 70-85%, #EF4444 (red) if <70%
- **Text:** White, 18px, bold
- **Padding:** 8px horizontal, 4px vertical
- **Border Radius:** 20px (pill shape)
- **Margin:** 8px bottom

### Illustration
- **Size:** 200px × 200px
- **Style:** Simple silhouette or icon
- **Color:** #E2E8F0 (light gray) or #DBEAFE (light cyan tint)
- **Margin:** 24px top/bottom

### Characteristics List
- **Heading:** 16px, bold, #0F172A, margin 24px top
- **Items:** 16px, #475569, 32px line height
- **Checkmark:** ✓ green (#10B981), 20px before text

### Similar Athletes
- **Heading:** 16px, bold, #0F172A
- **Separator:** Horizontal line, 1px, #E2E8F0, margin 24px top/bottom
- **Items:** 16px, #475569, bullet list
- **Format:** "Name (Team)"

### Strengths
- **Heading:** 16px, bold, #0F172A
- **Items:** Icon (24px) + text (16px)
  - 💪 for strength metrics
  - ⚡ for power metrics
  - ⚖️ for balance metrics
- **Format:** "Category: Value (Rating)"

### Continue Button
- **Size:** Full-width, 56px height
- **Background:** #06B6D4 (cyan)
- **Text:** White, 18px, bold
- **Border Radius:** 12px
- **Margin:** 32px top
- **Hover:** Background #0891B2 (darker cyan), shadow-lg

---

## HTML/React Implementation

```tsx
<div className="min-h-screen bg-gray-50 px-4 py-8">
  <div className="max-w-2xl mx-auto bg-white rounded-2xl p-8 shadow-lg">
    {/* Header */}
    <div className="text-center mb-8">
      <h1 className="text-3xl md:text-4xl font-bold text-cyan-500 uppercase mb-3">
        🎯 YOU'RE A {motor_profile.profile.toUpperCase()}!
      </h1>
      
      {/* Confidence Badge */}
      <div 
        className={`inline-block px-4 py-2 rounded-full text-lg font-bold text-white ${getConfidenceBadgeColor(motor_profile.confidence)}`}
      >
        {Math.round(motor_profile.confidence * 100)}% Confidence
      </div>
    </div>
    
    {/* Illustration */}
    <div className="flex justify-center mb-8">
      <div className="w-48 h-48 rounded-full bg-cyan-50 flex items-center justify-center">
        <span className="text-6xl">{getProfileIcon(motor_profile.profile)}</span>
      </div>
    </div>
    
    {/* Characteristics */}
    <div className="mb-6">
      <h2 className="text-base font-bold text-gray-900 uppercase tracking-wide mb-3">
        CHARACTERISTICS:
      </h2>
      <ul className="space-y-2">
        {characteristics.map((char, index) => (
          <li key={index} className="flex items-start gap-2 text-gray-700">
            <span className="text-green-500 text-lg">✓</span>
            <span>{char}</span>
          </li>
        ))}
      </ul>
    </div>
    
    {/* Separator */}
    <div className="border-t border-gray-200 my-6"></div>
    
    {/* Similar Athletes */}
    <div className="mb-6">
      <h2 className="text-base font-bold text-gray-900 uppercase tracking-wide mb-3">
        SIMILAR TO:
      </h2>
      <ul className="space-y-1">
        {similar_athletes.map((athlete, index) => (
          <li key={index} className="text-gray-700">
            • {athlete.name} ({athlete.team})
          </li>
        ))}
      </ul>
    </div>
    
    {/* Separator */}
    <div className="border-t border-gray-200 my-6"></div>
    
    {/* Strengths */}
    <div className="mb-8">
      <h2 className="text-base font-bold text-gray-900 uppercase tracking-wide mb-3">
        YOUR STRENGTHS:
      </h2>
      <div className="space-y-2">
        {strengths.map((strength, index) => (
          <div key={index} className="flex items-center gap-3 text-gray-700">
            <span className="text-2xl">{getStrengthIcon(strength.category)}</span>
            <span>
              {strength.category}: <strong>{strength.value}</strong>
              {strength.rating && ` (${strength.rating})`}
            </span>
          </div>
        ))}
      </div>
    </div>
    
    {/* Continue Button */}
    <button
      onClick={() => navigate('/home')}
      className="w-full py-4 bg-cyan-500 hover:bg-cyan-600 text-white text-lg font-bold rounded-xl transition shadow-md hover:shadow-lg"
      aria-label="Continue to your dashboard to start training"
    >
      CONTINUE TO DASHBOARD →
    </button>
  </div>
</div>
```

### Helper Functions

```typescript
// Confidence badge color
function getConfidenceBadgeColor(confidence: number): string {
  if (confidence >= 0.85) return 'bg-green-500';
  if (confidence >= 0.70) return 'bg-yellow-500';
  return 'bg-red-500';
}

// Profile icon emoji
function getProfileIcon(profile: string): string {
  const icons = {
    'Spinner': '🏹',
    'Slingshotter': '🎯',
    'Whipper': '⚡',
    'Titan': '💪'
  };
  return icons[profile] || '🎯';
}

// Strength category icon
function getStrengthIcon(category: string): string {
  if (category.toLowerCase().includes('hip') || category.toLowerCase().includes('rotation')) {
    return '💪';
  }
  if (category.toLowerCase().includes('power') || category.toLowerCase().includes('jump')) {
    return '⚡';
  }
  if (category.toLowerCase().includes('balance') || category.toLowerCase().includes('stability')) {
    return '⚖️';
  }
  return '✓';
}
```

---

## Responsive Behavior

**Mobile (320-767px):**
- Single column layout
- Profile title: 28px
- Illustration: 180px × 180px
- Button: Full-width

**Tablet (768-1023px):**
- Single column, max-width: 600px, centered
- Profile title: 30px
- Illustration: 200px × 200px

**Desktop (1024px+):**
- Single column, max-width: 600px, centered
- Profile title: 32px
- Illustration: 200px × 200px

---

## Animations

**On Load:**
1. Profile title: Fade-in + slide-up (0.3s delay)
2. Confidence badge: Fade-in (0.5s delay)
3. Illustration: Scale from 0.8 to 1.0 (0.4s, 0.6s delay)
4. Characteristics: Fade-in stagger (each item +0.1s delay)
5. Athletes list: Fade-in (1.0s delay)
6. Strengths: Fade-in stagger (1.2s start)
7. Button: Fade-in (1.5s delay)

**Button Hover:**
- Scale: 1.02
- Shadow: elevation increase (shadow-md to shadow-lg)
- Transition: 0.2s ease

**CSS Implementation:**

```css
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.profile-title {
  animation: fadeInUp 0.5s ease 0.3s both;
}

.confidence-badge {
  animation: fadeInUp 0.5s ease 0.5s both;
}

.illustration {
  animation: scaleIn 0.4s ease 0.6s both;
}

@keyframes scaleIn {
  from {
    opacity: 0;
    transform: scale(0.8);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.characteristic-item {
  animation: fadeInUp 0.4s ease both;
}

.characteristic-item:nth-child(1) { animation-delay: 0.8s; }
.characteristic-item:nth-child(2) { animation-delay: 0.9s; }
.characteristic-item:nth-child(3) { animation-delay: 1.0s; }
.characteristic-item:nth-child(4) { animation-delay: 1.1s; }

.athletes-section {
  animation: fadeInUp 0.5s ease 1.0s both;
}

.strength-item {
  animation: fadeInUp 0.4s ease both;
}

.strength-item:nth-child(1) { animation-delay: 1.2s; }
.strength-item:nth-child(2) { animation-delay: 1.3s; }
.strength-item:nth-child(3) { animation-delay: 1.4s; }

.continue-button {
  animation: fadeInUp 0.5s ease 1.5s both;
}
```

---

## Accessibility

- **Profile title:** `<h1>` tag, `aria-label="Your motor profile is Slingshotter with 92% confidence"`
- **Confidence badge:** `role="status"`, `aria-label="92 percent confidence"`
- **Characteristics list:** `<ul role="list">` with `<li>` items
- **Athletes list:** `<ul role="list">`
- **Strengths:** Each item has `aria-label` with full text
- **Button:** `aria-label="Continue to your dashboard to start training"`
- **Keyboard navigation:** Tab through all elements, Enter to activate button
- **Focus indicators:** Visible outline on button
- **Screen reader:** Proper heading hierarchy (h1 for title, h2 for sections)

---

## Error Handling

**Scenarios:**

1. **Low Confidence (<70%):**
   - Show warning badge (red background)
   - Add text below confidence: "We recommend retaking the assessment for a more accurate profile"
   - Add secondary button: "Retake Assessment"
   
   ```tsx
   {motor_profile.confidence < 0.70 && (
     <div className="mb-4 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
       <p className="text-sm text-yellow-800">
         ⚠️ Low confidence score. For best results, consider retaking the assessment.
       </p>
       <button 
         onClick={() => navigate('/assessment')}
         className="mt-2 text-sm text-yellow-700 underline"
       >
         Retake Assessment
       </button>
     </div>
   )}
   ```

2. **Assessment Incomplete:**
   - If user navigates here without completing all 5 movements
   - Redirect back to Movement Assessment with message: "Please complete all 5 movements first"
   
   ```tsx
   useEffect(() => {
     if (movements_completed < 5) {
       navigate('/assessment', { 
         state: { error: 'Please complete all 5 movements first' } 
       });
     }
   }, [movements_completed]);
   ```

3. **API Error:**
   - Show generic error: "We couldn't determine your profile. Please try again."
   - Offer "Retry" button
   
   ```tsx
   {error && (
     <div className="text-center p-8">
       <p className="text-red-600 mb-4">
         ❌ We couldn't determine your profile. Please try again.
       </p>
       <button 
         onClick={() => window.location.reload()}
         className="px-6 py-3 bg-cyan-500 text-white rounded-lg"
       >
         Retry
       </button>
     </div>
   )}
   ```

---

## Analytics Events

Track these events for product insights:

```javascript
// Profile determined
analytics.track('motor_profile_determined', {
  profile: 'Slingshotter',
  confidence: 0.92,
  player_id: 'player_001',
  assessment_duration: 320 // seconds
});

// User viewed profile result
analytics.track('motor_profile_result_viewed', {
  profile: 'Slingshotter',
  confidence: 0.92,
  time_to_view: 2.3 // seconds after determination
});

// User clicked continue
analytics.track('motor_profile_result_continue', {
  profile: 'Slingshotter',
  time_on_screen: 45 // seconds
});

// User clicked retake (if low confidence)
analytics.track('motor_profile_retake_initiated', {
  previous_profile: 'Slingshotter',
  previous_confidence: 0.65
});
```

---

## User Testing Questions

**Validate with real users:**
1. Does the profile description match how you see your swing?
2. Do the example athletes make sense to you?
3. Is the confidence % clear and trustworthy?
4. Do you understand what to do next?
5. Would you retake the assessment if confidence was 68%?

---

## Profile-Specific Content Variations

### Spinner Display
```tsx
profile="Spinner"
icon="🏹"
characteristics=[
  "Generates bat speed through torso rotation",
  "Quick, compact swing path",
  "High hand speed",
  "Strong top-hand dominance"
]
athletes=["Mookie Betts", "José Altuve", "Freddie Freeman", "Luis Arraez"]
strengths=[
  { category: "T-spine rotation", value: "72°", rating: "Excellent" },
  { category: "Hand speed", value: "Fast", rating: null },
  { category: "Bat control", value: "8.5/10", rating: "Elite" }
]
krs_range="65-80"
```

### Whipper Display
```tsx
profile="Whipper"
icon="⚡"
characteristics=[
  "Explosive hip turn initiates swing",
  "High rotational velocity",
  "Fast tempo (load to contact)",
  "Leverage through hip-shoulder separation"
]
athletes=["Juan Soto", "Aaron Judge", "Yordan Alvarez", "Kyle Schwarber"]
strengths=[
  { category: "Hip rotation", value: "88°", rating: "Elite" },
  { category: "Vertical jump", value: "28\"", rating: "Explosive" },
  { category: "Ground force", value: "850 N", rating: "Strong" }
]
krs_range="75-95"
```

### Titan Display
```tsx
profile="Titan"
icon="💪"
characteristics=[
  "Generates power through raw strength",
  "Slower tempo, longer swing",
  "Strong through contact",
  "Physicality over sequencing"
]
athletes=["Giancarlo Stanton", "Pete Alonso", "Matt Olson"]
strengths=[
  { category: "Squat strength", value: "Good", rating: null },
  { category: "Ground force", value: "920 N", rating: "Excellent" },
  { category: "Power to all fields", value: "Strong", rating: null }
]
krs_range="60-75"
```

---

## ✅ VALIDATION CHECKLIST

- [x] All 4 Motor Profiles defined with complete characteristics
- [x] Physical traits specified per profile
- [x] Strengths and areas to develop listed
- [x] Example MLB athletes (3-4 per profile)
- [x] Typical KRS ranges defined
- [x] Screen layout with ASCII mockup
- [x] Complete data binding specification (API endpoint + schema)
- [x] UI mapping documented
- [x] Layout specifications (fonts, colors, spacing)
- [x] React/TypeScript implementation example
- [x] Helper functions provided
- [x] Responsive behavior defined (mobile/tablet/desktop)
- [x] Animations specified with CSS
- [x] Accessibility complete (ARIA labels, keyboard nav)
- [x] Error handling (3 scenarios)
- [x] Analytics events defined
- [x] Profile-specific content variations

---

**STATUS**: ✅ COMPLETE - Ready for Phase 1 implementation
