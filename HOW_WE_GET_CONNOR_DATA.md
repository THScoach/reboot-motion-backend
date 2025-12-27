# HOW WE'RE GETTING CONNOR'S DATA FROM REBOOT API

**Complete Data Pipeline Documentation**

---

## 📍 Step 1: Reboot API Call

### API Endpoint
```bash
GET https://reboot-motion-backend-production.up.railway.app/api/reboot/sessions/4f1a7010-1324-469d-8e1a-e05a1dc45f2e/biomechanics
```

### Response Structure
```json
{
  "session_id": "4f1a7010-1324-469d-8e1a-e05a1dc45f2e",
  "session_date": "2025-12-20",
  "status": "processed",
  "player": {
    "org_player_id": "80e77691-d7cc-4ebb-b955-2fd45676f0ca",
    "first_name": "Connor",
    "last_name": "Gray"
  },
  "biomechanics": {
    "inverse_kinematics": {
      "available": true,
      "download_urls": [
        "https://reboot-motion-data-exports.s3.amazonaws.com/.../inverse-kinematics/csv/..."
      ],
      "data_format": "csv",
      "data_type": "inverse-kinematics"
    },
    "momentum_energy": {
      "available": true,
      "download_urls": [
        "https://reboot-motion-data-exports.s3.amazonaws.com/.../momentum-energy/csv/..."
      ],
      "data_format": "csv",
      "data_type": "momentum-energy"
    }
  }
}
```

**What We Get:**
- ✅ Session metadata (ID, date, player info)
- ✅ AWS S3 URLs for downloading CSVs
- ❌ No high-level metrics (rotation ROM, bat speed, etc.)
- ❌ No event detection (contact frame, load frame, etc.)
- ❌ No kinematic sequence metrics

---

## 📍 Step 2: Download CSV Files

### Inverse Kinematics CSV
```bash
curl -o /tmp/connor_ik.csv "https://reboot-motion-data-exports.s3.amazonaws.com/.../inverse-kinematics/csv/..."
```

**File Contents:**
- 2,903 rows (frames)
- 211 columns
- ~12 seconds of data at 240 Hz

**Key Columns We Use:**
```
Column 193: torso_rot       # Torso rotation angle
Column 194: pelvis_rot      # Pelvis rotation angle
Column 198: left_hip_rot    # Left hip rotation
Column 204: right_hip_rot   # Right hip rotation
```

**Example Data:**
```csv
index,torso_rot,pelvis_rot,left_hip_rot,right_hip_rot,...
0,-1.347,0.757,-1.571,-1.571,...
1,-1.289,0.812,-1.523,-1.534,...
2,-1.234,0.865,-1.478,-1.498,...
...
2902,0.869,3.756,0.921,1.571,...
```

### Momentum-Energy CSV
```bash
curl -o /tmp/connor_me.csv "https://reboot-motion-data-exports.s3.amazonaws.com/.../momentum-energy/csv/..."
```

**File Contents:**
- 2,903 rows (same frames as IK)
- ~24 energy columns
- Peak energies for each body segment

**Key Columns:**
```
torso_kinetic_energy        # Torso energy
lowertorso_kinetic_energy   # Lower torso
lth_kinetic_energy          # Left thigh
rth_kinetic_energy          # Right thigh
bat_kinetic_energy          # Bat (if tracked)
```

---

## 📍 Step 3: Load CSVs in Python

### Code (from analyze_connor_gray_actual.py)
```python
import pandas as pd

# Load Connor's data
ik_df = pd.read_csv('/tmp/connor_ik.csv')
me_df = pd.read_csv('/tmp/connor_me.csv')

print(f"Frames: {len(ik_df):,}")  # 2,903 frames
print(f"Duration: ~{len(ik_df) / 240.0:.2f}s")  # ~12 seconds
```

**Output:**
```
Frames: 2,903
Duration: ~12.10s
```

---

## 📍 Step 4: Calculate Rotation ROM (CURRENT METHOD)

