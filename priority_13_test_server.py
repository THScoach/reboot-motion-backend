"""
PRIORITY 13: VIDEO-ENHANCED TEST SERVER
========================================

Test server with video library integration
Extends Priority 12 with video recommendations
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

from priority_13_video_enhanced_analysis import enhance_analysis_with_videos
from video_library_routes import router as video_router

# Initialize FastAPI app
app = FastAPI(
    title="Priority 13 Test Server - Video-Enhanced Analysis",
    description="Testing Priority 10 + 11 + 13 (Video Library Integration)",
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

# Include video library routes
app.include_router(video_router)


# Root endpoint
@app.get("/")
def read_root():
    """Serve the enhanced analysis UI"""
    return FileResponse("templates/enhanced_analysis.html")


# Request model
class EnhancedAnalysisRequest(BaseModel):
    """Request model for enhanced analysis with Priority 10 + 11 + 13"""
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
    
    # Video options
    include_videos: bool = True
    max_videos_per_drill: int = 3


@app.post("/analyze/enhanced")
def enhanced_analysis(request: EnhancedAnalysisRequest):
    """
    Enhanced analysis with Priority 9 + 10 + 11 + 13 (VIDEO LIBRARY)
    
    This endpoint combines:
    - Priority 9: Kinetic Capacity Framework
    - Priority 10: Swing Rehab Recommendation Engine
    - Priority 11: BioSwing Motor-Preference System
    - Priority 13: Video Library Integration ⭐ NEW
    
    Returns comprehensive analysis including:
    - Motor preference detection (SPINNER/GLIDER/LAUNCHER)
    - Adjusted scores (motor-aware scoring)
    - Kinetic capacity (bat speed potential)
    - Gap analysis (actual vs potential)
    - Energy leak identification
    - Personalized correction plan (drills, strength work, timeline)
    - Video demonstrations for each drill ⭐ NEW
    - Featured educational videos ⭐ NEW
    - Motor-preference specific videos ⭐ NEW
    """
    try:
        result = enhance_analysis_with_videos(
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
            translation_ke_joules=request.translation_ke_joules,
            include_videos=request.include_videos,
            max_videos_per_drill=request.max_videos_per_drill
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
        "service": "Priority 13 Video-Enhanced Test Server",
        "features": [
            "Priority 9: Kinetic Capacity",
            "Priority 10: Recommendation Engine",
            "Priority 11: Motor Preference",
            "Priority 13: Video Library"
        ]
    }


if __name__ == "__main__":
    import uvicorn
    print("=" * 80)
    print("PRIORITY 13 VIDEO-ENHANCED TEST SERVER")
    print("=" * 80)
    print("Starting server on http://0.0.0.0:8002")
    print("Open: http://localhost:8002")
    print("")
    print("Features:")
    print("  ✅ Motor Preference Detection (Priority 11)")
    print("  ✅ Adjusted Scoring (Priority 11)")
    print("  ✅ Kinetic Capacity (Priority 9)")
    print("  ✅ Recommendation Engine (Priority 10)")
    print("  ✅ Video Library Integration (Priority 13) ⭐ NEW")
    print("")
    print("Video API Endpoints:")
    print("  - GET  /videos (all videos)")
    print("  - GET  /videos/featured")
    print("  - GET  /videos/search?q=hip")
    print("  - GET  /videos/for-drill/{drill_id}")
    print("  - GET  /videos/{video_id}")
    print("=" * 80)
    uvicorn.run(app, host="0.0.0.0", port=8002)
