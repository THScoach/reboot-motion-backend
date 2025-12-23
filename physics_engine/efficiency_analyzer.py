"""
Efficiency Analyzer Module
Identifies energy leaks and inefficiencies in the kinetic chain

Part of Priority 9: Kinetic Capacity Framework
Localizes where energy is being lost (Ground, Engine, Weapon)
"""

from typing import Dict, List, Tuple
import logging

logger = logging.getLogger(__name__)


class EfficiencyAnalyzer:
    """
    Analyzes efficiency and identifies energy leaks in the kinetic chain
    Shows WHERE capacity is being lost (Ground vs Engine vs Weapon)
    """
    
    # Thresholds for leak severity
    LEAK_CRITICAL = 50  # Score below 50 = CRITICAL leak
    LEAK_HIGH = 65      # Score below 65 = HIGH leak
    LEAK_MEDIUM = 80    # Score below 80 = MEDIUM leak
    LEAK_LOW = 90       # Score below 90 = LOW leak
    
    # Expected gains per component fix (mph)
    GAIN_PER_POINT = {
        'GROUND': 0.15,   # 0.15 mph per point improvement
        'ENGINE': 0.12,   # 0.12 mph per point improvement
        'WEAPON': 0.10    # 0.10 mph per point improvement
    }
    
    def __init__(self):
        """Initialize efficiency analyzer"""
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def analyze_component_efficiency(
        self,
        component_name: str,
        score: float,
        target_score: float = 85.0
    ) -> Dict:
        """
        Analyze efficiency of a single component (Ground, Engine, or Weapon)
        
        Args:
            component_name: 'GROUND', 'ENGINE', or 'WEAPON'
            score: Current score (0-100)
            target_score: Target score (default 85)
            
        Returns:
            Dictionary with efficiency analysis:
            {
                'component': 'GROUND',
                'score': 72.0,
                'leak_severity': 'MEDIUM',
                'efficiency_pct': 84.7,
                'points_to_target': 13.0,
                'estimated_gain_mph': 1.95
            }
        """
        # Calculate leak severity
        if score < self.LEAK_CRITICAL:
            leak_severity = 'CRITICAL'
        elif score < self.LEAK_HIGH:
            leak_severity = 'HIGH'
        elif score < self.LEAK_MEDIUM:
            leak_severity = 'MEDIUM'
        elif score < self.LEAK_LOW:
            leak_severity = 'LOW'
        else:
            leak_severity = 'NONE'
        
        # Calculate efficiency as percentage of target
        efficiency_pct = (score / target_score) * 100 if target_score > 0 else 0
        
        # Calculate points needed to reach target
        points_to_target = max(0, target_score - score)
        
        # Estimate potential gain if fixed
        gain_per_point = self.GAIN_PER_POINT.get(component_name, 0.10)
        estimated_gain_mph = points_to_target * gain_per_point
        
        return {
            'component': component_name,
            'score': round(score, 1),
            'leak_severity': leak_severity,
            'efficiency_pct': round(efficiency_pct, 1),
            'points_to_target': round(points_to_target, 1),
            'estimated_gain_mph': round(estimated_gain_mph, 1)
        }
    
    def identify_energy_leaks(
        self,
        ground_score: float,
        engine_score: float,
        weapon_score: float
    ) -> Dict:
        """
        Identify all energy leaks across the kinetic chain
        
        Args:
            ground_score: Ground (lower body) score 0-100
            engine_score: Engine (torso rotation) score 0-100
            weapon_score: Weapon (bat path) score 0-100
            
        Returns:
            Dictionary with leak analysis and priority ranking:
            {
                'ground': {...},
                'engine': {...},
                'weapon': {...},
                'priority_order': ['GROUND', 'WEAPON', 'ENGINE'],
                'total_potential_gain_mph': 5.2,
                'weakest_link': 'GROUND'
            }
        """
        # Analyze each component
        ground_analysis = self.analyze_component_efficiency('GROUND', ground_score)
        engine_analysis = self.analyze_component_efficiency('ENGINE', engine_score)
        weapon_analysis = self.analyze_component_efficiency('WEAPON', weapon_score)
        
        # Sort by severity (lowest score first)
        components = [
            (ground_analysis, ground_score),
            (engine_analysis, engine_score),
            (weapon_analysis, weapon_score)
        ]
        components_sorted = sorted(components, key=lambda x: x[1])
        
        # Priority order (weakest first)
        priority_order = [comp[0]['component'] for comp in components_sorted]
        
        # Calculate total potential gain
        total_gain = (
            ground_analysis['estimated_gain_mph'] +
            engine_analysis['estimated_gain_mph'] +
            weapon_analysis['estimated_gain_mph']
        )
        
        # Identify weakest link
        weakest_link = priority_order[0]
        
        return {
            'ground': ground_analysis,
            'engine': engine_analysis,
            'weapon': weapon_analysis,
            'priority_order': priority_order,
            'total_potential_gain_mph': round(total_gain, 1),
            'weakest_link': weakest_link
        }
    
    def calculate_overall_efficiency(
        self,
        ground_score: float,
        engine_score: float,
        weapon_score: float
    ) -> Dict:
        """
        Calculate overall efficiency of the kinetic chain
        
        Args:
            ground_score: Ground score 0-100
            engine_score: Engine score 0-100
            weapon_score: Weapon score 0-100
            
        Returns:
            Dictionary with overall efficiency metrics:
            {
                'overall_efficiency_pct': 76.1,
                'average_score': 65.7,
                'grade': 'C',
                'bottleneck': 'WEAPON',
                'status': 'BELOW_AVERAGE'
            }
        """
        # Calculate average score
        avg_score = (ground_score + engine_score + weapon_score) / 3.0
        
        # Overall efficiency (as percentage of perfect 100)
        overall_efficiency = avg_score
        
        # Determine grade
        if avg_score >= 90:
            grade = 'A'
            status = 'ELITE'
        elif avg_score >= 80:
            grade = 'B'
            status = 'GOOD'
        elif avg_score >= 70:
            grade = 'C'
            status = 'AVERAGE'
        elif avg_score >= 60:
            grade = 'D'
            status = 'BELOW_AVERAGE'
        else:
            grade = 'F'
            status = 'UNDERTRAINED'
        
        # Identify bottleneck (lowest score)
        components = {
            'GROUND': ground_score,
            'ENGINE': engine_score,
            'WEAPON': weapon_score
        }
        bottleneck = min(components, key=components.get)
        
        return {
            'overall_efficiency_pct': round(overall_efficiency, 1),
            'average_score': round(avg_score, 1),
            'grade': grade,
            'bottleneck': bottleneck,
            'status': status
        }
    
    def generate_leak_prescription(
        self,
        leaks: Dict,
        capacity_gap_mph: float
    ) -> Dict:
        """
        Generate actionable prescription for fixing energy leaks
        
        Args:
            leaks: Output from identify_energy_leaks()
            capacity_gap_mph: Gap between actual and capacity midpoint
            
        Returns:
            Prescription with focus area and expected gains:
            {
                'primary_focus': 'GROUND',
                'primary_leak_severity': 'HIGH',
                'primary_estimated_gain_mph': 1.95,
                'secondary_focus': 'WEAPON',
                'total_available_gain_mph': 3.8,
                'focus_strategy': 'Fix GROUND first (HIGH priority)...'
            }
        """
        # Get priority order
        priority_order = leaks['priority_order']
        primary_focus = priority_order[0]
        secondary_focus = priority_order[1] if len(priority_order) > 1 else None
        
        # Get details for primary focus
        primary_analysis = leaks[primary_focus.lower()]
        
        # Generate strategy text
        focus_strategy = (
            f"Fix {primary_focus} first ({primary_analysis['leak_severity']} priority). "
            f"Expected gain: +{primary_analysis['estimated_gain_mph']} mph. "
        )
        
        if secondary_focus:
            secondary_analysis = leaks[secondary_focus.lower()]
            focus_strategy += (
                f"Then address {secondary_focus} ({secondary_analysis['leak_severity']} priority) "
                f"for an additional +{secondary_analysis['estimated_gain_mph']} mph."
            )
        
        return {
            'primary_focus': primary_focus,
            'primary_leak_severity': primary_analysis['leak_severity'],
            'primary_estimated_gain_mph': primary_analysis['estimated_gain_mph'],
            'secondary_focus': secondary_focus,
            'total_available_gain_mph': leaks['total_potential_gain_mph'],
            'focus_strategy': focus_strategy,
            'capacity_gap_mph': round(capacity_gap_mph, 1)
        }
    
    def compare_to_capacity(
        self,
        actual_bat_speed_mph: float,
        capacity_midpoint_mph: float,
        capacity_max_mph: float,
        ground_score: float,
        engine_score: float,
        weapon_score: float
    ) -> Dict:
        """
        Complete analysis: Compare actual performance to capacity and identify leaks
        
        This is the MAIN method that ties everything together
        
        Args:
            actual_bat_speed_mph: Measured bat speed
            capacity_midpoint_mph: Calculated capacity midpoint (85% efficiency)
            capacity_max_mph: Calculated capacity max (95% efficiency)
            ground_score: Ground score
            engine_score: Engine score
            weapon_score: Weapon score
            
        Returns:
            Complete analysis with capacity comparison and leak identification
        """
        # Identify energy leaks
        leaks = self.identify_energy_leaks(ground_score, engine_score, weapon_score)
        
        # Calculate overall efficiency
        overall = self.calculate_overall_efficiency(ground_score, engine_score, weapon_score)
        
        # Calculate capacity gaps
        gap_to_midpoint = capacity_midpoint_mph - actual_bat_speed_mph
        gap_to_max = capacity_max_mph - actual_bat_speed_mph
        
        # Generate prescription
        prescription = self.generate_leak_prescription(leaks, gap_to_midpoint)
        
        return {
            'actual_bat_speed_mph': round(actual_bat_speed_mph, 1),
            'capacity_midpoint_mph': round(capacity_midpoint_mph, 1),
            'capacity_max_mph': round(capacity_max_mph, 1),
            'gap_to_midpoint_mph': round(gap_to_midpoint, 1),
            'gap_to_max_mph': round(gap_to_max, 1),
            'overall_efficiency': overall,
            'energy_leaks': leaks,
            'prescription': prescription
        }


