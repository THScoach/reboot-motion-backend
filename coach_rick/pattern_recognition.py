"""
Pattern Recognition Engine
===========================

Identifies specific mechanical issues based on motor profile and swing metrics.

Uses rule-based pattern matching to diagnose:
- Spinner-specific patterns
- Whipper-specific patterns
- Torquer-specific patterns
- Universal patterns (any motor profile)

Author: Builder 2
Date: 2024-12-24
"""

from typing import Dict, List, Optional
from dataclasses import dataclass

try:
    from .knowledge_base import PATTERN_RULES
except ImportError:
    from knowledge_base import PATTERN_RULES


@dataclass
class PatternMatch:
    """A matched pattern/issue"""
    pattern_id: str
    diagnosis: str
    symptoms: List[str]
    root_cause: str
    priority: str  # HIGH, MEDIUM, LOW
    confidence: float = 1.0


class PatternRecognitionEngine:
    """
    Pattern recognition engine for diagnosing mechanical issues.
    
    Uses rule-based pattern matching against PATTERN_RULES from knowledge base.
    """
    
    def __init__(self):
        """Initialize pattern recognition engine"""
        self.rules = PATTERN_RULES
        self.priority_order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    
    def analyze(self, swing_data: Dict, motor_profile: str) -> List[PatternMatch]:
        """
        Analyze swing data and identify patterns.
        
        Args:
            swing_data: Dictionary with swing analysis data
            motor_profile: Motor profile (Spinner, Whipper, Torquer, Mixed)
        
        Returns:
            List of PatternMatch objects, sorted by priority
        """
        matched_patterns = []
        
        for pattern_id, pattern_rule in self.rules.items():
            if self._matches_conditions(swing_data, motor_profile, pattern_rule['conditions']):
                matched_patterns.append(PatternMatch(
                    pattern_id=pattern_id,
                    diagnosis=pattern_rule['diagnosis'],
                    symptoms=pattern_rule['symptoms'],
                    root_cause=pattern_rule['root_cause'],
                    priority=pattern_rule['priority'],
                    confidence=1.0  # TODO: Calculate confidence based on how well conditions match
                ))
        
        # Sort by priority (HIGH > MEDIUM > LOW)
        matched_patterns.sort(key=lambda x: self.priority_order[x.priority])
        
        return matched_patterns
    
    def _matches_conditions(self, swing_data: Dict, motor_profile: str, conditions: Dict) -> bool:
        """
        Check if swing data matches pattern conditions.
        
        Args:
            swing_data: Swing analysis data
            motor_profile: Motor profile string
            conditions: Condition rules to check
        
        Returns:
            True if all conditions match
        """
        # Check motor profile
        if 'motor_profile' in conditions:
            if motor_profile != conditions['motor_profile']:
                return False
        
        # Check each metric constraint
        for metric, constraint in conditions.items():
            if metric == 'motor_profile':
                continue
            
            value = self._get_metric_value(swing_data, metric)
            
            if value is None:
                # Metric not available, skip this condition
                continue
            
            if isinstance(constraint, dict):
                # Range constraint (min/max)
                if 'min' in constraint and value < constraint['min']:
                    return False
                if 'max' in constraint and value > constraint['max']:
                    return False
            elif isinstance(constraint, list):
                # List constraint (value must be in list)
                if value not in constraint:
                    return False
        
        return True
    
    def _get_metric_value(self, swing_data: Dict, metric: str) -> Optional[float]:
        """
        Get metric value from swing data.
        
        Handles nested keys like 'tempo.ratio' or 'stability.score'.
        Also handles special computed metrics like 'hip_shoulder_gap_ms'.
        
        Args:
            swing_data: Swing analysis data
            metric: Metric name (can be nested with dots)
        
        Returns:
            Metric value or None if not found
        """
        # Special computed metrics
        if metric == 'hip_shoulder_gap_ms':
            return self._calculate_hip_shoulder_gap(swing_data.get('kinematic_sequence', {}))
        elif metric == 'hands_bat_gap_ms':
            return self._calculate_hands_bat_gap(swing_data.get('kinematic_sequence', {}))
        elif metric == 'tempo_ratio':
            return swing_data.get('tempo', {}).get('ratio')
        elif metric == 'stability_score':
            return swing_data.get('stability', {}).get('score')
        elif metric == 'sequence_grade':
            return swing_data.get('kinematic_sequence', {}).get('grade')
        
        # Handle nested keys like 'tempo.ratio'
        keys = metric.split('.')
        value = swing_data
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key)
            else:
                return None
            if value is None:
                return None
        return value
    
    def _calculate_hip_shoulder_gap(self, kinematic_seq: Dict) -> Optional[float]:
        """Calculate time gap between hip and shoulder peaks (ms)"""
        # Try specific keys first
        if 'hips_peak_time' in kinematic_seq and 'shoulders_peak_time' in kinematic_seq:
            return abs(kinematic_seq['shoulders_peak_time'] - kinematic_seq['hips_peak_time'])
        
        # Fallback to torso/arms
        if 'torso_peak_ms' in kinematic_seq and 'arms_peak_ms' in kinematic_seq:
            return abs(kinematic_seq['arms_peak_ms'] - kinematic_seq['torso_peak_ms'])
        
        return None
    
    def _calculate_hands_bat_gap(self, kinematic_seq: Dict) -> Optional[float]:
        """Calculate time gap between hands and bat peaks (ms)"""
        # Try specific keys first
        if 'hands_peak_time' in kinematic_seq and 'bat_peak_time' in kinematic_seq:
            return abs(kinematic_seq['bat_peak_time'] - kinematic_seq['hands_peak_time'])
        
        # Fallback to arms/bat
        if 'arms_peak_ms' in kinematic_seq and 'bat_peak_ms' in kinematic_seq:
            return abs(kinematic_seq['bat_peak_ms'] - kinematic_seq['arms_peak_ms'])
        
        return None


