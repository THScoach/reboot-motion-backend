# 🎥 YOUR VIDEO FILES — TECHNICAL ANALYSIS

**Date**: 2025-12-22  
**Location**: `/home/user/uploaded_files/`  
**Total Videos**: 8

---

## 📊 YOUR ON-FORM APP VIDEOS (5 files)

### **Video 1: 131151-Hitting.mov**
- **Resolution**: 1280×720 (720p HD)
- **Frame Rate**: 30 FPS
- **Duration**: 15.4 seconds
- **Weapon Score Cap**: 85/100 (due to 30 FPS)
- **Quality**: Good for testing, limited bat detail

### **Video 2: 131200-Hitting.mov**
- **Resolution**: 1280×720 (720p HD)
- **Frame Rate**: 30 FPS
- **Duration**: 19.2 seconds
- **Weapon Score Cap**: 85/100 (due to 30 FPS)
- **Quality**: Good for testing, limited bat detail

### **Video 3: 131215-Hitting.mov**
- **Resolution**: 1280×720 (720p HD)
- **Frame Rate**: 30 FPS
- **Duration**: 16.4 seconds
- **Weapon Score Cap**: 85/100 (due to 30 FPS)
- **Quality**: Good for testing, limited bat detail

### **Video 4: 131233-Hitting.mov**
- **Resolution**: 1280×720 (720p HD)
- **Frame Rate**: 30 FPS
- **Duration**: 19.5 seconds
- **Weapon Score Cap**: 85/100 (due to 30 FPS)
- **Quality**: Good for testing, limited bat detail

### **Video 5: 131301-Hitting.mov**
- **Resolution**: 1280×720 (720p HD)
- **Frame Rate**: 30 FPS
- **Duration**: 26.3 seconds
- **Weapon Score Cap**: 85/100 (due to 30 FPS)
- **Quality**: Good for testing, limited bat detail

---

## ⚡ SHOHEI OHTANI VIDEOS (3 files) — HIGH SPEED!

### **Video 6: 340109 (1).mp4**
- **Resolution**: 896×672
- **Frame Rate**: 300 FPS ✅ (CONFIRMED!)
- **Duration**: 11.3 seconds
- **Weapon Score Cap**: 100/100 (240+ FPS)
- **Quality**: EXCELLENT for bat speed analysis
- **Notes**: This is your GOLD STANDARD test video

### **Video 7: 340109 (2).mp4**
- **Resolution**: 896×672
- **Frame Rate**: 300 FPS ✅ (CONFIRMED!)
- **Duration**: 7.2 seconds
- **Weapon Score Cap**: 100/100 (240+ FPS)
- **Quality**: EXCELLENT for bat speed analysis

### **Video 8: 340109 (3).mp4**
- **Resolution**: 896×672
- **Frame Rate**: 300 FPS ✅ (CONFIRMED!)
- **Duration**: 10.7 seconds
- **Weapon Score Cap**: 100/100 (240+ FPS)
- **Quality**: EXCELLENT for bat speed analysis

---

## 🎯 WHAT THIS MEANS FOR YOUR PHYSICS ENGINE

### **Frame Rate Impact (From Your Spec)**

#### **30 FPS Videos (Your on-form app videos)**
```
✅ GOOD FOR:
- Tempo Ratio (accurate)
- Ground Score (accurate)
- Engine Score (accurate)
- Transfer Ratio (accurate)
- Motor Profile (accurate)
- Pro Comparison (accurate)

⚠️ LIMITED FOR:
- Weapon Score (capped at 85/100)
- Bat speed precision (±2-3 mph error)
- Hand path detail (33ms between frames)
```

**Why capped at 85/100?**  
At 30 FPS, each frame is 33 milliseconds apart. A bat moving 75+ mph travels ~3.6 feet per frame, making precise bat lag and hand path calculations difficult.

#### **300 FPS Videos (Shohei Ohtani)**
```
✅ EXCELLENT FOR EVERYTHING:
- All scores (0-100 full range)
- Bat speed (±0.3 mph precision)
- Hand path (3.3ms between frames)
- Bat lag angle (high precision)
```

**Why full range?**  
At 300 FPS, each frame is 3.3 milliseconds apart. A bat moving 75+ mph travels only ~4 inches per frame, allowing precise tracking of bat movement.

---

## 🧪 TESTING STRATEGY

### **Phase 1: Validate on 30 FPS Videos (Your swings)**
**Goal**: Prove the physics engine works on typical consumer videos

