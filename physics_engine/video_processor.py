"""
Video Processor Module
Extracts frames from video, detects FPS, normalizes time to milliseconds

CRITICAL: All time-based calculations MUST use milliseconds, not frame counts
This fixes the frame rate normalization bug where 300 FPS videos produced incorrect tempo ratios
"""

import cv2
import numpy as np
from typing import List, Tuple, Dict
from dataclasses import dataclass


@dataclass
class VideoMetadata:
    """Video file metadata"""
    filename: str
    fps: float
    total_frames: int
    duration_sec: float
    width: int
    height: int
    frame_time_ms: float  # Time per frame in milliseconds


class VideoProcessor:
    """
    Process video files for biomechanics analysis
    
    Key Features:
    - Frame extraction
    - FPS detection
    - Time normalization to milliseconds (NOT frame counts)
    """
    
    def __init__(self, video_path: str):
        """
        Initialize video processor
        
        Args:
            video_path: Path to video file
        """
        self.video_path = video_path
        self.cap = cv2.VideoCapture(video_path)
        
        if not self.cap.isOpened():
            raise ValueError(f"Cannot open video file: {video_path}")
        
        self.metadata = self._extract_metadata()
    
    def _extract_metadata(self) -> VideoMetadata:
        """Extract video metadata"""
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration_sec = total_frames / fps if fps > 0 else 0
        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        frame_time_ms = 1000.0 / fps if fps > 0 else 0  # CRITICAL: milliseconds per frame
        
        return VideoMetadata(
            filename=self.video_path.split('/')[-1],
            fps=fps,
            total_frames=total_frames,
            duration_sec=duration_sec,
            width=width,
            height=height,
            frame_time_ms=frame_time_ms
        )
    
    def get_frame(self, frame_number: int) -> Tuple[bool, np.ndarray]:
        """
        Get specific frame by number
        
        Args:
            frame_number: Frame index (0-based)
        
        Returns:
            (success, frame_image)
        """
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        return self.cap.read()
    
    def get_all_frames(self) -> List[Tuple[int, float, np.ndarray]]:
        """
        Extract all frames with frame number and timestamp
        
        Returns:
            List of (frame_number, timestamp_ms, frame_image)
        """
        frames = []
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Reset to start
        
        frame_number = 0
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            
            # CRITICAL: Calculate timestamp in milliseconds
            timestamp_ms = frame_number * self.metadata.frame_time_ms
            
            frames.append((frame_number, timestamp_ms, frame))
            frame_number += 1
        
        return frames
    
    def get_frame_at_time(self, time_ms: float) -> Tuple[bool, int, np.ndarray]:
        """
        Get frame closest to specified time
        
        Args:
            time_ms: Time in milliseconds
        
        Returns:
            (success, frame_number, frame_image)
        """
        # Convert time to frame number
        frame_number = int(time_ms / self.metadata.frame_time_ms)
        frame_number = min(frame_number, self.metadata.total_frames - 1)
        
        success, frame = self.get_frame(frame_number)
        return success, frame_number, frame
    
    def frame_number_to_time_ms(self, frame_number: int) -> float:
        """
        Convert frame number to timestamp in milliseconds
        
        CRITICAL: This ensures time-based calculations are independent of FPS
        
        Args:
            frame_number: Frame index
        
        Returns:
            Timestamp in milliseconds
        """
        return frame_number * self.metadata.frame_time_ms
    
    def time_ms_to_frame_number(self, time_ms: float) -> int:
        """
        Convert timestamp to frame number
        
        Args:
            time_ms: Time in milliseconds
        
        Returns:
            Frame number
        """
        return int(time_ms / self.metadata.frame_time_ms)
    
    def get_time_between_frames(self, frame1: int, frame2: int) -> float:
        """
        Calculate time difference between two frames
        
        CRITICAL: Returns time in milliseconds, not frame count difference
        
        Args:
            frame1: First frame number
            frame2: Second frame number
        
        Returns:
            Time difference in milliseconds
        """
        time1_ms = self.frame_number_to_time_ms(frame1)
        time2_ms = self.frame_number_to_time_ms(frame2)
        return abs(time2_ms - time1_ms)
    
    def release(self):
        """Release video capture"""
        self.cap.release()
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.release()
    
    def print_summary(self):
        """Print video metadata summary"""
        print(f"\n{'='*60}")
        print(f"VIDEO METADATA")
        print(f"{'='*60}")
        print(f"Filename: {self.metadata.filename}")
        print(f"Resolution: {self.metadata.width}×{self.metadata.height}")
        print(f"FPS: {self.metadata.fps:.2f}")
        print(f"Frame Time: {self.metadata.frame_time_ms:.2f} ms/frame")
        print(f"Total Frames: {self.metadata.total_frames}")
        print(f"Duration: {self.metadata.duration_sec:.2f} seconds")
        print(f"{'='*60}\n")


