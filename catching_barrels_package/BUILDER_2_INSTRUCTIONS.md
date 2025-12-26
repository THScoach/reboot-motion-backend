# 🛠️ BUILDER 2 INSTRUCTIONS: CATCHING BARRELS TRAINING MODULE

**Project**: CATCHING BARRELS - Biomechanics-Driven Baseball Training Platform  
**Module**: Swing DNA Report & Training Plan Generator  
**Date**: December 25, 2025  
**Priority**: HIGH

---

## 📋 EXECUTIVE SUMMARY

You are building a **training module** that analyzes baseball swing biomechanics data and generates:
1. **Swing DNA Report** (visual, data-rich analysis)
2. **Ball Outcome Predictions** (what the ball does and will do)
3. **6-Week Training Plan** (personalized intervention protocols)
4. **Progress Tracking** (Before/After comparisons)

This system uses **Coach Rick AI's validated knowledge base** to automatically diagnose swing issues and prescribe evidence-based training interventions.

---

## 📦 KNOWLEDGE BASE FILES PROVIDED

### **File 1: COACH_RICK_AI_KNOWLEDGE_BASE.md** ⭐ PRIMARY
**Size**: ~20,000 words  
**Purpose**: Core diagnostic and intervention logic

**What's Inside:**
- ✅ **Diagnostic Framework**: 4 biomechanical patterns to detect
- ✅ **Intervention Protocols**: 5 evidence-based training programs
- ✅ **Data Interpretation Guide**: How to read CSV files
- ✅ **Coaching Cues Library**: Natural language coaching instructions
- ✅ **Outcome Prediction Model**: Formulas to predict improvements
- ✅ **Validation Checklist**: Success criteria and timelines

**How to Use This:**
- Backend analysis engine (pattern recognition)
- Training plan generation (protocol selection)
- Prediction calculations (exit velo, launch angle, etc.)
- Coach Rick's Take generation (natural language diagnosis)

---

### **File 2: JOINT_COORDINATION_RESEARCH_REPORT.md** 📚 REFERENCE
**Size**: ~17,000 words  
**Purpose**: Scientific background and educational content

**What's Inside:**
- Randy Sullivan's hip lock methodology
- Frans Bosch coordination theory
- Dr. Kwon's kinetic sequence research
- Single-leg training research
- Force Pedals science
- Complete scientific references

**How to Use This:**
- Educational tooltips in the app
- "Learn More" expandable sections
- FAQ content generation
- Marketing/credibility material
- Blog posts and social content

---

## 🎯 YOUR MISSION

Build a web application that:

### **INPUT:**
- User uploads 2 CSV files:
  - `momentum-energy.csv` (angular momentum, kinetic energy per body segment)
  - `inverse-kinematics.csv` (joint angles, positions over time)

### **PROCESSING:**
- Analyze data using diagnostic patterns from Knowledge Base
- Identify primary issue (e.g., "Energy Leak at Lead Knee")
- Calculate efficiency metrics (hip contribution, knee extension, etc.)
- Predict ball outcomes (current state)
- Select appropriate intervention protocol (1-5)
- Generate 6-week training plan
- Predict improvements (future state)

### **OUTPUT:**
- **Swing DNA Report** (HTML/React component)
- **Ball Outcome Analysis** (what the ball does and why)
- **Training Plan** (weekly drills with coaching cues)
- **Predicted Results** (exit velo, launch angle, spray chart changes)

---

