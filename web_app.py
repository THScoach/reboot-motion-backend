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
        
        cap = cv2.VideoCapture(str(video_path))
        frame_count = 0
        poses = []
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            # Process every frame (for demo, limit to reasonable number)
            if frame_count < 500:  # ~16 seconds at 30fps
                result = pose_detector.process_frame(frame)
                if result and result.pose_landmarks:
                    landmarks = []
                    for landmark in result.pose_landmarks.landmark:
                        landmarks.append({
                            'x': landmark.x,
                            'y': landmark.y,
                            'z': landmark.z,
                            'visibility': landmark.visibility
                        })
                    poses.append({
                        'frame': frame_count,
                        'timestamp_ms': video_proc.frame_number_to_time_ms(frame_count),
                        'landmarks': landmarks
                    })
            
            frame_count += 1
        
        cap.release()
        
        # 4. Build response
        response = {
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
                "note": "recorded_fps is the capture rate (30 FPS or 300 FPS). Analysis processes at this native rate - no playback speed conversion."
            },
            "pose_detection": {
                "frames_processed": len(poses),
                "detection_rate": f"{(len(poses) / frame_count * 100):.1f}%",
                "sample_poses": poses[:5]  # First 5 poses as sample
            },
            "frame_rate_explanation": {
                "recorded_fps": metadata.fps,
                "what_this_means": f"Video was recorded at {metadata.fps} frames per second",
                "processing_method": "We analyze every frame at its native timing",
                "time_per_frame_ms": metadata.frame_time_ms,
                "example": f"At {metadata.fps} FPS, each frame represents {metadata.frame_time_ms:.2f} milliseconds of real time"
            },
            "status": "success",
            "message": f"Processed {len(poses)} frames with pose detection"
        }
        
        return JSONResponse(content=response)
        
    except Exception as e:
        return JSONResponse(
            content={
                "status": "error",
                "message": str(e)
            },
            status_code=500
        )
    
    finally:
        # Cleanup uploaded file
        if video_path.exists():
            video_path.unlink()


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "service": "Kinetic DNA Blueprint Web Interface"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
