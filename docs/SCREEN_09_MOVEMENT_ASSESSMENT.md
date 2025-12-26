# Screen 09: Movement Assessment

**Screen Name**: Movement Assessment  
**Route**: `/assessment/[step]`  
**Complexity**: MEDIUM-HIGH (Multi-step interactive flow)  
**Priority**: P1 (Important for motor profile)

---

## 📐 Flow Overview

```
Movement Assessment
    ↓
Step 1: Introduction
    ↓
Step 2: Physical Capacity Test
    ↓
Step 3: Movement Pattern Test
    ↓
Step 4: Results Processing
    ↓
Motor Profile Result (Screen 10)
```

---

## 🎯 Step 1: Introduction

### Layout
```
┌───────────────────────────────┐
│  ← Skip                       │
├───────────────────────────────┤
│                               │
│       [Icon: Clipboard]       │
│           96×96                │
│                               │
│   Movement Assessment         │
│                               │
│   This 2-minute test helps    │
│   us understand your unique   │
│   movement patterns and       │
│   build your motor profile.   │
│                               │
│   What to Expect:             │
│   • 5 simple movements        │
│   • No equipment needed       │
│   • Takes ~2 minutes          │
│                               │
│   Best Results:               │
│   • Find a clear space        │
│   • Stand 6 feet from camera  │
│   • Ensure good lighting      │
│                               │
│   ○ ● ○ ○                     │ ← Progress (Step 1/4)
│                               │
│   [Start Assessment]          │
│                               │
└───────────────────────────────┘
```

---

## 🎯 Step 2: Physical Capacity Test

### Layout
```
┌───────────────────────────────┐
│  ← Back            Skip →     │
├───────────────────────────────┤
│                               │
│   Physical Capacity           │
│                               │
│   How many push-ups can you   │
│   do in one set?              │
│                               │
│   ┌─────────────────────────┐ │
│   │ ◯ 0-10                  │ │
│   │ ◯ 11-20                 │ │
│   │ ◯ 21-30                 │ │
│   │ ◯ 31-40                 │ │
│   │ ◯ 41+                   │ │
│   └─────────────────────────┘ │
│                               │
│   How far can you jump        │
│   (standing broad jump)?      │
│                               │
│   ┌─────────────────────────┐ │
│   │ ◯ Less than 5 feet      │ │
│   │ ◯ 5-6 feet              │ │
│   │ ◯ 6-7 feet              │ │
│   │ ◯ 7-8 feet              │ │
│   │ ◯ 8+ feet               │ │
│   └─────────────────────────┘ │
│                               │
│   ○ ○ ● ○                     │ ← Progress (Step 2/4)
│                               │
│   [Continue]                  │
│                               │
└───────────────────────────────┘
```

---

## 🎯 Step 3: Movement Pattern Test

### Layout
```
┌───────────────────────────────┐
│  ← Back                       │
├───────────────────────────────┤
│                               │
│   Movement Patterns           │
│                               │
│   [Camera Preview]            │
│   ┌─────────────────────────┐ │
│   │                         │ │
│   │    📹 Live Feed         │ │
│   │                         │ │
│   │    [Skeleton Overlay]   │ │
│   │                         │ │
│   └─────────────────────────┘ │
│                               │
│   Test 1 of 5: Hip Rotation   │
│                               │
│   Instructions:               │
│   • Stand facing camera       │
│   • Rotate hips left to right │
│   • Keep shoulders still      │
│                               │
│   ┌──────────────┐            │
│   │  Recording   │            │
│   │    3 sec     │            │
│   └──────────────┘            │
│                               │
│   ○ ○ ○ ●                     │ ← Progress (Step 3/4)
│                               │
│   [Start Test]  [Skip Test]   │
│                               │
└───────────────────────────────┘
```

---

## 🎯 Step 4: Results Processing

