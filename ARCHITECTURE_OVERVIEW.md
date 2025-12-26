# 🏗️ CATCHING BARRELS — SYSTEM ARCHITECTURE

**Date**: 2025-12-22  
**Project**: Kinetic Blueprint Assessment ($299 Product)

---

## 🎯 CURRENT STATE (WHAT'S BUILT)

```
┌─────────────────────────────────────────────────────────────┐
│                    REBOOT MOTION API                        │
│              https://api.rebootmotion.com                   │
│                                                             │
│  • OAuth 2.0 Authentication ✅                              │
│  • 100 Athletes ✅                                          │
│  • Hitting Sessions ✅                                      │
│  • Biomechanics Data (Pipeline v2) ⚠️                       │
└─────────────────────────────────────────────────────────────┘
                            ↓ (OAuth 2.0)
                            ↓
┌─────────────────────────────────────────────────────────────┐
│              YOUR BACKEND API (FastAPI)                     │
│    https://reboot-motion-backend-production.up.railway.app  │
│                                                             │
│  • Python 3.11 ✅                                           │
│  • FastAPI ✅                                               │
│  • SQLAlchemy ✅                                            │
│  • Auto-Deploy from GitHub ✅                               │
│                                                             │
│  DATABASE (PostgreSQL on Railway):                          │
│  ├── players (100 records) ✅                               │
│  ├── sessions (110 records) ✅                              │
│  ├── biomechanics_data (0 records) ⚠️                       │
│  └── sync_log ✅                                            │
│                                                             │
│  API ENDPOINTS:                                             │
│  ├── GET  /players                                          │
│  ├── GET  /players/{id}                                     │
│  ├── GET  /players/{id}/sessions                            │
│  ├── GET  /sessions/{id}                                    │
│  ├── POST /sync/trigger                                     │
│  └── GET  /docs (Swagger UI)                                │
└─────────────────────────────────────────────────────────────┘
                            ↓
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                   NO FRONTEND YET ❌                         │
│                   (This is what we need)                    │
└─────────────────────────────────────────────────────────────┘
```

**Status**: Backend is 100% complete, but it only serves Reboot Motion data. We need to add the Physics Engine + Frontend for your $299 product.

---

## 🎯 TARGET STATE (WHAT WE'RE BUILDING)

```
┌─────────────────────────────────────────────────────────────┐
│                    ATHLETE (Customer)                        │
│                  (Pays $299 for assessment)                  │
└─────────────────────────────────────────────────────────────┘
                            ↓
                            ↓ (Upload video + profile)
                            ↓
┌─────────────────────────────────────────────────────────────┐
│              PLAYER PORTAL (React/Next.js)                   │
│                  https://catchingbarrels.app                 │
│                                                              │
│  • Upload video                                              │
│  • Enter height/weight/bat side                              │
│  • View processing status                                    │
│  • View Lab Report (Coach Rick's voice)                      │
│  • Download PDF                                              │
│  • Stripe payment ($299)                                     │
└─────────────────────────────────────────────────────────────┘
                            ↓
                            ↓ (HTTP POST)
                            ↓
┌─────────────────────────────────────────────────────────────┐
│              YOUR BACKEND API (FastAPI)                      │
│    https://reboot-motion-backend-production.up.railway.app   │
│                                                              │
│  NEW ENDPOINTS:                                              │
│  ├── POST /videos/upload         (Upload video)             │
│  ├── POST /videos/{id}/analyze   (Trigger analysis)         │
│  ├── GET  /videos/{id}/status    (Check progress)           │
│  ├── GET  /reports/{id}          (Full JSON report)         │
│  ├── GET  /reports/{id}/pdf      (Lab Report PDF)           │
│  └── POST /stripe/webhook        (Payment confirmation)     │
│                                                              │
│  NEW DATABASE TABLES:                                        │
│  ├── videos                                                  │
│  ├── analysis_jobs                                           │
│  └── reports                                                 │
└─────────────────────────────────────────────────────────────┘
                            ↓
                            ↓ (Process video)
                            ↓
┌─────────────────────────────────────────────────────────────┐
│              PHYSICS ENGINE (Python)                         │
│                (This is the CORE we build first)             │
│                                                              │
│  INPUT:                                                      │
│  • Video file (30-600 FPS)                                   │
│  • Athlete height (cm)                                       │
│  • Athlete weight (kg)                                       │
│  • Bat side (right/left)                                     │
│                                                              │
│  PROCESSING:                                                 │
│  ├── Video Processor (Extract frames, detect FPS)           │
│  ├── Pose Detector (MediaPipe → 33 joints/frame)            │
│  ├── Physics Calculator (Angular momentum, kinematics)      │
│  ├── Event Detector (First Move, Foot Plant, Contact)       │
│  ├── Scoring System (Tempo, Ground, Engine, Weapon)         │
│  └── Profile Matcher (Motor Profile + Pro Comparison)       │
│                                                              │
│  OUTPUT (JSON):                                              │
│  {                                                           │
│    "tempo_ratio": 2.8,                                       │
│    "tempo_category": "IDEAL",                                │
│    "ground_score": 87,                                       │
│    "engine_score": 92,                                       │
│    "weapon_score": 78,                                       │
│    "transfer_ratio": 1.15,                                   │
│    "transfer_category": "STRONG",                            │
│    "motor_profile": "WHIPPER",                               │
│    "pro_comparison": "Mookie Betts (94%)",                   │
│    "events": {...},                                          │
│    "detailed_metrics": {...}                                 │
│  }                                                           │
└─────────────────────────────────────────────────────────────┘
                            ↓
                            ↓ (Store results)
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                CLOUD STORAGE (Cloudflare R2)                 │
│                                                              │
│  • Uploaded videos                                           │
│  • Generated PDF reports                                     │
│  • Cost: ~$1/month                                           │
└─────────────────────────────────────────────────────────────┘
```

