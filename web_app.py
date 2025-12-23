"""
KINETIC DNA BLUEPRINT - Web Interface
Simple upload and analysis interface for testing
"""

from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import shutil
from pathlib import Path
import sys
import cv2

# Add physics_engine to path
sys.path.insert(0, str(Path(__file__).parent / "physics_engine"))

from anthropometry import AnthropometricModel
from video_processor import VideoProcessor
from pose_detector import PoseDetector
from physics_calculator import PhysicsCalculator
from event_detection_v2 import EventDetector  # V2: TypeScript-based proven logic
from scoring_engine import ScoringEngine

app = FastAPI(title="Kinetic DNA Blueprint - Demo")

# Create directories
UPLOAD_DIR = Path("/home/user/webapp/uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

TEMPLATES_DIR = Path("/home/user/webapp/templates")
TEMPLATES_DIR.mkdir(exist_ok=True)

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page with upload form"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/analyze")
async def analyze_video(
    video: UploadFile = File(...),
    name: str = Form(...),
    height_inches: float = Form(...),
    weight_lbs: float = Form(...),
    wingspan_inches: float = Form(None),
    bat_side: str = Form(...),
    age: int = Form(16)
):
    """
    Process uploaded video and return biomechanics analysis
    """
    
    # Save uploaded file
    video_path = UPLOAD_DIR / video.filename
    with open(video_path, "wb") as buffer:
        shutil.copyfileobj(video.file, buffer)
    
    try:
        # 1. Create anthropometric model
        anthro = AnthropometricModel(
            height_inches=height_inches,
            weight_lbs=weight_lbs,
            age=age,
            wingspan_inches=wingspan_inches
        )
        
        # 2. Get video metadata
        video_proc = VideoProcessor(str(video_path))
        metadata = video_proc.metadata
        
        # 3. Extract poses from video
        pose_detector = PoseDetector()
        physics_calc = PhysicsCalculator()
        
        cap = cv2.VideoCapture(str(video_path))
        frame_count = 0
        pose_frames = []  # Store PoseFrame objects
        
        # Optimize: Process every 2nd frame for 30 FPS, every 5th for higher FPS
        frame_skip = 2 if metadata.fps <= 60 else 5
        max_frames = 500  # Limit total frames processed
        
        while cap.isOpened() and frame_count < max_frames * frame_skip:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Only process every Nth frame
            if frame_count % frame_skip == 0:
                timestamp_ms = video_proc.frame_number_to_time_ms(frame_count)
                pose_frame = pose_detector.process_frame(frame, frame_count, timestamp_ms)
                
                if pose_frame.is_valid:
                    pose_frames.append(pose_frame)
            
            frame_count += 1
        
        cap.release()
        
        # 4. Calculate physics
        angles = [physics_calc.extract_joint_angles(pf) for pf in pose_frames]
        angles = [a for a in angles if a is not None]  # Filter invalid
        
        if len(angles) < 10:
            raise ValueError("Not enough valid poses detected. Need at least 10 frames with full body visible.")
        
        # Calculate velocities (use athlete height for scaling)
        scale_factor = anthro.height_m
        velocities = physics_calc.calculate_velocities(angles, pose_frames, scale_factor)
        
        if len(velocities) < 5:
            raise ValueError("Not enough velocity data. Video may be too short.")
        
        # 5. Detect swing events
        event_detector = EventDetector(debug=True)  # Enable debug mode
        events = event_detector.detect_all_events(angles, velocities)
        
        if not events:
            raise ValueError("Could not detect swing window. Video may not contain a clear swing or have insufficient motion data.")
        
        # 6. Find kinetic sequence
        kinetic_seq = physics_calc.find_kinetic_sequence(velocities)
        
        # 7. Calculate scores
        scoring_engine = ScoringEngine()
        scores = scoring_engine.calculate_all_scores(velocities, events, kinetic_seq, weight_lbs)
        
        # 8. Build response
        response = {
            "status": "success",
            "athlete": {
                "name": name,
                "bat_side": bat_side,
                "age": age
            },
            "anthropometrics": anthro.get_summary(),
            "video": {
                "filename": video.filename,
                "width": metadata.width,
                "height": metadata.height,
                "recorded_fps": metadata.fps,
                "frame_time_ms": metadata.frame_time_ms,
                "duration_seconds": metadata.duration_sec,
                "total_frames": frame_count,
                "frames_analyzed": len(pose_frames)
            },
            "pose_detection": {
                "frames_processed": len(pose_frames),
                "detection_rate": f"{(len(pose_frames) / frame_count * 100):.1f}%"
            },
            "swing_events": event_detector.get_event_summary(events),
            "kinetic_sequence": {
                "pelvis_peak_ms": round(kinetic_seq.pelvis_peak_time_ms, 1),
                "torso_peak_ms": round(kinetic_seq.torso_peak_time_ms, 1),
                "shoulder_peak_ms": round(kinetic_seq.shoulder_peak_time_ms, 1),
                "hand_peak_ms": round(kinetic_seq.hand_peak_time_ms, 1),
                "bat_peak_ms": round(kinetic_seq.bat_peak_time_ms, 1),
                "sequence_quality_score": round(kinetic_seq.get_sequence_quality(), 0)
            },
            "scores": scores.to_dict(),
            "interpretation": {
                "tempo_ratio": get_tempo_interpretation(scores.tempo_ratio),
                "ground_score": get_score_interpretation(scores.ground_score),
                "engine_score": get_score_interpretation(scores.engine_score),
                "weapon_score": get_score_interpretation(scores.weapon_score),
                "transfer_ratio": get_transfer_interpretation(scores.transfer_ratio),
                "motor_profile": f"Your swing pattern is {scores.motor_profile}"
            }
        }
        
        return JSONResponse(content=response)
        
    except Exception as e:
        import traceback
        return JSONResponse(
            content={
                "status": "error",
                "message": str(e),
                "traceback": traceback.format_exc()
            },
            status_code=500
        )
    
    finally:
        # Cleanup uploaded file
        if video_path.exists():
            video_path.unlink()


def get_tempo_interpretation(tempo_ratio: float) -> str:
    """Interpret tempo ratio"""
    if tempo_ratio >= 3.5:
        return "Excellent - Elite timing pattern"
    elif tempo_ratio >= 2.5:
        return "Good - Strong timing control"
    elif tempo_ratio >= 2.0:
        return "Developing - Work on loading longer"
    else:
        return "Needs work - Load phase too short"


def get_score_interpretation(score: int) -> str:
    """Interpret 0-100 score"""
    if score >= 80:
        return "Elite level"
    elif score >= 70:
        return "Advanced"
    elif score >= 60:
        return "Above average"
    elif score >= 50:
        return "Average"
    else:
        return "Developing"


def get_transfer_interpretation(transfer_pct: int) -> str:
    """Interpret transfer ratio percentage"""
    if transfer_pct >= 85:
        return "Elite - Excellent energy transfer"
    elif transfer_pct >= 75:
        return "Strong - Solid kinetic chain"
    elif transfer_pct >= 65:
        return "Good - Room for improvement"
    elif transfer_pct >= 55:
        return "Developing - Energy leaks present"
    else:
        return "Focus area - Significant energy loss"


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "service": "Kinetic DNA Blueprint Web Interface"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