### Layout
```
┌───────────────────────────────┐
│                               │
│       [Animation]             │
│       🧬 Processing           │
│                               │
│   Analyzing Your Movement     │
│                               │
│   We're calculating your      │
│   motor profile based on      │
│   your responses...           │
│                               │
│   ▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░  75%    │
│                               │
│   ✓ Physical capacity mapped  │
│   ✓ Movement patterns analyzed│
│   → Determining motor profile │
│                               │
│   ○ ○ ○ ○                     │ ← Progress (Step 4/4)
│                               │
└───────────────────────────────┘
```

---

## 🎨 Visual Specifications

### Container
```css
max-width: 480px;
margin: 0 auto;
padding: 24px;
min-height: 100vh;
background: #FAFAFA;
display: flex;
flex-direction: column;
```

### Radio Button Group
```css
background: #FFFFFF;
border: 1px solid #E5E7EB;
border-radius: 12px;
overflow: hidden;
margin-bottom: 24px;
```

**Each Option**:
```css
display: flex;
align-items: center;
gap: 12px;
padding: 16px;
border-bottom: 1px solid #E5E7EB;
cursor: pointer;
transition: all 200ms ease;
```

**Option Hover**:
```css
background: #F9FAFB;
```

**Option Selected**:
```css
background: #EFF6FF; /* Very light blue */
border-left: 4px solid #06B6D4; /* Electric Cyan */
```

**Radio Icon**:
- Unselected: Empty circle (Gray-300)
- Selected: Filled circle (Electric Cyan)
- Size: 20px

### Camera Preview
```css
width: 100%;
aspect-ratio: 16/9;
background: #000000;
border-radius: 12px;
overflow: hidden;
position: relative;
margin-bottom: 24px;
```

