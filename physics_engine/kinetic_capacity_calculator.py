"""
Kinetic Capacity Calculator Module
Calculates the theoretical capacity range (ceiling) based on body specifications

Part of Priority 9: Kinetic Capacity Framework
Core Philosophy: Shift from predicting exact bat speed to calculating kinetic capacity ceiling

Uses Priority 1's PotentialCalculator as the baseline (85% efficiency)
and applies efficiency bounds (75-95%) to create a capacity range
"""

from typing import Dict
import logging
from physics_engine.potential_calculator_v2 import PotentialCalculator

logger = logging.getLogger(__name__)


class KineticCapacityCalculator:
    """
    Calculates kinetic capacity ceiling from body specifications
    Shows bat speed range (e.g., 75-85 mph) instead of exact prediction
    
    IMPORTANT: Uses Priority 1's PotentialCalculator as the 85% efficiency baseline
    and applies efficiency bounds to create capacity range
    """
    
    # Efficiency bounds for capacity range
    MIN_EFFICIENCY = 0.75  # 75% minimum achievable (undertrained)
    MAX_EFFICIENCY = 0.95  # 95% maximum achievable (elite)
    TYPICAL_EFFICIENCY = 0.85  # 85% typical for trained athletes (Priority 1 baseline)
    
    def __init__(self):
        """Initialize the kinetic capacity calculator"""
        self.logger = logging.getLogger(self.__class__.__name__)
        self.potential_calc = PotentialCalculator()
    
    def calculate_capacity_range(
        self,
        wingspan_inches: float,
        weight_lbs: float,
        height_inches: float,
        bat_weight_oz: float = 30,
        age: int = 25
    ) -> Dict:
        """
        Calculate the kinetic capacity range (bat speed ceiling)
        
        This is the CORE method for Priority 9
        Returns a RANGE (e.g., 75-85 mph) instead of exact prediction
        
        Uses Priority 1's calculation as the 85% efficiency baseline,
        then applies efficiency bounds (75-95%) to create range
        
        Args:
            wingspan_inches: Arm span
            weight_lbs: Body weight
            height_inches: Height
            bat_weight_oz: Bat weight (default 30oz)
            age: Player age (default 25)
            
        Returns:
            Dictionary with capacity range and midpoint
        """
        # Get baseline from Priority 1 (this is the 85% efficiency point)
        potential_result = self.potential_calc.calculate_full_potential(
            wingspan_inches=wingspan_inches,
            weight_lbs=weight_lbs,
            height_inches=height_inches,
            bat_weight_oz=bat_weight_oz,
            age=age
        )
        
        # Extract the baseline bat speed (85% efficiency)
        baseline_mph = potential_result['bat_speed']['potential_mph']
        
        # Calculate capacity range by scaling the baseline
        # Baseline is 85% efficiency, so we scale to get 75% and 95%
        capacity_min_mph = baseline_mph * (self.MIN_EFFICIENCY / self.TYPICAL_EFFICIENCY)
        capacity_max_mph = baseline_mph * (self.MAX_EFFICIENCY / self.TYPICAL_EFFICIENCY)
        capacity_midpoint_mph = baseline_mph  # Baseline IS the midpoint
        
        self.logger.debug(
            f"Capacity range: {capacity_min_mph:.1f}-{capacity_max_mph:.1f} mph "
            f"(baseline: {baseline_mph:.1f} mph @ 85%)"
        )
        
        return {
            'capacity_min_mph': round(capacity_min_mph, 1),
            'capacity_max_mph': round(capacity_max_mph, 1),
            'capacity_midpoint_mph': round(capacity_midpoint_mph, 1),
            'baseline_bat_speed_mph': round(baseline_mph, 1),
            'efficiency_range': f'{int(self.MIN_EFFICIENCY*100)}-{int(self.MAX_EFFICIENCY*100)}%',
            'typical_efficiency': f'{int(self.TYPICAL_EFFICIENCY*100)}%'
        }
    
    def calculate_efficiency_from_actual(
        self,
        actual_bat_speed_mph: float,
        capacity_midpoint_mph: float
    ) -> float:
        """
        Calculate % of capacity being used based on actual performance
        
        Args:
            actual_bat_speed_mph: Measured bat speed
            capacity_midpoint_mph: Calculated capacity midpoint (85% efficiency baseline)
            
        Returns:
            Efficiency percentage (0-100+)
        """
        if capacity_midpoint_mph <= 0:
            return 0.0
        
        # Calculate efficiency relative to the 85% baseline
        # If actual equals midpoint, efficiency is 85%
        # Scale proportionally
        
        efficiency_ratio = actual_bat_speed_mph / capacity_midpoint_mph
        efficiency_pct = efficiency_ratio * self.TYPICAL_EFFICIENCY * 100
        
        return round(efficiency_pct, 1)
    
    def get_capacity_status(self, efficiency_pct: float) -> str:
        """
        Determine capacity utilization status
        
        Args:
            efficiency_pct: Efficiency percentage
            
        Returns:
            Status string
        """
        if efficiency_pct >= 90:
            return 'ELITE'
        elif efficiency_pct >= 80:
            return 'GOOD'
        elif efficiency_pct >= 70:
            return 'AVERAGE'
        elif efficiency_pct >= 60:
            return 'BELOW_AVERAGE'
        else:
            return 'UNDERTRAINED'


if __name__ == "__main__":
    # Test with Eric Williams data
    print("="*70)
    print("KINETIC CAPACITY CALCULATOR TEST - ERIC WILLIAMS")
    print("="*70)
    
    calculator = KineticCapacityCalculator()
    
    # Eric Williams specs
    wingspan = 68  # inches (5'8")
    weight = 190   # lbs
    height = 68    # inches (5'8")
    age = 33
    actual_bat_speed = 67  # mph (from Blast sensor)
    
    # Calculate capacity range
    capacity = calculator.calculate_capacity_range(wingspan, weight, height, age=age)
    
    print(f"\n📊 KINETIC CAPACITY (Body Specs):")
    print(f"   Wingspan: {wingspan}\" | Weight: {weight} lbs | Height: {height}\" | Age: {age}")
    print(f"   Baseline (Priority 1): {capacity['baseline_bat_speed_mph']} mph @ 85% efficiency")
    
    print(f"\n⚡ BAT SPEED CAPACITY RANGE:")
    print(f"   Min (75% efficiency): {capacity['capacity_min_mph']} mph")
    print(f"   Midpoint (85% typical): {capacity['capacity_midpoint_mph']} mph")
    print(f"   Max (95% elite): {capacity['capacity_max_mph']} mph")
    
    # Calculate efficiency from actual
    efficiency = calculator.calculate_efficiency_from_actual(
        actual_bat_speed,
        capacity['capacity_midpoint_mph']
    )
    
    status = calculator.get_capacity_status(efficiency)
    
    print(f"\n🎯 CURRENT PERFORMANCE:")
    print(f"   Actual Bat Speed: {actual_bat_speed} mph")
    print(f"   Capacity Used: {efficiency}%")
    print(f"   Status: {status}")
    
    # Calculate untapped capacity
    gap_to_midpoint = capacity['capacity_midpoint_mph'] - actual_bat_speed
    gap_to_max = capacity['capacity_max_mph'] - actual_bat_speed
    
    print(f"\n💡 UNTAPPED CAPACITY:")
    print(f"   To Midpoint (typical): +{gap_to_midpoint:.1f} mph")
    print(f"   To Maximum (elite): +{gap_to_max:.1f} mph")
    
    print("\n" + "="*70)
