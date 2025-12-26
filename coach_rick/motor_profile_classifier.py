"""
Motor Profile Classifier
========================

Classifies players into motor profiles based on swing mechanics:
- Spinner: Rotational dominance
- Whipper: Late acceleration dominance
- Torquer: Ground force dominance

Author: Builder 2
Date: 2024-12-24
"""

from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class MotorProfileResult:
    """Motor profile classification result"""
    profile: str  # "Spinner", "Whipper", "Torquer", "Mixed"
    confidence: float  # 0.0 - 1.0
    characteristics: List[str]
    metrics_used: Dict[str, float]


class MotorProfileClassifier:
    """
    Classifies players into motor profiles based on biomechanical data.
    
    Profiles:
    - SPINNER: Rotational power generation, moderate timing gaps
    - WHIPPER: Elite hip-shoulder separation, explosive late acceleration
    - TORQUER: Ground force dominance, fast compact swing
    - MIXED: Combination of patterns, no dominant power source
    """
    
    def __init__(self):
        """Initialize classifier"""
        pass
    
    def classify(self, swing_data: Dict) -> MotorProfileResult:
        """
        Classify player motor profile.
        
        Args:
            swing_data: Dictionary with kinematic_sequence, tempo, stability, bat_speed
        
        Returns:
            MotorProfileResult with classification
        """
        # Extract metrics
        kinematic_seq = swing_data.get('kinematic_sequence', {})
        tempo = swing_data.get('tempo', {})
        stability = swing_data.get('stability', {})
        
        # Calculate key metrics
        hip_shoulder_gap = self._calculate_hip_shoulder_gap(kinematic_seq)
        hands_bat_gap = self._calculate_hands_bat_gap(kinematic_seq)
        tempo_ratio = tempo.get('ratio', 0)
        stability_score = stability.get('score', 0)
        
        metrics = {
            'hip_shoulder_gap_ms': hip_shoulder_gap,
            'hands_bat_gap_ms': hands_bat_gap,
            'tempo_ratio': tempo_ratio,
            'stability_score': stability_score
        }
        
        # Classification logic
        
        # SPINNER: Rotational dominance
        if (hip_shoulder_gap < 25 and 
            hands_bat_gap < 20 and 
            tempo_ratio >= 1.8 and tempo_ratio <= 2.5):
            return MotorProfileResult(
                profile="Spinner",
                confidence=0.85,
                characteristics=[
                    "Rotational power generation",
                    "Moderate timing gaps",
                    "Risk: Can pull across pitch plane",
                    "Strength: Consistent barrel path"
                ],
                metrics_used=metrics
            )
        
        # WHIPPER: Late acceleration dominance
        elif (hip_shoulder_gap >= 25 and 
              hands_bat_gap >= 20 and 
              tempo_ratio >= 2.0):
            return MotorProfileResult(
                profile="Whipper",
                confidence=0.90,
                characteristics=[
                    "Elite hip-shoulder separation",
                    "Explosive late bat acceleration",
                    "Risk: Can disconnect if too quick",
                    "Strength: Plus bat speed potential"
                ],
                metrics_used=metrics
            )
        
        # TORQUER: Ground force dominance
        elif (tempo_ratio < 1.8 and 
              stability_score > 85):
            return MotorProfileResult(
                profile="Torquer",
                confidence=0.80,
                characteristics=[
                    "Ground force dominance",
                    "Fast, compact swing",
                    "Risk: Can rush if too fast",
                    "Strength: Quick hands, adjustability"
                ],
                metrics_used=metrics
            )
        
        # MIXED: No clear dominant pattern
        else:
            return MotorProfileResult(
                profile="Mixed",
                confidence=0.60,
                characteristics=[
                    "Combination of movement patterns",
                    "No dominant power source yet",
                    "Opportunity to develop defined profile"
                ],
                metrics_used=metrics
            )
    
    def _calculate_hip_shoulder_gap(self, kinematic_seq: Dict) -> float:
        """
        Calculate time gap between hip and shoulder peaks (ms).
        """
        hips_peak = kinematic_seq.get('torso_peak_ms', 0)  # Use torso as proxy for hips
        shoulders_peak = kinematic_seq.get('arms_peak_ms', 0)  # Use arms as proxy for shoulders
        
        # If we have more specific data
        if 'hips_peak_time' in kinematic_seq and 'shoulders_peak_time' in kinematic_seq:
            hips_peak = kinematic_seq['hips_peak_time']
            shoulders_peak = kinematic_seq['shoulders_peak_time']
        
        return abs(shoulders_peak - hips_peak)
    
    def _calculate_hands_bat_gap(self, kinematic_seq: Dict) -> float:
        """
        Calculate time gap between hands and bat peaks (ms).
        """
        hands_peak = kinematic_seq.get('arms_peak_ms', 0)
        bat_peak = kinematic_seq.get('bat_peak_ms', 0)
        
        # If we have more specific data
        if 'hands_peak_time' in kinematic_seq and 'bat_peak_time' in kinematic_seq:
            hands_peak = kinematic_seq['hands_peak_time']
            bat_peak = kinematic_seq['bat_peak_time']
        
        return abs(bat_peak - hands_peak)


