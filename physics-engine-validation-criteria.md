# PHYSICS ENGINE VALIDATION — TEST CRITERIA

## Overview

Before declaring the physics engine "working," it must pass these validation tests. Use your test videos to verify each metric produces sensible results.

---

## TEST VIDEOS

| Video | Type | FPS | Expected Profile | Expected Level |
|-------|------|-----|------------------|----------------|
| 340109 (1).mp4 | Shohei Ohtani | 300 | Whipper or Slingshotter | Elite (80+ scores) |
| 340109 (2).mp4 | Shohei Ohtani | 300 | Whipper or Slingshotter | Elite (80+ scores) |
| 340109 (3).mp4 | Shohei Ohtani | 300 | Whipper or Slingshotter | Elite (80+ scores) |
| Your videos | Your swings | 30 | Unknown (discover) | Good (60-80 scores) |

---

## TEST 1: Event Detection

### What to Check

The system must correctly identify three key moments:

| Event | What It Is | How to Verify |
|-------|------------|---------------|
| **First Movement** | Start of weight shift / leg lift | Should be early in swing (100-500ms from video start if swing is centered) |
| **Foot Plant** | Front foot lands | Should be 200-400ms AFTER first movement |
| **Contact** | Bat meets ball (or peak bat speed) | Should be 100-200ms AFTER foot plant |

### Required Output

```json
{
  "events": {
    "first_movement_ms": 1250,
    "foot_plant_ms": 1580,
    "contact_ms": 1720,
    "load_duration_ms": 330,
    "launch_duration_ms": 140
  }
}
```

### Validation Criteria

| Check | Pass | Fail |
|-------|------|------|
| First movement detected | Value exists, > 0 | Null, 0, or negative |
| Foot plant after first movement | foot_plant > first_movement | foot_plant ≤ first_movement |
| Contact after foot plant | contact > foot_plant | contact ≤ foot_plant |
| Load duration realistic | 200-600ms | < 100ms or > 1000ms |
| Launch duration realistic | 100-250ms | < 50ms or > 400ms |
| Events are frame-rate normalized | Values in ms, not frames | Values suspiciously match frame numbers |

### Red Flags 🚩

- Load duration < 100ms → Events detected wrong
- Launch duration < 50ms → Contact detected too early
- Launch duration > 400ms → Contact detected too late (in follow-through)
- All events at 0ms → Event detection not running
- Events not in sequence → Logic error

---

## TEST 2: Tempo Ratio

### What to Check

```
Tempo Ratio = Load Duration / Launch Duration
```

### Expected Ranges

| Ratio | Category | Interpretation |
|-------|----------|----------------|
| < 1.5 | 🔴 RUSHED | Impossible or detection error |
| 1.5 - 1.99 | 🟡 RUSHED | Firing before fully loaded |
| 2.0 - 2.49 | 🟢 FAST | Contact-oriented, quick trigger |
| 2.5 - 3.0 | 🟢 IDEAL | Maximum power zone |
| 3.01 - 3.5 | 🟢 SLOW | Long load, may struggle with velo |
| 3.5 - 4.0 | 🟡 TOO SLOW | Timing issues likely |
| > 4.0 | 🔴 TOO SLOW | Detection error likely |

### Validation Criteria

| Check | Pass | Fail |
|-------|------|------|
| Shohei video tempo | 2.0 - 3.5 | < 1.5 or > 4.0 |
| Your videos tempo | 1.8 - 4.0 | < 1.0 or > 5.0 |
| Consistent across swings | Within ±0.5 for same player | Varies by > 1.0 between swings |
| Math is correct | load_ms / launch_ms = tempo | Values don't match |

### Red Flags 🚩

- Tempo < 1.0 → Load/launch inverted or events wrong
- Tempo = exactly 1.0 → Hardcoded or not calculating
- Tempo > 5.0 → Contact detected in follow-through
- Tempo = NaN or Infinity → Division error

---

## TEST 3: Ground Score

### What It Measures

- Weight transfer (COM movement from back to front)
- Leg drive (back knee extension velocity)
- Ground reaction (vertical COM acceleration)

### Expected Ranges

| Player Type | Expected Ground Score |
|-------------|----------------------|
| Elite pro (Shohei) | 80-95 |
| Good amateur | 65-80 |
| Average youth | 50-70 |
| Poor mechanics | 30-50 |

### Validation Criteria

| Check | Pass | Fail |
|-------|------|------|
| Score range | 0-100 | Negative, > 100, or null |
| Shohei score | 75-95 | < 60 (too low for pro) |
| Your score | 50-85 | < 30 or > 95 |
| Different from Engine/Weapon | Varies by player | All three scores identical |

### Red Flags 🚩

