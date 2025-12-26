"""
PRIORITY 12: TEST SERVER (Standalone)
Simple FastAPI server for testing Priority 12 UI without database dependencies
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import sys
from pathlib import Path

# Add physics_engine to path
sys.path.insert(0, str(Path(__file__).parent / "physics_engine"))

from priority_12_api_enhancement import enhance_analysis_with_priority_10_11

# Initialize FastAPI app
app = FastAPI(
    title="Priority 12 Test Server",
    description="Testing Priority 10 + 11 Enhanced Analysis UI",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Root endpoint
@app.get("/")
def read_root():
    """Serve the enhanced analysis UI"""
    return FileResponse("templates/enhanced_analysis.html")


# Request model
class EnhancedAnalysisRequest(BaseModel):
    """Request model for enhanced analysis with Priority 10 + 11"""
    # Scores
    ground_score: int
    engine_score: int
    weapon_score: int
    
    # Athlete data
    height_inches: float
    wingspan_inches: Optional[float] = None
    weight_lbs: float
    age: int
    bat_weight_oz: int = 30
    
    # Optional actual data
    actual_bat_speed_mph: Optional[float] = None
    rotation_ke_joules: Optional[float] = None
    translation_ke_joules: Optional[float] = None


@app.post("/analyze/enhanced")
def enhanced_analysis(request: EnhancedAnalysisRequest):
    """
    Enhanced analysis with Priority 9 + 10 + 11
    
    This endpoint combines:
    - Priority 9: Kinetic Capacity Framework
    - Priority 10: Swing Rehab Recommendation Engine
    - Priority 11: BioSwing Motor-Preference System
    
    Returns comprehensive analysis including:
    - Motor preference detection (SPINNER/GLIDER/LAUNCHER)
    - Adjusted scores (motor-aware scoring)
    - Kinetic capacity (bat speed potential)
    - Gap analysis (actual vs potential)
    - Energy leak identification
    - Personalized correction plan (drills, strength work, timeline)
    """
    try:
        result = enhance_analysis_with_priority_10_11(
            ground_score=request.ground_score,
            engine_score=request.engine_score,
            weapon_score=request.weapon_score,
            height_inches=request.height_inches,
            wingspan_inches=request.wingspan_inches,
            weight_lbs=request.weight_lbs,
            age=request.age,
            bat_weight_oz=request.bat_weight_oz,
            actual_bat_speed_mph=request.actual_bat_speed_mph,
            rotation_ke_joules=request.rotation_ke_joules,
            translation_ke_joules=request.translation_ke_joules
        )
        
        return {
            "status": "success",
            "data": result
        }
    except Exception as e:
        import traceback
        print(f"Error in enhanced analysis: {e}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Analysis error: {str(e)}")


# Health check
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Priority 12 Test Server"
    }


if __name__ == "__main__":
    import uvicorn
    print("=" * 80)
    print("PRIORITY 12 TEST SERVER")
    print("=" * 80)
    print("Starting server on http://0.0.0.0:8001")
    print("Open: http://localhost:8001")
    print("=" * 80)
    uvicorn.run(app, host="0.0.0.0", port=8001)
