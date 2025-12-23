# 🔴 CRITICAL BUGS IDENTIFIED

## Test Results: FAILED

### Video: Shohei Ohtani (340109.mp4) - 300 FPS, 11.27 seconds

| Metric | Expected | Actual | Status |
|--------|----------|--------|--------|
| Tempo Ratio | 2.0-3.5 | **0.05** | ❌ FAIL |
| Ground Score | 75-95 | **100** | ❌ FAIL |
| Engine Score | 75-95 | **100** | ❌ FAIL |
| Weapon Score | 80-95 | **32** | ❌ FAIL |
| Transfer Ratio | 75-95% | **0.32** | ❌ FAIL |
| Bat Speed | 70-85 mph | **21.6 mph** | ❌ FAIL |
| Motor Profile | Whipper/Slingshotter | **"Hybrid"** | ❌ FAIL |

---

## Root Cause Analysis:

### Problem 1: Contact Detection Broken
```
load_start_ms: 2766.7
contact_ms: 8300          ← 5.5 SECONDS later?!
swing_duration: 5283ms    ← A swing takes ~150ms, not 5000ms
```

**Why it's wrong:** The video is 11.27 seconds and likely contains:
- Setup/waiting (0-2s)
- **Swing 1 (2-3s)** ← The actual swing
- Reset/waiting (3-7s)
- Possibly Swing 2 or movement (7-9s) ← System detected this as "contact"
- Follow through (9-11s)

**The system is detecting a frame 5+ seconds after the swing as "contact".**

### Problem 2: Scores Hardcoded/Broken
- Ground = 100, Engine = 100 → Nobody gets perfect 100
- Weapon = 32 for elite pro at 300 FPS → Should be 80-95
- Bat speed = 21.6 mph → Should be 70-85 mph

### Problem 3: Motor Profile Still Wrong
- Shows "Hybrid" instead of valid profiles
- Classification logic didn't update properly

### Problem 4: Kinetic Sequence Impossible
```
Pelvis peak: 2766ms
Torso peak: 8250ms  ← 5.5 seconds later?!
```

Should be 20-40ms gap, not 5500ms.

---

## Required Fixes:

### FIX 1: Detect Swing Window First
Before detecting events, find the actual swing:

```python
def detect_swing_window(velocities):
    """
    Find the window where the swing actually happens
    Look for sustained high velocity period
    """
    # Find frames with high combined velocity
    combined_vels = []
    for v in velocities:
        combined = abs(v.pelvis_velocity) + abs(v.torso_velocity) + v.hand_velocity
        combined_vels.append(combined)
    
    # Smooth the signal
    window_size = 10
    smoothed = moving_average(combined_vels, window_size)
    
    # Find the peak and work backwards/forwards
    peak_idx = np.argmax(smoothed)
    
    # Swing window is typically 1 second centered on peak
    start_idx = max(0, peak_idx - 15)  # ~0.5s before peak at 30fps
    end_idx = min(len(velocities), peak_idx + 15)  # ~0.5s after peak
    
    return start_idx, end_idx, velocities[peak_idx].timestamp_ms
```

### FIX 2: Detect Contact via Peak Bat Velocity
```python
def detect_contact_correct(velocities, swing_window_start, swing_window_end):
    """
    Contact = peak bat velocity WITHIN the swing window
    """
    swing_vels = velocities[swing_window_start:swing_window_end]
    
    bat_vels = [v.bat_velocity for v in swing_vels]
    contact_idx = np.argmax(bat_vels)
    
    return swing_vels[contact_idx].timestamp_ms
```

### FIX 3: Remove Score Caps/Hardcoding
The 100 scores suggest the scoring is using max() somewhere wrong:

```python
# WRONG:
score = min(100, max(0, score))  # If score > 100, caps at 100

# RIGHT:
# Recalibrate reference values so pros score 80-95, not 100+
```

### FIX 4: Fix Motor Profile Classification
The motor profile is still returning "Hybrid" - the code didn't update properly.

---

## Reboot Motion Backend Status:

**IMPORTANT FINDING:** 
```json
{
  "data_points": [],
  "total_points": 0
}
```

The Reboot Motion backend has **NO biomechanics data**. We're only syncing player metadata (name, height, weight, session dates).

**This confirms we MUST build our own physics engine from video.**

---

## Immediate Action Items:

1. **FIX event detection** - Detect swing window first
2. **FIX contact detection** - Use peak bat velocity in swing window
3. **FIX scoring** - Recalibrate references so pros score 80-95
4. **FIX motor profile** - Actually use new classification
5. **TEST** - Verify tempo ratio is 2.0-3.5 for Shohei

---

## Expected After Fix:

### Shohei Ohtani (300 FPS):
```json
{
  "tempo_ratio": 2.8,              // ← Fixed (was 0.05)
  "ground_score": 85,               // ← Fixed (was 100)
  "engine_score": 88,               // ← Fixed (was 100)
  "weapon_score": 87,               // ← Fixed (was 32)
  "transfer_ratio": 82,             // ← Fixed (was 0.32)
  "bat_speed_mph": 76.3,            // ← Fixed (was 21.6)
  "motor_profile": "Whipper",       // ← Fixed (was "Hybrid")
  "motor_profile_confidence": 78
}
```

---

**DO NOT PROCEED until these fixes are implemented and tested.**
