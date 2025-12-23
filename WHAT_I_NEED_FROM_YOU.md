# WHAT I NEED FROM YOU TO START

**Date**: 2025-12-22  
**Purpose**: Start physics engine development and test on your videos

---

## 1. YOUR PROFILE DATA (REQUIRED)

To test the physics engine on your 5 videos, I need:

### Minimum (Required)
```
Height:   ___ inches (or ___ cm)
Weight:   ___ lbs    (or ___ kg)
Bat Side: Right / Left
```

**This gives ~85% accuracy** and is enough to start development.

---

### Standard (Optional - Recommended)
If you want to test Tier 2 accuracy (~92%):

```
Age:        ___ years
Wingspan:   ___ inches (fingertip to fingertip in T-pose)
Bat Length: ___ inches
Bat Weight: ___ oz
```

**Why wingspan matters**: Two players with same height but different wingspans will have different arm lengths → different Motor Profile classifications (SPINNER vs WHIPPER).

---

## 2. CHOOSE YOUR TIMELINE

### Option A: Conservative (12 Weeks)
- Weeks 1-2: Physics Engine (validate on 8 videos)
- Week 3: Backend Integration
- Week 4: Lab Report Generation
- Week 5: Simple Upload Interface
- Weeks 6-8: Full Player Portal
- Weeks 9-12: Beta Testing + Launch

**Revenue**: Starts Week 12  
**Risk**: Low (fully validated product)

---

### Option B: Aggressive (8 Weeks)
- Weeks 1-2: Physics Engine + Manual Beta (you run script, $99/customer)
- Weeks 3-4: Backend Integration
- Week 5: Simple Upload ($199 early adopter price)
- Weeks 6-8: Full Portal ($299 full price)

**Revenue**: Starts Week 2 (manual processing)  
**Risk**: Medium (you handle manual workflow initially)

---

### Option C: Validation First (2 Weeks)
- Weeks 1-2: Physics Engine only
- Test on all 8 videos
- Validate against your methodology
- THEN decide Option A or B

**Revenue**: TBD  
**Risk**: Low (prove physics works before committing)

**My Recommendation**: Option C → then Option B

---

## 3. LAB REPORT CONTENT SPEC

I need to know how you write about each score. For example:

### Tempo Ratio
**Score**: 2.8 (IDEAL)

**How do you explain this to a 16-year-old player?**
- What language do you use?
- What's the tone? (Technical? Conversational? Motivational?)
- What recommendations do you give?

### Motor Profile
**Classification**: WHIPPER

**How do you describe this?**
- What are the strengths of a WHIPPER?
- What should they focus on?
- Who are good pro examples?

### Pro Comparison
**Match**: Mookie Betts (89% similarity)

**How do you frame this?**
- What does the percentage mean?
- How do you avoid false expectations?
- What's the messaging?

**If you have an existing Lab Report spec or template, share it. If not, I can draft one for your review.**

---

## 4. VALIDATION CRITERIA

What does "working" mean to you?

### Current Proposed Criteria
Before declaring physics engine valid:

**Technical**:
1. Tempo Ratio: 1.5:1 to 4.0:1 for all videos
2. Frame Rate Independence: 300 FPS and 30 FPS produce comparable scores (±10%)
3. Consistency: <15% variation across multiple swings from same player
4. Event Detection: Within ±50ms of manual review
5. Motor Profile: 80%+ match with your manual assessment

**Output**:
6. Lab Report metrics are defensible (align with biomechanics research)
7. Language sounds like Coach Rick
8. Recommendations are actionable

**Do these criteria make sense to you? Any additions/changes?**

---

## PROVIDE THIS TO START

**Minimum to start development**:
```
Height: ___
Weight: ___
Bat Side: ___

Timeline: Option ___ (A, B, or C)
```

**Optional (improves testing)**:
```
Age: ___
Wingspan: ___
Bat Length: ___
Bat Weight: ___

Lab Report: [share spec or say "draft one for me"]
Validation: [approve criteria or suggest changes]
```

---

## WHAT HAPPENS NEXT

Once you provide:

