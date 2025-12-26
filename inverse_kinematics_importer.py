"""
Inverse Kinematics CSV Importer
Parse inverse-kinematics CSV files from Reboot Motion

IK files contain:
- Joint angles (3D rotations)
- Joint positions (x, y, z coordinates)
- Segment orientations
- Angular velocities (if available)
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import re


@dataclass
class RebootIKData:
    """Parsed inverse-kinematics data from Reboot Motion CSV"""
    session_id: str
    athlete_name: Optional[str]
    movement_type: str
    fps: float
    duration_s: float
    num_frames: int
    
    # Time data
    time_s: np.ndarray
    time_from_max_hand: Optional[np.ndarray]
    
    # Joint angles (degrees) - all segments
    joint_angles: Dict[str, np.ndarray]  # e.g., {'pelvis_x': [...], 'pelvis_y': [...]}
    
    # Joint positions (meters)
    joint_positions: Dict[str, np.ndarray]  # e.g., {'left_wrist_x': [...], 'left_wrist_y': [...]}
    
    # Segment orientations (if available)
    segment_orientations: Optional[Dict[str, np.ndarray]]
    
    # Angular velocities (deg/s) - if available
    angular_velocities: Optional[Dict[str, np.ndarray]]
    
    # Contact frame detection
    contact_frame: int
    contact_time_s: float


class InverseKinematicsImporter:
    """
    Import and parse inverse-kinematics CSV files from Reboot Motion
    """
    
    # Common joint names in Reboot Motion IK exports
    JOINTS = [
        'pelvis', 'torso', 'thorax',
        'left_shoulder', 'right_shoulder',
        'left_elbow', 'right_elbow',
        'left_wrist', 'right_wrist',
        'left_hip', 'right_hip',
        'left_knee', 'right_knee',
        'left_ankle', 'right_ankle',
        'bat_knob', 'bat_barrel'
    ]
    
    # Angle axes
    ANGLE_AXES = ['x', 'y', 'z', 'flex', 'ext', 'rot', 'tilt']
    
    # Position axes
    POSITION_AXES = ['x', 'y', 'z']
    
    def __init__(self):
        """Initialize importer"""
        self.data = None
    
    def parse_filename(self, filename: str) -> Dict[str, str]:
        """
        Extract metadata from filename
        
        Expected format:
        20251220_session_3_rebootmotion_{session_id}_baseball-hitting_inverse-kinematics.csv
        
        Returns:
            Dict with: date, session_num, session_id, movement_type, data_type
        """
        pattern = r'(\d{8})_session_(\d+)_rebootmotion_([a-f0-9-]+)_([a-z-]+)_([a-z-]+)\.csv'
        match = re.match(pattern, filename)
        
        if match:
            return {
                'date': match.group(1),
                'session_num': match.group(2),
                'session_id': match.group(3),
                'movement_type': match.group(4),
                'data_type': match.group(5)
            }
        
        # Fallback: extract what we can
        parts = filename.replace('.csv', '').split('_')
        return {
            'session_id': parts[-2] if len(parts) >= 2 else 'unknown',
            'movement_type': parts[-3] if len(parts) >= 3 else 'baseball-hitting',
            'data_type': parts[-1] if len(parts) >= 1 else 'unknown'
        }
    
    def load_ik_csv(self, csv_path: str) -> RebootIKData:
        """
        Load and parse inverse-kinematics CSV file
        
        Args:
            csv_path: Path to CSV file
        
        Returns:
            RebootIKData with parsed joint angles, positions, velocities
        """
        print(f"\n📂 Loading Inverse Kinematics CSV: {csv_path}")
        
        # Load CSV
        df = pd.read_csv(csv_path)
        
        print(f"   Loaded {len(df)} rows, {len(df.columns)} columns")
        
        # Parse filename
        filename = Path(csv_path).name
        metadata = self.parse_filename(filename)
        
        print(f"   Session ID: {metadata['session_id']}")
        print(f"   Movement: {metadata['movement_type']}")
        print(f"   Data Type: {metadata['data_type']}")
        
        # Extract time data
        time_s = self._get_column(df, ['time', 'timestamp', 't'], required=True)
        time_from_max_hand = self._get_column(df, ['time_from_max_hand'], required=False)
        
        # Calculate FPS and duration
        if len(time_s) > 1:
            fps = 1.0 / np.mean(np.diff(time_s))
            duration_s = time_s[-1] - time_s[0]
        else:
            fps = 240.0
            duration_s = 0.0
        
        print(f"   FPS: {fps:.1f}, Duration: {duration_s:.2f}s, Frames: {len(df)}")
        
        # Find contact frame
        if time_from_max_hand is not None:
            contact_frame = np.argmin(np.abs(time_from_max_hand))
            contact_time_s = time_s[contact_frame]
        else:
            # Fallback: assume contact is at 70% of video
            contact_frame = int(len(df) * 0.7)
            contact_time_s = time_s[contact_frame]
        
        print(f"   Contact frame: {contact_frame}, Time: {contact_time_s:.3f}s")
        
        # Extract joint angles
        print(f"\n   Extracting joint angles...")
        joint_angles = self._extract_joint_angles(df)
        print(f"   Found {len(joint_angles)} joint angle series")
        
        # Extract joint positions
        print(f"   Extracting joint positions...")
        joint_positions = self._extract_joint_positions(df)
        print(f"   Found {len(joint_positions)} joint position series")
        
        # Extract angular velocities (if available)
        angular_velocities = self._extract_angular_velocities(df)
        if angular_velocities:
            print(f"   Found {len(angular_velocities)} angular velocity series")
        
        # Extract segment orientations (if available)
        segment_orientations = self._extract_segment_orientations(df)
        if segment_orientations:
            print(f"   Found {len(segment_orientations)} segment orientation series")
        
        # Create IK data object
        ik_data = RebootIKData(
            session_id=metadata['session_id'],
            athlete_name=None,
            movement_type=metadata['movement_type'],
            fps=fps,
            duration_s=duration_s,
            num_frames=len(df),
            time_s=time_s,
            time_from_max_hand=time_from_max_hand,
            joint_angles=joint_angles,
            joint_positions=joint_positions,
            segment_orientations=segment_orientations,
            angular_velocities=angular_velocities,
            contact_frame=contact_frame,
            contact_time_s=contact_time_s
        )
        
        print(f"   ✅ Successfully loaded inverse kinematics data")
        
        return ik_data
    
    def _extract_joint_angles(self, df: pd.DataFrame) -> Dict[str, np.ndarray]:
        """Extract all joint angles from dataframe"""
        joint_angles = {}
        
        # Look for columns like: pelvis_x, pelvis_y, pelvis_z, etc.
        for joint in self.JOINTS:
            for axis in self.ANGLE_AXES:
                # Try multiple naming conventions
                col_names = [
                    f"{joint}_{axis}",
                    f"{joint}_angle_{axis}",
                    f"{joint}_{axis}_angle",
                    f"{joint}_rot_{axis}"
                ]
                
                for col_name in col_names:
                    if col_name in df.columns:
                        joint_angles[f"{joint}_{axis}"] = df[col_name].values
                        break
        
        return joint_angles
    
    def _extract_joint_positions(self, df: pd.DataFrame) -> Dict[str, np.ndarray]:
        """Extract all joint positions from dataframe"""
        joint_positions = {}
        
        # Look for columns like: left_wrist_x, left_wrist_y, left_wrist_z
        for joint in self.JOINTS:
            for axis in self.POSITION_AXES:
                # Try multiple naming conventions
                col_names = [
                    f"{joint}_{axis}",
                    f"{joint}_pos_{axis}",
                    f"{joint}_position_{axis}",
                    f"pos_{joint}_{axis}"
                ]
                
                for col_name in col_names:
                    if col_name in df.columns:
                        joint_positions[f"{joint}_{axis}"] = df[col_name].values
                        break
        
        return joint_positions
    
    def _extract_angular_velocities(self, df: pd.DataFrame) -> Optional[Dict[str, np.ndarray]]:
        """Extract angular velocities if available"""
        angular_velocities = {}
        
        for joint in self.JOINTS:
            for axis in self.ANGLE_AXES:
                col_names = [
                    f"{joint}_vel_{axis}",
                    f"{joint}_angular_vel_{axis}",
                    f"{joint}_omega_{axis}",
                    f"vel_{joint}_{axis}"
                ]
                
                for col_name in col_names:
                    if col_name in df.columns:
                        angular_velocities[f"{joint}_{axis}"] = df[col_name].values
                        break
        
        return angular_velocities if angular_velocities else None
    
    def _extract_segment_orientations(self, df: pd.DataFrame) -> Optional[Dict[str, np.ndarray]]:
        """Extract segment orientations if available"""
        orientations = {}
        
        segments = ['pelvis', 'torso', 'bat']
        
        for segment in segments:
            for axis in ['qw', 'qx', 'qy', 'qz']:  # Quaternions
                col_names = [
                    f"{segment}_orient_{axis}",
                    f"{segment}_quaternion_{axis}",
                    f"{segment}_{axis}"
                ]
                
                for col_name in col_names:
                    if col_name in df.columns:
                        orientations[f"{segment}_{axis}"] = df[col_name].values
                        break
        
        return orientations if orientations else None
    
    def _get_column(self, df: pd.DataFrame, column_names: List[str], 
                   required: bool = True) -> Optional[np.ndarray]:
        """
        Try to find column by multiple possible names
        """
        for col_name in column_names:
            if col_name in df.columns:
                return df[col_name].values
        
        if required:
            raise ValueError(f"Required column not found. Tried: {column_names}")
        
        return None
    
    def calculate_ik_metrics(self, ik_data: RebootIKData) -> Dict:
        """
        Calculate metrics from inverse kinematics data
        
        Args:
            ik_data: Parsed IK data
        
        Returns:
            Dict with calculated metrics
        """
        print(f"\n📊 Calculating IK Metrics")
        
        contact_idx = ik_data.contact_frame
        
        metrics = {
            'contact_frame': contact_idx,
            'contact_time_s': ik_data.contact_time_s
        }
        
        # Calculate joint ranges of motion
        rom = {}
        for joint_name, angles in ik_data.joint_angles.items():
            rom[joint_name] = {
                'min': float(np.min(angles)),
                'max': float(np.max(angles)),
                'range': float(np.max(angles) - np.min(angles)),
                'at_contact': float(angles[contact_idx])
            }
        
        metrics['range_of_motion'] = rom
        
        # Calculate max angular velocities (if available)
        if ik_data.angular_velocities:
            max_vels = {}
            for joint_name, vels in ik_data.angular_velocities.items():
                max_vels[joint_name] = {
                    'max': float(np.max(np.abs(vels))),
                    'at_contact': float(vels[contact_idx])
                }
            
            metrics['max_angular_velocities'] = max_vels
        
        # Calculate bat path (if available)
        if 'bat_barrel_x' in ik_data.joint_positions and 'bat_barrel_y' in ik_data.joint_positions:
            bat_x = ik_data.joint_positions['bat_barrel_x']
            bat_y = ik_data.joint_positions['bat_barrel_y']
            bat_z = ik_data.joint_positions.get('bat_barrel_z', np.zeros_like(bat_x))
            
            # Calculate path length
            path_length = 0
            for i in range(1, len(bat_x)):
                dx = bat_x[i] - bat_x[i-1]
                dy = bat_y[i] - bat_y[i-1]
                dz = bat_z[i] - bat_z[i-1]
                path_length += np.sqrt(dx**2 + dy**2 + dz**2)
            
            metrics['bat_path_length_m'] = float(path_length)
            
            print(f"   Bat path length: {path_length:.2f}m")
        
        # Hip-shoulder separation
        if 'pelvis_y' in ik_data.joint_angles and 'torso_y' in ik_data.joint_angles:
            pelvis_angle = ik_data.joint_angles['pelvis_y']
            torso_angle = ik_data.joint_angles['torso_y']
            
            separation = torso_angle - pelvis_angle
            max_separation = np.max(np.abs(separation))
            separation_at_contact = abs(separation[contact_idx])
            
            metrics['hip_shoulder_separation'] = {
                'max_deg': float(max_separation),
                'at_contact_deg': float(separation_at_contact)
            }
            
            print(f"   Max hip-shoulder separation: {max_separation:.1f}°")
            print(f"   Separation at contact: {separation_at_contact:.1f}°")
        
        print(f"   ✅ IK metrics calculated")
        
        return metrics


def test_ik_importer():
    """Test the IK importer"""
    importer = InverseKinematicsImporter()
    
    # Example - would need actual IK CSV file
    print("Inverse Kinematics Importer ready")
    print("Waiting for IK CSV file upload...")


if __name__ == "__main__":
    test_ik_importer()
