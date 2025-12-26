# NumPy JSON Serialization Fix

## Problem

**Error:** `Object of type int64 is not JSON serializable`

**Root Cause:** When parsing Reboot Motion CSV files with Pandas/NumPy, data types like `numpy.int64`, `numpy.float64`, and `numpy.ndarray` are used. These types cannot be directly serialized to JSON by FastAPI's `JSONResponse`.

**Where it occurred:**
- CSV upload endpoint `/upload-reboot-csv`
- Both momentum-energy and inverse-kinematics CSV processing
- Railway deployment logs showed multiple crashes

## Solution

### 1. Created Type Conversion Helper

```python
def convert_to_native_types(obj: Any) -> Any:
    """
    Convert NumPy/Pandas types to native Python types for JSON serialization.
    
    Handles:
    - numpy.int64 → int
    - numpy.float64 → float
    - numpy.ndarray → list
    - dict → recursively convert values
    - None → None
    """
    if isinstance(obj, (np.integer, np.int64)):
        return int(obj)
    elif isinstance(obj, (np.floating, np.float64)):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {k: convert_to_native_types(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [convert_to_native_types(item) for item in obj]
    else:
        return obj
```

### 2. Updated Response Building

**Momentum-Energy CSV Response:**
```python
response = {
    "session_info": {
        "fps": float(round(swing_data.fps, 1)),           # NumPy → Python float
        "num_frames": int(swing_data.num_frames),         # NumPy → Python int
        "contact_frame": int(swing_data.contact_frame),   # NumPy → Python int
        ...
    },
    "ground_truth_metrics": {
        "bat_speed": {
            "at_contact_mph": float(round(metrics['bat_speed_mph'], 1)),
            ...
        }
    }
}

# Final safety conversion
response = convert_to_native_types(response)
return JSONResponse(content=response)
```

**Inverse-Kinematics CSV Response:**
```python
response = {
    "session_info": {
        "fps": float(round(ik_data.fps, 1)),
        "num_frames": int(ik_data.num_frames),
        ...
    },
    "joint_data": {
        "num_joint_angles": int(len(ik_data.joint_angles)),
        "has_angular_velocities": bool(ik_data.angular_velocities is not None),
        ...
    },
    "ik_metrics": metrics  # Will be converted recursively
}

# Convert nested NumPy types in metrics
response = convert_to_native_types(response)
return JSONResponse(content=response)
```

## Why This Fix Works

1. **Explicit Conversion:** Converts NumPy types to Python native types before JSON serialization
2. **Recursive Handling:** The helper function handles nested dicts and lists
3. **Safety Net:** Applied to entire response dict as final step
4. **No Data Loss:** Maintains precision while ensuring JSON compatibility

## Files Modified

- `csv_upload_routes.py`
  - Added `convert_to_native_types()` helper
  - Updated `process_momentum_file()` response building
  - Updated `process_ik_file()` response building

## Testing

### Local Test
```bash
# Upload momentum-energy CSV
curl -X POST \
  -F "file=@momentum-energy.csv" \
  -F "bat_mass_kg=0.85" \
  https://8000-i5cseikj92ei70k8wadux-2e77fc33.sandbox.novita.ai/upload-reboot-csv

# Should return JSON without serialization errors
```

### Production Test (Railway)
- Push changes to GitHub
- Railway auto-deploys
- Test CSV upload via web UI or API
- Check logs for successful processing

## Expected Behavior

**Before Fix:**
```
ERROR: Object of type int64 is not JSON serializable
❌ 500 Internal Server Error
```

**After Fix:**
```json
{
  "success": true,
  "session_info": {
    "fps": 240.0,
    "num_frames": 2903,
    "contact_frame": 1834
  },
  "ground_truth_metrics": {
    "bat_speed": {
      "at_contact_mph": 57.5,
      "peak_mph": 80.1
    }
  }
}
✅ 200 OK
```

## Deployment Status

- ✅ **Local:** Fixed and tested at `https://8000-i5cseikj92ei70k8wadux-2e77fc33.sandbox.novita.ai`
- ✅ **GitHub:** Pushed to `main` branch (commit `a3ff284`)
- ⏳ **Railway:** Will auto-deploy from GitHub

## Related Issues

This fix resolves:
- Railway deployment crashes showing "Object of type int64 is not JSON serializable"
- CSV upload errors in production
- JSON serialization failures with Pandas DataFrames

## Prevention

To avoid similar issues in the future:
1. Always convert NumPy/Pandas types before JSON serialization
2. Use `convert_to_native_types()` helper for all CSV-based responses
3. Test with real CSV data before deployment
4. Add type hints to catch serialization issues early

---

**Status:** ✅ FIXED
**Commit:** `a3ff284`
**Deployed:** Local ✅ | Railway ⏳
