# UPLOAD REQUIREMENTS SPECIFICATION

## Minimum Swings Per Session

| Swings | Assessment |
|--------|------------|
| **1** | ❌ Single swing could be an outlier — bad cut, off-balance, etc. |
| **2** | ❌ Still not enough to see patterns |
| **3-5** | ✅ **MINIMUM** — Enough to aggregate, filter outliers, see real patterns |
| **5-10** | ✅ **IDEAL** for full $299 assessment |

**Rule:** Minimum 3 swings to generate a Lab Report. Recommend 5.

---

## Frame Rate Detection (Critical)

The 300 FPS bug proved this is critical.

### The App MUST:

1. **DETECT** frame rate from video metadata (not assume 30fps)
2. **DISPLAY** detected FPS to user for confirmation
3. **NORMALIZE** all calculations to milliseconds, not frames
4. **WARN** if FPS seems wrong (e.g., video says 30fps but duration math suggests otherwise)

### Frame Rate Guide for Users:

```
30-60 fps   → Basic analysis (Tempo, Ground, Engine)
120 fps     → Good analysis (all metrics)
240+ fps    → Best analysis (full Weapon precision)

Most iPhone slow-mo is 120 or 240fps — that's perfect.
```

---

## Upload Flow (Revised)

### STEP 1: Upload Videos (3-5 required)

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│   Upload Your Swings                                    │
│   ─────────────────                                     │
│   Add 3-5 swings from the same session.                 │
│   More swings = more accurate results.                  │
│                                                         │
│   ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐      │
│   │  ✓ #1  │ │  ✓ #2  │ │  ✓ #3  │ │  + Add  │      │
│   │ 120fps │ │ 120fps │ │ 120fps │ │  More   │      │
│   └─────────┘ └─────────┘ └─────────┘ └─────────┘      │
│                                                         │
│   ⚠️ All videos should be from the same session         │
│                                                         │
│   [Continue →]  (disabled until 3+ uploaded)            │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### STEP 2: Confirm Frame Rates

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│   Confirm Video Settings                                │
│   ──────────────────────                                │
│   We detected these frame rates. Please confirm:        │
│                                                         │
│   Video 1:  [120 fps ▼]  ✓ Detected automatically       │
│   Video 2:  [120 fps ▼]  ✓ Detected automatically       │
│   Video 3:  [120 fps ▼]  ✓ Detected automatically       │
│                                                         │
│   ℹ️ Higher frame rates (120-240fps) give more          │
│      accurate Weapon scores.                            │
│                                                         │
│   [← Back]                    [Analyze My Swings →]     │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## Video Requirements (Show to User)

```
VIDEO REQUIREMENTS
──────────────────

✓ 3-5 swings minimum (5+ recommended)
✓ Same session (don't mix old and new)
✓ Side angle (perpendicular to plate)
✓ Full body visible (head to feet)
✓ Stable camera (tripod or steady hand)

FRAME RATE GUIDE
────────────────
30-60 fps   → Basic analysis (Tempo, Ground, Engine)
120 fps     → Good analysis (all metrics)
240+ fps    → Best analysis (full Weapon precision)

Most iPhone slow-mo is 120 or 240fps — that's perfect.
```

---

## Backend Data Models

### TypeScript Interface Example:

```typescript
interface SwingUpload {
  video_url: string;
  detected_fps: number;
  confirmed_fps: number;  // User can override if detection is wrong
  duration_ms: number;
  upload_order: number;   // 1, 2, 3, 4, 5
}

interface Session {
  id: string;
  user_id: string;
  swings: SwingUpload[];  // Minimum 3, max 10
  status: 'uploading' | 'ready' | 'analyzing' | 'complete';
  created_at: Date;
}
```

### Validation Logic:

```typescript
function validateSession(session: Session): { valid: boolean; error?: string } {
  if (session.swings.length < 3) {
    return { 
      valid: false, 
      error: 'Minimum 3 swings required. Please upload more videos.' 
    };
  }
  
  if (session.swings.length > 10) {
    return { 
      valid: false, 
      error: 'Maximum 10 swings per session. Please create a new session.' 
    };
  }
  
  // Check for mixed frame rates (warning, not error)
  const fps_values = session.swings.map(s => s.confirmed_fps);
  const unique_fps = [...new Set(fps_values)];
  if (unique_fps.length > 1) {
    console.warn('Mixed frame rates detected — results may vary');
  }
  
  return { valid: true };
}
```

