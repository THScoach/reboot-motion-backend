"""
Anthropometric Scaling Module
Based on de Leva (1996) - Adjustments to Zatsiorsky-Seluyanov's segment inertia parameters

Calculates body segment masses, lengths, and moments of inertia for biomechanics analysis
"""

import numpy as np
from typing import Dict, Tuple


class AnthropometricModel:
    """
    de Leva (1996) anthropometric model for adult males
    
    Reference:
    de Leva, P. (1996). Adjustments to Zatsiorsky-Seluyanov's segment inertia parameters.
    Journal of Biomechanics, 29(9), 1223-1230.
    """
    
    # Segment mass as proportion of total body mass
    SEGMENT_MASS_RATIOS = {
        'head': 0.0694,
        'trunk': 0.4346,  # Upper trunk + middle trunk + lower trunk
        'upper_arm': 0.0271,
        'forearm': 0.0162,
        'hand': 0.0061,
        'thigh': 0.1416,
        'shank': 0.0433,
        'foot': 0.0137
    }
    
    # Segment length as proportion of total body height
    SEGMENT_LENGTH_RATIOS = {
        'head': 0.130,
        'trunk': 0.288,  # C7 (neck) to hip
        'upper_arm': 0.188,  # Shoulder to elbow
        'forearm': 0.146,  # Elbow to wrist
        'hand': 0.108,  # Wrist to fingertip
        'thigh': 0.245,  # Hip to knee
        'shank': 0.246,  # Knee to ankle
        'foot': 0.039  # Ankle to toe
    }
    
    # Radius of gyration as proportion of segment length (for moment of inertia)
    # I = m * (k * L)^2
    RADIUS_OF_GYRATION = {
        'head': 0.495,
        'trunk': 0.496,
        'upper_arm': 0.322,
        'forearm': 0.303,
        'hand': 0.587,
        'thigh': 0.329,
        'shank': 0.302,
        'foot': 0.475
    }
    
    # Center of mass location (from proximal end as proportion of segment length)
    CENTER_OF_MASS = {
        'head': 0.500,
        'trunk': 0.500,
        'upper_arm': 0.436,
        'forearm': 0.430,
        'hand': 0.506,
        'thigh': 0.433,
        'shank': 0.433,
        'foot': 0.500
    }
    
    def __init__(self, height_inches: float, weight_lbs: float, 
                 age: int = 18, wingspan_inches: float = None):
        """
        Initialize anthropometric model for an athlete
        
        Args:
            height_inches: Total body height in inches
            weight_lbs: Total body weight in pounds
            age: Age in years (affects proportions for youth <18)
            wingspan_inches: Fingertip to fingertip span (optional, improves arm length accuracy)
        """
        self.height_cm = height_inches * 2.54
        self.height_m = self.height_cm / 100.0
        self.weight_kg = weight_lbs * 0.453592
        self.age = age
        self.wingspan_cm = wingspan_inches * 2.54 if wingspan_inches else None
        
        # Adjust proportions for youth athletes
        if age < 18:
            # Youth have proportionally longer legs and shorter trunks
            self.SEGMENT_LENGTH_RATIOS = self.SEGMENT_LENGTH_RATIOS.copy()
            self.SEGMENT_LENGTH_RATIOS['trunk'] = 0.270  # vs 0.288 for adults
            self.SEGMENT_LENGTH_RATIOS['thigh'] = 0.260  # vs 0.245 for adults
            self.SEGMENT_LENGTH_RATIOS['shank'] = 0.260  # vs 0.246 for adults
        
        # Calculate all segment properties
        self.segments = self._calculate_segments()
    
    def _calculate_segments(self) -> Dict[str, Dict[str, float]]:
        """Calculate mass, length, and inertia for all body segments"""
        segments = {}
        
        for segment_name in self.SEGMENT_MASS_RATIOS.keys():
            # Mass (kg)
            mass = self.weight_kg * self.SEGMENT_MASS_RATIOS[segment_name]
            
            # Length (m)
            length = self.height_m * self.SEGMENT_LENGTH_RATIOS[segment_name]
            
            # Radius of gyration (m)
            k = self.RADIUS_OF_GYRATION[segment_name]
            
            # Moment of inertia (kg⋅m²)
            # I = m × (k × L)²
            inertia = mass * (k * length) ** 2
            
            # Center of mass location (m from proximal end)
            com = length * self.CENTER_OF_MASS[segment_name]
            
            segments[segment_name] = {
                'mass': mass,
                'length': length,
                'inertia': inertia,
                'com': com,
                'k': k
            }
        
        return segments
    
    def get_arm_length(self) -> float:
        """
        Calculate total arm length (shoulder to fingertip)
        Uses wingspan if available for higher accuracy
        
        Returns:
            Arm length in meters
        """
        if self.wingspan_cm:
            # Measured wingspan approach
            shoulder_width = self.height_m * 0.259  # Biacromial breadth
            arm_length = (self.wingspan_cm / 100.0 - shoulder_width) / 2.0
        else:
            # Estimated from height
            arm_length = (self.segments['upper_arm']['length'] + 
                         self.segments['forearm']['length'] + 
                         self.segments['hand']['length'])
        
        return arm_length
    
    def get_torso_length(self) -> float:
        """Calculate torso length (neck to hip)"""
        return self.segments['trunk']['length']
    
    def get_leg_length(self) -> float:
        """Calculate total leg length (hip to toe)"""
        return (self.segments['thigh']['length'] + 
                self.segments['shank']['length'] + 
                self.segments['foot']['length'])
    
    def get_pelvis_inertia(self) -> float:
        """
        Calculate pelvis moment of inertia for rotation
        Approximated as lower trunk segment
        """
        # Lower trunk is approximately 1/3 of total trunk
        lower_trunk_mass = self.segments['trunk']['mass'] * 0.33
        
        # Hip width (biiliac breadth) ~ 0.191 * height
        hip_width = self.height_m * 0.191
        
        # Moment of inertia for rotation about vertical axis
        # Approximated as cylinder: I = m * r²
        pelvis_inertia = lower_trunk_mass * (hip_width / 2) ** 2
        
        return pelvis_inertia
    
    def get_torso_inertia(self) -> float:
        """
        Calculate torso moment of inertia for rotation
        """
        torso_mass = self.segments['trunk']['mass']
        
        # Shoulder width (biacromial breadth) ~ 0.259 * height
        shoulder_width = self.height_m * 0.259
        
        # Moment of inertia for rotation about vertical axis
        # Approximated as cylinder: I = m * r²
        torso_inertia = torso_mass * (shoulder_width / 2) ** 2
        
        return torso_inertia
    
    def get_bat_inertia(self, bat_length_inches: float = 33, 
                       bat_weight_oz: float = 30) -> float:
        """
        Calculate bat moment of inertia
        
        Args:
            bat_length_inches: Bat length in inches (default 33")
            bat_weight_oz: Bat weight in ounces (default 30 oz)
        
        Returns:
            Moment of inertia in kg⋅m²
        """
        bat_length_m = bat_length_inches * 0.0254
        bat_mass_kg = bat_weight_oz * 0.0283495
        
        # Model bat as uniform rod rotating about one end
        # I = (1/3) * m * L²
        bat_inertia = (1/3) * bat_mass_kg * bat_length_m ** 2
        
        return bat_inertia
    
    def get_segment(self, segment_name: str) -> Dict[str, float]:
        """Get properties for a specific segment"""
        return self.segments.get(segment_name, {})
    
    def print_summary(self):
        """Print anthropometric summary for debugging"""
        print(f"\n{'='*60}")
        print(f"ANTHROPOMETRIC MODEL SUMMARY")
        print(f"{'='*60}")
        print(f"Height: {self.height_cm:.1f} cm ({self.height_cm/2.54:.1f} in)")
        print(f"Weight: {self.weight_kg:.1f} kg ({self.weight_kg*2.20462:.1f} lbs)")
        print(f"Age: {self.age} years")
        if self.wingspan_cm:
            print(f"Wingspan: {self.wingspan_cm:.1f} cm ({self.wingspan_cm/2.54:.1f} in)")
        print(f"\n{'Segment':<15} {'Mass (kg)':<12} {'Length (cm)':<12} {'Inertia (kg⋅m²)'}")
        print(f"{'-'*60}")
        
        for segment_name, props in self.segments.items():
            print(f"{segment_name:<15} {props['mass']:<12.2f} {props['length']*100:<12.1f} {props['inertia']:<12.4f}")
        
        print(f"\n{'Key Measurements':<30} {'Value'}")
        print(f"{'-'*60}")
        print(f"{'Arm Length (shoulder-fingertip)':<30} {self.get_arm_length()*100:.1f} cm")
        print(f"{'Torso Length (neck-hip)':<30} {self.get_torso_length()*100:.1f} cm")
        print(f"{'Leg Length (hip-toe)':<30} {self.get_leg_length()*100:.1f} cm")
        print(f"{'Pelvis Inertia':<30} {self.get_pelvis_inertia():.4f} kg⋅m²")
        print(f"{'Torso Inertia':<30} {self.get_torso_inertia():.4f} kg⋅m²")
        print(f"{'Bat Inertia (33\", 30oz)':<30} {self.get_bat_inertia():.4f} kg⋅m²")
        print(f"{'='*60}\n")


if __name__ == "__main__":
    # Test with Conor Gray
    print("Testing Conor Gray (High School):")
    conor = AnthropometricModel(
        height_inches=72,  # 6'0"
        weight_lbs=160,
        age=16,
        wingspan_inches=76
    )
    conor.print_summary()
    
    # Test with Shohei Ohtani
    print("\nTesting Shohei Ohtani (MLB):")
    shohei = AnthropometricModel(
        height_inches=76,  # 6'4"
        weight_lbs=210,
        age=29,
        wingspan_inches=79
    )
    shohei.print_summary()
