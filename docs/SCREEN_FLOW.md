# Screen Flow & Navigation
## Catching Barrels PWA
**Version:** 2.0  
**Last Updated:** December 26, 2025  
**Status:** Design Specification — Complete

---

## Table of Contents
1. [Overview](#overview)
2. [Navigation Architecture](#navigation-architecture)
3. [User Flows](#user-flows)
4. [Screen Flow Diagrams](#screen-flow-diagrams)
5. [Interaction Patterns](#interaction-patterns)
6. [Error States](#error-states)

---

## 1. Overview

### Purpose
This document defines the navigation structure and user flows for all 13 screens in the Catching Barrels PWA.

### Key Principles
- **Mobile-First:** Bottom navigation for primary actions
- **Minimal Taps:** < 3 taps to any feature
- **Clear Hierarchy:** Primary → Secondary → Tertiary actions
- **Persistent Context:** Bottom nav always visible
- **Gestural Navigation:** Swipe-back, pull-to-refresh

### Navigation Types
1. **Bottom Navigation** — Primary screens (Home, Upload, Report, More)
2. **Header Navigation** — Back button, page title, actions
3. **Modal Navigation** — Onboarding, settings, dialogs
4. **Deep Links** — Direct access to specific screens

---

## 2. Navigation Architecture

### 2.1 Bottom Navigation (Primary)

```
┌─────────────────────────────────┐
│                                 │
│        [Content Area]           │
│                                 │
├─────────────────────────────────┤
│  Home  Upload  Report   More    │  ← Bottom Nav (always visible)
└─────────────────────────────────┘
```

**Bottom Nav Items:**
1. **Home** — `/` — Dashboard (KRS, Progress, Drills)
2. **Upload** — `/upload` — Record/Upload swings
3. **Report** — `/report` — Player metrics & 4B breakdown
4. **More** — `/more` — Settings, Profile, Drills, Progress

**Active States:**
- Active: Electric Cyan (#06B6D4), filled icon
- Inactive: Slate 400 (#94A3B8), outline icon
- Badge: Red dot for notifications

---

### 2.2 Header Navigation (Secondary)

```
┌─────────────────────────────────┐
│  ← Back   Page Title   Action   │  ← Header
├─────────────────────────────────┤
│                                 │
│        [Content Area]           │
│                                 │
└─────────────────────────────────┘
```

**Header Components:**
- **Left:** Back button (← icon) → Previous screen
- **Center:** Page title (16px bold)
- **Right:** Context action (Share, Edit, Help)

**Visibility:**
- Always visible on secondary screens
- Hidden on primary screens (Home, Upload, Report, More)

---

### 2.3 Modal Navigation (Tertiary)

**Full-Screen Modals:**
- Onboarding (4 screens, swipe/tap navigation)
- Settings (scroll, back to close)
- Movement Assessment (5 movements, next/back buttons)
- Motor Profile Result (full-screen, tap to continue)

**Overlay Modals:**
- Confirmation dialogs
- Error alerts
- Success messages

**Gesture Dismissal:**
- Swipe down to dismiss (iOS pattern)
- Tap outside to dismiss (Android pattern)
- ESC key to dismiss (desktop)

---

## 3. User Flows

### 3.1 First-Time User Flow (New User Onboarding)

```
┌─────────────┐
│   Splash    │ 2s auto-advance or tap Skip
│  (Screen 6) │
└──────┬──────┘
       │
       ↓
┌─────────────┐
│ Onboarding  │ 4 screens: KRS → Profiles → Modes → Progress
│  (Screen 7) │ Swipe or tap Next
└──────┬──────┘
       │
       ↓
┌─────────────┐
│   Create    │ Name, Age, Height, Weight, Team, Position
│   Profile   │ Tap Create Profile
│  (Screen 8) │
└──────┬──────┘
       │
       ↓
┌─────────────┐
│  Movement   │ 5 movements × 4 states = 20 assessments
│ Assessment  │ Tap Start → Complete → Next Movement
│  (Screen 4) │
└──────┬──────┘
       │
       ↓
┌─────────────┐
│   Motor     │ Result: Whipper (example)
│   Profile   │ Confidence: 92%
│   Result    │ Tap Continue
│  (Screen 5) │
└──────┬──────┘
       │
       ↓
┌─────────────┐
│    Home     │ Dashboard with KRS 0, empty state
│ Dashboard   │ "Upload your first swing!"
│  (Screen 1) │
└─────────────┘
```

**Estimated Time:** 5-8 minutes  
**Exit Points:** Skip Onboarding → Home, Skip Assessment → Home (profile incomplete)

---

### 3.2 Upload & Analysis Flow (Returning User)

```
┌─────────────┐
│    Home     │ Tap "Upload Swing" button
│ Dashboard   │
│  (Screen 1) │
└──────┬──────┘
       │
       ↓
┌─────────────┐
│   Upload    │ Option A: Record (Live Mode)
│  (Screen 9) │ Option B: Upload (from gallery)
└──────┬──────┘
       │
       ├─────→ Option A: Record (Live Mode)
       │       ┌─────────────┐
       │       │ Live Mode   │ 60 FPS positional feedback
       │       │ (Screen 2)  │ Tap Stop Recording
       │       └──────┬──────┘
       │              │
       ├─────→ Option B: Upload
       │       (Select video from gallery)
       │
       ↓
┌─────────────┐
│ Processing  │ 60-90s processing
│ (Screen 10) │ Progress bar, status updates
└──────┬──────┘
       │
       ↓
┌─────────────┐
│   Player    │ KRS updated (e.g., 75)
│   Report    │ 4B Framework cards
│  (Screen 3) │ Tap Share or View Breakdown
└──────┬──────┘
       │
       ↓
┌─────────────┐
│    Home     │ Dashboard updated with new KRS
│ Dashboard   │ 30-Day Progress chart updated
│  (Screen 1) │
└─────────────┘
```

**Estimated Time:** 3-5 minutes (record/upload + processing + review)  
**Exit Points:** Cancel Upload → Home, Cancel Processing → Home (swing saved as draft)

---

### 3.3 Progress Review Flow

```
┌─────────────┐
│    Home     │ Tap "View Progress" or bottom nav → More → Progress
│ Dashboard   │
│  (Screen 1) │
└──────┬──────┘
       │
       ↓
┌─────────────┐
│  Progress   │ KRS journey chart (0-100 scale)
│ Dashboard   │ Session history list
│ (Screen 12) │ Tap Session to view details
└──────┬──────┘
       │
       ↓
┌─────────────┐
│   Player    │ Session-specific KRS
│   Report    │ 4B breakdown for that session
│  (Screen 3) │ Tap Back to Progress
└──────┬──────┘
       │
       ↓
┌─────────────┐
│  Progress   │ Return to session list
│ Dashboard   │
│ (Screen 12) │
└─────────────┘
```

**Estimated Time:** 2-3 minutes  
**Exit Points:** Back to Home (bottom nav), Deep link to specific session

---

### 3.4 Drills Discovery Flow

```
┌─────────────┐
│    Home     │ Tap "Recommended Drills" card
│ Dashboard   │
│  (Screen 1) │
└──────┬──────┘
       │
       ↓
┌─────────────┐
│   Drills    │ 10-15 drills (personalized)
│   Library   │ Filter by category (Brain, Body, Bat, Ball)
│ (Screen 11) │ Tap Drill card
└──────┬──────┘
       │
       ↓
┌─────────────┐
│    Drill    │ Video preview, Instructions, Benefits
│   Detail    │ Tap Start Drill → External video player
│   (Modal)   │ Tap Back to Library
└──────┬──────┘
       │
       ↓
┌─────────────┐
│   Drills    │ Return to library
│   Library   │
│ (Screen 11) │
└─────────────┘
```

**Estimated Time:** 1-2 minutes (discovery + detail view)  
**Exit Points:** Back to Home, Start Drill → External video player

---

## 4. Screen Flow Diagrams

### 4.1 Complete Screen Map (All 13 Screens)

```
                        ┌─────────────┐
                        │   Splash    │
                        │  (Screen 6) │
                        └──────┬──────┘
                               │
                               ↓
                        ┌─────────────┐
                        │ Onboarding  │
                        │  (Screen 7) │
                        └──────┬──────┘
                               │
                               ↓
                        ┌─────────────┐
                        │   Create    │
                        │   Profile   │
                        │  (Screen 8) │
                        └──────┬──────┘
                               │
                               ↓
                        ┌─────────────┐
                        │  Movement   │
                        │ Assessment  │
                        │  (Screen 4) │
                        └──────┬──────┘
                               │
                               ↓
                        ┌─────────────┐
                        │   Motor     │
                        │   Profile   │
                        │   Result    │
                        │  (Screen 5) │
                        └──────┬──────┘
                               │
                               ↓
┌───────────────────────────────────────────────────────────────┐
│                     PRIMARY NAVIGATION                        │
│                    (Bottom Navigation Bar)                    │
├───────────────┬──────────────┬──────────────┬─────────────────┤
│     Home      │   Upload     │    Report    │      More       │
│  (Screen 1)   │  (Screen 9)  │  (Screen 3)  │  (Menu/Drills)  │
└───────┬───────┴──────┬───────┴──────┬───────┴────────┬────────┘
        │              │              │                │
        ↓              ↓              ↓                ↓
┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│ 30-Day      │ │ Live Mode   │ │ KRS Hero    │ │  Progress   │
│ Progress    │ │ (Screen 2)  │ │ Display     │ │ Dashboard   │
│ Chart       │ │             │ │             │ │ (Screen 12) │
└─────────────┘ └──────┬──────┘ └─────────────┘ └─────────────┘
                       │
                       ↓
                ┌─────────────┐
                │ Processing  │
                │ (Screen 10) │
                └──────┬──────┘
                       │
                       ↓
                ┌─────────────┐
                │   Player    │
                │   Report    │
                │  (Screen 3) │
                └─────────────┘

More Menu → Settings (Screen 13)
         → Drills Library (Screen 11)
         → Progress Dashboard (Screen 12)
         → Profile Edit
         → Help & Support
```

---

### 4.2 Bottom Navigation Flow

```
                        [Any Screen]
                             │
                             ↓
            ┌────────────────┼────────────────┐
            │                │                │
    ┌───────▼───────┐ ┌─────▼─────┐ ┌────────▼────────┐
    │   Tap Home    │ │ Tap Upload│ │   Tap Report    │
    │   Nav Icon    │ │  Nav Icon │ │    Nav Icon     │
    └───────┬───────┘ └─────┬─────┘ └────────┬────────┘
            │                │                │
            ↓                ↓                ↓
    ┌───────────────┐ ┌─────────────┐ ┌─────────────────┐
    │     Home      │ │   Upload    │ │  Player Report  │
    │   Dashboard   │ │   Screen    │ │   (Screen 3)    │
    │  (Screen 1)   │ │  (Screen 9) │ │                 │
    └───────────────┘ └─────────────┘ └─────────────────┘
            │                │                │
            ↓                ↓                ↓
    [Bottom Nav Active: Home]   [Upload]   [Report]
```

**Navigation Rules:**
- Tapping active tab scrolls to top
- Tapping inactive tab navigates to that screen
- Back button returns to previous screen (not bottom nav)
- Bottom nav persists across all primary screens

---

### 4.3 Modal Flow Pattern

```
         ┌─────────────┐
         │  Any Screen │
         └──────┬──────┘
                │
                ↓ Trigger Action (button, link)
         ┌─────────────┐
         │    Modal    │
         │   Overlay   │
         │             │
         │  [Content]  │
         │             │
         │ [Actions]   │
         └──────┬──────┘
                │
    ┌───────────┼───────────┐
    │                       │
    ↓                       ↓
[Dismiss]              [Action]
    │                       │
    ↓                       ↓
[Return to           [Execute Action
 Previous Screen]     → New Screen]
```

**Dismissal Methods:**
- Tap close button (× icon)
- Swipe down (iOS pattern)
- Tap outside modal (dimmed background)
- ESC key (desktop)
- Back button (Android)

---

## 5. Interaction Patterns

### 5.1 Tap Targets

**Minimum Size:** 44×44px (iOS), 48×48px (Android)

**Component Sizes:**
- Button: 48px height, full width
- Icon button: 44×44px touch area
- List item: 56px min height
- Card: Full width, 120px min height
- Bottom nav item: 56px height, 80px width

---

### 5.2 Gestures

**Swipe:**
- Swipe left/right: Navigate between onboarding screens
- Swipe down: Dismiss modal (iOS)
- Swipe back: Return to previous screen (iOS edge swipe)

**Pinch-to-Zoom:**
- Enabled on video player
- Disabled on UI elements

**Pull-to-Refresh:**
- Home Dashboard: Refresh KRS and progress data
- Progress Dashboard: Refresh session history
- Drills Library: Refresh drill recommendations

**Long Press:**
- Drill card: Quick actions (Add to favorites, Share)
- Session item: Quick actions (View details, Delete)

---

### 5.3 Transitions

**Page Transitions:**
- Default: Slide left (forward), slide right (back)
- Modal: Slide up (open), slide down (close)
- Duration: 300ms ease-in-out

**Component Transitions:**
- Fade: 200ms (loading states, tooltips)
- Scale: 150ms (button press, card tap)
- Slide: 300ms (drawer open/close)

---

### 5.4 Loading States

**Skeleton Screens:**
- Home Dashboard: KRS skeleton, chart skeleton, card skeletons
- Drills Library: Drill card skeletons (3×)
- Progress Dashboard: Chart skeleton, list skeletons

**Progress Indicators:**
- Processing: Linear progress bar (0-100%)
- Upload: Circular progress (upload %)
- Live Mode: Recording timer (seconds elapsed)

**Empty States:**
- No swings: "Upload your first swing!" with Upload button
- No drills: "No drills match your filters" with Reset button
- No sessions: "Start your KRS journey today!" with Upload button

---

## 6. Error States

### 6.1 Network Errors

**Offline:**
```
┌─────────────────────────────────┐
│  ⚠️  No Internet Connection     │
│                                 │
│  Please check your connection   │
│  and try again.                 │
│                                 │
│  [Retry]         [Go Offline]   │
└─────────────────────────────────┘
```

**Timeout:**
```
┌─────────────────────────────────┐
│  ⏱️  Request Timed Out          │
│                                 │
│  The server took too long to    │
│  respond. Please try again.     │
│                                 │
│  [Retry]              [Cancel]  │
└─────────────────────────────────┘
```

---

### 6.2 Validation Errors

**Form Validation:**
```
┌─────────────────────────────────┐
│  Name *                         │
│  [John Doe______________]       │
│                                 │
│  Age *                          │
│  [5_____]                       │
│  ⚠️  Age must be 8-18 years     │  ← Inline error
│                                 │
│  [Create Profile]               │  ← Disabled until valid
└─────────────────────────────────┘
```

**Upload Validation:**
```
┌─────────────────────────────────┐
│  ⚠️  Invalid Video Format       │
│                                 │
│  Please upload a video in       │
│  MP4, MOV, or AVI format.       │
│                                 │
│  [Upload Another]    [Cancel]   │
└─────────────────────────────────┘
```

---

### 6.3 Processing Errors

**Analysis Failed:**
```
┌─────────────────────────────────┐
│  ❌  Analysis Failed             │
│                                 │
│  We couldn't detect a swing in  │
│  this video. Please try:        │
│                                 │
│  • Ensure good lighting         │
│  • Film from the side view      │
│  • Keep the camera steady       │
│                                 │
│  [Try Another Video]  [Cancel]  │
└─────────────────────────────────┘
```

**Low Confidence:**
```
┌─────────────────────────────────┐
│  ⚠️  Low Confidence Results     │
│                                 │
│  KRS: 68 (Confidence: 55%)      │
│                                 │
│  Results may be less accurate.  │
│  Consider re-recording with:    │
│  • Better lighting              │
│  • Full body in frame           │
│                                 │
│  [Accept]        [Re-Record]    │
└─────────────────────────────────┘
```

---

## Summary

### Navigation Architecture
- **3-Tier System:** Bottom Nav (primary) → Header Nav (secondary) → Modals (tertiary)
- **13 Total Screens:** 4 primary (bottom nav) + 9 secondary/modal
- **< 3 Taps:** To any feature from home

### Key User Flows
1. **First-Time:** Splash → Onboarding → Profile → Assessment → Home (5-8 min)
2. **Upload:** Home → Upload → Processing → Report → Home (3-5 min)
3. **Progress:** Home → Progress → Session Detail → Home (2-3 min)
4. **Drills:** Home → Drills → Detail → Home (1-2 min)

### Interaction Patterns
- **Tap Targets:** 44×44px minimum
- **Gestures:** Swipe, pinch, pull-to-refresh, long press
- **Transitions:** 300ms slide, 200ms fade, 150ms scale
- **Loading:** Skeleton screens, progress bars, empty states

### Error Handling
- **Network:** Offline, timeout with retry
- **Validation:** Inline errors, disabled actions
- **Processing:** Failed analysis, low confidence warnings

**Estimated Review Time:** 45-60 minutes  
**Next Steps:** Review flows, validate tap counts, test on device

---

**Last Updated:** December 26, 2025  
**Contact:** Builder 2 — Phase 0 Corrections
