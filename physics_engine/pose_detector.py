"""
Pose Detector Module
Uses MediaPipe PoseLandmarker (new API) to extract 33 body landmarks from video frames

MediaPipe Pose Landmarks (33 joints):
0: nose, 1-2: eyes, 3-4: ears, 5-6: shoulders, 7-8: elbows, 9-10: wrists
11-12: hips, 13-14: knees, 15-16: ankles, 17-22: hands, 23-28: feet
"""

import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
import urllib.request
import os


@dataclass
class PoseLandmark:
    """Single pose landmark (joint) with 3D coordinates"""
    x: float  # Normalized x coordinate (0-1)
    y: float  # Normalized y coordinate (0-1)
    z: float  # Depth (relative to hips, in image scale)
    visibility: float  # Confidence score (0-1)


@dataclass
class PoseFrame:
    """Pose data for a single frame"""
    frame_number: int
    timestamp_ms: float
    landmarks: Dict[str, PoseLandmark]  # Joint name → landmark
    is_valid: bool  # Whether pose was detected


class PoseDetector:
    """
    Detect human pose using MediaPipe PoseLandmarker
    
    Returns 33 body landmarks per frame with confidence scores
    """
    
    # MediaPipe landmark indices
    LANDMARK_NAMES = {
        0: 'nose',
        1: 'left_eye_inner', 2: 'left_eye', 3: 'left_eye_outer',
        4: 'right_eye_inner', 5: 'right_eye', 6: 'right_eye_outer',
        7: 'left_ear', 8: 'right_ear',
        9: 'mouth_left', 10: 'mouth_right',
        11: 'left_shoulder', 12: 'right_shoulder',
        13: 'left_elbow', 14: 'right_elbow',
        15: 'left_wrist', 16: 'right_wrist',
        17: 'left_pinky', 18: 'right_pinky',
        19: 'left_index', 20: 'right_index',
        21: 'left_thumb', 22: 'right_thumb',
        23: 'left_hip', 24: 'right_hip',
        25: 'left_knee', 26: 'right_knee',
        27: 'left_ankle', 28: 'right_ankle',
        29: 'left_heel', 30: 'right_heel',
        31: 'left_foot_index', 32: 'right_foot_index'
    }
    
    def __init__(self, min_detection_confidence: float = 0.5,
                 min_tracking_confidence: float = 0.5):
        """
        Initialize MediaPipe pose detector
        
        Args:
            min_detection_confidence: Minimum confidence for detection (0-1)
            min_tracking_confidence: Minimum confidence for tracking (0-1)
        """
        # Download model if needed
        model_path = self._ensure_model()
        
        # Create PoseLandmarker
        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.PoseLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.VIDEO,
            min_pose_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
        self.detector = vision.PoseLandmarker.create_from_options(options)
    
    def _ensure_model(self) -> str:
        """Download pose landmarker model if not present"""
        model_dir = "/tmp/mediapipe_models"
        os.makedirs(model_dir, exist_ok=True)
        model_path = os.path.join(model_dir, "pose_landmarker_heavy.task")
        
        if not os.path.exists(model_path):
            print("Downloading MediaPipe pose landmarker model...")
            url = "https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_heavy/float16/latest/pose_landmarker_heavy.task"
            urllib.request.urlretrieve(url, model_path)
            print(f"✅ Model downloaded to {model_path}")
        
        return model_path
    
    def process_frame(self, frame: np.ndarray, frame_number: int, 
                     timestamp_ms: float) -> PoseFrame:
        """
        Process single frame to extract pose landmarks
        
        Args:
            frame: Image frame (BGR format from OpenCV)
            frame_number: Frame index
            timestamp_ms: Timestamp in milliseconds
        
        Returns:
            PoseFrame with landmarks
        """
        # Convert BGR to RGB (MediaPipe uses RGB)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Create MediaPipe Image
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)
        
        # Process with MediaPipe (timestamp must be in milliseconds)
        timestamp_mp = int(timestamp_ms)
        results = self.detector.detect_for_video(mp_image, timestamp_mp)
        
        # Extract landmarks
        landmarks = {}
        is_valid = False
        
        if results.pose_landmarks and len(results.pose_landmarks) > 0:
            is_valid = True
            pose_landmarks = results.pose_landmarks[0]  # First detected person
            
            for idx, landmark in enumerate(pose_landmarks):
                name = self.LANDMARK_NAMES.get(idx, f'landmark_{idx}')
                landmarks[name] = PoseLandmark(
                    x=landmark.x,
                    y=landmark.y,
                    z=landmark.z,
                    visibility=landmark.visibility if hasattr(landmark, 'visibility') else 1.0
                )
        
        return PoseFrame(
            frame_number=frame_number,
            timestamp_ms=timestamp_ms,
            landmarks=landmarks,
            is_valid=is_valid
        )
    
    def get_joint_position_2d(self, pose_frame: PoseFrame, 
                              joint_name: str) -> Optional[Tuple[float, float]]:
        """Get 2D position of a joint (normalized 0-1 coordinates)"""
        if not pose_frame.is_valid:
            return None
        
        landmark = pose_frame.landmarks.get(joint_name)
        if landmark is None:
            return None
        
        return (landmark.x, landmark.y)
    
    def get_joint_position_3d(self, pose_frame: PoseFrame, 
                              joint_name: str) -> Optional[Tuple[float, float, float]]:
        """Get 3D position of a joint"""
        if not pose_frame.is_valid:
            return None
        
        landmark = pose_frame.landmarks.get(joint_name)
        if landmark is None:
            return None
        
        return (landmark.x, landmark.y, landmark.z)
    
    def get_midpoint(self, pose_frame: PoseFrame, 
                     joint1: str, joint2: str) -> Optional[Tuple[float, float, float]]:
        """Calculate midpoint between two joints"""
        pos1 = self.get_joint_position_3d(pose_frame, joint1)
        pos2 = self.get_joint_position_3d(pose_frame, joint2)
        
        if pos1 is None or pos2 is None:
            return None
        
        return (
            (pos1[0] + pos2[0]) / 2,
            (pos1[1] + pos2[1]) / 2,
            (pos1[2] + pos2[2]) / 2
        )
    
    def calculate_angle_2d(self, pose_frame: PoseFrame,
                          joint1: str, joint2: str, joint3: str) -> Optional[float]:
        """Calculate angle between three joints in 2D (degrees)"""
        p1 = self.get_joint_position_2d(pose_frame, joint1)
        p2 = self.get_joint_position_2d(pose_frame, joint2)
        p3 = self.get_joint_position_2d(pose_frame, joint3)
        
        if None in (p1, p2, p3):
            return None
        
        # Vectors from vertex (p2) to other points
        v1 = np.array([p1[0] - p2[0], p1[1] - p2[1]])
        v2 = np.array([p3[0] - p2[0], p3[1] - p2[1]])
        
        # Calculate angle using dot product
        cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2) + 1e-6)
        cos_angle = np.clip(cos_angle, -1.0, 1.0)
        angle_rad = np.arccos(cos_angle)
        angle_deg = np.degrees(angle_rad)
        
        return angle_deg
    
    def close(self):
        """Clean up MediaPipe resources"""
        self.detector.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


