"""
Coach Rick AI Engine - Unified API Routes
==========================================

Main endpoint: POST /api/v1/reboot-lite/analyze-with-coach
Integrates all Coach Rick AI components into single response

Author: Builder 2
Date: 2024-12-24
Status: Phase 4 - Unified API
"""

import os
import uuid
from datetime import datetime
from typing import Optional, List, Dict
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import BaseModel, Field
import json

# Coach Rick AI Components
from coach_rick.motor_profile_classifier import classify_motor_profile
from coach_rick.pattern_recognition import PatternRecognitionEngine
from coach_rick.drill_prescription import DrillPrescriptionEngine
from coach_rick.conversational_ai import ConversationalAI

# Reboot Lite components (existing)
# These would be imported from your existing Reboot Lite API
# For now, we'll create mock responses


# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class CoachRickAnalysisRequest(BaseModel):
    """Request model for Coach Rick AI analysis"""
    player_name: str = Field(..., description="Player's name")
    player_id: Optional[str] = Field(None, description="Player ID (optional)")
    height_inches: float = Field(..., description="Player height in inches")
    weight_lbs: float = Field(..., description="Player weight in lbs")
    age: int = Field(..., description="Player age")
    bat_weight_oz: Optional[float] = Field(30.0, description="Bat weight in oz")
    wingspan_inches: Optional[float] = Field(None, description="Wingspan in inches")


class MotorProfileResponse(BaseModel):
    """Motor profile classification"""
    type: str  # Spinner, Whipper, Torquer
    confidence: float
    characteristics: List[str]


class PatternResponse(BaseModel):
    """Detected pattern/issue"""
    pattern_id: str
    name: str
    description: str
    severity: str  # HIGH, MEDIUM, LOW
    root_cause: str
    symptoms: List[str]


class DrillResponse(BaseModel):
    """Prescribed drill"""
    drill_id: str
    name: str
    category: str
    volume: str
    frequency: str
    key_cues: List[str]


class PrescriptionResponse(BaseModel):
    """Complete drill prescription"""
    drills: List[DrillResponse]
    duration_weeks: int
    expected_gains: str
    weekly_schedule: Dict[str, List[Dict]]  # Changed from List[str] to List[Dict]


class CoachMessagesResponse(BaseModel):
    """Coach Rick AI messages"""
    analysis: str
    drill_intro: str
    encouragement: str


class CoachRickAnalysisResponse(BaseModel):
    """Complete Coach Rick AI analysis response"""
    session_id: str
    player_name: str
    timestamp: str
    
    # Core metrics (from Reboot Lite)
    bat_speed_mph: float
    exit_velocity_mph: float
    efficiency_percent: float
    
    # Motor profile
    motor_profile: MotorProfileResponse
    
    # Patterns detected
    patterns: List[PatternResponse]
    primary_issue: str
    
    # Drill prescription
    prescription: PrescriptionResponse
    
    # Coach Rick messages
    coach_messages: CoachMessagesResponse
    
    # Additional metrics
    tempo_score: float
    stability_score: float
    gew_overall: float


# ============================================================================
# API ROUTER
# ============================================================================

router = APIRouter(prefix="/api/v1/reboot-lite", tags=["Coach Rick AI"])


# ============================================================================
# MAIN ENDPOINT: ANALYZE WITH COACH RICK
# ============================================================================

