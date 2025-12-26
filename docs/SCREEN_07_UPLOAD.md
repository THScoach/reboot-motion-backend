# Screen 07: Upload

**Screen Name**: Upload Video  
**Route**: `/upload`  
**Complexity**: LOW (Simple upload UI)  
**Priority**: P0 (Critical Path)

---

## 📐 Layout Overview

```
┌───────────────────────────────┐
│  ← Home          Upload   🔔  │ ← Header
├───────────────────────────────┤
│                               │
│  Upload Your Swing            │ ← Heading-01
│                               │
│  Record a new video or        │ ← Body-02
│  upload an existing one.      │
│                               │
│  ┌─────────────────────────┐ │
│  │                         │ │
│  │        📹               │ │ ← Upload area
│  │                         │ │   (dashed border)
│  │   Tap to upload or      │ │
│  │   drag and drop         │ │
│  │                         │ │
│  │   MP4, MOV, AVI         │ │
│  │   Max 500MB             │ │
│  │                         │ │
│  └─────────────────────────┘ │
│                               │
│  or                           │
│                               │
│  [Record Live Swing]          │ ← Secondary button
│                               │
│                               │
│  Recent Uploads               │ ← Section heading
│  ┌─────────────────────────┐ │
│  │ [Thumbnail] 2 hours ago │ │ ← Recent item
│  │ Analyzed • View Report  │ │
│  └─────────────────────────┘ │
│  ┌─────────────────────────┐ │
│  │ [Thumbnail] Yesterday   │ │
│  │ Analyzed • View Report  │ │
│  └─────────────────────────┘ │
│                               │
└───────────────────────────────┘
│  Home  Upload  Report  More  │ ← Bottom Nav
└───────────────────────────────┘
```

---

## 🎨 Visual Specifications

### Upload Area
```css
width: 100%;
min-height: 280px;
border: 2px dashed #D1D5DB; /* Gray-300 */
border-radius: 12px;
background: #FFFFFF;
display: flex;
flex-direction: column;
align-items: center;
justify-content: center;
cursor: pointer;
transition: all 200ms ease;
```

**Hover**:
```css
border-color: #06B6D4; /* Electric Cyan */
background: #F0F9FF; /* Very light cyan */
```

**Active (Dragging)**:
```css
border-color: #0284C7; /* Darker cyan */
background: #E0F2FE; /* Light cyan */
transform: scale(0.98);
```

