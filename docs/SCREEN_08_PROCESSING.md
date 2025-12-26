# Screen 08: Processing

**Screen Name**: Processing / Analyzing  
**Route**: `/processing/[sessionId]`  
**Complexity**: LOW (Loading state with progress)  
**Priority**: P0 (Critical Path)

---

## 📐 Layout Overview

```
┌───────────────────────────────┐
│                               │
│                               │
│                               │
│       [Animation]             │ ← Animated icon
│       📊 + ⚡                 │   (pulse/spin)
│                               │
│                               │
│   Analyzing Your Swing        │ ← Heading-01
│                               │
│   Our AI is processing your   │ ← Body-02
│   video and calculating your  │
│   KRS score...                │
│                               │
│                               │
│   ▓▓▓▓▓▓▓▓▓▓░░░░░░░░  65%    │ ← Progress bar
│                               │
│                               │
│   ✓ Video uploaded            │ ← Status list
│   ✓ Pose detection complete   │   (checkmarks)
│   → Calculating KRS score...  │   (in progress)
│   ○ Generating report         │   (pending)
│                               │
│                               │
│   Estimated: 45 seconds       │ ← Time estimate
│                               │
│                               │
│                               │
└───────────────────────────────┘
```

---

## 🎨 Visual Specifications

### Container
```css
max-width: 480px;
margin: 0 auto;
padding: 40px 24px;
min-height: 100vh;
background: #FAFAFA; /* Gray-50 */
display: flex;
flex-direction: column;
align-items: center;
justify-content: center;
```

### Animation Icon
```css
width: 120px;
height: 120px;
margin-bottom: 32px;
display: flex;
align-items: center;
justify-content: center;
background: linear-gradient(135deg, #06B6D4 0%, #0284C7 100%);
border-radius: 50%;
animation: pulse 2s ease-in-out infinite;
```

**Pulse Animation**:
```css
@keyframes pulse {
  0%, 100% {
    transform: scale(1);
    box-shadow: 0 0 0 0 rgba(6, 182, 212, 0.4);
  }
  50% {
    transform: scale(1.05);
    box-shadow: 0 0 0 20px rgba(6, 182, 212, 0);
  }
}
```