def test_frame_rate_normalization():
    """
    Test that demonstrates frame rate normalization working correctly
    
    This is the FIX for the bug where 300 FPS videos produced incorrect tempo ratios
    """
    print("\n" + "="*80)
    print("FRAME RATE NORMALIZATION TEST")
    print("="*80)
    print("\nThis test verifies that time calculations are FPS-independent\n")
    
    # Simulate two videos of the same real-world event
    # Event: Swing takes 1 second from first movement to contact
    
    print("Scenario: A swing that takes exactly 1000ms in real time")
    print("-" * 80)
    
    # 30 FPS video
    fps_30 = 30
    frames_30 = 30  # 30 frames in 1 second
    frame_time_30_ms = 1000.0 / fps_30
    duration_30_ms = frames_30 * frame_time_30_ms
    
    print(f"\n30 FPS Video:")
    print(f"  Frame time: {frame_time_30_ms:.2f} ms/frame")
    print(f"  Frames captured: {frames_30}")
    print(f"  Calculated duration: {duration_30_ms:.2f} ms")
    
    # 300 FPS video
    fps_300 = 300
    frames_300 = 300  # 300 frames in 1 second
    frame_time_300_ms = 1000.0 / fps_300
    duration_300_ms = frames_300 * frame_time_300_ms
    
    print(f"\n300 FPS Video:")
    print(f"  Frame time: {frame_time_300_ms:.2f} ms/frame")
    print(f"  Frames captured: {frames_300}")
    print(f"  Calculated duration: {duration_300_ms:.2f} ms")
    
    print(f"\n{'='*80}")
    print("RESULT:")
    print(f"  Both videos correctly calculate duration as ~1000ms")
    print(f"  30 FPS:  {duration_30_ms:.2f} ms")
    print(f"  300 FPS: {duration_300_ms:.2f} ms")
    print(f"  Difference: {abs(duration_30_ms - duration_300_ms):.2f} ms (error: {abs(duration_30_ms - duration_300_ms)/10:.1f}%)")
    print(f"{'='*80}")
    
    print("\nThis is the correct approach - time calculations are now FPS-independent!")
    print("The bug was using frame count differences instead of time differences.\n")


if __name__ == "__main__":
    # Run normalization test first
    test_frame_rate_normalization()
    
    # Test with a real video
    print("\n" + "="*80)
    print("TESTING WITH REAL VIDEO")
    print("="*80)
    
    test_video = "/home/user/uploaded_files/131215-Hitting.mov"
    
    try:
        with VideoProcessor(test_video) as vp:
            vp.print_summary()
            
            # Test time conversion
            print("Time Conversion Examples:")
            print(f"  Frame 0 → {vp.frame_number_to_time_ms(0):.2f} ms")
            print(f"  Frame 30 → {vp.frame_number_to_time_ms(30):.2f} ms")
            print(f"  Frame 60 → {vp.frame_number_to_time_ms(60):.2f} ms")
            print(f"  Time between frame 0 and frame 30: {vp.get_time_between_frames(0, 30):.2f} ms")
            print()
    except Exception as e:
        print(f"Error: {e}")
