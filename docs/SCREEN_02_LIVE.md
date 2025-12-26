# 📱 Screen 2: Live Mode

**Version:** 1.0  
**Date:** December 26, 2025  
**Device:** Mobile landscape + portrait (375×812)  
**Status:** Design Specification

---

## 🎯 Overview

**Purpose:** Real-time swing coaching with 60 FPS camera + pose detection  
**Entry Point:** From Home (Quick Actions) or Bottom Nav  
**Key Features:** Camera overlay, pose skeleton, phase detection, coaching cues

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
│ │🟢│    ✓ Stance                                            │
│ │🟢│    ✓ Timing                                            │
│ │🟡│    ⚠ Balance                                            │
│ │⚪│    ○ Path                                               │
│ └──┘                                                          │
│                                                               │
│         👤 Pose Skeleton (32 keypoints, cyan overlay)        │
│         👤 Template Skeleton (Motor Profile, blue,ghost)     │
│                                                               │
│ ┌──────────────────────────────────────────────────────────┐ │
│ │ Bottom HUD (Gradient Overlay)                            │ │
│ │                                                           │ │
│ │ [Coach Cue Card: "Keep weight back"]                     │ │
│ │                                                           │ │
│ │ Phase: [Setup] [Load] [Launch] [Contact] [Follow]       │ │
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
- Motor Profile badge: Glass pill with icon + text

**Interactions:**
- Close (X) → Exit Live Mode, return to Home
- Settings → Open camera settings (resolution, FPS, grid)

---

### **2. Status Pills (Left Side, Vertical)**

**Layout:**
```html
<div class="absolute left-4 top-20 space-y-2">
  <!-- Green: Good -->
  <div class="px-3 py-2 bg-white/90 backdrop-blur-md rounded-full flex items-center gap-2 shadow-lg">
    <div class="w-2 h-2 rounded-full bg-green-500 animate-pulse"></div>
    <span class="text-xs font-semibold text-gray-900">Stance</span>
  </div>
  
  <!-- Green: Good -->
  <div class="px-3 py-2 bg-white/90 backdrop-blur-md rounded-full flex items-center gap-2 shadow-lg">
    <div class="w-2 h-2 rounded-full bg-green-500 animate-pulse"></div>
    <span class="text-xs font-semibold text-gray-900">Timing</span>
  </div>
  
  <!-- Yellow: Warning -->
  <div class="px-3 py-2 bg-white/90 backdrop-blur-md rounded-full flex items-center gap-2 shadow-lg">
    <div class="w-2 h-2 rounded-full bg-yellow-500 animate-pulse"></div>
    <span class="text-xs font-semibold text-gray-900">Balance</span>
  </div>
  
  <!-- Gray: Neutral -->
  <div class="px-3 py-2 bg-white/90 backdrop-blur-md rounded-full flex items-center gap-2 shadow-lg">
    <div class="w-2 h-2 rounded-full bg-gray-400"></div>
    <span class="text-xs font-semibold text-gray-900">Path</span>
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
Green (#10B981): On target (within 5% of template)
Yellow (#F59E0B): Close (5-15% off template)
Red (#EF4444): Off target (>15% off template)
Gray (#9CA3AF): Not yet evaluated / neutral
```

**Metrics Displayed:**
1. **Stance:** Weight distribution (60/40 back leg)
2. **Timing:** Tempo ratio (ideal range)
3. **Balance:** Stability score
4. **Path:** Bat path angle

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
- Template skeleton: Blue/50, dashed lines

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

---

### **4. Bottom HUD (120px height)**

