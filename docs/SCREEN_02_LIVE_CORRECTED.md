# 📱 Screen 02: Live Mode - CORRECTED VERSION

**Version:** 2.0 (Corrected)  
**Date:** December 26, 2025  
**Device:** Mobile landscape + portrait (375×812)  
**Status:** Design Specification - VALIDATED

**⚠️ CRITICAL CORRECTIONS APPLIED:**
- Live Mode provides POSITIONAL FEEDBACK ONLY (60 FPS camera)
- Does NOT show Exit Velocity (requires radar or 240+ FPS)
- Does NOT show Launch Angle (requires ball tracking)
- Does NOT show Bat Speed (unreliable at 60 FPS)
- Focus: Pose quality, phase detection, coaching cues

---

## 🎯 Overview

**Purpose:** Real-time swing coaching with 60 FPS camera + pose detection  
**Entry Point:** From Home (Quick Actions) or Bottom Nav  
**Key Features:** Camera overlay, pose skeleton, phase detection, coaching cues, positional feedback

**⚠️ TECHNICAL CONSTRAINTS:**
- **Camera Input**: 60 FPS (standard mobile camera)
- **Can Measure**: Body positions, joint angles, timing, sequencing
- **Cannot Measure**: Exit velocity, launch angle, bat speed (requires 240 FPS or external sensors)

---

## 📐 Layout Specification

### **Orientation: LANDSCAPE (Recommended)**
```
Width: 812px (landscape)
Height: 375px
Reason: Better camera framing for full-body swing capture
```

### **Portrait Fallback**
```
Width: 375px
Height: 812px
Note: Less ideal but supported
```

---

## 🎬 Screen Structure (Landscape)

```
┌──────────────────────────────────────────────────────────────┐
│ Camera Feed (Full Screen)                                    │
│ ┌──────────────────────────────────────────────────────────┐ │
│ │ Top HUD (Gradient Overlay)                               │ │
│ │ [X] Close    Motor: Spinner 🏹    [Settings]             │ │
│ └──────────────────────────────────────────────────────────┘ │
│                                                               │
│ ┌──┐  ← Status Pills (Left Side, Vertical Stack)            │
│ │🟢│    ✓ Hip Rotation                                       │
│ │🟢│    ✓ Knee Bend                                          │
│ │🟡│    ⚠ Lead Leg                                           │
│ │⚪│    ○ Shoulder Tilt                                      │
│ └──┘                                                          │
│                                                               │
│         👤 Pose Skeleton (32 keypoints, cyan overlay)        │
│         👤 Template Skeleton (Motor Profile, blue, ghost)    │
│                                                               │
│ ┌──────────────────────────────────────────────────────────┐ │
│ │ Bottom HUD (Gradient Overlay)                            │ │
│ │                                                           │ │
│ │ [Coach Cue Card: "Drive back knee toward pitcher"]      │ │
│ │                                                           │ │
│ │ Phase: [Setup] [Load] [Launch] [Contact] [Follow]       │ │
│ │                                                           │ │
│ │ Swings: 8  |  Session: 00:04:32                         │ │
│ │                                                           │ │
│ │ [Flip] [●REC] [Gallery]                                  │ │
│ └──────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
```

---

## 🧱 Component Breakdown

### **1. Top HUD (64px height)**

**Layout:**
```html
<div class="absolute top-0 left-0 right-0 h-16 bg-gradient-to-b from-black/60 to-transparent px-4 flex items-center justify-between">
  <!-- Left: Close Button -->
  <button class="w-10 h-10 rounded-full bg-black/40 backdrop-blur-sm flex items-center justify-center">
    <IconX class="w-5 h-5 text-white" />
  </button>
  
  <!-- Center: Motor Profile Badge -->
  <div class="px-4 py-2 bg-white/20 backdrop-blur-md rounded-full flex items-center gap-2">
    <span class="text-xl">🏹</span>
    <span class="text-sm font-semibold text-white">Spinner</span>
  </div>
  
  <!-- Right: Settings -->
  <button class="w-10 h-10 rounded-full bg-black/40 backdrop-blur-sm flex items-center justify-center">
    <IconSettings class="w-5 h-5 text-white" />
  </button>
</div>
```

**Design Details:**
- Background: Gradient from black/60 to transparent
- Buttons: Glassmorphism (white/20 + backdrop blur)
- Icons: White, 20px
- Motor Profile badge: Glass pill with icon + text (Spinner/Slingshotter/Whipper/Titan)

**Interactions:**
- Close (X) → Exit Live Mode, return to Home
- Settings → Open camera settings (resolution, grid overlay, coaching verbosity)

---

### **2. Status Pills (Left Side, Vertical) ✅ CORRECTED**

