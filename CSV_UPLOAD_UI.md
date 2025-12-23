# 📂 CSV Upload UI - Complete!

## ✅ What Was Added

I've added a **beautiful tabbed interface** to the web app that allows users to choose between:
1. **📹 Video Analysis** - Upload swing videos (existing feature)
2. **📂 CSV Import** - Upload Reboot Motion CSV files (NEW!)

---

## 🎨 UI Features

### Tabbed Interface
- Clean tab switching between Video Analysis and CSV Import
- Active tab highlighting with purple underline
- Smooth transitions
- Consistent design with existing purple gradient theme

### CSV Upload Tab

#### Upload Section
- **File input**: Accept `.csv` files only
- **Athlete name**: Optional text input (CSV doesn't contain name)
- **Bat mass**: Number input with default 0.85 kg (33"/30oz bat)
- **Help text**: Explains each field clearly

#### Results Display
Beautiful metric cards showing:

**Session Info Card**
- Session ID
- Athlete name
- FPS and duration
- Total frames
- Contact frame and time

**Bat Speed Card**
- At contact (mph)
- Peak (mph)

**Energy Distribution Card**
- Total energy (Joules)
- Lower half percentage
- Torso percentage
- Arms percentage

**Kinematic Sequence Card**
- Time before contact for each segment
- Pelvis, Torso, Left Arm, Right Arm, Bat

**Tempo Card**
- Tempo ratio (e.g., 3.38:1)
- Load duration (ms)
- Swing duration (ms)

**Full JSON View**
- Collapsible `<details>` section
- Complete API response for developers

---

## 🌐 Access the Web App

**URL**: https://8000-i5cseikj92ei70k8wadux-2e77fc33.sandbox.novita.ai

### How to Use

#### Option 1: Video Analysis (Existing)
1. Click "📹 Video Analysis" tab
2. Upload a swing video
3. Fill in athlete details
4. Click "Analyze Video"
5. Wait 30-60 seconds
6. View results

#### Option 2: CSV Import (NEW!)
1. Click "📂 CSV Import" tab
2. Upload a momentum-energy.csv file
3. Enter athlete name (optional)
4. Adjust bat mass if needed (default 0.85 kg)
5. Click "Import CSV"
6. Results appear instantly (<1 second)

---

## 📊 Example CSV Results

When you upload a CSV, you'll see beautiful metric cards like this:

```
📊 Ground Truth Metrics

┌─ SESSION INFO ──────────────────────────────┐
│ Session ID:  ad25f0a5-d0d6-48bd-...        │
│ Athlete:     Connor Gray                    │
│ FPS:         240.0                          │
│ Duration:    2.66s (1234 frames)            │
│ Contact:     Frame 1022 (0.900s)            │
└─────────────────────────────────────────────┘

┌─ BAT SPEED ─────────────────────────────────┐
│ At Contact:  57.5 mph                       │
│ Peak:        80.1 mph                       │
└─────────────────────────────────────────────┘

┌─ ENERGY DISTRIBUTION (at contact) ──────────┐
│ Total:       2305 J                         │
│ Lower Half:  61.0%                          │
│ Torso:       29.0%                          │
│ Arms:        15.0%                          │
└─────────────────────────────────────────────┘

┌─ KINEMATIC SEQUENCE (ms before contact) ────┐
│ Pelvis:      17 ms                          │
│ Torso:       4 ms                           │
│ Larm:        58 ms                          │
│ Rarm:        45 ms                          │
│ Bat:         0 ms                           │
└─────────────────────────────────────────────┘

┌─ TEMPO (estimated) ─────────────────────────┐
│ Ratio:           3.38:1                     │
│ Load Duration:   1579 ms                    │
│ Swing Duration:  467 ms                     │
└─────────────────────────────────────────────┘
```

---

## 💻 Technical Details

### Frontend (JavaScript)
- Async form submission with `fetch` API
- Loading states with animated spinner
- Error handling with user-friendly messages
- Dynamic metric card generation
- Collapsible JSON view with `<details>`

### Backend (Python/FastAPI)
- `POST /upload-reboot-csv` endpoint
- Multipart form data handling
- CSV parsing with pandas
- Ground truth calculation
- JSON response with metrics

### Styling
- Purple gradient theme (matches existing)
- Card-based layout for metrics
- Responsive design
- Hover effects and transitions
- Clean typography

---

## 🧪 Testing the Feature

### Quick Test
1. Go to https://8000-i5cseikj92ei70k8wadux-2e77fc33.sandbox.novita.ai
2. Click "📂 CSV Import" tab
3. You should see:
   - File upload input
   - Athlete name field
   - Bat mass field (default 0.85)
   - Blue info box explaining the feature
   - "Import CSV" button

### Full Test (with CSV file)
1. Export a momentum-energy CSV from Reboot Motion
2. Go to the CSV Import tab
3. Upload the file
4. Enter athlete name (e.g., "Connor Gray")
5. Click "Import CSV"
6. Within 1 second, you should see:
   - 5 metric cards with data
   - Collapsible JSON view
   - All values populated correctly

---

## 📁 Files Modified

**Updated**:
- `templates/index.html` - Added CSV upload tab and metric display

**Created Previously**:
- `reboot_csv_importer.py` - CSV parsing logic
- `csv_upload_routes.py` - FastAPI endpoints
- `CSV_IMPORT_FEATURE.md` - Documentation
- `test_csv_upload.py` - Test script

---

## 🎯 Use Cases

### 1. **API Fallback**
When Reboot Motion API is down:
- Switch to CSV Import tab
- Upload CSV file
- Get instant results

### 2. **Ground Truth Validation**
Compare video analysis vs CSV data:
- Analyze video in Video tab
- Import corresponding CSV in CSV tab
- Compare metrics side-by-side

### 3. **Offline Development**
Work without API credentials:
- Use CSV files exported earlier
- Test physics engine calculations
- Validate against ground truth

### 4. **Historical Data**
Process archived CSV files:
- Upload old CSV exports
- Get updated metrics
- Track athlete progress over time

---

## 🚀 What's Next

### Potential Enhancements
- [ ] Side-by-side comparison (Video vs CSV)
- [ ] Batch CSV upload (multiple files)
- [ ] CSV data visualization (charts/graphs)
- [ ] Export comparison report
- [ ] Save results to database
- [ ] Download sample CSV template

---

## ✅ Summary

**What Users Can Now Do**:
1. ✅ Switch between Video Analysis and CSV Import tabs
2. ✅ Upload Reboot Motion momentum-energy CSV files
3. ✅ View beautiful metric cards with ground truth data
4. ✅ See bat speed, energy distribution, kinematic sequence, tempo
5. ✅ Expand full JSON response for details
6. ✅ Get instant results (<1 second processing)

**When to Use CSV Import**:
- 🔴 Reboot Motion API unavailable
- 🔴 Need ground truth for validation
- 🔴 Offline development/testing
- 🔴 Processing historical data

**Endpoints Used**:
- `POST /upload-reboot-csv` - CSV processing
- `POST /analyze` - Video analysis (existing)

**Status**: ✅ **Live and Ready!**

**URL**: https://8000-i5cseikj92ei70k8wadux-2e77fc33.sandbox.novita.ai

---

**Result**: Users now have a **beautiful, intuitive interface** for uploading Reboot Motion CSV files and instantly viewing ground truth biomechanics data! 🎉
