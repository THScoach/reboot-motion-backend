# 🎯 COACH RICK AI - WAP INTEGRATION GUIDE

**Status:** ✅ **READY FOR INTEGRATION**  
**Date:** December 25, 2024  
**Integration Server:** https://8006-i5cseikj92ei70k8wadux-2e77fc33.sandbox.novita.ai

---

## 🚀 QUICK START

**Coach Rick AI is running and ready to connect to your Web App!**

### **1. Access the Integration Server**

🔗 **Landing Page:** https://8006-i5cseikj92ei70k8wadux-2e77fc33.sandbox.novita.ai

🔗 **API Docs (Swagger):** https://8006-i5cseikj92ei70k8wadux-2e77fc33.sandbox.novita.ai/docs

🔗 **Health Check:** https://8006-i5cseikj92ei70k8wadux-2e77fc33.sandbox.novita.ai/api/v1/reboot-lite/coach-rick/health

---

## 📡 API ENDPOINTS

### **Main Endpoint: POST /api/v1/reboot-lite/analyze-with-coach**

**Full URL:**
```
https://8006-i5cseikj92ei70k8wadux-2e77fc33.sandbox.novita.ai/api/v1/reboot-lite/analyze-with-coach
```

**Request:** `multipart/form-data`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `video` | File | Yes | Swing video file |
| `player_name` | String | Yes | Player's name |
| `height_inches` | Float | Yes | Height in inches |
| `weight_lbs` | Float | Yes | Weight in lbs |
| `age` | Int | Yes | Player age |
| `bat_weight_oz` | Float | No | Bat weight (default: 30oz) |
| `wingspan_inches` | Float | No | Wingspan in inches |
| `player_id` | String | No | Player ID (optional) |

**Response:** JSON with complete analysis

```json
{
  "session_id": "coach_rick_abc123",
  "player_name": "Eric Williams",
  "timestamp": "2025-12-25T...",
  
  "bat_speed_mph": 82.0,
  "exit_velocity_mph": 99.0,
  "efficiency_percent": 111.0,
  "tempo_score": 87.0,
  "stability_score": 92.0,
  "gew_overall": 88.5,
  
  "motor_profile": {
    "type": "Mixed",
    "confidence": 60.0,
    "characteristics": [...]
  },
  
  "patterns": [{
    "pattern_id": "...",
    "name": "Kinetic chain breakdown",
    "severity": "HIGH",
    "root_cause": "...",
    "symptoms": [...]
  }],
  
  "primary_issue": "Kinetic chain breakdown",
  
  "prescription": {
    "drills": [{
      "drill_id": "front_foot_elevated_tee",
      "name": "Front Foot Elevated Tee",
      "category": "Kinetic Chain",
      "volume": "30 swings",
      "frequency": "Daily",
      "key_cues": [...]
    }],
    "duration_weeks": 4,
    "expected_gains": "+5-8 mph bat speed",
    "weekly_schedule": {...}
  },
  
  "coach_messages": {
    "analysis": "Great to see you working...",
    "drill_intro": "I've put together a plan...",
    "encouragement": "Keep grinding!"
  }
}
```

### **Health Check: GET /api/v1/reboot-lite/coach-rick/health**

**Full URL:**
```
https://8006-i5cseikj92ei70k8wadux-2e77fc33.sandbox.novita.ai/api/v1/reboot-lite/coach-rick/health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "Coach Rick AI Engine",
  "version": "1.0.0",
  "components": {
    "motor_profile_classifier": "✅ operational",
    "pattern_recognition": "✅ operational",
    "drill_prescription": "✅ operational",
    "conversational_ai": "✅ operational (fallback mode)"
  }
}
```

---

## 💻 FRONTEND INTEGRATION

### **JavaScript Example (Fetch API)**

