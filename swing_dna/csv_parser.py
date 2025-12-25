"""
CSV Parser for Swing DNA Analysis
=================================

Parses biomechanical data from two CSV files:
1. momentum-energy.csv: Angular momentum and kinetic energy per body segment
2. inverse-kinematics.csv: Joint angles and positions over time

Extracts key metrics for pattern recognition and efficiency calculation.
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple, Optional
from dataclasses import dataclass


@dataclass
class SwingMetrics:
    """Container for extracted swing metrics"""
    # Frame data
    contact_frame: int
    total_frames: int
    
    # Knee metrics
    lead_knee_angle: float  # degrees at contact
    
    # Hip metrics
    hip_angular_momentum: float  # angular momentum magnitude
    hip_peak_frame: int
    
    # Shoulder metrics
    shoulder_angular_momentum: float
    shoulder_peak_frame: int
    
    # Ratios and timing
    shoulder_hip_ratio: float
    timing_gap_ms: float  # milliseconds between hip and shoulder peaks
    
    # Bat metrics
    bat_speed: float  # mph
    bat_kinetic_energy: float
    
    # Arm extension
    lead_arm_extension: float  # degrees
    
    # Ground force estimate
    vertical_grf_estimate: float  # multiple of bodyweight
    lead_leg_energy: float
    
    # Additional context
    handedness: str  # 'RHH' or 'LHH'


class CSVParser:
    """
    Parse biomechanical CSV files and extract swing metrics
    """
    
    def __init__(self, fps: float = 120.0):
        """
        Initialize parser
        
        Args:
            fps: Frames per second of motion capture (default: 120)
        """
        self.fps = fps
        self.ms_per_frame = 1000.0 / fps  # milliseconds per frame
    
    def parse_files(
        self, 
        momentum_file_path: str, 
        kinematics_file_path: str,
        handedness: str = 'RHH'
    ) -> SwingMetrics:
        """
        Parse both CSV files and extract metrics
        
        Args:
            momentum_file_path: Path to momentum-energy.csv
            kinematics_file_path: Path to inverse-kinematics.csv
            handedness: 'RHH' (right-handed) or 'LHH' (left-handed)
            
        Returns:
            SwingMetrics object with extracted values
        """
        # Load CSV files
        momentum_df = pd.read_csv(momentum_file_path)
        kinematics_df = pd.read_csv(kinematics_file_path)
        
        # Validate required columns
        self._validate_columns(momentum_df, kinematics_df)
        
        # Find contact frame (rel_frame = 0)
        contact_frame = self._find_contact_frame(momentum_df)
        
        # Extract metrics from momentum file
        hip_metrics = self._extract_hip_metrics(momentum_df, contact_frame)
        shoulder_metrics = self._extract_shoulder_metrics(momentum_df, contact_frame)
        bat_metrics = self._extract_bat_metrics(momentum_df, contact_frame)
        leg_metrics = self._extract_leg_metrics(momentum_df, contact_frame)
        
        # Extract metrics from kinematics file
        knee_angle = self._extract_knee_angle(kinematics_df, contact_frame, handedness)
        arm_extension = self._extract_arm_extension(kinematics_df, contact_frame, handedness)
        
        # Calculate derived metrics
        shoulder_hip_ratio = self._calculate_ratio(
            shoulder_metrics['peak'], 
            hip_metrics['peak']
        )
        
        timing_gap_ms = self._calculate_timing_gap(
            hip_metrics['peak_frame'],
            shoulder_metrics['peak_frame']
        )
        
        # Estimate vertical GRF
        vertical_grf = self._estimate_vertical_grf(
            leg_metrics['energy'],
            hip_metrics['peak']
        )
        
        # Create metrics object
        return SwingMetrics(
            contact_frame=contact_frame,
            total_frames=len(momentum_df),
            lead_knee_angle=knee_angle,
            hip_angular_momentum=hip_metrics['peak'],
            hip_peak_frame=hip_metrics['peak_frame'],
            shoulder_angular_momentum=shoulder_metrics['peak'],
            shoulder_peak_frame=shoulder_metrics['peak_frame'],
            shoulder_hip_ratio=shoulder_hip_ratio,
            timing_gap_ms=timing_gap_ms,
            bat_speed=bat_metrics['speed'],
            bat_kinetic_energy=bat_metrics['energy'],
            lead_arm_extension=arm_extension,
            vertical_grf_estimate=vertical_grf,
            lead_leg_energy=leg_metrics['energy'],
            handedness=handedness
        )
    
    def _validate_columns(self, momentum_df: pd.DataFrame, kinematics_df: pd.DataFrame):
        """Validate required columns exist"""
        required_momentum = [
            'rel_frame',
            'lowertorso_angular_momentum_mag',
            'torso_angular_momentum_mag',
            'bat_kinetic_energy',
            'lleg_trans_energy'
        ]
        
        required_kinematics = [
            'rel_frame',
            'left_knee',
            'right_knee'
        ]
        
        missing_momentum = [col for col in required_momentum if col not in momentum_df.columns]
        missing_kinematics = [col for col in required_kinematics if col not in kinematics_df.columns]
        
        if missing_momentum:
            raise ValueError(f"Missing columns in momentum file: {missing_momentum}")
        if missing_kinematics:
            raise ValueError(f"Missing columns in kinematics file: {missing_kinematics}")
    
    def _find_contact_frame(self, df: pd.DataFrame) -> int:
        """Find contact frame (rel_frame = 0)"""
        contact_rows = df[df['rel_frame'] == 0]
        if contact_rows.empty:
            raise ValueError("No contact frame found (rel_frame = 0)")
        return contact_rows.index[0]
    
    def _extract_hip_metrics(self, df: pd.DataFrame, contact_frame: int) -> Dict:
        """Extract hip angular momentum metrics"""
        # Get pre-contact data only
        pre_contact = df[df['rel_frame'] <= 0]
        
        # Find peak hip angular momentum
        hip_angmom_col = 'lowertorso_angular_momentum_mag'
        peak_value = pre_contact[hip_angmom_col].max()
        peak_frame = pre_contact[hip_angmom_col].idxmax()
        
        # Value at contact
        contact_value = df.loc[contact_frame, hip_angmom_col]
        
        return {
            'peak': peak_value,
            'peak_frame': peak_frame,
            'contact': contact_value
        }
    
    def _extract_shoulder_metrics(self, df: pd.DataFrame, contact_frame: int) -> Dict:
        """Extract shoulder angular momentum metrics"""
        # Get pre-contact data only
        pre_contact = df[df['rel_frame'] <= 0]
        
        # Find peak shoulder angular momentum
        shoulder_angmom_col = 'torso_angular_momentum_mag'
        peak_value = pre_contact[shoulder_angmom_col].max()
        peak_frame = pre_contact[shoulder_angmom_col].idxmax()
        
        # Value at contact
        contact_value = df.loc[contact_frame, shoulder_angmom_col]
        
        return {
            'peak': peak_value,
            'peak_frame': peak_frame,
            'contact': contact_value
        }
    
    def _extract_bat_metrics(self, df: pd.DataFrame, contact_frame: int) -> Dict:
        """Extract bat speed and energy"""
        bat_ke = df.loc[contact_frame, 'bat_kinetic_energy']
        
        # Estimate bat speed from kinetic energy
        # KE = 0.5 * m * v^2
        # Assume bat mass ~900g = 0.9 kg
        # v = sqrt(2 * KE / m)
        bat_mass_kg = 0.9
        bat_speed_ms = np.sqrt(2 * bat_ke / bat_mass_kg) if bat_ke > 0 else 0
        bat_speed_mph = bat_speed_ms * 2.237  # m/s to mph
        
        return {
            'energy': bat_ke,
            'speed': bat_speed_mph
        }
    
    def _extract_leg_metrics(self, df: pd.DataFrame, contact_frame: int) -> Dict:
        """Extract lead leg energy"""
        leg_energy = df.loc[contact_frame, 'lleg_trans_energy']
        
        return {
            'energy': leg_energy
        }
    
    def _extract_knee_angle(
        self, 
        df: pd.DataFrame, 
        contact_frame: int, 
        handedness: str
    ) -> float:
        """Extract lead knee angle at contact"""
        # For RHH, lead leg is left
        # For LHH, lead leg is right
        knee_col = 'left_knee' if handedness == 'RHH' else 'right_knee'
        
        knee_angle = df.loc[contact_frame, knee_col]
        return knee_angle
    
    def _extract_arm_extension(
        self, 
        df: pd.DataFrame, 
        contact_frame: int, 
        handedness: str
    ) -> float:
        """
        Extract lead arm extension at contact
        
        This is a simplified calculation. In production, you'd calculate
        the angle between shoulder, elbow, and wrist positions.
        For now, use a proxy or default value.
        """
        # TODO: Implement proper arm extension calculation
        # For now, return a default/estimated value
        # This would require shoulder, elbow, wrist positions
        return 1.5  # Default placeholder
    
    def _calculate_ratio(self, shoulder: float, hip: float) -> float:
        """Calculate shoulder/hip angular momentum ratio"""
        if hip == 0 or np.isnan(hip):
            return 999.0  # Very high ratio (invalid)
        return shoulder / hip
    
    def _calculate_timing_gap(self, hip_frame: int, shoulder_frame: int) -> float:
        """Calculate timing gap between hip and shoulder peaks in milliseconds"""
        frame_diff = abs(shoulder_frame - hip_frame)
        timing_gap_ms = frame_diff * self.ms_per_frame
        return timing_gap_ms
    
    def _estimate_vertical_grf(self, leg_energy: float, hip_angmom: float) -> float:
        """
        Estimate vertical ground reaction force as multiple of bodyweight
        
        This is a simplified estimation. In production, you'd use force plate data.
        """
        # Rough estimation based on leg energy and hip output
        # Higher leg energy + higher hip momentum = higher vGRF
        if leg_energy > 100 and hip_angmom > 8:
            return 1.8  # Strong vertical force
        elif leg_energy > 50 and hip_angmom > 5:
            return 1.2  # Moderate vertical force
        else:
            return 0.8  # Weak vertical force
    
    def to_dict(self, metrics: SwingMetrics) -> Dict:
        """Convert SwingMetrics to dictionary"""
        return {
            'lead_knee_angle': metrics.lead_knee_angle,
            'hip_angular_momentum': metrics.hip_angular_momentum,
            'shoulder_angular_momentum': metrics.shoulder_angular_momentum,
            'shoulder_hip_ratio': metrics.shoulder_hip_ratio,
            'bat_speed': metrics.bat_speed,
            'timing_gap_ms': metrics.timing_gap_ms,
            'lead_arm_extension': metrics.lead_arm_extension,
            'vertical_grf_estimate': metrics.vertical_grf_estimate
        }


# Example usage
if __name__ == "__main__":
    parser = CSVParser()
    
    # Parse Eric Williams data
    metrics = parser.parse_files(
        momentum_file_path="example_data/eric_williams_momentum_energy.csv",
        kinematics_file_path="example_data/eric_williams_inverse_kinematics.csv",
        handedness="RHH"
    )
    
    print("📊 Extracted Metrics:")
    print(f"  Lead Knee Angle: {metrics.lead_knee_angle:.1f}°")
    print(f"  Hip Angular Momentum: {metrics.hip_angular_momentum:.2f}")
    print(f"  Shoulder Angular Momentum: {metrics.shoulder_angular_momentum:.2f}")
    print(f"  Shoulder/Hip Ratio: {metrics.shoulder_hip_ratio:.2f}x")
    print(f"  Bat Speed: {metrics.bat_speed:.1f} mph")
    print(f"  Timing Gap: {metrics.timing_gap_ms:.1f} ms")