### Code
```python
# Extract rotation columns
pelvis_rot = ik_df['pelvis_rot'].dropna()
torso_rot = ik_df['torso_rot'].dropna()

# Calculate Range of Motion (ROM)
pelvis_rom = pelvis_rot.max() - pelvis_rot.min()
torso_rom = torso_rot.max() - torso_rot.min()

print(f"Pelvis ROM: {pelvis_rom:.2f}°")  # 3.00°
print(f"Torso ROM: {torso_rom:.2f}°")    # 2.22°
```

**Output:**
```
Pelvis ROM: 3.00°
Torso ROM: 2.22°
```

### ⚠️ THE PROBLEM WITH THIS METHOD

**What `pelvis_rot` / `torso_rot` Actually Represent:**
- These are **POSE ANGLES** - the orientation of pelvis/torso in 3D space
- NOT **SWING ROTATION** - how much they rotated during the swing
- Like measuring "which direction is he facing" not "how much did he turn"

**Example:**
```
Frame 0: pelvis_rot = 0.757° (facing slightly right)
Frame 2902: pelvis_rot = 3.756° (facing more right)
ROM = 3.756° - 0.757° = 2.999°

But this is the TOTAL VARIATION across entire 12-second session
NOT the rotation during a single swing!
```

---

## 📍 Step 5: What We SHOULD Be Doing

### Option A: Calculate from Joint Positions

```python
import numpy as np

def calculate_pelvis_rotation(ik_df):
    """
    Calculate actual pelvis rotation from hip joint positions
    """
    # Extract hip joint positions
    left_hip = ik_df[['lhjc_x', 'lhjc_y', 'lhjc_z']].values  # Column 100-102
    right_hip = ik_df[['rhjc_x', 'rhjc_y', 'rhjc_z']].values  # Column 133-135
    
    # Calculate pelvis vector (from left to right hip)
    pelvis_vector = right_hip - left_hip
    
    # Project onto horizontal plane (ignore vertical component)
    pelvis_horiz = pelvis_vector[:, [0, 2]]  # x and z components
    
    # Calculate angle over time
    angles = np.arctan2(pelvis_horiz[:, 1], pelvis_horiz[:, 0])
    angles_deg = np.degrees(angles)
    
    # Find swing event (bat acceleration peak)
    # Measure rotation from load to contact
    # This would require event detection
    
    return angles_deg

# Usage
pelvis_angles = calculate_pelvis_rotation(ik_df)
# Need to identify swing window, then calculate ROM within that window
```

### Option B: Use Reboot's High-Level Metrics (DOESN'T EXIST YET)

**What the API SHOULD return:**
```json
{
  "session_id": "4f1a7010...",
  "biomechanics": {
    "swing_metrics": {
      "pelvis_rotation_rom": 42.3,  // ← THIS IS WHAT WE NEED
      "torso_rotation_rom": 35.7,   // ← THIS IS WHAT WE NEED
      "bat_speed_mph": 59.4,        // ← FROM BAT TRACKING
      "exit_velocity_mph": 98.0,    // ← IF AVAILABLE
      "attack_angle_deg": 12.5
    },
    "kinematic_sequence": {
      "pelvis_peak_velocity": 425,
      "pelvis_peak_timing": 0.145,
      "torso_peak_velocity": 738,
      "torso_peak_timing": 0.185,
      "x_factor": 45.2
    },
    "events": {
      "load_frame": 245,
      "stride_frame": 412,
      "contact_frame": 587,
      "follow_through_frame": 723
    }
  }
}
```

**But this DOESN'T EXIST in current API response!**

---

## 📍 Step 6: Where the 3° Value Comes From

### Exact Calculation Path

1. **API Call** → Get CSV URLs
2. **Download CSV** → Get 2,903 rows of `inverse-kinematics`
3. **Read Column 194** → `pelvis_rot` values range from 0.757° to 3.756°
4. **Calculate ROM** → `3.756° - 0.757° = 2.999° ≈ 3.00°`
5. **Report** → "Connor has 3° pelvis rotation"

### Why This is Wrong

**The 3° is the VARIATION across entire 12-second session:**
- Includes pre-swing stance
- Includes multiple swings (maybe)
- Includes post-swing recovery
- Includes random body sway/movement

