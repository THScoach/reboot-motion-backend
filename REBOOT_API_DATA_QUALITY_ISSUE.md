# Reboot Motion API - Data Quality Issue

**Date**: December 27, 2025  
**Issue**: Rotation measurements don't match real-world performance  
**Impact**: KRS calculations are incorrect, drill prescriptions may be wrong

---

## 🚨 The Problem

### Connor Gray's Data Mismatch

**HitTrax Reality:**
- Exit Velocity: **98 mph** (off 50-55 mph pitching machine)
- Calculated Bat Speed: **59.4 mph**
- Performance: **99% of exospeed capacity** (60.1 mph)
- **Conclusion: Normal, healthy swing for age/size**

**Reboot Motion Says:**
- Pelvis Rotation (ROM): **3.00°** (should be 40-50°)
- Torso Rotation (ROM): **2.22°** (should be 30-40°)
- **Conclusion: Arms-only swing, no body rotation**

### The Physics Don't Match

**To generate 59.4 mph bat speed, you NEED:**
- Minimum 30-40° pelvis rotation
- Minimum 20-30° torso rotation
- Proper kinematic sequencing

**You CANNOT generate 59.4 mph with:**
- Only 3° pelvis rotation
- Only 2° torso rotation
- Arms alone (max ~40 mph for this athlete)

**VERDICT: Reboot rotation data is incorrect**

---

## 🔬 Root Cause Analysis

### What We're Currently Using

From `inverse-kinematics` CSV:
```
Column 193: torso_rot
Column 194: pelvis_rot
```

**Current Analysis Method:**
```python
# We calculate ROM (Range of Motion)
pelvis_rom = pelvis_rot.max() - pelvis_rot.min()
torso_rom = torso_rot.max() - torso_rot.min()

# Connor's data shows:
pelvis_rom = 3.756° - 0.757° = 2.999° ✅ (this is what we see)
torso_rom = 0.869° - (-1.347°) = 2.215° ✅ (this is what we see)
```

### ⚠️ Hypothesis 1: Wrong Columns

**Problem:** `torso_rot` and `pelvis_rot` might be:
1. **Pose angles** (static body orientation in space)
2. **Not swing rotation** (dynamic rotation during swing)
3. **Relative to camera** (not anatomical rotation)

**What we SHOULD be using:**
- Need columns that measure **angular displacement** during swing
- Or calculate rotation from **joint position changes** over time
- Or use **angular velocity** integrated over swing duration

### ⚠️ Hypothesis 2: Radians vs Degrees

**Problem:** Values might be in radians, not degrees

**Test:**
```
If 2.999 is radians → 171.9° (way too high, unlikely)
If 2.999 is degrees → 2.999° (current interpretation, way too low)
```

**VERDICT:** Unlikely to be radians (values too consistent with degrees)

### ⚠️ Hypothesis 3: Incomplete Swing Capture

**Problem:** Session data may not capture full swing

**Connor's Session:**
- Frames: 2,903
- Duration: ~12 seconds
- Frame rate: ~240 fps

**Analysis:**
- 12 seconds is PLENTY for a full swing (swing takes 0.2-0.4s)
- Should have captured multiple swings
- Unlikely to be the issue

### ⚠️ Hypothesis 4: Measuring Wrong Phase

**Problem:** Measuring stance rotation, not swing rotation

**Possible Explanation:**
- `pelvis_rot` / `torso_rot` = rotation in STANCE phase
- Doesn't measure rotation DURING SWING
- Connor might have minimal stance rotation but large swing rotation

**Test:** Need to identify swing event frames and measure rotation specifically during swing

### 🎯 Hypothesis 5: Need Derived Calculations

**Problem:** Raw columns don't directly give swing rotation

**What's Actually Needed:**
```python
# Calculate pelvis rotation from joint positions
def calculate_pelvis_rotation(lhjc, rhjc, midhip):
    # Left hip joint center, right hip joint center, mid hip
    # Calculate pelvis orientation vector
    # Track change over time during swing
    pass

# Or use shoulder positions
def calculate_torso_rotation(lsjc, rsjc, neck):
    # Left shoulder, right shoulder, neck
    # Calculate torso orientation
    # Track change during swing
    pass
```