@router.post("/analyze-with-coach", response_model=CoachRickAnalysisResponse)
async def analyze_swing_with_coach(
    video: UploadFile = File(..., description="Swing video file"),
    player_name: str = Form(..., description="Player's name"),
    height_inches: float = Form(..., description="Player height in inches"),
    weight_lbs: float = Form(..., description="Player weight in lbs"),
    age: int = Form(..., description="Player age"),
    player_id: Optional[str] = Form(None, description="Player ID (optional)"),
    bat_weight_oz: Optional[float] = Form(30.0, description="Bat weight in oz"),
    wingspan_inches: Optional[float] = Form(None, description="Wingspan in inches")
):
    """
    🧠 ANALYZE SWING WITH COACH RICK AI
    
    Complete swing analysis with personalized AI coaching:
    1. Video analysis (Reboot Lite pipeline)
    2. Motor profile classification
    3. Pattern recognition (mechanical issues)
    4. Drill prescription (personalized training plan)
    5. Coach Rick AI messages (GPT-4 powered)
    
    Returns:
        Complete analysis with Coach Rick's personalized feedback
    """
    
    try:
        # Generate session ID
        session_id = f"coach_rick_{uuid.uuid4().hex[:12]}"
        
        # ====================================================================
        # STEP 1: REBOOT LITE VIDEO ANALYSIS
        # ====================================================================
        # In production, this would call your existing Reboot Lite pipeline
        # For now, we'll use mock data based on Eric Williams profile
        
        reboot_lite_metrics = await _analyze_video_reboot_lite(
            video=video,
            height_inches=height_inches,
            weight_lbs=weight_lbs,
            age=age,
            bat_weight_oz=bat_weight_oz,
            wingspan_inches=wingspan_inches
        )
        
        # ====================================================================
        # STEP 2: MOTOR PROFILE CLASSIFICATION
        # ====================================================================
        motor_profile_result = classify_motor_profile({
            'hip_shoulder_gap_ms': reboot_lite_metrics['hip_shoulder_gap_ms'],
            'hands_bat_gap_ms': reboot_lite_metrics['hands_bat_gap_ms'],
            'tempo_ratio': reboot_lite_metrics['tempo_ratio'],
            'stability_score': reboot_lite_metrics['stability_score']
        })
        
        motor_profile = MotorProfileResponse(
            type=motor_profile_result.profile,
            confidence=motor_profile_result.confidence * 100,  # Convert to percentage
            characteristics=motor_profile_result.characteristics
        )
        
        # ====================================================================
        # STEP 3: PATTERN RECOGNITION
        # ====================================================================
        pattern_engine = PatternRecognitionEngine()
        
        pattern_matches = pattern_engine.analyze(
            swing_data=reboot_lite_metrics,
            motor_profile=motor_profile.type
        )
        
        # Convert PatternMatch objects to dictionaries for response
        detected_patterns = [
            {
                'pattern_id': pm.pattern_id,
                'name': pm.diagnosis,
                'description': pm.root_cause,
                'severity': pm.priority,
                'root_cause': pm.root_cause,
                'symptoms': pm.symptoms
            }
            for pm in pattern_matches
        ]
        
        patterns = [
            PatternResponse(
                pattern_id=p['pattern_id'],
                name=p['name'],
                description=p['description'],
                severity=p['severity'],
                root_cause=p['root_cause'],
                symptoms=p['symptoms']
            )
            for p in detected_patterns
        ]
        
        primary_issue = patterns[0].name if patterns else "No significant issues detected"
        
        # ====================================================================
        # STEP 4: DRILL PRESCRIPTION
        # ====================================================================
        prescription_engine = DrillPrescriptionEngine()
        
        # Use the primary pattern for prescription
        if pattern_matches:
            prescription_obj = prescription_engine.prescribe(pattern_matches[0])
            
            # Convert to response model
            drills = [
                DrillResponse(
                    drill_id=drill['drill_id'],
                    name=drill['drill_name'],  # Use drill_name from knowledge base
                    category=drill['category'],
                    volume=drill['volume'],
                    frequency=drill['frequency'],
                    key_cues=drill['coaching_cues']  # Use coaching_cues from knowledge base
                )
                for drill in prescription_obj.drills
            ]
            
            prescription = PrescriptionResponse(
                drills=drills,
                duration_weeks=prescription_obj.duration_weeks,
                expected_gains=prescription_obj.expected_gains,
                weekly_schedule=prescription_obj.weekly_schedule
            )
        else:
            # No patterns detected - provide general training
            prescription = PrescriptionResponse(
                drills=[],
                duration_weeks=2,
                expected_gains="Maintain current performance with consistent training",
                weekly_schedule={}
            )
        
        # ====================================================================
        # STEP 5: COACH RICK AI MESSAGES
        # ====================================================================
        coach_ai = ConversationalAI()
        
        # Analysis message
        analysis_msg = coach_ai.generate_analysis_message(
            player_name=player_name,
            motor_profile=motor_profile.type,
            confidence=motor_profile.confidence,
            patterns=[p.dict() for p in patterns],
            metrics={
                'bat_speed_mph': reboot_lite_metrics['bat_speed_mph'],
                'exit_velocity_mph': reboot_lite_metrics['exit_velocity_mph'],
                'efficiency_percent': reboot_lite_metrics['efficiency_percent']
            }
        )
        
        # Drill introduction
        drill_intro_msg = coach_ai.generate_drill_introduction(
            player_name=player_name,
            primary_issue=primary_issue,
            drill_name=drills[0].name if drills else "Training",
            expected_gains=prescription.expected_gains
        )
        
        # Encouragement
        encouragement_msg = coach_ai.generate_encouragement(
            player_name=player_name,
            context="general"
        )
        
        coach_messages = CoachMessagesResponse(
            analysis=analysis_msg.content,
            drill_intro=drill_intro_msg.content,
            encouragement=encouragement_msg.content
        )
        
        # ====================================================================
        # STEP 6: BUILD COMPLETE RESPONSE
        # ====================================================================
        response = CoachRickAnalysisResponse(
            session_id=session_id,
            player_name=player_name,
            timestamp=datetime.utcnow().isoformat(),
            
            # Core metrics
            bat_speed_mph=reboot_lite_metrics['bat_speed_mph'],
            exit_velocity_mph=reboot_lite_metrics['exit_velocity_mph'],
            efficiency_percent=reboot_lite_metrics['efficiency_percent'],
            
            # Motor profile
            motor_profile=motor_profile,
            
            # Patterns
            patterns=patterns,
            primary_issue=primary_issue,
            
            # Prescription
            prescription=prescription,
            
            # Coach messages
            coach_messages=coach_messages,
            
            # Additional metrics
            tempo_score=reboot_lite_metrics['tempo_score'],
            stability_score=reboot_lite_metrics['stability_score'],
            gew_overall=reboot_lite_metrics['gew_overall']
        )
        
        # ====================================================================
        # STEP 7: SAVE TO DATABASE (Optional)
        # ====================================================================
        # In production, save to coach_rick_analyses table
        # await _save_to_database(response, player_id)
        
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Coach Rick AI analysis failed: {str(e)}"
        )


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