**Skeleton Overlay**:
- MediaPipe Pose landmarks
- 17 keypoints connected with lines
- Color: Electric Cyan (#06B6D4)
- Opacity: 0.8
- Line width: 2px

### Test Instructions Card
```css
background: #FFFFFF;
border: 1px solid #E5E7EB;
border-radius: 12px;
padding: 20px;
margin-bottom: 24px;
```

**Test Title**:
```css
font-size: 18px;
font-weight: 600;
color: #111827;
margin-bottom: 12px;
```

**Instruction List**:
```css
list-style: none;
padding: 0;
```

**Each Instruction**:
```css
display: flex;
align-items: start;
gap: 8px;
padding: 6px 0;
font-size: 15px;
color: #374151;
```

**Bullet**: Bullet point (•) in Electric Cyan

### Recording Indicator
```css
background: #EF4444; /* Error Red */
color: #FFFFFF;
padding: 8px 16px;
border-radius: 6px;
font-size: 14px;
font-weight: 600;
display: inline-flex;
align-items: center;
gap: 8px;
margin-bottom: 24px;
animation: pulse 1.5s ease-in-out infinite;
```

**Recording Dot**:
```css
width: 8px;
height: 8px;
background: #FFFFFF;
border-radius: 50%;
animation: blink 1s ease-in-out infinite;
```

---

## 🔄 Assessment Logic

### Step 1: Introduction
```typescript
const handleStartAssessment = () => {
  // Check camera permission
  requestCameraPermission();
  
  // Navigate to Step 2
  router.push('/assessment/2');
  
  // Track analytics
  analytics.track('Assessment Started');
};
```

### Step 2: Physical Capacity
```typescript
interface PhysicalCapacity {
  pushups: '0-10' | '11-20' | '21-30' | '31-40' | '41+';
  broadJump: '<5' | '5-6' | '6-7' | '7-8' | '8+';
}

const handleContinue = () => {
  // Validate selections
  if (!physicalCapacity.pushups || !physicalCapacity.broadJump) {
    showError('Please answer both questions');
    return;
  }
  
  // Save to state
  savePhysicalCapacity(physicalCapacity);
  
  // Navigate to Step 3
  router.push('/assessment/3');
};
```

### Step 3: Movement Pattern Tests
```typescript
interface MovementTest {
  testId: string;
  testName: string;
  instructions: string[];
  duration: number; // seconds
  videoUrl?: string;
}

const movementTests: MovementTest[] = [
  {
    testId: 'hip_rotation',
    testName: 'Hip Rotation',
    instructions: [
      'Stand facing camera',
      'Rotate hips left to right',
      'Keep shoulders still',
    ],
    duration: 3,
  },
  {
    testId: 'shoulder_turn',
    testName: 'Shoulder Turn',
    instructions: [
      'Stand sideways to camera',
      'Turn shoulders back and forth',
      'Keep hips forward',
    ],
    duration: 3,
  },
  {
    testId: 'squat_depth',
    testName: 'Squat Depth',
    instructions: [
      'Stand facing camera',
      'Perform a deep squat',
      'Hold for 2 seconds',
    ],
    duration: 3,
  },
  {
    testId: 'arm_speed',
    testName: 'Arm Speed',
    instructions: [
      'Stand sideways to camera',
      'Swing arm back and forth rapidly',
      'Like throwing a baseball',
    ],
    duration: 3,
  },
  {
    testId: 'balance',
    testName: 'Single Leg Balance',
    instructions: [
      'Stand facing camera',
      'Balance on one leg',
      'Hold for 3 seconds',
    ],
    duration: 3,
  },
];

const handleStartTest = async (test: MovementTest) => {
  // Start camera recording
  const stream = await startCameraRecording();
  
  // Enable MediaPipe Pose detection
  const poseDetector = await initializePoseDetector();
  
  // Show countdown (3, 2, 1, GO!)
  await showCountdown();
  
  // Record for test duration
  const videoBlob = await recordForDuration(test.duration);
  
  // Stop recording
  stopRecording();
  
  // Upload video
  const videoUrl = await uploadTestVideo(videoBlob, test.testId);
  
  // Save result
  saveTestResult(test.testId, videoUrl);
  
  // Move to next test or finish
  if (currentTestIndex < movementTests.length - 1) {
    setCurrentTestIndex(currentTestIndex + 1);
  } else {
    router.push('/assessment/4');
  }
};
```

### Step 4: Results Processing
```typescript
const processAssessmentResults = async () => {
  try {
    // Gather all data
    const assessmentData = {
      physical_capacity: physicalCapacity,
      movement_tests: testResults,
      user_id: userId,
    };
    
    // Send to backend for analysis
    const response = await fetch('/api/assessment/analyze', {
      method: 'POST',
      body: JSON.stringify(assessmentData),
    });
    
    const result = await response.json();
    
    // Save motor profile
    await saveMotorProfile(result.motor_profile);
    
    // Navigate to results
    router.push(`/motor-profile/${result.id}`);
    
  } catch (error) {
    showError('Failed to process assessment');
  }
};
```

---

## 📊 Motor Profile Calculation

### Input Data
- Physical capacity (pushups, broad jump)
- Hip rotation range
- Shoulder turn speed
- Squat depth
- Arm speed
- Balance stability

### Motor Profile Types
1. **Spinner** (Quick hands, short path)
2. **Slingshotter** (Whip-like action)
3. **Whipper** (Fast rotational)
4. **Torquer** (Power-based)
5. **Tilter** (Leverage-focused)
6. **Hybrid** (Balanced)

### Calculation Logic
```typescript
const calculateMotorProfile = (data: AssessmentData): MotorProfile => {
  let scores = {
    spinner: 0,
    slingshotter: 0,
    whipper: 0,
    torquer: 0,
    tilter: 0,
    hybrid: 0,
  };
  
  // Physical capacity scoring
  if (data.pushups >= '31-40') scores.torquer += 20;
  if (data.broadJump >= '7-8') scores.whipper += 20;
  
  // Movement test scoring
  if (data.hip_rotation_range > 80) scores.spinner += 30;
  if (data.shoulder_turn_speed > 150) scores.whipper += 30;
  if (data.squat_depth > 90) scores.torquer += 20;
  if (data.arm_speed > 120) scores.slingshotter += 30;
  
  // Find highest score
  const primaryProfile = Object.entries(scores)
    .sort((a, b) => b[1] - a[1])[0][0];
  
  return {
    primary: primaryProfile,
    confidence: scores[primaryProfile],
  };
};
```

---

## 📱 Responsive Behavior

### Mobile (< 768px)
- Full-width camera preview
- Stacked buttons
- Padding: 24px

### Tablet (768px - 1023px)
- Camera preview: 16:9 aspect ratio
- Side-by-side buttons
- Padding: 32px

### Desktop (1024px+)
- Max-width: 600px
- Larger camera preview
- Padding: 40px

---

## ♿ Accessibility

### Camera Access
```html
<div role="region" aria-label="Movement test camera view">
  <video 
    ref={videoRef}
    aria-label="Live camera feed"
    autoPlay
    playsInline
  />
  <canvas 
    ref={canvasRef}
    aria-hidden="true"
    role="presentation"
  />
</div>
```

### Test Instructions
```html
<div role="article" aria-labelledby="test-title">
  <h3 id="test-title">Hip Rotation Test</h3>
  <ul aria-label="Test instructions">
    <li>Stand facing camera</li>
    <li>Rotate hips left to right</li>
    <li>Keep shoulders still</li>
  </ul>
</div>
```

### Recording Status
```html
<div 
  role="status" 
  aria-live="polite"
  aria-atomic="true"
>
  <span className={isRecording ? 'recording' : 'idle'}>
    {isRecording ? 'Recording in progress' : 'Ready to record'}
  </span>
</div>
```

---

## 📊 Analytics Events

```typescript
// Assessment started
analytics.track('Assessment Started');

// Step completed
analytics.track('Assessment Step Completed', {
  step: number,
  stepName: string,
});

// Physical capacity answered
analytics.track('Physical Capacity Answered', {
  pushups: string,
  broadJump: string,
});

// Movement test started
analytics.track('Movement Test Started', {
  testId: string,
  testName: string,
});

// Movement test completed
analytics.track('Movement Test Completed', {
  testId: string,
  duration: number,
});

// Test skipped
analytics.track('Movement Test Skipped', {
  testId: string,
});

// Assessment completed
analytics.track('Assessment Completed', {
  duration: number,
  testsCompleted: number,
  testsSkipped: number,
});
```

---

## 🔍 Testing Checklist

- [ ] All 4 steps render
- [ ] Navigation works (back, skip, continue)
- [ ] Radio button selection
- [ ] Camera permission request
- [ ] Camera preview displays
- [ ] MediaPipe Pose detection
- [ ] Recording functionality
- [ ] Countdown timer
- [ ] Test progress tracking
- [ ] Skip test works
- [ ] Results processing
- [ ] Motor profile calculation
- [ ] Navigation to results
- [ ] Error handling
- [ ] Responsive design
- [ ] Accessibility

---

## ✅ Definition of Done

- [ ] All 4 steps implemented
- [ ] Camera integration works
- [ ] MediaPipe Pose integrated
- [ ] Recording functional
- [ ] 5 movement tests defined
- [ ] Physical capacity form
- [ ] Results processing
- [ ] Motor profile calculation
- [ ] Navigation logic
- [ ] Skip functionality
- [ ] Error handling
- [ ] Responsive design
- [ ] Accessibility
- [ ] Analytics

---

**Priority**: P1 (Important)  
**Complexity**: MEDIUM-HIGH (Multi-step + camera)  
**Estimated Dev Time**: 12-16 hours (Phase 2)

**Dependencies**:
- Camera access (getUserMedia)
- MediaPipe Pose (TensorFlow.js)
- Video recording/upload
- Backend motor profile analysis

---

*Last Updated: December 28, 2025*  
*Screen Specification v1.0*