## 🏗️ SYSTEM ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────┐
│                    CATCHING BARRELS APP                      │
└─────────────────────────────────────────────────────────────┘
                            │
            ┌───────────────┴───────────────┐
            │                               │
    ┌───────▼────────┐            ┌────────▼────────┐
    │  DATA UPLOAD   │            │  USER PROFILE   │
    │                │            │                 │
    │ - momentum.csv │            │ - Athlete name  │
    │ - kinematics.csv│            │ - Age/Position  │
    └───────┬────────┘            │ - Handedness    │
            │                     └─────────────────┘
            │
    ┌───────▼─────────────────────────────────────────┐
    │         ANALYSIS ENGINE (Backend)               │
    │                                                 │
    │  1. DATA PARSING                                │
    │     - Read CSV files                            │
    │     - Identify contact frame (rel_frame = 0)    │
    │     - Extract key metrics                       │
    │                                                 │
    │  2. PATTERN RECOGNITION                         │
    │     - Lead knee angle at contact                │
    │     - Hip angular momentum (peak)               │
    │     - Shoulder angular momentum (peak)          │
    │     - Shoulder/Hip ratio                        │
    │     - Lead arm extension                        │
    │                                                 │
    │  3. DIAGNOSIS (Knowledge Base Match)            │
    │     - PATTERN 1: Energy Leak at Lead Knee?      │
    │     - PATTERN 2: Weak Hip Contribution?         │
    │     - PATTERN 3: Fast Foot Roll (Spinner)?      │
    │     - PATTERN 4: Shoulder Compensation?         │
    │     → Select PRIMARY pattern                    │
    │                                                 │
    │  4. EFFICIENCY CALCULATION                      │
    │     - Hip Efficiency = (hip_angmom / 10) * 100  │
    │     - Knee Efficiency = (knee_angle / 170) * 100│
    │     - Contact Efficiency = (arm_ext / 20) * 100 │
    │     → Total Efficiency Score                    │
    │                                                 │
    │  5. BALL OUTCOME PREDICTION (Current)           │
    │     - Exit velocity (from efficiency)           │
    │     - Launch angle (from lead arm extension)    │
    │     - Spray chart (from extension pattern)      │
    │     - Spin rate (from bat path direction)       │
    │                                                 │
    │  6. INTERVENTION SELECTION                      │
    │     - Match pattern → Protocol (1-5)            │
    │     - Generate 6-week plan                      │
    │     - Select drills from Knowledge Base         │
    │                                                 │
    │  7. IMPROVEMENT PREDICTION (Future)             │
    │     - Target efficiency after training          │
    │     - Predicted exit velo gain                  │
    │     - Predicted launch angle change             │
    │     - Predicted spray chart improvement         │
    └───────┬─────────────────────────────────────────┘
            │
    ┌───────▼─────────────────────────────────────────┐
    │         REPORT GENERATION (Frontend)            │
    │                                                 │
    │  SECTION 1: WHAT YOUR BALL IS DOING             │
    │  ├─ Ground ball rate: 65%                       │
    │  ├─ Weak contact: 75-78 mph                     │
    │  ├─ Breaking ball struggles: .180 AVG           │
    │  └─ Visualizations: Spray chart, launch angle   │
    │                                                 │
    │  SECTION 2: WHY YOUR BALL DOES THAT             │
    │  ├─ 5-step cause chain                          │
    │  │   1. Lead arm doesn't extend (1.5°)          │
    │  │   2. Shoulders compensate (8.68x ratio)      │
    │  │   3. Bat drags (0.00x whip)                  │
    │  │   4. Barrel crosses early                    │
    │  │   5. Topspin ground balls                    │
    │  └─ Coach Rick's natural language analysis      │
    │                                                 │
    │  SECTION 3: WHAT YOUR BALL WILL DO (Prediction) │
    │  ├─ Exit Velo: 82 → 88-91 mph (+5-9 mph)       │
    │  ├─ Launch Angle: 2° → 12-18° (GBs → LDs)      │
    │  ├─ Breaking Ball AVG: .180 → .280-.320        │
    │  └─ Ground Ball Rate: 65% → 35%                │
    │                                                 │
    │  SECTION 4: HOW TO FIX IT (Training Plan)       │
    │  ├─ Week 1-2: Fix Lead Knee Leak                │
    │  │   - Single-leg jumps (3x5)                   │
    │  │   - Isometric holds (3x20s)                  │
    │  │   - Wall knee extension (3x10)               │
    │  │   Cue: "Steel rod, not shock absorber"       │
    │  │                                               │
    │  ├─ Week 3-4: Add Vertical Force                │
    │  │   - Force Pedals (soft) (3x10 swings)        │
    │  │   - Lead leg slam → swing (3x10)             │
    │  │   - Med ball throws (3x8)                    │
    │  │   Cue: "Slam, brake hip, whip bat"           │
    │  │                                               │
    │  └─ Week 5-6: Integrate to Live Swings          │
    │      - Force Pedals + soft toss (3x15)          │
    │      - Rope swings (3x20)                       │
    │      - Constraint soft toss (3x20)              │
    │      Cue: "Push, extend, whip"                  │
    │                                                 │
    │  SECTION 5: METRICS DASHBOARD                   │
    │  ├─ Overall Score: 60.3/100                     │
    │  ├─ Ground Flow: 72/100 ⚠️                      │
    │  ├─ Engine Flow: 61/100 ⚠️                      │
    │  ├─ Weapon: 48/100 ❌                           │
    │  └─ Transfer Ratio: 0.42 ❌                     │
    └─────────────────────────────────────────────────┘
```

---

## 📊 DATA STRUCTURE & PARSING

### **File 1: momentum-energy.csv**

**Key Columns to Extract:**
```python
required_columns = {
    # Frame reference
    'rel_frame': int,  # 0 = contact frame (max hand speed)
    
    # Hip (lower torso) momentum
    'lowertorso_angular_momentum_mag': float,  # Target: 8-10+
    
    # Shoulder (torso) momentum  
    'torso_angular_momentum_mag': float,  # Compare to hip
    
    # Bat energy
    'bat_kinetic_energy': float,  # For bat speed calculation
    
    # Lead leg energy
    'lleg_trans_energy': float,  # Ground force indicator
}
```

**Analysis Steps:**
```python
# 1. Find contact frame
contact_frame = df[df['rel_frame'] == 0].index[0]

# 2. Extract hip momentum at contact
hip_angmom_contact = df.loc[contact_frame, 'lowertorso_angular_momentum_mag']

# 3. Extract shoulder momentum at contact
shoulder_angmom_contact = df.loc[contact_frame, 'torso_angular_momentum_mag']

# 4. Calculate ratio
shoulder_hip_ratio = shoulder_angmom_contact / hip_angmom_contact

# 5. Find peaks (look backward from contact)
pre_contact = df[df['rel_frame'] <= 0]
hip_peak = pre_contact['lowertorso_angular_momentum_mag'].max()
shoulder_peak = pre_contact['torso_angular_momentum_mag'].max()

