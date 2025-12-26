# 🎯 CATCHING BARRELS — WHAT YOU HAVE & WHAT YOU NEED

**Date**: 2025-12-22  
**Coach**: Rick  
**Developer**: Claude  
**Status**: Backend Complete → Physics Engine Next

---

## 📊 WHAT YOU HAVE RIGHT NOW (COMPLETE ✅)

### 1. **Reboot Motion Backend API** (LIVE & WORKING)
- **URL**: `https://reboot-motion-backend-production.up.railway.app`
- **Status**: ✅ Production-Ready
- **Database**: PostgreSQL on Railway
- **Authentication**: OAuth 2.0 with Reboot Motion API
- **Auto-Deploy**: Every git push → Railway redeploy

#### Current Data:
- **100 Athletes** (synced from Reboot Motion)
- **110 Session Records** (10 unique hitting sessions × ~11 players each)
- **0 Biomechanics Records** (ready to implement)

#### API Endpoints Working:
```
GET  /players                  → All athletes
GET  /players/{id}             → Single athlete
GET  /players/{id}/sessions    → Athlete's sessions
GET  /sessions/{id}            → Session details
GET  /sessions/{id}/data       → Session biomechanics (when implemented)
GET  /sessions/{id}/metrics    → Session metrics (when implemented)
POST /sync/trigger             → Manual sync with Reboot Motion
GET  /sync/status              → Sync status
GET  /stats                    → System statistics
GET  /docs                     → Interactive API documentation
```

#### GitHub Repo:
- **Repository**: `https://github.com/THScoach/reboot-motion-backend`
- **Branch**: `main`
- **Auto-Deploy**: Enabled to Railway

---

## 🎥 WHAT YOU UPLOADED (YOUR VIDEOS)

### Video Files Available:
```
1. 131215-Hitting.mov    (Your swing #1)
2. 131151-Hitting.mov    (Your swing #2)
3. 131233-Hitting.mov    (Your swing #3)
4. 131200-Hitting.mov    (Your swing #4)
5. 131301-Hitting.mov    (Your swing #5)
6. 340109 (1).mp4        (Shohei Ohtani - requested 300fps)
7. 340109 (2).mp4        (Shohei Ohtani - requested 300fps)
8. 340109 (3).mp4        (Shohei Ohtani - requested 300fps)
```

**Location**: `/home/user/uploaded_files/`

---

## 🎯 WHAT YOU WANT TO BUILD (YOUR VISION)

### **THE PRODUCT**: Kinetic Blueprint Assessment
**Price**: $299  
**What It Does**: Automated 2-hour assessment → Lab Report in Coach Rick's voice

### **The Physics Engine** (CORE FEATURE)
Takes a video of a baseball swing and produces:

#### **Outputs** (From Your Spec):
1. **Tempo Ratio** (Load Duration / Launch Duration)
   - IDEAL: 2.5-3.0:1
   - GOOD: 2.0-2.5:1 or 3.0-3.5:1
   - FOCUS_AREA: <2.0:1 or >3.5:1

2. **Ground Score** (0-100)
   - Weight transfer
   - Leg drive
   - Ground reaction force (via COM acceleration)

3. **Engine Score** (0-100)
   - Hip rotation speed
   - Hip-shoulder separation
   - Sequence timing (pelvis peaks before torso)

4. **Weapon Score** (0-100)
   - Bat speed at contact
   - Hand path efficiency
   - Bat lag angle

5. **Transfer Ratio** (Energy Transfer)
   - Bat Momentum at Contact / Pelvis Peak Momentum
   - ELITE: ≥1.20
   - STRONG: 1.00-1.19
   - AVERAGE: 0.80-0.99
   - FOCUS_AREA: <0.80

6. **Motor Profile** (Movement Pattern)
   - SPINNER (rotation dominant)
   - SLINGSHOTTER (weight transfer dominant)
   - WHIPPER (bat speed dominant)
   - TITAN modifier (for athletes ≥90kg with high Ground Score)

7. **Pro Player Comparison**
   - Matches athlete to MLB players with similar movement patterns
   - Examples: Mookie Betts, Aaron Judge, Freddie Freeman, etc.

#### **Technical Requirements** (From Your Spec):
- **Input**: Video (30-600 FPS)
- **Processing**: MediaPipe pose detection (33 joints/frame)
- **Physics**: Angular momentum, moment of inertia, kinematic chain analysis
- **Anthropometrics**: de Leva tables for segment mass/length based on height/weight
- **Event Detection**: First Movement, Foot Plant, Contact (peak bat velocity)
- **Frame Rate Normalization**: Critical millisecond precision
- **Weapon Score FPS Caps**:
  - 240+ FPS: Full range (0-100)
  - 120-239 FPS: Cap at 95
  - 60-119 FPS: Cap at 90
  - 30-59 FPS: Cap at 85

