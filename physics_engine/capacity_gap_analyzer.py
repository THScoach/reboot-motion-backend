"""
Capacity Gap Analyzer Module
Compares actual performance to kinetic capacity ceiling

Part of Priority 9: Kinetic Capacity Framework
This is different from the Priority 3 gap_analyzer.py which compares to exact predictions
"""

from typing import Dict
import logging

logger = logging.getLogger(__name__)


class CapacityGapAnalyzer:
    """
    Analyzes the gap between actual performance and kinetic capacity ceiling
    Shows % of capacity being used and untapped capacity remaining
    """
    
    def __init__(self):
        """Initialize capacity gap analyzer"""
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def calculate_capacity_gap(
        self,
        actual_bat_speed_mph: float,
        capacity_min_mph: float,
        capacity_midpoint_mph: float,
        capacity_max_mph: float
    ) -> Dict:
        """
        Calculate gap between actual performance and capacity range
        
        Args:
            actual_bat_speed_mph: Measured bat speed
            capacity_min_mph: Minimum capacity (75% efficiency)
            capacity_midpoint_mph: Midpoint capacity (85% efficiency)
            capacity_max_mph: Maximum capacity (95% efficiency)
            
        Returns:
            Dictionary with capacity gap analysis:
            {
                'actual_mph': 67.0,
                'capacity_range': '75-85 mph',
                'capacity_midpoint_mph': 80.0,
                'gap_to_midpoint_mph': 13.0,
                'gap_to_max_mph': 18.0,
                'capacity_used_pct': 83.8,
                'capacity_untapped_pct': 16.2,
                'position_in_range': 'BELOW_TYPICAL',
                'status': 'BELOW_AVERAGE'
            }
        """
        # Calculate gaps
        gap_to_midpoint = capacity_midpoint_mph - actual_bat_speed_mph
        gap_to_max = capacity_max_mph - actual_bat_speed_mph
        
        # Calculate capacity used (relative to midpoint as baseline)
        if capacity_midpoint_mph > 0:
            capacity_used_pct = (actual_bat_speed_mph / capacity_midpoint_mph) * 100
        else:
            capacity_used_pct = 0.0
        
        capacity_untapped_pct = 100 - capacity_used_pct
        
        # Determine position in range
        if actual_bat_speed_mph >= capacity_max_mph:
            position = 'ABOVE_MAXIMUM'  # Exceeding theoretical capacity (rare)
        elif actual_bat_speed_mph >= capacity_midpoint_mph:
            position = 'ABOVE_TYPICAL'  # Between midpoint and max
        elif actual_bat_speed_mph >= capacity_min_mph:
            position = 'BELOW_TYPICAL'  # Between min and midpoint
        else:
            position = 'BELOW_MINIMUM'  # Below theoretical minimum
        
        # Determine status
        if capacity_used_pct >= 95:
            status = 'ELITE'
        elif capacity_used_pct >= 85:
            status = 'GOOD'
        elif capacity_used_pct >= 75:
            status = 'AVERAGE'
        elif capacity_used_pct >= 65:
            status = 'BELOW_AVERAGE'
        else:
            status = 'UNDERTRAINED'
        
        return {
            'actual_mph': round(actual_bat_speed_mph, 1),
            'capacity_range': f'{capacity_min_mph:.0f}-{capacity_max_mph:.0f} mph',
            'capacity_midpoint_mph': round(capacity_midpoint_mph, 1),
            'gap_to_midpoint_mph': round(gap_to_midpoint, 1),
            'gap_to_max_mph': round(gap_to_max, 1),
            'capacity_used_pct': round(capacity_used_pct, 1),
            'capacity_untapped_pct': round(capacity_untapped_pct, 1),
            'position_in_range': position,
            'status': status
        }
    
    def predict_with_fixes(
        self,
        actual_bat_speed_mph: float,
        total_potential_gain_mph: float,
        capacity_max_mph: float
    ) -> Dict:
        """
        Predict bat speed after fixing energy leaks
        
        Args:
            actual_bat_speed_mph: Current bat speed
            total_potential_gain_mph: Total gain if all leaks fixed
            capacity_max_mph: Maximum capacity ceiling
            
        Returns:
            Prediction with leak fixes:
            {
                'current_mph': 67.0,
                'predicted_with_fixes_mph': 74.8,
                'predicted_gain_mph': 7.8,
                'capacity_max_mph': 85.0,
                'remaining_to_max_mph': 10.2,
                'pct_of_capacity_after_fixes': 88.0
            }
        """
        # Predict bat speed after fixes
        predicted_mph = actual_bat_speed_mph + total_potential_gain_mph
        
        # Cap at maximum capacity (can't exceed theoretical ceiling)
        predicted_mph = min(predicted_mph, capacity_max_mph)
        
        # Calculate actual gain (might be less than potential if capped)
        predicted_gain = predicted_mph - actual_bat_speed_mph
        
        # Remaining capacity after fixes
        remaining_to_max = capacity_max_mph - predicted_mph
        
        # Percentage of capacity after fixes
        if capacity_max_mph > 0:
            pct_after_fixes = (predicted_mph / capacity_max_mph) * 100
        else:
            pct_after_fixes = 0.0
        
        return {
            'current_mph': round(actual_bat_speed_mph, 1),
            'predicted_with_fixes_mph': round(predicted_mph, 1),
            'predicted_gain_mph': round(predicted_gain, 1),
            'capacity_max_mph': round(capacity_max_mph, 1),
            'remaining_to_max_mph': round(remaining_to_max, 1),
            'pct_of_capacity_after_fixes': round(pct_after_fixes, 1)
        }
    
    def generate_capacity_summary(
        self,
        capacity_gap: Dict,
        leak_prescription: Dict
    ) -> str:
        """
        Generate human-readable summary of capacity analysis
        
        Args:
            capacity_gap: Output from calculate_capacity_gap()
            leak_prescription: Output from EfficiencyAnalyzer.generate_leak_prescription()
            
        Returns:
            Summary string
        """
        summary = (
            f"Your body has {capacity_gap['capacity_range']} capacity. "
            f"You're using {capacity_gap['capacity_used_pct']}% of it "
            f"({capacity_gap['actual_mph']} mph actual). "
            f"Fix {leak_prescription['primary_focus']} leaks "
            f"(+{leak_prescription['primary_estimated_gain_mph']} mph gain) "
            f"to reach {capacity_gap['capacity_midpoint_mph']} mph."
        )
        
        return summary
    
    def complete_capacity_analysis(
        self,
        actual_bat_speed_mph: float,
        capacity_min_mph: float,
        capacity_midpoint_mph: float,
        capacity_max_mph: float,
        ground_score: float,
        engine_score: float,
        weapon_score: float,
        total_potential_gain_mph: float,
        leak_prescription: Dict
    ) -> Dict:
        """
        Complete capacity analysis with all metrics
        
        This is the MAIN integration method for Priority 9
        
        Args:
            actual_bat_speed_mph: Measured bat speed
            capacity_min_mph: Minimum capacity
            capacity_midpoint_mph: Midpoint capacity
            capacity_max_mph: Maximum capacity
            ground_score: Ground score
            engine_score: Engine score
            weapon_score: Weapon score
            total_potential_gain_mph: Total potential gain from fixing leaks
            leak_prescription: Prescription from EfficiencyAnalyzer
            
        Returns:
            Complete capacity analysis
        """
        # Calculate capacity gap
        capacity_gap = self.calculate_capacity_gap(
            actual_bat_speed_mph,
            capacity_min_mph,
            capacity_midpoint_mph,
            capacity_max_mph
        )
        
        # Predict with fixes
        prediction = self.predict_with_fixes(
            actual_bat_speed_mph,
            total_potential_gain_mph,
            capacity_max_mph
        )
        
        # Generate summary
        summary = self.generate_capacity_summary(capacity_gap, leak_prescription)
        
        return {
            'capacity_gap': capacity_gap,
            'prediction_with_fixes': prediction,
            'leak_prescription': leak_prescription,
            'summary': summary,
            'component_scores': {
                'ground': round(ground_score, 1),
                'engine': round(engine_score, 1),
                'weapon': round(weapon_score, 1)
            }
        }


