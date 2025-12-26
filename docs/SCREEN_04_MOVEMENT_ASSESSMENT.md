# Screen 04: Movement Assessment

**Version:** 1.0  
**Date:** December 26, 2025  
**Status:** Design Specification - Phase 0 Corrections

---

## Overview

**Purpose:** Assess athlete's physical capabilities through 5 standardized movements to determine Motor Profile (Spinner, Slingshotter, Whipper, or Titan).

**User Flow:**
1. Introduction screen explaining the 5 movements
2. For each movement (5 total):
   - State 1: Instruction (how to perform)
   - State 2: Recording (camera active, 10-15 seconds)
   - State 3: Analyzing (processing, 5-10 seconds)
   - State 4: Result (✓ complete, feedback)
3. After all 5 movements → Navigate to Motor Profile Result screen

**Duration:** ~5 minutes total (1 minute per movement)

---

## The 5 Movements

### Movement 1: Hip Rotation Test

**Purpose:** Measure hip mobility and rotational power initiation

**Setup:**
- Stand sideways to camera (left or right profile)
- 6-8 feet from camera
- Feet shoulder-width apart
- Arms crossed over chest

**Action:**
- Rotate hips 90 degrees (toward camera)
- Keep feet planted, don't twist ankles
- Return to neutral
- Repeat 5 times (left and right)

**What We Measure:**
- Hip rotation range (degrees)
- Speed of rotation (degrees/second)
- Stability (pelvis control)

**Duration:** 15 seconds (5 rotations)

---

### Movement 2: T-Spine Rotation Test

**Purpose:** Measure upper body separation and spinal mobility

**Setup:**
- Sit on chair or bench
- Face camera directly
- Hands behind head (elbows out)
- Feet flat on floor

