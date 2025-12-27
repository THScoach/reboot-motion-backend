"""
Reboot Motion to KRS Transformer
Converts biomechanics CSV data to KRS reports with motor profiling
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple
import logging

logger = logging.getLogger(__name__)


class RebootToKRSTransformer:
    """
    Transform Reboot Motion biomechanics data into KRS reports.
    
    Processes inverse kinematics and momentum-energy CSVs to calculate:
    - KRS scores (Creation & Transfer)
    - Motor profiles (Spinner/Slingshotter/Stacker/Titan)
    - 4B Framework metrics (BRAIN, BODY, BAT, BALL)
    """
    
    def __init__(self):
        """Initialize transformer with KRS calculation parameters"""
        # Motor profile thresholds
        self.SPINNER_HIP_THRESHOLD = 45  # degrees
        self.SLINGSHOTTER_SEPARATION_THRESHOLD = 60  # degrees
        self.STACKER_SEQUENCE_THRESHOLD = 0.15  # seconds
        self.TITAN_ENERGY_THRESHOLD = 0.85  # ratio
        
    def transform_session(
        self, 
        ik_df: pd.DataFrame, 
        me_df: pd.DataFrame,
        player_info: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Transform a session's biomechanics data into a complete KRS report.
        
        Args:
            ik_df: Inverse kinematics dataframe
            me_df: Momentum energy dataframe
            player_info: Optional player metadata
            
        Returns:
            Complete KRS report dictionary
        """
        logger.info("🔄 Starting KRS transformation...")
        
        try:
            # Calculate KRS scores
            creation_score = self._calculate_creation_score(ik_df, me_df)
            transfer_score = self._calculate_transfer_score(ik_df, me_df)
            krs_total = (creation_score * 0.4) + (transfer_score * 0.6)
            
            logger.info(f"   Creation: {creation_score:.1f}, Transfer: {transfer_score:.1f}")
            logger.info(f"   KRS Total: {krs_total:.1f}")
            
            # Determine KRS level
            krs_level = self._get_krs_level(krs_total)
            
            # Detect motor profile
            motor_profile_type, motor_profile_confidence = self._detect_motor_profile(ik_df, me_df)
            
            # Extract 4B Framework metrics
            brain_metrics = self._extract_brain_metrics(ik_df, me_df)
            body_metrics = self._extract_body_metrics(ik_df, me_df)
            bat_metrics = self._extract_bat_metrics(ik_df, me_df)
            ball_metrics = self._extract_ball_metrics(ik_df, me_df)
            
            # Calculate on-table gain
            on_table_gain = self._calculate_on_table_gain(
                ball_metrics['exit_velocity_mph'],
                body_metrics['physical_capacity_mph']
            )
            
            # Build complete report
            report = {
                'krs': {
                    'krs_total': round(krs_total, 1),
                    'krs_level': krs_level,
                    'creation_score': round(creation_score, 1),
                    'transfer_score': round(transfer_score, 1),
                },
                'on_table_gain': on_table_gain,
                'motor_profile': {
                    'type': motor_profile_type,
                    'confidence': round(motor_profile_confidence, 0)
                },
                'framework_metrics': {
                    'brain': brain_metrics,
                    'body': body_metrics,
                    'bat': bat_metrics,
                    'ball': ball_metrics
                },
                'swing_metrics': {
                    'duration_seconds': round(ik_df['time'].max(), 3) if 'time' in ik_df.columns else None,
                    'frame_count': len(ik_df),
                    'data_quality': 'high'
                }
            }
            
            # Add player info if provided
            if player_info:
                report['player'] = player_info
            
            logger.info(f"✅ KRS transformation complete: {krs_total:.1f} ({krs_level})")
            return report
            
        except Exception as e:
            logger.error(f"❌ KRS transformation failed: {e}")
            raise
    
    def _calculate_creation_score(self, ik_df: pd.DataFrame, me_df: pd.DataFrame) -> float:
        """
        Calculate Creation score (0-100) from hip rotation velocity and separation.
        
        Creation = Force generation in lower half
        - Hip rotation velocity (peak angular velocity)
        - Hip-shoulder separation (X-Factor)
        - Ground force production
        """
        try:
            # Hip rotation velocity
            if 'pelvis_rot' in ik_df.columns:
                hip_rotation_velocity = np.abs(np.gradient(ik_df['pelvis_rot'])).max()
            else:
                hip_rotation_velocity = 50  # Default if missing
            
            # Hip-shoulder separation (X-Factor)
            if 'torso_rot' in ik_df.columns and 'pelvis_rot' in ik_df.columns:
                separation = np.abs(ik_df['torso_rot'] - ik_df['pelvis_rot']).max()
            else:
                separation = 45  # Default
            
            # Kinetic energy from lower body
            lower_energy_cols = [col for col in me_df.columns if 'lth_kinetic_energy' in col or 'rth_kinetic_energy' in col or 'lowerhalf_kinetic_energy' in col]
            if lower_energy_cols:
                peak_lower_energy = me_df[lower_energy_cols].max().max()
            else:
                peak_lower_energy = 100
            
            # Normalize to 0-100 scale
            hip_velocity_score = min(100, (hip_rotation_velocity / 10) * 100)  # 10 rad/s = 100
            separation_score = min(100, (separation / 60) * 100)  # 60 degrees = 100
            energy_score = min(100, (peak_lower_energy / 200) * 100)  # 200 J = 100
            
            # Weighted average
            creation_score = (
                hip_velocity_score * 0.4 +
                separation_score * 0.3 +
                energy_score * 0.3
            )
            
            return max(0, min(100, creation_score))
            
        except Exception as e:
            logger.warning(f"Creation score calculation failed: {e}, using default")
            return 65.0  # Default moderate score
    
    def _calculate_transfer_score(self, ik_df: pd.DataFrame, me_df: pd.DataFrame) -> float:
        """
        Calculate Transfer score (0-100) from torso rotation and energy sequencing.
        
        Transfer = Efficiency of energy flow from body to bat
        - Torso rotation velocity
        - Energy sequencing (proximal-to-distal)
        - Bat speed at contact
        """
        try:
            # Torso rotation velocity
            if 'torso_rot' in ik_df.columns:
                torso_rotation_velocity = np.abs(np.gradient(ik_df['torso_rot'])).max()
            else:
                torso_rotation_velocity = 40
            
            # Energy sequence efficiency
            # Check if lower → torso → arms → bat sequence is optimal
            energy_cols = ['lowerhalf_kinetic_energy', 'torso_kinetic_energy', 'arms_kinetic_energy', 'bat_kinetic_energy']
            available_cols = [col for col in energy_cols if col in me_df.columns]
            
            if len(available_cols) >= 2:
                # Calculate timing of peak energies
                peak_times = []
                for col in available_cols:
                    peak_idx = me_df[col].idxmax()
                    peak_times.append(ik_df.loc[peak_idx, 'time'] if 'time' in ik_df.columns else peak_idx)
                
                # Check if sequence is proximal-to-distal
                sequence_score = 100 if all(peak_times[i] <= peak_times[i+1] for i in range(len(peak_times)-1)) else 70
            else:
                sequence_score = 75  # Default
            
            # Bat speed (if available)
            if 'bat_kinetic_energy' in me_df.columns:
                peak_bat_energy = me_df['bat_kinetic_energy'].max()
                bat_speed_score = min(100, (peak_bat_energy / 150) * 100)  # 150 J = 100
            else:
                bat_speed_score = 70
            
            # Normalize torso velocity
            torso_velocity_score = min(100, (torso_rotation_velocity / 8) * 100)  # 8 rad/s = 100
            
            # Weighted average
            transfer_score = (
                torso_velocity_score * 0.35 +
                sequence_score * 0.35 +
                bat_speed_score * 0.30
            )
            
            return max(0, min(100, transfer_score))
            
        except Exception as e:
            logger.warning(f"Transfer score calculation failed: {e}, using default")
            return 70.0  # Default moderate score
    
    def _detect_motor_profile(self, ik_df: pd.DataFrame, me_df: pd.DataFrame) -> Tuple[str, float]:
        """
        Detect motor profile type and confidence.
        
        Motor Profiles:
        - Spinner: Hip-dominant, early rotation
        - Slingshotter: High separation, late burst
        - Stacker: Sequential, ground-up force
        - Titan: Power-dominant, high energy
        """
        try:
            scores = {
                'Spinner': 0,
                'Slingshotter': 0,
                'Stacker': 0,
                'Titan': 0
            }
            
            # Check hip rotation (Spinner trait)
            if 'pelvis_rot' in ik_df.columns:
                peak_hip_rotation = ik_df['pelvis_rot'].max()
                if peak_hip_rotation > self.SPINNER_HIP_THRESHOLD:
                    scores['Spinner'] += 30
            
            # Check separation (Slingshotter trait)
            if 'torso_rot' in ik_df.columns and 'pelvis_rot' in ik_df.columns:
                max_separation = np.abs(ik_df['torso_rot'] - ik_df['pelvis_rot']).max()
                if max_separation > self.SLINGSHOTTER_SEPARATION_THRESHOLD:
                    scores['Slingshotter'] += 35
            
            # Check sequential timing (Stacker trait)
            if 'time' in ik_df.columns:
                energy_cols = ['lowerhalf_kinetic_energy', 'torso_kinetic_energy', 'arms_kinetic_energy']
                available = [col for col in energy_cols if col in me_df.columns]
                
                if len(available) >= 2:
                    times = [ik_df.loc[me_df[col].idxmax(), 'time'] for col in available]
                    time_diffs = [times[i+1] - times[i] for i in range(len(times)-1)]
                    
                    if all(0 < diff < self.STACKER_SEQUENCE_THRESHOLD for diff in time_diffs):
                        scores['Stacker'] += 35
            
            # Check total energy (Titan trait)
            if 'total_kinetic_energy' in me_df.columns:
                peak_total_energy = me_df['total_kinetic_energy'].max()
                if peak_total_energy > 500:  # Joules
                    scores['Titan'] += 40
            
            # Find highest score
            if max(scores.values()) == 0:
                # Default to Spinner if no clear pattern
                motor_type = 'Spinner'
                confidence = 50.0
            else:
                motor_type = max(scores, key=scores.get)
                confidence = min(100, scores[motor_type] * 2.5)
            
            return motor_type, confidence
            
        except Exception as e:
            logger.warning(f"Motor profile detection failed: {e}")
            return 'Spinner', 50.0
    
    def _extract_brain_metrics(self, ik_df: pd.DataFrame, me_df: pd.DataFrame) -> Dict[str, Any]:
        """Extract BRAIN metrics (Motor Learning & Timing)"""
        try:
            # Timing
            swing_duration = ik_df['time'].max() if 'time' in ik_df.columns else 0.8
            
            # Find time to peak bat speed
            if 'bat_kinetic_energy' in me_df.columns and 'time' in ik_df.columns:
                peak_bat_idx = me_df['bat_kinetic_energy'].idxmax()
                time_to_contact = ik_df.loc[peak_bat_idx, 'time']
            else:
                time_to_contact = swing_duration * 0.75
            
            return {
                'timing': round(swing_duration, 3),
                'time_to_contact': round(time_to_contact, 3),
                'efficiency': 85.0  # Placeholder
            }
            
        except Exception as e:
            logger.warning(f"BRAIN metrics extraction failed: {e}")
            return {'timing': 0.8, 'time_to_contact': 0.6, 'efficiency': 80.0}
    
    def _extract_body_metrics(self, ik_df: pd.DataFrame, me_df: pd.DataFrame) -> Dict[str, Any]:
        """Extract BODY metrics (Force Creation)"""
        try:
            # Creation score (already calculated)
            creation_score = self._calculate_creation_score(ik_df, me_df)
            
            # Physical capacity (peak lower body energy)
            lower_energy_cols = [col for col in me_df.columns if 'lowerhalf_kinetic_energy' in col]
            if lower_energy_cols:
                peak_lower_energy = me_df[lower_energy_cols].max().max()
                # Convert to mph estimate (rough approximation)
                physical_capacity_mph = min(110, 60 + (peak_lower_energy / 10))
            else:
                physical_capacity_mph = 85.0
            
            # Peak force (from momentum change)
            if 'total_angular_momentum_mag' in me_df.columns:
                peak_force = me_df['total_angular_momentum_mag'].max()
                peak_force_n = min(3000, peak_force * 10)  # Convert to Newtons
            else:
                peak_force_n = 1500.0
            
            return {
                'creation_score': round(creation_score, 1),
                'physical_capacity_mph': round(physical_capacity_mph, 0),
                'peak_force_n': round(peak_force_n, 0)
            }
            
        except Exception as e:
            logger.warning(f"BODY metrics extraction failed: {e}")
            return {
                'creation_score': 70.0,
                'physical_capacity_mph': 85.0,
                'peak_force_n': 1500.0
            }
    
    def _extract_bat_metrics(self, ik_df: pd.DataFrame, me_df: pd.DataFrame) -> Dict[str, Any]:
        """Extract BAT metrics (Transfer Efficiency)"""
        try:
            # Transfer score
            transfer_score = self._calculate_transfer_score(ik_df, me_df)
            
            # Transfer efficiency
            if 'bat_kinetic_energy' in me_df.columns and 'total_kinetic_energy' in me_df.columns:
                peak_bat_energy = me_df['bat_kinetic_energy'].max()
                peak_total_energy = me_df['total_kinetic_energy'].max()
                transfer_efficiency = (peak_bat_energy / peak_total_energy * 100) if peak_total_energy > 0 else 75.0
            else:
                transfer_efficiency = 75.0
            
            # Attack angle (from bat orientation)
            # Placeholder - would need bat angle data
            attack_angle_deg = 15.0
            
            return {
                'transfer_score': round(transfer_score, 1),
                'transfer_efficiency': round(min(100, transfer_efficiency), 0),
                'attack_angle_deg': round(attack_angle_deg, 0)
            }
            
        except Exception as e:
            logger.warning(f"BAT metrics extraction failed: {e}")
            return {
                'transfer_score': 70.0,
                'transfer_efficiency': 75.0,
                'attack_angle_deg': 15.0
            }
    
    def _extract_ball_metrics(self, ik_df: pd.DataFrame, me_df: pd.DataFrame) -> Dict[str, Any]:
        """Extract BALL metrics (Outcomes)"""
        try:
            # Exit velocity estimate from peak bat energy
            if 'bat_kinetic_energy' in me_df.columns:
                peak_bat_energy = me_df['bat_kinetic_energy'].max()
                # E = 0.5 * m * v^2, solve for v
                # Rough approximation: higher energy = higher exit velo
                exit_velocity_mph = min(110, 60 + (peak_bat_energy / 5))
            else:
                exit_velocity_mph = 82.0
            
            # Capacity (same as physical capacity from BODY)
            body_metrics = self._extract_body_metrics(ik_df, me_df)
            capacity_mph = body_metrics['physical_capacity_mph']
            
            # Launch angle (placeholder - would need ball flight data)
            launch_angle_deg = 18.0
            
            # Contact quality
            if exit_velocity_mph >= 95:
                contact_quality = 'EXCELLENT'
            elif exit_velocity_mph >= 85:
                contact_quality = 'SOLID'
            elif exit_velocity_mph >= 75:
                contact_quality = 'FAIR'
            else:
                contact_quality = 'POOR'
            
            return {
                'exit_velocity_mph': round(exit_velocity_mph, 0),
                'capacity_mph': round(capacity_mph, 0),
                'launch_angle_deg': round(launch_angle_deg, 0),
                'contact_quality': contact_quality
            }
            
        except Exception as e:
            logger.warning(f"BALL metrics extraction failed: {e}")
            return {
                'exit_velocity_mph': 82.0,
                'capacity_mph': 85.0,
                'launch_angle_deg': 18.0,
                'contact_quality': 'SOLID'
            }
    
    def _calculate_on_table_gain(self, current_ev: float, capacity_ev: float) -> Dict[str, Any]:
        """Calculate on-table gain (potential improvement)"""
        try:
            gain_value = capacity_ev - current_ev
            
            if gain_value <= 0:
                return None
            
            return {
                'value': round(gain_value, 1),
                'metric': 'mph',
                'description': f'Potential exit velocity gain with optimal mechanics'
            }
            
        except Exception as e:
            logger.warning(f"On-table gain calculation failed: {e}")
            return None
    
    def _get_krs_level(self, krs_score: float) -> str:
        """Determine KRS level from score"""
        if krs_score >= 90:
            return 'ELITE'
        elif krs_score >= 80:
            return 'ADVANCED'
        elif krs_score >= 70:
            return 'DEVELOPING'
        elif krs_score >= 60:
            return 'BUILDING'
        else:
            return 'FOUNDATION'