**It's NOT measuring a single swing's rotation!**

---

## 📍 Step 7: How to Validate (Using HitTrax)

### Ground Truth Calculation

```python
# Connor's HitTrax data
exit_velocity = 98  # mph
pitch_speed = 52.5  # mph (50-55 range)

# Reverse-calculate bat speed
BALL_MASS_OZ = 5.125
BAT_WEIGHT_OZ = 29
COR_WOOD = 0.50
q = BALL_MASS_OZ / BAT_WEIGHT_OZ

bat_speed = (exit_velocity * (1 + q) - pitch_speed * COR_WOOD) / (1 + COR_WOOD)
# bat_speed = 59.4 mph

# Estimate required rotation
# Rule of thumb: 60 mph bat speed requires ~35-40° pelvis rotation
# Connor's 59.4 mph → needs ~35-40° pelvis rotation

# But Reboot says: 3° rotation
# CONTRADICTION! The data doesn't match physics
```

---

## 🎯 SUMMARY: Exact Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│ 1. API Request                                               │
│    GET /api/reboot/sessions/{id}/biomechanics               │
└────────────┬────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. API Response                                              │
│    - Session metadata                                        │
│    - CSV download URLs (S3 signed URLs)                     │
│    ❌ NO high-level metrics                                 │
└────────────┬────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. Download CSVs                                             │
│    - inverse-kinematics.csv (2,903 rows x 211 cols)        │
│    - momentum-energy.csv (2,903 rows x ~24 cols)           │
└────────────┬────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. Load in Pandas                                            │
│    ik_df = pd.read_csv(...)                                 │
│    me_df = pd.read_csv(...)                                 │
└────────────┬────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. Extract Rotation Columns (WRONG METHOD)                  │
│    pelvis_rot = ik_df['pelvis_rot']  # Column 194          │
│    torso_rot = ik_df['torso_rot']    # Column 193          │
│                                                              │
│    ROM = max(pelvis_rot) - min(pelvis_rot)                 │
│    Result: 3.756° - 0.757° = 2.999° ≈ 3.00°              │
└────────────┬────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────┐
│ 6. Report Results                                            │
│    "Connor has 3° pelvis rotation"                          │
│    ⚠️ BUT THIS IS WRONG!                                   │
│    - This is pose angle variation (not swing rotation)     │
│    - Measured across entire 12-second session              │
│    - Doesn't isolate single swing event                    │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔧 What Needs to Change

### Short-term Fix (In Our Code)
```python
# Instead of using pelvis_rot/torso_rot directly:
❌ pelvis_rom = ik_df['pelvis_rot'].max() - ik_df['pelvis_rot'].min()

# Do this:
✅ 1. Detect swing events (contact frame)
✅ 2. Calculate pelvis orientation from joint positions
✅ 3. Measure rotation from load → contact
✅ 4. Validate against HitTrax bat speed
```

### Long-term Fix (Request from Reboot)
```
Contact Reboot Motion and request:
1. swing_metrics.pelvis_rotation_rom
2. swing_metrics.torso_rotation_rom
3. kinematic_sequence metrics
4. event detection (contact frame)
5. bat_speed_mph from bat tracking
```

---

## 📊 Current State

**What We Have:**
- ✅ Raw joint position data (3D coordinates)
- ✅ Raw pose angles (pelvis_rot, torso_rot)
- ✅ Energy data (momentum-energy CSV)

**What We're Missing:**
- ❌ High-level swing metrics
- ❌ Event detection
- ❌ Kinematic sequence
- ❌ Validated bat speed
- ❌ Rotation ROM (actual swing rotation)

**Result:**
- We calculate 3° pelvis rotation (from pose angles)
- HitTrax shows 59.4 mph bat speed (requires 35-40° rotation)
- **DATA DOESN'T MATCH PHYSICS**

---

**File:** `analyze_connor_gray_actual.py` (lines 1-253)  
**Data Source:** Reboot Motion API → S3 CSV files  
**Problem:** Using wrong columns (pose angles, not swing rotation)  
**Solution:** Calculate from joint positions OR request enhanced API
