# START HERE — CORRECTED QUICK REFERENCE

**Date**: 2025-12-22  
**Project**: Kinetic DNA Blueprint Assessment  
**Target**: $299 Automated Swing Analysis Product

---

## WHAT YOU BUILT (COMPLETE)

**Reboot Motion Backend API**
- Live at `https://reboot-motion-backend-production.up.railway.app`
- Syncing 100 athletes, 110 session records
- OAuth 2.0 authentication working
- Auto-deploy from GitHub to Railway
- Cost: $6/month

**What it does**: Syncs Reboot Motion data, provides REST API for queries  
**What it does NOT do**: Video upload, swing analysis, scoring, reports

---

## YOUR ACTUAL FRAMEWORK: THE 4B SYSTEM

### **1. BRAIN** (Timing/Tempo)
- Tempo Ratio: Load Duration / Launch Duration
- IDEAL: 2.5-3.0:1
- FOCUS AREA: <2.0:1 or >3.5:1

### **2. BODY** (Energy Transfer Chain)
- **Ground Flow** (0-100): Weight transfer, leg drive, ground reaction
- **Engine Flow** (0-100): Hip rotation, hip-shoulder separation, sequencing
- **Weapon Flow** (0-100): Bat speed, hand path efficiency, bat lag
  - *Note: FPS-dependent cap (30fps→85, 240+fps→100)*

### **3. BAT** (Delivery Quality)
- **Transfer Ratio**: Bat Momentum at Contact / Pelvis Peak Momentum
  - ELITE: ≥1.20
  - STRONG: 1.00-1.19
  - AVERAGE: 0.80-0.99
  - FOCUS AREA: <0.80
- *This is a calculated metric, not a score category*

### **4. BALL** (Predicted Output)
- Exit velocity prediction
- Launch angle optimization
- Barrel probability

### **Additional Outputs**
- **Motor Profile** (Classification): SPINNER, SLINGSHOTTER, WHIPPER, TITAN
- **Pro Comparison** (Matching algorithm): Similarity % to MLB players

---

## YOUR TEST VIDEOS

### Your Swings (5 videos, 30 FPS, 720p)
```
1. 131215-Hitting.mov — 16.4s
2. 131151-Hitting.mov — 15.4s
3. 131233-Hitting.mov — 19.5s
4. 131200-Hitting.mov — 19.2s
5. 131301-Hitting.mov — 26.3s
```
**Quality**: Suitable for Ground/Engine Flow and Tempo  
**Limitation**: Weapon Flow capped at 85/100 due to 30 FPS

### Shohei Ohtani Videos (3 videos, 300 FPS)
```
6. 340109 (1).mp4 — 11.3s
7. 340109 (2).mp4 — 7.2s
8. 340109 (3).mp4 — 10.7s
```
**Purpose**: High-precision testing for Weapon Flow  
**Note**: Scores will be generated once physics engine is validated

**Location**: `/home/user/uploaded_files/`

---

## KNOWN ISSUES

### Critical Bug: Frame Rate Normalization
**Problem**: 300 FPS videos produce impossible tempo ratios (0.96:1 instead of ~2.5:1)

**Root Cause**: Time calculations use frame counts, not milliseconds. At 300 FPS, each frame = 3.3ms. At 30 FPS, each frame = 33ms. All physics must normalize to absolute time.

**Status**: Must be fixed before any demo is valid.

### Technical Challenges
1. MediaPipe accuracy in various lighting
2. Event detection reliability (First Movement, Foot Plant, Contact)
3. Bat tracking at 30 FPS (limited Weapon Flow precision)
4. Anthropometric scaling validation
5. Angular momentum calculation accuracy

---

## REALISTIC TIMELINE

### Physics Engine Core: 1-2 Weeks
Not 3 days. This involves:
- Frame rate normalization (30-600 FPS → milliseconds)
- MediaPipe pose extraction (33 joints/frame)
- de Leva anthropometric scaling
- Angular momentum: L = I × ω
- Event detection via kinematic thresholds
- 4B scoring algorithms
- Motor Profile classification
- Pro comparison matching

