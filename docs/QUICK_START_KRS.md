# Quick Start Guide: KRS Transformer & Analysis

**Last Updated**: 2025-12-27  
**Status**: ✅ Production Ready

---

## Overview

The KRS Transformer converts Reboot Motion biomechanics data into comprehensive KRS reports with:
- **KRS Scores** (Creation, Transfer, Total)
- **Motor Profiles** (Spinner, Slingshotter, Stacker, Titan)
- **4B Framework** (BRAIN, BODY, BAT, BALL metrics)

---

## Quick Test (30 seconds)

### Option 1: Use the UI
```bash
# Open the Coach Rick Analysis interface
open https://reboot-motion-backend-production.up.railway.app/coach-rick-analysis

# Steps:
1. Type "Connor Gray" in the search box
2. Click on Connor's player card
3. See his 3 sessions listed
4. Click "Generate KRS Report" on any session
5. View complete KRS analysis with scores and metrics
```

### Option 2: Use the API
```bash
# Generate KRS report for Connor Gray's first session
curl -X POST "https://reboot-motion-backend-production.up.railway.app/api/reboot/generate-krs-report?session_id=4f1a7010-1324-469d-8e1a-e05a1dc45f2e"

# Response includes:
{
  "krs": {
    "krs_total": 48.5,
    "krs_level": "FOUNDATION",
    "creation_score": 35.0,
    "transfer_score": 57.6
  },
  "motor_profile": {
    "type": "Titan",
    "confidence": 100
  },
  "framework_metrics": {
    "brain": {...},
    "body": {...},
    "bat": {...},
    "ball": {...}
  }
}
```

---

## Available Endpoints

### 1. Search Players
```bash
GET /api/reboot/players/search?query=Connor
```
Returns list of matching players with IDs.

### 2. Get Player Sessions
```bash
GET /api/reboot/players/{player_id}/sessions?limit=10
```
Returns list of sessions for the player.

### 3. Get Session Biomechanics
```bash
GET /api/reboot/sessions/{session_id}/biomechanics
```
Returns download URLs for CSV files (inverse kinematics + momentum energy).

### 4. Generate KRS Report (NEW!)
```bash
POST /api/reboot/generate-krs-report?session_id={session_id}
```
Downloads CSVs, transforms to KRS, returns complete report.

---

## How It Works

### Step 1: User selects a session
- Search for player (e.g., "Connor Gray")
- View their session history
- Click "Generate KRS Report"

### Step 2: Backend processes biomechanics
1. **Authenticate** with Reboot Motion API (OAuth)
2. **Retrieve** session details and player info
3. **Export** biomechanics data (IK + ME)
4. **Download** CSV files from S3 signed URLs
5. **Parse** ~2900 frames × 555 columns = 1.6M data points
6. **Calculate** KRS scores and metrics
7. **Return** complete JSON report

### Step 3: Display results
- KRS Score with level badge
- Motor Profile with confidence
- 4B Framework cards (BRAIN, BODY, BAT, BALL)
- On-table gain (potential improvement)

---

## KRS Scoring Logic

### Creation Score (0-100)
**What**: Force generation in lower half  
**Inputs**:
- Hip rotation velocity (40% weight)
- Hip-shoulder separation / X-Factor (30% weight)
- Lower body kinetic energy (30% weight)

**Formula**:
```python
hip_velocity_score = min(100, (hip_rotation_velocity / 10) * 100)
separation_score = min(100, (separation / 60) * 100)
energy_score = min(100, (peak_lower_energy / 200) * 100)

creation_score = (
    hip_velocity_score * 0.4 +
    separation_score * 0.3 +
    energy_score * 0.3
)
```

### Transfer Score (0-100)
**What**: Efficiency of energy flow from body to bat  
**Inputs**:
- Torso rotation velocity (35% weight)
- Energy sequencing (proximal-to-distal) (35% weight)
- Bat speed at contact (30% weight)

**Formula**:
```python
torso_velocity_score = min(100, (torso_rotation_velocity / 8) * 100)
sequence_score = 100 if proper_sequence else 70
bat_speed_score = min(100, (peak_bat_energy / 150) * 100)

transfer_score = (
    torso_velocity_score * 0.35 +
    sequence_score * 0.35 +
    bat_speed_score * 0.30
)
```

### KRS Total
```python
krs_total = (creation_score * 0.4) + (transfer_score * 0.6)
```

### KRS Levels
- **90-100**: ELITE
- **80-89**: ADVANCED
- **70-79**: DEVELOPING
- **60-69**: BUILDING
- **0-59**: FOUNDATION

---

## Motor Profile Detection

### Spinner
**Traits**: Hip-dominant, early rotation  
**Detection**: Peak hip rotation > 45°  
**Confidence**: Based on hip rotation magnitude

### Slingshotter
**Traits**: High separation, late burst  
**Detection**: Hip-shoulder separation > 60°  
**Confidence**: Based on X-Factor magnitude

### Stacker
**Traits**: Sequential, ground-up force  
**Detection**: Energy peaks follow proximal-to-distal order with timing < 0.15s  
**Confidence**: Based on sequence timing precision

### Titan
**Traits**: Power-dominant, high energy  
**Detection**: Total kinetic energy > 500 J  
**Confidence**: Based on total energy magnitude

---

## 4B Framework Metrics

### BRAIN (Motor Learning & Timing)
- `timing`: Total swing duration (seconds)
- `time_to_contact`: Time from start to peak bat speed (seconds)
- `efficiency`: Movement efficiency percentage