**Icon** (inside circle):
- Icon: `<Activity />` or `<Zap />` from Lucide
- Size: 64px
- Color: White (#FFFFFF)
- Animation: Gentle spin or bounce

### Heading
```css
font-family: 'Inter', sans-serif;
font-weight: 600; /* Semibold */
font-size: 28px;
line-height: 36px;
color: #111827; /* Gray-900 */
text-align: center;
margin-bottom: 12px;
```

### Subheading
```css
font-family: 'Inter', sans-serif;
font-weight: 400; /* Regular */
font-size: 16px;
line-height: 24px;
color: #6B7280; /* Gray-500 */
text-align: center;
margin-bottom: 32px;
max-width: 360px;
```

### Progress Bar
```css
width: 100%;
max-width: 400px;
height: 8px;
background: #E5E7EB; /* Gray-200 */
border-radius: 4px;
overflow: hidden;
position: relative;
margin-bottom: 8px;
```

**Fill**:
```css
height: 100%;
background: linear-gradient(90deg, #06B6D4 0%, #0284C7 100%);
border-radius: 4px;
transition: width 500ms ease;
```

**Animated shimmer** (optional):
```css
@keyframes shimmer {
  0% {
    background-position: -400px 0;
  }
  100% {
    background-position: 400px 0;
  }
}

.progress-fill::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.3),
    transparent
  );
  animation: shimmer 2s infinite;
}
```

**Percentage**:
```css
font-size: 14px;
font-weight: 600;
color: #06B6D4; /* Electric Cyan */
text-align: right;
margin-bottom: 32px;
```

### Status List
```css
width: 100%;
max-width: 360px;
margin-bottom: 24px;
```

**Each Status Item**:
```css
display: flex;
align-items: center;
gap: 12px;
padding: 12px 0;
font-size: 15px;
color: #374151; /* Gray-700 */
```

**Icon States**:
- **Complete**: `<Check />` in green circle (Success #10B981)
- **In Progress**: `<Loader />` spinning in cyan (Electric #06B6D4)
- **Pending**: `<Circle />` in gray (Gray-300 #D1D5DB)

```css
.status-icon {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
}

.status-icon.complete {
  color: #10B981;
}

.status-icon.in-progress {
  color: #06B6D4;
  animation: spin 1s linear infinite;
}

.status-icon.pending {
  color: #D1D5DB;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
```

### Time Estimate
```css
font-size: 14px;
color: #9CA3AF; /* Gray-400 */
text-align: center;
font-style: italic;
```

---

## 🔄 Processing Stages

### Stage 1: Upload (0-10%)
```
Status: "Video uploaded"
Icon: ✓ (complete)
Duration: Instant (already done)
```

### Stage 2: Pose Detection (10-40%)
```
Status: "Detecting pose landmarks..."
Icon: → (in progress)
Duration: 10-20 seconds
```

### Stage 3: Motion Analysis (40-70%)
```
Status: "Analyzing motion patterns..."
Icon: → (in progress)
Duration: 15-25 seconds
```

### Stage 4: KRS Calculation (70-90%)
```
Status: "Calculating KRS score..."
Icon: → (in progress)
Duration: 5-10 seconds
```

### Stage 5: Report Generation (90-100%)
```
Status: "Generating your report..."
Icon: → (in progress)
Duration: 5-10 seconds
```

---

## 🔄 Real-time Updates

### Polling Strategy
```typescript
const pollProcessingStatus = async (sessionId: string) => {
  const interval = setInterval(async () => {
    try {
      // Fetch session status from API
      const response = await fetch(`/api/sessions/${sessionId}/status`);
      const data = await response.json();
      
      // Update progress
      setProgress(data.progress);
      setCurrentStage(data.stage);
      
      // Check if complete
      if (data.status === 'completed') {
        clearInterval(interval);
        
        // Wait 500ms for dramatic effect
        setTimeout(() => {
          router.push(`/report/${sessionId}`);
        }, 500);
      }
      
      // Check if failed
      if (data.status === 'failed') {
        clearInterval(interval);
        showError(data.error || 'Analysis failed. Please try again.');
      }
      
    } catch (error) {
      console.error('Polling error:', error);
    }
  }, 2000); // Poll every 2 seconds
  
  return () => clearInterval(interval);
};
```

### WebSocket Alternative (for real-time)
```typescript
const ws = new WebSocket(`wss://api.example.com/sessions/${sessionId}`);

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  
  setProgress(data.progress);
  setCurrentStage(data.stage);
  setStatusList(data.statuses);
  
  if (data.status === 'completed') {
    router.push(`/report/${sessionId}`);
  }
};
```

---

## 📱 Responsive Behavior

### Mobile (< 768px)
- Icon: 120px
- Max width: 100%
- Padding: 24px

### Tablet (768px - 1023px)
- Icon: 140px
- Max width: 480px
- Padding: 32px

### Desktop (1024px+)
- Icon: 160px
- Max width: 480px
- Padding: 40px

---

## ⚠️ Error Handling

### Timeout (> 5 minutes)
```
Error: "Analysis is taking longer than expected"
Action: "Retry" button or "Go Back"
```

### Processing Failed
```
Error: "We couldn't analyze your video"
Reason: "Video quality too low" or "Motion not detected"
Action: "Upload New Video" button
```

### Network Error
```
Error: "Connection lost"
Action: Automatic retry (3 attempts)
Fallback: "Retry" button
```

---

## ♿ Accessibility

### Screen Reader
```html
<div role="status" aria-live="polite" aria-atomic="true">
  <h1>Analyzing Your Swing</h1>
  <p>Our AI is processing your video and calculating your KRS score</p>
  <div role="progressbar" 
       aria-valuenow={progress} 
       aria-valuemin="0" 
       aria-valuemax="100"
       aria-label={`Analysis progress: ${progress} percent complete`}>
    <div style={{width: `${progress}%`}} />
  </div>
  <ul aria-label="Processing stages">
    {statuses.map(status => (
      <li key={status.id} aria-current={status.active}>
        {status.text}
      </li>
    ))}
  </ul>
  <p>Estimated time remaining: {estimatedTime} seconds</p>
</div>
```

### Loading Announcements
- Progress updates announced every 25%
- Stage changes announced
- Completion announced
- Errors announced immediately

---

## 🎯 Time Estimates

### Average Processing Time
- **Fast**: 30-45 seconds
- **Normal**: 45-90 seconds
- **Slow**: 90-120 seconds

### Dynamic Estimation
```typescript
const estimateTimeRemaining = (progress: number) => {
  // Based on average processing time
  const avgTotalTime = 60; // seconds
  const remaining = avgTotalTime * (1 - progress / 100);
  return Math.max(0, Math.ceil(remaining));
};
```

---

## 📊 Analytics Events

```typescript
// Processing viewed
analytics.track('Processing Screen Viewed', {
  sessionId: string,
});

// Progress milestone
analytics.track('Processing Milestone', {
  sessionId: string,
  progress: number, // 25, 50, 75, 100
});

// Processing completed
analytics.track('Processing Completed', {
  sessionId: string,
  duration: number, // ms
});

// Processing failed
analytics.track('Processing Failed', {
  sessionId: string,
  error: string,
  duration: number, // ms
});
```

---

## 🔍 Testing Checklist

- [ ] Animation renders smoothly
- [ ] Progress bar updates
- [ ] Status list updates
- [ ] Polling works
- [ ] Completion navigation
- [ ] Error handling works
- [ ] Timeout handling
- [ ] Retry functionality
- [ ] Responsive design
- [ ] Accessibility
- [ ] Screen reader announcements
- [ ] Analytics events

---

## ✅ Definition of Done

- [ ] Processing UI implemented
- [ ] Animation smooth (60 FPS)
- [ ] Progress bar functional
- [ ] Status list updates
- [ ] Polling implemented
- [ ] Completion navigation
- [ ] Error handling
- [ ] Timeout handling
- [ ] Responsive design
- [ ] Accessibility
- [ ] Analytics

---

**Priority**: P0 (Critical Path)  
**Complexity**: LOW (Loading state)  
**Estimated Dev Time**: 3-4 hours (Phase 1)

**Dependencies**:
- Processing API endpoint
- WebSocket or polling mechanism
- Session status tracking

---

*Last Updated: December 27, 2025*  
*Screen Specification v1.0*
