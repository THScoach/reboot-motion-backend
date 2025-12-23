"""
Scoring Engine Module
Converts physics data into 4B Framework scores

4B Framework:
- Brain: Tempo Ratio, timing patterns
- Body: Ground Score (lower body power)
- Bat: Engine Score (torso rotation)
- Ball: Weapon Score (bat speed through zone)

Plus: Transfer Ratio (efficiency of energy transfer)
"""

import numpy as np
from typing import Dict, Optional, List
from dataclasses import dataclass
from event_detection import SwingEvents
from physics_calculator import KineticSequence, JointVelocities


@dataclass
class SwingScores:
    """Complete scoring for a swing"""
    # 4B Framework
    tempo_ratio: float          # Brain: Load/Swing timing (ideal 2.5-3.5)
    ground_score: int           # Body: Lower body power (0-100)
    engine_score: int           # Bat: Torso rotation power (0-100)
    weapon_score: int           # Ball: Bat speed through zone (0-100)
    
    # Additional metrics
    transfer_ratio: float       # Energy transfer efficiency (ideal >1.20)
    sequence_score: int         # Kinetic chain quality (0-100)
    
    # Peak velocities
    peak_pelvis_velocity: float  # deg/s
    peak_torso_velocity: float   # deg/s
    peak_bat_velocity: float     # m/s (mph when multiplied by 2.237)
    
    # Motor profile classification
    motor_profile: str          # "Rotational", "Linear", "Hybrid"
    
    def get_overall_score(self) -> int:
        """Calculate overall swing quality (0-100)"""
        return int((self.ground_score + self.engine_score + self.weapon_score) / 3)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for API response"""
        return {
            "tempo_ratio": round(self.tempo_ratio, 2),
            "ground_score": self.ground_score,
            "engine_score": self.engine_score,
            "weapon_score": self.weapon_score,
            "transfer_ratio": round(self.transfer_ratio, 2),
            "sequence_score": self.sequence_score,
            "peak_bat_velocity_mph": round(self.peak_bat_velocity * 2.237, 1),
            "peak_pelvis_velocity": round(self.peak_pelvis_velocity, 0),
            "peak_torso_velocity": round(self.peak_torso_velocity, 0),
            "motor_profile": self.motor_profile,
            "overall_score": self.get_overall_score()
        }


class ScoringEngine:
    """
    Calculate 4B Framework scores from physics data
    """
    
    # Reference values (MLB average / elite)
    REFERENCE_PELVIS_VELOCITY = 600  # deg/s
    REFERENCE_TORSO_VELOCITY = 800   # deg/s
    REFERENCE_BAT_VELOCITY = 30      # m/s (~67 mph)
    
    def __init__(self):
        """Initialize scoring engine"""
        pass
    
    def calculate_tempo_score(self, events: SwingEvents) -> float:
        """
        Calculate tempo ratio (Brain metric)
        
        Tempo Ratio = Load Duration / Swing Duration
        
        Ideal: 2.5 - 3.5
        Good: 2.0 - 4.0
        Poor: <1.5 or >5.0
        
        Args:
            events: SwingEvents
        
        Returns:
            Tempo ratio
        """
        return events.get_tempo_ratio()
    
    def calculate_ground_score(self, velocities: List[JointVelocities],
                               events: SwingEvents) -> tuple:
        """
        Calculate Ground Score (Body metric)
        Measures lower body power generation
        
        Based on:
        - Peak pelvis velocity
        - Pelvis acceleration during launch
        - Weight transfer quality
        
        Args:
            velocities: List of JointVelocities
            events: SwingEvents
        
        Returns:
            (score 0-100, peak_pelvis_velocity)
        """
        if not velocities:
            return 0, 0.0
        
        # Find peak pelvis velocity
        pelvis_vels = [abs(v.pelvis_velocity) for v in velocities]
        peak_pelvis = max(pelvis_vels) if pelvis_vels else 0
        
        # Score based on peak velocity (reference: 600 deg/s for MLB)
        # Scale: 50% of reference = 50 score, 100% = 80 score, 120% = 100 score
        score_ratio = peak_pelvis / self.REFERENCE_PELVIS_VELOCITY
        
        if score_ratio >= 1.2:
            score = 100
        elif score_ratio >= 1.0:
            score = 80 + int((score_ratio - 1.0) * 100)
        elif score_ratio >= 0.5:
            score = 50 + int((score_ratio - 0.5) * 60)
        else:
            score = int(score_ratio * 100)
        
        return min(100, max(0, score)), peak_pelvis
    
    def calculate_engine_score(self, velocities: List[JointVelocities],
                               events: SwingEvents) -> tuple:
        """
        Calculate Engine Score (Bat metric - torso rotation)
        Measures torso power generation
        
        Based on:
        - Peak torso velocity
        - Hip-shoulder separation
        - Torso acceleration
        
        Args:
            velocities: List of JointVelocities
            events: SwingEvents
        
        Returns:
            (score 0-100, peak_torso_velocity)
        """
        if not velocities:
            return 0, 0.0
        
        # Find peak torso velocity
        torso_vels = [abs(v.torso_velocity) for v in velocities]
        peak_torso = max(torso_vels) if torso_vels else 0
        
        # Score based on peak velocity (reference: 800 deg/s for MLB)
        score_ratio = peak_torso / self.REFERENCE_TORSO_VELOCITY
        
        if score_ratio >= 1.2:
            score = 100
        elif score_ratio >= 1.0:
            score = 80 + int((score_ratio - 1.0) * 100)
        elif score_ratio >= 0.5:
            score = 50 + int((score_ratio - 0.5) * 60)
        else:
            score = int(score_ratio * 100)
        
        return min(100, max(0, score)), peak_torso
    
    def calculate_weapon_score(self, velocities: List[JointVelocities],
                               events: SwingEvents) -> tuple:
        """
        Calculate Weapon Score (Ball metric - bat speed)
        Measures bat speed through contact zone
        
        Based on:
        - Peak bat velocity
        - Bat velocity at contact
        - Velocity consistency
        
        Args:
            velocities: List of JointVelocities
            events: SwingEvents
        
        Returns:
            (score 0-100, peak_bat_velocity m/s)
        """
        if not velocities:
            return 0, 0.0
        
        # Find bat velocities near contact
        contact_window = [
            v for v in velocities 
            if abs(v.timestamp_ms - events.contact_ms) < 100
        ]
        
        if not contact_window:
            contact_window = velocities[-10:]  # Last 10 frames
        
        bat_vels = [v.bat_velocity for v in contact_window]
        peak_bat = max(bat_vels) if bat_vels else 0
        
        # Score based on peak velocity (reference: 30 m/s = 67 mph for MLB)
        score_ratio = peak_bat / self.REFERENCE_BAT_VELOCITY
        
        if score_ratio >= 1.2:
            score = 100
        elif score_ratio >= 1.0:
            score = 80 + int((score_ratio - 1.0) * 100)
        elif score_ratio >= 0.5:
            score = 50 + int((score_ratio - 0.5) * 60)
        else:
            score = int(score_ratio * 100)
        
        return min(100, max(0, score)), peak_bat
    
    def calculate_transfer_ratio(self, ground_score: int, engine_score: int,
                                 weapon_score: int) -> float:
        """
        Calculate Transfer Ratio (efficiency metric)
        
        Measures how well energy transfers from:
        Ground → Engine → Weapon
        
        Perfect transfer: Each stage amplifies the previous
        Transfer Ratio = (Weapon / Ground) * efficiency_factor
        
        Elite: >1.20
        Good: 1.0 - 1.20
        Poor: <1.0
        
        Args:
            ground_score: Ground score (0-100)
            engine_score: Engine score (0-100)
            weapon_score: Weapon score (0-100)
        
        Returns:
            Transfer ratio
        """
        if ground_score == 0:
            return 0.0
        
        # Basic ratio
        base_ratio = weapon_score / ground_score
        
        # Adjust for engine contribution
        engine_factor = engine_score / 100.0
        transfer_ratio = base_ratio * (0.7 + 0.3 * engine_factor)
        
        return transfer_ratio
    
    def classify_motor_profile(self, ground_score: int, engine_score: int,
                               weapon_score: int) -> str:
        """
        Classify motor profile based on score distribution
        
        Rotational: High engine, moderate ground
        Linear: High ground, moderate engine
        Hybrid: Balanced scores
        
        Args:
            ground_score: Ground score
            engine_score: Engine score
            weapon_score: Weapon score
        
        Returns:
            Motor profile classification
        """
        ground_pct = ground_score / 100.0
        engine_pct = engine_score / 100.0
        
        diff = abs(engine_pct - ground_pct)
        
        if diff < 0.15:
            return "Hybrid"
        elif engine_pct > ground_pct:
            return "Rotational"
        else:
            return "Linear"
    
    def calculate_all_scores(self, velocities: List[JointVelocities],
                            events: SwingEvents,
                            kinetic_seq: KineticSequence) -> SwingScores:
        """
        Calculate all scores for a swing
        
        Args:
            velocities: List of JointVelocities
            events: SwingEvents
            kinetic_seq: KineticSequence
        
        Returns:
            SwingScores with all metrics
        """
        # Calculate individual scores
        tempo_ratio = self.calculate_tempo_score(events)
        ground_score, peak_pelvis = self.calculate_ground_score(velocities, events)
        engine_score, peak_torso = self.calculate_engine_score(velocities, events)
        weapon_score, peak_bat = self.calculate_weapon_score(velocities, events)
        
        # Calculate transfer ratio
        transfer_ratio = self.calculate_transfer_ratio(
            ground_score, engine_score, weapon_score
        )
        
        # Classify motor profile
        motor_profile = self.classify_motor_profile(
            ground_score, engine_score, weapon_score
        )
        
        # Kinetic sequence quality
        sequence_score = int(kinetic_seq.get_sequence_quality())
        
        return SwingScores(
            tempo_ratio=tempo_ratio,
            ground_score=ground_score,
            engine_score=engine_score,
            weapon_score=weapon_score,
            transfer_ratio=transfer_ratio,
            sequence_score=sequence_score,
            peak_pelvis_velocity=peak_pelvis,
            peak_torso_velocity=peak_torso,
            peak_bat_velocity=peak_bat,
            motor_profile=motor_profile
        )


if __name__ == "__main__":
    print("Scoring Engine Module")
    print("=" * 60)
    print("4B Framework Scores:")
    print("  - Brain: Tempo Ratio (Load/Swing timing)")
    print("  - Body: Ground Score (lower body power)")
    print("  - Bat: Engine Score (torso rotation)")
    print("  - Ball: Weapon Score (bat speed)")
    print("\nAdditional Metrics:")
    print("  - Transfer Ratio (energy transfer efficiency)")
    print("  - Sequence Score (kinetic chain quality)")
    print("  - Motor Profile (Rotational/Linear/Hybrid)")
    print("=" * 60)
