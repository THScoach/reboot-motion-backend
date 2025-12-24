"""
Stability Score Calculator
Calculates head movement and spine stability across swing phases

Head stability is critical for consistent bat-to-ball contact.
Measures total head movement from stance through contact.

Grading Scale:
- A+ (95-100): < 1.0 inches movement
- A (90-94): 1.0-1.5 inches
- A- (85-89): 1.5-2.0 inches
- B (75-84): 2.0-3.0 inches
- C (<75): > 3.0 inches

Author: Builder 2 (Backend & Database AI)
Date: 2024-12-24
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import numpy as np


@dataclass
class PoseLandmark:
    """Single pose landmark with 3D coordinates"""
    x: float  # Normalized x coordinate (0-1)
    y: float  # Normalized y coordinate (0-1)
    z: float  # Depth (relative to hips, in image scale)
    visibility: float  # Confidence score (0-1)


@dataclass
class PoseFrame:
    """Pose data for a single frame"""
    frame_number: int
    timestamp_ms: float
    landmarks: Dict[str, PoseLandmark]
    is_valid: bool


def calculate_stability_score(
    pose_frames: List[PoseFrame],
    key_phases: Dict[str, List[int]],
    frame_width: int = 1920,
    frame_height: int = 1080,
    player_height_inches: float = 72.0
) -> Dict:
    """
    Calculate head movement and spine stability across swing phases
    
    Args:
        pose_frames: List of PoseFrame objects with head landmark positions
        key_phases: Dict with phase boundaries:
            {
                'load': [0, 30],
                'stride': [30, 60],
                'launch': [60, 90],
                'contact': [90, 120],
                'finish': [120, 150]
            }
        frame_width: Video frame width in pixels (for scaling)
        frame_height: Video frame height in pixels (for scaling)
        player_height_inches: Player's height in inches (for real-world scaling)
    
    Returns:
        Dictionary with stability analysis:
        {
            'total_movement_inches': 2.1,
            'stability_score': 92,
            'grade': 'A-',
            'phase_movements': {
                'load': 1.2,
                'stride': 0.8,
                'launch': 0.4,
                'contact': 0.4,
                'finish': 0.6
            }
        }
    """
    if not pose_frames:
        return _empty_stability_score()
    
    # Extract head positions (nose landmark) across all frames
    head_positions = _extract_head_positions(pose_frames)
    
    if len(head_positions) < 2:
        return _empty_stability_score()
    
    # Calculate pixel-to-inch conversion factor
    # Assume player's head-to-toe height spans ~60% of frame height (typical framing)
    pixels_per_inch = (frame_height * 0.6) / player_height_inches
    
    # Calculate phase-by-phase movement
    phase_movements = _calculate_phase_movements(
        head_positions,
        key_phases,
        pixels_per_inch
    )
    
    # Calculate total movement (sum of all phases)
    total_movement_inches = sum(phase_movements.values())
    
    # Calculate stability score (0-100)
    stability_score = _calculate_score(total_movement_inches)
    
    # Assign grade
    grade = _assign_grade(stability_score)
    
    return {
        'total_movement_inches': round(total_movement_inches, 2),
        'stability_score': stability_score,
        'grade': grade,
        'phase_movements': {
            phase: round(movement, 2)
            for phase, movement in phase_movements.items()
        },
        'description': _get_grade_description(grade)
    }


def _extract_head_positions(pose_frames: List[PoseFrame]) -> List[Tuple[float, float, int]]:
    """
    Extract head (nose) positions from pose frames
    
    Returns:
        List of (x, y, frame_number) tuples in normalized coordinates
    """
    head_positions = []
    
    for frame in pose_frames:
        if not frame.is_valid:
            continue
        
        # Get nose landmark (index 0 in MediaPipe Pose)
        nose = frame.landmarks.get('nose')
        if nose and nose.visibility > 0.5:  # Only use confident detections
            head_positions.append((nose.x, nose.y, frame.frame_number))
    
    return head_positions


def _calculate_phase_movements(
    head_positions: List[Tuple[float, float, int]],
    key_phases: Dict[str, List[int]],
    pixels_per_inch: float
) -> Dict[str, float]:
    """
    Calculate head movement for each swing phase
    
    Args:
        head_positions: List of (x, y, frame_number) tuples
        key_phases: Phase boundaries
        pixels_per_inch: Conversion factor from pixels to inches
    
    Returns:
        Dictionary of phase names to movement in inches
    """
    phase_movements = {}
    
    # Convert head positions to dict for easy lookup
    pos_dict = {frame_num: (x, y) for x, y, frame_num in head_positions}
    
    for phase_name, (start_frame, end_frame) in key_phases.items():
        # Get positions within this phase
        phase_pos = [
            (x, y) for frame_num, (x, y) in pos_dict.items()
            if start_frame <= frame_num <= end_frame
        ]
        
        if len(phase_pos) < 2:
            phase_movements[phase_name] = 0.0
            continue
        
        # Calculate total path length (sum of distances between consecutive points)
        total_distance_normalized = 0.0
        for i in range(1, len(phase_pos)):
            x1, y1 = phase_pos[i-1]
            x2, y2 = phase_pos[i]
            
            # Euclidean distance in normalized coordinates
            dist = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            total_distance_normalized += dist
        
        # Convert to pixels (assume average frame dimension)
        avg_frame_dimension = 1500  # Typical average of width and height
        distance_pixels = total_distance_normalized * avg_frame_dimension
        
        # Convert to inches
        distance_inches = distance_pixels / pixels_per_inch
        
        phase_movements[phase_name] = distance_inches
    
    return phase_movements


def _calculate_score(total_movement_inches: float) -> int:
    """
    Calculate stability score (0-100) based on total head movement
    
    Scoring curve:
    - < 1.0 inches: 95-100 (Excellent)
    - 1.0-1.5 inches: 90-94 (Very Good)
    - 1.5-2.0 inches: 85-89 (Good)
    - 2.0-3.0 inches: 75-84 (Fair)
    - > 3.0 inches: < 75 (Needs Improvement)
    """
    if total_movement_inches < 1.0:
        # Excellent range: 95-100
        score = 100 - (total_movement_inches / 1.0) * 5
    elif total_movement_inches < 1.5:
        # Very Good range: 90-94
        score = 94 - ((total_movement_inches - 1.0) / 0.5) * 4
    elif total_movement_inches < 2.0:
        # Good range: 85-89
        score = 89 - ((total_movement_inches - 1.5) / 0.5) * 4
    elif total_movement_inches < 3.0:
        # Fair range: 75-84
        score = 84 - ((total_movement_inches - 2.0) / 1.0) * 9
    else:
        # Needs Improvement: < 75
        # Exponential decay below 75
        score = 75 * np.exp(-0.3 * (total_movement_inches - 3.0))
    
    return int(round(max(0, min(100, score))))


def _assign_grade(stability_score: int) -> str:
    """
    Assign letter grade based on stability score
    
    Args:
        stability_score: Score from 0-100
    
    Returns:
        Letter grade (A+, A, A-, B, C, D, F)
    """
    if stability_score >= 95:
        return 'A+'
    elif stability_score >= 90:
        return 'A'
    elif stability_score >= 85:
        return 'A-'
    elif stability_score >= 80:
        return 'B+'
    elif stability_score >= 75:
        return 'B'
    elif stability_score >= 70:
        return 'B-'
    elif stability_score >= 65:
        return 'C+'
    elif stability_score >= 60:
        return 'C'
    elif stability_score >= 55:
        return 'C-'
    elif stability_score >= 50:
        return 'D'
    else:
        return 'F'


def _get_grade_description(grade: str) -> str:
    """Get descriptive text for grade"""
    descriptions = {
        'A+': 'Elite head stability - Minimal movement ensures consistent contact',
        'A': 'Excellent stability - Very slight movement',
        'A-': 'Very good stability - Minor movement within acceptable range',
        'B+': 'Good stability - Some movement but manageable',
        'B': 'Fair stability - Noticeable movement may affect consistency',
        'B-': 'Below average stability - Movement reducing contact quality',
        'C+': 'Poor stability - Significant head movement',
        'C': 'Poor stability - Major head movement issues',
        'C-': 'Very poor stability - Severe head movement',
        'D': 'Critical stability issue - Excessive head movement',
        'F': 'Critical stability issue - Extreme head movement'
    }
    return descriptions.get(grade, 'Unknown')


def _empty_stability_score() -> Dict:
    """Return empty stability score for invalid input"""
    return {
        'total_movement_inches': 0.0,
        'stability_score': 0,
        'grade': 'N/A',
        'phase_movements': {},
        'description': 'Unable to calculate - insufficient pose data'
    }


def analyze_stability_from_pose_frames(
    pose_frames: List[Dict],
    player_height_inches: float = 72.0
) -> Dict:
    """
    High-level function to analyze stability from raw pose frame data
    
    Args:
        pose_frames: List of pose frame dictionaries (from MediaPipe)
        player_height_inches: Player's height in inches
    
    Returns:
        Stability score dictionary
    """
    # Convert dict format to PoseFrame objects
    converted_frames = []
    for frame_data in pose_frames:
        landmarks = {}
        for name, lm_data in frame_data.get('landmarks', {}).items():
            landmarks[name] = PoseLandmark(
                x=lm_data['x'],
                y=lm_data['y'],
                z=lm_data.get('z', 0.0),
                visibility=lm_data.get('visibility', 1.0)
            )
        
        converted_frames.append(PoseFrame(
            frame_number=frame_data['frame_number'],
            timestamp_ms=frame_data['timestamp_ms'],
            landmarks=landmarks,
            is_valid=frame_data.get('is_valid', True)
        ))
    
    # Infer phase boundaries from frame count
    total_frames = len(converted_frames)
    key_phases = {
        'load': [0, int(total_frames * 0.2)],
        'stride': [int(total_frames * 0.2), int(total_frames * 0.4)],
        'launch': [int(total_frames * 0.4), int(total_frames * 0.6)],
        'contact': [int(total_frames * 0.6), int(total_frames * 0.8)],
        'finish': [int(total_frames * 0.8), total_frames]
    }
    
    return calculate_stability_score(
        pose_frames=converted_frames,
        key_phases=key_phases,
        player_height_inches=player_height_inches
    )


# Example usage
if __name__ == "__main__":
    print("Stability Score Calculator - Example")
    print("=" * 50)
    
    # Example: Perfect stability (A+)
    print("\nExample 1: Excellent Stability")
    print("  Total Movement: 0.8 inches")
    score = _calculate_score(0.8)
    grade = _assign_grade(score)
    print(f"  Score: {score}/100")
    print(f"  Grade: {grade}")
    print(f"  Description: {_get_grade_description(grade)}")
    
    # Example: Good stability (A-)
    print("\nExample 2: Good Stability")
    print("  Total Movement: 1.8 inches")
    score = _calculate_score(1.8)
    grade = _assign_grade(score)
    print(f"  Score: {score}/100")
    print(f"  Grade: {grade}")
    print(f"  Description: {_get_grade_description(grade)}")
    
    # Example: Fair stability (B)
    print("\nExample 3: Fair Stability")
    print("  Total Movement: 2.8 inches")
    score = _calculate_score(2.8)
    grade = _assign_grade(score)
    print(f"  Score: {score}/100")
    print(f"  Grade: {grade}")
    print(f"  Description: {_get_grade_description(grade)}")