if __name__ == "__main__":
    # Test with Eric Williams data
    print("="*70)
    print("CAPACITY GAP ANALYZER TEST - ERIC WILLIAMS")
    print("="*70)
    
    analyzer = CapacityGapAnalyzer()
    
    # Eric's data
    actual_bat_speed = 67  # mph
    capacity_min = 75  # mph
    capacity_midpoint = 76.1  # mph (85% efficiency)
    capacity_max = 85  # mph
    
    # Component scores
    ground_score = 72
    engine_score = 85
    weapon_score = 40
    
    # Leak prescription (mock)
    leak_prescription = {
        'primary_focus': 'GROUND',
        'primary_leak_severity': 'HIGH',
        'primary_estimated_gain_mph': 1.95,
        'secondary_focus': 'WEAPON',
        'total_available_gain_mph': 3.8
    }
    
    # Run analysis
    analysis = analyzer.complete_capacity_analysis(
        actual_bat_speed,
        capacity_min,
        capacity_midpoint,
        capacity_max,
        ground_score,
        engine_score,
        weapon_score,
        leak_prescription['total_available_gain_mph'],
        leak_prescription
    )
    
    print("\n📊 CAPACITY GAP:")
    gap = analysis['capacity_gap']
    print(f"   Actual: {gap['actual_mph']} mph")
    print(f"   Capacity Range: {gap['capacity_range']}")
    print(f"   Midpoint: {gap['capacity_midpoint_mph']} mph")
    print(f"   Gap to Midpoint: {gap['gap_to_midpoint_mph']} mph")
    print(f"   Gap to Max: {gap['gap_to_max_mph']} mph")
    print(f"   Capacity Used: {gap['capacity_used_pct']}%")
    print(f"   Capacity Untapped: {gap['capacity_untapped_pct']}%")
    print(f"   Position: {gap['position_in_range']}")
    print(f"   Status: {gap['status']}")
    
    print("\n🔮 PREDICTION WITH FIXES:")
    pred = analysis['prediction_with_fixes']
    print(f"   Current: {pred['current_mph']} mph")
    print(f"   After Fixes: {pred['predicted_with_fixes_mph']} mph")
    print(f"   Gain: +{pred['predicted_gain_mph']} mph")
    print(f"   Remaining to Max: {pred['remaining_to_max_mph']} mph")
    print(f"   % of Capacity After Fixes: {pred['pct_of_capacity_after_fixes']}%")
    
    print(f"\n💊 PRESCRIPTION:")
    presc = analysis['leak_prescription']
    print(f"   Focus: {presc['primary_focus']} ({presc['primary_leak_severity']})")
    print(f"   Expected Gain: +{presc['primary_estimated_gain_mph']} mph")
    print(f"   Total Available: +{presc['total_available_gain_mph']} mph")
    
    print(f"\n📝 SUMMARY:")
    print(f"   {analysis['summary']}")
    
    print("\n" + "="*70)