**Layout:**
```html
<div class="absolute left-4 top-20 space-y-2">
  <!-- Green: Good -->
  <div class="px-3 py-2 bg-white/90 backdrop-blur-md rounded-full flex items-center gap-2 shadow-lg">
    <div class="w-2 h-2 rounded-full bg-green-500 animate-pulse"></div>
    <span class="text-xs font-semibold text-gray-900">Hip Rotation</span>
  </div>
  
  <!-- Green: Good -->
  <div class="px-3 py-2 bg-white/90 backdrop-blur-md rounded-full flex items-center gap-2 shadow-lg">
    <div class="w-2 h-2 rounded-full bg-green-500 animate-pulse"></div>
    <span class="text-xs font-semibold text-gray-900">Knee Bend</span>
  </div>
  
  <!-- Yellow: Warning -->
  <div class="px-3 py-2 bg-white/90 backdrop-blur-md rounded-full flex items-center gap-2 shadow-lg">
    <div class="w-2 h-2 rounded-full bg-yellow-500 animate-pulse"></div>
    <span class="text-xs font-semibold text-gray-900">Lead Leg</span>
  </div>
  
  <!-- Gray: Neutral -->
  <div class="px-3 py-2 bg-white/90 backdrop-blur-md rounded-full flex items-center gap-2 shadow-lg">
    <div class="w-2 h-2 rounded-full bg-gray-400"></div>
    <span class="text-xs font-semibold text-gray-900">Shoulder Tilt</span>
  </div>
</div>
```

**Design Details:**
- Background: White/90 + backdrop blur (glassmorphism)
- Dot: 8px circle, colored based on status
- Pulse animation on active statuses
- Text: 12px, semibold, black

**Color Logic:**
```
Green (#10B981): On target (within 5° of ideal angle)
Yellow (#F59E0B): Close (5-15° off ideal)
Red (#EF4444): Off target (>15° off ideal)
Gray (#9CA3AF): Not yet evaluated / neutral
```

**✅ POSITIONAL METRICS ONLY (60 FPS Camera Can Measure):**

1. **Hip Rotation**
   - Angle between hips and shoulders at load
   - Target: 40-60° (varies by motor profile)
   - Calculation: Pose estimation of hip/shoulder landmarks

2. **Knee Bend**
   - Back leg knee angle at launch
   - Target: 135-165° (slightly bent to straight)
   - Calculation: Thigh-shin angle from pose

3. **Lead Leg**
   - Lead knee angle and stability
   - Target: No early collapse (<90°)
   - Warning: Collapsing before contact

4. **Shoulder Tilt**
   - Upper body tilt relative to vertical
   - Target: 5-15° away from pitcher
   - Calculation: Shoulder line angle

5. **Weight Transfer** (additional metric)
   - Hip position shift from setup to contact
   - Target: Forward progression
   - Calculation: Center of mass estimation

6. **Posture**
   - Spine angle and head position
   - Target: Tall spine, head still
   - Calculation: Torso landmarks

**❌ CANNOT SHOW IN LIVE MODE:**
- Exit Velocity (requires radar or 240+ FPS for ball tracking)
- Launch Angle (requires ball trajectory tracking)
- Bat Speed (unreliable at 60 FPS, needs high-speed video)
- Bat Path Angle (requires accurate bat tracking)
- Contact Point (requires ball-bat collision detection)

**💡 For Full KRS Analysis:**
- User must upload 240 FPS high-speed video
- OR use external sensors (radar, TrackMan, etc.)
- Live Mode = Daily practice with positional feedback
- KRS Mode = Full biomechanical analysis

---

### **3. Camera Feed + Pose Overlay**

**Canvas Layer Structure:**
```html
<div class="relative w-full h-full">
  <!-- Video Element (Camera Feed) -->
  <video 
    ref={videoRef}
    class="absolute inset-0 w-full h-full object-cover"
    autoplay 
    playsInline
  ></video>
  
  <!-- Canvas Layer (Pose Overlay) -->
  <canvas 
    ref={canvasRef}
    class="absolute inset-0 w-full h-full pointer-events-none"
  ></canvas>
</div>
```

**Pose Skeleton Design:**
- 32 keypoints from MediaPipe Pose
- Connections: White lines (2px, opacity 0.8)
- Joints: Cyan dots (12px diameter, glow effect)
- Template skeleton: Blue/50, dashed lines (based on motor profile)

**Pose Dot Colors:**
```css
/* Default: Cyan */
.pose-dot {
  fill: #06B6D4;
  filter: drop-shadow(0 0 8px rgba(6, 182, 212, 0.6));
}

/* On Target: Green */
.pose-dot.good {
  fill: #10B981;
  filter: drop-shadow(0 0 8px rgba(16, 185, 129, 0.6));
}

/* Warning: Yellow */
.pose-dot.warning {
  fill: #F59E0B;
  filter: drop-shadow(0 0 8px rgba(245, 158, 11, 0.6));
}

/* Critical: Red */
.pose-dot.critical {
  fill: #EF4444;
  filter: drop-shadow(0 0 8px rgba(239, 68, 68, 0.6));
}
```