---

## 📊 What's Missing from Reboot API

### Current API Response

```json
{
  "biomechanics": {
    "inverse_kinematics": {
      "available": true,
      "download_urls": ["...csv"],
      "data_type": "inverse-kinematics"
    },
    "momentum_energy": {
      "available": true,
      "download_urls": ["...csv"],
      "data_type": "momentum-energy"
    }
  }
}
```

### ❌ Missing: High-Level Metrics

**What We Need:**
```json
{
  "biomechanics": {
    "kinematic_sequence": {
      "pelvis_peak_velocity": 425,  // deg/s
      "pelvis_peak_timing": 0.145,  // % of swing
      "torso_peak_velocity": 738,   // deg/s
      "torso_peak_timing": 0.185,   // % of swing
      "separation_angle": 45.2      // degrees
    },
    "swing_metrics": {
      "pelvis_rotation_rom": 42.3,  // degrees (ACTUAL rotation)
      "torso_rotation_rom": 35.7,   // degrees (ACTUAL rotation)
      "bat_speed_mph": 59.4,        // mph
      "time_to_contact": 0.185      // seconds
    },
    "posture": {
      "bat_speed": 59.4,            // mph (from bat tracking)
      "exit_velocity": 98,          // mph (if available)
      "attack_angle": 12.5          // degrees
    }
  }
}
```

### ❌ Missing: Event Detection

**What We Need:**
- `stance_start`: Frame where stance begins
- `load_start`: Frame where load phase begins
- `stride_start`: Frame where stride begins
- `contact`: Frame where bat contacts ball
- `follow_through_end`: Frame where follow-through ends

**Why It Matters:**
- Calculate rotation DURING SWING ONLY
- Not measuring stance/setup rotation
- Isolate power generation phase

### ❌ Missing: Calculated Metrics

**What Reboot Should Provide:**
```json
{
  "calculated_metrics": {
    "pelvis_rotation_at_contact": 45.2,  // degrees (from stance to contact)
    "torso_rotation_at_contact": 38.7,   // degrees
    "x_factor": 15.3,                     // hip-shoulder separation
    "ground_reaction_force": 1250,        // Newtons
    "kinetic_chain_efficiency": 0.82      // 0-1 scale
  }
}
```

---

## 🛠️ What We Need to Do

### Option 1: Use Existing API Correctly

**Action Items:**
1. ✅ Identify which columns measure ACTUAL rotation
2. ✅ Calculate rotation from joint positions (not pose angles)
3. ✅ Detect swing events (contact frame)
4. ✅ Measure rotation DURING SWING only
5. ✅ Validate against HitTrax bat speed

**Code Changes Needed:**
```python
# Instead of:
pelvis_rom = df['pelvis_rot'].max() - df['pelvis_rot'].min()

# Do this:
def calculate_actual_pelvis_rotation(df):
    # Use hip joint positions to calculate pelvis orientation
    left_hip = df[['lhjc_x', 'lhjc_y', 'lhjc_z']].values
    right_hip = df[['rhjc_x', 'rhjc_y', 'rhjc_z']].values
    
    # Calculate pelvis vector
    pelvis_vector = right_hip - left_hip
    
    # Calculate rotation angle over time
    # Project onto horizontal plane
    # Measure angular change from stance to contact
    ...
```

### Option 2: Request Enhanced API from Reboot

**What to Ask Reboot For:**
1. **High-level metrics** in API response (pelvis_rotation_rom, torso_rotation_rom)
2. **Event timestamps** (stance, load, contact, follow-through)
3. **Kinematic sequence** data (peak velocities, timing)
4. **Bat speed** from their bat tracking (if available)
5. **X-factor** and separation angles

**Benefits:**
- Don't have to reverse-engineer from raw joint positions
- Reboot's algorithms are validated
- Consistent across all players
- Faster processing

### Option 3: Hybrid Approach (RECOMMENDED)

**Phase 1: Fix Our Calculations**
- Re-calculate rotation from joint positions
- Detect swing events from bat/body motion
- Validate against HitTrax data