---

## Aggregation Logic

After analyzing all swings, aggregate for the Lab Report:

```typescript
interface SwingAnalysis {
  tempo_ratio: number;
  ground_score: number;
  engine_score: number;
  weapon_score: number;
  transfer_ratio: number;
  motor_profile: string;
  confidence: number;
}

function aggregateSession(swings: SwingAnalysis[]): SessionReport {
  // Remove outliers (optional: swings where scores deviate >20% from median)
  const filtered = removeOutliers(swings);
  
  // Average the scores
  const avg = {
    tempo_ratio: average(filtered.map(s => s.tempo_ratio)),
    ground_score: Math.round(average(filtered.map(s => s.ground_score))),
    engine_score: Math.round(average(filtered.map(s => s.engine_score))),
    weapon_score: Math.round(average(filtered.map(s => s.weapon_score))),
    transfer_ratio: Math.round(average(filtered.map(s => s.transfer_ratio))),
  };
  
  // Motor Profile = most common across swings
  const profiles = filtered.map(s => s.motor_profile);
  const motor_profile = mode(profiles);
  
  // Confidence = how consistent were the swings?
  const confidence = calculateConsistency(filtered);
  
  return {
    ...avg,
    motor_profile,
    confidence,
    swing_count: filtered.length,
    outliers_removed: swings.length - filtered.length,
  };
}

function removeOutliers(swings: SwingAnalysis[]): SwingAnalysis[] {
  // Calculate median for each metric
  const medians = {
    tempo: median(swings.map(s => s.tempo_ratio)),
    ground: median(swings.map(s => s.ground_score)),
    engine: median(swings.map(s => s.engine_score)),
    weapon: median(swings.map(s => s.weapon_score)),
  };
  
  // Filter out swings that deviate >20% from median on multiple metrics
  return swings.filter(swing => {
    const deviations = [
      Math.abs(swing.tempo_ratio - medians.tempo) / medians.tempo,
      Math.abs(swing.ground_score - medians.ground) / medians.ground,
      Math.abs(swing.engine_score - medians.engine) / medians.engine,
      Math.abs(swing.weapon_score - medians.weapon) / medians.weapon,
    ];
    
    // Keep swing if <2 metrics deviate by >20%
    const outlier_count = deviations.filter(d => d > 0.20).length;
    return outlier_count < 2;
  });
}
```

---

## Developer Instructions Summary

### UPLOAD REQUIREMENTS:

1. **MINIMUM 3 SWINGS per session**
   - Don't generate Lab Report with fewer
   - Recommend 5 for $299 assessment
   - Max 10 per session

2. **FRAME RATE DETECTION**
   - Auto-detect FPS from video metadata
   - Show user what was detected
   - Let user override if wrong
   - ALL time calculations use milliseconds, not frames

