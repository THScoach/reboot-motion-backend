# ✅ DATA EXPORT ENDPOINT ADDED TO BACKEND

## What Was Added:

### New Endpoint:
```
GET /reboot/data-export/{session_id}?movement_type=baseball-hitting
```

**Location:** `main.py` lines 258-337

### What It Does:
1. Takes Reboot Motion session UUID (e.g., `6764e74b-516d-45eb-a8a9-c50a069ef50d`)
2. Gets OAuth token from sync service
3. Calls Reboot Motion Data Export API
4. Returns full biomechanics data

### Response Format:
```json
{
  "status": "success",
  "session_id": "6764e74b-516d-45eb-a8a9-c50a069ef50d",
  "movement_type": "baseball-hitting",
  "data": {
    // Full biomechanics data here
    // Angular velocities, peak velocities, event timing, etc.
  }
}
```

---

## How to Deploy:

### Option 1: Manual Deploy on Railway
1. Go to Railway dashboard
2. Open `reboot-motion-backend` project
3. Go to deployments
4. Click "Deploy" to trigger manual deployment

### Option 2: Push to GitHub (Auto-deploy)
Railway is connected to GitHub and auto-deploys on push to main.

**To push:**
```bash
cd /home/user/webapp
git push origin main
```

(You'll need to authenticate with GitHub token)

---

## After Deployment:

### Test the Endpoint:
```bash
# Get Ronald Acuna's biomechanics
curl "https://reboot-motion-backend-production.up.railway.app/reboot/data-export/6764e74b-516d-45eb-a8a9-c50a069ef50d"
```

### Expected Response:
Full biomechanics JSON including:
- `angular_velocity` - Pelvis, torso, arm, bat
- `peak_velocities` - Peak values for each segment
- `timing_events` - First move, foot plant, contact
- `kinematic_sequence` - Sequence timing
- `bat_speed` - Actual bat speed data
- `momentum` - Momentum-based kinematics (344 columns)
- `inverse_kinematics` - Joint angles and velocities (211 columns)

---

## What This Enables:

### 1. Physics Engine Validation
Compare our MediaPipe calculations to Reboot's ground truth:
```python
# Our calculation
our_bat_speed = 61.4 mph

# Reboot's measurement
reboot_bat_speed = 78.3 mph

# Calibration factor
calibration = reboot_bat_speed / our_bat_speed  # 1.28
```

### 2. Event Detection Calibration
See where Reboot detects events:
```python
# Reboot's timing
{
  "first_move": 1250ms,
  "foot_plant": 1580ms,
  "contact": 1720ms
}

# Fix our detection to match
```

### 3. Pro Player Benchmarks
Use as reference for scoring:
```python
# Shohei Ohtani
{
  "peak_pelvis_velocity": 650 deg/s,
  "peak_torso_velocity": 820 deg/s,
  "peak_bat_velocity": 78 mph,
  "tempo_ratio": 2.8
}

# Use as 90-score reference
```

---

## Available Sessions:

We have 10 hitting sessions synced:
- Ronald Acuna: `6764e74b-516d-45eb-a8a9-c50a069ef50d`
- 9 others (check `/players/{id}/sessions`)

All are professional MLB players with validated biomechanics data.

---

## Next Steps After Deployment:

1. ✅ Test endpoint with sample session
2. ✅ Document data structure
3. ✅ Compare to our MediaPipe output
4. ✅ Calibrate physics engine references
5. ✅ Fix event detection with real timing
6. ✅ Re-test with Shohei video

---

## Files Modified:

- `main.py` - Added Data Export endpoint (83 new lines)
- Committed: `2246e1d`

---

## Deployment Status:

⏳ **Waiting for deployment**

After Railway deploys, the endpoint will be available at:
```
https://reboot-motion-backend-production.up.railway.app/reboot/data-export/{session_id}
```

---

**Ready to deploy and pull real pro player biomechanics data!** 🎯
