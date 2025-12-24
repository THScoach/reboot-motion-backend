"""
Reboot Lite API Routes
Endpoints for Reboot Lite analysis features

Author: Builder 2 (Backend & Database AI)
Date: 2024-12-24
"""

from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Depends
from sqlalchemy.orm import Session
from typing import Optional, List, Dict
from datetime import datetime
import logging
import os
import tempfile

# Import database
from database import get_db
from models import Player, Session as SessionModel, BiomechanicsData

# Import physics engine components
from physics_engine.video_processor import VideoProcessor
from physics_engine.pose_detector import PoseDetector
from physics_engine.event_detection_v2 import KineticChainAnalyzer
from physics_engine.physics_calculator import PhysicsCalculator
from physics_engine.kinetic_capacity_calculator import calculate_energy_capacity
from physics_engine.scoring_engine import ScoringEngine
from physics_engine.motor_profile_classifier import MotorProfileClassifier

# Import new Reboot Lite components
from physics_engine.tempo_calculator import calculate_tempo_score, calculate_tempo_from_events
from physics_engine.stability_calculator import calculate_stability_score, analyze_stability_from_pose_frames
from physics_engine.race_bar_formatter import format_kinetic_sequence_for_race_bar

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/reboot-lite", tags=["Reboot Lite"])


