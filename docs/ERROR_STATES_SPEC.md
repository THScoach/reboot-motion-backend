# Error States & Empty States

**Document**: Error Handling Specification  
**Version**: 1.0  
**Date**: December 29, 2025

---

## 📋 Error State Categories

### 1. Network Errors
### 2. API Errors  
### 3. Form Validation Errors
### 4. Permission Errors
### 5. Empty States
### 6. Offline Mode

---

## 🚨 1. Network Errors

### Connection Lost
```
┌───────────────────────────────┐
│                               │
│       [Icon: WiFi Off]        │
│          📡❌                  │
│                               │
│   Connection Lost             │
│                               │
│   Please check your internet  │
│   connection and try again.   │
│                               │
│   [Retry]                     │
│   [Continue Offline]          │
│                               │
└───────────────────────────────┘
```

**Trigger**: Network request timeout or failure  
**User Action**: Retry or switch to offline mode  
**Auto-retry**: 3 attempts with exponential backoff

---

### Slow Connection
```
┌───────────────────────────────┐
│                               │
│   ⚠️ Slow Connection          │
│                               │
│   This is taking longer than  │
│   expected. You can:          │
│                               │
│   • Keep waiting (45s left)   │
│   • Try again                 │
│   • Work offline              │
│                               │
│   [Keep Waiting]  [Cancel]    │
│                               │
└───────────────────────────────┘
```

**Trigger**: Request > 10 seconds  
**Timeout**: 60 seconds total  
**Options**: Wait, retry, or go offline

---

## ⚠️ 2. API Errors

### 404 Not Found
```
┌───────────────────────────────┐
│                               │
│       [Icon: Search]          │
│          🔍❌                  │
│                               │
│   Report Not Found            │
│                               │
│   We couldn't find this       │
│   analysis report. It may     │
│   have been deleted.          │
│                               │
│   [Go to Home]                │
│                               │
└───────────────────────────────┘
```

**HTTP Code**: 404  
**User Action**: Navigate to home or upload new video

---

### 500 Server Error
```
┌───────────────────────────────┐
│                               │
│       [Icon: Server]          │
│          🖥️❌                  │
│                               │
│   Something Went Wrong        │
│                               │
│   Our servers encountered an  │
│   error. We've been notified  │
│   and are working on it.      │
│                               │
│   Error ID: #abc123           │
│                               │
│   [Try Again]  [Contact Support]│
│                               │
└───────────────────────────────┘
```

**HTTP Code**: 500, 502, 503  
**Logging**: Error ID sent to Sentry  
**User Action**: Retry or contact support

---

### 401 Unauthorized
```
┌───────────────────────────────┐
│                               │
│       [Icon: Lock]            │
│          🔒                    │
│                               │
│   Session Expired             │
│                               │
│   Your session has expired.   │
│   Please sign in again.       │
│                               │
│   [Sign In]                   │
│                               │
└───────────────────────────────┘
```

**HTTP Code**: 401  
**Action**: Clear session, redirect to sign in  
**Preserve**: Redirect URL to return after auth

---

### 413 File Too Large
```
┌───────────────────────────────┐
│                               │
│       [Icon: File]            │
│          📁❌                  │
│                               │
│   File Too Large              │
│                               │
│   The video file exceeds the  │
│   500MB limit. Please:        │
│                               │
│   • Compress the video        │
│   • Trim to 5-30 seconds      │
│   • Record at lower quality   │
│                               │
│   [Choose Another File]       │
│                               │
└───────────────────────────────┘
```

**HTTP Code**: 413  
**Max Size**: 500MB  
**Guidance**: Compression tips provided

---

## ✏️ 3. Form Validation Errors

### Inline Field Error
```
Name *
┌─────────────────────────┐
│ Jo                      │
└─────────────────────────┘
❌ Name must be at least 3 characters
```

