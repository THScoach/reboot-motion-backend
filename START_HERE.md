# 🚀 START HERE — QUICK REFERENCE

**Date**: 2025-12-22  
**Project**: Catching Barrels — Kinetic Blueprint Assessment  
**Your Goal**: Build $299 automated swing analysis product

---

## 📚 DOCUMENTS CREATED FOR YOU

### **1. EXECUTIVE_SUMMARY.md** ⭐ READ THIS FIRST
- What you have (backend complete)
- What you need (physics engine + frontend)
- Timeline options (3 days to 10 weeks)
- Economics (costs + revenue projections)
- **TL;DR section at bottom**

### **2. CATCHING_BARRELS_ACTION_PLAN.md**
- Full product vision
- Core truth: People buy access to Coach Rick
- Value ladder (5 levels: $0 → $1,997)
- Build order (what to build first)
- Recommended approach (Option C: 3-day proof of concept)

### **3. ARCHITECTURE_OVERVIEW.md**
- Technical stack (Python, FastAPI, MediaPipe, React)
- Current state diagram (what's built)
- Target state diagram (what we're building)
- Data flow (step-by-step)
- Cost breakdown ($7/month)
- Scalability plan (50-200+ customers/month)

### **4. VIDEO_ANALYSIS_SUMMARY.md**
- Technical details of your 8 videos
- Frame rate analysis (30 FPS vs 300 FPS)
- Weapon Score caps (FPS-dependent)
- Testing strategy (your swings vs Shohei)
- Example JSON outputs (what you'll get)

---

## 🎥 YOUR TEST VIDEOS (8 FILES)

### **Your Swings** (5 videos, 30 FPS, 720p)
```
1. 131215-Hitting.mov — 16.4s
2. 131151-Hitting.mov — 15.4s
3. 131233-Hitting.mov — 19.5s
4. 131200-Hitting.mov — 19.2s
5. 131301-Hitting.mov — 26.3s
```
**Quality**: Good for testing, Weapon Score capped at 85/100 (due to 30 FPS)

### **Shohei Ohtani** (3 videos, 300 FPS ✅)
```
6. 340109 (1).mp4 — 11.3s
7. 340109 (2).mp4 — 7.2s
8. 340109 (3).mp4 — 10.7s
```
**Quality**: EXCELLENT — Full precision (300 FPS → Weapon Score 0-100)

**Location**: `/home/user/uploaded_files/`

---

## 🎯 THE 7 KEY METRICS (FROM YOUR SPEC)

1. **Tempo Ratio** (Load Duration / Launch Duration)
   - IDEAL: 2.5-3.0:1

2. **Ground Score** (0-100)
   - Weight transfer + leg drive

3. **Engine Score** (0-100)
   - Hip rotation + hip-shoulder separation

4. **Weapon Score** (0-100)
   - Bat speed + hand path efficiency
   - **FPS-dependent**: 30fps cap=85, 240+fps cap=100

5. **Transfer Ratio** (Energy Transfer)
   - Bat Momentum / Pelvis Peak Momentum
   - ELITE: ≥1.20

6. **Motor Profile**
   - SPINNER / SLINGSHOTTER / WHIPPER / TITAN

7. **Pro Player Comparison**
   - Mookie Betts, Aaron Judge, Freddie Freeman, etc.

---

## ⏰ TIMELINE OPTIONS

### **Option C: Proof of Concept (3 Days)** ⭐ RECOMMENDED
```
Day 1: Video processing + pose detection
Day 2: Physics calculations + event detection
Day 3: Scoring + validation (test on 8 videos)
```
**Deliverable**: Python script → JSON reports  
**Risk**: Low (validate physics first)  
**Cost**: $0 (no infrastructure yet)

### **Option B: Fast Track (2-10 Weeks)**
```
Week 1-2:   Physics Engine + Manual Beta → $999 revenue
Week 3-4:   Backend Integration → Automate
Week 5-6:   Simple Frontend → $199 price
Week 7-10:  Full Product → $299 price
```
**Deliverable**: Full product, revenue starts Week 2  
**Risk**: Medium (manual work initially)

### **Option A: Full MVP (6-8 Weeks)**
```
Week 1-8: Build everything before launch
Week 8:   Launch at $299
```
**Deliverable**: Polished product  
**Risk**: High (no revenue until Week 8)

---

## 💰 ECONOMICS

### **Revenue Model (Year 1)**
```
Assessments ($299):      100 × $299 = $29,900
Membership ($97/mo):      40 × $970 = $38,800
Pods ($297/mo):           10 × $2,673 = $26,730
90-Day ($1,997):          10 × $1,997 = $19,970
───────────────────────────────────────────────
TOTAL:                                $115,400
```

### **Cost Structure**
```
Fixed:
  Railway (Backend): $5/month
  Cloudflare R2:     $1/month
  Domain:            $1/month
  ─────────────────────────────
  TOTAL:             $7/month = $84/year

Per-Transaction:
  Stripe:            2.9% + $0.30 = ~$9 per $299 sale
  Net revenue:       $290 per sale

Profit Margin: 97%
```

---

## 🛠️ TECH STACK

### **What You Have (Backend)**
```
✅ Python 3.11
✅ FastAPI
✅ SQLAlchemy
✅ PostgreSQL (Railway)
✅ OAuth 2.0 (Reboot Motion)
✅ Auto-deploy (GitHub → Railway)
```

### **What We're Building (Physics Engine)**
```
⏳ MediaPipe (pose detection)
⏳ OpenCV (video processing)
⏳ NumPy (physics calculations)
⏳ SciPy (signal processing)
⏳ de Leva tables (anthropometrics)
```

### **What's Later (Frontend)**
```
🔜 Next.js (React)
🔜 Tailwind CSS
🔜 Stripe (payments)
🔜 Vercel (hosting)
```

---

## ✅ WHAT YOU NEED TO DO NOW

### **1. Provide Your Profile** (for testing your videos)
```
Height: ___ cm (or ___ inches)
Weight: ___ kg (or ___ lbs)
Bat Side: Right or Left
```

### **2. Choose Your Approach**
```
□ Option C: Proof of Concept (3 days, validate first)
□ Option B: Fast Track (start revenue in 2 weeks)
□ Option A: Full MVP (6-8 weeks, polished product)
```

### **3. Say "GO"**
```
"GO — Build Proof of Concept"
```

---

## 🚀 WHAT HAPPENS NEXT (PROOF OF CONCEPT)

### **Day 1: Setup & Video Processing**
- Install dependencies (MediaPipe, OpenCV, NumPy)
- Build video frame extractor
- Build pose detector
- Test on 1 video (131215-Hitting.mov)

### **Day 2: Physics Calculations**
- Implement de Leva anthropometrics
- Calculate angular momentum, moment of inertia
- Implement event detection
- Test on 3 videos

### **Day 3: Scoring & Validation**
- Build 7 scoring algorithms
- Motor profile detection
- Pro player comparison
- Test on all 8 videos
- Generate JSON reports

### **End of Day 3**:
You get:
- ✅ Working Python script
- ✅ 8 JSON reports (your swings + Shohei)
- ✅ Side-by-side comparison (You vs Shohei)
- ✅ Validation (do scores make sense?)

### **Then You Decide**:
- ✅ Physics works → Build backend integration
- ⚠️ Needs refinement → Iterate on physics
- 🚀 Works great → Fast-track to revenue

---

## 📄 FILE LOCATIONS

### **Your Backend**
```
Repository: https://github.com/THScoach/reboot-motion-backend
Live API:   https://reboot-motion-backend-production.up.railway.app
API Docs:   https://reboot-motion-backend-production.up.railway.app/docs
```

### **Your Videos**
```
Location: /home/user/uploaded_files/
Files:    8 videos (5 yours + 3 Shohei)
```

### **Your Documents**
```
Location: /home/user/webapp/
Files:    
  - START_HERE.md (this file)
  - EXECUTIVE_SUMMARY.md
  - CATCHING_BARRELS_ACTION_PLAN.md
  - ARCHITECTURE_OVERVIEW.md
  - VIDEO_ANALYSIS_SUMMARY.md
```

---

## ❓ QUICK FAQS

**Q: How accurate will this be?**  
A: Your spec is based on peer-reviewed research. We'll validate on 300 FPS Shohei videos (gold standard).

**Q: What if customers only have 30 FPS videos?**  
A: 6/7 metrics work perfectly. Only Weapon Score is capped (85/100 vs 0-100).

**Q: How long does processing take?**  
A: ~2-5 minutes per video. Can optimize with GPU later.

**Q: Can I test manually before automating?**  
A: YES! Fast Track approach = you run script manually, then automate.

**Q: What if physics doesn't work?**  
A: That's why we do 3-day Proof of Concept first. Low risk.

---

## 🎯 TL;DR

**What You Have**: Backend complete, 8 test videos, physics spec  
**What You Need**: Physics engine (3 days), then frontend (2-3 weeks)  
**Timeline**: 3 days to validate, 10 weeks to revenue  
**Cost**: $7/month  
**Revenue**: $115k Year 1  
**Next Step**: Provide height/weight/bat side, say "GO"

---

## 🚀 READY?

**Just type:**
```
My height is ___ cm
My weight is ___ kg
My bat side is right (or left)

GO — Build Proof of Concept
```

**I'll start immediately! 🚀**

---

**Last Updated**: 2025-12-22