**Joint-Specific Coloring:**
- **Hips**: Color based on Hip Rotation status
- **Knees**: Color based on Knee Bend status
- **Shoulders**: Color based on Shoulder Tilt status
- **All others**: Default cyan

---

### **4. Bottom HUD (140px height) ✅ CORRECTED**

**Layout:**
```html
<div class="absolute bottom-0 left-0 right-0 pb-8 bg-gradient-to-t from-black/60 to-transparent">
  <!-- Coach Cue Card -->
  <div class="mx-4 mb-3 p-4 bg-white/90 backdrop-blur-md rounded-2xl shadow-2xl">
    <div class="flex items-center gap-3">
      <div class="w-10 h-10 rounded-full bg-cyan-50 flex items-center justify-center flex-shrink-0">
        <IconTarget class="w-5 h-5 text-cyan-600" />
      </div>
      <p class="text-sm font-medium text-gray-900">
        Drive back knee toward pitcher to maintain weight shift
      </p>
    </div>
  </div>
  
  <!-- Phase Indicator -->
  <div class="flex justify-center gap-2 mb-3 px-4">
    <button class="px-4 py-2 bg-white/20 backdrop-blur-sm rounded-full text-xs font-semibold text-white">
      Setup
    </button>
    <button class="px-4 py-2 bg-white/90 backdrop-blur-sm rounded-full text-xs font-semibold text-gray-900">
      Load
    </button>
    <button class="px-4 py-2 bg-white/20 backdrop-blur-sm rounded-full text-xs font-semibold text-white">
      Launch
    </button>
    <button class="px-4 py-2 bg-white/20 backdrop-blur-sm rounded-full text-xs font-semibold text-white">
      Contact
    </button>
    <button class="px-4 py-2 bg-white/20 backdrop-blur-sm rounded-full text-xs font-semibold text-white">
      Follow
    </button>
  </div>
  
  <!-- Session Stats -->
  <div class="flex justify-center gap-4 mb-3 px-4">
    <div class="px-3 py-1 bg-white/20 backdrop-blur-sm rounded-full">
      <span class="text-xs text-white/80">Swings:</span>
      <span class="text-xs font-bold text-white ml-1">8</span>
    </div>
    <div class="px-3 py-1 bg-white/20 backdrop-blur-sm rounded-full">
      <span class="text-xs text-white/80">Time:</span>
      <span class="text-xs font-bold text-white ml-1">00:04:32</span>
    </div>
  </div>
  
  <!-- Action Buttons -->
  <div class="flex justify-center items-center gap-6">
    <!-- Flip Camera -->
    <button class="w-12 h-12 rounded-full bg-white/20 backdrop-blur-sm flex items-center justify-center">
      <IconRefreshCw class="w-6 h-6 text-white" />
    </button>
    
    <!-- Record Button (Center, Large) -->
    <button class="w-16 h-16 rounded-full bg-red-500 flex items-center justify-center shadow-2xl">
      <div class="w-6 h-6 rounded-full bg-white animate-pulse"></div>
    </button>
    
    <!-- Gallery -->
    <button class="w-12 h-12 rounded-full bg-white/20 backdrop-blur-sm flex items-center justify-center">
      <IconImage class="w-6 h-6 text-white" />
    </button>
  </div>
</div>
```

**Coach Cue Examples (Positional Feedback Only):**
- "Keep your weight 60/40 on your back leg during setup"
- "Drive back knee toward pitcher to maintain weight shift"
- "Maintain hip-shoulder separation through launch"
- "Lead leg is collapsing early - stay tall"
- "Good hip rotation - maintain that tempo"
- "Tilt away slightly to create launch angle"