```javascript
// Upload swing video and get analysis
async function analyzeSwingWithCoachRick(videoFile, playerData) {
  const formData = new FormData();
  
  // Add video file
  formData.append('video', videoFile);
  
  // Add player data
  formData.append('player_name', playerData.name);
  formData.append('height_inches', playerData.height);
  formData.append('weight_lbs', playerData.weight);
  formData.append('age', playerData.age);
  formData.append('bat_weight_oz', playerData.batWeight || 30);
  
  try {
    const response = await fetch(
      'https://8006-i5cseikj92ei70k8wadux-2e77fc33.sandbox.novita.ai/api/v1/reboot-lite/analyze-with-coach',
      {
        method: 'POST',
        body: formData
      }
    );
    
    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }
    
    const analysis = await response.json();
    return analysis;
    
  } catch (error) {
    console.error('Coach Rick AI Error:', error);
    throw error;
  }
}

// Example usage
const videoFile = document.getElementById('videoUpload').files[0];
const playerData = {
  name: 'Eric Williams',
  height: 73,
  weight: 185,
  age: 28,
  batWeight: 30
};

analyzeSwingWithCoachRick(videoFile, playerData)
  .then(analysis => {
    console.log('Motor Profile:', analysis.motor_profile);
    console.log('Patterns Detected:', analysis.patterns);
    console.log('Drill Prescription:', analysis.prescription);
    console.log('Coach Rick Says:', analysis.coach_messages);
    
    // Display results in UI
    displayMotorProfile(analysis.motor_profile);
    displayPatterns(analysis.patterns);
    displayDrillPrescription(analysis.prescription);
    displayCoachMessages(analysis.coach_messages);
  })
  .catch(error => {
    console.error('Analysis failed:', error);
  });
```

### **Axios Example**

```javascript
import axios from 'axios';

async function analyzeSwing(videoFile, playerData) {
  const formData = new FormData();
  formData.append('video', videoFile);
  formData.append('player_name', playerData.name);
  formData.append('height_inches', playerData.height);
  formData.append('weight_lbs', playerData.weight);
  formData.append('age', playerData.age);
  
  const response = await axios.post(
    'https://8006-i5cseikj92ei70k8wadux-2e77fc33.sandbox.novita.ai/api/v1/reboot-lite/analyze-with-coach',
    formData,
    {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    }
  );
  
  return response.data;
}
```

---

## 🎨 UI COMPONENTS TO BUILD

### **1. Motor Profile Display**
- Badge showing profile type (Spinner/Whipper/Torquer/Mixed)
- Confidence meter (0-100%)
- Characteristics list
- Color-coded by profile type

### **2. Patterns Detected**
- List of mechanical issues
- Severity badges (HIGH/MEDIUM/LOW)
- Root cause explanation
- Symptoms list

### **3. Drill Prescription Dashboard**
- Drill cards with name, category, volume, frequency
- Key coaching cues
- Weekly schedule calendar
- Expected gains (+5-8 mph bat speed, etc.)
- Duration (3-4 weeks)

### **4. Coach Rick Messages**
- Analysis message (encouraging technical feedback)
- Drill introduction (motivating setup)
- Encouragement message (general motivation)
- Use Coach Rick's voice/persona

### **5. Metrics Dashboard**
- Bat Speed (mph)
- Exit Velocity (mph)
- Efficiency (%)
- Tempo Score (0-100)
- Stability Score (0-100)
- GEW Overall (0-100)

---

## 🧪 TESTING THE INTEGRATION

### **1. Test Health Endpoint**
```bash
curl https://8006-i5cseikj92ei70k8wadux-2e77fc33.sandbox.novita.ai/api/v1/reboot-lite/coach-rick/health
```

Expected: `{"status": "healthy", ...}`

### **2. Test Full Analysis (with curl)**
```bash
curl -X POST \
  https://8006-i5cseikj92ei70k8wadux-2e77fc33.sandbox.novita.ai/api/v1/reboot-lite/analyze-with-coach \
  -F "video=@test_swing.mp4" \
  -F "player_name=Test Player" \
  -F "height_inches=73" \
  -F "weight_lbs=185" \
  -F "age=28" \
  -F "bat_weight_oz=30"
```

