"""
Pattern Recognition for Swing DNA Analysis
==========================================

Diagnoses swing patterns based on biomechanical metrics.

4 Diagnostic Patterns:
1. PATTERN_1_KNEE_LEAK: Energy Leak at Lead Knee
2. PATTERN_2_WEAK_HIP: Weak Hip Contribution (Despite Good Timing)
3. PATTERN_3_SPINNER: Fast Foot Roll (Spinner Pattern)
4. PATTERN_4_SHOULDER_COMP: Shoulder Compensation (Over-Rotation)
"""

from typing import Dict
from dataclasses import dataclass
from .csv_parser import SwingMetrics


@dataclass
class PatternDiagnosis:
    """Container for pattern diagnosis results"""
    type: str  # Pattern ID
    severity: str  # CRITICAL, HIGH, MODERATE, LOW
    title: str  # Human-readable title
    description: str  # Detailed description
    root_cause: str  # Root cause explanation
    primary_protocol: str  # Primary intervention protocol
    secondary_protocol: str  # Secondary protocol (optional)


class PatternRecognizer:
    """
    Recognize biomechanical swing patterns from metrics
    """
    
    # Pattern thresholds
    THRESHOLDS = {
        'lead_knee_extended': 160,  # degrees (below = flexed)
        'lead_knee_critical': 140,  # degrees (severe flexion)
        'hip_angmom_target': 8.0,  # target value
        'hip_angmom_weak': 5.0,  # below = weak
        'shoulder_hip_ratio_normal': 1.5,  # normal ratio
        'shoulder_hip_ratio_high': 3.0,  # elevated ratio
        'shoulder_hip_ratio_critical': 4.0,  # very high ratio
        'timing_gap_good': 15,  # ms (above = good timing)
        'timing_gap_short': 15,  # ms (below = fast foot roll)
    }
    
    def diagnose(self, metrics: SwingMetrics) -> PatternDiagnosis:
        """
        Diagnose swing pattern from metrics
        
        Args:
            metrics: SwingMetrics object from CSV parser
            
        Returns:
            PatternDiagnosis object
        """
        # Extract key values
        knee = metrics.lead_knee_angle
        hip = metrics.hip_angular_momentum
        shoulder = metrics.shoulder_angular_momentum
        ratio = metrics.shoulder_hip_ratio
        timing = metrics.timing_gap_ms
        
        # Pattern matching logic (order matters - check most critical first)
        
        # PATTERN 1: Energy Leak at Lead Knee
        if (knee < self.THRESHOLDS['lead_knee_critical'] and 
            hip < self.THRESHOLDS['hip_angmom_weak'] and 
            ratio > self.THRESHOLDS['shoulder_hip_ratio_high']):
            
            return self._pattern_1_knee_leak(metrics)
        
        # PATTERN 2: Weak Hip Contribution (Good Timing)
        elif (hip < self.THRESHOLDS['hip_angmom_weak'] and 
              timing > self.THRESHOLDS['timing_gap_good'] and 
              ratio > self.THRESHOLDS['shoulder_hip_ratio_critical']):
            
            return self._pattern_2_weak_hip(metrics)
        
        # PATTERN 3: Fast Foot Roll (Spinner)
        elif (knee < self.THRESHOLDS['lead_knee_critical'] and 
              timing < self.THRESHOLDS['timing_gap_short'] and 
              hip < self.THRESHOLDS['hip_angmom_weak']):
            
            return self._pattern_3_spinner(metrics)
        
        # PATTERN 4: Shoulder Compensation
        elif (ratio > self.THRESHOLDS['shoulder_hip_ratio_critical'] and 
              hip < self.THRESHOLDS['hip_angmom_weak']):
            
            return self._pattern_4_shoulder_comp(metrics)
        
        # No clear pattern (needs manual review)
        else:
            return self._pattern_unclear(metrics)
    
    def _pattern_1_knee_leak(self, metrics: SwingMetrics) -> PatternDiagnosis:
        """Pattern 1: Energy Leak at Lead Knee"""
        knee = metrics.lead_knee_angle
        hip = metrics.hip_angular_momentum
        ratio = metrics.shoulder_hip_ratio
        target_knee = 170
        energy_loss_pct = int((target_knee - knee) / target_knee * 100)
        
        description = (
            f"Your lead knee is flexed at {knee:.1f}° (should be 160-180°). "
            f"This absorbs {energy_loss_pct}% of your ground force before "
            f"it reaches your hips. Result: Weak hip contribution ({hip:.1f} "
            f"vs target 8-10+) and shoulder compensation ({ratio:.1f}x "
            f"vs target 0.7-1.5x)."
        )
        
        return PatternDiagnosis(
            type="PATTERN_1_KNEE_LEAK",
            severity="CRITICAL",
            title="Energy Leak at Lead Knee",
            description=description,
            root_cause="Coordination issue - lead knee flexing instead of extending",
            primary_protocol="PROTOCOL_1",
            secondary_protocol="PROTOCOL_2"
        )
    
    def _pattern_2_weak_hip(self, metrics: SwingMetrics) -> PatternDiagnosis:
        """Pattern 2: Weak Hip Contribution"""
        hip = metrics.hip_angular_momentum
        timing = metrics.timing_gap_ms
        ratio = metrics.shoulder_hip_ratio
        
        description = (
            f"Your timing is good ({timing:.0f}ms gap), but your hips only "
            f"contribute {hip:.1f} angular momentum (should be 8-10+). "
            f"Shoulders forced to compensate ({ratio:.1f}x ratio). "
            f"You have the deceleration mechanism but weak hip input."
        )
        
        return PatternDiagnosis(
            type="PATTERN_2_WEAK_HIP",
            severity="HIGH",
            title="Weak Hip Contribution",
            description=description,
            root_cause="Weak vertical ground force and/or lead knee leak",
            primary_protocol="PROTOCOL_2",
            secondary_protocol="PROTOCOL_3"
        )
    
    def _pattern_3_spinner(self, metrics: SwingMetrics) -> PatternDiagnosis:
        """Pattern 3: Spinner Pattern (Fast Foot Roll)"""
        knee = metrics.lead_knee_angle
        timing = metrics.timing_gap_ms
        hip = metrics.hip_angular_momentum
        
        description = (
            f"Your lead foot is rolling too quickly (weak vertical push). "
            f"Lead knee never extends ({knee:.1f}°), hips and shoulders "
            f"rotate together (only {timing:.0f}ms gap). You're spinning "
            f"instead of posting and rotating."
        )
        
        return PatternDiagnosis(
            type="PATTERN_3_SPINNER",
            severity="HIGH",
            title="Spinner Pattern (Fast Foot Roll)",
            description=description,
            root_cause="Not pushing vertically through ball of lead foot",
            primary_protocol="PROTOCOL_2",
            secondary_protocol="PROTOCOL_1"
        )
    
    def _pattern_4_shoulder_comp(self, metrics: SwingMetrics) -> PatternDiagnosis:
        """Pattern 4: Shoulder Compensation"""
        ratio = metrics.shoulder_hip_ratio
        hip = metrics.hip_angular_momentum
        
        description = (
            f"Your shoulders are doing work your hips should do. "
            f"Shoulder/hip ratio: {ratio:.1f}x (should be 0.7-1.5x). "
            f"This leads to 'muscling' the swing and bat drag."
        )
        
        return PatternDiagnosis(
            type="PATTERN_4_SHOULDER_COMP",
            severity="MODERATE",
            title="Shoulder Compensation (Over-Rotation)",
            description=description,
            root_cause="Weak hip contribution forces shoulder compensation",
            primary_protocol="PROTOCOL_3",
            secondary_protocol="PROTOCOL_4"
        )
    
    def _pattern_unclear(self, metrics: SwingMetrics) -> PatternDiagnosis:
        """No clear pattern detected"""
        return PatternDiagnosis(
            type="PATTERN_UNCLEAR",
            severity="LOW",
            title="Pattern Unclear - Manual Review Needed",
            description="Metrics do not match standard patterns. Consult with coach for personalized analysis.",
            root_cause="Unknown",
            primary_protocol=None,
            secondary_protocol=None
        )
    
    def to_dict(self, diagnosis: PatternDiagnosis) -> Dict:
        """Convert PatternDiagnosis to dictionary"""
        return {
            'type': diagnosis.type,
            'severity': diagnosis.severity,
            'title': diagnosis.title,
            'description': diagnosis.description,
            'root_cause': diagnosis.root_cause,
            'primary_protocol': diagnosis.primary_protocol,
            'secondary_protocol': diagnosis.secondary_protocol
        }


# Example usage
if __name__ == "__main__":
    from .csv_parser import SwingMetrics
    
    # Eric Williams example metrics
    metrics = SwingMetrics(
        contact_frame=100,
        total_frames=200,
        lead_knee_angle=0.3,
        hip_angular_momentum=2.10,
        hip_peak_frame=95,
        shoulder_angular_momentum=18.25,
        shoulder_peak_frame=98,
        shoulder_hip_ratio=8.68,
        timing_gap_ms=158.3,
        bat_speed=82.0,
        bat_kinetic_energy=150.0,
        lead_arm_extension=1.5,
        vertical_grf_estimate=0.8,
        lead_leg_energy=50.0,
        handedness='RHH'
    )
    
    recognizer = PatternRecognizer()
    diagnosis = recognizer.diagnose(metrics)
    
    print("🎯 Pattern Diagnosis:")
    print(f"  Type: {diagnosis.type}")
    print(f"  Severity: {diagnosis.severity}")
    print(f"  Title: {diagnosis.title}")
    print(f"  Root Cause: {diagnosis.root_cause}")
    print(f"  Primary Protocol: {diagnosis.primary_protocol}")
    print(f"  Secondary Protocol: {diagnosis.secondary_protocol}")
