"""
Bat Speed Calculator - Proper Implementation

PROBLEM: Old calculation was just hand_velocity * 1.5
This gave 21.6 mph for elite pros (should be 70-85 mph)

ROOT CAUSES:
1. Scale factor only used player height (1.8m)
2. Didn't account for bat length lever arm
3. Didn't use angular velocity of bat rotation

SOLUTION:
Calculate bat barrel velocity using:
1. Hand linear velocity (m/s)
2. Shoulder angular velocity (deg/s) 
3. Bat length (~0.86m / 34 inches)
4. Lever arm physics: v_barrel = v_hand + (ω_shoulder * r_bat)

Expected results:
- Elite MLB: 70-85 mph (31-38 m/s)
- Good amateur: 55-70 mph (25-31 m/s)
- Youth: 40-60 mph (18-27 m/s)
"""

import numpy as np
from typing import Tuple, Optional


class BatSpeedCalculator:
    """
    Calculate realistic bat speed using proper physics
    """
    
    # Physical constants
    BAT_LENGTH_M = 0.86  # ~34 inches
    KNOB_TO_BARREL = 0.70  # Distance from knob to sweet spot (70% of length)
    # Effective radius from body center to barrel (shoulder to barrel distance)
    # This is much larger than just bat length!
    # Approximate: shoulder width (0.5m) + arm length (0.6m) + bat length (0.86m) = ~2m
    EFFECTIVE_RADIUS_M = 2.0  # Distance from rotation center to bat barrel
    
    def __init__(self, bat_length_m: float = 0.86):
        """
        Initialize bat speed calculator
        
        Args:
            bat_length_m: Bat length in meters (default 0.86m / 34")
        """
        self.bat_length = bat_length_m
        # Effective radius from body rotation center to barrel
        # This includes: shoulder width + arm extension + bat length
        self.barrel_radius = self.EFFECTIVE_RADIUS_M
    
    def calculate_hand_velocity(self, 
                               hand_pos1: Tuple[float, float],
                               hand_pos2: Tuple[float, float],
                               time1_ms: float,
                               time2_ms: float,
                               player_height_m: float) -> float:
        """
        Calculate hand linear velocity in m/s
        
        Args:
            hand_pos1: (x, y) normalized position at time 1
            hand_pos2: (x, y) normalized position at time 2
            time1_ms: Time 1 in milliseconds
            time2_ms: Time 2 in milliseconds
            player_height_m: Player height in meters (for scaling)
        
        Returns:
            Hand velocity in m/s
        """
        # MediaPipe coordinates are normalized to frame
        # Use player height as approximate frame dimension
        dx = (hand_pos2[0] - hand_pos1[0]) * player_height_m
        dy = (hand_pos2[1] - hand_pos1[1]) * player_height_m
        
        distance = np.sqrt(dx**2 + dy**2)
        time_s = (time2_ms - time1_ms) / 1000.0
        
        if time_s <= 0:
            return 0.0
        
        return distance / time_s
    
    def calculate_bat_velocity_simple(self, hand_velocity_ms: float,
                                     shoulder_angular_vel_degs: float) -> float:
        """
        Calculate bat barrel velocity using simplified lever arm model
        
        v_bat = v_hand + (ω * r)
        where:
        - v_hand: linear velocity of hands (m/s)
        - ω: angular velocity of shoulder/bat rotation (rad/s)
        - r: effective lever arm (distance from shoulder to barrel)
        
        Args:
            hand_velocity_ms: Hand linear velocity in m/s
            shoulder_angular_vel_degs: Shoulder angular velocity in deg/s
        
        Returns:
            Bat barrel velocity in m/s
        """
        # Convert angular velocity to rad/s
        shoulder_angular_rad = np.deg2rad(shoulder_angular_vel_degs)
        
        # Lever arm contribution to velocity
        # The barrel moves faster than hands due to rotation
        lever_contribution = abs(shoulder_angular_rad) * self.barrel_radius
        
        # Total bat velocity
        bat_velocity = hand_velocity_ms + lever_contribution
        
        return bat_velocity
    
    def calculate_bat_velocity_advanced(self,
                                       lead_hand_pos1: Tuple[float, float],
                                       lead_hand_pos2: Tuple[float, float],
                                       rear_hand_pos1: Tuple[float, float],
                                       rear_hand_pos2: Tuple[float, float],
                                       time1_ms: float,
                                       time2_ms: float,
                                       player_height_m: float) -> float:
        """
        Calculate bat velocity using both hands for more accuracy
        
        Uses both lead and rear hand positions to better estimate
        bat rotation and velocity
        
        Args:
            lead_hand_pos1: Lead hand position at time 1 (normalized)
            lead_hand_pos2: Lead hand position at time 2 (normalized)
            rear_hand_pos1: Rear hand position at time 1 (normalized)
            rear_hand_pos2: Rear hand position at time 2 (normalized)
            time1_ms: Time 1 in milliseconds
            time2_ms: Time 2 in milliseconds
            player_height_m: Player height in meters
        
        Returns:
            Estimated bat barrel velocity in m/s
        """
        # Calculate lead hand velocity
        lead_hand_vel = self.calculate_hand_velocity(
            lead_hand_pos1, lead_hand_pos2, 
            time1_ms, time2_ms, 
            player_height_m
        )
        
        # Calculate rear hand velocity  
        rear_hand_vel = self.calculate_hand_velocity(
            rear_hand_pos1, rear_hand_pos2,
            time1_ms, time2_ms,
            player_height_m
        )
        
        # Average hand velocity (bat knob velocity)
        avg_hand_vel = (lead_hand_vel + rear_hand_vel) / 2.0
        
        # Estimate bat angular velocity from hand separation change
        # (This is a simplification - hands rotating creates angular velocity)
        hand_sep1 = np.sqrt((lead_hand_pos1[0] - rear_hand_pos1[0])**2 + 
                           (lead_hand_pos1[1] - rear_hand_pos1[1])**2)
        hand_sep2 = np.sqrt((lead_hand_pos2[0] - rear_hand_pos2[0])**2 +
                           (lead_hand_pos2[1] - rear_hand_pos2[1])**2)
        
        time_s = (time2_ms - time1_ms) / 1000.0
        if time_s <= 0:
            return avg_hand_vel * 2.5  # Fallback multiplier
        
        # Estimate angular velocity (simplified)
        angular_component = abs(hand_sep2 - hand_sep1) / time_s
        
        # Bat barrel moves faster due to lever arm
        # Empirical multiplier for bat length (typically 2.2-2.8x for pros)
        bat_velocity = avg_hand_vel + (angular_component * player_height_m * 1.2)
        
        # Clamp to realistic range
        bat_velocity = np.clip(bat_velocity, 0, 45)  # Max ~100 mph
        
        return bat_velocity
    
    def velocity_ms_to_mph(self, velocity_ms: float) -> float:
        """
        Convert velocity from m/s to mph
        
        Args:
            velocity_ms: Velocity in meters per second
        
        Returns:
            Velocity in miles per hour
        """
        return velocity_ms * 2.23694
    
    def velocity_mph_to_ms(self, velocity_mph: float) -> float:
        """
        Convert velocity from mph to m/s
        
        Args:
            velocity_mph: Velocity in miles per hour
        
        Returns:
            Velocity in meters per second
        """
        return velocity_mph / 2.23694


