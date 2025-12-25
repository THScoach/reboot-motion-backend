"""
Swing DNA API Endpoints
FastAPI router for CSV upload, analysis, and report generation

Author: Coach Rick AI
Date: 2025-12-25
"""

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional, Dict, Any
import pandas as pd
import io
import traceback
from datetime import datetime

# Import Swing DNA modules
from .csv_parser import CSVParser
from .pattern_recognition import diagnose_swing_pattern, PatternDiagnosis
from .efficiency_calculator import calculate_efficiency_scores
from .ball_outcome_predictor import predict_ball_outcomes
from .training_plan_generator import generate_training_plan
from .coach_take_generator import generate_coach_take


# Create router
router = APIRouter(prefix="/api/swing-dna", tags=["Swing DNA"])


# In-memory storage (replace with database in production)
ANALYSIS_RESULTS = {}


@router.post("/analyze")
async def analyze_swing(
    momentum_file: UploadFile = File(..., description="Momentum-energy CSV file"),
    kinematics_file: UploadFile = File(..., description="Inverse-kinematics CSV file"),
    athlete_name: str = Form(..., description="Athlete's name"),
    handedness: str = Form("RHH", description="RHH or LHH")
):
    """
    Analyze swing from CSV uploads
    
    Uploads:
    - momentum_file: momentum-energy.csv (angular momentum, kinetic energy)
    - kinematics_file: inverse-kinematics.csv (joint angles, positions)
    
    Returns:
    - Complete Swing DNA report with diagnosis, predictions, training plan
    """
    try:
        # Read CSV files
        momentum_content = await momentum_file.read()
        kinematics_content = await kinematics_file.read()
        
        momentum_df = pd.read_csv(io.BytesIO(momentum_content))
        kinematics_df = pd.read_csv(io.BytesIO(kinematics_content))
        
        # Parse data using CSVParser
        parser = CSVParser()
        swing_metrics = parser.parse_files(momentum_df, kinematics_df)
        
        # Convert to dict for compatibility
        metrics = parser.to_dict(swing_metrics)
        
        # Diagnose pattern
        pattern = diagnose_swing_pattern(swing_metrics)
        
        # Calculate efficiency
        efficiency = calculate_efficiency_scores(metrics)
        
        # Predict ball outcomes
        ball_outcomes = predict_ball_outcomes(metrics, efficiency, pattern)
        
        # Generate training plan
        training_result = generate_training_plan(athlete_name, pattern, metrics)
        
        # Generate Coach Rick's Take
        coach_take = generate_coach_take(
            pattern,
            metrics,
            ball_outcomes["current"],
            ball_outcomes["predicted"]
        )
        
        # Calculate overall score
        overall_score = (
            efficiency["hip_efficiency"] * 0.3 +
            efficiency["knee_efficiency"] * 0.3 +
            efficiency["contact_efficiency"] * 0.4
        )
        
        # Build complete result
        result = {
            "analysis_id": f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "athlete": {
                "name": athlete_name,
                "handedness": handedness
            },
            "metrics": metrics,
            "pattern": pattern.to_dict(),
            "efficiency": efficiency,
            "ball_outcomes": ball_outcomes,
            "training_plan": training_result["training_plan"],
            "drill_summary": training_result["drill_summary"],
            "timeline": training_result["timeline"],
            "coach_take": coach_take,
            "overall_score": round(overall_score, 1),
            "created_at": datetime.now().isoformat()
        }
        
        # Store result
        ANALYSIS_RESULTS[result["analysis_id"]] = result
        
        return JSONResponse(content=result)
    
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )


@router.get("/analysis/{analysis_id}")
async def get_analysis(analysis_id: str):
    """
    Retrieve stored analysis by ID
    """
    if analysis_id not in ANALYSIS_RESULTS:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    return JSONResponse(content=ANALYSIS_RESULTS[analysis_id])


@router.get("/analysis/{analysis_id}/report")
async def get_report(analysis_id: str):
    """
    Get formatted report for display
    """
    if analysis_id not in ANALYSIS_RESULTS:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    data = ANALYSIS_RESULTS[analysis_id]
    
    # Format for frontend display
    report = {
        "header": {
            "athlete_name": data["athlete"]["name"],
            "handedness": data["athlete"]["handedness"],
            "date": data["created_at"],
            "overall_score": data["overall_score"]
        },
        "ball_outcomes": {
            "current": data["ball_outcomes"]["current"],
            "predicted": data["ball_outcomes"]["predicted"],
            "improvement": data["ball_outcomes"]["improvement"]
        },
        "diagnosis": {
            "pattern": data["pattern"]["pattern"],
            "severity": data["pattern"]["severity"],
            "root_cause": data["pattern"]["root_cause"],
            "confidence": data["pattern"]["confidence"],
            "visual_cues": data["pattern"].get("visual_cues", [])
        },
        "training_plan": {
            "weeks": data["training_plan"]["weeks"],
            "protocols": data["training_plan"]["protocols_used"],
            "drill_summary": data["drill_summary"]
        },
        "coach_take": data["coach_take"]["full_text"],
        "metrics_dashboard": {
            "efficiency": data["efficiency"],
            "key_metrics": {
                "hip_angular_momentum": data["metrics"]["hip_angular_momentum"],
                "shoulder_hip_ratio": data["metrics"]["shoulder_hip_ratio"],
                "lead_knee_angle": data["metrics"]["lead_knee_angle"],
                "bat_speed": data["metrics"]["bat_speed"]
            }
        }
    }
    
    return JSONResponse(content=report)