def classify_motor_profile(swing_data: Dict) -> MotorProfileResult:
    """
    Convenience function to classify motor profile.
    
    Args:
        swing_data: Dictionary with swing analysis data
    
    Returns:
        MotorProfileResult
    
    Example:
        >>> swing_data = {
        ...     "kinematic_sequence": {
        ...         "torso_peak_ms": 145,
        ...         "arms_peak_ms": 165
        ...     },
        ...     "tempo": {"ratio": 2.1},
        ...     "stability": {"score": 92}
        ... }
        >>> result = classify_motor_profile(swing_data)
        >>> print(result.profile)
        'Spinner'
    """
    classifier = MotorProfileClassifier()
    return classifier.classify(swing_data)


# Example usage and testing
if __name__ == "__main__":
    # Test case 1: Spinner
    spinner_data = {
        "kinematic_sequence": {
            "torso_peak_ms": 145,
            "arms_peak_ms": 165,
            "bat_peak_ms": 180
        },
        "tempo": {"ratio": 2.1},
        "stability": {"score": 92},
        "bat_speed": 82
    }
    
    result = classify_motor_profile(spinner_data)
    print("=" * 60)
    print("SPINNER TEST")
    print("=" * 60)
    print(f"Profile: {result.profile}")
    print(f"Confidence: {result.confidence:.1%}")
    print(f"Characteristics:")
    for char in result.characteristics:
        print(f"  - {char}")
    print(f"Metrics: {result.metrics_used}")
    print()
    
    # Test case 2: Whipper
    whipper_data = {
        "kinematic_sequence": {
            "torso_peak_ms": 140,
            "arms_peak_ms": 175,
            "bat_peak_ms": 200
        },
        "tempo": {"ratio": 2.8},
        "stability": {"score": 88},
        "bat_speed": 85
    }
    
    result = classify_motor_profile(whipper_data)
    print("=" * 60)
    print("WHIPPER TEST")
    print("=" * 60)
    print(f"Profile: {result.profile}")
    print(f"Confidence: {result.confidence:.1%}")
    print(f"Characteristics:")
    for char in result.characteristics:
        print(f"  - {char}")
    print(f"Metrics: {result.metrics_used}")
    print()
    
    # Test case 3: Torquer
    torquer_data = {
        "kinematic_sequence": {
            "torso_peak_ms": 150,
            "arms_peak_ms": 160,
            "bat_peak_ms": 170
        },
        "tempo": {"ratio": 1.5},
        "stability": {"score": 94},
        "bat_speed": 80
    }
    
    result = classify_motor_profile(torquer_data)
    print("=" * 60)
    print("TORQUER TEST")
    print("=" * 60)
    print(f"Profile: {result.profile}")
    print(f"Confidence: {result.confidence:.1%}")
    print(f"Characteristics:")
    for char in result.characteristics:
        print(f"  - {char}")
    print(f"Metrics: {result.metrics_used}")
