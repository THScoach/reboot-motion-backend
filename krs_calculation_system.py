"""
KRS (Kinetic Rotation Score) Calculation System
Integrated with Reboot Motion biomechanics data

This system calculates KRS scores, detects motor profiles, and prescribes drills
based on Reboot Motion inverse kinematics and momentum/energy data.
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class KRSCalculator:
    """
    Main KRS calculation engine.
    Processes Reboot Motion biomechanics data to calculate KRS scores,
    detect motor profiles, and prescribe personalized drill plans.
    """
    
    # Elite benchmarks (based on MLB/pro data)
    ELITE_BENCHMARKS = {
        'hip_rotation_velocity': 50.0,  # degrees/sec
        'torso_rotation_velocity': 8.0,  # degrees/sec (gradient-based)
        'hip_shoulder_separation': 40.0,  # degrees
        'peak_force': 1500.0,  # Newtons
        'bat_speed': 85.0,  # mph (elite high school / pro)
        'sequence_timing_optimal': 0.10,  # seconds (100ms hip-to-torso delay)
        'energy_sequence_threshold': 0.15  # seconds max for stacker profile
    }
    
    # Motor profile thresholds
    MOTOR_PROFILE_THRESHOLDS = {
        'SPINNER': {'hip_velocity': 45.0},  # degrees/sec
        'SLINGSHOTTER': {'separation': 60.0},  # degrees
        'STACKER': {'sequence_timing': 0.15},  # seconds
        'TITAN': {'total_energy': 500.0}  # Joules
    }
    
    def __init__(self, athlete_data: Optional[Dict] = None):
        """
        Initialize KRS Calculator.
        
        Args:
            athlete_data: Optional dict with height_inches, weight_lbs, wingspan_inches
        """
        self.athlete_data = athlete_data or {}
        logger.info("KRS Calculator initialized")
    
    def calculate_krs(self, reboot_data: Dict) -> Dict:
        """
        Main calculation method - processes Reboot Motion data and returns complete KRS analysis.
        
        Args:
            reboot_data: Dict containing 'ik_df' and 'me_df' (pandas DataFrames)
                        OR legacy format with kinematic_sequence, torso_kinematics, etc.
        
        Returns:
            Dict with:
                - krs_scores: {total, creation, transfer, level}
                - motor_profile: {primary, confidence, description, primary_issue, fix_focus}
                - timing_analysis: {timing_gap_ms, sequence_quality, ...}
                - drill_prescription: List of prescribed drills
                - component_scores: Detailed breakdown
        """
        logger.info("Starting KRS calculation...")
        
        # Check if we have DataFrames (new format) or dict (legacy format)
        if 'ik_df' in reboot_data and 'me_df' in reboot_data:
            # New format - use existing transformer
            from app.transformers.reboot_to_krs import RebootToKRSTransformer
            transformer = RebootToKRSTransformer()
            
            # Get external bat speed if available
            external_bat_speed = reboot_data.get('external_bat_speed_mph')
            external_bat_speed_avg = reboot_data.get('external_bat_speed_avg_mph')
            
            krs_report = transformer.transform_session(
                ik_df=reboot_data['ik_df'],
                me_df=reboot_data['me_df'],
                player_info=reboot_data.get('player_info'),
                external_bat_speed_mph=external_bat_speed,
                external_bat_speed_avg_mph=external_bat_speed_avg
            )
            
            # Convert to standard format
            return self._convert_transformer_output(krs_report)
        
        else:
            # Legacy format - extract metrics
            return self._calculate_from_legacy_format(reboot_data)
    
    def _convert_transformer_output(self, krs_report: Dict) -> Dict:
        """Convert transformer output to standard KRS format."""
        
        # Extract scores
        krs_scores = krs_report.get('krs', {})
        motor_profile = krs_report.get('motor_profile', {})
        framework = krs_report.get('framework_metrics', {})
        
        # Build motor profile description
        profile_type = motor_profile.get('type', 'BALANCED')
        profile_descriptions = {
            'Titan': {
                'description': 'Power-dominant swing with high energy generation. Strengths in raw force production.',
                'primary_issue': 'Energy transfer efficiency - generating power but not optimally transferring to bat',
                'fix_focus': 'Connection drills and sequencing work to channel force through kinetic chain'
            },
            'Spinner': {
                'description': 'Rotation-dominant swing. High hip velocity drives power through torso rotation.',
                'primary_issue': 'Early hip rotation - hips fire before hands are loaded',
                'fix_focus': 'Timing drills to delay hip firing and maintain separation'
            },
            'Slingshotter': {
                'description': 'Elastic energy dominant. Creates power through extreme hip-shoulder separation.',
                'primary_issue': 'Maintaining separation while accelerating - losing coil at launch',
                'fix_focus': 'Load retention drills and stretch-shortening cycle training'
            },
            'Stacker': {
                'description': 'Sequence-dominant. Efficient energy flow through precise timing of body segments.',
                'primary_issue': 'Speed of sequence - segments firing too slow or fast',
                'fix_focus': 'Tempo drills and segment isolation work'
            }
        }
        
        profile_info = profile_descriptions.get(profile_type, profile_descriptions['Titan'])
        
        # Calculate timing gap
        brain_metrics = framework.get('brain', {})
        timing = brain_metrics.get('timing', 0)
        time_to_contact = brain_metrics.get('time_to_contact', 0)
        timing_gap_ms = abs(timing - time_to_contact) * 1000 if time_to_contact > 0 else 0
        
        # Prescribe drills based on scores
        creation_score = krs_scores.get('creation_score', 0)
        transfer_score = krs_scores.get('transfer_score', 0)
        
        drill_prescription = self._prescribe_drills(
            creation_score=creation_score,
            transfer_score=transfer_score,
            motor_profile=profile_type,
            brain_score=brain_metrics.get('efficiency', 85),
            body_score=creation_score,
            bat_score=transfer_score
        )
        
        # Build final result
        return {
            'krs_scores': {
                'total': krs_scores.get('krs_total', 0),
                'creation': creation_score,
                'transfer': transfer_score,
                'level': krs_scores.get('krs_level', 'FOUNDATION')
            },
            'motor_profile': {
                'primary': profile_type,
                'confidence': motor_profile.get('confidence', 0),
                'description': profile_info['description'],
                'primary_issue': profile_info['primary_issue'],
                'fix_focus': profile_info['fix_focus']
            },
            'timing_analysis': {
                'timing_gap_ms': timing_gap_ms,
                'sequence_quality': 'OPTIMAL' if timing_gap_ms < 50 else 'NEEDS_WORK',
                'swing_duration': timing,
                'time_to_contact': time_to_contact
            },
            'drill_prescription': drill_prescription,
            'component_scores': {
                'brain': brain_metrics,
                'body': framework.get('body', {}),
                'bat': framework.get('bat', {}),
                'ball': framework.get('ball', {})
            },
            'on_table_gain': krs_report.get('on_table_gain', {})
        }
    
    def _calculate_from_legacy_format(self, reboot_data: Dict) -> Dict:
        """
        Calculate KRS from legacy format (for backwards compatibility).
        Expected format: kinematic_sequence, torso_kinematics, swing_posture
        """
        logger.info("Processing legacy format data...")
        
        # Extract metrics
        kinematic = reboot_data.get('kinematic_sequence', {})
        torso = reboot_data.get('torso_kinematics', {})
        posture = reboot_data.get('swing_posture', {})
        
        # Calculate creation score
        hip_velocity = kinematic.get('pelvis', {}).get('peak_velocity', 0) / 10  # Convert to deg/s
        separation = torso.get('separation', 0)
        peak_force = 1000  # Placeholder - would come from force plate data
        
        creation_score = self._calculate_creation_score_legacy(
            hip_velocity, separation, peak_force
        )
        
        # Calculate transfer score
        torso_velocity = kinematic.get('torso', {}).get('peak_velocity', 0) / 100  # Convert
        bat_speed = posture.get('bat_speed', 0)
        
        # Check sequence timing
        pelvis_timing = kinematic.get('pelvis', {}).get('peak_timing', 0)
        torso_timing = kinematic.get('torso', {}).get('peak_timing', 0)
        timing_gap_ms = abs(torso_timing - pelvis_timing) * 10  # Convert to ms
        
        transfer_score = self._calculate_transfer_score_legacy(
            torso_velocity, bat_speed, timing_gap_ms
        )
        
        # Calculate total KRS
        krs_total = (creation_score * 0.40) + (transfer_score * 0.60)
        krs_level = self._get_krs_level(krs_total)
        
        # Detect motor profile
        motor_profile = self._detect_motor_profile_legacy(
            hip_velocity, separation, timing_gap_ms, peak_force
        )
        
        # Prescribe drills
        drill_prescription = self._prescribe_drills(
            creation_score=creation_score,
            transfer_score=transfer_score,
            motor_profile=motor_profile['primary'],
            brain_score=85,  # Default
            body_score=creation_score,
            bat_score=transfer_score
        )
        
        return {
            'krs_scores': {
                'total': round(krs_total, 1),
                'creation': round(creation_score, 1),
                'transfer': round(transfer_score, 1),
                'level': krs_level
            },
            'motor_profile': motor_profile,
            'timing_analysis': {
                'timing_gap_ms': timing_gap_ms,
                'sequence_quality': 'OPTIMAL' if timing_gap_ms < 50 else 'NEEDS_WORK'
            },
            'drill_prescription': drill_prescription,
            'component_scores': {
                'hip_velocity': hip_velocity,
                'separation': separation,
                'torso_velocity': torso_velocity,
                'bat_speed': bat_speed
            }
        }
    
    def _calculate_creation_score_legacy(self, hip_velocity: float, separation: float, peak_force: float) -> float:
        """Calculate creation score from individual components."""
        # Hip velocity score (0-100)
        hip_score = min(100, (hip_velocity / self.ELITE_BENCHMARKS['hip_rotation_velocity']) * 100)
        
        # Separation score (0-100)
        sep_score = min(100, (separation / self.ELITE_BENCHMARKS['hip_shoulder_separation']) * 100)
        
        # Force score (0-100)
        force_score = min(100, (peak_force / self.ELITE_BENCHMARKS['peak_force']) * 100)
        
        # Weighted combination
        creation = (0.40 * hip_score) + (0.30 * sep_score) + (0.30 * force_score)
        return max(0, min(100, creation))
    
    def _calculate_transfer_score_legacy(self, torso_velocity: float, bat_speed: float, timing_gap_ms: float) -> float:
        """Calculate transfer score from individual components."""
        # Torso velocity score
        torso_score = min(100, (torso_velocity / self.ELITE_BENCHMARKS['torso_rotation_velocity']) * 100)
        
        # Bat speed score
        bat_score = min(100, (bat_speed / self.ELITE_BENCHMARKS['bat_speed']) * 100)
        
        # Sequence timing score (optimal at 100ms)
        if timing_gap_ms < 50:
            timing_score = 70  # Too fast
        elif timing_gap_ms > 150:
            timing_score = 70  # Too slow
        else:
            timing_score = 100  # Optimal
        
        # Weighted combination
        transfer = (0.35 * torso_score) + (0.35 * timing_score) + (0.30 * bat_score)
        return max(0, min(100, transfer))
    
    def _detect_motor_profile_legacy(self, hip_velocity: float, separation: float, 
                                    timing_gap_ms: float, peak_force: float) -> Dict:
        """Detect motor profile from metrics."""
        profiles = []
        
        # Check each profile
        if hip_velocity > self.MOTOR_PROFILE_THRESHOLDS['SPINNER']['hip_velocity']:
            profiles.append(('Spinner', 100))
        
        if separation > self.MOTOR_PROFILE_THRESHOLDS['SLINGSHOTTER']['separation']:
            profiles.append(('Slingshotter', 100))
        
        if timing_gap_ms < (self.MOTOR_PROFILE_THRESHOLDS['STACKER']['sequence_timing'] * 1000):
            profiles.append(('Stacker', 100))
        
        if peak_force > self.MOTOR_PROFILE_THRESHOLDS['TITAN']['total_energy']:
            profiles.append(('Titan', 100))
        
        # Default to primary
        if not profiles:
            primary_profile = 'Titan'
            confidence = 75
        else:
            primary_profile = profiles[0][0]
            confidence = profiles[0][1]
        
        profile_descriptions = {
            'Titan': {
                'description': 'Power-dominant swing with high energy generation',
                'primary_issue': 'Energy transfer efficiency',
                'fix_focus': 'Connection drills and sequencing'
            },
            'Spinner': {
                'description': 'Rotation-dominant swing with high hip velocity',
                'primary_issue': 'Early hip rotation',
                'fix_focus': 'Timing drills to delay hip firing'
            },
            'Slingshotter': {
                'description': 'Elastic energy dominant with extreme separation',
                'primary_issue': 'Maintaining separation at launch',
                'fix_focus': 'Load retention drills'
            },
            'Stacker': {
                'description': 'Sequence-dominant with efficient energy flow',
                'primary_issue': 'Speed of sequence timing',
                'fix_focus': 'Tempo drills and segment isolation'
            }
        }
        
        profile_info = profile_descriptions.get(primary_profile, profile_descriptions['Titan'])
        
        return {
            'primary': primary_profile,
            'confidence': confidence,
            'description': profile_info['description'],
            'primary_issue': profile_info['primary_issue'],
            'fix_focus': profile_info['fix_focus']
        }
    
    def _prescribe_drills(self, creation_score: float, transfer_score: float, 
                         motor_profile: str, brain_score: float, 
                         body_score: float, bat_score: float) -> List[Dict]:
        """
        Prescribe drills based on KRS scores and motor profile.
        """
        prescriptions = []
        
        # BRAIN SCORE < 75: Timing Issues
        if brain_score < 75:
            prescriptions.append({
                'drill_id': 1,
                'name': 'Rope Rhythm Control',
                'tool': 'Quan Ropes',
                'goal': f'Improve timing/sequencing (Brain Score: {brain_score:.0f}/100)',
                'priority': 1,
                'weeks': 2,
                'duration_min': 5,
                'frequency': 'Daily warmup'
            })
            
            if motor_profile in ['Spinner', 'Slingshotter']:
                prescriptions.append({
                    'drill_id': 2,
                    'name': 'Synapse Stride Delay',
                    'tool': 'Synapse CCR',
                    'goal': f'Control early hip rotation ({motor_profile} profile)',
                    'priority': 2,
                    'weeks': 4,
                    'duration_min': 15,
                    'frequency': '3x per week'
                })
        
        # BODY SCORE < 75: Force Generation
        if body_score < 75:
            prescriptions.append({
                'drill_id': 4,
                'name': 'Synapse Hip Load & Fire',
                'tool': 'Synapse CCR',
                'goal': f'Build force creation (Body Score: {body_score:.0f}/100)',
                'priority': 2,
                'weeks': 4,
                'duration_min': 20,
                'frequency': '3x per week'
            })
        
        # BAT SCORE < 75: Transfer Issues
        if bat_score < 75:
            if motor_profile == 'Spinner':
                prescriptions.append({
                    'drill_id': 7,
                    'name': 'Synapse Connection Lock',
                    'tool': 'Synapse CCR',
                    'goal': f'Fix disconnection (Spinner with {bat_score:.0f}/100 transfer)',
                    'priority': 1,
                    'weeks': 4,
                    'duration_min': 20,
                    'frequency': '4x per week'
                })
            else:
                prescriptions.append({
                    'drill_id': 7,
                    'name': 'Synapse Connection Lock',
                    'tool': 'Synapse CCR',
                    'goal': f'Improve transfer efficiency ({bat_score:.0f}/100)',
                    'priority': 2,
                    'weeks': 3,
                    'duration_min': 15,
                    'frequency': '3x per week'
                })
        
        # Sort by priority and limit to top 5
        prescriptions.sort(key=lambda x: x['priority'])
        return prescriptions[:5]
    
    def _get_krs_level(self, krs_total: float) -> str:
        """Map KRS score to level."""
        if krs_total >= 80:
            return "ELITE"
        elif krs_total >= 60:
            return "DEVELOPING"
        else:
            return "FOUNDATION"


# Example usage
if __name__ == "__main__":
    # Eric Williams test case
    print("=" * 80)
    print("KRS CALCULATOR - ERIC WILLIAMS TEST CASE")
    print("=" * 80)
    
    # Initialize calculator
    athlete_data = {
        'height_inches': 72,
        'weight_lbs': 185,
        'wingspan_inches': 74
    }
    
    calculator = KRSCalculator(athlete_data)
    
    # Simulate Reboot Motion data (legacy format)
    reboot_data_legacy = {
        'kinematic_sequence': {
            'pelvis': {'peak_velocity': 425.7, 'peak_timing': 98.5},
            'torso': {'peak_velocity': 738.9, 'peak_timing': 98.8}
        },
        'torso_kinematics': {
            'pelvis_rotation': 42,
            'torso_rotation': 80,
            'separation': 38
        },
        'swing_posture': {
            'bat_speed': 82
        }
    }
    
    # Calculate KRS
    results = calculator.calculate_krs(reboot_data_legacy)
    
    # Print results
    print(f"\n📊 KRS SCORES:")
    print(f"   Total: {results['krs_scores']['total']}/100 ({results['krs_scores']['level']})")
    print(f"   Creation: {results['krs_scores']['creation']}/100")
    print(f"   Transfer: {results['krs_scores']['transfer']}/100")
    
    print(f"\n🎯 MOTOR PROFILE:")
    print(f"   Type: {results['motor_profile']['primary']} ({results['motor_profile']['confidence']}%)")
    print(f"   Description: {results['motor_profile']['description']}")
    print(f"   Primary Issue: {results['motor_profile']['primary_issue']}")
    print(f"   Fix Focus: {results['motor_profile']['fix_focus']}")
    
    print(f"\n💊 PRESCRIBED DRILLS:")
    for i, drill in enumerate(results['drill_prescription'], 1):
        print(f"   {i}. {drill['name']} ({drill['tool']})")
        print(f"      Goal: {drill['goal']}")
        print(f"      {drill['duration_min']} min, {drill['frequency']} for {drill['weeks']} weeks")
    
    print("\n" + "=" * 80)