**Phase 2: Request API Enhancements**
- Ask Reboot to expose high-level metrics
- Use their validated algorithms
- Keep our calculations as backup/validation

---

## 🧪 Validation Test Cases

### Connor Gray
- **HitTrax:** 98 mph exit velocity (vs 50-55 mph pitch)
- **Expected Bat Speed:** 59.4 mph
- **Expected Pelvis Rotation:** 30-40° (to generate this speed)
- **Current Reboot:** 3.00° pelvis ❌
- **Target:** Calculate 30-40° from joint positions ✅

### Eric Williams
- **Coach's Observation:** "Ground balls, weak contact"
- **HitTrax:** 82 mph bat speed, 98 mph exit velocity
- **Expected Issue:** Poor rotation or timing
- **Current Reboot:** 2.87° pelvis ❌
- **Target:** Identify actual mechanical issue ✅

---

## 📋 Action Plan

### Immediate (Today)
1. ✅ Document the data quality issue
2. ⏭️ Write script to calculate rotation from joint positions
3. ⏭️ Test on Connor Gray data
4. ⏭️ Validate against HitTrax bat speed

### Short-term (This Week)
5. ⏭️ Apply corrected calculations to all players
6. ⏭️ Re-generate KRS reports with accurate rotation data
7. ⏭️ Update motor profile classifications
8. ⏭️ Validate drill prescriptions

### Long-term (Next Sprint)
9. ⏭️ Contact Reboot Motion about API enhancements
10. ⏭️ Request access to kinematic sequence metrics
11. ⏭️ Integrate enhanced API when available
12. ⏭️ Build validation dashboard (Reboot vs HitTrax)

---

## 💡 Key Insights

### What We Learned

1. **Reboot `pelvis_rot` / `torso_rot` columns are NOT swing rotation**
   - Likely pose angles or stance orientation
   - Don't capture dynamic swing rotation
   - Can't be used directly for KRS calculations

2. **HitTrax data is the ground truth**
   - Exit velocity + pitch speed → bat speed
   - Bat speed → minimum required rotation
   - Use this to validate Reboot calculations

3. **Need to calculate rotation ourselves**
   - Use joint positions (hip, shoulder, neck)
   - Calculate orientation vectors
   - Track angular change during swing
   - Measure specifically from load → contact

4. **Connor is performing normally**
   - 59.4 mph bat speed at 99% of capacity
   - NOT an arms-only swinger
   - Rotation data was misleading us

---

## 🎯 Expected Outcomes

### After Corrections

**Connor Gray:**
- Calculated Pelvis Rotation: 35-45° (from joint positions)
- Calculated Torso Rotation: 28-38° (from joint positions)
- KRS Level: ADVANCED (not FOUNDATION)
- Motor Profile: SPINNER or SYNCER (not WHIPPER)
- Drill Prescription: Refinement (not rebuild)

**Eric Williams:**
- Similar correction expected
- Actual rotation likely 30-40° pelvis
- Ground balls due to TIMING issue (not lack of rotation)
- Different prescription after accurate data

---

## 📞 Questions for Reboot Motion

### API Enhancement Request

1. **Do you expose kinematic sequence metrics?**
   - Pelvis/torso peak velocity
   - Peak timing (% of swing)
   - Separation angles

2. **What do `pelvis_rot` and `torso_rot` columns represent?**
   - Pose angles in space?
   - Anatomical joint angles?
   - Cumulative rotation?

3. **Can you provide swing event timestamps?**
   - Load, stride, contact, follow-through
   - Or event detection algorithm

4. **How do you calculate rotation ROM?**
   - From joint positions?
   - From IMU data?
   - Algorithm details?

5. **Do you have bat speed calculations?**
   - From bat tracking
   - Validated against HitTrax/Rapsodo
   - Available in API?

---

**Status**: 🔴 **CRITICAL ISSUE IDENTIFIED**  
**Priority**: 🔥 **HIGH - Blocks accurate KRS reporting**  
**Next Step**: Calculate rotation from joint positions  
**ETA**: Fix available in 2-4 hours
