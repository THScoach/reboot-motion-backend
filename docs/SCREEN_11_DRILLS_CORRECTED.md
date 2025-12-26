# Screen 11: Drills Library

**Screen Name:** Drills Library  
**Route:** `/drills`  
**Complexity:** MEDIUM  
**Priority:** P0

**Version:** 2.0  
**Date:** 2025-12-26  
**Status:** Design Specification — Corrected

---

## 📋 Overview

The Drills Library provides personalized drill recommendations organized by the **4B Framework** (Brain, Body, Bat, Ball). Drills target specific KRS gaps identified in the player's latest report.

**Key Features:**
- 10-15 drills organized by 4B Framework
- Personalized recommendations based on KRS gaps
- Drill cards with name, focus area, prescription, duration
- Demo video thumbnails
- Algorithm: IF creation < 80 THEN hip_load_drills; IF transfer < 80 THEN connection_drills

---

## 🎨 Layout (Mobile-First: 375×812)

\`\`\`
┌─────────────────────────────────────┐
│  ← Back           Drills        🔍   │  ← Header (64px)
├─────────────────────────────────────┤
│                                     │
│  Recommended for You                │  ← Section Title
│                                     │
│  Based on your KRS Report:          │
│  Creation 74.8 → Body drills        │
│  Transfer 69.5 → Bat drills         │
│                                     │
│  ┌─────────────────────────────┐    │
│  │ [Drill Card 1]              │    │  ← Drill Card (180px)
│  │ Hip Load Sequence           │    │
│  │ Focus: Body - Creation      │    │
│  │ 10 reps, 3 sets • 5 min     │    │
│  │ [Demo Video Thumb]          │    │
│  └─────────────────────────────┘    │
│                                     │
│  ┌─────────────────────────────┐    │
│  │ [Drill Card 2]              │    │
│  │ Connection Drill            │    │
│  │ Focus: Bat - Transfer       │    │
│  │ 15 reps, 2 sets • 8 min     │    │
│  │ [Demo Video Thumb]          │    │
│  └─────────────────────────────┘    │
│                                     │
│  All Drills                         │  ← Section Title
│                                     │
│  🧠 Brain Drills                    │  ← Category Header
│                                     │
│  ┌──────────┬──────────┬──────────┐ │
│  │ Timing   │ Motor    │ Tempo    │ │  ← 3-column grid
│  │ Drill    │ Profile  │ Control  │ │
│  │ [Thumb]  │ [Thumb]  │ [Thumb]  │ │
│  └──────────┴──────────┴──────────┘ │
│                                     │
│  💪 Body Drills                     │  ← Category Header
│                                     │
│  ┌──────────┬──────────┬──────────┐ │
│  │ Hip Load │ Ground   │ Rotation │ │
│  │ Sequence │ Force    │ Power    │ │
│  │ [Thumb]  │ [Thumb]  │ [Thumb]  │ │
│  └──────────┴──────────┴──────────┘ │
│                                     │
│  🏏 Bat Drills                      │  ← Category Header
│                                     │
│  ┌──────────┬──────────┬──────────┐ │
│  │ Connect  │ Attack   │ Kinetic  │ │
│  │ ion      │ Angle    │ Chain    │ │
│  │ [Thumb]  │ [Thumb]  │ [Thumb]  │ │
│  └──────────┴──────────┴──────────┘ │
│                                     │
│  ⚾ Ball Drills                     │  ← Category Header
│                                     │
│  ┌──────────┬──────────┬──────────┐ │
│  │ Launch   │ Contact  │ Sweet    │ │
│  │ Angle    │ Quality  │ Spot     │ │
│  │ [Thumb]  │ [Thumb]  │ [Thumb]  │ │
│  └──────────┴──────────┴──────────┘ │
│                                     │
└─────────────────────────────────────┘
│  Home  Upload  Report  More        │  ← Bottom Nav (64px)
└─────────────────────────────────────┘
\`\`\`

**Viewport Dimensions:**
- **Width:** 375px (mobile), 768px (tablet), 1024px (desktop)
- **Height:** Variable scroll (est. 1600-2000px)
- **Safe Areas:** Top 44px, Bottom 34px
- **Content Area:** 375×734px (mobile)

---

## 🎨 Component Specifications

### **1. Header (64px)**

**Layout:**
\`\`\`
┌─────────────────────────────────────┐
│  ← Back           Drills        🔍   │
└─────────────────────────────────────┘
\`\`\`

**Elements:**
- **Back Button:** `<` icon, tap to return to previous screen
- **Title:** "Drills" (center, 20px semibold, #111827)
- **Search Icon:** 🔍 (24×24, tap to search drills)

**Styling:**
\`\`\`css
.header {
  height: 64px;
  background: #FAFAFA;
  border-bottom: 1px solid #E5E7EB;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 16px;
}

.back-button {
  font-size: 16px;
  color: #6B7280;
  cursor: pointer;
}

.title {
  font-size: 20px;
  font-weight: 600;
  color: #111827;
}

.search-icon {
  width: 24px;
  height: 24px;
  color: #6B7280;
  cursor: pointer;
}
\`\`\`

---

### **2. Recommended Drills Section (Variable Height)**

**Purpose:** Display personalized drill recommendations based on KRS gaps.

**Recommendation Logic:**
\`\`\`
IF creation_score < 80:
  RECOMMEND Body drills (Hip Load Sequence, Ground Force Generation, Rotational Power)
  
IF transfer_score < 80:
  RECOMMEND Bat drills (Connection Drill, Attack Angle Optimization, Kinetic Chain Sequencing)
  
IF motor_profile_confidence < 90:
  RECOMMEND Brain drills (Timing Recognition, Motor Profile Consistency, Tempo Control)
  
IF exit_velocity_gap > 10 mph:
  RECOMMEND Ball drills (Launch Angle Control, Contact Quality, Sweet Spot Hitting)
\`\`\`

**Header Card:**
\`\`\`
┌─────────────────────────────┐
│ Recommended for You         │  ← Header (16px semibold)
│                             │
│ Based on your KRS Report:   │  ← Explanation (14px)
│ Creation 74.8 → Body drills │
│ Transfer 69.5 → Bat drills  │
└─────────────────────────────┘
\`\`\`

**Drill Card Layout:**
\`\`\`
┌─────────────────────────────┐
│ Hip Load Sequence Drill     │  ← Title (16px semibold)
│ Focus: Body - Creation      │  ← Focus Area (14px)
│ 10 reps, 3 sets • 5 min     │  ← Prescription + Duration (12px)
│                             │
│ [Demo Video Thumbnail]      │  ← 16:9 video thumbnail (320×180)
│                             │
│ Reason: Your creation score │  ← Reason (12px, italic)
│ is 74.8. This drill helps   │
│ improve hip loading for     │
│ +5-8 points.                │
│                             │
│ [Start Drill]               │  ← Primary CTA button
└─────────────────────────────┘
\`\`\`

**Data Structure:**
\`\`\`typescript
interface RecommendedDrill {
  id: string;                    // "drill_hip_load_001"
  name: string;                  // "Hip Load Sequence Drill"
  focus_area: string;            // "Body - Creation"
  category: '4B_Brain' | '4B_Body' | '4B_Bat' | '4B_Ball';
  prescription: string;          // "10 reps, 3 sets"
  duration: string;              // "5 minutes"
  video_url: string;             // URL to demo video
  thumbnail_url: string;         // URL to video thumbnail
  reason: string;                // "Your creation score is 74.8..."
  expected_gain: string;         // "+5-8 points to Creation"
}
\`\`\`

**React Component:**
\`\`\`tsx
interface RecommendedDrillsProps {
  drills: RecommendedDrill[];
  krs_gaps: {
    creation_score: number;      // 74.8
    transfer_score: number;      // 69.5
    motor_confidence: number;    // 92
    exit_velocity_gap: number;   // 13
  };
}

const RecommendedDrills: React.FC<RecommendedDrillsProps> = ({ drills, krs_gaps }) => {
  return (
    <section className="recommended-drills">
      <h2 className="section-title">Recommended for You</h2>
      
      {/* Recommendation Header */}
      <div className="recommendation-header">
        <p className="explanation">Based on your KRS Report:</p>
        {krs_gaps.creation_score < 80 && (
          <p className="gap-item">Creation {krs_gaps.creation_score} → Body drills</p>
        )}
        {krs_gaps.transfer_score < 80 && (
          <p className="gap-item">Transfer {krs_gaps.transfer_score} → Bat drills</p>
        )}
        {krs_gaps.motor_confidence < 90 && (
          <p className="gap-item">Motor Profile {krs_gaps.motor_confidence}% → Brain drills</p>
        )}
        {krs_gaps.exit_velocity_gap > 10 && (
          <p className="gap-item">Exit Velo Gap {krs_gaps.exit_velocity_gap} mph → Ball drills</p>
        )}
      </div>
      
      {/* Drill Cards */}
      {drills.map((drill) => (
        <div key={drill.id} className="recommended-drill-card">
          {/* Title */}
          <h3 className="drill-title">{drill.name}</h3>
          
          {/* Focus Area */}
          <div className="drill-focus">
            <span className="focus-label">Focus:</span>
            <span className="focus-value">{drill.focus_area}</span>
          </div>
          
          {/* Prescription + Duration */}
          <div className="drill-meta">
            <span className="prescription">{drill.prescription}</span>
            <span className="separator">•</span>
            <span className="duration">{drill.duration}</span>
          </div>
          
          {/* Video Thumbnail */}
          <div className="drill-thumbnail">
            <img 
              src={drill.thumbnail_url} 
              alt={`${drill.name} demo video`}
              className="thumbnail-image"
            />
            <div className="play-button">▶</div>
          </div>
          
          {/* Reason */}
          <p className="drill-reason">{drill.reason}</p>
          
          {/* CTA Button */}
          <button className="start-drill-button">Start Drill</button>
        </div>
      ))}
    </section>
  );
};
\`\`\`

**Styling:**
\`\`\`css
.recommended-drills {
  margin-bottom: 32px;
}

.section-title {
  font-size: 20px;
  font-weight: 600;
  color: #111827;
  margin-bottom: 12px;
}

.recommendation-header {
  background: #EFF6FF;
  border: 1px solid #BFDBFE;
  border-radius: 8px;
  padding: 12px 16px;
  margin-bottom: 16px;
}

.explanation {
  font-size: 14px;
  color: #374151;
  margin-bottom: 8px;
}

.gap-item {
  font-size: 14px;
  color: #1F2937;
  margin: 4px 0;
  font-weight: 500;
}

.recommended-drill-card {
  background: #FFFFFF;
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  margin-bottom: 16px;
}

.drill-title {
  font-size: 18px;
  font-weight: 600;
  color: #111827;
  margin-bottom: 8px;
}

.drill-focus {
  font-size: 14px;
  color: #374151;
  margin-bottom: 8px;
}

.focus-label {
  font-weight: 500;
  margin-right: 4px;
}

.focus-value {
  color: #06B6D4;
}

.drill-meta {
  font-size: 12px;
  color: #6B7280;
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  gap: 6px;
}

.separator {
  color: #D1D5DB;
}

.drill-thumbnail {
  position: relative;
  width: 100%;
  aspect-ratio: 16 / 9;
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 12px;
  background: #E5E7EB;
}

.thumbnail-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.play-button {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 48px;
  height: 48px;
  background: rgba(6, 182, 212, 0.9);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #FFFFFF;
  font-size: 20px;
  cursor: pointer;
}

.play-button:hover {
  background: rgba(6, 182, 212, 1);
}

.drill-reason {
  font-size: 12px;
  color: #6B7280;
  font-style: italic;
  margin-bottom: 12px;
  line-height: 1.5;
}

.start-drill-button {
  width: 100%;
  height: 44px;
  background: #06B6D4;
  color: #FFFFFF;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: background 200ms;
}

.start-drill-button:hover {
  background: #0284C7;
}
\`\`\`

---

### **3. All Drills by 4B Framework**

**Purpose:** Display all drills organized by Brain, Body, Bat, Ball categories.

**Category Layout:**
\`\`\`
┌─────────────────────────────┐
│ 🧠 Brain Drills             │  ← Category Header
│                             │
│ ┌────────┬────────┬────────┐│
│ │ Drill  │ Drill  │ Drill  ││  ← 3-column grid (mobile)
│ │   1    │   2    │   3    ││
│ │[Thumb] │[Thumb] │[Thumb] ││
│ └────────┴────────┴────────┘│
└─────────────────────────────┘
\`\`\`

---

#### **3A. Brain Drills (Motor Profile, Timing, Tempo)**

**Drills:**
1. **Timing Recognition Drill**
   - Focus: Brain - Motor Profile
   - Prescription: 20 reps
   - Duration: 5 minutes
   - Description: Practice recognizing pitch timing to improve motor profile consistency

2. **Motor Profile Consistency**
   - Focus: Brain - Motor Profile
   - Prescription: 15 reps, 3 sets
   - Duration: 8 minutes
   - Description: Reinforce Slingshotter motor pattern with consistent swing tempo

3. **Tempo Control Drill**
   - Focus: Brain - Timing
   - Prescription: 10 reps
   - Duration: 4 minutes
   - Description: Practice maintaining consistent swing tempo (0.65s Load-to-Contact)

**Category Header:**
\`\`\`tsx
<div className="category-header brain">
  <span className="category-icon">🧠</span>
  <h3 className="category-title">Brain Drills</h3>
  <p className="category-description">Motor Profile, Timing, Tempo</p>
</div>
\`\`\`

---

#### **3B. Body Drills (Creation, Ground Force, Hip Rotation)**

**Drills:**
1. **Hip Load Sequence Drill**
   - Focus: Body - Creation
   - Prescription: 10 reps, 3 sets
   - Duration: 5 minutes
   - Description: Improve hip loading mechanics for +5-8 points to Creation score
   - Expected Gain: +5-8 points Creation

2. **Ground Force Generation**
   - Focus: Body - Creation
   - Prescription: 15 reps, 2 sets
   - Duration: 7 minutes
   - Description: Maximize ground reaction forces through legs
   - Expected Gain: +3-5 points Creation

3. **Rotational Power Drill**
   - Focus: Body - Creation
   - Prescription: 12 reps, 3 sets
   - Duration: 6 minutes
   - Description: Develop explosive hip rotation power
   - Expected Gain: +4-6 points Creation

**Category Header:**
\`\`\`tsx
<div className="category-header body">
  <span className="category-icon">💪</span>
  <h3 className="category-title">Body Drills</h3>
  <p className="category-description">Creation, Ground Force, Hip Rotation</p>
</div>
\`\`\`

---

#### **3C. Bat Drills (Transfer, Connection, Attack Angle)**

**Drills:**
1. **Connection Drill**
   - Focus: Bat - Transfer
   - Prescription: 15 reps, 2 sets
   - Duration: 8 minutes
   - Description: Improve bat-to-body connection for efficient energy transfer
   - Expected Gain: +6-9 points Transfer

2. **Attack Angle Optimization**
   - Focus: Bat - Transfer
   - Prescription: 10 reps, 3 sets
   - Duration: 6 minutes
   - Description: Optimize attack angle (15-20°) for consistent contact
   - Expected Gain: +4-7 points Transfer

3. **Kinetic Chain Sequencing**
   - Focus: Bat - Transfer
   - Prescription: 12 reps, 2 sets
   - Duration: 7 minutes
   - Description: Perfect the sequence: Hips → Torso → Hands → Bat
   - Expected Gain: +5-8 points Transfer

**Category Header:**
\`\`\`tsx
<div className="category-header bat">
  <span className="category-icon">🏏</span>
  <h3 className="category-title">Bat Drills</h3>
  <p className="category-description">Transfer, Connection, Attack Angle</p>
</div>
\`\`\`

---

#### **3D. Ball Drills (Contact Quality, Launch Angle, Exit Velocity)**

**Drills:**
1. **Launch Angle Control**
   - Focus: Ball - Contact Quality
   - Prescription: 20 reps
   - Duration: 10 minutes
   - Description: Practice achieving optimal launch angle (15-30°)

2. **Contact Quality Drill**
   - Focus: Ball - Contact Quality
   - Prescription: 15 reps, 2 sets
   - Duration: 8 minutes
   - Description: Improve barrel-to-ball contact consistency

3. **Sweet Spot Hitting**
   - Focus: Ball - Exit Velocity
   - Prescription: 10 reps, 3 sets
   - Duration: 6 minutes
   - Description: Practice hitting the barrel's sweet spot for maximum exit velocity

**Category Header:**
\`\`\`tsx
<div className="category-header ball">
  <span className="category-icon">⚾</span>
  <h3 className="category-title">Ball Drills</h3>
  <p className="category-description">Contact Quality, Launch Angle, Exit Velocity</p>
</div>
\`\`\`

---

### **4. Drill Card (Grid Item)**

**Compact Card Layout:**
\`\`\`
┌──────────┐
│ [Thumb]  │  ← Video thumbnail (16:9)
│          │
│ Hip Load │  ← Title (14px semibold)
│ Sequence │
│          │
│ Body     │  ← Category badge (12px)
│ 5 min    │  ← Duration (12px)
└──────────┘
\`\`\`

**Data Structure:**
\`\`\`typescript
interface DrillCard {
  id: string;                    // "drill_hip_load_001"
  name: string;                  // "Hip Load Sequence"
  category: '4B_Brain' | '4B_Body' | '4B_Bat' | '4B_Ball';
  focus_area: string;            // "Body - Creation"
  duration: string;              // "5 minutes"
  thumbnail_url: string;         // URL to thumbnail
  video_url: string;             // URL to full video
}
\`\`\`

**React Component:**
\`\`\`tsx
interface DrillCardProps {
  drill: DrillCard;
  onClick: (drillId: string) => void;
}

const DrillCard: React.FC<DrillCardProps> = ({ drill, onClick }) => {
  return (
    <div className="drill-card" onClick={() => onClick(drill.id)}>
      {/* Thumbnail */}
      <div className="drill-card-thumbnail">
        <img 
          src={drill.thumbnail_url} 
          alt={`${drill.name} demo`}
          className="thumbnail-image"
        />
        <div className="play-icon">▶</div>
      </div>
      
      {/* Title */}
      <h4 className="drill-card-title">{drill.name}</h4>
      
      {/* Category Badge + Duration */}
      <div className="drill-card-meta">
        <span className="category-badge">{drill.category.replace('4B_', '')}</span>
        <span className="duration">{drill.duration}</span>
      </div>
    </div>
  );
};
\`\`\`

**Styling:**
\`\`\`css
.drill-card {
  background: #FFFFFF;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 200ms, box-shadow 200ms;
}

.drill-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
}

.drill-card-thumbnail {
  position: relative;
  width: 100%;
  aspect-ratio: 16 / 9;
  background: #E5E7EB;
}

.thumbnail-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.play-icon {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 32px;
  height: 32px;
  background: rgba(6, 182, 212, 0.9);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #FFFFFF;
  font-size: 14px;
}

.drill-card-title {
  font-size: 14px;
  font-weight: 600;
  color: #111827;
  padding: 12px 12px 8px 12px;
  line-height: 1.3;
  min-height: 44px;
}

.drill-card-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 12px 12px 12px;
  font-size: 12px;
}

.category-badge {
  background: #EFF6FF;
  color: #2563EB;
  padding: 4px 8px;
  border-radius: 4px;
  font-weight: 500;
}

.duration {
  color: #6B7280;
}
\`\`\`

---

## 🔌 Data Binding & API Specifications

### **API Endpoints**

#### **1. GET /api/drills (All Drills)**

**Request:**
\`\`\`http
GET /api/drills
Authorization: Bearer <token>
\`\`\`

**Response Schema:**
\`\`\`typescript
interface DrillsResponse {
  drills: Drill[];
}

interface Drill {
  id: string;                    // "drill_hip_load_001"
  name: string;                  // "Hip Load Sequence Drill"
  category: '4B_Brain' | '4B_Body' | '4B_Bat' | '4B_Ball';
  focus_area: string;            // "Body - Creation"
  prescription: string;          // "10 reps, 3 sets"
  duration: string;              // "5 minutes"
  video_url: string;             // Full demo video URL
  thumbnail_url: string;         // Thumbnail URL
  description: string;           // Long description
  expected_gain: string;         // "+5-8 points Creation"
}
\`\`\`

**Response Example:**
\`\`\`json
{
  "drills": [
    {
      "id": "drill_brain_001",
      "name": "Timing Recognition Drill",
      "category": "4B_Brain",
      "focus_area": "Brain - Motor Profile",
      "prescription": "20 reps",
      "duration": "5 minutes",
      "video_url": "https://cdn.example.com/drills/timing_recognition.mp4",
      "thumbnail_url": "https://cdn.example.com/drills/timing_recognition_thumb.jpg",
      "description": "Practice recognizing pitch timing to improve motor profile consistency.",
      "expected_gain": "+2-4 points Motor Profile Confidence"
    },
    {
      "id": "drill_body_001",
      "name": "Hip Load Sequence Drill",
      "category": "4B_Body",
      "focus_area": "Body - Creation",
      "prescription": "10 reps, 3 sets",
      "duration": "5 minutes",
      "video_url": "https://cdn.example.com/drills/hip_load.mp4",
      "thumbnail_url": "https://cdn.example.com/drills/hip_load_thumb.jpg",
      "description": "Improve hip loading mechanics for increased creation score.",
      "expected_gain": "+5-8 points Creation"
    }
  ]
}
\`\`\`

---

#### **2. GET /api/players/{playerId}/recommended-drills (Personalized Recommendations)**

**Request:**
\`\`\`http
GET /api/players/player_abc123/recommended-drills
Authorization: Bearer <token>
\`\`\`

**Algorithm:**
\`\`\`
1. Fetch player's latest KRS report
2. Identify gaps:
   - IF creation_score < 80 → creation_gap = 80 - creation_score
   - IF transfer_score < 80 → transfer_gap = 80 - transfer_score
   - IF motor_confidence < 90 → confidence_gap = 90 - motor_confidence
   - IF exit_velocity_gap > 10 → velocity_gap = capacity - current
3. Rank gaps by priority:
   - Priority 1: Largest gap
   - Priority 2: Second largest
   - Priority 3: Third largest
4. Select 3-5 drills targeting top gaps:
   - IF creation_gap largest → Body drills (Hip Load, Ground Force, Rotation)
   - IF transfer_gap largest → Bat drills (Connection, Attack Angle, Kinetic Chain)
   - IF confidence_gap largest → Brain drills (Timing, Motor Profile, Tempo)
   - IF velocity_gap largest → Ball drills (Launch Angle, Contact Quality, Sweet Spot)
5. Return drills with reasons
\`\`\`

**Response Schema:**
\`\`\`typescript
interface RecommendedDrillsResponse {
  player_id: string;
  krs_gaps: {
    creation_score: number;      // 74.8
    creation_gap: number;        // 5.2 (80 - 74.8)
    transfer_score: number;      // 69.5
    transfer_gap: number;        // 10.5 (80 - 69.5)
    motor_confidence: number;    // 92
    confidence_gap: number;      // 0 (no gap)
    exit_velocity_gap: number;   // 13 mph
  };
  recommended_drills: RecommendedDrill[];
}
\`\`\`

**Response Example:**
\`\`\`json
{
  "player_id": "player_abc123",
  "krs_gaps": {
    "creation_score": 74.8,
    "creation_gap": 5.2,
    "transfer_score": 69.5,
    "transfer_gap": 10.5,
    "motor_confidence": 92,
    "confidence_gap": 0,
    "exit_velocity_gap": 13
  },
  "recommended_drills": [
    {
      "id": "drill_bat_001",
      "name": "Connection Drill",
      "category": "4B_Bat",
      "focus_area": "Bat - Transfer",
      "prescription": "15 reps, 2 sets",
      "duration": "8 minutes",
      "video_url": "https://cdn.example.com/drills/connection.mp4",
      "thumbnail_url": "https://cdn.example.com/drills/connection_thumb.jpg",
      "reason": "Your transfer score is 69.5. This drill improves bat-to-body connection for +6-9 points to Transfer.",
      "expected_gain": "+6-9 points Transfer"
    },
    {
      "id": "drill_body_001",
      "name": "Hip Load Sequence Drill",
      "category": "4B_Body",
      "focus_area": "Body - Creation",
      "prescription": "10 reps, 3 sets",
      "duration": "5 minutes",
      "video_url": "https://cdn.example.com/drills/hip_load.mp4",
      "thumbnail_url": "https://cdn.example.com/drills/hip_load_thumb.jpg",
      "reason": "Your creation score is 74.8. This drill improves hip loading mechanics for +5-8 points to Creation.",
      "expected_gain": "+5-8 points Creation"
    },
    {
      "id": "drill_ball_001",
      "name": "Launch Angle Control",
      "category": "4B_Ball",
      "focus_area": "Ball - Contact Quality",
      "prescription": "20 reps",
      "duration": "10 minutes",
      "video_url": "https://cdn.example.com/drills/launch_angle.mp4",
      "thumbnail_url": "https://cdn.example.com/drills/launch_angle_thumb.jpg",
      "reason": "Your exit velocity gap is 13 mph. This drill helps achieve optimal launch angle for better contact.",
      "expected_gain": "+2-4 mph Exit Velocity"
    }
  ]
}
\`\`\`

---

### **React/TypeScript Implementation**

\`\`\`tsx
'use client';

import { useEffect, useState } from 'react';

interface DrillsPageProps {
  playerId: string;
}

const DrillsPage: React.FC<DrillsPageProps> = ({ playerId }) => {
  const [recommendedDrills, setRecommendedDrills] = useState<RecommendedDrillsResponse | null>(null);
  const [allDrills, setAllDrills] = useState<Drill[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchDrills() {
      try {
        setLoading(true);
        
        // Fetch recommended drills
        const recommendedRes = await fetch(`/api/players/${playerId}/recommended-drills`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('auth_token')}`,
          },
        });

        if (!recommendedRes.ok) {
          throw new Error(`Failed to fetch recommended drills: ${recommendedRes.status}`);
        }

        const recommendedData = await recommendedRes.json();
        setRecommendedDrills(recommendedData);

        // Fetch all drills
        const allDrillsRes = await fetch('/api/drills', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('auth_token')}`,
          },
        });

        if (!allDrillsRes.ok) {
          throw new Error(`Failed to fetch all drills: ${allDrillsRes.status}`);
        }

        const allDrillsData = await allDrillsRes.json();
        setAllDrills(allDrillsData.drills);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error');
      } finally {
        setLoading(false);
      }
    }

    fetchDrills();
  }, [playerId]);

  if (loading) return <div className="loading">Loading drills...</div>;
  if (error) return <div className="error">Error: {error}</div>;

  // Group drills by category
  const drillsByCategory = {
    '4B_Brain': allDrills.filter(d => d.category === '4B_Brain'),
    '4B_Body': allDrills.filter(d => d.category === '4B_Body'),
    '4B_Bat': allDrills.filter(d => d.category === '4B_Bat'),
    '4B_Ball': allDrills.filter(d => d.category === '4B_Ball'),
  };

  return (
    <div className="drills-page">
      {/* Header */}
      <header className="header">
        <button className="back-button">← Back</button>
        <h1 className="title">Drills</h1>
        <button className="search-icon">🔍</button>
      </header>

      {/* Recommended Drills */}
      {recommendedDrills && (
        <RecommendedDrills 
          drills={recommendedDrills.recommended_drills} 
          krs_gaps={recommendedDrills.krs_gaps}
        />
      )}

      {/* All Drills by Category */}
      <section className="all-drills">
        <h2 className="section-title">All Drills</h2>
        
        {/* Brain Drills */}
        <div className="category-section">
          <div className="category-header brain">
            <span className="category-icon">🧠</span>
            <h3 className="category-title">Brain Drills</h3>
            <p className="category-description">Motor Profile, Timing, Tempo</p>
          </div>
          
          <div className="drill-grid">
            {drillsByCategory['4B_Brain'].map(drill => (
              <DrillCard key={drill.id} drill={drill} onClick={(id) => console.log(id)} />
            ))}
          </div>
        </div>

        {/* Body Drills */}
        <div className="category-section">
          <div className="category-header body">
            <span className="category-icon">💪</span>
            <h3 className="category-title">Body Drills</h3>
            <p className="category-description">Creation, Ground Force, Hip Rotation</p>
          </div>
          
          <div className="drill-grid">
            {drillsByCategory['4B_Body'].map(drill => (
              <DrillCard key={drill.id} drill={drill} onClick={(id) => console.log(id)} />
            ))}
          </div>
        </div>

        {/* Bat Drills */}
        <div className="category-section">
          <div className="category-header bat">
            <span className="category-icon">🏏</span>
            <h3 className="category-title">Bat Drills</h3>
            <p className="category-description">Transfer, Connection, Attack Angle</p>
          </div>
          
          <div className="drill-grid">
            {drillsByCategory['4B_Bat'].map(drill => (
              <DrillCard key={drill.id} drill={drill} onClick={(id) => console.log(id)} />
            ))}
          </div>
        </div>

        {/* Ball Drills */}
        <div className="category-section">
          <div className="category-header ball">
            <span className="category-icon">⚾</span>
            <h3 className="category-title">Ball Drills</h3>
            <p className="category-description">Contact Quality, Launch Angle, Exit Velocity</p>
          </div>
          
          <div className="drill-grid">
            {drillsByCategory['4B_Ball'].map(drill => (
              <DrillCard key={drill.id} drill={drill} onClick={(id) => console.log(id)} />
            ))}
          </div>
        </div>
      </section>

      {/* Bottom Navigation */}
      <nav className="bottom-nav">
        <button className="nav-item">Home</button>
        <button className="nav-item">Upload</button>
        <button className="nav-item">Report</button>
        <button className="nav-item active">More</button>
      </nav>
    </div>
  );
};

export default DrillsPage;
\`\`\`

---

## 📱 Responsive Behavior

### **Mobile (375px)**
- Drill grid: 3 columns (tight spacing)
- Recommended drills: Full width cards
- Category headers: Collapsible (optional)

### **Tablet (768px)**
- Drill grid: 4 columns
- Recommended drills: 2 columns
- Larger thumbnails

### **Desktop (1024px+)**
- Drill grid: 5-6 columns
- Recommended drills: 3 columns
- Max-width: 1200px (centered)

**Media Queries:**
\`\`\`css
/* Mobile-first (default) */
.drill-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}

/* Tablet */
@media (min-width: 768px) {
  .drill-grid {
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
  }
  
  .recommended-drills {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 16px;
  }
}

/* Desktop */
@media (min-width: 1024px) {
  .drills-page {
    max-width: 1200px;
    margin: 0 auto;
  }
  
  .drill-grid {
    grid-template-columns: repeat(5, 1fr);
    gap: 20px;
  }
  
  .recommended-drills {
    grid-template-columns: repeat(3, 1fr);
  }
}
\`\`\`

---

## ♿ Accessibility

### **Keyboard Navigation**
- Tab order: Header → Recommended drills → Category sections → Drill cards
- Focus indicators: 2px solid #06B6D4 outline
- Arrow keys: Navigate within drill grids

### **Screen Reader Support**
\`\`\`tsx
<div role="region" aria-label="Recommended Drills">
  {/* Recommended drills content */}
</div>

<div role="region" aria-label="All Drills by Category">
  {/* All drills content */}
</div>
\`\`\`

### **Video Accessibility**
- Captions: All demo videos have captions
- Transcripts: Text descriptions available
- Playback controls: Keyboard-accessible (Space = play/pause)

---

## 🎯 Success Criteria

**Drills Library passes when:**

1. ✅ 10-15 drills organized by 4B Framework (Brain, Body, Bat, Ball)
2. ✅ Personalized recommendations based on KRS gaps
3. ✅ Algorithm: IF creation < 80 THEN Body drills; IF transfer < 80 THEN Bat drills
4. ✅ Drill cards with name, focus area, prescription, duration
5. ✅ Demo video thumbnails (16:9 aspect ratio)
6. ✅ Complete API specs: GET /api/drills, GET /api/players/{id}/recommended-drills
7. ✅ React/TypeScript implementation
8. ✅ Responsive behavior (mobile/tablet/desktop)
9. ✅ Accessibility (keyboard nav, screen reader, video captions)

---

**Priority:** P0 — High Priority  
**Complexity:** MEDIUM  
**Est. Time:** 6-8 hours (Phase 1)

---

*Last Updated: December 26, 2025*