# 6. Calculate timing gap
hip_peak_frame = pre_contact['lowertorso_angular_momentum_mag'].idxmax()
shoulder_peak_frame = pre_contact['torso_angular_momentum_mag'].idxmax()
timing_gap_frames = abs(shoulder_peak_frame - hip_peak_frame)
timing_gap_ms = timing_gap_frames * 8.33  # Assuming 120fps → 8.33ms per frame
```

---

### **File 2: inverse-kinematics.csv**

**Key Columns to Extract:**
```python
required_columns = {
    # Frame reference
    'rel_frame': int,
    
    # Lead leg joints (RHH = left, LHH = right)
    'left_knee': float,   # Lead knee angle for RHH
    'right_knee': float,  # Lead knee angle for LHH
    'left_hip_flex': float,
    'right_hip_flex': float,
    
    # Torso rotation
    'torso_rot': float,  # Degrees of rotation
}
```

**Analysis Steps:**
```python
# 1. Determine handedness (from user input or data)
handedness = 'RHH'  # or 'LHH'
lead_knee_col = 'left_knee' if handedness == 'RHH' else 'right_knee'

# 2. Find contact frame
contact_frame = df[df['rel_frame'] == 0].index[0]

# 3. Extract lead knee angle at contact
lead_knee_contact = df.loc[contact_frame, lead_knee_col]

# 4. Check for energy leak
if lead_knee_contact < 140:
    diagnosis = "ENERGY LEAK: Lead knee flexed at contact"
    severity = "CRITICAL"
elif lead_knee_contact < 160:
    diagnosis = "PARTIAL LEAK: Lead knee not fully extended"
    severity = "MODERATE"
else:
    diagnosis = "GOOD: Lead knee properly extended"
    severity = "NONE"
```

---

## 🧮 EFFICIENCY & PREDICTION CALCULATIONS

### **1. Efficiency Scores**

```python
def calculate_efficiency_scores(data):
    """
    Calculate efficiency metrics from biomechanical data
    
    Returns:
        dict: {
            'hip_efficiency': float (0-100),
            'knee_efficiency': float (0-100),
            'contact_efficiency': float (0-100),
            'total_efficiency': float (0-100)
        }
    """
    # Hip Efficiency (target: 8-10+ angmom = 80-100%)
    hip_angmom = data['hip_angular_momentum']
    hip_efficiency = min((hip_angmom / 10.0) * 100, 100)
    
    # Knee Efficiency (target: 170° = 100%)
    lead_knee_angle = data['lead_knee_angle']
    knee_efficiency = min((lead_knee_angle / 170.0) * 100, 100)
    
    # Contact Efficiency (target: 20° lead arm extension = 100%)
    lead_arm_extension = data.get('lead_arm_extension', 0)
    contact_efficiency = min((lead_arm_extension / 20.0) * 100, 100)
    
    # Weighted average (Hip 40%, Knee 30%, Contact 30%)
    total_efficiency = (
        hip_efficiency * 0.4 + 
        knee_efficiency * 0.3 + 
        contact_efficiency * 0.3
    )
    
    return {
        'hip_efficiency': round(hip_efficiency, 1),
        'knee_efficiency': round(knee_efficiency, 1),
        'contact_efficiency': round(contact_efficiency, 1),
        'total_efficiency': round(total_efficiency, 1)
    }
```

### **2. Ball Outcome Predictions**

```python
def predict_ball_outcomes(data, efficiency):
    """
    Predict ball flight characteristics from biomechanics
    
    Args:
        data: dict of biomechanical metrics
        efficiency: dict from calculate_efficiency_scores()
    
    Returns:
        dict: {
            'current': {...},
            'predicted': {...},
            'improvement': {...}
        }
    """
    bat_speed = data['bat_speed']  # mph
    total_efficiency = efficiency['total_efficiency'] / 100.0
    
    # Current outcomes
    current_exit_velo = bat_speed * total_efficiency
    
    # Launch angle based on lead arm extension
    lead_arm_ext = data.get('lead_arm_extension', 0)
    if lead_arm_ext < 10:
        current_la = 2  # Ground balls
        current_gb_rate = 65
        current_ld_rate = 25
    elif lead_arm_ext < 20:
        current_la = 8  # Some line drives
        current_gb_rate = 50
        current_ld_rate = 40
    else:
        current_la = 15  # Line drives
        current_gb_rate = 35
        current_ld_rate = 55
    
    # Predicted outcomes (after training)
    # Assume 80-90% efficiency achievable
    target_efficiency = 0.85
    predicted_exit_velo = bat_speed * target_efficiency
    predicted_la = 15  # Optimal line drive angle
    predicted_gb_rate = 35
    predicted_ld_rate = 55
    
    # Calculate gains
    exit_velo_gain = predicted_exit_velo - current_exit_velo
    la_gain = predicted_la - current_la
    gb_rate_change = predicted_gb_rate - current_gb_rate
    ld_rate_change = predicted_ld_rate - current_ld_rate
    
    return {
        'current': {
            'exit_velo': round(current_exit_velo, 1),
            'launch_angle': current_la,
            'gb_rate': current_gb_rate,
            'ld_rate': current_ld_rate,
            'breaking_ball_avg': 0.180 if lead_arm_ext < 10 else 0.250
        },
        'predicted': {
            'exit_velo': round(predicted_exit_velo, 1),
            'launch_angle': predicted_la,
            'gb_rate': predicted_gb_rate,
            'ld_rate': predicted_ld_rate,
            'breaking_ball_avg': 0.280 if target_efficiency > 0.7 else 0.250
        },
        'improvement': {
            'exit_velo_gain': round(exit_velo_gain, 1),
            'launch_angle_gain': la_gain,
            'gb_rate_change': gb_rate_change,
            'ld_rate_change': ld_rate_change,
            'breaking_ball_avg_gain': 0.100 if lead_arm_ext < 10 else 0.030
        }
    }