- Score = 0 → Calculation not running
- Score = 100 → Hardcoded or no ceiling
- Score = exactly 50 → Default/placeholder value
- All videos same score → Not actually calculating

---

## TEST 4: Engine Score

### What It Measures

- Hip rotation speed (peak pelvis angular velocity)
- Hip-shoulder separation (max separation angle)
- Sequence timing (pelvis peaks before torso)

### Expected Ranges

| Player Type | Expected Engine Score |
|-------------|----------------------|
| Elite pro (Shohei) | 80-95 |
| Good rotational hitter | 70-85 |
| Linear hitter | 55-70 |
| Poor rotation | 40-55 |

### Validation Criteria

| Check | Pass | Fail |
|-------|------|------|
| Score range | 0-100 | Negative, > 100, or null |
| Shohei score | 75-95 | < 65 (too low for pro) |
| Your score | 50-90 | < 30 or > 95 |
| Correlates with rotation style | Spinners score higher | No correlation to movement |

### Red Flags 🚩

- Score = 0 → Hip tracking failed
- Engine > Ground by 30+ → Possible, but verify
- Engine = Weapon = Ground → Not differentiating segments

---

## TEST 5: Weapon Score

### What It Measures

- Bat speed (peak angular velocity)
- Hand path efficiency (directness of path)
- Bat lag (hands trail hips properly)

### Expected Ranges

| Player Type | Expected Weapon Score |
|-------------|----------------------|
| Elite pro (Shohei) | 80-95 |
| Power hitter | 75-90 |
| Contact hitter | 60-75 |
| Youth / developing | 45-65 |

### Frame Rate Impact

| FPS | Weapon Score Cap | Why |
|-----|------------------|-----|
| 30 | 85 max | Can't capture fast bat movement |
| 60 | 90 max | Better, still limited |
| 120+ | 100 | Full precision |
| 300 | 100 | Ideal |

### Validation Criteria

| Check | Pass | Fail |
|-------|------|------|
| Shohei (300fps) score | 80-95 | < 70 (too low for elite + high fps) |
| Your (30fps) score | Capped at 85 | > 90 at 30fps (impossible) |
| Bat speed reasonable | 60-90 mph (pro), 40-70 mph (amateur) | > 100 mph or < 30 mph |

### Red Flags 🚩

- Weapon score > 90 at 30fps → Not applying fps cap
- Bat speed > 100 mph → Calculation error (pros max ~85 mph)
- Bat speed < 30 mph → Tracking lost or wrong segment
- Weapon = 0 → Wrist/hand tracking failed

---

## TEST 6: Transfer Ratio

### What It Measures

How efficiently energy flows from ground to bat.

```
Transfer Ratio = Bat Momentum at Contact / Pelvis Peak Momentum
```

### Expected Ranges (as percentage 0-100)

| Score | Category | Meaning |
|-------|----------|---------|
| 85-100 | ELITE | Energy flows with minimal loss |
| 75-84 | STRONG | Solid transfer, minor leaks |
| 65-74 | GOOD | Room to improve |
| 55-64 | DEVELOPING | Noticeable energy loss |
| < 55 | FOCUS AREA | Significant leaks |

### Validation Criteria