---

## 📊 DATA FLOW (Step-by-Step)

### **Step 1: Athlete Visits Website**
```
Athlete → https://catchingbarrels.app
```

### **Step 2: Payment**
```
Athlete → Stripe Checkout → Pays $299 → Success
```

### **Step 3: Upload Video**
```
Athlete uploads video + enters profile:
- Height: 182 cm
- Weight: 85 kg
- Bat side: right
```

### **Step 4: Backend Receives Upload**
```
POST /videos/upload
{
  "player_id": 123,
  "video_file": <file>,
  "height_cm": 182,
  "weight_kg": 85,
  "bat_side": "right"
}

Response:
{
  "video_id": 456,
  "status": "queued"
}
```

### **Step 5: Physics Engine Processes Video**
```
Backend → Physics Engine:

1. Extract frames (30-600 FPS)
2. Run MediaPipe pose detection
3. Calculate physics:
   - Angular momentum
   - Moment of inertia
   - Kinematic chain
4. Detect events:
   - First Movement
   - Foot Plant
   - Contact
5. Generate scores:
   - Tempo Ratio: 2.8
   - Ground Score: 87
   - Engine Score: 92
   - Weapon Score: 78
   - Transfer Ratio: 1.15
6. Determine motor profile:
   - WHIPPER
7. Match to pro player:
   - Mookie Betts (94%)
```

### **Step 6: Store Report**
```
Backend → Database:

INSERT INTO reports (
  player_id,
  video_id,
  tempo_ratio,
  ground_score,
  engine_score,
  weapon_score,
  transfer_ratio,
  motor_profile,
  pro_comparison,
  detailed_metrics
) VALUES (...);
```

### **Step 7: Generate PDF**
```
Backend → PDF Generator:

Create Lab Report in Coach Rick's voice:
- Header: "Kinetic Blueprint Assessment"
- Athlete: John Smith
- Date: 2025-12-22
- Tempo Ratio: 2.8 (IDEAL)
- Ground Score: 87/100
- Engine Score: 92/100
- Weapon Score: 78/100
- Transfer Ratio: 1.15 (STRONG)
- Motor Profile: WHIPPER
- Pro Comparison: Mookie Betts (94%)
- Detailed breakdown + recommendations
```

### **Step 8: Notify Athlete**
```
Backend → Email Service:

Subject: "Your Kinetic Blueprint is Ready! 🎯"
Body: "Hi John, your assessment is complete. View your report here: [link]"
```

### **Step 9: Athlete Views Report**
```
Athlete → GET /reports/456
Athlete → Downloads PDF
Athlete → Shares on social media
Athlete → Buys membership ($97/month)
```

---

## 🔧 TECHNICAL STACK

### **Backend (What You Have)**
- **Language**: Python 3.11
- **Framework**: FastAPI
- **Database**: PostgreSQL (Railway)
- **ORM**: SQLAlchemy
- **Authentication**: OAuth 2.0 (for Reboot Motion)
- **Deployment**: Railway (auto-deploy from GitHub)
- **Cost**: $5/month

### **Physics Engine (What We're Building)**
- **Language**: Python 3.11
- **Pose Detection**: MediaPipe
- **Video Processing**: OpenCV
- **Physics Calculations**: NumPy
- **Signal Processing**: SciPy
- **Anthropometrics**: de Leva tables (1996)
- **Cost**: $0 (runs on same Railway instance)

### **Frontend (Future)**
- **Framework**: Next.js (React)
- **Styling**: Tailwind CSS
- **Authentication**: NextAuth.js
- **Payments**: Stripe
- **Deployment**: Vercel (free tier)
- **Cost**: $0/month

### **Cloud Storage (Future)**
- **Service**: Cloudflare R2 (S3-compatible)
- **Purpose**: Video storage, PDF reports
- **Cost**: ~$1/month

### **Email (Future)**
- **Service**: Resend (or SendGrid)
- **Purpose**: Report notifications, marketing
- **Cost**: $0/month (free tier)