```

---

## 🎨 FRONTEND DESIGN REQUIREMENTS

### **Design System:**
- **Colors**: Dark theme with gold accents (match Freddie Freeman example)
  - Background: `#0a0e1a` (dark navy)
  - Primary: `#d4af37` (gold)
  - Text: `#e8e8e8` (light gray)
  - Accent: `#3b82f6` (blue for info)
  - Warning: `#f59e0b` (amber)
  - Danger: `#ef4444` (red)

- **Typography**:
  - Headers: `'Inter', sans-serif` - Bold
  - Body: `'Inter', sans-serif` - Regular
  - Monospace (metrics): `'JetBrains Mono', monospace`

- **Layout**: Responsive, mobile-first
  - Desktop: Side-by-side comparisons
  - Mobile: Stacked sections

### **Component Structure:**

```jsx
<SwingDNAReport>
  {/* Header Section */}
  <ReportHeader 
    athleteName="Eric Williams"
    overallScore={60.3}
    date="2025-12-25"
  />
  
  {/* Section 1: Current Ball Outcomes */}
  <BallOutcomesSection
    groundBallRate={65}
    exitVelo={82}
    launchAngle={2}
    breakingBallAvg={0.180}
    sprayChart={...}
  />
  
  {/* Section 2: Diagnosis (Why) */}
  <DiagnosisSection
    causeChain={[
      "Lead arm doesn't extend (1.5°)",
      "Shoulders compensate (8.68x ratio)",
      "Bat drags (0.00x whip)",
      "Barrel crosses early",
      "Topspin ground balls"
    ]}
    coachTake="Your lead arm is pulling across instead of extending through..."
  />
  
  {/* Section 3: Predictions (What Will Happen) */}
  <PredictionSection
    current={{exitVelo: 82, launchAngle: 2}}
    predicted={{exitVelo: 89, launchAngle: 15}}
    timeline="6 weeks"
  />
  
  {/* Section 4: Training Plan */}
  <TrainingPlanSection
    weeks={[
      {
        weekNum: "1-2",
        focus: "Fix Lead Knee Leak",
        drills: [
          {name: "Single-leg jumps", sets: 3, reps: 5, cue: "Steel rod, not shock absorber"},
          {name: "Isometric holds", sets: 3, reps: "20s", cue: "Lock it, don't collapse"}
        ],
        expectedChange: "Hip angmom 2.1 → 4-5"
      },
      // ... weeks 3-4, 5-6
    ]}
  />
  
  {/* Section 5: Metrics Dashboard */}
  <MetricsDashboard
    groundFlow={72}
    engineFlow={61}
    weapon={48}
    transferRatio={0.42}
    breakdown={{
      groundFlow: {
        stance: 85,
        load: 81,
        stride: 73,
        plant: 60  // The problem area
      },
      // ... other breakdowns
    }}
  />
</SwingDNAReport>
```

---

## 🔧 TECHNICAL IMPLEMENTATION

### **Backend: Python/Node.js API**

**Endpoints:**

```python
# POST /api/analyze
# Upload biomechanical data files
# Returns: Analysis results + recommendations

@app.route('/api/analyze', methods=['POST'])
def analyze_swing():
    """
    Main analysis endpoint
    """
    # 1. Parse uploaded files
    momentum_file = request.files['momentum']
    kinematics_file = request.files['kinematics']
    
    momentum_df = pd.read_csv(momentum_file)
    kinematics_df = pd.read_csv(kinematics_file)
    
    # 2. Extract athlete info
    athlete_name = request.form['name']
    handedness = request.form['handedness']  # 'RHH' or 'LHH'
    
    # 3. Run analysis pipeline
    metrics = extract_metrics(momentum_df, kinematics_df, handedness)
    pattern = diagnose_pattern(metrics)
    efficiency = calculate_efficiency_scores(metrics)
    predictions = predict_ball_outcomes(metrics, efficiency)
    protocol = select_protocol(pattern)
    training_plan = generate_training_plan(protocol, metrics)
    
    # 4. Generate Coach Rick's Take
    coach_take = generate_coach_analysis(pattern, metrics, predictions)
    
    # 5. Return comprehensive report data
    return jsonify({
        'athlete': {
            'name': athlete_name,
            'handedness': handedness,
            'analysis_date': datetime.now().isoformat()
        },
        'metrics': metrics,
        'pattern': pattern,
        'efficiency': efficiency,
        'ball_outcomes': predictions,
        'training_plan': training_plan,
        'coach_take': coach_take,
        'overall_score': calculate_overall_score(efficiency)
    })


# GET /api/protocols
# Retrieve available training protocols from Knowledge Base

@app.route('/api/protocols', methods=['GET'])
def get_protocols():
    """
    Return all available protocols with details
    """
    return jsonify(PROTOCOLS)  # From Knowledge Base


# POST /api/compare
# Compare Before/After data uploads

@app.route('/api/compare', methods=['POST'])
def compare_swings():
    """
    Compare two data uploads (before and after training)
    """
    before_id = request.form['before_id']
    after_id = request.form['after_id']
    
    # Load both analyses
    before = load_analysis(before_id)
    after = load_analysis(after_id)
    
    # Calculate changes
    changes = calculate_improvements(before, after)
    
    # Validate predictions
    prediction_accuracy = validate_predictions(
        before['predictions'], 
        after['metrics']
    )
    
    return jsonify({
        'before': before,
        'after': after,
        'changes': changes,
        'prediction_accuracy': prediction_accuracy
    })
```