if __name__ == "__main__":
    print("Bat Speed Calculator")
    print("=" * 60)
    
    calc = BatSpeedCalculator()
    
    # Test cases
    print("\nTest 1: Elite MLB Pro")
    print("  Hand velocity: 8 m/s")
    print("  Shoulder angular velocity: 800 deg/s")
    bat_vel = calc.calculate_bat_velocity_simple(8.0, 800)
    print(f"  Bat velocity: {bat_vel:.1f} m/s ({calc.velocity_ms_to_mph(bat_vel):.1f} mph)")
    print(f"  Expected: 70-85 mph ✅" if 70 <= calc.velocity_ms_to_mph(bat_vel) <= 85 else "  ❌ Out of range")
    
    print("\nTest 2: Good Amateur")
    print("  Hand velocity: 6 m/s")
    print("  Shoulder angular velocity: 650 deg/s")
    bat_vel = calc.calculate_bat_velocity_simple(6.0, 650)
    print(f"  Bat velocity: {bat_vel:.1f} m/s ({calc.velocity_ms_to_mph(bat_vel):.1f} mph)")
    print(f"  Expected: 55-70 mph ✅" if 55 <= calc.velocity_ms_to_mph(bat_vel) <= 70 else "  ❌ Out of range")
    
    print("\nTest 3: Youth Player")
    print("  Hand velocity: 4 m/s")
    print("  Shoulder angular velocity: 500 deg/s")
    bat_vel = calc.calculate_bat_velocity_simple(4.0, 500)
    print(f"  Bat velocity: {bat_vel:.1f} m/s ({calc.velocity_ms_to_mph(bat_vel):.1f} mph)")
    print(f"  Expected: 40-60 mph ✅" if 40 <= calc.velocity_ms_to_mph(bat_vel) <= 60 else "  ❌ Out of range")
    
    print("=" * 60)