if __name__ == "__main__":
    # Test with Eric Williams data
    print("="*70)
    print("EFFICIENCY ANALYZER TEST - ERIC WILLIAMS")
    print("="*70)
    
    analyzer = EfficiencyAnalyzer()
    
    # Eric's scores
    ground_score = 72
    engine_score = 85
    weapon_score = 40
    
    # Eric's performance
    actual_bat_speed = 67  # mph (Blast sensor)
    capacity_midpoint = 76.1  # mph (from capacity calculator)
    capacity_max = 83.5  # mph
    
    # Run complete analysis
    analysis = analyzer.compare_to_capacity(
        actual_bat_speed,
        capacity_midpoint,
        capacity_max,
        ground_score,
        engine_score,
        weapon_score
    )
    
    print(f"\n📊 PERFORMANCE vs CAPACITY:")
    print(f"   Actual: {analysis['actual_bat_speed_mph']} mph")
    print(f"   Capacity Midpoint: {analysis['capacity_midpoint_mph']} mph")
    print(f"   Capacity Max: {analysis['capacity_max_mph']} mph")
    print(f"   Gap to Midpoint: {analysis['gap_to_midpoint_mph']} mph")
    print(f"   Gap to Max: {analysis['gap_to_max_mph']} mph")
    
    print(f"\n⚡ OVERALL EFFICIENCY:")
    print(f"   Efficiency: {analysis['overall_efficiency']['overall_efficiency_pct']}%")
    print(f"   Grade: {analysis['overall_efficiency']['grade']}")
    print(f"   Status: {analysis['overall_efficiency']['status']}")
    print(f"   Bottleneck: {analysis['overall_efficiency']['bottleneck']}")
    
    print(f"\n🔍 ENERGY LEAKS:")
    for comp in ['ground', 'engine', 'weapon']:
        leak = analysis['energy_leaks'][comp]
        print(f"   {leak['component']}: {leak['score']}/100 "
              f"({leak['leak_severity']} leak, +{leak['estimated_gain_mph']} mph potential)")
    
    print(f"\n   Priority Order: {' → '.join(analysis['energy_leaks']['priority_order'])}")
    print(f"   Total Potential Gain: +{analysis['energy_leaks']['total_potential_gain_mph']} mph")
    
    print(f"\n💊 PRESCRIPTION:")
    presc = analysis['prescription']
    print(f"   Primary Focus: {presc['primary_focus']} ({presc['primary_leak_severity']} priority)")
    print(f"   Expected Gain: +{presc['primary_estimated_gain_mph']} mph")
    if presc['secondary_focus']:
        print(f"   Secondary Focus: {presc['secondary_focus']}")
    print(f"   Total Available: +{presc['total_available_gain_mph']} mph")
    print(f"\n   Strategy: {presc['focus_strategy']}")
    
    print("\n" + "="*70)
