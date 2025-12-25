"""
Efficiency Calculator for Swing DNA Analysis
============================================

Calculates efficiency metrics from biomechanical data:
- Hip Efficiency (0-100%)
- Knee Efficiency (0-100%)
- Contact Efficiency (0-100%)
- Total Efficiency (weighted average)
"""

from typing import Dict
from dataclasses import dataclass
from .csv_parser import SwingMetrics


@dataclass
class EfficiencyScores:
    """Container for efficiency metrics"""
    hip_efficiency: float  # 0-100%
    knee_efficiency: float  # 0-100%
    contact_efficiency: float  # 0-100%
    total_efficiency: float  # weighted average


class EfficiencyCalculator:
    """Calculate efficiency metrics from swing data"""
    
    # Target values for 100% efficiency
    TARGETS = {
        'hip_angmom': 10.0,  # Target hip angular momentum
        'knee_angle': 170.0,  # Target lead knee angle (degrees)
        'arm_extension': 20.0,  # Target lead arm extension (degrees)
    }
    
    # Weights for total efficiency calculation
    WEIGHTS = {
        'hip': 0.4,  # 40% weight
        'knee': 0.3,  # 30% weight
        'contact': 0.3,  # 30% weight
    }
    
    def calculate(self, metrics: SwingMetrics) -> EfficiencyScores:
        """
        Calculate efficiency scores from swing metrics
        
        Args:
            metrics: SwingMetrics from CSV parser
            
        Returns:
            EfficiencyScores object
        """
        # Hip Efficiency: Based on hip angular momentum
        hip_eff = min((metrics.hip_angular_momentum / self.TARGETS['hip_angmom']) * 100, 100)
        
        # Knee Efficiency: Based on lead knee extension
        knee_eff = min((metrics.lead_knee_angle / self.TARGETS['knee_angle']) * 100, 100)
        
        # Contact Efficiency: Based on lead arm extension
        contact_eff = min((metrics.lead_arm_extension / self.TARGETS['arm_extension']) * 100, 100)
        
        # Total Efficiency: Weighted average
        total_eff = (
            hip_eff * self.WEIGHTS['hip'] +
            knee_eff * self.WEIGHTS['knee'] +
            contact_eff * self.WEIGHTS['contact']
        )
        
        return EfficiencyScores(
            hip_efficiency=round(hip_eff, 1),
            knee_efficiency=round(knee_eff, 1),
            contact_efficiency=round(contact_eff, 1),
            total_efficiency=round(total_eff, 1)
        )
    
    def to_dict(self, scores: EfficiencyScores) -> Dict:
        """Convert EfficiencyScores to dictionary"""
        return {
            'hip_efficiency': scores.hip_efficiency,
            'knee_efficiency': scores.knee_efficiency,
            'contact_efficiency': scores.contact_efficiency,
            'total_efficiency': scores.total_efficiency
        }


# Convenience function for easier imports
def calculate_efficiency_scores(metrics) -> Dict:
    """
    Calculate efficiency scores from swing metrics
    
    Args:
        metrics: SwingMetrics dataclass or dict with biomechanical data
        
    Returns:
        Dictionary with efficiency scores
    """
    calculator = EfficiencyCalculator()
    # Handle both SwingMetrics and dict inputs
    if isinstance(metrics, dict):
        from .csv_parser import SwingMetrics
        metrics = SwingMetrics(**metrics)
    scores = calculator.calculate(metrics)
    return calculator.to_dict(scores)
