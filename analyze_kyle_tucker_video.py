#!/usr/bin/env python3
"""
Kyle Tucker Single-Camera Video Analysis
Extracts biomechanics from high-speed video (300fps)
Generates KRS-compatible metrics
"""

import cv2
import numpy as np
from dataclasses import dataclass
from typing import List, Tuple, Optional
import json
import urllib.request
import os

@dataclass
class BiomechanicsFrame:
    """Single frame of biomechanics data"""
    frame_num: int
    timestamp_ms: float
    pelvis_angle: float  # degrees
    torso_angle: float   # degrees
    left_hip: Tuple[float, float, float]   # x, y, z
    right_hip: Tuple[float, float, float]
    left_shoulder: Tuple[float, float, float]
    right_shoulder: Tuple[float, float, float]
    bat_detected: bool
    confidence: float

@dataclass
class RotationMetrics:
    """Swing rotation analysis"""
    pelvis_rom: float           # degrees
    torso_rom: float            # degrees
    x_factor: float             # hip-shoulder separation
    pelvis_peak_velocity: float # deg/s
    torso_peak_velocity: float  # deg/s
    sequence_gap_ms: float      # timing between peaks
    load_frame: int
    contact_frame: int
    follow_through_frame: int

class VideoAnalyzer:
    """Analyze baseball swing from single-camera video"""
    
    def __init__(self, video_path: str):
        self.video_path = video_path
        self.cap = cv2.VideoCapture(video_path)
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        # Initialize MediaPipe Pose using tasks API
        import mediapipe as mp
        from mediapipe.tasks import python
        from mediapipe.tasks.python import vision
        
        # Download pose landmarker model
        model_path = '/tmp/pose_landmarker.task'
        if not os.path.exists(model_path):
            print("📥 Downloading MediaPipe Pose model...")
            url = 'https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_heavy/float16/latest/pose_landmarker_heavy.task'
            urllib.request.urlretrieve(url, model_path)
            print("✅ Model downloaded\n")
        
        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.PoseLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.VIDEO,
            min_pose_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.pose_landmarker = vision.PoseLandmarker.create_from_options(options)
        
        # Pose landmark indices (same as old MediaPipe)
        self.LEFT_HIP = 23
        self.RIGHT_HIP = 24
        self.LEFT_SHOULDER = 11
        self.RIGHT_SHOULDER = 12
        
        self.frames_data: List[BiomechanicsFrame] = []
        
    def __del__(self):
        if hasattr(self, 'cap'):
            self.cap.release()
        if hasattr(self, 'pose_landmarker'):
            self.pose_landmarker.close()
    
    def calculate_angle_2d(self, p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
        """Calculate angle in degrees from horizontal (0° = right, 90° = up)"""
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        angle = np.degrees(np.arctan2(dy, dx))
        return angle
    
    def extract_biomechanics(self) -> List[BiomechanicsFrame]:
        """Extract frame-by-frame biomechanics"""
        import mediapipe as mp
        
        print(f"🎥 Processing {self.frame_count} frames at {self.fps} fps...")
        
        frame_num = 0
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break
            
            # Convert to RGB and create MediaPipe Image
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
            
            # Process frame
            timestamp_ms = int(frame_num * 1000 / self.fps)
            results = self.pose_landmarker.detect_for_video(mp_image, timestamp_ms)
            
            if results.pose_landmarks and len(results.pose_landmarks) > 0:
                landmarks = results.pose_landmarks[0]  # First person detected
                
                # Extract joint positions
                left_hip = landmarks[self.LEFT_HIP]
                right_hip = landmarks[self.RIGHT_HIP]
                left_shoulder = landmarks[self.LEFT_SHOULDER]
                right_shoulder = landmarks[self.RIGHT_SHOULDER]
                
                # Calculate pelvis angle (line between hips)
                pelvis_angle = self.calculate_angle_2d(
                    (right_hip.x, right_hip.y),
                    (left_hip.x, left_hip.y)
                )
                
                # Calculate torso angle (line between shoulders)
                torso_angle = self.calculate_angle_2d(
                    (right_shoulder.x, right_shoulder.y),
                    (left_shoulder.x, left_shoulder.y)
                )
                
                # Calculate confidence (average visibility)
                confidence = np.mean([
                    left_hip.visibility,
                    right_hip.visibility,
                    left_shoulder.visibility,
                    right_shoulder.visibility
                ])
                
                frame_data = BiomechanicsFrame(
                    frame_num=frame_num,
                    timestamp_ms=frame_num * 1000.0 / self.fps,
                    pelvis_angle=pelvis_angle,
                    torso_angle=torso_angle,
                    left_hip=(left_hip.x, left_hip.y, left_hip.z),
                    right_hip=(right_hip.x, right_hip.y, right_hip.z),
                    left_shoulder=(left_shoulder.x, left_shoulder.y, left_shoulder.z),
                    right_shoulder=(right_shoulder.x, right_shoulder.y, right_shoulder.z),
                    bat_detected=False,  # TODO: Add bat tracking
                    confidence=confidence
                )
                
                self.frames_data.append(frame_data)
            
            frame_num += 1
            if frame_num % 100 == 0:
                print(f"  Processed {frame_num}/{self.frame_count} frames...")
        
        print(f"✅ Extracted {len(self.frames_data)} frames with pose data\n")
        return self.frames_data
    
    def detect_swing_events(self) -> Tuple[int, int, int]:
        """Detect load, contact, and follow-through frames"""
        if len(self.frames_data) < 10:
            return 0, len(self.frames_data) // 2, len(self.frames_data) - 1
        
        # Get pelvis angles
        pelvis_angles = [f.pelvis_angle for f in self.frames_data]
        
        # Smooth the signal
        window = 5
        smoothed = np.convolve(pelvis_angles, np.ones(window)/window, mode='same')
        
        # Find minimum (load position - hip rotated back)
        load_frame = np.argmin(smoothed[:len(smoothed)//2])
        
        # Find maximum (follow-through - hip rotated forward)
        follow_through_frame = np.argmax(smoothed[len(smoothed)//2:]) + len(smoothed)//2
        
        # Contact is approximately 2/3 of the way from load to follow-through
        contact_frame = int(load_frame + 0.67 * (follow_through_frame - load_frame))
        
        print(f"📍 Event Detection:")
        print(f"   Load Frame: {load_frame} ({load_frame * 1000 / self.fps:.1f}ms)")
        print(f"   Contact Frame: {contact_frame} ({contact_frame * 1000 / self.fps:.1f}ms)")
        print(f"   Follow-Through Frame: {follow_through_frame} ({follow_through_frame * 1000 / self.fps:.1f}ms)")
        print(f"   Swing Duration: {(follow_through_frame - load_frame) * 1000 / self.fps:.1f}ms\n")
        
        return load_frame, contact_frame, follow_through_frame
    
    def calculate_rotation_metrics(self) -> RotationMetrics:
        """Calculate rotation ROM and kinematic sequence"""
        
        load_frame, contact_frame, follow_through_frame = self.detect_swing_events()
        
        # Extract swing portion only (load to follow-through)
        swing_frames = self.frames_data[load_frame:follow_through_frame+1]
        
        if len(swing_frames) < 5:
            print("⚠️  Warning: Insufficient swing frames detected")
            return RotationMetrics(0, 0, 0, 0, 0, 0, 0, 0, 0)
        
        # Get angles during swing
        pelvis_angles = [f.pelvis_angle for f in swing_frames]
        torso_angles = [f.torso_angle for f in swing_frames]
        
        # Calculate ROM (Range of Motion)
        pelvis_rom = max(pelvis_angles) - min(pelvis_angles)
        torso_rom = max(torso_angles) - min(torso_angles)
        
        # Calculate peak velocities (degrees per second)
        dt = 1.0 / self.fps
        pelvis_velocities = np.diff(pelvis_angles) / dt
        torso_velocities = np.diff(torso_angles) / dt
        
        pelvis_peak_velocity = np.max(np.abs(pelvis_velocities))
        torso_peak_velocity = np.max(np.abs(torso_velocities))
        
        # Find timing of peaks
        pelvis_peak_frame = np.argmax(np.abs(pelvis_velocities))
        torso_peak_frame = np.argmax(np.abs(torso_velocities))
        sequence_gap_ms = abs(torso_peak_frame - pelvis_peak_frame) * 1000.0 / self.fps
        
        # Calculate X-factor (hip-shoulder separation) at load
        load_pelvis = swing_frames[0].pelvis_angle
        load_torso = swing_frames[0].torso_angle
        x_factor = abs(load_torso - load_pelvis)
        
        print(f"🔄 Rotation Metrics:")
        print(f"   Pelvis ROM: {pelvis_rom:.1f}°")
        print(f"   Torso ROM: {torso_rom:.1f}°")
        print(f"   X-Factor (Separation): {x_factor:.1f}°")
        print(f"   Pelvis Peak Velocity: {pelvis_peak_velocity:.0f}°/s")
        print(f"   Torso Peak Velocity: {torso_peak_velocity:.0f}°/s")
        print(f"   Kinematic Sequence Gap: {sequence_gap_ms:.1f}ms")
        
        # Check if sequence is correct (pelvis before torso)
        sequence_correct = pelvis_peak_frame < torso_peak_frame
        print(f"   Sequence Order: {'✅ CORRECT (Pelvis → Torso)' if sequence_correct else '❌ REVERSE (Torso → Pelvis)'}\n")
        
        return RotationMetrics(
            pelvis_rom=pelvis_rom,
            torso_rom=torso_rom,
            x_factor=x_factor,
            pelvis_peak_velocity=pelvis_peak_velocity,
            torso_peak_velocity=torso_peak_velocity,
            sequence_gap_ms=sequence_gap_ms,
            load_frame=load_frame,
            contact_frame=contact_frame,
            follow_through_frame=follow_through_frame
        )
    
    def export_to_reboot_format(self, metrics: RotationMetrics, athlete_name: str) -> dict:
        """Export in Reboot Motion report format for KRS system"""
        
        return {
            "session_id": "kyle_tucker_video_001",
            "athlete_name": athlete_name,
            "date": "2025-12-27",
            "video_fps": float(self.fps),
            "video_frames": int(self.frame_count),
            "rotation_metrics": {
                "pelvis_rotation_rom_deg": round(float(metrics.pelvis_rom), 1),
                "torso_rotation_rom_deg": round(float(metrics.torso_rom), 1),
                "x_factor_deg": round(float(metrics.x_factor), 1),
            },
            "kinematic_sequence": {
                "pelvis_peak_velocity_deg_per_s": round(float(metrics.pelvis_peak_velocity), 0),
                "torso_peak_velocity_deg_per_s": round(float(metrics.torso_peak_velocity), 0),
                "sequence_gap_ms": round(float(metrics.sequence_gap_ms), 1),
                "sequence_order": "pelvis_torso" if metrics.sequence_gap_ms > 0 else "reverse"
            },
            "event_frames": {
                "load_frame": int(metrics.load_frame),
                "contact_frame": int(metrics.contact_frame),
                "follow_through_frame": int(metrics.follow_through_frame),
                "load_time_ms": round(float(metrics.load_frame) * 1000 / self.fps, 1),
                "contact_time_ms": round(float(metrics.contact_frame) * 1000 / self.fps, 1),
                "swing_duration_ms": round(float(metrics.follow_through_frame - metrics.load_frame) * 1000 / self.fps, 1)
            },
            "data_quality": {
                "avg_confidence": round(float(np.mean([f.confidence for f in self.frames_data])), 3),
                "frames_with_pose": int(len(self.frames_data)),
                "total_frames": int(self.frame_count),
                "completeness_pct": round(100 * len(self.frames_data) / self.frame_count, 1)
            }
        }

def main():
    """Main analysis pipeline"""
    
    print("=" * 60)
    print("🏏 KYLE TUCKER VIDEO ANALYSIS")
    print("=" * 60)
    print()
    
    # Video path
    video_path = "/home/user/uploaded_files/340039 (4).mp4"
    
    # Initialize analyzer
    analyzer = VideoAnalyzer(video_path)
    
    # Extract biomechanics
    frames = analyzer.extract_biomechanics()
    
    # Calculate rotation metrics
    metrics = analyzer.calculate_rotation_metrics()
    
    # Export to Reboot format
    report = analyzer.export_to_reboot_format(metrics, "Kyle Tucker")
    
    # Save report
    output_path = "/home/user/webapp/kyle_tucker_biomechanics_report.json"
    with open(output_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"💾 Report saved to: {output_path}")
    print()
    print("=" * 60)
    print("✅ ANALYSIS COMPLETE")
    print("=" * 60)
    
    return report

if __name__ == "__main__":
    main()