@router.post("/analyze-swing")
async def analyze_swing_reboot_lite(
    video: UploadFile = File(...),
    player_id: int = Form(...),
    height_inches: int = Form(...),
    weight_lbs: int = Form(...),
    age: int = Form(...),
    wingspan_inches: Optional[int] = Form(None),
    bat_weight_oz: Optional[int] = Form(33),
    db: Session = Depends(get_db)
):
    """
    Complete Reboot Lite analysis for a single swing
    
    Combines ALL analysis components:
    1. V2.0.2 Kinetic Capacity Prediction
    2. Race Bar (Kinematic Sequence)
    3. Tempo Score
    4. Stability Score
    5. Motor Profile
    6. GEW Scores
    7. Training Recommendations
    
    Args:
        video: Video file (uploaded)
        player_id: Player database ID
        height_inches: Player height
        weight_lbs: Player weight
        age: Player age
        wingspan_inches: Player wingspan (optional)
        bat_weight_oz: Bat weight in ounces (default 33)
        db: Database session
    
    Returns:
        Complete Reboot Lite analysis JSON
    """
    try:
        logger.info(f"Starting Reboot Lite analysis for player {player_id}")
        
        # Save uploaded video temporarily
        temp_dir = tempfile.mkdtemp()
        video_path = os.path.join(temp_dir, video.filename)
        
        with open(video_path, "wb") as f:
            content = await video.read()
            f.write(content)
        
        logger.info(f"Video saved: {video_path} ({len(content)} bytes)")
        
        # ============================================================
        # STEP 1: Video Processing & Pose Detection
        # ============================================================
        logger.info("Step 1: Processing video and detecting pose...")
        
        video_processor = VideoProcessor(video_path)
        pose_detector = PoseDetector()
        
        # Extract pose data from video
        pose_frames = []
        frame_count = 0
        
        for frame_number in range(video_processor.metadata.total_frames):
            success, frame = video_processor.get_frame(frame_number)
            if not success:
                continue
            
            timestamp_ms = frame_number * video_processor.metadata.frame_time_ms
            pose_frame = pose_detector.detect_pose(frame, timestamp_ms)
            pose_frames.append(pose_frame)
            frame_count += 1
            
            # Log progress every 30 frames
            if frame_count % 30 == 0:
                logger.info(f"  Processed {frame_count}/{video_processor.metadata.total_frames} frames")
        
        logger.info(f"✅ Pose detection complete: {len(pose_frames)} frames analyzed")
        
        # ============================================================
        # STEP 2: Event Detection (Kinetic Chain Analysis)
        # ============================================================
        logger.info("Step 2: Analyzing kinetic chain events...")
        
        event_analyzer = KineticChainAnalyzer()
        events = event_analyzer.analyze(pose_frames)
        
        logger.info(f"✅ Events detected: {events}")
        
        # ============================================================
        # STEP 3: Physics Calculations
        # ============================================================
        logger.info("Step 3: Calculating physics metrics...")
        
        physics_calculator = PhysicsCalculator()
        physics_metrics = physics_calculator.calculate_all(pose_frames, events)
        
        logger.info(f"✅ Physics calculated: bat speed = {physics_metrics.get('bat_speed', 0):.1f} mph")
        
        # ============================================================
        # STEP 4: Kinetic Capacity Prediction (V2.0.2)
        # ============================================================
        logger.info("Step 4: Calculating kinetic capacity...")
        
        # Use wingspan if provided, otherwise estimate from height
        wingspan = wingspan_inches if wingspan_inches else height_inches + 2
        
        capacity_result = calculate_energy_capacity(
            height_inches=height_inches,
            weight_lbs=weight_lbs,
            age=age,
            wingspan_inches=wingspan,
            bat_weight_oz=bat_weight_oz
        )
        
        predicted_bat_speed = capacity_result['bat_speed_capacity_mph']
        logger.info(f"✅ Predicted capacity: {predicted_bat_speed:.1f} mph")
        
        # ============================================================
        # STEP 5: GEW Scoring
        # ============================================================
        logger.info("Step 5: Calculating GEW scores...")
        
        scoring_engine = ScoringEngine()
        gew_scores = scoring_engine.score_swing(physics_metrics)
        
        logger.info(f"✅ GEW scores: G={gew_scores.get('ground', 0)}, E={gew_scores.get('engine', 0)}, W={gew_scores.get('weapon', 0)}")
        
        # ============================================================
        # STEP 6: Motor Profile Classification
        # ============================================================
        logger.info("Step 6: Classifying motor profile...")
        
        motor_classifier = MotorProfileClassifier()
        motor_profile = motor_classifier.classify(physics_metrics, gew_scores)
        
        logger.info(f"✅ Motor profile: {motor_profile}")
        
        # ============================================================
        # STEP 7: Race Bar (Kinematic Sequence)
        # ============================================================
        logger.info("Step 7: Formatting race bar...")
        
        race_bar = format_kinetic_sequence_for_race_bar(events)
        
        logger.info(f"✅ Race bar: grade={race_bar['sequence_grade']}, efficiency={race_bar['energy_transfer']}%")
        
        # ============================================================
        # STEP 8: Tempo Score
        # ============================================================
        logger.info("Step 8: Calculating tempo score...")
        
        tempo_score = calculate_tempo_from_events(events)
        
        logger.info(f"✅ Tempo: {tempo_score['category']} (ratio={tempo_score['ratio']})")
        
        # ============================================================
        # STEP 9: Stability Score
        # ============================================================
        logger.info("Step 9: Calculating stability score...")
        
        # Convert pose frames to dict format for stability calculator
        pose_frames_dict = [
            {
                'frame_number': pf.frame_number,
                'timestamp_ms': pf.timestamp_ms,
                'landmarks': {
                    name: {
                        'x': lm.x,
                        'y': lm.y,
                        'z': lm.z,
                        'visibility': lm.visibility
                    }
                    for name, lm in pf.landmarks.items()
                },
                'is_valid': pf.is_valid
            }
            for pf in pose_frames
        ]
        
        stability_score = analyze_stability_from_pose_frames(
            pose_frames_dict,
            player_height_inches=height_inches
        )
        
        logger.info(f"✅ Stability: grade={stability_score['grade']}, score={stability_score['stability_score']}")
        
        # ============================================================
        # STEP 10: Assemble Complete Response
        # ============================================================
        logger.info("Step 10: Assembling final response...")
        
        response = {
            'session_id': f"rl_{player_id}_{int(datetime.now().timestamp())}",
            'player_id': player_id,
            'timestamp': datetime.now().isoformat(),
            'video_metadata': {
                'filename': video.filename,
                'fps': video_processor.metadata.fps,
                'duration_sec': video_processor.metadata.duration_sec,
                'total_frames': video_processor.metadata.total_frames,
                'frames_analyzed': len(pose_frames)
            },
            'analysis': {
                # Core Metrics
                'bat_speed_mph': physics_metrics.get('bat_speed', 0),
                'bat_speed_capacity_mph': predicted_bat_speed,
                'bat_speed_efficiency_pct': (physics_metrics.get('bat_speed', 0) / predicted_bat_speed * 100) if predicted_bat_speed > 0 else 0,
                'exit_velocity_mph': physics_metrics.get('exit_velo', 0),
                
                # Motor Profile
                'motor_profile': motor_profile,
                
                # GEW Scores
                'scores': {
                    'ground': gew_scores.get('ground', 0),
                    'engine': gew_scores.get('engine', 0),
                    'weapon': gew_scores.get('weapon', 0),
                    'overall': (gew_scores.get('ground', 0) + gew_scores.get('engine', 0) + gew_scores.get('weapon', 0)) / 3
                },
                
                # Race Bar (Kinematic Sequence)
                'race_bar': race_bar,
                
                # Tempo Score
                'tempo': tempo_score,
                
                # Stability Score
                'stability': stability_score,
                
                # Kinetic Chain (raw events)
                'kinetic_chain': {
                    'lower_half_peak_ms': events.get('lower_half_peak_ms', 0),
                    'torso_peak_ms': events.get('torso_peak_ms', 0),
                    'arms_peak_ms': events.get('arms_peak_ms', 0),
                    'tempo_lower_to_torso_ms': events.get('tempo_lower_to_torso', 0),
                    'tempo_torso_to_arms_ms': events.get('tempo_torso_to_arms', 0),
                    'sequence_valid': events.get('sequence_valid', False)
                },
                
                # Energy Metrics
                'energy': {
                    'rotational_ke_joules': physics_metrics.get('rotational_ke', 0),
                    'translational_ke_joules': physics_metrics.get('translational_ke', 0),
                    'total_ke_joules': physics_metrics.get('total_ke', 0),
                    'energy_transfer_efficiency': physics_metrics.get('energy_efficiency', 0)
                },
                
                # Anthropometry
                'anthropometry': {
                    'height_inches': height_inches,
                    'weight_lbs': weight_lbs,
                    'wingspan_inches': wingspan,
                    'age': age,
                    'bat_weight_oz': bat_weight_oz
                }
            }
        }
        
        # Clean up temporary video file
        try:
            os.remove(video_path)
            os.rmdir(temp_dir)
        except:
            pass
        
        logger.info("✅ Reboot Lite analysis complete!")
        
        return response
        
    except Exception as e:
        logger.error(f"❌ Error in Reboot Lite analysis: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.get("/health")
async def health_check():
    """Health check for Reboot Lite API"""
    return {
        "status": "healthy",
        "service": "Reboot Lite API",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }
