"""
Reboot Motion CSV Importer
Import and parse momentum-energy and inverse-kinematics CSV files

This provides a fallback if the Reboot Motion API is unavailable or slow.
Users can upload CSV files exported from Reboot Motion directly.

Supported file types:
1. momentum-energy.csv - Energy, momentum, kinetic data
2. inverse-kinematics.csv - Joint angles, positions, velocities (if available)
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import re


@dataclass
class RebootSwingData:
    """Parsed data from Reboot Motion CSV files"""
    session_id: str
    athlete_name: Optional[str]
    movement_type: str
    fps: float
    duration_s: float
    num_frames: int
    
    # Time data
    time_s: np.ndarray  # Time in seconds
    time_from_max_hand: np.ndarray  # Time relative to contact
    
    # Bat data
    bat_angular_momentum: np.ndarray
    bat_kinetic_energy: np.ndarray
    bat_position: Optional[np.ndarray]  # x, y, z if available
    
    # Body segment angular momentum
    pelvis_angular_momentum: np.ndarray
    torso_angular_momentum: np.ndarray
    lowertorso_angular_momentum: np.ndarray
    larm_angular_momentum: np.ndarray
    rarm_angular_momentum: np.ndarray
    
    # Energy data
    total_kinetic_energy: np.ndarray
    lowerhalf_kinetic_energy: Optional[np.ndarray]
    torso_kinetic_energy_val: Optional[np.ndarray]
    arms_kinetic_energy: Optional[np.ndarray]
    
    # Contact frame detection
    contact_frame: int
    contact_time_s: float


class RebootCSVImporter:
    """
    Import and parse Reboot Motion CSV files
    """
    
    def __init__(self):
        """Initialize importer"""
        self.data = None
    
    def parse_filename(self, filename: str) -> Dict[str, str]:
        """
        Extract metadata from filename
        
        Expected format:
        20251220_session_3_rebootmotion_{session_id}_baseball-hitting_momentum-energy.csv
        
        Returns:
            Dict with: date, session_num, session_id, movement_type, data_type
        """
        # Pattern: YYYYMMDD_session_N_rebootmotion_UUID_MOVEMENT-TYPE_DATA-TYPE.csv
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
    
    def load_momentum_energy_csv(self, csv_path: str) -> RebootSwingData:
        """
        Load and parse momentum-energy CSV file
        
        Args:
            csv_path: Path to CSV file
        
        Returns:
            RebootSwingData with parsed biomechanics
        """
        print(f"\n📂 Loading Reboot Motion CSV: {csv_path}")
        
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
        time_s = df['time'].values if 'time' in df.columns else np.arange(len(df)) / 240  # Assume 240 FPS
        time_from_max_hand = df['time_from_max_hand'].values if 'time_from_max_hand' in df.columns else np.zeros(len(df))
        
        # Calculate FPS and duration
        if len(time_s) > 1:
            fps = 1.0 / np.mean(np.diff(time_s))
            duration_s = time_s[-1] - time_s[0]
        else:
            fps = 240.0
            duration_s = 0.0
        
        print(f"   FPS: {fps:.1f}, Duration: {duration_s:.2f}s, Frames: {len(df)}")
        
        # Find contact frame (where time_from_max_hand is closest to 0)
        contact_frame = np.argmin(np.abs(time_from_max_hand))
        contact_time_s = time_s[contact_frame]
        
        print(f"   Contact frame: {contact_frame}, Time: {contact_time_s:.3f}s")
        
        # Extract bat data
        bat_columns = {
            'angular_momentum': 'bat_angular_momentum_mag',
            'kinetic_energy': 'bat_kinetic_energy',
            'x': 'bat_x',
            'y': 'bat_y',
            'z': 'bat_z'
        }
        
        bat_angular_momentum = self._get_column(df, [
            'bat_angular_momentum_mag',
            'bat_angmom_mag',
            'bat_angular_momentum'
        ])
        
        bat_kinetic_energy = self._get_column(df, [
            'bat_kinetic_energy',
            'bat_ke',
            'bat_energy'
        ])
        
        bat_position = None
        if 'bat_x' in df.columns and 'bat_y' in df.columns:
            bat_position = np.column_stack([
                df['bat_x'].values,
                df['bat_y'].values,
                df['bat_z'].values if 'bat_z' in df.columns else np.zeros(len(df))
            ])
        
        # Extract body segment angular momentum
        pelvis_angular_momentum = self._get_column(df, [
            'pelvis_angular_momentum_mag',
            'pelvis_angmom_mag',
            'lowertorso_angular_momentum_mag'
        ])
        
        torso_angular_momentum = self._get_column(df, [
            'torso_angular_momentum_mag',
            'torso_angmom_mag'
        ])
        
        lowertorso_angular_momentum = self._get_column(df, [
            'lowertorso_angular_momentum_mag',
            'lowertorso_angmom_mag',
            'pelvis_angular_momentum_mag'
        ])
        
        larm_angular_momentum = self._get_column(df, [
            'larm_angular_momentum_mag',
            'larm_angmom_mag',
            'left_arm_angular_momentum_mag'
        ])
        
        rarm_angular_momentum = self._get_column(df, [
            'rarm_angular_momentum_mag',
            'rarm_angmom_mag',
            'right_arm_angular_momentum_mag'
        ])
        
        # Extract energy data
        total_kinetic_energy = self._get_column(df, [
            'total_kinetic_energy',
            'total_ke',
            'total_energy'
        ])
        
        lowerhalf_kinetic_energy = self._get_column(df, [
            'lowerhalf_kinetic_energy',
            'legs_kinetic_energy',
            'lower_half_ke'
        ], required=False)
        
        torso_kinetic_energy_val = self._get_column(df, [
            'torso_kinetic_energy',
            'torso_ke'
        ], required=False)
        
        arms_kinetic_energy = self._get_column(df, [
            'arms_kinetic_energy',
            'arms_ke'
        ], required=False)
        
        # Create RebootSwingData object
        swing_data = RebootSwingData(
            session_id=metadata['session_id'],
            athlete_name=None,  # Not in CSV, user must provide
            movement_type=metadata['movement_type'],
            fps=fps,
            duration_s=duration_s,
            num_frames=len(df),
            time_s=time_s,
            time_from_max_hand=time_from_max_hand,
            bat_angular_momentum=bat_angular_momentum,
            bat_kinetic_energy=bat_kinetic_energy,
            bat_position=bat_position,
            pelvis_angular_momentum=pelvis_angular_momentum,
            torso_angular_momentum=torso_angular_momentum,
            lowertorso_angular_momentum=lowertorso_angular_momentum,
            larm_angular_momentum=larm_angular_momentum,
            rarm_angular_momentum=rarm_angular_momentum,
            total_kinetic_energy=total_kinetic_energy,
            lowerhalf_kinetic_energy=lowerhalf_kinetic_energy,
            torso_kinetic_energy_val=torso_kinetic_energy_val,
            arms_kinetic_energy=arms_kinetic_energy,
            contact_frame=contact_frame,
            contact_time_s=contact_time_s
        )
        
        print(f"   ✅ Successfully loaded Reboot Motion data")
        
        return swing_data
    
    def _get_column(self, df: pd.DataFrame, column_names: List[str], 
                   required: bool = True) -> Optional[np.ndarray]:
        """
        Try to find column by multiple possible names
        
        Args:
            df: DataFrame
            column_names: List of possible column names (in priority order)
            required: If True, raise error if not found
        
        Returns:
            Column data as numpy array, or None if not found and not required
        """
        for col_name in column_names:
            if col_name in df.columns:
                return df[col_name].values
        
        if required:
            raise ValueError(f"Required column not found. Tried: {column_names}")
        
        return None
    
    def calculate_ground_truth_metrics(self, swing_data: RebootSwingData,
                                      bat_mass_kg: float = 0.85) -> Dict:
        """
        Calculate ground truth metrics from Reboot Motion data
        
        Args:
            swing_data: Parsed Reboot swing data
            bat_mass_kg: Bat mass in kg (default 0.85 kg for 33"/30oz)
        
        Returns:
            Dict with ground truth metrics
        """
        print(f"\n📊 Calculating Ground Truth Metrics")
        
        # Find contact frame
        contact_idx = swing_data.contact_frame
        
        # Bat speed at contact (from kinetic energy)
        # KE = 0.5 * m * v^2  =>  v = sqrt(2 * KE / m)
        bat_ke_at_contact = swing_data.bat_kinetic_energy[contact_idx]
        bat_speed_ms = np.sqrt(2 * bat_ke_at_contact / bat_mass_kg)
        bat_speed_mph = bat_speed_ms * 2.237
        
        print(f"   Bat Speed at Contact: {bat_speed_mph:.1f} mph")
        
        # Peak bat speed (maximum in dataset)
        peak_bat_ke = np.max(swing_data.bat_kinetic_energy)
        peak_bat_speed_ms = np.sqrt(2 * peak_bat_ke / bat_mass_kg)
        peak_bat_speed_mph = peak_bat_speed_ms * 2.237
        
        print(f"   Peak Bat Speed: {peak_bat_speed_mph:.1f} mph")
        
        # Energy distribution at contact
        total_ke = swing_data.total_kinetic_energy[contact_idx]
        
        if swing_data.lowerhalf_kinetic_energy is not None:
            lowerhalf_ke = swing_data.lowerhalf_kinetic_energy[contact_idx]
            lowerhalf_pct = (lowerhalf_ke / total_ke) * 100
        else:
            lowerhalf_pct = None
        
        if swing_data.torso_kinetic_energy_val is not None:
            torso_ke = swing_data.torso_kinetic_energy_val[contact_idx]
            torso_pct = (torso_ke / total_ke) * 100
        else:
            torso_pct = None
        
        if swing_data.arms_kinetic_energy is not None:
            arms_ke = swing_data.arms_kinetic_energy[contact_idx]
            arms_pct = (arms_ke / total_ke) * 100
        else:
            arms_pct = None
        
        print(f"   Energy Distribution at Contact:")
        if lowerhalf_pct:
            print(f"      Lower Half: {lowerhalf_pct:.1f}%")
        if torso_pct:
            print(f"      Torso: {torso_pct:.1f}%")
        if arms_pct:
            print(f"      Arms: {arms_pct:.1f}%")
        
        # Find kinematic sequence peaks (time before contact)
        # Look in window before contact
        pre_contact_window = max(0, contact_idx - int(0.5 * swing_data.fps))  # 500ms before
        
        pelvis_peak_idx = pre_contact_window + np.argmax(
            swing_data.pelvis_angular_momentum[pre_contact_window:contact_idx+1]
        )
        torso_peak_idx = pre_contact_window + np.argmax(
            swing_data.torso_angular_momentum[pre_contact_window:contact_idx+1]
        )
        larm_peak_idx = pre_contact_window + np.argmax(
            swing_data.larm_angular_momentum[pre_contact_window:contact_idx+1]
        )
        rarm_peak_idx = pre_contact_window + np.argmax(
            swing_data.rarm_angular_momentum[pre_contact_window:contact_idx+1]
        )
        bat_peak_idx = pre_contact_window + np.argmax(
            swing_data.bat_angular_momentum[pre_contact_window:contact_idx+1]
        )
        
        # Calculate time before contact (ms)
        contact_time = swing_data.time_s[contact_idx]
        pelvis_time_before = (contact_time - swing_data.time_s[pelvis_peak_idx]) * 1000
        torso_time_before = (contact_time - swing_data.time_s[torso_peak_idx]) * 1000
        larm_time_before = (contact_time - swing_data.time_s[larm_peak_idx]) * 1000
        rarm_time_before = (contact_time - swing_data.time_s[rarm_peak_idx]) * 1000
        bat_time_before = (contact_time - swing_data.time_s[bat_peak_idx]) * 1000
        
        print(f"   Kinematic Sequence (ms before contact):")
        print(f"      Pelvis: {pelvis_time_before:.0f} ms")
        print(f"      Torso: {torso_time_before:.0f} ms")
        print(f"      L Arm: {larm_time_before:.0f} ms")
        print(f"      R Arm: {rarm_time_before:.0f} ms")
        print(f"      Bat: {bat_time_before:.0f} ms")
        
        # Calculate CORRECT tempo from lower half kinetic energy curve
        # Method: Load Start (min KE) → Hip Peak (max KE) → Contact
        # This matches the ground truth validation method
        
        # Get lower half KE (if available)
        lower_ke = swing_data.lower_half_kinetic_energy
        if lower_ke is None:
            # Fallback: estimate from simplified windows
            load_start_idx = max(0, contact_idx - int(2.0 * swing_data.fps))
            launch_idx = max(0, contact_idx - int(0.5 * swing_data.fps))
            load_duration_ms = (swing_data.time_s[launch_idx] - swing_data.time_s[load_start_idx]) * 1000
            swing_duration_ms = (swing_data.time_s[contact_idx] - swing_data.time_s[launch_idx]) * 1000
            tempo_ratio = load_duration_ms / swing_duration_ms if swing_duration_ms > 0 else 0
        else:
            # CORRECT METHOD: Use lower half KE curve
            # Find load start: minimum KE in window [-2.5s, -0.5s] from contact
            load_window_start = max(0, contact_idx - int(2.5 * swing_data.fps))
            load_window_end = max(0, contact_idx - int(0.5 * swing_data.fps))
            load_window = lower_ke[load_window_start:load_window_end]
            
            if len(load_window) > 0:
                load_start_idx_rel = np.argmin(load_window)
                load_start_idx = load_window_start + load_start_idx_rel
            else:
                load_start_idx = load_window_start
            
            # Find hip peak: maximum KE in window [-1.0s, -0.1s] from contact
            hip_window_start = max(0, contact_idx - int(1.0 * swing_data.fps))
            hip_window_end = max(0, contact_idx - int(0.1 * swing_data.fps))
            hip_window = lower_ke[hip_window_start:hip_window_end]
            
            if len(hip_window) > 0:
                hip_peak_idx_rel = np.argmax(hip_window)
                hip_peak_idx = hip_window_start + hip_peak_idx_rel
            else:
                hip_peak_idx = hip_window_start
            
            # Calculate durations
            load_duration_ms = (swing_data.time_s[hip_peak_idx] - swing_data.time_s[load_start_idx]) * 1000
            swing_duration_ms = (swing_data.time_s[contact_idx] - swing_data.time_s[hip_peak_idx]) * 1000
            tempo_ratio = load_duration_ms / swing_duration_ms if swing_duration_ms > 0 else 0
        
        print(f"   Tempo (from lower half KE curve):")
        print(f"      Load Duration: {load_duration_ms:.0f} ms")
        print(f"      Swing Duration: {swing_duration_ms:.0f} ms")
        print(f"      Tempo Ratio: {tempo_ratio:.2f}:1")
        print(f"      Expected: 3.38:1 (Connor Gray ground truth)")
        
        return {
            'bat_speed_mph': bat_speed_mph,
            'peak_bat_speed_mph': peak_bat_speed_mph,
            'total_energy_j': total_ke,
            'lowerhalf_pct': lowerhalf_pct,
            'torso_pct': torso_pct,
            'arms_pct': arms_pct,
            'kinematic_sequence_ms_before_contact': {
                'pelvis': pelvis_time_before,
                'torso': torso_time_before,
                'larm': larm_time_before,
                'rarm': rarm_time_before,
                'bat': bat_time_before
            },
            'tempo_ratio_estimated': tempo_ratio,
            'load_duration_ms_estimated': load_duration_ms,
            'swing_duration_ms_estimated': swing_duration_ms
        }


def test_importer():
    """Test the importer with sample data"""
    importer = RebootCSVImporter()
    
    # Example usage
    csv_path = "/home/user/webapp/20251220_session_3_rebootmotion_ad25f0a5-d0d6-48bd-871c-f3d2a78e1576_baseball-hitting_momentum-energy.csv"
    
    if Path(csv_path).exists():
        swing_data = importer.load_momentum_energy_csv(csv_path)
        metrics = importer.calculate_ground_truth_metrics(swing_data)
        
        print("\n✅ Import and calculation successful!")
        return swing_data, metrics
    else:
        print(f"❌ File not found: {csv_path}")
        return None, None


if __name__ == "__main__":
    test_importer()