if __name__ == "__main__":
    print("\n" + "="*80)
    print("MEDIAPIPE POSE DETECTOR TEST")
    print("="*80)
    
    from video_processor import VideoProcessor
    
    test_video = "/home/user/uploaded_files/131215-Hitting.mov"
    
    print(f"\nTesting on: {test_video}")
    print("Processing first 10 frames...\n")
    
    try:
        with VideoProcessor(test_video) as vp, PoseDetector() as pd:
            # Process first 10 frames
            for i in range(min(10, vp.metadata.total_frames)):
                success, frame = vp.get_frame(i)
                if not success:
                    break
                
                timestamp_ms = vp.frame_number_to_time_ms(i)
                pose_frame = pd.process_frame(frame, i, timestamp_ms)
                
                if pose_frame.is_valid:
                    # Get key joint positions
                    left_shoulder = pd.get_joint_position_2d(pose_frame, 'left_shoulder')
                    right_shoulder = pd.get_joint_position_2d(pose_frame, 'right_shoulder')
                    
                    print(f"Frame {i} ({timestamp_ms:.0f}ms): ✅ Pose detected")
                    print(f"  Left Shoulder: ({left_shoulder[0]:.3f}, {left_shoulder[1]:.3f})")
                    print(f"  Right Shoulder: ({right_shoulder[0]:.3f}, {right_shoulder[1]:.3f})")
                    print(f"  Total landmarks: {len(pose_frame.landmarks)}")
                else:
                    print(f"Frame {i} ({timestamp_ms:.0f}ms): ❌ No pose detected")
                
                print()
        
        print("="*80)
        print("✅ MediaPipe pose detection working!")
        print("="*80)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