| Check | Pass | Fail |
|-------|------|------|
| Score range | 0-100 (percentage) | Raw ratio like 1.12 without context |
| Shohei score | 75-95 | < 65 (energy shouldn't leak in elite) |
| Correlates with scores | High G/E/W = High transfer | No correlation |

### Red Flags 🚩

- Transfer > 100% → Calculation error (can't create energy)
- Transfer shows as ratio (1.12) not percentage → Wrong format
- Transfer = 0 → Momentum calculation failed

---

## TEST 7: Motor Profile

### What It Should Classify

| Profile | Primary Characteristic | Key Indicators |
|---------|----------------------|----------------|
| **SPINNER** | Rotation-first | High hip speed, tight axis, early pelvis fire |
| **SLINGSHOTTER** | Separation-first | High separation, late hands, linear start |
| **WHIPPER** | Arm-first | High bat speed, bat lag, arm speed > body speed |
| **TITAN** | Size modifier | Added to primary profile if weight > 200 lbs |

### Validation Criteria

| Check | Pass | Fail |
|-------|------|------|
| Uses correct names | Spinner/Slingshotter/Whipper/Titan | Rotational/Linear/Hybrid |
| Includes confidence % | 60-95% | No confidence or always 100% |
| Shohei classification | Whipper or Slingshotter | Spinner (unlikely for his style) |
| Consistent for same player | Same profile across swings | Different profile each swing |

### Red Flags 🚩

- Profile = "Rotational" → Wrong terminology
- Profile = "Hybrid" → Not a valid profile in your system
- Profile changes every swing → Classification unstable
- Confidence always 100% → Not actually calculating

---

## TEST 8: Kinetic Sequence

### What to Check

Proper sequence: **Pelvis → Torso → Arms → Bat**

Each segment should peak AFTER the previous one.

### Expected Peak Order (ms before contact)

| Segment | Elite Timing | Acceptable Range |
|---------|--------------|------------------|
| Pelvis peak | -80 to -60ms | -100 to -40ms |
| Torso peak | -60 to -40ms | -80 to -20ms |
| Arms peak | -30 to -15ms | -50 to -5ms |
| Bat peak | 0ms (contact) | -10 to +5ms |

### Validation Criteria

| Check | Pass | Fail |
|-------|------|------|
| Sequence order correct | Pelvis → Torso → Arms → Bat | Out of order |
| Gap between peaks | 20-40ms each | < 10ms or > 100ms |
| Bat peak near contact | Within 10ms of detected contact | > 50ms off |

### Red Flags 🚩

- Bat peaks before pelvis → Sequence inverted
- All segments peak at same time → Not detecting peaks
- Gaps > 100ms → Something's wrong with detection

---

## TEST 9: Consistency Check

### Run Same Video 3 Times

Upload the same video three times. Results should be identical.

| Check | Pass | Fail |
|-------|------|------|
| Tempo ratio | Identical to 0.01 | Varies by > 0.1 |
| Scores | Identical | Varies by > 2 points |
| Motor Profile | Same classification | Different each time |
| Events | Same timestamps | Different each time |

### Red Flags 🚩

- Results vary significantly → Non-deterministic bug
- Results vary slightly → Floating point issues (minor)

---

## TEST 10: Cross-Video Comparison

### Compare Shohei vs Your Swings

| Metric | Shohei (Expected) | You (Expected) | Check |
|--------|-------------------|----------------|-------|
| Ground | 80-95 | 60-80 | Shohei > You |
| Engine | 80-95 | 60-85 | Shohei > You (unless you're elite rotator) |
| Weapon | 85-95 | 55-75 | Shohei > You (he's a pro) |
| Bat Speed | 75-85 mph | 55-70 mph | Shohei > You |
| Transfer | 80-95 | 60-80 | Shohei ≥ You |

### Validation Criteria

| Check | Pass | Fail |
|-------|------|------|
| Pro scores higher than amateur | Shohei > You on most metrics | You score higher than Shohei |
| Scores differentiate skill | Clear gap between pro and amateur | Same scores for both |

### Red Flags 🚩

- Your scores higher than Shohei → Calculation error
- Identical scores → Not actually measuring anything
- Shohei scores like a youth player → Calibration wrong

---

## VALIDATION SUMMARY CHECKLIST

### Before Approving, ALL Must Pass:

```
EVENT DETECTION
[ ] First movement detected (reasonable timestamp)
[ ] Foot plant detected (after first movement)
[ ] Contact detected (after foot plant)
[ ] Load duration: 200-600ms
[ ] Launch duration: 100-250ms

TEMPO RATIO
[ ] Falls between 1.5 and 4.0
[ ] Shohei: 2.0-3.5
[ ] Math checks out (load_ms / launch_ms)

GROUND SCORE
[ ] Range 0-100
[ ] Shohei: 75-95
[ ] Varies between videos

ENGINE SCORE
[ ] Range 0-100
[ ] Shohei: 75-95
[ ] Correlates with rotation style

WEAPON SCORE
[ ] Range 0-100
[ ] Shohei (300fps): 80-95
[ ] Your videos (30fps): capped at 85
[ ] Bat speed: 50-90 mph (reasonable)

TRANSFER RATIO
[ ] Shows as percentage (0-100)
[ ] Shohei: 75-95
[ ] Correlates with other scores

MOTOR PROFILE
[ ] Uses correct names (Spinner/Slingshotter/Whipper/Titan)
[ ] Includes confidence %
[ ] Consistent for same player

KINETIC SEQUENCE
[ ] Correct order (Pelvis → Torso → Arms → Bat)
[ ] Reasonable gaps between peaks

CONSISTENCY
[ ] Same video = same results (3x test)
[ ] Pro scores > Amateur scores
```

---

## WHAT TO SEND IF TESTS FAIL

```
The physics engine failed validation:

FAILED: [specific test]
Expected: [what it should be]
Actual: [what it showed]
Video: [which video]

Please fix and retest before proceeding.
```

---

## WHAT TO SEND IF TESTS PASS

```
Physics engine validated. All tests pass:

✓ Event detection working
✓ Tempo ratio: [value] (within range)
✓ Ground/Engine/Weapon scores reasonable
✓ Transfer ratio calculating correctly
✓ Motor Profile using correct names
✓ Kinetic sequence in proper order
✓ Consistency confirmed
✓ Pro > Amateur differentiation working

Ready to proceed with Lab Report integration.
```
