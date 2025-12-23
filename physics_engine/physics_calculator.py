"""
Physics Calculator Module
Calculates angular velocities, linear velocities, and kinetic chain sequencing

Key Calculations:
1. Joint angular velocities (pelvis, torso, shoulders, hips)
2. Linear velocities (hands, bat barrel)
3. Kinetic chain sequencing (ground → pelvis → torso → arms → bat)
4. Energy transfer efficiency

CRITICAL FIX: Bat speed now uses proper lever arm physics
- Old: bat_velocity = hand_velocity * 1.5 (gave 21.6 mph for pros)
- New: bat_velocity = hand_velocity + (angular_velocity * effective_radius)
- Expected: 70-85 mph for elite pros
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from pose_detector import PoseFrame
from bat_speed_calculator import BatSpeedCalculator


@dataclass
class JointAngles:
    """Joint angles at a specific frame"""
    frame_number: int
    timestamp_ms: float
    pelvis_angle: float  # Rotation from stance position (degrees)
    torso_angle: float   # Rotation from stance position (degrees)
    hip_angle: float     # Hip flexion/extension (degrees)
    shoulder_angle: float  # Shoulder rotation (degrees)
    elbow_angle: float   # Elbow flexion (degrees)
    wrist_angle: float   # Wrist angle (degrees)
    knee_angle: float    # Knee flexion (degrees)


@dataclass
class JointVelocities:
    """Joint angular velocities at a specific frame"""
    frame_number: int
    timestamp_ms: float
    pelvis_velocity: float  # deg/s
    torso_velocity: float   # deg/s
    shoulder_velocity: float  # deg/s
    hip_velocity: float     # deg/s
    hand_velocity: float    # m/s (linear)
    bat_velocity: float     # m/s (linear, estimated)


@dataclass
class KineticSequence:
    """Timing of peak velocities in kinetic chain"""
    pelvis_peak_time_ms: float
    torso_peak_time_ms: float
    shoulder_peak_time_ms: float
    hand_peak_time_ms: float
    bat_peak_time_ms: float
    
    def get_sequence_quality(self) -> float:
        """
        Calculate how well the sequence follows ground → bat
        Perfect sequence: each peak comes after the previous
        Returns 0-100 score
        """
        times = [
            self.pelvis_peak_time_ms,
            self.torso_peak_time_ms,
            self.shoulder_peak_time_ms,
            self.hand_peak_time_ms,
            self.bat_peak_time_ms
        ]
        
        # Check if sequence is in order
        in_order = all(times[i] <= times[i+1] for i in range(len(times)-1))
        
        if not in_order:
            # Calculate how many inversions
            inversions = sum(1 for i in range(len(times)-1) if times[i] > times[i+1])
            score = max(0, 100 - (inversions * 25))
        else:
            # Perfect sequence, score based on timing gaps
            gaps = [times[i+1] - times[i] for i in range(len(times)-1)]
            avg_gap = np.mean(gaps)
            
            # Ideal gap is 15-30ms between segments
            if 15 <= avg_gap <= 30:
                score = 100
            elif avg_gap < 15:
                score = 80  # Too fast, possible early release
            else:
                score = 90  # Slightly slow but still good
        
        return score


class PhysicsCalculator:
    """
    Calculate physics metrics from pose data
    """
    
    def __init__(self):
        """Initialize physics calculator"""
        self.bat_speed_calc = BatSpeedCalculator()
    
    def calculate_angle_2d(self, point1: Tuple[float, float], 
                          point2: Tuple[float, float], 
                          point3: Tuple[float, float]) -> float:
        """
        Calculate angle between three points in 2D
        
        Args:
            point1: (x, y) first point
            point2: (x, y) vertex point
            point3: (x, y) third point
        
        Returns:
            Angle in degrees (0-180)
        """
        v1 = np.array([point1[0] - point2[0], point1[1] - point2[1]])
        v2 = np.array([point3[0] - point2[0], point3[1] - point2[1]])
        
        # Normalize
        v1_norm = v1 / (np.linalg.norm(v1) + 1e-6)
        v2_norm = v2 / (np.linalg.norm(v2) + 1e-6)
        
        # Calculate angle
        dot_product = np.clip(np.dot(v1_norm, v2_norm), -1.0, 1.0)
        angle_rad = np.arccos(dot_product)
        angle_deg = np.degrees(angle_rad)
        
        return angle_deg
    
    def calculate_rotation_angle(self, left_point: Tuple[float, float],
                                 right_point: Tuple[float, float],
                                 reference_vertical: bool = True) -> float:
        """
        Calculate rotation angle of a segment (e.g., shoulders, hips)
        
        Args:
            left_point: (x, y) left landmark
            right_point: (x, y) right landmark
            reference_vertical: If True, measure from vertical; else from horizontal
        
        Returns:
            Angle in degrees
        """
        dx = right_point[0] - left_point[0]
        dy = right_point[1] - left_point[1]
        
        angle_rad = np.arctan2(dy, dx)
        angle_deg = np.degrees(angle_rad)
        
        if reference_vertical:
            # Measure from vertical (0 = perfectly vertical)
            angle_deg = 90 - angle_deg
        
        return angle_deg
    
    def extract_joint_angles(self, pose_frame: PoseFrame) -> Optional[JointAngles]:
        """
        Extract all joint angles from a pose frame
        
        Args:
            pose_frame: PoseFrame with landmarks
        
        Returns:
            JointAngles or None if pose invalid
        """
        if not pose_frame.is_valid or not pose_frame.landmarks:
            return None
        
        lm = pose_frame.landmarks
        
        # Check required landmarks exist
        required = [
            'left_shoulder', 'right_shoulder',
            'left_hip', 'right_hip',
            'left_elbow', 'right_elbow',
            'left_wrist', 'right_wrist',
            'left_knee', 'right_knee'
        ]
        
        if not all(joint in lm for joint in required):
            return None
        
        # Extract positions
        def get_pos(joint_name):
            return (lm[joint_name].x, lm[joint_name].y)
        
        # 1. Pelvis rotation (hip line angle)
        pelvis_angle = self.calculate_rotation_angle(
            get_pos('left_hip'), get_pos('right_hip')
        )
        
        # 2. Torso rotation (shoulder line angle)
        torso_angle = self.calculate_rotation_angle(
            get_pos('left_shoulder'), get_pos('right_shoulder')
        )
        
        # 3. Hip angle (torso to thigh) - use right side
        hip_angle = self.calculate_angle_2d(
            get_pos('right_shoulder'),
            get_pos('right_hip'),
            get_pos('right_knee')
        )
        
        # 4. Shoulder angle (torso to upper arm) - use lead arm
        shoulder_angle = self.calculate_angle_2d(
            get_pos('right_hip'),  # Body reference
            get_pos('right_shoulder'),
            get_pos('right_elbow')
        )
        
        # 5. Elbow angle
        elbow_angle = self.calculate_angle_2d(
            get_pos('right_shoulder'),
            get_pos('right_elbow'),
            get_pos('right_wrist')
        )
        
        # 6. Knee angle - use back leg
        knee_angle = self.calculate_angle_2d(
            get_pos('left_hip'),
            get_pos('left_knee'),
            get_pos('left_ankle')
        )
        
        # 7. Wrist angle (simplified)
        wrist_angle = 180.0  # Placeholder for now
        
        return JointAngles(
            frame_number=pose_frame.frame_number,
            timestamp_ms=pose_frame.timestamp_ms,
            pelvis_angle=pelvis_angle,
            torso_angle=torso_angle,
            hip_angle=hip_angle,
            shoulder_angle=shoulder_angle,
            elbow_angle=elbow_angle,
            wrist_angle=wrist_angle,
            knee_angle=knee_angle
        )
    
    def calculate_angular_velocity(self, angle1: float, angle2: float,
                                   time1_ms: float, time2_ms: float) -> float:
        """
        Calculate angular velocity between two angles
        
        Args:
            angle1: Angle at time 1 (degrees)
            angle2: Angle at time 2 (degrees)
            time1_ms: Time 1 in milliseconds
            time2_ms: Time 2 in milliseconds
        
        Returns:
            Angular velocity in degrees/second
        """
        delta_angle = angle2 - angle1
        delta_time_s = (time2_ms - time1_ms) / 1000.0
        
        if delta_time_s <= 0:
            return 0.0
        
        angular_velocity = delta_angle / delta_time_s
        return angular_velocity
    
    def calculate_linear_velocity(self, pos1: Tuple[float, float],
                                  pos2: Tuple[float, float],
                                  time1_ms: float, time2_ms: float,
                                  scale_factor: float = 1.0) -> float:
        """
        Calculate linear velocity between two positions
        
        Args:
            pos1: (x, y) at time 1 (normalized 0-1)
            pos2: (x, y) at time 2 (normalized 0-1)
            time1_ms: Time 1 in milliseconds
            time2_ms: Time 2 in milliseconds
            scale_factor: Conversion from normalized to meters
        
        Returns:
            Linear velocity in m/s
        """
        dx = (pos2[0] - pos1[0]) * scale_factor
        dy = (pos2[1] - pos1[1]) * scale_factor
        
        distance = np.sqrt(dx**2 + dy**2)
        delta_time_s = (time2_ms - time1_ms) / 1000.0
        
        if delta_time_s <= 0:
            return 0.0
        
        velocity = distance / delta_time_s
        return velocity
    
    def calculate_velocities(self, angles: List[JointAngles],
                            poses: List[PoseFrame],
                            scale_factor: float = 1.8) -> List[JointVelocities]:
        """
        Calculate velocities from angle and pose sequences
        
        Args:
            angles: List of JointAngles (time series)
            poses: List of PoseFrame (for hand positions)
            scale_factor: Approximate height in meters (for scaling)
        
        Returns:
            List of JointVelocities
        """
        velocities = []
        
        for i in range(1, len(angles)):
            prev = angles[i-1]
            curr = angles[i]
            
            # Angular velocities
            pelvis_vel = self.calculate_angular_velocity(
                prev.pelvis_angle, curr.pelvis_angle,
                prev.timestamp_ms, curr.timestamp_ms
            )
            
            torso_vel = self.calculate_angular_velocity(
                prev.torso_angle, curr.torso_angle,
                prev.timestamp_ms, curr.timestamp_ms
            )
            
            shoulder_vel = self.calculate_angular_velocity(
                prev.shoulder_angle, curr.shoulder_angle,
                prev.timestamp_ms, curr.timestamp_ms
            )
            
            hip_vel = self.calculate_angular_velocity(
                prev.hip_angle, curr.hip_angle,
                prev.timestamp_ms, curr.timestamp_ms
            )
            
            # Hand velocity (linear)
            prev_pose = poses[i-1]
            curr_pose = poses[i]
            
            if curr_pose.is_valid and 'right_wrist' in curr_pose.landmarks:
                prev_hand = (prev_pose.landmarks['right_wrist'].x,
                           prev_pose.landmarks['right_wrist'].y)
                curr_hand = (curr_pose.landmarks['right_wrist'].x,
                           curr_pose.landmarks['right_wrist'].y)
                
                hand_vel = self.calculate_linear_velocity(
                    prev_hand, curr_hand,
                    prev.timestamp_ms, curr.timestamp_ms,
                    scale_factor
                )
            else:
                hand_vel = 0.0
            
            # Bat velocity (using proper lever arm physics)
            # v_bat = v_hand + (ω_shoulder * r_effective)
            # where r_effective ≈ 2m (shoulder to barrel distance)
            bat_vel = self.bat_speed_calc.calculate_bat_velocity_simple(
                hand_vel, 
                shoulder_vel
            )
            
            velocities.append(JointVelocities(
                frame_number=curr.frame_number,
                timestamp_ms=curr.timestamp_ms,
                pelvis_velocity=pelvis_vel,
                torso_velocity=torso_vel,
                shoulder_velocity=shoulder_vel,
                hip_velocity=hip_vel,
                hand_velocity=hand_vel,
                bat_velocity=bat_vel
            ))
        
        return velocities
    
    def find_kinetic_sequence(self, velocities: List[JointVelocities]) -> KineticSequence:
        """
        Find peak velocities for each segment to determine kinetic sequence
        
        Args:
            velocities: List of JointVelocities
        
        Returns:
            KineticSequence with peak timing
        """
        # Extract velocity arrays
        pelvis_vels = [v.pelvis_velocity for v in velocities]
        torso_vels = [v.torso_velocity for v in velocities]
        shoulder_vels = [v.shoulder_velocity for v in velocities]
        hand_vels = [v.hand_velocity for v in velocities]
        bat_vels = [v.bat_velocity for v in velocities]
        
        # Find peak indices (use absolute value for rotation velocities)
        pelvis_peak_idx = np.argmax(np.abs(pelvis_vels))
        torso_peak_idx = np.argmax(np.abs(torso_vels))
        shoulder_peak_idx = np.argmax(np.abs(shoulder_vels))
        hand_peak_idx = np.argmax(hand_vels)
        bat_peak_idx = np.argmax(bat_vels)
        
        # Get timestamps
        pelvis_peak_time = velocities[pelvis_peak_idx].timestamp_ms
        torso_peak_time = velocities[torso_peak_idx].timestamp_ms
        shoulder_peak_time = velocities[shoulder_peak_idx].timestamp_ms
        hand_peak_time = velocities[hand_peak_idx].timestamp_ms
        bat_peak_time = velocities[bat_peak_idx].timestamp_ms
        
        return KineticSequence(
            pelvis_peak_time_ms=pelvis_peak_time,
            torso_peak_time_ms=torso_peak_time,
            shoulder_peak_time_ms=shoulder_peak_time,
            hand_peak_time_ms=hand_peak_time,
            bat_peak_time_ms=bat_peak_time
        )


if __name__ == "__main__":
    print("Physics Calculator Module")
    print("=" * 60)
    print("Calculates:")
    print("  - Joint angles from poses")
    print("  - Angular velocities (pelvis, torso, shoulders)")
    print("  - Linear velocities (hands, bat)")
    print("  - Kinetic chain sequencing")
    print("=" * 60)