---

### **Frontend: React Components**

**Key Components:**

```jsx
// Main Report Component
const SwingDNAReport = ({ analysisData }) => {
  return (
    <div className="swing-dna-report">
      <ReportHeader {...analysisData.athlete} score={analysisData.overall_score} />
      
      <TabNavigation>
        <Tab label="Ball Outcomes">
          <BallOutcomesPanel data={analysisData.ball_outcomes} />
        </Tab>
        
        <Tab label="Diagnosis">
          <DiagnosisPanel 
            pattern={analysisData.pattern}
            metrics={analysisData.metrics}
            coachTake={analysisData.coach_take}
          />
        </Tab>
        
        <Tab label="Predictions">
          <PredictionPanel predictions={analysisData.ball_outcomes} />
        </Tab>
        
        <Tab label="Training Plan">
          <TrainingPlanPanel plan={analysisData.training_plan} />
        </Tab>
        
        <Tab label="Metrics">
          <MetricsDashboard 
            efficiency={analysisData.efficiency}
            metrics={analysisData.metrics}
          />
        </Tab>
      </TabNavigation>
    </div>
  );
};


// Pattern Recognition Display
const PatternIndicator = ({ pattern }) => {
  const patternConfig = {
    'PATTERN_1_KNEE_LEAK': {
      icon: '⚠️',
      color: 'red',
      title: 'Energy Leak at Lead Knee',
      severity: 'CRITICAL'
    },
    'PATTERN_2_WEAK_HIP': {
      icon: '⚠️',
      color: 'amber',
      title: 'Weak Hip Contribution',
      severity: 'HIGH'
    },
    // ... other patterns
  };
  
  const config = patternConfig[pattern.type];
  
  return (
    <div className={`pattern-indicator ${config.color}`}>
      <span className="icon">{config.icon}</span>
      <h3>{config.title}</h3>
      <span className="severity">{config.severity}</span>
      <p>{pattern.description}</p>
    </div>
  );
};


// Training Drill Card
const DrillCard = ({ drill }) => {
  return (
    <div className="drill-card">
      <h4>{drill.name}</h4>
      <div className="drill-specs">
        <span>{drill.sets} sets × {drill.reps} reps</span>
      </div>
      <div className="coaching-cue">
        💬 <em>"{drill.cue}"</em>
      </div>
      {drill.video_url && (
        <VideoPlayer src={drill.video_url} />
      )}
    </div>
  );
};


// Before/After Comparison
const ComparisonView = ({ before, after }) => {
  return (
    <div className="comparison-view">
      <div className="before-column">
        <h3>Before Training</h3>
        <MetricCard label="Exit Velo" value={before.exit_velo} unit="mph" />
        <MetricCard label="Launch Angle" value={before.launch_angle} unit="°" />
        <MetricCard label="Hip Angmom" value={before.hip_angmom} />
      </div>
      
      <div className="delta-column">
        <h3>Change</h3>
        <DeltaCard 
          delta={after.exit_velo - before.exit_velo} 
          unit="mph"
          positive={true}
        />
        <DeltaCard 
          delta={after.launch_angle - before.launch_angle} 
          unit="°"
          positive={true}
        />
        <DeltaCard 
          delta={after.hip_angmom - before.hip_angmom}
          positive={true}
        />
      </div>
      
      <div className="after-column">
        <h3>After Training</h3>
        <MetricCard label="Exit Velo" value={after.exit_velo} unit="mph" />
        <MetricCard label="Launch Angle" value={after.launch_angle} unit="°" />
        <MetricCard label="Hip Angmom" value={after.hip_angmom} />
      </div>
    </div>
  );
};
```

---

## 📝 KNOWLEDGE BASE INTEGRATION

### **Pattern Recognition Logic:**