**Test Cases**:
1. 131215-Hitting.mov (16.4s) — Primary test
2. 131151-Hitting.mov (15.4s) — Secondary test
3. 131233-Hitting.mov (19.5s) — Tertiary test

**Expected Results**:
- Tempo Ratio: 2.0-3.5 range
- Ground Score: 60-90
- Engine Score: 65-85
- Weapon Score: 50-85 (capped)
- Transfer Ratio: 0.8-1.2
- Motor Profile: SPINNER / SLINGSHOTTER / WHIPPER
- Pro Comparison: 75-90% similarity

**Success Criteria**:
✅ All 7 metrics calculated
✅ Scores make intuitive sense
✅ Event detection works (First Move, Foot Plant, Contact)
✅ No crashes or errors

---

### **Phase 2: Validate on 300 FPS Videos (Shohei Ohtani)**
**Goal**: Prove the physics engine achieves full precision on high-speed video

**Test Cases**:
1. 340109 (1).mp4 (11.3s) — Primary test
2. 340109 (2).mp4 (7.2s) — Secondary test
3. 340109 (3).mp4 (10.7s) — Tertiary test

**Expected Results**:
- Tempo Ratio: 2.5-3.0 (IDEAL)
- Ground Score: 90-100 (elite)
- Engine Score: 90-100 (elite)
- Weapon Score: 85-100 (no FPS cap)
- Transfer Ratio: 1.15-1.30 (ELITE)
- Motor Profile: WHIPPER + TITAN (193cm, 95kg)
- Pro Comparison: Aaron Judge or Giancarlo Stanton (power hitters)

**Success Criteria**:
✅ Weapon Score reaches 90+ (proves FPS scaling works)
✅ Motor Profile = WHIPPER + TITAN
✅ Pro Comparison matches a power hitter
✅ Bat speed ~85-90 mph (elite MLB level)

---

## 📐 PHYSICS CALCULATIONS (YOUR SPEC)

### **Anthropometric Data Needed**

#### **For Your Videos (Coach Rick)**
Please provide:
- **Height**: ___ cm (or ___ inches)
- **Weight**: ___ kg (or ___ lbs)
- **Bat Side**: Right or Left