**❌ DO NOT SHOW:**
- "Increase exit velocity" (can't measure)
- "Adjust launch angle" (can't measure)
- "Swing faster" (can't measure bat speed reliably)

**Design Details:**
- Coach cue: Glass card, white text on white/90 background
- Phase pills: Active = white/90, Inactive = white/20
- Session stats: Swings detected + time elapsed
- Record button: Red circle, large (64px), pulsing white dot
- Flip/Gallery: Smaller glass buttons (48px)

**Interactions:**
- Phase tap → Switch to that phase's template overlay
- Record tap → Start/stop recording swing (saves for later KRS analysis)
- Flip tap → Switch front/back camera
- Gallery tap → View recorded swings (can upload for full analysis)

---

## 🎬 Phase Detection ✅ CORRECTED

**5 Swing Phases:**

1. **Setup** (0.0s)
   - Stance established, weight distribution
   - Check: Hip rotation = 0°, knees bent 15-20°

2. **Load** (0.0-0.3s)
   - Weight shifts back, hands load
   - Check: Hip rotation increases to 40-60°, back knee bent 30-45°

3. **Launch** (0.3-0.4s)
   - Hip rotation initiates, front foot plants
   - Check: Hips begin rotation, lead leg straightens

4. **Contact** (0.4-0.5s)
   - Maximum hip-shoulder separation, bat accelerates
   - Check: Hip-shoulder sep 40-60°, weight forward

5. **Follow-through** (0.5-0.7s)
   - Weight fully transferred, rotation completes
   - Check: Hips fully rotated, balanced finish

**Phase Transition Detection:**
- Pose landmark analysis
- Key angle changes (hip rotation, knee angles)
- Timing thresholds (typical durations)
- NO reliance on ball contact or bat position

---

## 🎨 Color Coding

**Status Colors:**
```
Green (#10B981):  On target (✓ Good)
Yellow (#F59E0B): Warning (⚠ Close)
Red (#EF4444):    Critical (✗ Off target)
Gray (#9CA3AF):   Neutral (○ Not evaluated)
Cyan (#06B6D4):   Default pose overlay
```

**Usage:**
- Status pills: Dot color indicates positional quality
- Pose joints: Color based on specific joint assessment
- Coach cues: Icon color matches severity (green/yellow/red)

---

## 📊 Data Collection (For Future KRS Analysis)

**What Live Mode Saves:**
- Video recording (60 FPS, standard resolution)
- Pose landmarks (32 keypoints per frame)
- Phase timestamps
- Coaching cues triggered
- Session metadata (duration, swings detected)

**For Full KRS Report:**
- User uploads 240+ FPS high-speed video separately
- Backend performs comprehensive biomechanical analysis
- Calculates Creation/Transfer scores, exit velo, bat speed
- Generates full Player Report with 4B Framework

**Live Mode Purpose:**
- Daily practice with real-time positional feedback
- Build muscle memory for motor profile
- Track progress over time (consistency, phase timing)
- NOT a replacement for KRS analysis

---

## ♿ Accessibility

### **Challenges:**
- Camera view is visual-only
- Real-time feedback requires seeing pose overlay

### **Solutions:**
- ✅ Voice coaching cues (optional audio)
- ✅ Haptic feedback for status changes (vibration on warnings)
- ✅ High contrast mode for pose overlay
- ✅ Large touch targets (min 44×44px)

---

## 🧪 Testing Scenarios

### **Scenario 1: Setup Phase**
- User enters stance
- Camera detects 32 keypoints
- Status pills show: Hip Rotation (Gray), Knee Bend (Green), Posture (Green)
- Coach cue: "Weight 60/40 back - looking good"

### **Scenario 2: Load Phase**
- Hip rotation increases to 50°
- Status pills: Hip Rotation (Green), Lead Leg (Yellow - slight drift)
- Coach cue: "Maintain lead leg stability through load"

### **Scenario 3: Launch Phase**
- Hips begin rotating forward
- Lead knee straightens too early
- Status pills: Lead Leg (Red), warning dot pulses
- Coach cue: "Lead knee collapsing early - stay tall"

### **Scenario 4: Recording**
- User taps red record button
- Video saves with pose data
- "Swing recorded! Upload for full KRS analysis" notification

---

## ✅ VALIDATION CHECKLIST

- [x] Live Mode shows ONLY positional feedback (no exit velo/launch angle)
- [x] Status pills measure joint angles and positions
- [x] Coach cues are positional (hip rotation, knee bend, etc.)
- [x] Phase detection based on pose landmarks only
- [x] Recording saves video for future 240 FPS upload
- [x] Clearly distinguishes Live Mode (60 FPS, daily practice) from KRS Mode (240 FPS, full analysis)
- [x] No overpromising on metrics that require high-speed video or sensors
- [x] Template skeleton based on motor profile (Spinner/Slingshotter/Whipper/Titan)

---

## 📱 User Flow

**Entry → Live Mode:**
1. Tap "Live Mode" from Home Dashboard
2. Camera permission prompt (if first time)
3. Camera opens in landscape orientation
4. Motor Profile badge loads (from user profile)
5. Template skeleton overlay appears
6. Real-time pose detection begins

**During Session:**
1. User takes stance (Setup phase detected)
2. Status pills update based on pose quality
3. Coach cues appear as positional issues arise
4. Phase pills highlight current phase
5. User can tap Record to save swing

**Exit → Gallery/Upload:**
1. User taps Gallery to view recorded swings
2. Option to "Upload for KRS Analysis" (240 FPS required)
3. Swings saved locally for reference
4. Return to Home Dashboard

---

**STATUS**: ✅ CORRECTED - Validated for 60 FPS positional feedback only