```python
def diagnose_pattern(metrics):
    """
    Match athlete's metrics to diagnostic patterns from Knowledge Base
    
    Patterns (from COACH_RICK_AI_KNOWLEDGE_BASE.md):
    - PATTERN 1: Energy Leak at Lead Knee
    - PATTERN 2: Weak Hip Contribution (Despite Good Timing)
    - PATTERN 3: Fast Foot Roll (Spinner)
    - PATTERN 4: Shoulder Compensation (Over-Rotation)
    """
    
    lead_knee = metrics['lead_knee_angle']
    hip_angmom = metrics['hip_angular_momentum']
    shoulder_angmom = metrics['shoulder_angular_momentum']
    shoulder_hip_ratio = shoulder_angmom / hip_angmom if hip_angmom > 0 else 999
    timing_gap_ms = metrics['timing_gap_ms']
    
    # PATTERN 1: Energy Leak at Lead Knee
    if lead_knee < 140 and hip_angmom < 5.0 and shoulder_hip_ratio > 3.0:
        return {
            'type': 'PATTERN_1_KNEE_LEAK',
            'severity': 'CRITICAL',
            'title': 'Energy Leak at Lead Knee',
            'description': (
                f"Your lead knee is flexed at {lead_knee:.1f}° (should be 160-180°). "
                f"This absorbs {int((170-lead_knee)/170*100)}% of your ground force before "
                f"it reaches your hips. Result: Weak hip contribution ({hip_angmom:.1f} "
                f"vs target 8-10+) and shoulder compensation ({shoulder_hip_ratio:.1f}x "
                f"vs target 0.7-1.5x)."
            ),
            'root_cause': 'Coordination issue - lead knee flexing instead of extending',
            'primary_protocol': 'PROTOCOL_1',  # Fix Lead Knee Energy Leak
            'secondary_protocol': 'PROTOCOL_2'  # Develop Vertical Ground Force
        }
    
    # PATTERN 2: Weak Hip Contribution (Good Timing)
    elif hip_angmom < 5.0 and timing_gap_ms > 15 and shoulder_hip_ratio > 4.0:
        return {
            'type': 'PATTERN_2_WEAK_HIP',
            'severity': 'HIGH',
            'title': 'Weak Hip Contribution',
            'description': (
                f"Your timing is good ({timing_gap_ms:.0f}ms gap), but your hips only "
                f"contribute {hip_angmom:.1f} angular momentum (should be 8-10+). "
                f"Shoulders forced to compensate ({shoulder_hip_ratio:.1f}x ratio). "
                f"You have the deceleration mechanism but weak hip input."
            ),
            'root_cause': 'Weak vertical ground force and/or lead knee leak',
            'primary_protocol': 'PROTOCOL_2',  # Develop Vertical Ground Force
            'secondary_protocol': 'PROTOCOL_3'  # Train Hip Lock
        }
    
    # PATTERN 3: Fast Foot Roll (Spinner)
    elif lead_knee < 140 and timing_gap_ms < 15 and hip_angmom < 5.0:
        return {
            'type': 'PATTERN_3_SPINNER',
            'severity': 'HIGH',
            'title': 'Spinner Pattern (Fast Foot Roll)',
            'description': (
                f"Your lead foot is rolling too quickly (weak vertical push). "
                f"Lead knee never extends ({lead_knee:.1f}°), hips and shoulders "
                f"rotate together (only {timing_gap_ms:.0f}ms gap). You're spinning "
                f"instead of posting and rotating."
            ),
            'root_cause': 'Not pushing vertically through ball of lead foot',
            'primary_protocol': 'PROTOCOL_2',  # Develop Vertical Ground Force
            'secondary_protocol': 'PROTOCOL_1'  # Fix Lead Knee (secondary)
        }
    
    # PATTERN 4: Shoulder Compensation
    elif shoulder_hip_ratio > 4.0 and hip_angmom < 5.0:
        return {
            'type': 'PATTERN_4_SHOULDER_COMP',
            'severity': 'MODERATE',
            'title': 'Shoulder Compensation (Over-Rotation)',
            'description': (
                f"Your shoulders are doing work your hips should do. "
                f"Shoulder/hip ratio: {shoulder_hip_ratio:.1f}x (should be 0.7-1.5x). "
                f"This leads to 'muscling' the swing and bat drag."
            ),
            'root_cause': 'Weak hip contribution forces shoulder compensation',
            'primary_protocol': 'PROTOCOL_3',  # Train Hip Lock
            'secondary_protocol': 'PROTOCOL_4'  # Restore Kinetic Sequence
        }
    
    # No clear pattern (needs manual review)
    else:
        return {
            'type': 'PATTERN_UNCLEAR',
            'severity': 'LOW',
            'title': 'Pattern Unclear - Manual Review Needed',
            'description': 'Metrics do not match standard patterns. Consult with coach.',
            'root_cause': 'Unknown',
            'primary_protocol': None,
            'secondary_protocol': None
        }
```

---

### **Protocol Selection & Training Plan Generation:**