**Action:**
- Rotate torso left as far as comfortable
- Keep hips and pelvis stable (don't rotate lower body)
- Return to center
- Rotate right
- Repeat 5 times each direction

**What We Measure:**
- T-spine rotation range (degrees)
- Hip-shoulder separation (degrees)
- Stability (ability to isolate upper body)

**Duration:** 15 seconds (5 rotations per side)

---

### Movement 3: Single-Leg Balance Test

**Purpose:** Measure stability and weight transfer readiness

**Setup:**
- Stand on back leg only (right leg for RHH, left leg for LHH)
- Camera angle: front-facing, 6 feet away
- Arms at sides or crossed

**Action:**
- Lift front leg off ground (knee bent to 90°)
- Hold balance for 10 seconds
- Try to minimize wobbling

**What We Measure:**
- Balance time (seconds without foot touching down)
- Stability (amount of wobble/sway)
- Hip control

**Duration:** 10 seconds per leg (20 seconds total)

---

### Movement 4: Squat Assessment

**Purpose:** Measure lower body strength, ankle and hip mobility

**Setup:**
- Stand facing camera, 6 feet away
- Feet shoulder-width apart
- Arms straight in front (parallel to ground)

**Action:**
- Squat down until thighs are parallel to ground
- Hold for 2 seconds
- Stand back up
- Repeat 3 times

**What We Measure:**
- Squat depth (knee angle)
- Ankle mobility (dorsiflexion)
- Hip mobility (flexion)
- Knee tracking (alignment)

**Duration:** 15 seconds (3 reps)

---

### Movement 5: Vertical Jump Test

**Purpose:** Measure explosive power and fast-twitch capacity

**Setup:**
- Stand sideways to camera (profile view)
- 6-8 feet from camera
- Arms at sides

**Action:**
- Countermovement (quick dip)
- Jump as high as possible
- Land softly
- Repeat 3 times (max effort each time)

**What We Measure:**
- Jump height (inches)
- Countermovement depth
- Ground contact time
- Power output

**Duration:** 15 seconds (3 jumps with rest)

---

## Screen States

### State 1: Instruction Screen

```
┌─────────────────────────────────────────────────────────┐
│  ← Back                MOVEMENT 1 of 5             ⋮    │
├─────────────────────────────────────────────────────────┤
│                                                          │
│                   Hip Rotation Test                      │
│                                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │                                                    │ │
│  │         [Illustration: Side view figure           │ │
│  │          rotating hips with arrows]               │ │
│  │                                                    │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
│  SETUP:                                                  │
│  • Stand sideways to camera (6 feet away)               │
│  • Feet shoulder-width apart                            │
│  • Arms crossed over chest                              │
│                                                          │
│  ACTION:                                                 │
│  • Rotate hips 90° toward camera                        │
│  • Keep feet planted                                     │
│  • Repeat 5 times (15 seconds)                          │
│                                                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │          [START RECORDING]                       │  │  ← 56px height, full-width
│  └──────────────────────────────────────────────────┘  │
│                                                          │
│  Progress: ●○○○○                                        │  ← 5 dots for 5 movements
└─────────────────────────────────────────────────────────┘
```

**Layout:**
- **Title:** 24px, bold, centered
- **Illustration:** 200px height, grayscale or light cyan tint
- **Instructions:** 16px, left-aligned, bullet list, 24px line height
- **Start Button:** 56px height, cyan bg, white text, 12px radius
- **Progress Dots:** 12px diameter, filled = complete, outline = pending

---

### State 2: Recording Screen

```
┌─────────────────────────────────────────────────────────┐
│  ✕ Cancel              HIP ROTATION TEST                │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │                                                    │ │
│  │                                                    │ │
│  │            [LIVE CAMERA FEED]                     │ │
│  │            720p, 16:9 aspect ratio                │ │
│  │                                                    │ │
│  │            [Pose overlay: skeleton dots]          │ │
│  │                                                    │ │
│  │                                                    │ │
│  │    ┌─────────────┐                                │ │
│  │    │  🔴 REC     │                                │ │  ← Recording indicator
│  │    │  00:12      │                                │ │  ← Timer countdown
│  │    └─────────────┘                                │ │
│  │                                                    │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
│  💡 Keep rotating your hips back and forth              │  ← Live coach cue
│     You've completed 3 of 5 rotations                   │
│                                                          │
│  Progress: ●○○○○  (Movement 1 of 5)                    │
└─────────────────────────────────────────────────────────┘
```

**Technical Specs:**
- **Camera:** WebRTC API, 720p resolution, 30-60 FPS
- **Pose Detection:** MediaPipe Pose Landmarker (browser-based)
- **Recording Duration:** 15 seconds (auto-stop)
- **Progress Tracking:** Count detected rotations in real-time
- **Cancel Button:** Top-left, returns to instruction state

---

### State 3: Analyzing Screen

```
┌─────────────────────────────────────────────────────────┐
│                 HIP ROTATION TEST                        │
├─────────────────────────────────────────────────────────┤
│                                                          │
│                                                          │
│                  ⚙️ Analyzing...                         │
│                                                          │
│              [Spinner animation]                         │  ← 64px spinner
│                                                          │
│          Detecting rotation range...                     │  ← 16px, gray text
│                                                          │
│                                                          │
│  Progress: ●○○○○  (Movement 1 of 5)                    │
└─────────────────────────────────────────────────────────┘
```

**Duration:** 5-10 seconds (backend processing)

**Processing Steps:**
1. Upload video frames to backend
2. Run pose detection on all frames
3. Calculate rotation angles
4. Determine range, speed, stability
5. Store results

---

### State 4: Result Screen

```
┌─────────────────────────────────────────────────────────┐
│                 HIP ROTATION TEST                        │
├─────────────────────────────────────────────────────────┤
│                                                          │
│                    ✅ Complete!                          │
│                                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │  Rotation Range: 85°                               │ │  ← Results
│  │  Speed: Good                                       │ │
│  │  Stability: Excellent                              │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
│  You completed 5 rotations in 15 seconds                │
│                                                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │          [NEXT MOVEMENT →]                       │  │  ← 56px button
│  └──────────────────────────────────────────────────┘  │
│                                                          │
│  Progress: ●○○○○  (Movement 1 of 5)                    │
└─────────────────────────────────────────────────────────┘
```

**Auto-advance:** After 3 seconds, proceed to next movement (or allow manual next)

---

## Motor Profile Determination Algorithm

After completing all 5 movements, determine Motor Profile based on results:

### Decision Tree

```
IF (hip_rotation > 80° AND vertical_jump > 24"):
  → WHIPPER (high hip mobility + explosive power)

ELSE IF (tspine_rotation > 70° AND hip_rotation < 70°):
  → SPINNER (high upper body rotation, lower hip rotation)

ELSE IF (hip_rotation > 75° AND vertical_jump > 20" AND balance_time > 8s):
  → SLINGSHOTTER (balanced rotation + good power + stability)

ELSE IF (squat_depth < 90° AND vertical_jump < 18"):
  → TITAN (strength-focused, mobility limited)

ELSE:
  → SLINGSHOTTER (default for balanced profile)
```

### Confidence Calculation

```
confidence = base_confidence + consistency_bonus + measurement_quality

WHERE:
- base_confidence = 70%
- consistency_bonus = (movements_matching_profile / 5) * 20%
  (e.g., 4 of 5 movements match = +16%)
- measurement_quality = clear_angles_detected ? +10% : 0%

RESULT: 70-100% confidence
```

**Example:**
- Hip rotation: 85° → Matches Whipper profile
- T-spine rotation: 65° → Matches Whipper profile
- Balance: 9s → Matches Slingshotter profile
- Squat: 95° (parallel) → Matches Slingshotter profile
- Vertical jump: 26" → Matches Whipper profile

**Result:** 4 of 5 match Whipper or high-mobility profiles → **WHIPPER, 86% confidence**

---

## Data Model

### Movement Assessment Session

```json
{
  "assessment_id": "assess_001",
  "player_id": "player_001",
  "date": "2025-12-25",
  "movements": [
    {
      "movement_type": "hip_rotation",
      "video_path": "/videos/assess_001_hip.mp4",
      "results": {
        "rotation_range": 85,
        "speed": "good",
        "stability": "excellent",
        "rotations_completed": 5,
        "duration": 15
      }
    },
    {
      "movement_type": "tspine_rotation",
      "video_path": "/videos/assess_001_tspine.mp4",
      "results": {
        "rotation_range": 65,
        "separation": 55,
        "stability": "good"
      }
    },
    {
      "movement_type": "balance",
      "video_path": "/videos/assess_001_balance.mp4",
      "results": {
        "balance_time_left": 9.2,
        "balance_time_right": 8.8,
        "wobble_score": 7.5
      }
    },
    {
      "movement_type": "squat",
      "video_path": "/videos/assess_001_squat.mp4",
      "results": {
        "depth_angle": 95,
        "ankle_mobility": "good",
        "knee_tracking": "excellent"
      }
    },
    {
      "movement_type": "vertical_jump",
      "video_path": "/videos/assess_001_jump.mp4",
      "results": {
        "jump_height": 26,
        "power_output": "high",
        "ground_contact_time": 0.32
      }
    }
  ],
  "motor_profile_result": {
    "profile": "Whipper",
    "confidence": 0.86,
    "reasoning": "High hip rotation (85°) + explosive power (26\" jump)"
  }
}
```

---

## API Endpoints

### Start Assessment
```
POST /api/motor-profile/assessments
Body: { "player_id": "player_001" }
Response: { "assessment_id": "assess_001" }
```

### Upload Movement Video
```
POST /api/motor-profile/assessments/{assessment_id}/movements
Body: {
  "movement_type": "hip_rotation",
  "video": <file>
}
Response: {
  "movement_id": "mov_001",
  "status": "analyzing",
  "estimated_time": 8
}
```

### Get Movement Result
```
GET /api/motor-profile/assessments/{assessment_id}/movements/{movement_id}
Response: {
  "movement_type": "hip_rotation",
  "status": "complete",
  "results": {
    "rotation_range": 85,
    "speed": "good",
    "stability": "excellent"
  }
}
```

### Get Final Profile
```
GET /api/motor-profile/assessments/{assessment_id}/result
Response: {
  "motor_profile": "Whipper",
  "confidence": 0.86,
  "characteristics": [...],
  "example_athletes": [...]
}
```

---

## Accessibility

- Camera permission prompt with clear explanation
- Alternative text-based assessment if camera denied (manual input)
- Keyboard navigation (Space to start/stop recording, Enter to advance)
- Screen reader announcements for each state change
- High contrast mode support
- Pause/resume capability for accessibility needs

---

## Error Handling

**Scenarios:**
1. **Camera permission denied** → Show modal: "We need camera access to assess your movements. Please enable in Settings."
2. **Poor lighting** → Show warning: "Lighting is too dim. Move to a brighter area."
3. **Body not in frame** → Show warning: "Step back 2 feet. We can't see your full body."
4. **Movement not detected** → Allow retry: "We couldn't detect rotation. Try again or skip this movement."
5. **Upload fails** → Show error: "Upload failed. Check your connection and retry."

---

## Performance Considerations

- **Video compression:** 720p H.264, target 2-5 MB per 15-second clip
- **Browser caching:** Cache pose detection model (9 MB) on first load
- **Progressive upload:** Upload video chunks during analysis phase
- **Offline mode:** Allow recording all 5 movements, queue uploads for later

---

## ✅ VALIDATION CHECKLIST

- [x] 5 movements defined with clear instructions
- [x] 4 states per movement (Instruction/Recording/Analyzing/Result)
- [x] Motor Profile determination algorithm (4 profiles)
- [x] Confidence calculation (70-100%)
- [x] Complete data model with JSON examples
- [x] API endpoints documented
- [x] Error handling scenarios
- [x] Accessibility considerations
- [x] Performance optimizations

---

**STATUS**: ✅ COMPLETE - Ready for Phase 1 implementation
