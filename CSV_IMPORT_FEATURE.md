# 📂 Reboot Motion CSV Import Feature

## Overview

This feature provides a **fallback mechanism** for importing Reboot Motion biomechanics data when the API is unavailable, slow, or rate-limited. Users can upload CSV files exported directly from Reboot Motion to get ground truth metrics instantly.

---

## 🎯 Use Cases

### When to Use CSV Import

1. **API Downtime**: Reboot Motion API is unavailable
2. **Rate Limiting**: Hit API request limits
3. **Offline Development**: Testing without API credentials
4. **Data Archive**: Working with historical CSV exports
5. **Faster Processing**: Bypass API latency for large datasets

---

## 📋 Supported File Types

### 1. Momentum-Energy CSV ✅
**Filename Pattern**:
```
YYYYMMDD_session_N_rebootmotion_{UUID}_baseball-hitting_momentum-energy.csv
```

**Example**:
```
20251220_session_3_rebootmotion_ad25f0a5-d0d6-48bd-871c-f3d2a78e1576_baseball-hitting_momentum-energy.csv
```

**Contains**:
- 344 columns of biomechanics data
- Angular momentum (bat, pelvis, torso, arms)
- Kinetic energy (total, segments)
- Time series (240-480 FPS typical)
- Contact point detection (`time_from_max_hand`)

### 2. Inverse-Kinematics CSV 🚧
**Status**: Coming soon
**Will contain**:
- Joint angles (3D)
- Joint positions (x, y, z)
- Segment velocities
- Full skeleton tracking

---

## 🔧 API Usage

### Endpoint
```
POST /upload-reboot-csv
```

### Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `file` | File | ✅ Yes | - | CSV file (momentum-energy or IK) |
| `bat_mass_kg` | float | ❌ No | 0.85 | Bat mass in kg (33"/30oz = 0.85kg) |
| `athlete_name` | string | ❌ No | null | Athlete name (not in CSV) |

### Example: cURL
```bash
curl -X POST \
  -F "file=@momentum-energy.csv" \
  -F "bat_mass_kg=0.85" \
  -F "athlete_name=Connor Gray" \
  http://localhost:8000/upload-reboot-csv
```

### Example: Python
```python
import requests

url = "http://localhost:8000/upload-reboot-csv"

files = {
    'file': open('momentum-energy.csv', 'rb')
}

data = {
    'bat_mass_kg': 0.85,
    'athlete_name': 'Connor Gray'
}

response = requests.post(url, files=files, data=data)
print(response.json())
```

### Example: JavaScript
```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);
formData.append('bat_mass_kg', '0.85');
formData.append('athlete_name', 'Connor Gray');

fetch('http://localhost:8000/upload-reboot-csv', {
  method: 'POST',
  body: formData
})
.then(res => res.json())
.then(data => console.log(data));
```

---

## 📊 Response Format

### Success Response (200)
```json
{
  "success": true,
  "message": "CSV file processed successfully",
  "session_info": {
    "session_id": "ad25f0a5-d0d6-48bd-871c-f3d2a78e1576",
    "athlete_name": "Connor Gray",
    "movement_type": "baseball-hitting",
    "fps": 240.0,
    "duration_s": 2.66,
    "num_frames": 1234,
    "contact_frame": 1022,
    "contact_time_s": 0.900
  },
  "ground_truth_metrics": {
    "bat_speed": {
      "at_contact_mph": 57.5,
      "peak_mph": 80.1
    },
    "energy_distribution": {
      "total_j": 2305,
      "lowerhalf_pct": 61.0,
      "torso_pct": 29.0,
      "arms_pct": 15.0
    },
    "kinematic_sequence_ms_before_contact": {
      "pelvis": 17,
      "torso": 4,
      "larm": 58,
      "rarm": 45,
      "bat": 0
    },
    "tempo_estimated": {
      "ratio": 3.38,
      "load_duration_ms": 1579,
      "swing_duration_ms": 467
    }
  }
}
```

### Error Responses

#### 400 - Invalid File Type
```json
{
  "detail": "File must be a CSV"
}
```

#### 400 - Not a Reboot Motion File
```json
{
  "detail": "File must be a Reboot Motion export (filename should contain 'rebootmotion' or 'momentum')"
}
```

#### 500 - Processing Error
```json
{
  "detail": "Error processing CSV: Required column not found. Tried: ['bat_angular_momentum_mag', 'bat_angmom_mag']"
}
```

---

## 🧮 Calculated Metrics

### 1. Bat Speed
**Formula**: `v = sqrt(2 * KE / m) * 2.237`

Where:
- `KE` = Bat kinetic energy at contact (Joules)
- `m` = Bat mass (kg)
- `2.237` = Conversion factor (m/s → mph)

**Returns**:
- `at_contact_mph`: Speed at detected contact point
- `peak_mph`: Maximum speed in dataset (may include artifacts)

**Validation**:
- High School: 55-70 mph
- College: 65-80 mph
- MLB: 70-85 mph

### 2. Energy Distribution
**Calculated at contact frame**

**Formula**: `pct = (segment_KE / total_KE) * 100`

**Optimal Ranges**:
- Lower Half: 55-65%
- Torso: 25-35%
- Arms: 10-20%

### 3. Kinematic Sequence
**Method**: Find peak angular momentum for each segment before contact

**Reports**: Time (ms) before contact that each segment peaked

**Optimal Sequence**:
1. Pelvis/Lower Half (30-50ms before)
2. Torso (20-30ms before)
3. Arms (10-20ms before)
4. Bat (0ms = contact)

**Gaps**: Should be 10-40ms between sequential peaks

### 4. Tempo (Estimated)
**Method**: Simplified estimation based on time windows

**Formula**: `tempo = load_duration / swing_duration`

Where:
- Load phase: -2.0s to -0.5s before contact
- Swing phase: -0.5s to contact

**Note**: This is an estimate. Actual tempo requires event detection from video.

**Optimal Range**: 2.0-3.5

---

## 🔍 Column Mapping

The importer intelligently searches for columns by multiple names:

### Bat Data
| Metric | Possible Column Names |
|--------|---------------------|
| Angular Momentum | `bat_angular_momentum_mag`, `bat_angmom_mag`, `bat_angular_momentum` |
| Kinetic Energy | `bat_kinetic_energy`, `bat_ke`, `bat_energy` |
| Position X | `bat_x` |
| Position Y | `bat_y` |
| Position Z | `bat_z` |

### Body Segments
| Segment | Possible Column Names |
|---------|---------------------|
| Pelvis | `pelvis_angular_momentum_mag`, `pelvis_angmom_mag`, `lowertorso_angular_momentum_mag` |
| Torso | `torso_angular_momentum_mag`, `torso_angmom_mag` |
| Left Arm | `larm_angular_momentum_mag`, `larm_angmom_mag`, `left_arm_angular_momentum_mag` |
| Right Arm | `rarm_angular_momentum_mag`, `rarm_angmom_mag`, `right_arm_angular_momentum_mag` |

### Energy
| Type | Possible Column Names |
|------|---------------------|
| Total | `total_kinetic_energy`, `total_ke`, `total_energy` |
| Lower Half | `lowerhalf_kinetic_energy`, `legs_kinetic_energy`, `lower_half_ke` |
| Torso | `torso_kinetic_energy`, `torso_ke` |
| Arms | `arms_kinetic_energy`, `arms_ke` |

---

## 📝 File Requirements

### Must Have Columns
1. `time` - Timestamp in seconds
2. `time_from_max_hand` - Time relative to contact
3. `bat_angular_momentum_mag` (or equivalent)
4. `bat_kinetic_energy` (or equivalent)
5. `total_kinetic_energy` (or equivalent)
6. Segment angular momentum columns

### Optional Columns
- `bat_x`, `bat_y`, `bat_z` - Bat position
- Energy breakdown by segment
- Additional biomechanics data

---

## 🚀 Integration with Physics Engine

### Use Case: Validate Physics Calculations

```python
# 1. Upload CSV to get ground truth
response = upload_csv("connor_gray.csv", bat_mass_kg=0.85)
ground_truth = response['ground_truth_metrics']

# 2. Process video with physics engine
video_results = analyze_video("connor_gray.mov")

# 3. Compare results
comparison = {
    'bat_speed': {
        'ground_truth': ground_truth['bat_speed']['at_contact_mph'],
        'calculated': video_results['bat_speed_mph'],
        'error_pct': calculate_error(...)
    },
    'tempo': {
        'ground_truth': ground_truth['tempo_estimated']['ratio'],
        'calculated': video_results['tempo_ratio'],
        'error_pct': calculate_error(...)
    }
}
```

---

## 🧪 Testing the Feature

### 1. Get Info Endpoint
```bash
curl http://localhost:8000/csv-upload-info
```

Returns documentation about the feature.

### 2. Test Import
Save a sample CSV and upload:
```bash
curl -X POST \
  -F "file=@test_momentum.csv" \
  http://localhost:8000/upload-reboot-csv
```

### 3. Validate Results
Check response includes:
- ✅ Session info parsed from filename
- ✅ Ground truth metrics calculated
- ✅ All expected fields present
- ✅ Values in realistic ranges

---

## 🔒 Security Considerations

### Validations Performed
1. ✅ File extension must be `.csv`
2. ✅ Filename must contain `rebootmotion` or `momentum`
3. ✅ Required columns must be present
4. ✅ File saved to temporary directory (auto-deleted)
5. ✅ Maximum file size enforced by FastAPI

### File Size Limits
- Typical momentum-energy CSV: 5-10 MB
- Recommended max: 50 MB
- Can be configured in FastAPI settings

---

## 📈 Performance

### Processing Time
| File Size | Frames | Processing Time |
|-----------|--------|-----------------|
| 5 MB | 1,234 | ~0.5 seconds |
| 10 MB | 2,903 | ~1.0 seconds |
| 20 MB | 5,000+ | ~2.0 seconds |

### Memory Usage
- Pandas DataFrame: ~2-3x file size in RAM
- Peak memory: ~30-50 MB for typical files
- Temporary file: Deleted immediately after processing

---

## 🛠️ Troubleshooting

### "Required column not found"
**Problem**: CSV format doesn't match expected structure

**Solution**: Check column names in CSV. The importer tries multiple variations, but non-standard exports may fail.

### "File must be a Reboot Motion export"
**Problem**: Filename validation failed

**Solution**: Ensure filename contains `rebootmotion` or `momentum`. Rename if needed:
```bash
mv myfile.csv rebootmotion_myfile.csv
```

### "Error processing CSV"
**Problem**: Data parsing failed

**Solution**: 
1. Open CSV in text editor, check for corruption
2. Ensure CSV has header row
3. Verify numeric columns contain valid numbers

---

## 📚 Future Enhancements

### Planned Features
- [ ] Inverse-kinematics CSV support
- [ ] Batch CSV upload (multiple files)
- [ ] CSV export of calculated metrics
- [ ] Comparison view (CSV vs Video analysis)
- [ ] Store CSV data in database
- [ ] Download sample CSV template

---

## 📖 API Documentation

The feature is automatically documented in:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

Look for the **"CSV Import"** tag.

---

## ✅ Summary

**What It Does**:
- Parses Reboot Motion CSV files (momentum-energy format)
- Calculates ground truth biomechanics metrics
- Provides instant results without API calls

**When To Use**:
- API unavailable/slow/rate-limited
- Need ground truth for validation
- Testing/development without API credentials

**Benefits**:
- Instant processing (sub-second)
- No API dependencies
- Direct access to Reboot Motion data
- Perfect for validation & comparison

**Endpoints**:
- `POST /upload-reboot-csv` - Upload and process CSV
- `GET /csv-upload-info` - Feature documentation

---

**Status**: ✅ Implemented and tested  
**Version**: 1.0  
**Last Updated**: December 23, 2025