### Backend Integration: 1 Week
- New database tables (videos, analysis_jobs, reports)
- API endpoints (upload, analyze, status, report)
- Cloudflare R2 storage integration

### Lab Report Generation: 3-5 Days
- PDF output matching your voice
- Requires: Lab Report Content Spec

### Simple Upload Interface: 3-5 Days
- Basic web form (testing only)
- No payment or auth yet

### Full Player Portal: 2-3 Weeks
- User authentication
- Mobile-responsive upload
- Stripe integration ($299)
- Reports dashboard

### Membership Features: 1-2 Weeks
- Subscription billing ($97/month)
- Video library
- Live Q&A integration
- Community forum

---

## TIMELINE OPTIONS

### Conservative (12 Weeks) — Recommended
```
Weeks 1-2:   Physics Engine (validate with 8 videos)
Week 3:      Backend Integration
Week 4:      Lab Report Generation
Week 5:      Simple Upload Interface
Weeks 6-8:   Full Player Portal
Weeks 9-10:  Beta Testing
Week 11:     Launch Prep
Week 12:     Public Launch
```
**Revenue starts**: Week 12  
**Risk**: Low (validated product)

### Aggressive (8 Weeks)
```
Weeks 1-2:   Physics Engine + Manual Beta
             (You run script manually, $99/customer)
             Revenue: ~$999 (10 beta customers)
Weeks 3-4:   Backend Integration
Week 5:      Simple Upload ($199 early adopter)
Weeks 6-8:   Full Portal ($299 full price)
```
**Revenue starts**: Week 2  
**Risk**: Medium (manual processing burden)

### Validation First (2 Weeks)
```
Weeks 1-2:   Physics Engine only
             Test on 8 videos
             Validate against your methodology
             THEN decide Conservative vs Aggressive
```
**Revenue starts**: TBD  
**Risk**: Low (prove physics works first)

---

## VALIDATION CRITERIA

Before declaring physics engine "working":

### Technical Requirements
1. Tempo Ratio: 1.5:1 to 4.0:1 for all test videos
2. Frame Rate Independence: 300 FPS and 30 FPS produce comparable Body scores (±10%)
3. Consistency: Multiple swings from same player show <15% score variation
4. Event Detection: Identifies events within ±50ms of manual review
5. Motor Profile: 80%+ match with manual assessment

### Output Requirements
6. Lab Report metrics are defensible (align with biomechanics research)
7. Report language sounds like Coach Rick
8. Recommendations are actionable

**If criteria not met**: Iterate, do not proceed to customer-facing product.

---

## COST STRUCTURE

### Fixed Costs
```
Railway (Backend):         $5/month
Cloudflare R2 (Storage):   $1/month
Domain:                    $1/month
Email (Resend free tier):  $0/month
Frontend (Vercel free):    $0/month
────────────────────────────────────
TOTAL:                     $7/month ($84/year)
```

### Variable Costs Per Sale
```
Stripe fees:               $9 per $299 assessment
Video storage (30 days):   ~$0.10
PDF generation:            ~$0.01
────────────────────────────────────
NET REVENUE:               ~$290 per sale
```

### Hidden Costs
- Your time (support, content, sales)
- Refunds (5-10%)
- Marketing/ads
- Maintenance
- Failed payments
- Chargebacks

**Realistic profit margin**: 60-75% (not 97%)

---

## REVENUE PROJECTIONS

### Year 1 Potential (IF Targets Met)
```
Kinetic DNA Blueprints:  100 × $299    = $29,900
Membership (Annual):      50 × $797    = $39,850
Pods:                     15 × $297×9  = $40,095
90-Day:                   10 × $1,997  = $19,970
───────────────────────────────────────────────
TOTAL POTENTIAL:                       $129,815
```

### Critical Dependencies
- Lead generation (500+ qualified leads/month)
- Conversion funnel (20%+ conversion)
- Content strategy (weekly content)
- Customer acquisition cost (<$50/customer)
- Retention (80%+ stay past month 3)

