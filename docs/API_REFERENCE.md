# API Reference
## Catching Barrels PWA
**Version:** 2.0  
**Last Updated:** December 26, 2025  
**Status:** Design Specification — Complete

---

## Table of Contents
1. [Overview](#overview)
2. [Authentication](#authentication)
3. [Player Endpoints](#player-endpoints)
4. [Analysis Endpoints](#analysis-endpoints)
5. [Drills Endpoints](#drills-endpoints)
6. [Progress Endpoints](#progress-endpoints)
7. [Data Models](#data-models)
8. [Error Handling](#error-handling)

---

## 1. Overview

### Base URL
```
Production:  https://api.catchingbarrels.com
Staging:     https://staging-api.catchingbarrels.com
Development: http://localhost:8000
```

### API Version
- Current: `v1`
- Path: `/api/v1/*`

### Authentication
- Type: Bearer Token (JWT)
- Header: `Authorization: Bearer <token>`

### Rate Limiting
- Authenticated: 1000 requests/hour
- Unauthenticated: 100 requests/hour
- Upload: 50 uploads/day per user

---

## 2. Authentication

### 2.1 Register

**POST** `/api/v1/auth/register`

**Request Body:**
```json
{
  "email": "player@example.com",
  "password": "SecurePassword123!",
  "name": "John Doe",
  "age": 16,
  "team": "Central High School"
}
```

**Response (201 Created):**
```json
{
  "user": {
    "id": "user_abc123",
    "email": "player@example.com",
    "name": "John Doe",
    "created_at": "2025-12-26T10:00:00Z"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expires_in": 86400
}
```

---

### 2.2 Login

**POST** `/api/v1/auth/login`

**Request Body:**
```json
{
  "email": "player@example.com",
  "password": "SecurePassword123!"
}
```

**Response (200 OK):**
```json
{
  "user": {
    "id": "user_abc123",
    "email": "player@example.com",
    "name": "John Doe"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expires_in": 86400
}
```

---

## 3. Player Endpoints

### 3.1 Get Player Profile

**GET** `/api/v1/players/{playerId}`

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "id": "player_xyz789",
  "name": "John Doe",
  "age": 16,
  "height_cm": 175,
  "weight_kg": 70,
  "team": "Central High School",
  "position": "Outfielder",
  "motor_profile": {
    "profile": "Whipper",
    "confidence": 92,
    "determined_at": "2025-12-20T14:30:00Z"
  },
  "physical_capacity": {
    "max_exit_velocity_mph": 95,
    "measured_at": "2025-12-25T09:15:00Z"
  },
  "created_at": "2025-12-01T10:00:00Z",
  "updated_at": "2025-12-26T10:00:00Z"
}
```

---

### 3.2 Update Player Profile

**PATCH** `/api/v1/players/{playerId}`

**Headers:**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "name": "John Doe Jr.",
  "height_cm": 177,
  "weight_kg": 72,
  "team": "Central High School Varsity",
  "position": "Center Fielder"
}
```

**Response (200 OK):**
```json
{
  "id": "player_xyz789",
  "name": "John Doe Jr.",
  "age": 16,
  "height_cm": 177,
  "weight_kg": 72,
  "team": "Central High School Varsity",
  "position": "Center Fielder",
  "updated_at": "2025-12-26T11:00:00Z"
}
```

---

### 3.3 Get Player KRS Summary

**GET** `/api/v1/players/{playerId}/krs`

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "player_id": "player_xyz789",
  "krs_score": 75.2,
  "krs_level": "ADVANCED",
  "creation_score": 74.8,
  "transfer_score": 69.5,
  "on_table_gain": {
    "value": 3.1,
    "metric": "mph",
    "description": "Exit velocity improvement with optimal mechanics"
  },
  "last_updated": "2025-12-25T16:45:00Z",
  "total_swings": 150,
  "trend": {
    "last_7_days": 2.3,
    "last_30_days": 5.1
  }
}
```

---

### 3.4 Movement Assessment

**POST** `/api/v1/players/{playerId}/assessment`

**Headers:**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "assessments": [
    {
      "movement": "hip_rotation_r",
      "states": {
        "static_hold": { "score": 85, "notes": "Good stability" },
        "dynamic_movement": { "score": 78, "notes": "Slight compensation" },
        "loaded_position": { "score": 82, "notes": "Strong position" },
        "explosive_output": { "score": 88, "notes": "Excellent power" }
      }
    },
    {
      "movement": "hip_rotation_l",
      "states": { /* ... */ }
    }
    // ... 3 more movements
  ]
}
```

**Response (200 OK):**
```json
{
  "player_id": "player_xyz789",
  "assessment_id": "assess_def456",
  "motor_profile": "Whipper",
  "confidence": 92,
  "profile_scores": {
    "Spinner": 68,
    "Slingshotter": 72,
    "Whipper": 92,
    "Titan": 65
  },
  "recommendations": [
    {
      "category": "4B-Body",
      "focus_area": "Creation",
      "drill_id": "drill_001",
      "reason": "Enhance hip rotation mobility for Whipper profile"
    }
  ],
  "completed_at": "2025-12-26T12:00:00Z"
}
```

---

## 4. Analysis Endpoints

### 4.1 Upload Swing Video

**POST** `/api/v1/analysis/upload`

**Headers:**
```
Authorization: Bearer <token>
Content-Type: multipart/form-data
```

**Request Body (Form Data):**
```
video: <file> (MP4, MOV, AVI; max 100MB)
player_id: "player_xyz789"
recorded_at: "2025-12-26T10:30:00Z"
notes: "Batting practice session"
```

**Response (202 Accepted):**
```json
{
  "swing_id": "swing_ghi012",
  "player_id": "player_xyz789",
  "status": "PROCESSING",
  "estimated_completion": "2025-12-26T10:32:00Z",
  "video_url": "https://storage.catchingbarrels.com/swings/swing_ghi012.mp4",
  "thumbnail_url": "https://storage.catchingbarrels.com/swings/swing_ghi012_thumb.jpg",
  "created_at": "2025-12-26T10:30:15Z"
}
```

---

### 4.2 Get Analysis Status

**GET** `/api/v1/analysis/{swingId}/status`

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "swing_id": "swing_ghi012",
  "status": "PROCESSING",
  "progress": 45,
  "current_stage": "pose_extraction",
  "stages": [
    { "name": "video_validation", "status": "COMPLETED", "duration_ms": 2000 },
    { "name": "pose_extraction", "status": "IN_PROGRESS", "duration_ms": null },
    { "name": "metrics_calculation", "status": "PENDING", "duration_ms": null },
    { "name": "krs_computation", "status": "PENDING", "duration_ms": null }
  ],
  "estimated_completion": "2025-12-26T10:32:00Z",
  "updated_at": "2025-12-26T10:31:00Z"
}
```

**Status Values:**
- `PENDING` — Queued for processing
- `PROCESSING` — Analysis in progress
- `COMPLETED` — Analysis successful
- `FAILED` — Analysis failed (see error field)

---

### 4.3 Get Swing Report

**GET** `/api/v1/analysis/{swingId}/report`

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "swing_id": "swing_ghi012",
  "player_id": "player_xyz789",
  "krs_score": 75.2,
  "krs_level": "ADVANCED",
  "creation_score": 74.8,
  "transfer_score": 69.5,
  "framework_metrics": {
    "brain": {
      "motor_profile": "Whipper",
      "confidence": 92,
      "timing": 0.24
    },
    "body": {
      "creation_score": 74.8,
      "physical_capacity_mph": 95,
      "peak_force_n": 723
    },
    "bat": {
      "transfer_score": 69.5,
      "transfer_efficiency": 82,
      "attack_angle_deg": 12
    },
    "ball": {
      "exit_velocity_mph": 82,
      "capacity_mph": 95,
      "launch_angle_deg": 18,
      "contact_quality": "SOLID"
    }
  },
  "on_table_gain": {
    "value": 3.1,
    "metric": "mph",
    "description": "Exit velocity improvement with optimal mechanics"
  },
  "video_url": "https://storage.catchingbarrels.com/swings/swing_ghi012.mp4",
  "thumbnail_url": "https://storage.catchingbarrels.com/swings/swing_ghi012_thumb.jpg",
  "pose_data_url": "https://storage.catchingbarrels.com/swings/swing_ghi012_pose.json",
  "analyzed_at": "2025-12-26T10:31:45Z"
}
```

---

### 4.4 Live Mode Feedback (WebSocket)

**WebSocket** `wss://api.catchingbarrels.com/ws/live/{sessionId}`

**Connection:**
```javascript
const ws = new WebSocket('wss://api.catchingbarrels.com/ws/live/session_abc123');
ws.onopen = () => {
  ws.send(JSON.stringify({ type: 'AUTH', token: '<bearer_token>' }));
};
```

**Client → Server (Video Frame):**
```json
{
  "type": "FRAME",
  "timestamp": 1672051200000,
  "frame_data": "<base64_encoded_jpeg>"
}
```

**Server → Client (Positional Feedback):**
```json
{
  "type": "FEEDBACK",
  "timestamp": 1672051200000,
  "pose": {
    "hip_rotation": { "angle": 45, "target": 50, "status": "GOOD" },
    "knee_bend": { "angle": 30, "target": 35, "status": "ADJUST" },
    "weight_transfer": { "balance": 0.65, "target": 0.70, "status": "GOOD" }
  },
  "cue": "Rotate hips slightly more"
}
```

**Status Values:**
- `GOOD` — Within optimal range
- `ADJUST` — Needs minor adjustment
- `WARNING` — Significant deviation

---

## 5. Drills Endpoints

### 5.1 Get Drills Library

**GET** `/api/v1/drills`

**Headers:**
```
Authorization: Bearer <token>
```

**Query Parameters:**
```
category: 4B-Brain | 4B-Body | 4B-Bat | 4B-Ball (optional)
difficulty: Beginner | Intermediate | Advanced (optional)
limit: 20 (default)
offset: 0 (default)
```

**Response (200 OK):**
```json
{
  "drills": [
    {
      "id": "drill_001",
      "name": "Hip Rotation Drill",
      "category": "4B-Body",
      "focus_area": "Creation",
      "prescription": "Develop rotational power through progressive hip activation sequences",
      "duration": 5,
      "difficulty": "Intermediate",
      "equipment": "None",
      "thumbnail_url": "https://cdn.catchingbarrels.com/drills/hip-rotation-thumb.jpg",
      "video_url": "https://cdn.catchingbarrels.com/drills/hip-rotation-video.mp4"
    },
    // ... 19 more drills
  ],
  "total": 45,
  "limit": 20,
  "offset": 0
}
```

---

### 5.2 Get Recommended Drills

**GET** `/api/v1/players/{playerId}/recommended-drills`

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "player_id": "player_xyz789",
  "motor_profile": "Whipper",
  "drills": [
    {
      "drill_id": "drill_001",
      "name": "Hip Rotation Drill",
      "category": "4B-Body",
      "focus_area": "Creation",
      "prescription": "Develop rotational power through progressive hip activation sequences",
      "duration": 5,
      "difficulty": "Intermediate",
      "thumbnail_url": "https://cdn.catchingbarrels.com/drills/hip-rotation-thumb.jpg",
      "video_url": "https://cdn.catchingbarrels.com/drills/hip-rotation-video.mp4",
      "reason": "Enhance hip rotation mobility for Whipper profile",
      "expected_gain": "Improve Creation score by 2-3 points"
    },
    // ... 9-14 more recommended drills
  ],
  "generated_at": "2025-12-26T10:00:00Z"
}
```

---

### 5.3 Get Drill Detail

**GET** `/api/v1/drills/{drillId}`

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "id": "drill_001",
  "name": "Hip Rotation Drill",
  "category": "4B-Body",
  "focus_area": "Creation",
  "prescription": "Develop rotational power through progressive hip activation sequences",
  "duration": 5,
  "difficulty": "Intermediate",
  "equipment": "None",
  "benefits": [
    "Improves hip mobility",
    "Increases rotational power",
    "Enhances timing and sequencing"
  ],
  "instructions": [
    "Stand with feet shoulder-width apart",
    "Rotate hips slowly to the right, holding for 3 seconds",
    "Return to center, then rotate left",
    "Repeat 10 times per side"
  ],
  "video_url": "https://cdn.catchingbarrels.com/drills/hip-rotation-video.mp4",
  "thumbnail_url": "https://cdn.catchingbarrels.com/drills/hip-rotation-thumb.jpg",
  "related_drills": ["drill_002", "drill_003"]
}
```

---

## 6. Progress Endpoints

### 6.1 Get Session History

**GET** `/api/v1/players/{playerId}/sessions`

**Headers:**
```
Authorization: Bearer <token>
```

**Query Parameters:**
```
start_date: 2025-12-01 (ISO 8601, optional)
end_date: 2025-12-31 (ISO 8601, optional)
limit: 30 (default)
offset: 0 (default)
```

**Response (200 OK):**
```json
{
  "player_id": "player_xyz789",
  "sessions": [
    {
      "session_id": "session_001",
      "date": "2025-12-25",
      "swing_count": 12,
      "duration_minutes": 45,
      "krs_score": 75.2,
      "krs_delta": 2.1,
      "creation_score": 74.8,
      "transfer_score": 69.5,
      "best_swing": {
        "swing_id": "swing_ghi012",
        "exit_velocity_mph": 82
      }
    },
    // ... 29 more sessions
  ],
  "total": 150,
  "limit": 30,
  "offset": 0
}
```

---

### 6.2 Get Progress Dashboard Data

**GET** `/api/v1/players/{playerId}/progress`

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "player_id": "player_xyz789",
  "total_swings": 150,
  "week_streak": 12,
  "days_since_last_swing": 1,
  "average_krs": 72.5,
  "krs_trend": {
    "current": 75.2,
    "last_session": 73.1,
    "delta": 2.1,
    "direction": "up"
  },
  "creation_trend": {
    "current": 74.8,
    "last_30_days_avg": 72.3,
    "delta": 2.5,
    "direction": "up"
  },
  "transfer_trend": {
    "current": 69.5,
    "last_30_days_avg": 68.1,
    "delta": 1.4,
    "direction": "up"
  },
  "most_improved_area": "Creation (+5.2 points)",
  "session_history": [
    {
      "date": "2025-12-25",
      "krs_score": 75.2,
      "creation_score": 74.8,
      "transfer_score": 69.5
    },
    // ... last 30 sessions
  ],
  "generated_at": "2025-12-26T10:00:00Z"
}
```

---

## 7. Data Models

### 7.1 Player

```typescript
interface Player {
  id: string;
  name: string;
  email: string;
  age: number;
  height_cm: number;
  weight_kg: number;
  team?: string;
  position?: string;
  motor_profile?: MotorProfile;
  physical_capacity?: PhysicalCapacity;
  created_at: string; // ISO 8601
  updated_at: string; // ISO 8601
}
```

---

### 7.2 Motor Profile

```typescript
interface MotorProfile {
  profile: 'Spinner' | 'Slingshotter' | 'Whipper' | 'Titan';
  confidence: number; // 0-100
  determined_at: string; // ISO 8601
}
```

---

### 7.3 Physical Capacity

```typescript
interface PhysicalCapacity {
  max_exit_velocity_mph: number;
  measured_at: string; // ISO 8601
}
```

---

### 7.4 KRS Summary

```typescript
interface KRSSummary {
  player_id: string;
  krs_score: number; // 0-100
  krs_level: 'FOUNDATION' | 'BUILDING' | 'DEVELOPING' | 'ADVANCED' | 'ELITE';
  creation_score: number; // 0-100
  transfer_score: number; // 0-100
  on_table_gain?: OnTableGain;
  last_updated: string; // ISO 8601
  total_swings: number;
  trend?: Trend;
}
```

---

### 7.5 On Table Gain

```typescript
interface OnTableGain {
  value: number;
  metric: 'mph' | 'degrees' | '%';
  description: string;
}
```

---

### 7.6 Framework Metrics

```typescript
interface FrameworkMetrics {
  brain: {
    motor_profile: 'Spinner' | 'Slingshotter' | 'Whipper' | 'Titan';
    confidence: number; // 0-100
    timing: number; // seconds
  };
  body: {
    creation_score: number; // 0-100
    physical_capacity_mph: number;
    peak_force_n: number;
  };
  bat: {
    transfer_score: number; // 0-100
    transfer_efficiency: number; // 0-100%
    attack_angle_deg: number;
  };
  ball: {
    exit_velocity_mph: number;
    capacity_mph: number;
    launch_angle_deg: number;
    contact_quality: 'POOR' | 'FAIR' | 'SOLID' | 'EXCELLENT';
  };
}
```

---

### 7.7 Drill

```typescript
interface Drill {
  id: string;
  name: string;
  category: '4B-Brain' | '4B-Body' | '4B-Bat' | '4B-Ball';
  focus_area: string;
  prescription: string;
  duration: number; // minutes
  difficulty?: 'Beginner' | 'Intermediate' | 'Advanced';
  equipment?: string;
  benefits?: string[];
  instructions?: string[];
  video_url: string;
  thumbnail_url: string;
  related_drills?: string[];
}
```

---

### 7.8 Session

```typescript
interface Session {
  session_id: string;
  player_id: string;
  date: string; // ISO 8601 date
  swing_count: number;
  duration_minutes: number;
  krs_score: number;
  krs_delta: number;
  creation_score: number;
  transfer_score: number;
  best_swing?: {
    swing_id: string;
    exit_velocity_mph: number;
  };
}
```

---

## 8. Error Handling

### 8.1 Error Response Format

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request parameters",
    "details": [
      {
        "field": "age",
        "message": "Age must be between 8 and 18 years"
      }
    ],
    "request_id": "req_abc123",
    "timestamp": "2025-12-26T10:00:00Z"
  }
}
```

---

### 8.2 Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `VALIDATION_ERROR` | 400 | Invalid request parameters |
| `UNAUTHORIZED` | 401 | Missing or invalid authentication token |
| `FORBIDDEN` | 403 | Insufficient permissions |
| `NOT_FOUND` | 404 | Resource not found |
| `CONFLICT` | 409 | Resource conflict (e.g., duplicate email) |
| `RATE_LIMIT_EXCEEDED` | 429 | Too many requests |
| `INTERNAL_ERROR` | 500 | Server error |
| `SERVICE_UNAVAILABLE` | 503 | Service temporarily unavailable |

---

### 8.3 Example Error Responses

**400 Validation Error:**
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid video format",
    "details": [
      {
        "field": "video",
        "message": "Video must be in MP4, MOV, or AVI format"
      }
    ]
  }
}
```

**401 Unauthorized:**
```json
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Invalid or expired authentication token"
  }
}
```

**404 Not Found:**
```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "Swing with ID 'swing_invalid' not found"
  }
}
```

**429 Rate Limit:**
```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Too many requests. Please try again later.",
    "retry_after": 3600
  }
}
```

---

## Summary

### API Overview
- **Base URL:** `https://api.catchingbarrels.com/api/v1`
- **Authentication:** Bearer Token (JWT)
- **Rate Limits:** 1000 req/hour (authenticated), 100 req/hour (unauthenticated)

### Endpoint Categories
1. **Authentication** — Register, Login
2. **Player** — Profile, KRS Summary, Movement Assessment
3. **Analysis** — Upload, Status, Report, Live Mode (WebSocket)
4. **Drills** — Library, Recommendations, Detail
5. **Progress** — Session History, Dashboard Data

### Key Data Models
- **Player:** Profile, Motor Profile, Physical Capacity
- **KRS:** Score (0-100), Level, Creation/Transfer subscores
- **Framework:** Brain, Body, Bat, Ball metrics
- **Drill:** Name, Category, Prescription, Video
- **Session:** Date, Swing Count, KRS, Delta

### Error Handling
- **Standard Format:** code, message, details, request_id
- **HTTP Status Codes:** 400, 401, 403, 404, 409, 429, 500, 503

**Estimated Review Time:** 30-45 minutes  
**Next Steps:** Review endpoints, validate data models, test with Postman/Swagger

---

**Last Updated:** December 26, 2025  
**Contact:** Builder 2 — Phase 0 Corrections