---

## 📋 VALUE LADDER (WHAT YOU'RE SELLING)

### **Level 1**: Free Content + Quiz ($0)
- Lead generation
- "Which Motor Profile Are You?" quiz

### **Level 2**: Kinetic Blueprint Assessment ($299) ⭐ **BUILD THIS FIRST**
- Automated assessment
- Lab Report in Rick's voice
- One-time purchase

### **Level 3**: Blueprint Membership ($97/month or $797/year)
- Unlimited assessments
- Video library
- Monthly live Q&A
- Community access

### **Level 4**: Blueprint + Pods ($297/month)
- Weekly video review by Rick
- Direct messaging
- Custom drill prescriptions

### **Level 5**: 90-Day Transformation ($1,997, Winter Only)
- 1:1 calls with Rick
- Custom program
- Unlimited messaging

---

## 🛠️ WHAT YOU NEED TO BUILD NEXT

### **PHASE 1: Physics Engine (Core)** 🎯 **START HERE**
**Timeline**: 1-2 weeks  
**Goal**: Python script that takes video → produces JSON report

#### Deliverables:
```python
# Input
video_path = "131215-Hitting.mov"
athlete_height = 182  # cm
athlete_weight = 85   # kg
bat_side = "right"    # or "left"

# Output (JSON)
{
  "tempo_ratio": 2.8,
  "tempo_category": "IDEAL",
  "ground_score": 87,
  "engine_score": 92,
  "weapon_score": 78,
  "transfer_ratio": 1.15,
  "transfer_category": "STRONG",
  "motor_profile": "WHIPPER",
  "pro_comparison": "Mookie Betts (94% similarity)",
  "events": {
    "first_movement": {"frame": 15, "time_ms": 500},
    "foot_plant": {"frame": 45, "time_ms": 1500},
    "contact": {"frame": 65, "time_ms": 2167}
  },
  "detailed_metrics": {
    "load_duration_ms": 1000,
    "launch_duration_ms": 667,
    "peak_bat_speed_mph": 78.5,
    "peak_pelvis_angular_momentum": 245.6,
    "bat_momentum_at_contact": 282.3
  }
}
```

#### Technical Stack:
- **Python 3.11**
- **MediaPipe** (pose detection)
- **OpenCV** (video processing)
- **NumPy** (physics calculations)
- **SciPy** (signal processing)

#### What We'll Build:
1. **Video Processor**
   - Extract frames
   - Detect frame rate
   - Normalize to millisecond precision

2. **Pose Detector**
   - MediaPipe integration
   - 33 joint landmarks per frame
   - Confidence filtering

3. **Physics Calculator**
   - Anthropometric scaling (de Leva tables)
   - Segment mass & moment of inertia
   - Angular velocity & momentum
   - Kinematic chain analysis

4. **Event Detector**
   - First Movement (hip rotation threshold)
   - Foot Plant (front foot velocity → 0)
   - Contact (peak bat velocity)

5. **Scoring System**
   - Tempo Ratio
   - Ground Score (0-100)
   - Engine Score (0-100)
   - Weapon Score (0-100, FPS-adjusted)
   - Transfer Ratio

6. **Profile Matcher**
   - Motor Profile (SPINNER/SLINGSHOTTER/WHIPPER/TITAN)
   - Pro Player Comparison

#### Test Cases:
We'll use YOUR 8 videos to validate:
- 5 swings from your on-form app (varied quality)
- 3 Shohei Ohtani swings (300fps, pro-level)

---

### **PHASE 2: Backend Integration** 
**Timeline**: 3-5 days  
**Goal**: Connect physics engine to FastAPI backend

#### New Database Tables:
```sql
CREATE TABLE videos (
    id SERIAL PRIMARY KEY,
    player_id INTEGER REFERENCES players(id),
    filename VARCHAR(255),
    url TEXT,
    fps INTEGER,
    duration_ms INTEGER,
    upload_date TIMESTAMP,
    status VARCHAR(50)  -- 'uploaded', 'processing', 'completed', 'failed'
);

CREATE TABLE analysis_jobs (
    id SERIAL PRIMARY KEY,
    video_id INTEGER REFERENCES videos(id),
    status VARCHAR(50),  -- 'queued', 'processing', 'completed', 'failed'
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    error_message TEXT
);

CREATE TABLE reports (
    id SERIAL PRIMARY KEY,
    player_id INTEGER REFERENCES players(id),
    video_id INTEGER REFERENCES videos(id),
    tempo_ratio DECIMAL(4,2),
    tempo_category VARCHAR(20),
    ground_score INTEGER,
    engine_score INTEGER,
    weapon_score INTEGER,
    transfer_ratio DECIMAL(4,2),
    transfer_category VARCHAR(20),
    motor_profile VARCHAR(50),
    pro_comparison VARCHAR(100),
    detailed_metrics JSONB,  -- Full physics data
    created_at TIMESTAMP
);
```

