# 🔌 API DOCUMENTATION - CATCHING BARRELS Training Module

**Version**: 1.0  
**Date**: December 25, 2025  
**Base URL**: `https://api.catchingbarrels.com/v1`

---

## 📋 TABLE OF CONTENTS

1. [Authentication](#authentication)
2. [Core Endpoints](#core-endpoints)
3. [Request/Response Formats](#request-response-formats)
4. [Error Handling](#error-handling)
5. [Rate Limiting](#rate-limiting)
6. [Data Models](#data-models)
7. [Code Examples](#code-examples)

---

## 🔐 AUTHENTICATION

### **API Key Authentication** (Recommended for MVP)

```http
Authorization: Bearer YOUR_API_KEY
```

**Example:**
```bash
curl -X POST https://api.catchingbarrels.com/v1/analyze \
  -H "Authorization: Bearer sk_test_abc123xyz" \
  -H "Content-Type: multipart/form-data" \
  -F "momentum_file=@momentum-energy.csv" \
  -F "kinematics_file=@inverse-kinematics.csv"
```

---

## 🎯 CORE ENDPOINTS

### **1. POST /analyze**

Upload biomechanical data and receive comprehensive swing analysis.

#### **Request:**

```http
POST /api/analyze
Content-Type: multipart/form-data
Authorization: Bearer YOUR_API_KEY
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `momentum_file` | File | Yes | CSV file containing momentum-energy data |
| `kinematics_file` | File | Yes | CSV file containing inverse kinematics data |
| `athlete_name` | String | Yes | Athlete's full name |
| `handedness` | String | Yes | "RHH" or "LHH" |
| `age` | Integer | No | Athlete's age |
| `position` | String | No | Baseball position |

**Example Request:**

```bash
curl -X POST https://api.catchingbarrels.com/v1/analyze \
  -H "Authorization: Bearer sk_test_abc123" \
  -F "momentum_file=@eric_williams_momentum.csv" \
  -F "kinematics_file=@eric_williams_kinematics.csv" \
  -F "athlete_name=Eric Williams" \
  -F "handedness=RHH" \
  -F "age=24" \
  -F "position=OF"
```

#### **Response:**

```json
{
  "status": "success",
  "analysis_id": "anl_8x7a9f2k4d",
  "timestamp": "2025-12-25T15:30:00Z",
  "athlete": {
    "name": "Eric Williams",
    "handedness": "RHH",
    "age": 24,
    "position": "OF"
  },
  "metrics": {
    "lead_knee_angle": 0.3,
    "hip_angular_momentum": 2.10,
    "shoulder_angular_momentum": 18.25,
    "shoulder_hip_ratio": 8.68,
    "bat_speed": 82.0,
    "timing_gap_ms": 158.3,
    "lead_arm_extension": 1.5
  },
  "pattern": {
    "type": "PATTERN_1_KNEE_LEAK",
    "severity": "CRITICAL",
    "title": "Energy Leak at Lead Knee",
    "description": "Your lead knee is flexed at 0.3° (should be 160-180°)...",
    "root_cause": "Coordination issue - lead knee flexing instead of extending",
    "primary_protocol": "PROTOCOL_1",
    "secondary_protocol": "PROTOCOL_2"
  },
  "efficiency": {
    "hip_efficiency": 21.0,
    "knee_efficiency": 0.2,
    "contact_efficiency": 7.5,
    "total_efficiency": 11.2
  },
  "ball_outcomes": {
    "current": {
      "exit_velo": 82.0,
      "launch_angle": 2,
      "gb_rate": 65,
      "ld_rate": 25,
      "breaking_ball_avg": 0.180,
      "spray_chart": {
        "pull_pct": 60,
        "center_pct": 25,
        "oppo_pct": 15
      }
    },
    "predicted": {
      "exit_velo": 89.0,
      "launch_angle": 15,
      "gb_rate": 35,
      "ld_rate": 55,
      "breaking_ball_avg": 0.280,
      "spray_chart": {
        "pull_pct": 40,
        "center_pct": 35,
        "oppo_pct": 25
      }
    },
    "improvement": {
      "exit_velo_gain": 7.0,
      "launch_angle_gain": 13,
      "gb_rate_change": -30,
      "ld_rate_change": 30,
      "breaking_ball_avg_gain": 0.100
    }
  },
  "training_plan": {
    "total_weeks": 6,
    "primary_issue": "Energy Leak at Lead Knee",
    "protocols_used": ["PROTOCOL_1", "PROTOCOL_2", "PROTOCOL_5"],
    "weeks": [
      {
        "week": "1-2",
        "focus": "Fix Lead Knee Leak",
        "drills": [
          {
            "name": "Single-Leg Isometric Holds",
            "sets": 3,
            "reps": "20s",
            "cue": "Steel rod, not shock absorber",
            "description": "Stand on lead leg, knee at 160-170°...",
            "video_url": null
          }
        ],
        "expected_change": "Lead knee 140-160° → 160-180°",
        "downstream_effect": "Hip angmom ↑ by 2-3x"
      }
    ]
  },
  "coach_take": "Your ground forces and timing are elite. But here's the issue: your lead leg isn't extending through the pitch plane...",
  "overall_score": 60.3,
  "report_url": "https://app.catchingbarrels.com/reports/anl_8x7a9f2k4d"
}
```

---

### **2. GET /analysis/:analysis_id**

Retrieve a previously generated analysis.

#### **Request:**

```http
GET /api/analysis/anl_8x7a9f2k4d
Authorization: Bearer YOUR_API_KEY
```

#### **Response:**

Same structure as POST /analyze response.

---

### **3. POST /compare**

Compare two analyses (Before/After training).

#### **Request:**

```http
POST /api/compare
Content-Type: application/json
Authorization: Bearer YOUR_API_KEY
```

**Body:**

```json
{
  "before_analysis_id": "anl_8x7a9f2k4d",
  "after_analysis_id": "anl_9y8b0g3l5e"
}
```

#### **Response:**

```json
{
  "status": "success",
  "comparison_id": "cmp_1a2b3c4d5e",
  "timestamp": "2025-12-25T15:45:00Z",
  "before": {
    "analysis_id": "anl_8x7a9f2k4d",
    "date": "2025-11-01",
    "metrics": {
      "lead_knee_angle": 0.3,
      "hip_angular_momentum": 2.10,
      "exit_velo": 82.0
    }
  },
  "after": {
    "analysis_id": "anl_9y8b0g3l5e",
    "date": "2025-12-25",
    "metrics": {
      "lead_knee_angle": 165.2,
      "hip_angular_momentum": 8.85,
      "exit_velo": 89.5
    }
  },
  "changes": {
    "lead_knee_angle": {
      "delta": 164.9,
      "percent_change": 54966.7,
      "status": "IMPROVED"
    },
    "hip_angular_momentum": {
      "delta": 6.75,
      "percent_change": 321.4,
      "status": "IMPROVED"
    },
    "exit_velo": {
      "delta": 7.5,
      "percent_change": 9.1,
      "status": "IMPROVED"
    }
  },
  "prediction_accuracy": {
    "exit_velo": {
      "predicted": 89.0,
      "actual": 89.5,
      "error": 0.5,
      "accuracy_pct": 99.4
    },
    "launch_angle": {
      "predicted": 15,
      "actual": 14,
      "error": 1,
      "accuracy_pct": 93.3
    }
  },
  "summary": "Excellent progress! Lead knee extension improved dramatically, hip contribution increased 3.2x, and exit velocity gained 7.5 mph. Predictions were accurate within 6%."
}
```

---

### **4. GET /protocols**

Retrieve all available training protocols.

#### **Request:**

```http
GET /api/protocols
Authorization: Bearer YOUR_API_KEY
```

#### **Response:**

```json
{
  "status": "success",
  "protocols": [
    {
      "id": "PROTOCOL_1",
      "name": "Fix Lead Knee Energy Leak",
      "duration_weeks": 2,
      "focus": "Lead knee extension (0.3° → 160-180°)",
      "indications": [
        "Lead knee < 140° at contact",
        "Hip angmom < 5.0",
        "Shoulder/Hip ratio > 3.0x"
      ],
      "expected_outcomes": {
        "lead_knee_angle": "160-180°",
        "hip_angmom_increase": "2-3x"
      }
    },
    {
      "id": "PROTOCOL_2",
      "name": "Develop Vertical Ground Force",
      "duration_weeks": 4,
      "focus": "vGRF 0.8x → 1.5-2.0x bodyweight",
      "equipment_needed": ["Force Pedals (soft + firm)"],
      "indications": [
        "vGRF < 1.2x bodyweight",
        "Fast foot roll pattern",
        "Weak hip deceleration"
      ]
    }
  ]
}
```

---

### **5. GET /protocol/:protocol_id**

Get detailed information about a specific protocol.

#### **Request:**

```http
GET /api/protocol/PROTOCOL_1
Authorization: Bearer YOUR_API_KEY
```

#### **Response:**

```json
{
  "status": "success",
  "protocol": {
    "id": "PROTOCOL_1",
    "name": "Fix Lead Knee Energy Leak",
    "duration_weeks": 2,
    "weeks": [
      {
        "week": "1-2",
        "focus": "Fix Lead Knee Leak",
        "frequency": "Daily",
        "session_duration": "20-30 minutes",
        "drills": [
          {
            "name": "Single-Leg Isometric Holds",
            "sets": 3,
            "reps": "20s",
            "rest": "60s",
            "intensity": "Moderate",
            "cue": "Steel rod, not shock absorber",
            "description": "Stand on lead leg, knee at 160-170°. Push through ball of foot, engage quad + glute.",
            "video_url": null,
            "equipment": ["None"],
            "progression": "Increase hold time to 30s by Week 2"
          }
        ],
        "expected_change": "Lead knee 140-160° → 160-180° at contact",
        "validation_test": "Video swing analysis - measure lead knee angle at contact"
      }
    ]
  }
}
```

---

### **6. POST /export/pdf**

Export analysis report as PDF.

#### **Request:**

```http
POST /api/export/pdf
Content-Type: application/json
Authorization: Bearer YOUR_API_KEY
```

**Body:**

```json
{
  "analysis_id": "anl_8x7a9f2k4d",
  "include_training_plan": true,
  "include_coach_notes": true
}
```

#### **Response:**

```json
{
  "status": "success",
  "pdf_url": "https://cdn.catchingbarrels.com/reports/anl_8x7a9f2k4d.pdf",
  "expires_at": "2025-12-26T15:30:00Z"
}
```

---

## 📦 REQUEST/RESPONSE FORMATS

### **CSV File Requirements:**

#### **momentum-energy.csv:**

**Required Columns:**
- `rel_frame` (int)
- `lowertorso_angular_momentum_mag` (float)
- `torso_angular_momentum_mag` (float)
- `bat_kinetic_energy` (float)
- `lleg_trans_energy` (float)

**Example:**
```csv
rel_frame,lowertorso_angular_momentum_mag,torso_angular_momentum_mag,bat_kinetic_energy
-50,1.25,3.45,15.2
-40,1.89,5.67,28.4
-30,2.10,8.92,45.6
...
0,1.85,18.25,113.59
```

#### **inverse-kinematics.csv:**

**Required Columns:**
- `rel_frame` (int)
- `left_knee` (float) - for RHH lead leg
- `right_knee` (float) - for LHH lead leg
- `torso_rot` (float)

**Example:**
```csv
rel_frame,left_knee,right_knee,torso_rot
-50,145.2,168.3,25.4
-40,138.7,172.1,35.8
-30,125.4,175.2,48.2
...
0,0.3,178.5,85.6
```

---

### **Standard Response Format:**

All API responses follow this structure:

```json
{
  "status": "success" | "error",
  "message": "Optional message",
  "data": { ... },
  "meta": {
    "api_version": "1.0",
    "timestamp": "2025-12-25T15:30:00Z"
  }
}
```

---

## ⚠️ ERROR HANDLING

### **Error Response Format:**

```json
{
  "status": "error",
  "error": {
    "code": "INVALID_FILE_FORMAT",
    "message": "The momentum-energy.csv file is missing required columns",
    "details": {
      "missing_columns": ["rel_frame", "bat_kinetic_energy"],
      "found_columns": ["frame", "lowertorso_angular_momentum_mag"]
    }
  },
  "meta": {
    "api_version": "1.0",
    "timestamp": "2025-12-25T15:30:00Z"
  }
}
```

### **Error Codes:**

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `INVALID_API_KEY` | 401 | API key is invalid or expired |
| `MISSING_PARAMETER` | 400 | Required parameter is missing |
| `INVALID_FILE_FORMAT` | 400 | CSV file format is incorrect |
| `MISSING_COLUMNS` | 400 | Required columns not found in CSV |
| `FRAME_ALIGNMENT_ERROR` | 400 | rel_frame doesn't align between files |
| `NO_CONTACT_FRAME` | 400 | rel_frame = 0 not found (contact frame) |
| `INVALID_HANDEDNESS` | 400 | Handedness must be "RHH" or "LHH" |
| `FILE_TOO_LARGE` | 413 | File exceeds 10MB limit |
| `RATE_LIMIT_EXCEEDED` | 429 | Too many requests |
| `ANALYSIS_NOT_FOUND` | 404 | Analysis ID doesn't exist |
| `SERVER_ERROR` | 500 | Internal server error |

---

## 🚦 RATE LIMITING

**Limits:**
- **Free Tier**: 10 analyses per day
- **Pro Tier**: 100 analyses per day
- **Team Tier**: 500 analyses per day

**Headers:**
```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 87
X-RateLimit-Reset: 1640467200
```

**Rate Limit Exceeded Response:**
```json
{
  "status": "error",
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "You have exceeded your daily analysis limit",
    "details": {
      "limit": 100,
      "reset_at": "2025-12-26T00:00:00Z"
    }
  }
}
```

---

## 📊 DATA MODELS

### **Athlete Model:**

```typescript
interface Athlete {
  id: string;
  name: string;
  handedness: "RHH" | "LHH";
  age?: number;
  position?: string;
  created_at: string;
  updated_at: string;
}
```

### **Analysis Model:**

```typescript
interface Analysis {
  analysis_id: string;
  athlete: Athlete;
  timestamp: string;
  metrics: BiomechanicalMetrics;
  pattern: DiagnosticPattern;
  efficiency: EfficiencyScores;
  ball_outcomes: BallOutcomes;
  training_plan: TrainingPlan;
  coach_take: string;
  overall_score: number;
  report_url: string;
}

interface BiomechanicalMetrics {
  lead_knee_angle: number;
  hip_angular_momentum: number;
  shoulder_angular_momentum: number;
  shoulder_hip_ratio: number;
  bat_speed: number;
  timing_gap_ms: number;
  lead_arm_extension: number;
}

interface DiagnosticPattern {
  type: "PATTERN_1_KNEE_LEAK" | "PATTERN_2_WEAK_HIP" | "PATTERN_3_SPINNER" | "PATTERN_4_SHOULDER_COMP";
  severity: "CRITICAL" | "HIGH" | "MODERATE" | "LOW";
  title: string;
  description: string;
  root_cause: string;
  primary_protocol: string;
  secondary_protocol?: string;
}

interface EfficiencyScores {
  hip_efficiency: number;      // 0-100
  knee_efficiency: number;      // 0-100
  contact_efficiency: number;   // 0-100
  total_efficiency: number;     // 0-100
}

interface BallOutcomes {
  current: OutcomeMetrics;
  predicted: OutcomeMetrics;
  improvement: ImprovementMetrics;
}

interface OutcomeMetrics {
  exit_velo: number;           // mph
  launch_angle: number;        // degrees
  gb_rate: number;             // percent
  ld_rate: number;             // percent
  breaking_ball_avg: number;   // batting average
  spray_chart: SprayChart;
}

interface SprayChart {
  pull_pct: number;
  center_pct: number;
  oppo_pct: number;
}

interface ImprovementMetrics {
  exit_velo_gain: number;
  launch_angle_gain: number;
  gb_rate_change: number;
  ld_rate_change: number;
  breaking_ball_avg_gain: number;
}

interface TrainingPlan {
  total_weeks: number;
  primary_issue: string;
  protocols_used: string[];
  weeks: WeekPlan[];
}

interface WeekPlan {
  week: string;
  focus: string;
  drills: Drill[];
  expected_change: string;
  downstream_effect: string;
}

interface Drill {
  name: string;
  sets: number;
  reps: string | number;
  cue: string;
  description: string;
  video_url?: string;
  equipment?: string[];
  progression?: string;
}
```

---

## 💻 CODE EXAMPLES

### **Python Example:**

```python
import requests

# Configuration
API_KEY = "sk_test_abc123xyz"
BASE_URL = "https://api.catchingbarrels.com/v1"

# Upload and analyze
def analyze_swing(momentum_csv, kinematics_csv, athlete_info):
    """
    Upload biomechanical data and get analysis
    """
    url = f"{BASE_URL}/analyze"
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    
    files = {
        "momentum_file": open(momentum_csv, "rb"),
        "kinematics_file": open(kinematics_csv, "rb")
    }
    
    data = {
        "athlete_name": athlete_info["name"],
        "handedness": athlete_info["handedness"],
        "age": athlete_info.get("age"),
        "position": athlete_info.get("position")
    }
    
    response = requests.post(url, headers=headers, files=files, data=data)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.json())
        return None

# Example usage
athlete = {
    "name": "Eric Williams",
    "handedness": "RHH",
    "age": 24,
    "position": "OF"
}

result = analyze_swing(
    "eric_williams_momentum.csv",
    "eric_williams_kinematics.csv",
    athlete
)

if result:
    print(f"Analysis ID: {result['analysis_id']}")
    print(f"Pattern Detected: {result['pattern']['title']}")
    print(f"Overall Score: {result['overall_score']}/100")
    print(f"Predicted Exit Velo Gain: +{result['ball_outcomes']['improvement']['exit_velo_gain']} mph")
```

### **JavaScript/Node.js Example:**

```javascript
const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');

const API_KEY = 'sk_test_abc123xyz';
const BASE_URL = 'https://api.catchingbarrels.com/v1';

async function analyzeSwing(momentumFile, kinematicsFile, athleteInfo) {
  const form = new FormData();
  form.append('momentum_file', fs.createReadStream(momentumFile));
  form.append('kinematics_file', fs.createReadStream(kinematicsFile));
  form.append('athlete_name', athleteInfo.name);
  form.append('handedness', athleteInfo.handedness);
  if (athleteInfo.age) form.append('age', athleteInfo.age);
  if (athleteInfo.position) form.append('position', athleteInfo.position);
  
  try {
    const response = await axios.post(`${BASE_URL}/analyze`, form, {
      headers: {
        ...form.getHeaders(),
        'Authorization': `Bearer ${API_KEY}`
      }
    });
    
    return response.data;
  } catch (error) {
    console.error('Error:', error.response?.data || error.message);
    return null;
  }
}

// Example usage
const athlete = {
  name: 'Eric Williams',
  handedness: 'RHH',
  age: 24,
  position: 'OF'
};

analyzeSwing(
  'eric_williams_momentum.csv',
  'eric_williams_kinematics.csv',
  athlete
).then(result => {
  if (result) {
    console.log(`Analysis ID: ${result.analysis_id}`);
    console.log(`Pattern: ${result.pattern.title}`);
    console.log(`Overall Score: ${result.overall_score}/100`);
    console.log(`Exit Velo Gain: +${result.ball_outcomes.improvement.exit_velo_gain} mph`);
  }
});
```

### **cURL Example:**

```bash
#!/bin/bash

API_KEY="sk_test_abc123xyz"
BASE_URL="https://api.catchingbarrels.com/v1"

# Analyze swing
curl -X POST "${BASE_URL}/analyze" \
  -H "Authorization: Bearer ${API_KEY}" \
  -F "momentum_file=@eric_williams_momentum.csv" \
  -F "kinematics_file=@eric_williams_kinematics.csv" \
  -F "athlete_name=Eric Williams" \
  -F "handedness=RHH" \
  -F "age=24" \
  -F "position=OF"

# Get analysis by ID
curl -X GET "${BASE_URL}/analysis/anl_8x7a9f2k4d" \
  -H "Authorization: Bearer ${API_KEY}"

# Compare before/after
curl -X POST "${BASE_URL}/compare" \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "before_analysis_id": "anl_8x7a9f2k4d",
    "after_analysis_id": "anl_9y8b0g3l5e"
  }'
```

---

## 🧪 TESTING ENDPOINTS

### **Health Check:**

```http
GET /api/health
```

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0",
  "timestamp": "2025-12-25T15:30:00Z"
}
```

### **Validate CSV:**

```http
POST /api/validate-csv
Content-Type: multipart/form-data
```

**Parameters:**
- `file`: CSV file to validate
- `file_type`: "momentum" or "kinematics"

**Response:**
```json
{
  "status": "success",
  "validation": {
    "valid": true,
    "file_type": "momentum",
    "rows": 755,
    "columns_found": ["rel_frame", "lowertorso_angular_momentum_mag", ...],
    "missing_columns": [],
    "warnings": []
  }
}
```

---

## 📚 ADDITIONAL RESOURCES

- **Swagger/OpenAPI Spec**: `https://api.catchingbarrels.com/docs`
- **Postman Collection**: Available upon request
- **SDK Libraries**: Python, JavaScript (coming soon)
- **Webhooks**: For async processing (enterprise tier)

---

**API Version**: 1.0  
**Last Updated**: December 25, 2025  
**Support**: api-support@catchingbarrels.com

---

*End of API Documentation*