@router.post("/compare")
async def compare_analyses(
    before_id: str = Form(..., description="Before analysis ID"),
    after_id: str = Form(..., description="After analysis ID")
):
    """
    Compare two analyses (before/after training)
    """
    if before_id not in ANALYSIS_RESULTS:
        raise HTTPException(status_code=404, detail=f"Before analysis {before_id} not found")
    
    if after_id not in ANALYSIS_RESULTS:
        raise HTTPException(status_code=404, detail=f"After analysis {after_id} not found")
    
    before = ANALYSIS_RESULTS[before_id]
    after = ANALYSIS_RESULTS[after_id]
    
    # Calculate changes
    comparison = {
        "athlete": before["athlete"]["name"],
        "before": {
            "date": before["created_at"],
            "pattern": before["pattern"]["pattern"],
            "severity": before["pattern"]["severity"],
            "overall_score": before["overall_score"]
        },
        "after": {
            "date": after["created_at"],
            "pattern": after["pattern"]["pattern"],
            "severity": after["pattern"]["severity"],
            "overall_score": after["overall_score"]
        },
        "changes": {
            "overall_score": round(after["overall_score"] - before["overall_score"], 1),
            "exit_velo": round(
                after["ball_outcomes"]["current"]["exit_velo"] - 
                before["ball_outcomes"]["current"]["exit_velo"], 
                1
            ),
            "launch_angle": round(
                after["ball_outcomes"]["current"]["launch_angle"] - 
                before["ball_outcomes"]["current"]["launch_angle"], 
                1
            ),
            "hip_efficiency": round(
                after["efficiency"]["hip_efficiency"] - 
                before["efficiency"]["hip_efficiency"], 
                1
            ),
            "pattern_improved": after["pattern"]["severity"] != "CRITICAL" and before["pattern"]["severity"] == "CRITICAL"
        },
        "metrics_comparison": {
            "before": {
                "hip_angular_momentum": before["metrics"]["hip_angular_momentum"],
                "lead_knee_angle": before["metrics"]["lead_knee_angle"],
                "bat_speed": before["metrics"]["bat_speed"]
            },
            "after": {
                "hip_angular_momentum": after["metrics"]["hip_angular_momentum"],
                "lead_knee_angle": after["metrics"]["lead_knee_angle"],
                "bat_speed": after["metrics"]["bat_speed"]
            }
        }
    }
    
    return JSONResponse(content=comparison)


@router.get("/protocols")
async def list_protocols():
    """
    List all available training protocols
    """
    from .protocols import PROTOCOLS
    
    protocols_summary = {}
    for key, protocol in PROTOCOLS.items():
        protocols_summary[key] = {
            "name": protocol["name"],
            "indication": protocol["indication"],
            "timeline": protocol["timeline"],
            "total_weeks": len(protocol["weeks"]),
            "primary_focus": protocol["weeks"][0]["focus"] if protocol["weeks"] else "N/A"
        }
    
    return JSONResponse(content={"protocols": protocols_summary})


@router.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "service": "Swing DNA API",
        "version": "1.0.0",
        "endpoints": [
            "POST /api/swing-dna/analyze",
            "GET /api/swing-dna/analysis/{id}",
            "GET /api/swing-dna/analysis/{id}/report",
            "POST /api/swing-dna/compare",
            "GET /api/swing-dna/protocols"
        ]
    }


# Testing endpoint (development only)
@router.post("/test")
async def test_with_eric_williams():
    """
    Test endpoint using Eric Williams reference data
    (Development/testing only - remove in production)
    """
    try:
        # Load Eric Williams test data
        import os
        test_data_path = os.path.join(os.path.dirname(__file__), "..", "eric_williams_expected_output.json")
        
        if not os.path.exists(test_data_path):
            raise HTTPException(
                status_code=404,
                detail="Eric Williams test data not found"
            )
        
        import json
        with open(test_data_path, 'r') as f:
            expected = json.load(f)
        
        return JSONResponse(content={
            "message": "Test data loaded successfully",
            "expected_output": expected
        })
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Test failed: {str(e)}"
        )


# Export router
__all__ = ["router"]