#### New API Endpoints:
```
POST /videos/upload              → Upload video for analysis
POST /videos/{id}/analyze        → Trigger analysis
GET  /videos/{id}                → Video details
GET  /videos/{id}/status         → Analysis status
GET  /reports/{id}               → Full report (JSON)
GET  /reports/{id}/pdf           → Lab Report (PDF in Rick's voice)
GET  /players/{id}/reports       → All reports for a player
```

#### Cloud Storage:
- **Cloudflare R2** (S3-compatible, $0.015/GB/month)
- Store uploaded videos
- Store generated reports/PDFs

---

### **PHASE 3: Simple Web Interface**
**Timeline**: 3-5 days  
**Goal**: Basic dashboard to test video upload & report generation

#### Features:
- Upload video
- Enter athlete height/weight/bat side
- View processing status
- See JSON report
- Download PDF report

#### Tech:
- Simple HTML/CSS/JavaScript
- Hosted on Railway (same as backend)
- No authentication yet (testing only)

---

### **PHASE 4: Player Portal (React)**
**Timeline**: 2-3 weeks  
**Goal**: Full customer-facing app for $299 Kinetic Blueprint Assessment

#### Features:
1. **Authentication**
   - Sign up / Login
   - Email verification
   - Password reset

2. **Assessment Flow**
   - Upload video
   - Enter profile (height, weight, bat side)
   - Watch processing status
   - View Lab Report

3. **Reports Dashboard**
   - List all assessments
   - Compare assessments over time
   - Download PDFs

4. **Payment Integration**
   - Stripe checkout ($299)
   - One-time payment
   - Automatic access after payment

#### Tech Stack:
- **Next.js** (React framework)
- **Tailwind CSS** (styling)
- **Stripe** (payments)
- **Deployed on**: Vercel (free tier)

---

### **PHASE 5: Membership Features**
**Timeline**: 1-2 weeks  
**Goal**: $97/month Blueprint Membership