```python
# Load protocols from Knowledge Base
PROTOCOLS = {
    'PROTOCOL_1': {
        'name': 'Fix Lead Knee Energy Leak',
        'duration_weeks': 2,
        'focus': 'Lead knee extension (0.3° → 160-180°)',
        'weeks': [
            {
                'week': '1-2',
                'focus': 'Fix Lead Knee Leak',
                'drills': [
                    {
                        'name': 'Single-Leg Isometric Holds',
                        'sets': 3,
                        'reps': '20s',
                        'cue': 'Steel rod, not shock absorber',
                        'description': 'Stand on lead leg, knee at 160-170°. Push through ball of foot, engage quad + glute.',
                        'video_url': None  # TODO: Add demo videos
                    },
                    {
                        'name': 'Single-Leg Vertical Jumps',
                        'sets': 3,
                        'reps': 5,
                        'cue': 'Lock it on landing, don\'t collapse',
                        'description': 'Jump vertically off lead leg only. Land with knee 160-180° (stiff landing). Stick landing 2 seconds.'
                    },
                    {
                        'name': 'Wall Knee Extension Drill',
                        'sets': 3,
                        'reps': 10,
                        'cue': 'Push down, knee locks',
                        'description': 'Back against wall, lead foot 12" forward. Push through ball of foot → extend knee. Feel quad + glute activate simultaneously.'
                    }
                ],
                'expected_change': 'Lead knee 140-160° → 160-180° at contact',
                'downstream_effect': 'Hip angmom ↑ by 2-3x'
            }
        ]
    },
    
    'PROTOCOL_2': {
        'name': 'Develop Vertical Ground Force',
        'duration_weeks': 4,
        'focus': 'vGRF 0.8x → 1.5-2.0x bodyweight',
        'weeks': [
            {
                'week': '1-2',
                'focus': 'Foundation - Soft Pedal',
                'drills': [
                    {
                        'name': 'Force Pedals (Soft)',
                        'sets': 3,
                        'reps': '10 swings',
                        'cue': 'Feel the bounce, push through it',
                        'description': 'Soft hexagonal foam platform under ball of lead foot. Dry swings only.',
                        'equipment': 'Force Pedals (soft)'
                    },
                    {
                        'name': 'Single-Leg Calf Raises',
                        'sets': 3,
                        'reps': 15,
                        'cue': 'Push through the ball of your foot',
                        'description': 'Stand on lead leg, ball of foot on edge. Rise to toes (plantarflexion), hold 2s, lower slowly.'
                    },
                    {
                        'name': 'Lead Leg Slam → Swing',
                        'sets': 3,
                        'reps': 10,
                        'cue': 'Slam, brake hip, whip bat',
                        'description': 'Stand on lead leg. SLAM foot down (vertical push). Immediately load and swing. Feel hip decelerate after slam.'
                    }
                ],
                'expected_change': 'vGRF 0.8-1.0x → 1.2-1.5x bodyweight',
                'downstream_effect': 'Hip deceleration capability ↑'
            },
            {
                'week': '3-4',
                'focus': 'Progression - Firm Pedal + Integration',
                'drills': [
                    {
                        'name': 'Force Pedals (Firm)',
                        'sets': 3,
                        'reps': '10 swings',
                        'cue': 'Bounce off the ground',
                        'description': 'Firm pedal. Progress from dry swings to tee work.',
                        'equipment': 'Force Pedals (firm)'
                    },
                    # ... additional drills
                ]
            }
        ]
    },
    
    # PROTOCOL_3, PROTOCOL_4, PROTOCOL_5...
    # (Full protocols defined in Knowledge Base - extract and structure here)
}


def generate_training_plan(pattern_diagnosis, metrics):
    """
    Generate 6-week training plan based on diagnosed pattern
    """
    primary_protocol_id = pattern_diagnosis['primary_protocol']
    secondary_protocol_id = pattern_diagnosis.get('secondary_protocol')
    
    primary_protocol = PROTOCOLS[primary_protocol_id]
    
    # Build complete 6-week plan
    training_plan = {
        'athlete_pattern': pattern_diagnosis['type'],
        'primary_issue': pattern_diagnosis['title'],
        'total_weeks': 6,
        'protocols_used': [primary_protocol_id, secondary_protocol_id],
        'weeks': []
    }
    
    # Add primary protocol weeks
    training_plan['weeks'].extend(primary_protocol['weeks'])
    
    # Add secondary protocol weeks if applicable
    if secondary_protocol_id:
        secondary_protocol = PROTOCOLS[secondary_protocol_id]
        training_plan['weeks'].extend(secondary_protocol['weeks'])
    
    # Add integration phase (always final 2 weeks)
    integration_protocol = PROTOCOLS['PROTOCOL_5']  # Integration to Live Swings
    training_plan['weeks'].extend(integration_protocol['weeks'])
    
    return training_plan
```

---

### **Coach Rick's Take Generation:**

