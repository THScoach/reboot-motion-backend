# Screen 04: Splash Screen

**Screen Name**: Splash Screen  
**Route**: `/` (Initial load)  
**Complexity**: LOW (Simplest screen)  
**Priority**: P0 (Critical Path)

---

## 📐 Layout Overview

```
┌───────────────────────────────┐
│                               │
│                               │
│                               │
│                               │
│         [CB Logo]             │ ← Logo (centered)
│                               │
│     Catching Barrels          │ ← Wordmark
│                               │
│   Your swing, optimized.      │ ← Tagline
│                               │
│                               │
│        ● ● ● ●                │ ← Loading dots (animated)
│                               │
│                               │
│                               │
│                               │
│                               │
└───────────────────────────────┘
```

---

## 🎨 Visual Specifications

### Background
- **Color**: White (#FFFFFF)
- **Alternative**: Very light gradient (Gray-50 to White)

### Logo
- **Size**: 120px × 120px
- **Position**: Centered (both axes)
- **Style**: CB monogram with gradient
- **Colors**: Electric Cyan to deeper blue gradient

### Wordmark
- **Text**: "Catching Barrels"
- **Font**: Inter Bold
- **Size**: 32px (Heading-01)
- **Color**: Gray-900 (#111827)
- **Position**: 24px below logo
- **Alignment**: Center

### Tagline
- **Text**: "Your swing, optimized."
- **Font**: Inter Regular
- **Size**: 16px (Body-01)
- **Color**: Gray-500 (#6B7280)
- **Position**: 12px below wordmark
- **Alignment**: Center

### Loading Indicator
- **Type**: Animated dots (● ● ● ●)
- **Position**: 48px below tagline
- **Animation**: Sequential fade-in/fade-out (300ms each)
- **Color**: Electric Cyan (#06B6D4)
- **Size**: 8px diameter per dot
- **Gap**: 12px between dots

---

## 🎬 Animation Sequence

### 1. Logo Entrance (0-500ms)
```
Fade in + Scale up
- Start: opacity 0, scale 0.8
- End: opacity 1, scale 1
- Duration: 500ms
- Easing: ease-out
```

### 2. Wordmark Entrance (500-800ms)
```
Fade in + Slide up
- Start: opacity 0, translateY(10px)
- End: opacity 1, translateY(0)
- Duration: 300ms
- Easing: ease-out
```

### 3. Tagline Entrance (800-1100ms)
```
Fade in
- Start: opacity 0
- End: opacity 0.7
- Duration: 300ms
- Easing: ease-out
```

### 4. Loading Dots (1100ms - ongoing)
```
Sequential pulse animation
Dot 1: 0-300ms
Dot 2: 100-400ms
Dot 3: 200-500ms
Dot 4: 300-600ms
Loop indefinitely
```

---

## 🔄 Loading States

### Initial Load (0-1000ms)
- Show logo animation
- Show wordmark + tagline
- Start loading dots

### Data Loading (1000-2000ms)
- Check authentication status
- Load user preferences
- Initialize services

### Transition (2000ms+)
- **If authenticated**: Navigate to Home Dashboard
- **If new user**: Navigate to Onboarding
- **If returning**: Navigate to Home Dashboard

---

## 📱 Responsive Behavior

### Mobile (< 768px)
```
Logo: 120px × 120px
Wordmark: 32px
Tagline: 16px
Spacing: 24px, 12px, 48px
```

### Tablet (768px - 1023px)
```
Logo: 140px × 140px
Wordmark: 36px
Tagline: 18px
Spacing: 28px, 14px, 56px
```

### Desktop (1024px+)
```
Logo: 160px × 160px
Wordmark: 40px
Tagline: 20px
Spacing: 32px, 16px, 64px
```

---

## 🎯 Logo Specifications

### CB Monogram
```
┌─────────────┐
│             │
│   ╔═╗ ╔═╗   │  ← C and B letters
│   ║   ╠═╣   │     overlapped
│   ╚═╝ ╚═╝   │     with gradient
│             │
└─────────────┘
```

**Design Details**:
- **Style**: Modern, geometric, athletic
- **Gradient**: Electric Cyan (#06B6D4) → Blue (#0284C7)
- **Stroke**: 4px width
- **Corner Radius**: 2px
- **Inner Spacing**: 2px gap between C and B
- **Shadow**: Subtle (0 2px 4px rgba(0,0,0,0.1))

---

## 🔤 Typography Details

### Wordmark
```css
font-family: 'Inter', sans-serif;
font-weight: 700; /* Bold */
font-size: 32px;
line-height: 40px;
letter-spacing: -0.02em; /* Tight */
color: #111827; /* Gray-900 */
text-align: center;
```

### Tagline
```css
font-family: 'Inter', sans-serif;
font-weight: 400; /* Regular */
font-size: 16px;
line-height: 24px;
letter-spacing: 0;
color: #6B7280; /* Gray-500 */
text-align: center;
```

---

## 💫 Loading Dots Animation

### Keyframes
```css
@keyframes dotPulse {
  0%, 100% {
    opacity: 0.3;
    transform: scale(1);
  }
  50% {
    opacity: 1;
    transform: scale(1.2);
  }
}

.dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #06B6D4;
  display: inline-block;
  margin: 0 6px;
}

.dot:nth-child(1) {
  animation: dotPulse 1.2s ease-in-out 0s infinite;
}

.dot:nth-child(2) {
  animation: dotPulse 1.2s ease-in-out 0.15s infinite;
}

.dot:nth-child(3) {
  animation: dotPulse 1.2s ease-in-out 0.3s infinite;
}

.dot:nth-child(4) {
  animation: dotPulse 1.2s ease-in-out 0.45s infinite;
}
```

---

## 🔐 Authentication Flow

### Decision Tree
```
Splash Screen (2s)
    ↓
Check Auth Status
    ├─ Authenticated → Home Dashboard
    ├─ New User → Onboarding (Screen 05)
    └─ Error → Retry / Offline Mode
```

### Storage Check
```typescript
// Pseudocode
const checkAuthStatus = async () => {
  const session = await supabase.auth.getSession();
  
  if (session) {
    // Load user profile
    const profile = await loadUserProfile(session.user.id);
    
    if (profile.onboarded) {
      navigate('/home');
    } else {
      navigate('/onboarding');
    }
  } else {
    navigate('/onboarding');
  }
};
```

---

## ⚠️ Error Handling

### Network Error
- Show error toast: "Connection issue. Retrying..."
- Retry 3 times with exponential backoff
- If all retries fail: Navigate to onboarding (offline mode)

### Timeout (> 5 seconds)
- Log warning
- Navigate to onboarding anyway
- Show "Limited connectivity" banner

---

## ♿ Accessibility

### Screen Reader
```html
<div role="status" aria-live="polite">
  <img src="/logo.svg" alt="Catching Barrels logo" />
  <h1>Catching Barrels</h1>
  <p>Your swing, optimized.</p>
  <div aria-label="Loading application">
    <span class="sr-only">Loading, please wait</span>
    <div class="loading-dots" aria-hidden="true">
      <!-- Visual dots only -->
    </div>
  </div>
</div>
```

### Focus Management
- No interactive elements on splash
- Automatically move focus to first interactive element on next screen

### Motion Preference
```css
@media (prefers-reduced-motion: reduce) {
  /* Disable all animations */
  * {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
  
  /* Skip splash, go directly to next screen */
  /* Duration: 100ms instead of 2000ms */
}
```

---

## 🎨 Color Palette

```css
--splash-bg: #FFFFFF;
--logo-gradient-start: #06B6D4; /* Electric Cyan */
--logo-gradient-end: #0284C7;   /* Darker Blue */
--wordmark-color: #111827;      /* Gray-900 */
--tagline-color: #6B7280;       /* Gray-500 */
--loading-dot-color: #06B6D4;   /* Electric Cyan */
```

---

## 📏 Spacing & Layout

### Vertical Spacing
```
Top padding: calc(50vh - 200px)
Logo: 120px
Gap: 24px
Wordmark: 40px (line-height)
Gap: 12px
Tagline: 24px (line-height)
Gap: 48px
Loading dots: 8px
Bottom padding: calc(50vh - 200px)
```

### Horizontal Centering
```
Container: max-width 400px
Margin: 0 auto
Padding: 0 24px
```

---

## 🚀 Performance

### Critical Rendering Path
1. **Inline critical CSS** (logo, layout)
2. **Preload logo** (SVG in HTML or <link rel="preload">)
3. **Font-display: swap** for Inter font
4. **Minimal JavaScript** (auth check only)

### Metrics
- **LCP**: < 1s (logo)
- **FCP**: < 0.5s
- **TTI**: < 2s
- **CLS**: 0 (no layout shift)

---

## 📊 Analytics Events

```typescript
// Track splash screen view
analytics.track('Splash Screen Viewed', {
  timestamp: Date.now(),
  platform: 'web',
});

// Track auth status
analytics.track('Auth Status Checked', {
  authenticated: boolean,
  duration: number, // ms
});

// Track navigation
analytics.track('Navigated From Splash', {
  destination: string, // 'home' | 'onboarding'
  duration: number, // ms spent on splash
});
```

---

## 🎯 Success Metrics

### User Experience
- **Time on splash**: 2-3 seconds (target)
- **Animation smoothness**: 60 FPS
- **Perceived performance**: Fast, smooth, professional

### Technical
- **Load time**: < 1s
- **Auth check**: < 500ms
- **Navigation**: < 100ms after auth check

---

## 🔍 Testing Checklist

- [ ] Logo loads and animates smoothly
- [ ] Wordmark fades in correctly
- [ ] Tagline appears with proper timing
- [ ] Loading dots animate sequentially
- [ ] Navigation works (authenticated)
- [ ] Navigation works (new user)
- [ ] Error handling works (offline)
- [ ] Timeout handling works (slow network)
- [ ] Reduced motion respected
- [ ] Screen reader announces correctly
- [ ] 60 FPS on mobile devices
- [ ] No console errors or warnings

---

## 📱 Device Testing

### Minimum Requirements
- **iPhone SE (2020)**: 375×667
- **Android (Pixel 5)**: 393×851
- **iPad**: 768×1024
- **Desktop**: 1440×900

### Performance Targets
- **60 FPS** on all devices
- **< 1s** load time on 4G
- **< 500ms** on WiFi

---

## 🎨 Design Tokens

```json
{
  "splash": {
    "background": "#FFFFFF",
    "logo": {
      "size": {
        "mobile": "120px",
        "tablet": "140px",
        "desktop": "160px"
      },
      "gradient": {
        "start": "#06B6D4",
        "end": "#0284C7"
      }
    },
    "wordmark": {
      "fontSize": {
        "mobile": "32px",
        "tablet": "36px",
        "desktop": "40px"
      },
      "fontWeight": "700",
      "color": "#111827"
    },
    "tagline": {
      "fontSize": {
        "mobile": "16px",
        "tablet": "18px",
        "desktop": "20px"
      },
      "fontWeight": "400",
      "color": "#6B7280"
    },
    "loading": {
      "dotSize": "8px",
      "dotGap": "12px",
      "dotColor": "#06B6D4",
      "animationDuration": "1.2s"
    },
    "spacing": {
      "logoToWordmark": {
        "mobile": "24px",
        "tablet": "28px",
        "desktop": "32px"
      },
      "wordmarkToTagline": {
        "mobile": "12px",
        "tablet": "14px",
        "desktop": "16px"
      },
      "taglineToLoading": {
        "mobile": "48px",
        "tablet": "56px",
        "desktop": "64px"
      }
    }
  }
}
```

---

## 📝 Implementation Notes

### React/Next.js Component
```typescript
'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuthStore } from '@/stores/authStore';

export default function SplashScreen() {
  const router = useRouter();
  const { session, checkAuth } = useAuthStore();

  useEffect(() => {
    const init = async () => {
      // Minimum splash duration: 2s
      const minDuration = 2000;
      const startTime = Date.now();

      // Check auth status
      await checkAuth();

      // Wait for minimum duration
      const elapsed = Date.now() - startTime;
      const remaining = Math.max(0, minDuration - elapsed);
      await new Promise(resolve => setTimeout(resolve, remaining));

      // Navigate based on auth status
      if (session) {
        router.push('/home');
      } else {
        router.push('/onboarding');
      }
    };

    init();
  }, []);

  return (
    <div className="splash-screen">
      <div className="splash-content">
        <img src="/logo.svg" alt="Catching Barrels" className="logo" />
        <h1 className="wordmark">Catching Barrels</h1>
        <p className="tagline">Your swing, optimized.</p>
        <div className="loading-dots">
          <span className="dot"></span>
          <span className="dot"></span>
          <span className="dot"></span>
          <span className="dot"></span>
        </div>
      </div>
    </div>
  );
}
```

---

## ✅ Definition of Done

- [ ] Logo SVG created and optimized
- [ ] Logo animation implemented (fade + scale)
- [ ] Wordmark styles correct
- [ ] Tagline styles correct
- [ ] Loading dots animate sequentially
- [ ] Auth check implemented
- [ ] Navigation logic works (authenticated)
- [ ] Navigation logic works (new user)
- [ ] Error handling implemented
- [ ] Timeout handling implemented
- [ ] Reduced motion respected
- [ ] Screen reader accessible
- [ ] 60 FPS animation on mobile
- [ ] Lighthouse score > 90
- [ ] No console errors

---

**Priority**: P0 (Critical Path)  
**Complexity**: LOW (Simplest screen)  
**Estimated Dev Time**: 2-3 hours (Phase 1)

**Dependencies**:
- Logo SVG asset
- Inter font loaded
- Auth service configured
- Routing setup

---

*Last Updated: December 27, 2025*  
*Screen Specification v1.0*