3. **VALIDATION**
   - Block "Analyze" button until 3+ swings uploaded
   - Warn (don't block) if mixed frame rates
   - Warn if FPS < 60 (lower Weapon accuracy)

4. **AGGREGATION**
   - Average scores across all swings
   - Motor Profile = most common result
   - Remove outliers (>20% deviation from median)
   - Report shows aggregated results, not individual swings

5. **UI FLOW**
   - Step 1: Upload 3-5 videos
   - Step 2: Confirm frame rates
   - Step 3: Analyze
   - Step 4: Show Lab Report

---

## Python Implementation Example:

```python
from dataclasses import dataclass
from typing import List, Optional
import statistics

@dataclass
class SwingAnalysis:
    tempo_ratio: float
    ground_score: int
    engine_score: int
    weapon_score: int
    transfer_ratio: float
    motor_profile: str
    confidence: float

@dataclass
class SessionReport:
    tempo_ratio: float
    ground_score: int
    engine_score: int
    weapon_score: int
    transfer_ratio: float
    motor_profile: str
    confidence: float
    swing_count: int
    outliers_removed: int

def aggregate_session(swings: List[SwingAnalysis]) -> SessionReport:
    """Aggregate multiple swing analyses into session report"""
    
    # Validation
    if len(swings) < 3:
        raise ValueError("Minimum 3 swings required")
    
    # Remove outliers
    filtered = remove_outliers(swings)
    
    # Calculate averages
    tempo_ratio = statistics.mean([s.tempo_ratio for s in filtered])
    ground_score = round(statistics.mean([s.ground_score for s in filtered]))
    engine_score = round(statistics.mean([s.engine_score for s in filtered]))
    weapon_score = round(statistics.mean([s.weapon_score for s in filtered]))
    transfer_ratio = statistics.mean([s.transfer_ratio for s in filtered])
    
    # Motor Profile = most common
    profiles = [s.motor_profile for s in filtered]
    motor_profile = max(set(profiles), key=profiles.count)
    
    # Confidence = consistency
    confidence = calculate_consistency(filtered)
    
    return SessionReport(
        tempo_ratio=tempo_ratio,
        ground_score=ground_score,
        engine_score=engine_score,
        weapon_score=weapon_score,
        transfer_ratio=transfer_ratio,
        motor_profile=motor_profile,
        confidence=confidence,
        swing_count=len(filtered),
        outliers_removed=len(swings) - len(filtered)
    )

def remove_outliers(swings: List[SwingAnalysis]) -> List[SwingAnalysis]:
    """Remove swings that deviate >20% from median on multiple metrics"""
    
    if len(swings) <= 3:
        return swings  # Don't remove outliers if we only have 3 swings
    
    medians = {
        'tempo': statistics.median([s.tempo_ratio for s in swings]),
        'ground': statistics.median([s.ground_score for s in swings]),
        'engine': statistics.median([s.engine_score for s in swings]),
        'weapon': statistics.median([s.weapon_score for s in swings]),
    }
    
    filtered = []
    for swing in swings:
        deviations = [
            abs(swing.tempo_ratio - medians['tempo']) / medians['tempo'],
            abs(swing.ground_score - medians['ground']) / medians['ground'],
            abs(swing.engine_score - medians['engine']) / medians['engine'],
            abs(swing.weapon_score - medians['weapon']) / medians['weapon'],
        ]
        
        outlier_count = sum(1 for d in deviations if d > 0.20)
        if outlier_count < 2:
            filtered.append(swing)
    
    return filtered if filtered else swings  # Return all if all are outliers

def calculate_consistency(swings: List[SwingAnalysis]) -> float:
    """Calculate consistency score (0-100) based on standard deviation"""
    
    if len(swings) < 2:
        return 100.0
    
    # Calculate coefficient of variation for each metric
    cvs = []
    for attr in ['tempo_ratio', 'ground_score', 'engine_score', 'weapon_score']:
        values = [getattr(s, attr) for s in swings]
        mean_val = statistics.mean(values)
        if mean_val > 0:
            stdev = statistics.stdev(values)
            cv = stdev / mean_val
            cvs.append(cv)
    
    # Average CV, convert to consistency score (lower CV = higher consistency)
    avg_cv = statistics.mean(cvs)
    consistency = max(0, 100 * (1 - avg_cv))
    
    return round(consistency, 1)
```

---

## UI Messages

### Upload Screen:

```
"Upload 3-5 swings from the same session. More swings = more accurate results."

"⚠️ Need at least 3 swings to generate your Lab Report"

"✓ Video 1 uploaded (120 fps detected)"
"✓ Video 2 uploaded (120 fps detected)"
"✓ Video 3 uploaded (120 fps detected)"
"Ready to analyze! (or add 2 more for best results)"
```

### Validation Errors:

```
"Please upload at least 3 videos before analyzing"

"Maximum 10 swings per session. Start a new session for additional analysis."

"⚠️ Warning: Mixed frame rates detected (30 fps, 120 fps). Results may vary."

"⚠️ Warning: Video quality is below 60 fps. Weapon scores may be less accurate."
```

---

## Testing Checklist

- [ ] Can upload 1 video (button disabled)
- [ ] Can upload 2 videos (button disabled)
- [ ] Can upload 3 videos (button enabled)
- [ ] Can upload up to 10 videos
- [ ] Cannot upload 11th video
- [ ] Frame rate auto-detected correctly for each video
- [ ] User can override detected frame rate
- [ ] Mixed frame rates trigger warning
- [ ] Low frame rate (<60fps) triggers warning
- [ ] Aggregation averages scores correctly
- [ ] Outlier removal works (test with 1 bad swing)
- [ ] Motor Profile shows most common result
- [ ] Confidence score reflects consistency

---

This spec ensures consistent, accurate analysis across multiple swings while preventing single-swing outliers from skewing results.