async def _analyze_video_reboot_lite(
    video: UploadFile,
    height_inches: float,
    weight_lbs: float,
    age: int,
    bat_weight_oz: float,
    wingspan_inches: Optional[float]
) -> Dict:
    """
    Run Reboot Lite video analysis pipeline
    
    In production, this would:
    1. Save video file
    2. Run MediaPipe pose detection
    3. Calculate kinematic sequence
    4. Compute tempo, stability, GEW scores
    5. Predict exit velocity
    
    For now, returns mock data based on Eric Williams profile
    """
    
    # Mock data (replace with actual Reboot Lite pipeline)
    return {
        # Core metrics
        'bat_speed_mph': 82.0,
        'exit_velocity_mph': 99.0,
        'efficiency_percent': 111.0,
        
        # Kinematic sequence
        'hip_shoulder_gap_ms': 20,
        'hands_bat_gap_ms': 15,
        'tempo_ratio': 2.1,
        
        # Scores
        'tempo_score': 87.0,
        'stability_score': 92.0,
        'gew_overall': 88.5,
        
        # Video metadata
        'video_filename': video.filename,
        'frames_analyzed': 120,
        'fps': 30.0,
        'duration_seconds': 4.0
    }


# ============================================================================
# HEALTH CHECK
# ============================================================================

@router.get("/coach-rick/health")
async def coach_rick_health():
    """Health check for Coach Rick AI Engine"""
    return {
        "status": "healthy",
        "service": "Coach Rick AI Engine",
        "version": "1.0.0",
        "components": {
            "motor_profile_classifier": "✅ operational",
            "pattern_recognition": "✅ operational",
            "drill_prescription": "✅ operational",
            "conversational_ai": "✅ operational (fallback mode)"
        }
    }


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("COACH RICK API - MODULE TEST")
    print("="*70)
    print("\nAPI Routes:")
    print("  POST /api/v1/reboot-lite/analyze-with-coach")
    print("  GET  /api/v1/reboot-lite/coach-rick/health")
    print("\n" + "="*70)
    print("✅ API MODULE LOADED SUCCESSFULLY")
    print("="*70 + "\n")
