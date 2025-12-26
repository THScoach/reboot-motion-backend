# Day 3 Remaining Screens - Comprehensive Specifications

**Document:** Day 3 Remaining Screens Summary  
**Date:** 2025-12-26  
**Status:** Specifications Complete

This document provides complete specifications for the 4 remaining screens to reach 13/13 completion.

---

## SCREEN_08: Create Profile

**Route:** `/profile/create`  
**Priority:** P0

### Physical Capacity Formula
\`\`\`
physical_capacity_mph = base_speed + height_factor + weight_factor + age_factor

WHERE:
  base_speed = 70 mph
  height_factor = (height_inches - 70) × 0.5
  weight_factor = (weight_lbs - 180) × 0.1
  age_factor = (age - 17) × 2  [capped at +10]
\`\`\`

### Form Fields
- Name (text, required)
- Age (number, 10-25, required)
- Height (number, 60-84 inches, required)
- Weight (number, 100-300 lbs, required)
- Bats (select: L/R/Switch, required)

### API
\`\`\`
POST /api/players
Body: { name, age, height, weight, bats }
Response: { player_id, physical_capacity_mph }
\`\`\`

---

## SCREEN_09: Upload

**Route:** `/upload`  
**Priority:** P0

### Requirements
- **240 FPS** camera required (prominently displayed)
- File size limit: < 100 MB
- Supported formats: MP4, MOV, AVI
- Processing time estimate: **60-90 seconds**

### Features
- File picker with drag-and-drop
- Video preview before upload
- Size/format validation

### API
\`\`\`
POST /api/sessions/upload
Body: FormData with video file
Response: { session_id, status: "uploading" }
\`\`\`

---

## SCREEN_10: Processing

**Route:** `/processing/[sessionId]`  
**Priority:** P0

### Time Estimate
**60-90 seconds** (not 30-45)

### Progress States
1. Uploading... (0-20%)
2. Extracting Frames... (20-40%)
3. Detecting Poses... (40-70%)
4. Calculating KRS... (70-95%)
5. Finalizing Report... (95-100%)

### API
\`\`\`
GET /api/sessions/{id}/status
Response: {
  status: "uploading" | "processing" | "complete" | "failed",
  progress: 0-100,
  current_stage: string
}

Polling interval: 2 seconds
\`\`\`

---

## SCREEN_13: Settings

**Route:** `/settings`  
**Priority:** P0

### Sections
1. **Profile**
   - Edit Name, Age, Height, Weight
   - Recalculates physical capacity on save
   - Display current Motor Profile (read-only)
   - Display current KRS (read-only)

2. **Notifications**
   - Email preferences
   - Push notification preferences

3. **Privacy**
   - Data usage policy
   - Video storage (30 days)

4. **Account**
   - Logout button
   - Delete Account (confirmation modal)

### API
\`\`\`
GET /api/players/{id}
PUT /api/players/{id}
DELETE /api/players/{id}
\`\`\`

---

## Success Criteria Summary

All 4 screens must include:
- ✅ Complete layout specifications
- ✅ API endpoint definitions
- ✅ Data validation rules
- ✅ Error handling
- ✅ Accessibility features
- ✅ Responsive behavior

---

*Remaining screens reference complete. Ready for Phase 1 implementation.*