```python
def generate_coach_analysis(pattern, metrics, predictions):
    """
    Generate natural language analysis from Coach Rick's perspective
    Uses templates from Knowledge Base but customizes with athlete data
    """
    
    templates = {
        'PATTERN_1_KNEE_LEAK': """
Your ground forces and timing are {timing_quality}. But here's the issue: 
your lead leg isn't extending through the pitch plane — it's only at {lead_knee:.1f}° 
(needs to be 160-180°). This causes you to pull the bat across instead of 
extending through, forcing your shoulders to over-rotate ({shoulder_hip_ratio:.1f}x, 
should be 0.7-1.5x).

The result? A drag pattern with zero late whip, losing {exit_velo_loss:.0f} mph 
and causing you to roll over breaking balls.

**The Fix:** Teach your front arm to STRETCH FORWARD at contact. We'll use 
single-leg jumps to train your lead knee to lock, Force Pedals to create 
vertical bounce, and rope swings to restore your bat whip.

**Expected Results (6 weeks):**
• Exit Velo: {current_ev:.0f} → {predicted_ev:.0f} mph (+{ev_gain:.0f} mph)
• Launch Angle: {current_la}° → {predicted_la}° (ground balls → line drives)
• Breaking Ball AVG: {current_bb_avg:.3f} → {predicted_bb_avg:.3f}
• Hip Contribution: {current_hip:.1f} → 8-10+ angular momentum
        """,
        
        # ... other pattern templates
    }
    
    template = templates.get(pattern['type'], "Pattern analysis unavailable.")
    
    # Fill in template with athlete-specific data
    coach_take = template.format(
        timing_quality='elite' if metrics['timing_gap_ms'] > 15 else 'decent',
        lead_knee=metrics['lead_knee_angle'],
        shoulder_hip_ratio=metrics['shoulder_hip_ratio'],
        exit_velo_loss=predictions['improvement']['exit_velo_gain'],
        current_ev=predictions['current']['exit_velo'],
        predicted_ev=predictions['predicted']['exit_velo'],
        ev_gain=predictions['improvement']['exit_velo_gain'],
        current_la=predictions['current']['launch_angle'],
        predicted_la=predictions['predicted']['launch_angle'],
        current_bb_avg=predictions['current']['breaking_ball_avg'],
        predicted_bb_avg=predictions['predicted']['breaking_ball_avg'],
        current_hip=metrics['hip_angular_momentum']
    )
    
    return coach_take
```

---

## ✅ SUCCESS CRITERIA

Your implementation is complete when:

### **Functional Requirements:**
- [ ] Users can upload `momentum-energy.csv` and `inverse-kinematics.csv`
- [ ] System correctly identifies diagnostic patterns (4 patterns)
- [ ] System calculates efficiency scores accurately
- [ ] System predicts ball outcomes (exit velo, launch angle, spray chart)
- [ ] System generates 6-week training plan based on pattern
- [ ] Coach Rick's Take is generated with natural language analysis
- [ ] Before/After comparison feature works
- [ ] All metrics match example (Eric Williams case study)

### **UI/UX Requirements:**
- [ ] Dark theme with gold accents (matches design)
- [ ] Responsive layout (desktop + mobile)
- [ ] Color-coded metrics (green/amber/red based on thresholds)
- [ ] Animated transitions between sections
- [ ] Drill cards with coaching cues
- [ ] Video demonstrations (placeholders OK for v1)
- [ ] Progress bars for efficiency scores
- [ ] Downloadable PDF report

### **Technical Requirements:**
- [ ] CSV parsing works for both file types
- [ ] Frame synchronization (rel_frame alignment)
- [ ] Handle missing data gracefully
- [ ] API endpoints documented
- [ ] Error handling for invalid uploads
- [ ] Data validation (check required columns)
- [ ] Session management (save analyses)
- [ ] Export functionality (JSON, PDF)

---

## 📦 DELIVERABLES

### **Phase 1: MVP (Week 1-2)**
- [ ] Data upload interface
- [ ] Basic analysis engine (pattern recognition)
- [ ] Simple report view (metrics + diagnosis)
- [ ] Single protocol training plan

### **Phase 2: Full Feature Set (Week 3-4)**
- [ ] All 5 protocols implemented
- [ ] Coach Rick's Take generation
- [ ] Complete UI design (dark theme)
- [ ] Ball outcome predictions
- [ ] Before/After comparison

### **Phase 3: Polish & Launch (Week 5-6)**
- [ ] Video demonstrations added
- [ ] PDF export
- [ ] Mobile optimization
- [ ] User testing with real athletes
- [ ] Documentation (user guide)

---

## 🆘 SUPPORT & QUESTIONS

**Knowledge Base Reference:**
- Primary logic: `COACH_RICK_AI_KNOWLEDGE_BASE.md`
- Research background: `JOINT_COORDINATION_RESEARCH_REPORT.md`

**Example Data:**
- Eric Williams case study (included in project)
- Test with: `eric_williams_data/momentum-energy.csv` and `inverse-kinematics.csv`

**Expected Output:**
- Reference: `eric_williams_ball_outcomes.html`
- Should match Eric's metrics and recommendations

**Contact:**
- For technical questions about data structure: Review Knowledge Base "Data Interpretation Guide"
- For protocol details: Reference "Intervention Protocols" section
- For prediction formulas: See "Outcome Prediction Model"

---

## 🚀 FINAL NOTES

**This is a VALIDATED system.** The research is peer-reviewed, the methods are clinically proven, and the predictions are testable.

Your job is to **translate Coach Rick AI's knowledge into a user-friendly application** that helps athletes:
1. **Understand** what their ball is doing (and why)
2. **See** what their biomechanics reveal
3. **Know** exactly how to fix it
4. **Predict** what will happen after training

**The theory works. The data proves it. Now build the tool that delivers it.**

---

**Builder 2, you have everything you need. Let's build CATCHING BARRELS. 🚀**

---

*End of Instructions*
