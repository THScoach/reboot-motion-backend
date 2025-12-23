# REBOOT MOTION DATA EXPORT - ACTION PLAN

## What We Discovered:

### ✅ Reboot Motion HAS Biomechanics Data
The Data Export API exists and contains full biomechanics:
- Angular velocities (pelvis, torso, arms, bat)
- Peak velocities
- Event timing (first move, foot plant, contact)
- Kinematic sequence
- Bat speed
- Momentum data

### ❌ Our Backend is NOT Syncing It
Current status:
```json
{
  "players_synced": 100,
  "sessions_synced": 10,
  "biomechanics_synced": 0  ← NOT PULLING BIOMECHANICS
}
```

---

## HOW TO FIX:

### Option 1: Add Data Export Endpoint to Backend (FASTEST)

**Add to `main.py`:**
```python
@app.get("/reboot/data-export/{session_id}")
def get_reboot_data_export(session_id: str, movement_type: str = "baseball-hitting"):
    """Fetch biomechanics from Reboot Motion Data Export API"""
    sync = RebootMotionSync()
    token = sync._get_access_token()
    
    response = requests.get(
        "https://api.rebootmotion.com/data_export",
        headers={'Authorization': f'Bearer {token}'},
        params={'session_id': session_id, 'movement_type': movement_type}
    )
    
    return response.json()
```

**Then we can call:**
```
GET https://reboot-motion-backend-production.up.railway.app/reboot/data-export/{session_id}
```

### Option 2: Update Sync Service to Pull Biomechanics

**Update `sync_service.py`** to:
1. After syncing sessions
2. For each hitting session
3. Call Data Export API
4. Parse biomechanics data
5. Save to database

---

## WHAT THE DATA EXPORT CONTAINS:

Based on Reboot Motion documentation:

### Movement Analysis Data:
- **Momentum-based kinematics** (344 columns)
  - Pelvis momentum
  - Torso momentum
  - Arm momentum
  - Bat momentum
  
- **Inverse kinematics** (211 columns)
  - Joint angles
  - Angular velocities
  - Linear velocities
  
- **Event markers**
  - First movement timing
  - Foot plant timing
  - Contact timing
  - Follow-through
  
- **Peak velocity data**
  - Peak pelvis velocity
  - Peak torso velocity
  - Peak bat velocity
  - Kinematic sequence timing

### This is GOLD for:
1. **Validation** - Compare MediaPipe calculations to Reboot data
2. **Calibration** - Use pro player data as reference
3. **Benchmarking** - Build accurate pro comparison

---

## IMMEDIATE NEXT STEPS:

### Step 1: Add Endpoint to Backend
Copy `ENDPOINT_DATA_EXPORT.py` content into `main.py`

### Step 2: Deploy to Railway
```bash
git add main.py
git commit -m "feat: Add Reboot Motion Data Export endpoint"
git push
```

### Step 3: Test Data Retrieval
```bash
curl "https://reboot-motion-backend-production.up.railway.app/reboot/data-export/6764e74b-516d-45eb-a8a9-c50a069ef50d"
```

### Step 4: Analyze Data Structure
- Document what fields exist
- Map to our physics engine metrics
- Build validation tests

### Step 5: Use for Calibration
- Compare MediaPipe joint angles to Reboot inverse kinematics
- Calibrate velocity calculations
- Validate event detection

---

## WHY THIS MATTERS:

### Current Problem:
Our physics engine produces wrong results:
- Tempo: 0.05 (should be 2.0-3.5)
- Bat speed: 21.6 mph (should be 70-85 mph)
- Contact detected at wrong frame

### With Reboot Data:
- **Ground truth** for pro players
- **Validation** of our calculations
- **Calibration** of references
- **Benchmarking** for comparisons

---

## FILES CREATED:

1. `test_reboot_data.py` - Standalone test script
2. `ENDPOINT_DATA_EXPORT.py` - Backend endpoint code
3. `REBOOT_DATA_EXPORT_PLAN.md` - This file

---

## RECOMMENDATION:

**DO THIS FIRST** before fixing event detection:

1. Add Data Export endpoint to backend
2. Pull sample pro player biomechanics
3. Compare to our MediaPipe output
4. Calibrate physics engine with real data
5. Then fix event detection

This way we're calibrating against REAL pro data, not guessing.

---

**Session IDs we have:**
- Ronald Acuna: `6764e74b-516d-45eb-a8a9-c50a069ef50d`
- 9 other hitting sessions available

Let's pull their data and use it as ground truth! 🎯