### Week 1 (Days 1-3): Video Processing
- Install dependencies (MediaPipe, OpenCV, NumPy, SciPy)
- Build video frame extractor
- Build pose detector (MediaPipe 33 joints/frame)
- Fix frame rate normalization bug (milliseconds, not frame counts)
- Test on your first video (131215-Hitting.mov)

### Week 1 (Days 4-5): Physics Calculations
- Implement de Leva anthropometric scaling
- Calculate angular momentum (L = I × ω)
- Calculate moment of inertia (I = m × (k × L)²)
- Test on 3 videos (yours + Shohei)

### Week 2 (Days 1-3): Event Detection
- First Movement (hip rotation threshold)
- Foot Plant (front foot velocity → 0)
- Contact (peak bat velocity)
- Validate timing against manual review

### Week 2 (Days 4-5): Scoring Algorithms
- Brain: Tempo Ratio
- Body: Ground Flow, Engine Flow, Weapon Flow (FPS-adjusted)
- Bat: Transfer Ratio
- Motor Profile classification
- Pro Comparison matching
- Test on all 8 videos

### End of Week 2: Validation
- JSON reports for all 8 videos
- Side-by-side comparison (your swings vs Shohei)
- Review with you: Do scores make sense?
- THEN decide next phase

---

## EXAMPLE OUTPUT (After Week 2)

You'll get JSON reports like this:

### Your Video (131215-Hitting.mov, 30 FPS)
```json
{
  "athlete": {
    "height_inches": 72,
    "weight_lbs": 180,
    "bat_side": "right"
  },
  "video": {
    "filename": "131215-Hitting.mov",
    "fps": 30,
    "duration_sec": 16.4
  },
  "brain": {
    "tempo_ratio": 2.6,
    "tempo_category": "IDEAL",
    "load_duration_ms": 867,
    "launch_duration_ms": 600
  },
  "body": {
    "ground_flow": 82,
    "engine_flow": 88,
    "weapon_flow": 76,
    "weapon_flow_note": "Capped at 85 due to 30 FPS"
  },
  "bat": {
    "transfer_ratio": 1.08,
    "transfer_category": "STRONG"
  },
  "motor_profile": "WHIPPER",
  "pro_comparison": "Mookie Betts (89%)",
  "events": {
    "first_movement": {"frame": 12, "time_ms": 400},
    "foot_plant": {"frame": 38, "time_ms": 1267},
    "contact": {"frame": 56, "time_ms": 1867}
  }
}
```

### Shohei Video (340109 (1).mp4, 300 FPS)
```json
{
  "athlete": {
    "height_inches": 76,
    "weight_lbs": 210,
    "bat_side": "left"
  },
  "video": {
    "filename": "340109 (1).mp4",
    "fps": 300,
    "duration_sec": 11.3
  },
  "brain": {
    "tempo_ratio": 2.9,
    "tempo_category": "IDEAL"
  },
  "body": {
    "ground_flow": 94,
    "engine_flow": 96,
    "weapon_flow": 92,
    "weapon_flow_note": "Full precision (300 FPS)"
  },
  "bat": {
    "transfer_ratio": 1.23,
    "transfer_category": "ELITE"
  },
  "motor_profile": "WHIPPER + TITAN",
  "pro_comparison": "Aaron Judge (96%)"
}
```

**Then we review together**: Do these scores align with what you see in the videos?

---

## SUPPORTING DOCUMENTS

**Read these for full context**:
1. `READ_ME_FIRST.md` — Master index
2. `CORRECTED_EXECUTIVE_SUMMARY.md` — Complete overview
3. `ANTHROPOMETRIC_DATA_SPEC.md` — Measurement guide (3 tiers)
4. `CORRECTIONS_SUMMARY.md` — What changed from original docs

**All files in**: `/home/user/webapp/`

---

## READY TO START?

**Just provide**:
1. Your profile data (height, weight, bat side minimum)
2. Choose timeline (A, B, or C)
3. Lab Report guidance (share spec or ask me to draft)

**I'll begin immediately and have test results in 2 weeks.**

---

**Last Updated**: 2025-12-22