#### Features:
- Unlimited assessments
- Video library (Rick's content)
- Monthly live Q&A (Zoom integration)
- Community forum

#### Tech:
- Stripe subscription billing
- Video hosting (Vimeo/Cloudflare Stream)
- Forum (Circle/Discord integration)

---

## 💰 COST BREAKDOWN (REALISTIC)

### Current Costs:
- **Railway**: $5/month (Backend + PostgreSQL)
- **Domain**: $12/year (~$1/month)
- **Total**: **$6/month**

### After Full Build:
- **Railway**: $5/month
- **Cloudflare R2**: $1/month (video storage)
- **Stripe**: 2.9% + $0.30 per transaction
- **Vercel**: $0/month (free tier)
- **Email**: $0/month (Resend free tier)
- **Total Fixed**: **~$6-7/month**

### Revenue Model (Year 1):
- **Assessments** (100 × $299): $29,900
- **Membership** (40 × $97 × 10 months): $38,800
- **Pods** (10 × $297 × 9 months): $26,730
- **90-Day** (10 × $1,997): $19,970
- **TOTAL**: **$115,400**

**Profit Margin**: ~99% (after costs)

---

## 🚀 RECOMMENDED BUILD ORDER

### **Option A: Full MVP (6-8 weeks)**
Build everything end-to-end before launch.

**Pros**:
- Polished product
- Ready to take payments
- Professional look

**Cons**:
- Long wait before revenue
- More upfront work

---

### **Option B: Phased Launch (Start Revenue Sooner)**

#### **Week 1-2**: Build Physics Engine
- Test with your 8 videos
- Validate accuracy
- Output: Working Python script

#### **Week 3**: Manual Processing Beta ($99 Early Bird)
- You manually run the script for customers
- Email them PDF reports
- Collect feedback
- **Revenue**: 10 customers × $99 = $990

#### **Week 4-5**: Backend Integration
- Automate the process
- Build API endpoints
- Database integration

#### **Week 6-7**: Simple Upload Interface
- Basic web form
- Automated processing
- **Revenue**: Launch at $199 (early adopter price)

#### **Week 8-10**: Full Player Portal
- React app
- Stripe integration
- **Revenue**: Full $299 price

**Pros**:
- Start earning within 2 weeks
- Get real customer feedback early
- Validate demand before full build

**Cons**:
- Manual work initially
- Less polished at first

---

### **Option C: Proof of Concept (3 Days)** ⭐ **RECOMMENDED START**

**Goal**: Validate the physics engine works correctly

#### Deliverables:
1. **Python Script** (takes video path, height, weight, side)
2. **JSON Output** (all 7 key metrics)
3. **Test Results** (run on your 8 videos)

#### Why Start Here:
- **Risk Mitigation**: Prove the core technology works
- **Fast Validation**: 3 days to see if physics is accurate
- **Low Cost**: No infrastructure yet
- **Decision Point**: If physics works, proceed with Option B

#### After 3 Days, You'll Know:
- ✅ Can we detect poses reliably?
- ✅ Are the physics calculations accurate?
- ✅ Do the scores make sense?
- ✅ Can we differentiate between skill levels?
- ✅ Does the pro comparison work?

**If YES → Proceed to Option B (Phased Launch)**  
**If NO → Refine physics before building infrastructure**

---

## 🎯 MY RECOMMENDATION: START WITH OPTION C

### **Next 3 Days (Physics Engine Proof of Concept)**

#### Day 1: Setup & Video Processing
- Install MediaPipe, OpenCV, NumPy
- Build video frame extractor
- Build pose detector
- Test on 1 video (131215-Hitting.mov)

#### Day 2: Physics Calculations
- Implement anthropometric scaling (de Leva)
- Calculate angular momentum
- Implement event detection
- Test on 3 videos

#### Day 3: Scoring & Validation
- Build scoring algorithms
- Motor profile detection
- Pro player comparison
- Test on all 8 videos
- Generate JSON reports

### **Deliverable**:
```bash
python analyze_swing.py \
  --video "131215-Hitting.mov" \
  --height 182 \
  --weight 85 \
  --side right \
  --output report.json
```

### **Output**: 
Full JSON report with all 7 metrics, validated against your 8 test videos.

---

## ❓ QUESTIONS FOR YOU (TO PROCEED)

### 1. **Timeline**
How urgently do you need this? 
- ⚡ ASAP (start today)
- 📅 Within 1-2 weeks
- 🗓️ Flexible (1-2 months)

### 2. **First Customer**
Who will be the first person to use this?
- You (testing)
- Beta customers (small group)
- Public launch (anyone can buy)

### 3. **Video Details**
For your 5 on-form app videos:
- What's the frame rate? (30fps? 60fps? 120fps?)
- What's your height? (cm or inches)
- What's your weight? (kg or lbs)
- Bat side? (right or left)

For the 3 Shohei videos:
- Are they actually 300fps? (we'll verify)
- Do you know his height/weight? (193cm, 95kg)

### 4. **Accuracy Priority**
What's most important to you?
- **Physics accuracy** (perfect calculations)
- **Speed** (fast processing)
- **Visual output** (pretty reports)
- **All of the above** (takes longer)

### 5. **Budget**
Are you okay with:
- Current cost: $6/month (backend)
- After full build: ~$10-15/month (backend + video storage)
- Stripe fees: 2.9% + $0.30 per $299 sale (~$9/sale)

---

## 🏁 WHAT HAPPENS NEXT (IF YOU APPROVE)

### **I'll Build the Physics Engine Proof of Concept (3 Days)**

1. **Install dependencies** in `/home/user/webapp`
2. **Create `physics_engine/`** directory
3. **Build the 6 core modules**:
   - Video processor
   - Pose detector
   - Physics calculator
   - Event detector
   - Scoring system
   - Profile matcher
4. **Test on your 8 videos**
5. **Generate JSON reports** for each
6. **Validate accuracy** (you review the results)

### **By End of Day 3**:
You'll have a working Python script that:
- Takes any baseball swing video
- Produces a comprehensive physics report
- Matches Coach Rick's specs exactly

### **Then We Decide**:
- ✅ Physics works → Build backend integration (Option B)
- ⚠️ Needs refinement → Iterate on physics
- 🚀 Works great → Fast-track to manual beta (start revenue)

---

## 📞 READY TO START?

**Say "YES" and I'll immediately start building the Physics Engine Proof of Concept.**

I'll use your 8 uploaded videos as test cases and have a working demo in 3 days.

---

**Last Updated**: 2025-12-22  
**Your Backend**: https://reboot-motion-backend-production.up.railway.app  
**Your Repo**: https://github.com/THScoach/reboot-motion-backend  
**Your Videos**: 8 files ready in `/home/user/uploaded_files/`

**LET'S BUILD THIS! 🚀**