# Example usage and testing
if __name__ == "__main__":
    try:
        from .motor_profile_classifier import classify_motor_profile
    except ImportError:
        from motor_profile_classifier import classify_motor_profile
    
    # Test case 1: Spinner with lead arm bent pattern
    spinner_data = {
        "kinematic_sequence": {
            "torso_peak_ms": 145,
            "arms_peak_ms": 160,  # 15ms gap
            "bat_peak_ms": 173,   # 13ms gap
            "grade": "B"
        },
        "tempo": {"ratio": 2.1},
        "stability": {"score": 92},
        "bat_speed": 82
    }
    
    motor_profile_result = classify_motor_profile(spinner_data)
    engine = PatternRecognitionEngine()
    patterns = engine.analyze(spinner_data, motor_profile_result.profile)
    
    print("=" * 70)
    print("SPINNER PATTERN RECOGNITION TEST")
    print("=" * 70)
    print(f"Motor Profile: {motor_profile_result.profile}")
    print(f"Patterns Found: {len(patterns)}")
    print()
    
    for i, pattern in enumerate(patterns, 1):
        print(f"{i}. [{pattern.priority}] {pattern.diagnosis}")
        print(f"   Pattern ID: {pattern.pattern_id}")
        print(f"   Root Cause: {pattern.root_cause}")
        print(f"   Symptoms:")
        for symptom in pattern.symptoms:
            print(f"     - {symptom}")
        print()
    
    # Test case 2: Whipper with disconnection
    whipper_data = {
        "kinematic_sequence": {
            "torso_peak_ms": 140,
            "arms_peak_ms": 175,  # 35ms gap - excessive
            "bat_peak_ms": 200,
            "grade": "B"
        },
        "tempo": {"ratio": 3.2},  # Too slow
        "stability": {"score": 88},
        "bat_speed": 85
    }
    
    motor_profile_result = classify_motor_profile(whipper_data)
    patterns = engine.analyze(whipper_data, motor_profile_result.profile)
    
    print("=" * 70)
    print("WHIPPER PATTERN RECOGNITION TEST")
    print("=" * 70)
    print(f"Motor Profile: {motor_profile_result.profile}")
    print(f"Patterns Found: {len(patterns)}")
    print()
    
    for i, pattern in enumerate(patterns, 1):
        print(f"{i}. [{pattern.priority}] {pattern.diagnosis}")
        print(f"   Pattern ID: {pattern.pattern_id}")
        print(f"   Root Cause: {pattern.root_cause}")
        print(f"   Symptoms:")
        for symptom in pattern.symptoms:
            print(f"     - {symptom}")
        print()
    
    # Test case 3: Universal pattern (poor stability)
    poor_stability_data = {
        "kinematic_sequence": {
            "torso_peak_ms": 145,
            "arms_peak_ms": 165,
            "bat_peak_ms": 185,
            "grade": "A"
        },
        "tempo": {"ratio": 2.1},
        "stability": {"score": 68},  # Poor stability
        "bat_speed": 80
    }
    
    motor_profile_result = classify_motor_profile(poor_stability_data)
    patterns = engine.analyze(poor_stability_data, motor_profile_result.profile)
    
    print("=" * 70)
    print("UNIVERSAL PATTERN TEST (Poor Stability)")
    print("=" * 70)
    print(f"Motor Profile: {motor_profile_result.profile}")
    print(f"Patterns Found: {len(patterns)}")
    print()
    
    for i, pattern in enumerate(patterns, 1):
        print(f"{i}. [{pattern.priority}] {pattern.diagnosis}")
        print(f"   Pattern ID: {pattern.pattern_id}")
        print(f"   Root Cause: {pattern.root_cause}")
        print(f"   Symptoms:")
        for symptom in pattern.symptoms:
            print(f"     - {symptom}")
        print()