**Display**: Below input field  
**Color**: Error Red (#EF4444)  
**Icon**: ❌ or error icon  
**Timing**: On blur or submit

---

### Multiple Errors
```
❌ Please fix the following errors:
┌─────────────────────────┐
│ • Name is required      │
│ • Age must be 10-100    │
│ • Height is required    │
└─────────────────────────┘
```

**Display**: Top of form  
**Action**: Focus first error field  
**Accessibility**: Announced to screen reader

---

### Password Requirements
```
Password *
┌─────────────────────────┐
│ •••••••                 │
└─────────────────────────┘

Password must contain:
✓ At least 8 characters
✓ One uppercase letter
❌ One number
❌ One special character
```

**Display**: Below password field  
**Update**: Real-time as user types  
**Visual**: Checkmarks and X marks

---

## 🔐 4. Permission Errors

### Camera Permission Denied
```
┌───────────────────────────────┐
│                               │
│       [Icon: Camera]          │
│          📹🚫                  │
│                               │
│   Camera Access Required      │
│                               │
│   Catching Barrels needs      │
│   camera access to record     │
│   your swing.                 │
│                               │
│   Please enable camera        │
│   access in your device       │
│   settings.                   │
│                               │
│   [Open Settings]  [Skip]     │
│                               │
└───────────────────────────────┘
```

**Trigger**: Camera permission denied  
**Platform**: iOS/Android specific settings links  
**Fallback**: Option to upload video instead

---

### Microphone Permission Denied
```
┌───────────────────────────────┐
│                               │
│       [Icon: Mic]             │
│          🎤🚫                  │
│                               │
│   Microphone Access Needed    │
│                               │
│   For the best experience,    │
│   we recommend enabling       │
│   microphone access.          │
│                               │
│   [Enable]  [Continue Without]│
│                               │
└───────────────────────────────┘
```

**Trigger**: Microphone permission denied  
**Optional**: Can continue without audio  
**Use Case**: Video recording with coaching cues

---

### Storage Permission Denied
```
┌───────────────────────────────┐
│                               │
│   ⚠️ Storage Access Needed    │
│                               │
│   We need storage access to   │
│   save your swing videos.     │
│                               │
│   [Enable in Settings]        │
│                               │
└───────────────────────────────┘
```

**Trigger**: Storage/file access denied  
**Platform**: iOS/Android specific  
**Required**: For video saving

---

## 📭 5. Empty States

### No Uploaded Videos
```
┌───────────────────────────────┐
│                               │
│       [Icon: Video]           │
│          📹                    │
│                               │
│   No Videos Yet               │
│                               │
│   Upload or record your first │
│   swing to get started with   │
│   personalized analysis.      │
│                               │
│   [Upload Video]              │
│   [Record Live Swing]         │
│                               │
└───────────────────────────────┘
```

**Screen**: Upload page  
**First Use**: Encourage action  
**CTAs**: Upload or record

---

### No Reports Yet
```
┌───────────────────────────────┐
│                               │
│       [Icon: Report]          │
│          📊                    │
│                               │
│   No Reports Yet              │
│                               │
│   Complete 50 swings to       │
│   unlock your full detailed   │
│   analysis report.            │
│                               │
│   Progress: 10/50 swings      │
│   ▓▓░░░░░░░░ 20%              │
│                               │
│   [Upload Another Swing]      │
│                               │
└───────────────────────────────┘
```

**Screen**: Report page  
**Progressive**: Show progress to unlock  
**Motivation**: Clear goal (50 swings)

---

### No Drills Saved
```
┌───────────────────────────────┐
│                               │
│       [Icon: Star]            │
│          ⭐                    │
│                               │
│   No Saved Drills             │
│                               │
│   Browse the drill library    │
│   and save your favorites     │
│   for quick access.           │
│                               │
│   [Browse Drills]             │
│                               │
└───────────────────────────────┘
```

**Screen**: My Drills page  
**Action**: Browse library  
**Use Case**: Favorites/saved drills

---

### No Progress Data
```
┌───────────────────────────────┐
│                               │
│       [Icon: Chart]           │
│          📈                    │
│                               │
│   Start Tracking Progress     │
│                               │
│   Upload your first swing to  │
│   start tracking your KRS     │
│   score and improvements.     │
│                               │
│   [Get Started]               │
│                               │
└───────────────────────────────┘
```

**Screen**: Progress dashboard  
**First Use**: Motivational  
**Clear CTA**: Upload first swing

---

### Search No Results
```
┌───────────────────────────────┐
│                               │
│  🔍 No drills found for       │
│     "hip rotation"            │
│                               │
│   Try:                        │
│   • Check your spelling       │
│   • Use fewer keywords        │
│   • Browse all drills         │
│                               │
│   [Clear Search]              │
│   [Browse All]                │
│                               │
└───────────────────────────────┘
```

**Screen**: Drills search  
**Helpful**: Suggestions to try  
**Fallback**: Browse all drills

---

## 🔌 6. Offline Mode

### Offline Banner
```
┌───────────────────────────────┐
│ ⚠️ You're offline. Some      │
│    features are limited.      │
└───────────────────────────────┘
```

**Display**: Sticky top banner  
**Color**: Warning Amber (#F59E0B)  
**Dismissible**: No (auto-hide when online)

---

### Offline Upload Attempt
```
┌───────────────────────────────┐
│                               │
│       [Icon: Cloud Off]       │
│          ☁️❌                  │
│                               │
│   Can't Upload Offline        │
│                               │
│   Your video will be uploaded │
│   automatically when you're   │
│   back online.                │
│                               │
│   [Save for Later]  [Cancel]  │
│                               │
└───────────────────────────────┘
```

**Action**: Queue for later upload  
**Storage**: IndexedDB or local storage  
**Auto-sync**: When connection restored

---

### Offline Analysis
```
┌───────────────────────────────┐
│                               │
│   ⚠️ Analysis Unavailable     │
│                               │
│   Video analysis requires an  │
│   internet connection.        │
│                               │
│   You can:                    │
│   • View past reports         │
│   • Browse drills (cached)    │
│   • Wait for connection       │
│                               │
└───────────────────────────────┘
```

**Feature**: Analysis requires server  
**Fallback**: View cached content  
**Cache Strategy**: Service worker

---

## 🎨 Visual Specifications

### Error Card
```css
.error-card {
  max-width: 400px;
  margin: 40px auto;
  padding: 32px;
  background: #FFFFFF;
  border: 1px solid #FEE2E2; /* Light red */
  border-radius: 12px;
  text-align: center;
}

.error-icon {
  font-size: 64px;
  margin-bottom: 16px;
}

.error-title {
  font-size: 24px;
  font-weight: 600;
  color: #111827;
  margin-bottom: 12px;
}

.error-message {
  font-size: 16px;
  color: #6B7280;
  line-height: 24px;
  margin-bottom: 24px;
}

.error-actions {
  display: flex;
  gap: 12px;
  justify-content: center;
}
```

---

### Empty State
```css
.empty-state {
  max-width: 360px;
  margin: 60px auto;
  padding: 24px;
  text-align: center;
}

.empty-icon {
  font-size: 96px;
  opacity: 0.5;
  margin-bottom: 24px;
}

.empty-title {
  font-size: 20px;
  font-weight: 600;
  color: #111827;
  margin-bottom: 12px;
}

.empty-message {
  font-size: 16px;
  color: #6B7280;
  line-height: 24px;
  margin-bottom: 24px;
}
```

---

### Inline Error
```css
.field-error {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-top: 6px;
  font-size: 14px;
  color: #EF4444; /* Error Red */
}

.field-error-icon {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
}
```

---

### Banner
```css
.banner {
  padding: 12px 16px;
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 14px;
  position: sticky;
  top: 0;
  z-index: 1000;
}

.banner.offline {
  background: #FEF3C7; /* Light amber */
  color: #92400E; /* Dark amber */
  border-bottom: 1px solid #FCD34D;
}

.banner.error {
  background: #FEE2E2; /* Light red */
  color: #991B1B; /* Dark red */
  border-bottom: 1px solid #FCA5A5;
}

.banner.success {
  background: #D1FAE5; /* Light green */
  color: #065F46; /* Dark green */
  border-bottom: 1px solid #6EE7B7;
}
```

---

## 📊 Error State Inventory

### Complete List (18 states)

| # | Error State | Screen | Priority |
|---|-------------|--------|----------|
| 1 | Connection Lost | All | HIGH |
| 2 | Slow Connection | Upload, Processing | HIGH |
| 3 | 404 Not Found | Report | HIGH |
| 4 | 500 Server Error | All API calls | HIGH |
| 5 | 401 Unauthorized | All protected routes | HIGH |
| 6 | 413 File Too Large | Upload | HIGH |
| 7 | Validation Errors | All forms | HIGH |
| 8 | Camera Denied | Live Mode, Assessment | HIGH |
| 9 | Microphone Denied | Live Mode | MEDIUM |
| 10 | Storage Denied | Upload | MEDIUM |
| 11 | No Videos | Upload | MEDIUM |
| 12 | No Reports | Report | MEDIUM |
| 13 | No Drills | Drills | LOW |
| 14 | No Progress | Progress | LOW |
| 15 | Search No Results | Drills | LOW |
| 16 | Offline Banner | All | HIGH |
| 17 | Offline Upload | Upload | HIGH |
| 18 | Offline Analysis | Processing | HIGH |

---

## 🔄 Error Recovery Flows

### Auto-Retry Logic
```typescript
async function fetchWithRetry(
  url: string,
  options: RequestInit,
  maxRetries = 3
) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      const response = await fetch(url, options);
      if (response.ok) return response;
      
      // Don't retry client errors (4xx)
      if (response.status >= 400 && response.status < 500) {
        throw new Error(`HTTP ${response.status}`);
      }
      
      // Retry server errors (5xx)
      if (i < maxRetries - 1) {
        await delay(Math.pow(2, i) * 1000); // Exponential backoff
      }
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      await delay(Math.pow(2, i) * 1000);
    }
  }
}
```

---

### Offline Queue
```typescript
interface QueuedUpload {
  id: string;
  file: Blob;
  metadata: any;
  timestamp: number;
}

class OfflineQueue {
  private queue: QueuedUpload[] = [];
  
  async add(file: Blob, metadata: any) {
    const item: QueuedUpload = {
      id: crypto.randomUUID(),
      file,
      metadata,
      timestamp: Date.now(),
    };
    
    this.queue.push(item);
    await this.saveToStorage();
    
    // Try to process immediately
    if (navigator.onLine) {
      this.processQueue();
    }
  }
  
  async processQueue() {
    while (this.queue.length > 0 && navigator.onLine) {
      const item = this.queue[0];
      try {
        await uploadVideo(item.file, item.metadata);
        this.queue.shift();
        await this.saveToStorage();
      } catch (error) {
        break; // Stop processing on error
      }
    }
  }
}
```

---

## ♿ Accessibility

### Error Announcements
```html
<div
  role="alert"
  aria-live="assertive"
  aria-atomic="true"
>
  Connection lost. Please check your internet.
</div>
```

### Focus Management
- On error: Focus moves to error message
- On retry: Focus moves to retry button
- On success: Focus returns to original element

---

## 📊 Analytics Events

```typescript
// Error occurred
analytics.track('Error Occurred', {
  errorType: string,
  errorCode: number,
  errorMessage: string,
  screen: string,
});

// Error recovered
analytics.track('Error Recovered', {
  errorType: string,
  recoveryMethod: 'retry' | 'alternative' | 'skip',
});

// Offline mode activated
analytics.track('Offline Mode Activated');

// Queued for offline upload
analytics.track('Upload Queued Offline', {
  fileSize: number,
});
```

---

## ✅ Testing Checklist

- [ ] All 18 error states display correctly
- [ ] Error messages are clear and actionable
- [ ] Retry logic works
- [ ] Auto-retry with exponential backoff
- [ ] Offline mode detection
- [ ] Offline queue functionality
- [ ] Permission error handling
- [ ] Form validation errors
- [ ] Empty states render
- [ ] Accessibility (announcements, focus)
- [ ] Analytics events fire
- [ ] Error recovery flows work

---

**Priority**: P0 (Critical for production)  
**Coverage**: 18 error states + 6 empty states  
**Estimated Test Time**: 8-10 hours

---

*Last Updated: December 29, 2025*  
*Error Handling Specification v1.0*