#### **For Shohei Ohtani Videos**
Known data:
- **Height**: 193 cm (6'4")
- **Weight**: 95 kg (210 lbs)
- **Bat Side**: Left
- **Professional**: Yes (use for "TITAN" modifier)

---

## 🎨 VISUALIZATION PLAN (FUTURE)

### **Video Output Options**

#### **Option A: Side-by-Side Overlay**
```
┌─────────────────┬─────────────────┐
│  Original Video │  Skeleton View  │
│                 │                 │
│  [Raw footage]  │  [MediaPipe     │
│                 │   pose overlay] │
└─────────────────┴─────────────────┘
```

#### **Option B: Annotated Single View**
```
┌─────────────────────────────────────┐
│           Original Video            │
│                                     │
│  [Skeleton overlay + key metrics]  │
│                                     │
│  Tempo: 2.8  Ground: 87  Engine: 92│
└─────────────────────────────────────┘
```

#### **Option C: Graph View**
```
┌─────────────────────────────────────┐
│          Angular Momentum           │
│                                     │
│  [Real-time graph of pelvis/torso] │
│                                     │
│  ← First Move  ← Foot Plant ← Contact
└─────────────────────────────────────┘
```

---

## 💡 RECOMMENDATIONS

### **1. Start with 30 FPS Videos**
Your on-form app videos (30 FPS) are perfect for initial testing:
- ✅ Good enough for 6/7 metrics
- ✅ Typical consumer video quality
- ✅ Most customers will upload 30-60 FPS videos
- ⚠️ Only limitation: Weapon Score capped at 85

**Why this matters**: If you can make it work on 30 FPS, it'll work on anything.

### **2. Use 300 FPS Videos for Validation**
The Shohei Ohtani videos are your PROOF that the physics is accurate:
- ✅ Full precision on all metrics
- ✅ Elite-level swing to compare against
- ✅ Validates your scoring system
- ✅ Great for marketing ("Compared to MLB players!")

### **3. Accept Videos from 30-600 FPS**
Based on your spec, support this range:
```
30-59 FPS:   Weapon Score capped at 85
60-119 FPS:  Weapon Score capped at 90
120-239 FPS: Weapon Score capped at 95
240+ FPS:    Weapon Score full range (0-100)
```

**Marketing Message**:  
"Upload any video (30-600 FPS). Higher frame rates = more precise bat speed analysis."

---

## 🚀 NEXT STEPS

### **1. Provide Your Profile Data**
I need this to test your 5 videos:
- Height: ___ cm (or ___ inches)
- Weight: ___ kg (or ___ lbs)
- Bat side: Right or Left

### **2. Approve Build Plan**
Say "YES" to build the Physics Engine Proof of Concept:
- 3 days to working demo
- Test on all 8 videos
- Generate JSON reports

### **3. First Test**
I'll run the physics engine on:
1. **131215-Hitting.mov** (your swing, 30 FPS)
2. **340109 (1).mp4** (Shohei, 300 FPS)

You'll get side-by-side reports to compare:
- Your scores vs Shohei's scores
- Your motor profile vs Shohei's motor profile
- Pro player comparison for both

### **4. Validate Results**
You review the reports and tell me:
- ✅ Do the scores make sense?
- ✅ Is the motor profile accurate?
- ✅ Is the pro comparison reasonable?
- ⚠️ What needs adjustment?

---

## 📝 EXAMPLE OUTPUT (What You'll Get)

### **Report for 131215-Hitting.mov (Coach Rick)**
```json
{
  "athlete": {
    "name": "Coach Rick",
    "height_cm": 182,
    "weight_kg": 85,
    "bat_side": "right"
  },
  "video": {
    "filename": "131215-Hitting.mov",
    "fps": 30,
    "duration_sec": 16.4,
    "resolution": "1280x720"
  },
  "scores": {
    "tempo_ratio": 2.6,
    "tempo_category": "IDEAL",
    "ground_score": 82,
    "engine_score": 88,
    "weapon_score": 76,
    "weapon_score_note": "Capped at 85 due to 30 FPS",
    "transfer_ratio": 1.08,
    "transfer_category": "STRONG"
  },
  "profile": {
    "motor_profile": "WHIPPER",
    "pro_comparison": "Mookie Betts (89% similarity)",
    "reasoning": "High engine score + balanced transfer"
  },
  "events": {
    "first_movement": {"frame": 12, "time_ms": 400},
    "foot_plant": {"frame": 38, "time_ms": 1267},
    "contact": {"frame": 56, "time_ms": 1867}
  },
  "detailed_metrics": {
    "load_duration_ms": 867,
    "launch_duration_ms": 600,
    "peak_bat_speed_mph": 72.3,
    "peak_pelvis_angular_momentum": 235.8,
    "bat_momentum_at_contact": 254.7
  }
}
```

### **Report for 340109 (1).mp4 (Shohei Ohtani)**
```json
{
  "athlete": {
    "name": "Shohei Ohtani",
    "height_cm": 193,
    "weight_kg": 95,
    "bat_side": "left"
  },
  "video": {
    "filename": "340109 (1).mp4",
    "fps": 300,
    "duration_sec": 11.3,
    "resolution": "896x672"
  },
  "scores": {
    "tempo_ratio": 2.9,
    "tempo_category": "IDEAL",
    "ground_score": 94,
    "engine_score": 96,
    "weapon_score": 92,
    "weapon_score_note": "Full precision (300 FPS)",
    "transfer_ratio": 1.23,
    "transfer_category": "ELITE"
  },
  "profile": {
    "motor_profile": "WHIPPER + TITAN",
    "pro_comparison": "Aaron Judge (96% similarity)",
    "reasoning": "Elite power + size (95kg) + high transfer ratio"
  },
  "events": {
    "first_movement": {"frame": 120, "time_ms": 400},
    "foot_plant": {"frame": 380, "time_ms": 1267},
    "contact": {"frame": 560, "time_ms": 1867}
  },
  "detailed_metrics": {
    "load_duration_ms": 867,
    "launch_duration_ms": 600,
    "peak_bat_speed_mph": 88.7,
    "peak_pelvis_angular_momentum": 312.5,
    "bat_momentum_at_contact": 384.6
  }
}
```

---

## ✅ READY TO START?

**I have everything I need except:**
1. Your height/weight/bat side (for testing your videos)

**Once you provide that, I'll:**
1. Build the Physics Engine (3 days)
2. Test on all 8 videos
3. Generate JSON reports for each
4. Show you side-by-side comparison (You vs Shohei)

**Just say "GO" and provide your profile data! 🚀**

---

**Your Videos**: 8 files at `/home/user/uploaded_files/`  
**Backend**: https://reboot-motion-backend-production.up.railway.app  
**Repo**: https://github.com/THScoach/reboot-motion-backend  

**Last Updated**: 2025-12-22
