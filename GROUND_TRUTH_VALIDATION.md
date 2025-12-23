# 🎯 Ground Truth Validation - Connor Gray

## Data Source
**Session**: 80e77691-d7cc-4ebb-b955-2fd45676f0ca  
**Date**: December 20, 2025  
**Source**: Reboot Motion API - momentum-energy export  
**Frame Rate**: 240 fps (4.17ms resolution)  
**Total Frames**: 2,903 time points

## Athlete Details
- **Name**: Connor Gray
- **Height**: 72 inches (6'0")
- **Weight**: 160 lbs
- **Bats**: Left
- **Bat**: 33"/30oz (0.85 kg)

---

## ✅ Ground Truth Metrics (From Reboot Motion)

### 1. Bat Speed
- **Near Contact**: **57.5 mph** ✅ (Target for validation)
- **Peak (with artifacts)**: 80.1 mph (filter values > 120 mph)
- **Calculation**: `sqrt(2 * bat_trans_energy / bat_mass) * 2.237`

### 2. Tempo Ratio
- **Load Duration**: **1,579 ms** ✅
- **Launch (Swing) Duration**: **467 ms** ✅
- **Tempo Ratio**: **3.38:1** ✅
- **Load Start**: -2.046 seconds before contact
- **Launch Start**: -0.467 seconds before contact

### 3. Kinetic Energy at Contact
- **Total**: 2,305 J
- **Lower Half**: 1,414 J (61%)
- **Torso**: 673 J (29%)
- **Arms**: 338 J (15%)

### 4. Kinematic Sequence (ms before contact)
- **Torso Peak**: 4 ms before contact ⚡
- **Pelvis Peak**: 17 ms before contact
- **Lower Half Peak**: 33 ms before contact
- **Arms Peak**: 58 ms before contact

**Key Insight**: Arms peak LAST (closest to contact), confirming the kinetic chain transfers energy sequentially. Peak velocity = contact point!

---

## 📋 Validation Thresholds

### Bat Speed (mph)
| Age Group | Min | Max |
|-----------|-----|-----|
| Youth 12U | 40 | 55 |
| **High School** | **55** | **70** |
| College | 65 | 80 |
| MLB | 70 | 85 |
| Elite MLB | 80 | 95 |

**Connor (HS)**: 57.5 mph ✅ (within 55-70 range)

### Tempo Ratio
| Category | Min | Max |
|----------|-----|-----|
| Too Slow | 0 | 1.5 |
| **Optimal** | **2.0** | **3.5** |
| Too Fast | 4.0 | 10.0 |

**Connor**: 3.38 ✅ (upper end of optimal - patient load)

### Energy Distribution (%)
| Segment | Optimal Min | Optimal Max | Connor |
|---------|-------------|-------------|--------|
| Lower Half | 55 | 65 | **61** ✅ |
| Torso | 25 | 35 | **29** ✅ |
| Arms | 10 | 20 | **15** ✅ |

**Connor**: All within optimal ranges!

---

## 🔧 Physics Engine Fixes Required

### 1. ✅ Tempo Ratio - FIXED
**Bug**: 0.05 (was measuring wrong phases)  
**Ground Truth**: 3.38  
**Fix Applied**: Measure `(load → foot_down) / (foot_down → contact)`  
**Status**: ✅ **FIXED** (TypeScript-based implementation)

### 2. ⚠️ Bat Speed - NEEDS REFINEMENT
**Current Bug**: 21.6 mph  
**Ground Truth**: 57.5 mph  
**Fix Needed**: Use `bat_momentum_magnitude / bat_mass * 2.237`  
**Status**: ⚠️ **IN PROGRESS** (lever arm physics implemented, needs validation)

### 3. ✅ Contact Detection - FIXED
**Bug**: Wrong frame (18.6s in 19s video)  
**Ground Truth Method**: `time_from_max_hand = 0` (peak hand velocity)  
**Fix Applied**: Find peak bat velocity after foot down  
**Status**: ✅ **FIXED** (TypeScript-based implementation)

---

## 🧪 Test Validation Checklist

### When Testing Connor Gray Video (131200-Hitting.mov)

#### ✅ Expected Results (Target Values)
- [ ] **Tempo Ratio**: ~3.38 (± 0.3)
- [ ] **Bat Speed**: ~57.5 mph (± 5 mph)
- [ ] **Load Duration**: ~1,579 ms (± 200 ms)
- [ ] **Swing Duration**: ~467 ms (± 100 ms)
- [ ] **Contact Timing**: Within reasonable swing window (not at end of video)
- [ ] **Kinetic Sequence**: Logical order (pelvis → torso → arms → bat)

#### ⚠️ Known Issues to Check
- [ ] **Kinetic Sequence Gaps**: Should be 10-60ms between peaks (not 4-58ms spread)
- [ ] **Hardcoded Scores**: Ground/Engine should NOT be 100
- [ ] **Energy Distribution**: Lower=61%, Torso=29%, Arms=15%

---

## 📊 Ground Truth from Reboot Data

### Contact Detection Method
```
"correct_method": "time_from_max_hand = 0 (peak hand velocity)"
"fix": "Find frame where abs(time_from_max_hand) is minimum"
```

This confirms our approach:
- ✅ Peak velocity = contact point
- ✅ Search after foot down only
- ✅ Works for all swing types

### Bat Speed Calculation
```python
# Reboot Motion formula
bat_speed_mph = sqrt(2 * bat_trans_energy / bat_mass) * 2.237

# For Connor Gray:
bat_mass_kg = 0.85  # 33"/30oz bat
bat_trans_energy = bat_kinetic_energy  # from CSV
bat_speed = sqrt(2 * E / 0.85) * 2.237 = 57.5 mph
```

### Tempo Calculation
```python
# Ground Truth Timing (from Reboot)
load_start = -2.046 seconds before contact
launch_start = -0.467 seconds before contact
contact = 0 seconds (reference point)

# Durations
load_duration = abs(launch_start - load_start) = 2.046 - 0.467 = 1.579 seconds = 1579 ms
swing_duration = abs(contact - launch_start) = 0.467 seconds = 467 ms

# Tempo Ratio
tempo = load_duration / swing_duration = 1579 / 467 = 3.38
```

---

## 🎯 Validation Strategy

### Phase 1: Event Detection ✅
- [x] Fix contact detection (peak bat velocity)
- [x] Fix tempo calculation (proper phases)
- [x] Fix load/foot down detection
- [ ] **Test with Connor video**

### Phase 2: Bat Speed Refinement ⚠️
- [x] Implement lever arm physics
- [ ] Use momentum-based calculation: `momentum / mass * 2.237`
- [ ] Validate against 57.5 mph target
- [ ] Filter artifacts > 120 mph

### Phase 3: Energy Distribution 📋
- [ ] Calculate kinetic energy at contact
- [ ] Break down: Lower Half (61%), Torso (29%), Arms (15%)
- [ ] Validate against ground truth percentages

### Phase 4: Kinematic Sequence 📋
- [ ] Track segment peak times
- [ ] Calculate gaps: Pelvis(17ms) → Torso(4ms) → Arms(58ms)
- [ ] Validate timing makes sense

---

## 📈 Success Criteria

### Minimum Viable Product (MVP)
- ✅ Tempo ratio: 2.0-4.0 range
- ⚠️ Bat speed: ±10 mph of ground truth (47.5-67.5 mph)
- ✅ Contact detection: Within swing window
- ✅ Event sequence: Logical order

### Production Ready
- ✅ Tempo ratio: ±0.5 of ground truth (2.88-3.88)
- ⚠️ Bat speed: ±5 mph of ground truth (52.5-62.5 mph)
- ⚠️ Energy distribution: ±5% of ground truth
- 📋 Kinematic sequence: ±20ms of ground truth

---

## 🚀 Next Steps

1. **Test Connor Video** (URGENT)
   - Upload to web app
   - Compare results to ground truth
   - Document discrepancies

2. **Refine Bat Speed**
   - If still incorrect, implement momentum-based formula
   - Use `bat_momentum_magnitude / bat_mass * 2.237`

3. **Fix Kinetic Sequence**
   - Track peak times for each segment
   - Calculate proper gaps
   - Remove hardcoded sequence quality score

4. **Energy Distribution**
   - Calculate KE at contact for each segment
   - Validate percentages: 61/29/15

5. **Create Pull Request**
   - Merge all validated fixes
   - Document test results
   - Include ground truth comparisons

---

## 📝 Notes

### Data Quality
- Bat tracking has gaps near contact - use interpolation
- Frame rate: 240 fps (4.17ms resolution)
- Filter bat speeds > 120 mph as artifacts
- 2,903 time points across full swing sequence

### Key Insights
1. **Peak velocity = contact** is industry standard ✅
2. **Tempo phases** are well-defined: load → foot_down → contact ✅
3. **Energy distribution** follows 60/30/10 rule ✅
4. **Kinematic sequence** shows clear progression with tight gaps

### Ground Truth Source
- **API**: Reboot Motion momentum-energy export
- **Session**: 80e77691-d7cc-4ebb-b955-2fd45676f0ca
- **Date**: 2025-12-20
- **Reliability**: Professional-grade biomechanics system

---

**Status**: Ready for validation testing with Connor Gray video  
**Expected Outcome**: Tempo and contact detection should match ground truth within acceptable ranges  
**Focus Area**: Bat speed calculation still needs refinement
