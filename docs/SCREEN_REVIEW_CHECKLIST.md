# Screen Review Checklist

**Version:** 1.0  
**Date:** December 26, 2025  
**Purpose:** Verify all 13 screens use consistent terminology, correct KRS scale, proper Motor Profiles, and complete specifications.

---

## Checklist Table

| # | Screen | KRS Scale | Motor Profile | 4B Cards | Colors | Data Binding | Responsive | A11y | Status |
|---|--------|-----------|---------------|----------|--------|--------------|------------|------|--------|
| 01 | Home Dashboard | ✅ 0-100 | N/A | ✅ Correct | ✅ | ✅ | ✅ | ✅ | ✅ PASS |
| 02 | Live Mode | N/A | N/A | N/A | ✅ | ✅ | ✅ | ✅ | ✅ PASS |
| 03 | Player Report | ✅ 0-100 | ✅ 4 types | ✅ Correct | ✅ | ✅ | ✅ | ✅ | ✅ PASS |
| 04 | Movement Assessment | N/A | ✅ 4 types | N/A | ✅ | ✅ | ✅ | ✅ | ✅ PASS |
| 05 | Motor Profile Result | N/A | ✅ 4 types | N/A | ✅ | ✅ | ✅ | ✅ | ✅ PASS |
| 06 | Splash | N/A | N/A | N/A | ⬜ | ⬜ | ⬜ | ⬜ | ⚠️ TODO |
| 07 | Onboarding (4 screens) | ✅ 0-100 | ✅ 4 types | N/A | ⬜ | ⬜ | ⬜ | ⬜ | ⚠️ TODO |
| 08 | Create Profile | N/A | N/A | N/A | ⬜ | ⬜ | ⬜ | ⬜ | ⚠️ TODO |
| 09 | Upload | N/A | N/A | N/A | ⬜ | ⬜ | ⬜ | ⬜ | ⚠️ TODO |
| 10 | Processing | N/A | N/A | N/A | ⬜ | ⬜ | ⬜ | ⬜ | ⚠️ TODO |
| 11 | Drills Library | N/A | N/A | N/A | ⬜ | ⬜ | ⬜ | ⬜ | ⚠️ TODO |
| 12 | Progress Dashboard | ✅ 0-100 | N/A | N/A | ⬜ | ⬜ | ⬜ | ⬜ | ⚠️ TODO |
| 13 | Settings | N/A | N/A | N/A | ⬜ | ⬜ | ⬜ | ⬜ | ⚠️ TODO |

**Legend:**
- ✅ = Verified correct
- ⬜ = Not yet reviewed
- ❌ = Needs correction
- N/A = Not applicable to this screen

---

## Detailed Findings

### ✅ SCREENS PASSING (5/13)

#### **SCREEN_01: Home Dashboard** ✅ PASS

**File:** `docs/SCREEN_01_HOME_CORRECTED.md`

**What's Correct:**
- ✅ **KRS Scale:** Displays 75 (0-100 scale) with ADVANCED level badge
- ✅ **Subscores:** Creation 74.8, Transfer 69.5 (both out of 100)
- ✅ **On Table Gain:** "+3.1 mph bat speed available" (mph format)
- ✅ **Level Badge:** Uses 5 levels (FOUNDATION/BUILDING/DEVELOPING/ADVANCED/ELITE) with correct color coding
- ✅ **30-Day Progress:** Chart shows 0-100 KRS scale on y-axis, trending from 70→75
- ✅ **Data Binding:** Complete API specs
  - GET /api/sessions/latest (with full response schema)
  - GET /api/players/{id}/progress?days=30
  - GET /api/players/{id}/recommended-drills