### BODY (Force Creation)
- `creation_score`: Same as KRS creation score (0-100)
- `physical_capacity_mph`: Estimated max exit velocity from body metrics
- `peak_force_n`: Peak force production (Newtons)

### BAT (Transfer Efficiency)
- `transfer_score`: Same as KRS transfer score (0-100)
- `transfer_efficiency`: Percentage of body energy transferred to bat
- `attack_angle_deg`: Bat angle at contact (degrees)

### BALL (Outcomes)
- `exit_velocity_mph`: Estimated exit velocity (mph)
- `capacity_mph`: Maximum potential exit velocity (mph)
- `launch_angle_deg`: Launch angle (degrees)
- `contact_quality`: POOR / FAIR / SOLID / EXCELLENT

---

## Example: Connor Gray Analysis

**Session**: 2025-12-20  
**Session ID**: `4f1a7010-1324-469d-8e1a-e05a1dc45f2e`

### Results
```json
{
  "krs": {
    "krs_total": 48.5,
    "krs_level": "FOUNDATION",
    "creation_score": 35.0,
    "transfer_score": 57.6
  },
  "motor_profile": {
    "type": "Titan",
    "confidence": 100
  },
  "framework_metrics": {
    "brain": {
      "timing": 3.288,
      "time_to_contact": 1.55,
      "efficiency": 85.0
    },
    "body": {
      "creation_score": 35.0,
      "physical_capacity_mph": 110,
      "peak_force_n": 598.0
    },
    "bat": {
      "transfer_score": 57.6,
      "transfer_efficiency": 100,
      "attack_angle_deg": 15.0
    },
    "ball": {
      "exit_velocity_mph": 110,
      "capacity_mph": 110,
      "launch_angle_deg": 18.0,
      "contact_quality": "EXCELLENT"
    }
  }
}
```

### Interpretation
- **KRS 48.5 (FOUNDATION)**: Early in development, room for improvement
- **Titan Profile**: High-energy, power-dominant swing style
- **Creation 35.0**: Lower body force generation needs work
- **Transfer 57.6**: Energy transfer efficiency is moderate
- **Exit Velo 110 mph**: Excellent contact quality when connecting
- **No On-Table Gain**: Already at capacity, focus on consistency

---

## Performance

### Processing Time
- **Total**: ~6 seconds per session
- OAuth authentication: ~1s
- Session details: ~0.5s
- Data export URLs: ~1s
- CSV downloads: ~4s
- KRS transformation: ~0.1s

### Data Volume
- **Frames**: ~2,900 per swing
- **Columns**: 555 total (211 IK + 344 ME)
- **Data Points**: 1,611,165 per session
- **CSV Size**: ~1-2 MB per file

---

## Troubleshooting

### Error: "Reboot Motion credentials not configured"
**Solution**: Set environment variables in Railway:
```bash
REBOOT_USERNAME=coachrickpd@gmail.com
REBOOT_PASSWORD=Train@2025
```

### Error: "Session not found"
**Solution**: Verify session ID is correct and session exists:
```bash
curl "https://reboot-motion-backend-production.up.railway.app/api/reboot/players/search?query=Connor"
```

### Error: "Biomechanics download URLs not available"
**Solution**: Session may not be fully processed. Check session status:
```bash
curl "https://reboot-motion-backend-production.up.railway.app/api/reboot/sessions/{session_id}/biomechanics"
```

### Slow response time
**Expected**: First request may take ~10 seconds due to:
- OAuth token generation
- S3 signed URL generation
- Large CSV downloads

**Solution**: Normal behavior, subsequent requests use cached tokens.

---

## Local Development

### Run locally
```bash
cd /home/user/webapp

# Set credentials
export REBOOT_USERNAME='coachrickpd@gmail.com'
export REBOOT_PASSWORD='Train@2025'
export DATABASE_URL='sqlite:///catching_barrels.db'

# Test KRS endpoint
python3 test_krs_endpoint.py

# Expected output:
# ✅ KRS Score: 48.5 (FOUNDATION)
# ✅ Motor Profile: Titan (100%)
# ✅ 4B Framework: All metrics calculated
```

### Run tests
```bash
# End-to-end test with Connor Gray
python3 << 'EOF'
import os
os.environ['REBOOT_USERNAME'] = 'coachrickpd@gmail.com'
os.environ['REBOOT_PASSWORD'] = 'Train@2025'

from session_api import generate_krs_from_reboot
import asyncio

session_id = '4f1a7010-1324-469d-8e1a-e05a1dc45f2e'
result = asyncio.run(generate_krs_from_reboot(session_id))

print(f"KRS: {result['krs']['krs_total']}")
print(f"Motor Profile: {result['motor_profile']['type']}")
EOF
```

---

## Next Steps

### Use the system
1. Open https://reboot-motion-backend-production.up.railway.app/coach-rick-analysis
2. Search for any player
3. Generate KRS reports for their sessions
4. View complete analysis and metrics

### Optional enhancements
- Store reports in database for historical tracking
- Add progress charts (KRS over time)
- Generate drill recommendations based on motor profile
- Compare multiple sessions side-by-side
- Export reports to PDF

---

## Support

**Documentation**: `/docs` folder
- `TASK_COMPLETION_REPORT.md` - Complete implementation details
- `MISSION_ACCOMPLISHED.md` - Project summary
- `BIOMECHANICS_DATA_AVAILABLE.md` - Data sources guide

**GitHub**: https://github.com/THScoach/reboot-motion-backend

**Questions**: See `/docs` for detailed documentation

---

🎉 **Ready to analyze swings with real biomechanics data!**