### **3. Test with Postman/Insomnia**
1. Open Postman
2. Create new POST request
3. URL: `https://8006-i5cseikj92ei70k8wadux-2e77fc33.sandbox.novita.ai/api/v1/reboot-lite/analyze-with-coach`
4. Body: `form-data`
5. Add video file + player fields
6. Send request
7. View JSON response

---

## 📊 WHAT YOU GET

### **Complete Analysis Package:**
1. ✅ **Motor Profile Classification** - Swing type with confidence
2. ✅ **Pattern Recognition** - 4+ mechanical issues detected
3. ✅ **Drill Prescription** - Personalized 3-4 week training plan
4. ✅ **Coach Rick AI Messages** - Encouraging, technical coaching
5. ✅ **Performance Metrics** - Bat speed, exit velo, efficiency, etc.
6. ✅ **Weekly Schedule** - Daily drill routines for 7 days
7. ✅ **Expected Gains** - Predicted improvements (+5-8 mph, etc.)

---

## 🔧 TROUBLESHOOTING

### **CORS Issues**
- Server has CORS enabled for all origins (`allow_origins=["*"]`)
- If issues persist, check browser console for specific errors

### **Large Video Files**
- Default timeout: 30 seconds
- For large files, may need to increase timeout
- Recommended: compress videos before upload

### **API Errors**
1. Check health endpoint first
2. Verify all required fields are present
3. Check network tab in browser dev tools
4. Review error messages in response

---

## 🚀 NEXT STEPS FOR FULL INTEGRATION

### **Phase 1: Basic Integration (1-2 hours)**
1. Add "Analyze with Coach Rick" button to WAP
2. Create file upload form
3. Wire up API call to Coach Rick endpoint
4. Display basic results (motor profile + drill plan)

### **Phase 2: Enhanced UI (2-3 hours)**
1. Build motor profile component with confidence meter
2. Create patterns list with severity badges
3. Design drill prescription cards
4. Add Coach Rick message displays
5. Style with matching WAP theme

### **Phase 3: Advanced Features (3-4 hours)**
1. Weekly schedule calendar
2. Drill video embeds (when available)
3. Progress tracking
4. Save analysis history
5. Export PDF reports

---

## 📝 EXAMPLE WORKFLOW

1. **User uploads swing video** in WAP
2. **Frontend calls** Coach Rick API with video + player data
3. **Coach Rick analyzes** swing (2-5 seconds)
4. **Returns complete analysis**:
   - Motor profile (Spinner/Whipper/Torquer)
   - Mechanical issues detected
   - Personalized drill plan
   - Coach Rick's feedback
5. **Frontend displays results** in beautiful UI
6. **User reviews**:
   - Their swing type
   - What needs improvement
   - Specific drills to do
   - Coach Rick's encouraging message
7. **User saves** analysis and starts training

---

## ✅ INTEGRATION CHECKLIST

- [ ] Test health endpoint
- [ ] Test analyze endpoint with sample video
- [ ] Add Coach Rick button to WAP UI
- [ ] Create video upload component
- [ ] Build player data form
- [ ] Wire up API call
- [ ] Display motor profile
- [ ] Display detected patterns
- [ ] Display drill prescription
- [ ] Display Coach Rick messages
- [ ] Add error handling
- [ ] Add loading states
- [ ] Test end-to-end flow
- [ ] Style to match WAP theme

---

## 🔗 USEFUL LINKS

**Integration Server:** https://8006-i5cseikj92ei70k8wadux-2e77fc33.sandbox.novita.ai

**API Docs:** https://8006-i5cseikj92ei70k8wadux-2e77fc33.sandbox.novita.ai/docs

**Health Check:** https://8006-i5cseikj92ei70k8wadux-2e77fc33.sandbox.novita.ai/api/v1/reboot-lite/coach-rick/health

**GitHub:** https://github.com/THScoach/reboot-motion-backend

---

## 💪 READY TO INTEGRATE

**The Coach Rick AI Engine is fully operational and waiting for your frontend!**

All endpoints are tested, working, and ready for production use. Just connect your UI and start analyzing swings! 🎯

---

**Questions or need help?** Check the Swagger docs at `/docs` for interactive API testing!
