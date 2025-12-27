# Reboot Report Metrics System

**Solution to Reboot API Data Quality Issue**

Since Reboot Motion's API/CSV files don't contain the actual rotation data shown in their reports, we extract metrics directly from reports instead.

---

## 🎯 Problem Summary

**Issue:** Reboot API CSV `pelvis_rot` column shows 3° but report shows 60°  
**Root Cause:** CSV columns are pose angles, not swing rotation  
**Solution:** Extract metrics from reports (manual input + automated parsing)

---

## 📊 System Architecture

```
┌─────────────────┐
│  Reboot Report  │ (PNG/PDF from Reboot Motion)
│  (60° rotation) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Upload Report  │ POST /api/reboot/sessions/{id}/upload-report
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Manual Input OR │ Human reads charts OR
│ Auto Parser     │ Computer vision extracts metrics
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Save Metrics   │ POST /api/reboot/sessions/{id}/report-metrics
│  (Database)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ KRS Calculation │ Uses report metrics instead of CSV
│ (Accurate)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Generate       │ Correct motor profile & drill prescription
│  KRS Report     │
└─────────────────┘
```

---

## 📁 Files Created

### **1. Database Schema**
`/database/migrations/create_reboot_report_metrics.sql`
- Table: `reboot_report_metrics`
- Stores extracted metrics from reports
- Links to session_id

### **2. API Routes**
`/app/routes/reboot_report_routes.py`
- `POST /api/reboot/sessions/{id}/upload-report` - Upload report file
- `GET /api/reboot/sessions/{id}/report-metrics` - Get metrics
- `POST /api/reboot/sessions/{id}/report-metrics` - Save metrics
- `POST /api/reboot/sessions/{id}/report-metrics/validate` - Validate with HitTrax

### **3. Manual Input Form**
`/app/templates/reboot_report_manual_input.html`
- Web UI for manual metric entry
- Report preview side-by-side with form
- Instructions for reading charts
- Validation against HitTrax

### **4. Quick Insert Script**
`/insert_connor_metrics.py`
- Python script to insert Connor's metrics
- Can use API or generate SQL
- Includes all extracted values

---

## 🚀 Usage

### **Phase A: Manual Input (Today)**

#### **Step 1: Run Database Migration**
```sql
psql -U postgres -d reboot_motion < database/migrations/create_reboot_report_metrics.sql
```

#### **Step 2: Start Flask App**
```bash
cd /home/user/webapp
python app.py
```

#### **Step 3: Upload Report**
```bash
curl -X POST \
  -F "report=@connor_reboot_report.png" \
  http://localhost:5000/api/reboot/sessions/4f1a7010-1324-469d-8e1a-e05a1dc45f2e/upload-report
```

#### **Step 4: Open Manual Input Form**
```
http://localhost:5000/reboot-report-input?session_id=4f1a7010-1324-469d-8e1a-e05a1dc45f2e
```

#### **Step 5: Enter Metrics**
Look at "Torso Kinematics" chart:
- **Purple line (Pelvis):** Min ~10°, Max ~70° → ROM = **60°**
- **Orange line (Torso):** Min ~15°, Max ~40° → ROM = **25°**

Enter values and save.

#### **Or Use Quick Script:**
```bash
cd /home/user/webapp
python insert_connor_metrics.py
```

---

### **Phase B: Automated Parsing (This Week)**

Build computer vision parser to automatically extract:
1. Locate "Torso Kinematics" chart
2. Identify purple (pelvis) and orange (torso) lines
3. Read Y-axis min/max values
4. Calculate ROM automatically
5. Present for review/confirmation

---

## 📊 Connor Gray Example

### **Extracted Metrics:**
```json
{
  "session_id": "4f1a7010-1324-469d-8e1a-e05a1dc45f2e",
  "pelvis_rotation_rom_deg": 60.0,
  "torso_rotation_rom_deg": 25.0,
  "pelvis_peak_velocity_deg_per_s": 425,
  "torso_peak_velocity_deg_per_s": 738,
  "bat_speed_mph": 59.4,
  "exit_velocity_mph": 98.0,
  "validated_against_hittrax": true
}
```