- ✅ **UI Mapping:** Field-by-field mapping documented (krs.total → large number display, etc.)
- ✅ **Responsive:** Mobile (56px KRS) / Tablet (64px) / Desktop (72px)
- ✅ **Accessibility:** ARIA labels for KRS score, level badge has role="status", button has descriptive aria-label
- ✅ **Colors:** Match design-tokens.json (#06B6D4 primary cyan, #10B981 success green)
- ✅ **Typography:** Correct font sizes (72px KRS score desktop, 16px body, 14px captions)
- ✅ **React Implementation:** Complete code examples with helper functions

---

#### **SCREEN_02: Live Mode** ✅ PASS

**File:** `docs/SCREEN_02_LIVE_CORRECTED.md`

**What's Correct:**
- ✅ **Technical Constraints:** Explicitly states 60 FPS camera = positional feedback ONLY
- ✅ **No Overpromising:** Removed exit velocity, launch angle, bat speed (cannot measure at 60 FPS)
- ✅ **Status Pills:** Show positional metrics only
  - Hip Rotation (angle between hips/shoulders)
  - Knee Bend (back leg angle)
  - Lead Leg (stability check)
  - Shoulder Tilt (upper body angle)
  - Weight Transfer (hip position shift)
- ✅ **Coach Cues:** Positional focus ("Drive back knee toward pitcher", "Maintain hip-shoulder separation")
- ✅ **Phase Detection:** Based on pose landmarks (Setup → Load → Launch → Contact → Follow-through)
- ✅ **Recording:** Saves 60 FPS video for future 240 FPS upload to KRS analysis
- ✅ **Clear Distinction:** Live Mode (daily practice) vs KRS Mode (full analysis with 240 FPS)
- ✅ **Data Binding:** Complete API specs for camera stream, pose detection, recording
- ✅ **Responsive:** Landscape orientation recommended (812×375px), portrait fallback
- ✅ **Accessibility:** Voice coaching, haptic feedback, high contrast mode, large touch targets
- ✅ **Colors:** Match design-tokens.json (pose dots cyan #06B6D4, status colors green/yellow/red)

---

#### **SCREEN_03: Player Report** ✅ PASS

**File:** `docs/SCREEN_03_REPORT_CORRECTED.md`

**What's Correct:**
- ✅ **KRS Hero Section:**
  - KRS Total: 75 (0-100 scale, not 0-1000)
  - Level: ADVANCED (5 levels defined)
  - Creation: 74.8 / 100 (formula: Peak momentum / Physical capacity × 100)
  - Transfer: 69.5 / 100 (formula: Output bat speed / Peak momentum × 100)
  - On Table: "+3.1 mph bat speed available"
  - Progress to next level: "5 points from ELITE (85)"
  
- ✅ **4B Framework Cards:**
  - **Brain Card:** Motor Profile (Slingshotter, 92% confidence), Timing (Fast tempo, 0.65s), Characteristics
  - **Body Card:** Creation Score (74.8/100), Physical Capacity (85 mph bat speed), Peak Force (723 N), Kinetic Energy (125 J)
  - **Bat Card:** Transfer Score (69.5/100), Transfer Efficiency (82%), Attack Angle (18°), Hip-Shoulder Sep (45°)
  - **Ball Card:** Current Exit Velo (82 mph), Capacity Exit Velo (95 mph), Gap (+13 mph), Launch Angle (12-18°), Contact Quality (8.2/10)
  
- ✅ **Removed Invented Metrics:**
  - Removed: "Decision: 89", "Recognition: 91" (Brain)
  - Removed: "Power: 92", "Speed: 88", "Flexibility: 84" (Body)
  - Removed: "Path: 87", "Connection: 85" as scored metrics (Bat)
  
- ✅ **4B Colors:** Correct tinted backgrounds
  - Brain: Purple (#EDE9FE bg, #7C3AED text)
  - Body: Blue (#DBEAFE bg, #2563EB text)
  - Bat: Green (#D1FAE5 bg, #059669 text)
  - Ball: Red (#FEE2E2 bg, #DC2626 text)
  
- ✅ **Data Binding:** Complete API specs with session data structure
- ✅ **Responsive:** Mobile (56px KRS) / Tablet / Desktop (72px KRS)
- ✅ **Accessibility:** Complete ARIA labels, keyboard navigation, screen reader support
- ✅ **Component Specs:** KRSHeroCard, BrainCard, BodyCard, BatCard, BallCard all defined

---

#### **SCREEN_04: Movement Assessment** ✅ PASS

**File:** `docs/SCREEN_04_MOVEMENT_ASSESSMENT.md`

**What's Correct:**
- ✅ **All 5 Movements Defined:**
  1. Hip Rotation Test (15 seconds, 5 rotations, measures hip mobility)
  2. T-Spine Rotation Test (15 seconds, upper body separation)
  3. Single-Leg Balance Test (10 seconds per leg, stability)
  4. Squat Assessment (15 seconds, 3 reps, mobility)
  5. Vertical Jump Test (15 seconds, 3 jumps, explosive power)
  
- ✅ **4 States Per Movement:**
  - State 1: Instruction (setup + action steps)
  - State 2: Recording (camera active, pose overlay, 15 seconds)
  - State 3: Analyzing (processing, 5-10 seconds)
  - State 4: Result (metrics, feedback, next button)
  
- ✅ **Motor Profile Algorithm:** Decision tree defined
  - Whipper: hip_rotation >80° AND vertical_jump >24"
  - Spinner: tspine_rotation >70° AND hip_rotation <70°
  - Slingshotter: hip_rotation >75° AND vertical_jump >20" AND balance >8s
  - Titan: squat_depth <90° AND vertical_jump <18"
  - Default: Slingshotter
  
- ✅ **Confidence Calculation:**
  - Base: 70%
  - Consistency bonus: (movements_matching / 5) × 20%
  - Measurement quality: +10% if clear angles detected
  - Result: 70-100% confidence
  
- ✅ **Complete Data Model:** JSON schema with all 5 movement results
- ✅ **API Endpoints:** 4 endpoints documented (start, upload, get result, get final profile)
- ✅ **4 Motor Profiles:** Correctly references Spinner/Slingshotter/Whipper/Titan
- ✅ **Accessibility:** Camera permissions, keyboard nav, screen reader support
- ✅ **Error Handling:** 5 scenarios (camera denied, poor lighting, body not in frame, movement not detected, upload failed)
- ✅ **Performance:** Video compression, caching, progressive upload, offline mode

---

#### **SCREEN_05: Motor Profile Result** ✅ PASS

**File:** `docs/SCREEN_05_MOTOR_PROFILE_RESULT.md`

**What's Correct:**
- ✅ **All 4 Motor Profiles Defined:**
  
  **1. Spinner:**
  - Power source, characteristics, physical traits
  - Strengths: Contact hitting, bat control, handles inside pitches
  - Areas to develop: Lower body power, hip-shoulder separation
  - Athletes: Mookie Betts, José Altuve, Freddie Freeman, Luis Arraez
  - KRS range: 65-80
  
  **2. Slingshotter:**
  - Balanced rotation, explosive power, good timing
  - Strengths: Power+contact balance, consistent hard contact, adaptable
  - Areas to develop: Timing under pressure, transfer efficiency
  - Athletes: Fernando Tatis Jr., Ronald Acuña Jr., Francisco Lindor
  - KRS range: 70-90
  
  **3. Whipper:**
  - Aggressive hip rotation, high rotational velocity, fast tempo
  - Strengths: Elite exit velocity, extra-base power, handles velocity
  - Areas to develop: Bat control on offspeed, timing/discipline
  - Athletes: Juan Soto, Aaron Judge, Yordan Alvarez, Kyle Schwarber
  - KRS range: 75-95
  
  **4. Titan:**
  - Strength-dominant, slower tempo, less mobility
  - Strengths: Power to all fields, driving the ball, strong contact
  - Areas to develop: Mobility/flexibility, swing tempo, rotational efficiency
  - Athletes: Giancarlo Stanton, Pete Alonso, Matt Olson
  - KRS range: 60-75
  
- ✅ **Screen Layout:** ASCII mockup with profile title (32px), confidence badge (green >85%, yellow 70-85%), characteristics, athletes, strengths, continue button
- ✅ **Data Binding:** Complete API spec (GET /api/motor-profile/assessments/{id}/result) with response schema
- ✅ **UI Mapping:** motor_profile.profile → title, confidence → badge, characteristics → checkmark list, etc.
- ✅ **React Implementation:** Complete code with helper functions (getConfidenceBadgeColor, getProfileIcon, getStrengthIcon)
- ✅ **Layout Specs:** Fonts (28-32px title), colors (cyan/green/yellow/red), spacing, margins
- ✅ **Responsive:** Mobile (28px title) / Tablet (30px) / Desktop (32px)
- ✅ **Animations:** Fade-in sequence with stagger timing (title 0.3s, badge 0.5s, illustration 0.6s, etc.)
- ✅ **Accessibility:** ARIA labels, keyboard nav, role="status" for badge
- ✅ **Error Handling:** Low confidence (<70%), assessment incomplete, API error
- ✅ **Analytics Events:** Profile determined, viewed, continue clicked, retake initiated

---

### ⚠️ SCREENS NEEDING REVIEW (8/13)

#### **SCREEN_06: Splash** (Status: Spec exists, needs review)

**File:** `docs/SCREEN_04_SPLASH.md`

**Items to Verify:**
- [ ] Logo display (size, placement)
- [ ] Tagline: "Unlock Your Kinetic Potential"
- [ ] Color tokens match design-tokens.json
- [ ] Auto-advance after 2 seconds
- [ ] Responsive behavior defined
- [ ] Accessibility notes (screen reader announces app name)

---

#### **SCREEN_07: Onboarding** (Status: Spec exists, needs review)

**File:** `docs/SCREEN_05_ONBOARDING.md`

**Items to Verify:**
- [ ] **Screen 1: "What is KRS?"**
  - Explains 0-100 score (not 0-1000)
  - Mentions Creation + Transfer subscores
  - Shows "On Table" gain concept
  
- [ ] **Screen 2: "Motor Profiles"**
  - Shows 4 types: Spinner, Slingshotter, Whipper, Titan (not 6)
  - Brief description of each
  - Icons for each profile
  
- [ ] **Screen 3: "Two Modes"**
  - Live Mode: Daily feedback, 60 FPS camera, positional only
  - KRS Mode: Full analysis, 240 FPS video required
  - Clarifies Live Mode limitations (no exit velo/launch angle)
  
- [ ] **Screen 4: "Track Progress"**
  - Shows KRS journey chart (0-100 scale)
  - Explains 5 levels (FOUNDATION → ELITE)
  - Motivational messaging

**Actions:**
- [ ] Review all 4 onboarding screens for KRS scale consistency
- [ ] Verify Motor Profile terminology (4 types, not 6)
- [ ] Verify Live Mode constraints are explained
- [ ] Update any incorrect references

---

#### **SCREEN_08: Create Profile** (Status: Spec exists, needs review)

**File:** `docs/SCREEN_06_CREATE_PROFILE.md`

**Items to Verify:**
- [ ] Input fields: Name, Age, Height, Weight, Bats (L/R/Switch)
- [ ] Auto-calculate estimated physical capacity from body metrics
- [ ] No incorrect KRS references
- [ ] Data binding spec (POST /api/players endpoint)
- [ ] Validation rules (age 5-99, height/weight reasonable ranges)
- [ ] Responsive behavior
- [ ] Accessibility (labels, error messages)

---

#### **SCREEN_09: Upload** (Status: Spec exists, needs review)

**File:** `docs/SCREEN_07_UPLOAD.md`

**Items to Verify:**
- [ ] 240 FPS requirement warning (not 60 FPS)
- [ ] File size limits (e.g., 500 MB max)
- [ ] Supported formats (MP4, MOV)
- [ ] Preview selected video before upload
- [ ] Data binding spec (POST /api/sessions/upload endpoint)
- [ ] Error handling (file too large, wrong format, network error)
- [ ] Progress indicator during upload
- [ ] Responsive behavior

---

#### **SCREEN_10: Processing** (Status: Spec exists, needs review)

**File:** `docs/SCREEN_08_PROCESSING.md`

**Items to Verify:**
- [ ] Processing time estimate: 60-90 seconds (not 30-45)
- [ ] Progress bar (0-100%)
- [ ] Status updates: "Extracting frames... Detecting poses... Calculating KRS..."
- [ ] No early completion (backend needs full processing time)
- [ ] Error handling (processing failed, network interrupted)
- [ ] Auto-navigate to Report screen when complete
- [ ] Responsive behavior

---

#### **SCREEN_11: Drills Library** (Status: Spec exists, needs review)

**File:** `docs/SCREEN_11_DRILLS_LIBRARY.md`

**Items to Verify:**
- [ ] Drill cards show:
  - Drill name (e.g., "Hip Load Sequence")
  - Focus area aligned with 4B Framework (e.g., "Body - Creation", "Bat - Transfer")
  - Prescription (e.g., "10 reps, 3 sets")
  - Demo video thumbnail
  - Difficulty badge (Beginner/Intermediate/Advanced)
  
- [ ] Filter by focus area:
  - Brain (Motor Profile, Timing)
  - Body (Creation, Power)
  - Bat (Transfer, Efficiency)
  - Ball (Contact Quality)
  
- [ ] Data binding spec (GET /api/drills endpoint)
- [ ] Drill detail screen spec (when user taps drill card)
- [ ] Responsive: Grid layout (1 column mobile, 2 columns tablet, 3 columns desktop)
- [ ] Accessibility

---

#### **SCREEN_12: Progress Dashboard** (Status: Spec exists, needs review)

**File:** `docs/SCREEN_12_PROGRESS_DASHBOARD.md`

**Items to Verify:**
- [ ] **KRS History Chart:**
  - Y-axis: 0-100 scale (not 0-1000)
  - X-axis: Date range (last 30/60/90 days, all time)
  - Line chart showing KRS trend over time
  - Markers for each session
  
- [ ] **Session History List:**
  - Date, KRS Total, Level badge
  - Tap to view full report
  
- [ ] **Growth Indicators:**
  - "+5 points in 30 days"
  - "On track: +0.5 points per week"
  - Progress toward next level
  
- [ ] **Data Binding:**
  - GET /api/players/{id}/progress
  - GET /api/players/{id}/sessions
  
- [ ] Chart library: Recharts or Chart.js (specified)
- [ ] Responsive behavior
- [ ] Accessibility (chart has text alternative)

---

#### **SCREEN_13: Settings** (Status: Spec exists, needs review)

**File:** `docs/SCREEN_13_SETTINGS.md`

**Items to Verify:**
- [ ] **Profile Management:**
  - Edit name, age, height, weight, bats
  - Update motor profile (retake assessment option)
  
- [ ] **Notifications Preferences:**
  - Enable/disable push notifications
  - Email preferences
  
- [ ] **Privacy Settings:**
  - Data sharing preferences
  - Delete account option
  
- [ ] **Account:**
  - Logout
  - Delete account (with confirmation)
  
- [ ] Data binding specs:
  - GET /api/players/{id}/profile
  - PUT /api/players/{id}/profile
  - DELETE /api/players/{id}
  
- [ ] Responsive behavior
- [ ] Accessibility (clear labels, focus management)

---

## Action Items

### **High Priority (Day 3 Morning - 4 hours)**

1. ⬜ Review SCREEN_07_ONBOARDING (verify KRS scale and Motor Profiles in all 4 onboarding screens)
2. ⬜ Review SCREEN_12_PROGRESS (verify KRS chart scale 0-100, not 0-1000)
3. ⬜ Review SCREEN_11_DRILLS (verify focus areas align with 4B Framework)

### **Medium Priority (Day 3 Afternoon - 4 hours)**

4. ⬜ Review SCREEN_06_SPLASH (verify colors, timing, accessibility)
5. ⬜ Review SCREEN_08_CREATE_PROFILE (verify data binding, validation)
6. ⬜ Review SCREEN_09_UPLOAD (verify 240 FPS requirement, file limits)
7. ⬜ Review SCREEN_10_PROCESSING (verify 60-90 second estimate)
8. ⬜ Review SCREEN_13_SETTINGS (verify profile editing, data binding)

### **Low Priority (Day 3 Evening - Optional)**

9. ⬜ Add missing data binding specs to any screen without them
10. ⬜ Verify all screens reference correct design tokens
11. ⬜ Create unified API endpoint documentation (across all screens)

---

## Verification Checklist Template

Use this checklist when reviewing each screen:

### **KRS Scale (if applicable)**
- [ ] All KRS scores shown as 0-100 (not 0-1000 or any other scale)
- [ ] Level labels: FOUNDATION / BUILDING / DEVELOPING / ADVANCED / ELITE
- [ ] Creation and Transfer subscores shown (0-100 each)
- [ ] "On Table" gain shown (mph format)

### **Motor Profile (if applicable)**
- [ ] Only 4 profiles: Spinner, Slingshotter, Whipper, Titan
- [ ] No other profile names (e.g., no "Rotator", "Power Hitter", "Torquer", "Tilter")
- [ ] Confidence shown as percentage (e.g., "92%")
- [ ] Characteristics match profile definitions

### **4B Framework (if applicable)**
- [ ] Brain = Motor Profile + Timing (not "Decision", "Recognition")
- [ ] Body = Creation Score + Physical Capacity (not "Power", "Speed", "Flexibility" scores)
- [ ] Bat = Transfer Score + Efficiency (not "Path", "Connection" scores)
- [ ] Ball = Exit Velocity + Contact Quality (correct)

### **Design Tokens**
- [ ] Colors reference design-tokens.json (e.g., #06B6D4 for primary cyan)
- [ ] Typography references design-tokens.json (e.g., Inter, 72px for KRS score)
- [ ] Spacing uses 8px grid system (8/16/24/32/48/64)

### **Data Binding**
- [ ] API endpoint specified
- [ ] Request/response schema documented
- [ ] UI mapping defined (which API fields go where)

### **Responsive**
- [ ] Mobile behavior defined (320-767px)
- [ ] Tablet behavior defined (768-1023px)
- [ ] Desktop behavior defined (1024px+)

### **Accessibility**
- [ ] ARIA labels specified
- [ ] Keyboard navigation described
- [ ] Focus management noted
- [ ] Screen reader considerations mentioned

---

## Summary Statistics

**Total Screens:** 13  
**Screens Passing:** 5 (38%)  
**Screens Needing Review:** 8 (62%)

**Passing Screens:**
1. Home Dashboard (SCREEN_01)
2. Live Mode (SCREEN_02)
3. Player Report (SCREEN_03)
4. Movement Assessment (SCREEN_04)
5. Motor Profile Result (SCREEN_05)

**Pending Review (High Priority):**
- Onboarding (SCREEN_07)
- Progress Dashboard (SCREEN_12)
- Drills Library (SCREEN_11)

**Pending Review (Medium Priority):**
- Splash (SCREEN_06)
- Create Profile (SCREEN_08)
- Upload (SCREEN_09)
- Processing (SCREEN_10)
- Settings (SCREEN_13)

---

## Next Steps

**Day 3 Morning (4 hours):**
- Review high-priority screens (Onboarding, Progress, Drills)
- Update any incorrect references
- Add missing data binding specs

**Day 3 Afternoon (4 hours):**
- Review medium-priority screens (Splash, Create Profile, Upload, Processing, Settings)
- Verify all screens are consistent with corrected specifications
- Update design token references

**Day 3 Evening (Optional):**
- Create unified API documentation
- Final consistency check across all 13 screens
- Prepare for Day 4 (Design System documentation)

---

## Sign-Off

**Completed by:** Builder 2  
**Date:** December 26, 2025  
**Status:** 5 of 13 screens passing (38%), 8 need review (62%)

**Critical Corrections Complete:**
- ✅ KRS scale: 0-100 validated in 3 screens (Home, Report, and data structure)
- ✅ Motor Profiles: 4 types validated in 3 screens (Report, Movement Assessment, Motor Profile Result)
- ✅ 4B Framework: Correct metrics validated in 1 screen (Report)
- ✅ Live Mode: Positional feedback only validated

**Remaining Work:**
- Day 3: Review 8 screens for consistency with corrected specs
- Day 4: Design System documentation
- Day 5: Final polish and screen flow diagram

---

**STATUS:** ✅ CHECKLIST COMPLETE - Ready for Day 3 review work