**Layout:**
```html
<div class="absolute bottom-0 left-0 right-0 pb-8 bg-gradient-to-t from-black/60 to-transparent">
  <!-- Coach Cue Card -->
  <div class="mx-4 mb-4 p-4 bg-white/90 backdrop-blur-md rounded-2xl shadow-2xl">
    <div class="flex items-center gap-3">
      <div class="w-10 h-10 rounded-full bg-cyan-50 flex items-center justify-center flex-shrink-0">
        <IconTarget class="w-5 h-5 text-cyan-600" />
      </div>
      <p class="text-sm font-medium text-gray-900">
        Keep your weight 60/40 on your back leg during setup
      </p>
    </div>
  </div>
  
  <!-- Phase Selector -->
  <div class="flex justify-center gap-2 mb-4 px-4">
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

**Design Details:**
- Coach cue: Glass card, white text on white/90 background
- Phase pills: Active = white/90, Inactive = white/20
- Record button: Red circle, large (64px), pulsing white dot
- Flip/Gallery: Smaller glass buttons (48px)

**Interactions:**
- Phase tap → Switch to that phase's template
- Record tap → Start/stop recording swing
- Flip tap → Switch front/back camera
- Gallery tap → View recorded swings

---

## 🎬 Animations

### **Pose Detection (60 FPS)**
```typescript
// Update pose overlay every frame
function drawPose(pose: PoseLandmarks) {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  
  // Draw connections
  pose.connections.forEach(([start, end]) => {
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.8)';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(pose[start].x, pose[start].y);
    ctx.lineTo(pose[end].x, pose[end].y);
    ctx.stroke();
  });
  
  // Draw keypoints
  pose.landmarks.forEach(point => {
    const color = getStatusColor(point);
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.arc(point.x, point.y, 6, 0, 2 * Math.PI);
    ctx.fill();
  });
}
```

### **Recording Indicator**
```css
/* Pulse animation */
@keyframes pulse {
  0%, 100% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.1);
    opacity: 0.8;
  }
}

.recording-dot {
  animation: pulse 1s ease-in-out infinite;
}
```

---

## ♿ Accessibility

### **Challenges:**
- Camera view is visual-only
- Real-time feedback requires seeing pose overlay

### **Solutions:**
- [ ] Voice coaching cues (optional audio)
- [ ] Haptic feedback for status changes (vibration)
- [ ] High contrast mode for pose overlay
- [ ] Large touch targets (min 44×44px)

---

## 🎨 Color Coding

**Status Colors:**
```
Green: On target (#10B981)
Yellow: Needs adjustment (#F59E0B)
Red: Critical issue (#EF4444)
Cyan: Neutral/default (#06B6D4)
White: UI elements (overlays)
Black: Backgrounds (gradients)
```

---

## 🔧 Technical Requirements

### **Camera:**
- Request 60 FPS (fallback to 30 FPS)
- Resolution: 1280×720 minimum
- Permissions: Camera access required

### **MediaPipe:**
- Pose Detection model
- Real-time inference (<16ms per frame)
- 32 landmarks tracked

### **Performance:**
- 60 FPS rendering
- <8% battery drain per minute
- Smooth animations (no jank)

---

## 📱 Responsive Behavior

### **Landscape (Recommended)**
- Full-screen camera
- Status pills on left
- Bottom HUD with coach cue

### **Portrait (Fallback)**
- Status pills move to top (horizontal)
- Coach cue at bottom
- Record button remains centered bottom

---

## 🧪 States

### **Permission Denied**
```html
<div class="flex flex-col items-center justify-center h-full bg-gray-900 text-white p-8">
  <IconCameraOff class="w-16 h-16 mb-4 text-gray-400" />
  <h2 class="text-xl font-bold mb-2">Camera Access Required</h2>
  <p class="text-center text-gray-400 mb-6">
    Live Mode needs camera access to provide real-time coaching
  </p>
  <button class="px-6 py-3 bg-cyan-500 rounded-xl font-semibold">
    Enable Camera
  </button>
</div>
```

### **Loading (Initializing Camera)**
```html
<div class="flex flex-col items-center justify-center h-full bg-gray-900 text-white">
  <div class="w-16 h-16 border-4 border-gray-700 border-t-cyan-500 rounded-full animate-spin mb-4"></div>
  <p class="text-gray-400">Initializing camera...</p>
</div>
```

### **Recording Active**
- Record button shows "REC" text
- Red dot pulsing in top-right corner
- Coach cue updates in real-time

---

## ✅ Acceptance Criteria

- [ ] Camera feed displays at 55-60 FPS
- [ ] Pose detection runs in real-time (<16ms)
- [ ] 32 keypoints tracked accurately
- [ ] Status pills update every frame
- [ ] Coach cues display based on pose analysis
- [ ] Recording saves to device storage
- [ ] Flip camera works
- [ ] Phase selector changes template
- [ ] Smooth animations (no jank)
- [ ] Battery drain <8% per minute

---

**Status:** DESIGN COMPLETE  
**Next:** Report Screen (4B Breakdown)

---

*End of Live Mode Specification*