### Upload Icon
- Icon: `<Upload />` from Lucide React
- Size: 48px
- Color: Electric Cyan (#06B6D4)

### Upload Text
```css
font-size: 16px;
color: #374151; /* Gray-700 */
font-weight: 500;
margin-top: 16px;
text-align: center;
```

### Upload Hint
```css
font-size: 14px;
color: #9CA3AF; /* Gray-400 */
margin-top: 8px;
text-align: center;
```

### Divider ("or")
```css
display: flex;
align-items: center;
margin: 24px 0;
color: #9CA3AF; /* Gray-400 */
font-size: 14px;
```

**Line**:
```css
flex: 1;
height: 1px;
background: #E5E7EB; /* Gray-200 */
margin: 0 16px;
```

### Record Button
```css
width: 100%;
height: 48px;
background: transparent;
border: 2px solid #06B6D4; /* Electric Cyan */
color: #06B6D4;
border-radius: 8px;
font-size: 16px;
font-weight: 600;
cursor: pointer;
transition: all 200ms ease;
```

**Hover**:
```css
background: #06B6D4;
color: #FFFFFF;
```

### Recent Uploads Section
```css
margin-top: 40px;
```

**Heading**:
```css
font-size: 18px;
font-weight: 600;
color: #111827; /* Gray-900 */
margin-bottom: 16px;
```

### Recent Item Card
```css
background: #FFFFFF;
border: 1px solid #E5E7EB; /* Gray-200 */
border-radius: 12px;
padding: 16px;
margin-bottom: 12px;
display: flex;
gap: 16px;
cursor: pointer;
transition: all 200ms ease;
```

**Hover**:
```css
border-color: #06B6D4; /* Electric Cyan */
box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
```

**Thumbnail**:
```css
width: 80px;
height: 80px;
border-radius: 8px;
object-fit: cover;
background: #F3F4F6; /* Gray-100 */
```

**Content**:
```css
flex: 1;
display: flex;
flex-direction: column;
justify-content: center;
```

**Timestamp**:
```css
font-size: 14px;
color: #6B7280; /* Gray-500 */
margin-bottom: 4px;
```

**Status**:
```css
font-size: 14px;
color: #10B981; /* Success Green */
font-weight: 500;
```

**Action Link**:
```css
font-size: 14px;
color: #06B6D4; /* Electric Cyan */
margin-left: 4px;
text-decoration: underline;
```

---

## 🎬 Upload Flow

### 1. File Selection
```typescript
const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
  const file = e.target.files?.[0];
  if (!file) return;
  
  // Validate file type
  const validTypes = ['video/mp4', 'video/quicktime', 'video/x-msvideo'];
  if (!validTypes.includes(file.type)) {
    showError('Please upload a valid video file (MP4, MOV, or AVI)');
    return;
  }
  
  // Validate file size (500MB)
  if (file.size > 500 * 1024 * 1024) {
    showError('File size must be less than 500MB');
    return;
  }
  
  // Start upload
  uploadVideo(file);
};
```

### 2. Drag & Drop
```typescript
const handleDrop = (e: React.DragEvent) => {
  e.preventDefault();
  const file = e.dataTransfer.files[0];
  
  // Same validation as file select
  // ...
  
  uploadVideo(file);
};

const handleDragOver = (e: React.DragEvent) => {
  e.preventDefault();
  setIsDragging(true);
};

const handleDragLeave = () => {
  setIsDragging(false);
};
```

### 3. Upload to Supabase
```typescript
const uploadVideo = async (file: File) => {
  try {
    // Generate unique filename
    const timestamp = Date.now();
    const filename = `${userId}_${timestamp}_${file.name}`;
    
    // Upload to Supabase Storage
    const { data, error } = await supabase.storage
      .from('swing-videos')
      .upload(filename, file, {
        cacheControl: '3600',
        upsert: false,
      });
    
    if (error) throw error;
    
    // Create session record
    const session = await createSession({
      user_id: userId,
      video_url: data.path,
      status: 'uploaded',
    });
    
    // Navigate to processing screen
    router.push(`/processing/${session.id}`);
    
  } catch (error) {
    showError('Upload failed. Please try again.');
  }
};
```

---

## 📱 Responsive Behavior

### Mobile (< 768px)
- Upload area: Full width, 240px height
- Thumbnail: 80×80
- Padding: 24px

### Tablet (768px - 1023px)
- Upload area: Full width, 280px height
- Thumbnail: 96×96
- Padding: 32px

### Desktop (1024px+)
- Upload area: Max 600px, 320px height
- Thumbnail: 112×112
- Padding: 40px

---

## ♿ Accessibility

### Upload Area
```html
<div
  role="button"
  tabIndex={0}
  aria-label="Upload video file"
  onClick={handleClick}
  onKeyPress={(e) => e.key === 'Enter' && handleClick()}
  onDrop={handleDrop}
  onDragOver={handleDragOver}
  onDragLeave={handleDragLeave}
>
  <input
    type="file"
    accept="video/mp4,video/quicktime,video/x-msvideo"
    onChange={handleFileSelect}
    hidden
    aria-hidden="true"
  />
  <Upload size={48} />
  <p>Tap to upload or drag and drop</p>
  <p>MP4, MOV, AVI • Max 500MB</p>
</div>
```

### Screen Reader
- Upload area announced as button
- File input hidden but functional
- Error messages announced
- Success feedback provided

---

## 🎯 File Validation

### Accepted Formats
- **MP4**: video/mp4
- **MOV**: video/quicktime
- **AVI**: video/x-msvideo

### Size Limit
- **Maximum**: 500MB
- **Recommended**: 50-100MB

### Quality Guidelines
- **Resolution**: 720p or higher
- **Frame Rate**: 30 FPS or higher
- **Duration**: 5-30 seconds

---

## 📊 Analytics Events

```typescript
// Upload viewed
analytics.track('Upload Screen Viewed');

// File selected
analytics.track('Video File Selected', {
  fileType: string,
  fileSize: number,
});

// Upload started
analytics.track('Video Upload Started', {
  fileSize: number,
});

// Upload completed
analytics.track('Video Upload Completed', {
  sessionId: string,
  fileSize: number,
  duration: number, // ms
});

// Upload failed
analytics.track('Video Upload Failed', {
  error: string,
});

// Record live clicked
analytics.track('Record Live Clicked');

// Recent video clicked
analytics.track('Recent Video Clicked', {
  sessionId: string,
});
```

---

## 🔍 Testing Checklist

- [ ] Upload area renders
- [ ] File select works
- [ ] Drag & drop works
- [ ] File validation works
- [ ] Size validation works
- [ ] Upload to Supabase
- [ ] Session creation
- [ ] Navigation to processing
- [ ] Error handling
- [ ] Recent uploads display
- [ ] Record button works
- [ ] Responsive design
- [ ] Keyboard accessible
- [ ] Screen reader accessible

---

## ✅ Definition of Done

- [ ] Upload UI implemented
- [ ] File select functional
- [ ] Drag & drop functional
- [ ] File validation
- [ ] Supabase upload
- [ ] Session creation
- [ ] Recent uploads list
- [ ] Record button link
- [ ] Error handling
- [ ] Responsive design
- [ ] Accessibility
- [ ] Analytics

---

**Priority**: P0 (Critical Path)  
**Complexity**: LOW (Simple upload UI)  
**Estimated Dev Time**: 4-6 hours (Phase 1)

**Dependencies**:
- Supabase Storage configured
- Video processing pipeline
- Session storage table

---

*Last Updated: December 27, 2025*  
*Screen Specification v1.0*