**Reality**: These numbers require a marketing system, not just a working product.

---

## WHAT'S MISSING

### 1. Lab Report Content Spec
- How do you explain each score to players?
- What recommendations for each Motor Profile?
- How do you frame Pro Comparison?

### 2. Mobile Upload Flow
- 70% of users upload from phones
- File size limits
- Upload progress/resume
- Portrait vs landscape handling
- Format compatibility (iPhone HEVC)

### 3. Error Handling Strategy
- What happens when pose detection fails?
- Poor lighting/quality?
- Player out of frame?
- Multiple people in video?
- Wrong camera angle?

### 4. Content Strategy
- Where do leads come from?
- YouTube? Instagram? TikTok? Paid ads?
- Referrals from coaches? Travel teams?
- SEO/blog content?

---

## TECHNICAL RISKS

### High Risk
1. Frame rate normalization (already broken)
2. Bat tracking at 30 FPS (limited precision)
3. MediaPipe reliability (lighting, occlusion)
4. Angular momentum validation (need gold standard)
5. Motor Profile accuracy (must match manual assessment)

### Medium Risk
6. Video upload size (500MB+ may timeout)
7. Processing time (2-5 min may feel slow)
8. PDF formatting (must look professional at $299)
9. Mobile browser compatibility (iOS Safari)
10. Database scaling (free tier limits)

---

## DOCUMENTS CREATED

**Primary Reference**:
- `CORRECTED_EXECUTIVE_SUMMARY.md` (18 KB) — Start here

**Supporting Docs**:
- `CATCHING_BARRELS_ACTION_PLAN.md` (16 KB) — Full development phases
- `ARCHITECTURE_OVERVIEW.md` (19 KB) — System design
- `VIDEO_ANALYSIS_SUMMARY.md` (12 KB) — Video technical details

**Location**: `/home/user/webapp/`

---

## WHAT YOU NEED TO PROVIDE

### To Start Development
1. **Your profile** (height, weight, bat side) for testing your 5 videos
2. **Lab Report Content Spec** (how you write/recommend for each score)
3. **Validation data** (manual assessments of your test swings, if available)

### To Proceed to Production
4. **Error handling policy** (customer communication, refunds)
5. **Content pipeline** (lead generation strategy)
6. **Support strategy** (who handles questions, response times)

---

## TERMINOLOGY (USE THIS)

- **Kinetic DNA Blueprint** (not "swing analysis")
- **4B Framework**: Brain, Body, Bat, Ball
- **Body = Ground Flow → Engine Flow → Weapon Flow** (energy chain)
- **Transfer Ratio** (keystone metric)
- **Motor Profile** (Spinner, Slingshotter, Whipper, Titan)
- **Pro Comparison** (matching algorithm)
- **Lab Report in Coach Rick's voice**

---

## DECISION POINT

### Choose Your Path:

**Option A: Conservative (12 weeks)**  
Validated product, professional launch, no revenue until Week 12

**Option B: Aggressive (8 weeks)**  
Manual beta, early revenue (Week 2), more customer interaction burden

**Option C: Validation First (2 weeks)**  
Prove physics works, THEN choose A or B

**Recommendation**: Start with Option C.

---

## NEXT STEPS

1. Provide your profile data
2. Choose timeline approach (A, B, or C)
3. Review/provide Lab Report spec
4. Clarify what "working" means to you

Once provided, development can begin with clear success criteria and realistic expectations.

---

**Backend**: https://reboot-motion-backend-production.up.railway.app  
**Repo**: https://github.com/THScoach/reboot-motion-backend  
**Videos**: `/home/user/uploaded_files/` (8 files)

**Last Updated**: 2025-12-22

---

## BOTTOM LINE

You have a working backend. You need a physics engine implementing your 4B Framework. This takes 1-2 weeks to validate, not 3 days. Revenue of $115k+ is possible but requires lead generation, not just a product. True profit margin is 60-75% after all costs. The frame rate bug must be fixed before testing is valid.

Clear path. No hype. Facts only.