---

## 💰 COST BREAKDOWN

### **Current (Backend Only)**
```
Railway (Backend + PostgreSQL): $5/month
Domain (optional):              $1/month
─────────────────────────────────────────
TOTAL:                          $6/month
```

### **After Full Build**
```
Railway (Backend + PostgreSQL): $5/month
Cloudflare R2 (Video storage):  $1/month
Domain:                         $1/month
Email (Resend free tier):       $0/month
Frontend (Vercel free tier):    $0/month
─────────────────────────────────────────
TOTAL FIXED:                    $7/month

Per-Transaction Costs:
Stripe fees (2.9% + $0.30):     $9 per $299 sale
─────────────────────────────────────────
Net revenue per sale:           $290
```

### **At Scale (100 customers/month)**
```
Revenue:   100 × $299 = $29,900
Costs:     100 × $9   = $900 (Stripe)
           Fixed      = $7 (infrastructure)
─────────────────────────────────────────
PROFIT:                 $28,993/month
Profit Margin:          97%
```

---

## 📈 SCALABILITY

### **How Many Customers Can We Handle?**

#### **Current Setup (Railway $5/month plan)**
- **Concurrent analyses**: 2-3 (CPU-bound)
- **Storage**: 100GB video storage
- **Bandwidth**: Unlimited
- **Realistic capacity**: ~50 customers/month

#### **Upgraded Setup (Railway $10/month plan)**
- **Concurrent analyses**: 5-10
- **Storage**: 500GB
- **Realistic capacity**: ~200 customers/month

#### **At 200+ customers/month**
- **Use background job queue** (Celery + Redis)
- **Separate worker instance** for physics processing
- **Cost**: ~$20/month total
- **Capacity**: Unlimited (can add more workers)

---

## 🔒 SECURITY & PRIVACY

### **Data Security**
- **Videos**: Encrypted at rest (Cloudflare R2)
- **Database**: SSL connection (Railway PostgreSQL)
- **API**: HTTPS only
- **Authentication**: JWT tokens
- **Payments**: Stripe (PCI compliant)

### **Privacy**
- **Video retention**: 30 days (then deleted)
- **Report retention**: Permanent (unless customer requests deletion)
- **No third-party analytics** (athlete data stays private)
- **GDPR compliant**: Right to deletion

---

## 🚀 DEPLOYMENT STRATEGY

### **Phase 1: Proof of Concept (3 Days)**
```
Local development → Test with 8 videos → Validate physics
```

### **Phase 2: Manual Beta (1 Week)**
```
You run script manually for customers → Collect feedback
```

### **Phase 3: Automated Backend (1 Week)**
```
Deploy to Railway → Automate processing → Add API endpoints
```

### **Phase 4: Simple Frontend (3 Days)**
```
Basic HTML form → Upload + view results → No payment yet
```

### **Phase 5: Full Product (2 Weeks)**
```
React app → Stripe integration → Marketing site
```

### **Phase 6: Membership Features (2 Weeks)**
```
Subscription billing → Video library → Community
```

---

## 📋 TIMELINE SUMMARY

### **Fast Track (Start Revenue ASAP)**
```
Week 1-2:   Physics Engine + Manual Beta → First $999 revenue
Week 3-4:   Backend Integration → Automated processing
Week 5-6:   Simple Frontend → $199 early adopter price
Week 7-10:  Full Product → $299 full price
───────────────────────────────────────────────────────────
10 weeks to full product, revenue starts Week 2
```

### **Conservative (Polished Product)**
```
Week 1-2:   Physics Engine
Week 3-4:   Backend Integration
Week 5-6:   Frontend (Basic)
Week 7-8:   Frontend (Polished)
Week 9-10:  Payment Integration
Week 11:    Testing
Week 12:    Launch
───────────────────────────────────────────────────────────
12 weeks to launch, no revenue until launch
```

---

## ✅ WHAT YOU NEED TO DO NOW

### **1. Answer These Questions**
- What's your height/weight? (for testing your videos)
- What's your bat side? (right or left)
- Do you want Fast Track or Conservative approach?
- When do you want to launch? (target date)

### **2. Provide Video Details**
For your 5 on-form videos:
- What frame rate are they? (30fps? 60fps? 120fps?)

For the 3 Shohei videos:
- Are they actually 300fps? (we'll verify)

### **3. Approve the Plan**
Say "YES, build the Physics Engine" and I'll start immediately.

---

## 📞 READY TO START?

**I'll build the Physics Engine Proof of Concept in 3 days using your 8 videos as test cases.**

**Just say "GO" and I'll begin! 🚀**

---

**Your Backend**: https://reboot-motion-backend-production.up.railway.app  
**Your Repo**: https://github.com/THScoach/reboot-motion-backend  
**Your Videos**: 8 files ready at `/home/user/uploaded_files/`

**Last Updated**: 2025-12-22