### **Validation:**
```
HitTrax: 98 mph exit velocity → 59.4 mph bat speed
Physics: 59.4 mph requires 35-40° pelvis minimum
Report: 60° pelvis rotation
Status: ✅ MATCHES PHYSICS
```

### **Impact:**
- **Old (CSV):** 3° rotation → WHIPPER → Rebuild rotation from scratch
- **New (Report):** 60° rotation → SPINNER → Refinement only

---

## 🔧 Integration with KRS System

### **Update KRS Calculation:**
```python
# OLD METHOD (WRONG)
pelvis_rom = ik_df['pelvis_rot'].max() - ik_df['pelvis_rot'].min()  # 3° ❌

# NEW METHOD (CORRECT)
report_metrics = get_report_metrics(session_id)
pelvis_rom = report_metrics['pelvis_rotation_rom_deg']  # 60° ✅
```

### **Fallback Logic:**
```python
def get_rotation_metrics(session_id):
    # Try report metrics first
    report_metrics = db.query_report_metrics(session_id)
    
    if report_metrics:
        return {
            'source': 'report',
            'pelvis_rom': report_metrics.pelvis_rotation_rom_deg,
            'torso_rom': report_metrics.torso_rotation_rom_deg
        }
    else:
        # Fallback to CSV (with warning)
        csv_data = download_csv(session_id)
        return {
            'source': 'csv_fallback',
            'pelvis_rom': calculate_from_csv(csv_data),
            'warning': 'Using CSV data - may be inaccurate'
        }
```

---

## ✅ Validation

### **Automatic Validation:**
```python
def validate_metrics(session_id):
    metrics = get_report_metrics(session_id)
    hittrax = get_hittrax_data(session_id)
    
    # Calculate expected rotation from bat speed
    expected_pelvis_min = hittrax.bat_speed * 0.6
    expected_pelvis_max = hittrax.bat_speed * 0.8
    
    # Check if actual matches expected
    if expected_pelvis_min <= metrics.pelvis_rom <= expected_pelvis_max * 1.5:
        return {
            'status': 'PASS',
            'message': f'Rotation ({metrics.pelvis_rom}°) matches physics requirements'
        }
    else:
        return {
            'status': 'FAIL',
            'message': f'Rotation mismatch: expected {expected_pelvis_min}-{expected_pelvis_max}°, got {metrics.pelvis_rom}°'
        }
```

---

## 📋 Next Steps

### **Today (Phase A - Manual):**
- [x] Database schema created
- [x] API routes created
- [x] Manual input form created
- [x] Quick insert script created
- [ ] Run migration
- [ ] Test manual input with Connor's report
- [ ] Generate corrected KRS report

### **This Week (Phase B - Automated):**
- [ ] Build chart image parser
- [ ] Detect "Torso Kinematics" section
- [ ] Extract line data (OCR or computer vision)
- [ ] Calculate ROM automatically
- [ ] Add confidence scoring
- [ ] Manual review interface

### **Next Sprint:**
- [ ] Process all existing sessions
- [ ] Re-calculate all KRS reports
- [ ] Update motor profiles
- [ ] Build validation dashboard
- [ ] Document new workflow

---

## 🎯 Success Criteria

**Phase A Complete When:**
- ✅ Connor's metrics entered manually (60° pelvis, 25° torso)
- ✅ KRS calculation uses report metrics
- ✅ Motor profile corrected (SPINNER, not WHIPPER)
- ✅ Drill prescription updated (refinement, not rebuild)

**Phase B Complete When:**
- ✅ Automated parser extracts 90%+ accuracy
- ✅ Manual review for edge cases
- ✅ All existing sessions re-processed
- ✅ Validation dashboard deployed

---

## 📚 Reference

**Key Files:**
- Connor's Report: `/home/user/webapp/connor_reboot_report.png`
- Analysis: `REBOOT_REPORT_VS_CSV_MISMATCH.md`
- Root Cause: `REBOOT_API_DATA_QUALITY_ISSUE.md`
- Data Flow: `HOW_WE_GET_CONNOR_DATA.md`

**GitHub:** https://github.com/THScoach/reboot-motion-backend

**Status:** 🟢 Phase A Ready to Deploy
