"""
Bat Speed Calculator - Ground Truth Based Implementation

Based on Reboot Motion validation data:
- Connor Gray (16yo, HS): 57.5 mph
- Calculation: sqrt(2 * bat_trans_energy / bat_mass) * 2.237

SIMPLIFIED APPROACH:
Instead of complex lever arm physics, use the bat angular velocity directly
from the wrist-to-wrist angle (as in TypeScript implementation)

Formula: v_bat_mph = bat_angular_velocity_deg_per_sec * K * 2.237
Where K is a calibration constant based on bat length
"""

import numpy as np
from typing import Tuple

class BatSpeedCalculator:
    """
    Calculate bat speed using simplified, validated approach
    """
    
    def __init__(self, bat_length_inches: float = 33):
        """
        Initialize calculator
        
        Args:
            bat_length_inches: Bat length in inches (default 33")
        """
        self.bat_length_m = bat_length_inches * 0.0254
        
        # Calibration constant: convert angular velocity to linear bat speed
        # Based on: distance from hands to barrel (~75% of bat length)
        self.barrel_distance_m = self.bat_length_m * 0.75
    
    def calculate_bat_speed_mph(self, bat_angular_velocity_deg_per_sec: float) -> float:
        """
        Calculate bat speed in mph from angular velocity
        
        This matches the TypeScript implementation approach:
        - Bat is approximated by wrist-to-wrist line
        - Angular velocity of that line = bat angular velocity
        - Convert to linear velocity at barrel using lever arm
        
        Args:
            bat_angular_velocity_deg_per_sec: Bat angular velocity in deg/s
        
        Returns:
            Bat speed in mph
        """
        # Convert to radians per second
        omega_rad_per_sec = np.deg2rad(abs(bat_angular_velocity_deg_per_sec))
        
        # Linear velocity at barrel: v = ω × r
        velocity_m_per_s = omega_rad_per_sec * self.barrel_distance_m
        
        # Convert to mph: m/s × 2.237 = mph
        velocity_mph = velocity_m_per_s * 2.237
        
        # Sanity cap: 120 mph is theoretical max
        velocity_mph = min(velocity_mph, 120.0)
        
        return velocity_mph
    
    def calculate_bat_velocity_simple(self, hand_velocity_ms: float,
                                     shoulder_angular_vel_degs: float) -> float:
        """
        Legacy method for compatibility
        
        Now just returns the bat angular velocity converted to m/s
        (The calling code will convert to mph separately)
        """
        # Convert angular velocity to rad/s
        omega_rad_per_sec = np.deg2rad(abs(shoulder_angular_vel_degs))
        
        # Linear velocity at barrel
        bat_velocity_ms = omega_rad_per_sec * self.barrel_distance_m
        
        # Sanity cap: ~53 m/s = ~120 mph
        bat_velocity_ms = min(bat_velocity_ms, 53.0)
        
        return bat_velocity_ms
