# Screen 06: Splash Screen

**Screen Name:** Splash Screen  
**Route:** `/` (initial load)  
**Complexity:** LOW  
**Priority:** P0

**Version:** 2.0  
**Date:** 2025-12-26  
**Status:** Design Specification

---

## 📋 Overview

The Splash Screen is the first screen users see when opening the app. It displays the Catching Barrels logo and tagline, then auto-advances to either the Onboarding flow (first-time users) or the Home Dashboard (returning users).

**Key Features:**
- Catching Barrels logo (96×96 or larger)
- Tagline: "Unlock Your Kinetic Potential"
- Auto-advance after 2 seconds
- Skip button for accessibility
- Fade-in animation

---

## 🎨 Layout (Mobile: 375×812)

\`\`\`
┌─────────────────────────────────────┐
│                                     │
│                                     │
│                                     │
│                 ⚾                  │  ← Logo (96×96)
│     CATCHING BARRELS                │  ← App name (32px)
│                                     │
│   Unlock Your Kinetic Potential     │  ← Tagline (16px)
│                                     │
│                                     │
│                                     │
│            [Skip →]                 │  ← Skip button (bottom)
│                                     │
└─────────────────────────────────────┘
\`\`\`

**Viewport:** 375×812 (mobile portrait)
**Background:** #FAFAFA or white
**Animation:** Fade-in over 300ms

---

## 🎨 Visual Specifications

### **Logo**
- Size: 96×96px (mobile), 128×128px (tablet/desktop)
- Color: Electric Cyan #06B6D4
- Style: Baseball bat icon or "CB" monogram

### **App Name**
- Text: "CATCHING BARRELS"
- Font: Inter, 32px, Bold (700)
- Color: #111827
- Spacing: 16px below logo

### **Tagline**
- Text: "Unlock Your Kinetic Potential"
- Font: Inter, 16px, Regular (400)
- Color: #6B7280
- Spacing: 8px below app name

### **Skip Button**
- Position: Bottom center, 40px from bottom
- Text: "Skip →"
- Font: Inter, 14px, Medium (500)
- Color: #06B6D4
- Tap target: 44×44px minimum

---

## ⚙️ Behavior

### **Auto-Advance Logic**
\`\`\`
1. App loads → Display Splash Screen
2. Wait 2000ms (2 seconds)
3. Check user state:
   - IF first_time_user → Navigate to /onboarding/1
   - ELSE → Navigate to /home
\`\`\`

### **Skip Button**
- Tap "Skip" → Immediately check user state and navigate
- No waiting for 2-second timer

### **Animation Timing**
- Fade-in: 0-300ms (logo, app name, tagline)
- Display: 300-2000ms (hold for 1.7 seconds)
- Fade-out: 2000-2300ms (transition to next screen)

---

## 🔌 API / Data Binding

**Check User State:**
\`\`\`typescript
// On splash screen mount
async function checkUserState() {
  const hasSeenOnboarding = localStorage.getItem('has_seen_onboarding');
  
  if (hasSeenOnboarding === 'true') {
    // Returning user → Home
    router.push('/home');
  } else {
    // First-time user → Onboarding
    router.push('/onboarding/1');
  }
}
\`\`\`

---

## 💻 React Implementation

\`\`\`tsx
'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';

const SplashScreen: React.FC = () => {
  const router = useRouter();
  const [fadeOut, setFadeOut] = useState(false);

  useEffect(() => {
    // Auto-advance after 2 seconds
    const timer = setTimeout(() => {
      handleAdvance();
    }, 2000);

    return () => clearTimeout(timer);
  }, []);

  const handleAdvance = () => {
    setFadeOut(true);
    
    setTimeout(() => {
      const hasSeenOnboarding = localStorage.getItem('has_seen_onboarding');
      
      if (hasSeenOnboarding === 'true') {
        router.push('/home');
      } else {
        router.push('/onboarding/1');
      }
    }, 300); // Fade-out duration
  };

  const handleSkip = () => {
    handleAdvance();
  };

  return (
    <div className={\`splash-screen \${fadeOut ? 'fade-out' : 'fade-in'}\`}>
      {/* Logo */}
      <div className="logo">⚾</div>
      
      {/* App Name */}
      <h1 className="app-name">CATCHING BARRELS</h1>
      
      {/* Tagline */}
      <p className="tagline">Unlock Your Kinetic Potential</p>
      
      {/* Skip Button */}
      <button 
        className="skip-button" 
        onClick={handleSkip}
        aria-label="Skip splash screen"
      >
        Skip →
      </button>
    </div>
  );
};

export default SplashScreen;
\`\`\`

---

## 🎨 CSS Styling

\`\`\`css
.splash-screen {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: #FAFAFA;
  padding: 24px;
}

.logo {
  font-size: 96px;
  margin-bottom: 16px;
}

.app-name {
  font-size: 32px;
  font-weight: 700;
  color: #111827;
  margin-bottom: 8px;
  text-align: center;
  letter-spacing: 0.05em;
}

.tagline {
  font-size: 16px;
  font-weight: 400;
  color: #6B7280;
  text-align: center;
}

.skip-button {
  position: absolute;
  bottom: 40px;
  font-size: 14px;
  font-weight: 500;
  color: #06B6D4;
  background: none;
  border: none;
  cursor: pointer;
  min-width: 44px;
  min-height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.skip-button:hover {
  text-decoration: underline;
}

/* Animations */
.fade-in {
  animation: fadeIn 300ms ease-in;
}

.fade-out {
  animation: fadeOut 300ms ease-out;
  opacity: 0;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes fadeOut {
  from { opacity: 1; }
  to { opacity: 0; }
}
\`\`\`

---

## ♿ Accessibility

- **Skip Button:** Allows users to bypass splash screen immediately
- **ARIA Labels:** Skip button has aria-label="Skip splash screen"
- **Focus Management:** Skip button is keyboard-accessible (Tab, Enter)
- **No Motion:** Respects prefers-reduced-motion media query

---

## 📱 Responsive Behavior

- **Mobile (375px):** Logo 96px, App Name 32px
- **Tablet (768px):** Logo 112px, App Name 36px
- **Desktop (1024px+):** Logo 128px, App Name 40px

---

## 🎯 Success Criteria

1. ✅ Logo visible (96×96 or larger)
2. ✅ Tagline: "Unlock Your Kinetic Potential"
3. ✅ Auto-advance after 2 seconds
4. ✅ Skip button functional
5. ✅ Routes to /onboarding/1 (first-time) or /home (returning)
6. ✅ Fade-in/fade-out animations

---

**Priority:** P0  
**Complexity:** LOW  
**Est. Time:** 1-2 hours

---

*Last Updated: December 26, 2025*
