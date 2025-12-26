# 🎥 Player Video Upload - Testing Guide

## ✅ Production Status: **LIVE**

Production URL: **https://reboot-motion-backend-production.up.railway.app**

---

## 📹 Option 1: Browser Upload (Recommended)

### Step 1: Open the Coach Rick UI
**URL**: https://reboot-motion-backend-production.up.railway.app/coach-rick-ui

### Step 2: Upload Video
The UI provides a form to upload:
- **Video File**: Any swing video (MP4, MOV, AVI)
- **Player Name**: e.g., "John Smith"
- **Height**: inches (e.g., 72 for 6')
- **Weight**: pounds (e.g., 185)
- **Age**: years (e.g., 24)
- **Optional**: Bat weight, wingspan

### Step 3: Submit & Get Results
After upload, you'll receive:
- ✅ Motor Profile (Twister/Tilter/Hybrid/Spinner)
- ✅ Overall Score (0-100)
- ✅ Ground Flow Breakdown
- ✅ Engine Flow Breakdown
- ✅ Weapon Analysis
- ✅ Coach Rick's Commentary
- ✅ Personalized Training Recommendations

---

## 🔧 Option 2: API Testing via Swagger UI

### Step 1: Open Swagger UI
**URL**: https://reboot-motion-backend-production.up.railway.app/docs

### Step 2: Find the Endpoint
Look for: **POST /api/v1/reboot-lite/analyze-with-coach**

### Step 3: Click "Try it out"

### Step 4: Fill in the Form
- **video**: Click "Choose File" and select your swing video
- **player_name**: "Test Player"
- **height_inches**: 72
- **weight_lbs**: 185
- **age**: 24
- **player_id**: (optional) leave empty
- **bat_weight_oz**: 30
- **wingspan_inches**: (optional) leave empty

### Step 5: Execute
Click the blue "Execute" button to send the request.

### Step 6: View Response
Scroll down to see the JSON response with complete analysis.

---

## 💻 Option 3: Command Line (CURL)

If you have a video file on your computer:

```bash
curl -X POST "https://reboot-motion-backend-production.up.railway.app/api/v1/reboot-lite/analyze-with-coach" \
  -F "video=@/path/to/your/swing_video.mp4" \
  -F "player_name=John Smith" \
  -F "height_inches=72" \
  -F "weight_lbs=185" \
  -F "age=24" \
  -F "bat_weight_oz=30"
```

Replace `/path/to/your/swing_video.mp4` with actual video path.

---

## 📊 Expected Response Format

```json
{
  "player_info": {
    "player_name": "John Smith",
    "height_inches": 72,
    "weight_lbs": 185,
    "age": 24,
    "bat_weight_oz": 30
  },
  "motor_profile": {
    "type": "Spinner",
    "confidence": 0.85,
    "characteristics": [...],
    "match_percentage": 89
  },
  "overall_score": 75.4,
  "ground_flow": {
    "stance": 82,
    "load": 78,
    "stride": 75,
    "plant": 70
  },
  "engine_flow": {
    "pelvis_coil": 76,
    "hip_separation": 72,
    "torso_lag": 68,
    "sequencing": 80,
    "deceleration": 78
  },
  "weapon": {
    "bat_path": 71,
    "attack_angle": 69,
    "bat_speed": 85,
    "contact": 70
  },
  "tempo": {
    "load_time": 0.48,
    "launch_time": 0.15,
    "ratio": 3.2,
    "assessment": "Elite timing"
  },
  "coach_rick_messages": [
    {
      "message": "Your ground flow is solid...",
      "category": "strength",
      "priority": "high"
    }
  ],
  "analysis_id": "analysis_20251225_123456",
  "timestamp": "2025-12-25T12:34:56"
}
```

---

## 🎯 What Players Get

### 1. Motor Profile Classification
- **Type**: Twister, Tilter, Hybrid, or Spinner
- **Confidence Score**: How well you match the profile
- **Characteristics**: Key traits of your swing style
- **Strengths**: What you do well
- **Weaknesses**: What needs improvement

### 2. Overall Score (0-100)
Composite score based on:
- Ground Flow: 30%
- Engine Flow: 30%
- Weapon: 40%

### 3. Detailed Breakdown Scores
**Ground Flow** (Foundation):
- Stance positioning
- Load mechanics
- Stride efficiency
- Plant stability

**Engine Flow** (Power Generation):
- Pelvis coil
- Hip separation
- Torso lag
- Sequencing timing
- Deceleration control

**Weapon** (Bat Path & Contact):
- Bat path efficiency
- Attack angle
- Bat speed
- Contact quality

### 4. Tempo Analysis
- Load time (seconds)
- Launch time (seconds)
- Ratio assessment
- Timing quality

### 5. Coach Rick's Messages
- Personalized coaching commentary
- Strength identification
- Weakness analysis
- Training recommendations
- Drill suggestions

---

## 🧪 Quick Test Checklist

- [ ] Open Coach Rick UI: `/coach-rick-ui`
- [ ] Verify form displays correctly
- [ ] Upload test video
- [ ] Fill in player details
- [ ] Submit form
- [ ] Verify loading indicator appears
- [ ] Check response received
- [ ] Verify all scores displayed
- [ ] Read Coach Rick's messages
- [ ] Check motor profile classification
- [ ] Verify breakdown scores

---

## 🐛 Troubleshooting

### Issue: Form won't submit
- Check file size (max typically 100MB)
- Verify video format (MP4, MOV, AVI)
- Check all required fields filled

### Issue: "Service unavailable"
- Verify production URL is correct
- Check Railway dashboard for deployment status
- Wait 30 seconds and retry

### Issue: Analysis takes too long
- Video analysis typically takes 30-120 seconds
- Depends on video length and quality
- Be patient - AI processing in progress

### Issue: Error response
- Check error message in response
- Verify video file is valid
- Ensure all required fields provided
- Check Railway logs for details

---

## 📞 API Endpoints Reference

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Health check |
| `/docs` | GET | API documentation |
| `/coach-rick-ui` | GET | Video upload UI |
| `/api/v1/reboot-lite/analyze-with-coach` | POST | Video analysis |
| `/api/v1/reboot-lite/coach-rick/health` | GET | Coach Rick health |
| `/test-player` | GET | Test guide |

---

## ✅ Success Criteria

Upload is successful when you receive:
- ✅ HTTP 200 response
- ✅ analysis_id in response
- ✅ motor_profile with type
- ✅ overall_score value
- ✅ ground_flow scores
- ✅ engine_flow scores
- ✅ weapon scores
- ✅ coach_rick_messages array
- ✅ timestamp

---

## 🚀 Next Steps After Testing

1. **Frontend Integration**
   - Connect your frontend to the API
   - Use the response format to display results
   - Style the Coach Rick messages
   - Add loading states

2. **User Experience**
   - Add progress indicators during upload
   - Show analysis in progress message
   - Display results in clean UI
   - Save analysis history

3. **Whop Integration**
   - Check subscription status before analysis
   - Enforce tier limits (swings per month)
   - Track usage
   - Handle payment failures

4. **Production Monitoring**
   - Monitor Railway logs
   - Track API response times
   - Set up error alerts
   - Monitor success rates

---

## 📈 Analytics to Track

- Total video uploads
- Average analysis time
- Success rate
- Error types/frequency
- User engagement (viewing full results)
- Motor profile distribution
- Average scores by profile type

---

**Need Help?** Check the Railway logs at:
https://railway.app → reboot-motion-backend → Observability → Logs

**API Docs:** https://reboot-motion-backend-production.up.railway.app/docs

**GitHub:** https://github.com/THScoach/reboot-motion-backend
