"""
Gap Analysis Module
Compares actual performance to potential and identifies improvement opportunities

Part of Priority 3: Gap Analysis & Recommendations
"""

from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class GapAnalyzer:
    """
    Analyzes the gap between actual performance and potential
    Provides metrics on what percentage of potential has been achieved
    """
    
    def __init__(self):
        pass
    
    def calculate_bat_speed_gap(
        self,
        actual_bat_speed_mph: float,
        potential_bat_speed_mph: float
    ) -> Dict:
        """
        Calculate bat speed gap metrics
        
        Args:
            actual_bat_speed_mph: Measured bat speed from video/sensors
            potential_bat_speed_mph: Calculated potential from anthropometry
            
        Returns:
            Dictionary with gap analysis
        """
        if potential_bat_speed_mph <= 0:
            return {
                'actual_mph': round(actual_bat_speed_mph, 1),
                'potential_mph': 0.0,
                'gap_mph': 0.0,
                'pct_achieved': 0.0,
                'pct_untapped': 0.0,
                'status': 'UNKNOWN'
            }
        
        gap_mph = potential_bat_speed_mph - actual_bat_speed_mph
        pct_achieved = (actual_bat_speed_mph / potential_bat_speed_mph) * 100
        pct_untapped = 100 - pct_achieved
        
        # Determine status
        if pct_achieved >= 95:
            status = 'ELITE'
        elif pct_achieved >= 85:
            status = 'GOOD'
        elif pct_achieved >= 70:
            status = 'BELOW_POTENTIAL'
        else:
            status = 'UNDERTRAINED'
        
        return {
            'actual_mph': round(actual_bat_speed_mph, 1),
            'potential_mph': round(potential_bat_speed_mph, 1),
            'gap_mph': round(gap_mph, 1),
            'pct_achieved': round(pct_achieved, 1),
            'pct_untapped': round(pct_untapped, 1),
            'status': status
        }
    
    def calculate_exit_velocity_gap(
        self,
        actual_exit_velo_mph: float,
        potential_exit_velo_mph: float
    ) -> Dict:
        """
        Calculate exit velocity gap metrics
        
        Args:
            actual_exit_velo_mph: Measured exit velocity
            potential_exit_velo_mph: Calculated potential exit velocity
            
        Returns:
            Dictionary with gap analysis
        """
        if potential_exit_velo_mph <= 0:
            return {
                'actual_mph': round(actual_exit_velo_mph, 1),
                'potential_mph': 0.0,
                'gap_mph': 0.0,
                'pct_achieved': 0.0,
                'pct_untapped': 0.0,
                'status': 'UNKNOWN'
            }
        
        gap_mph = potential_exit_velo_mph - actual_exit_velo_mph
        pct_achieved = (actual_exit_velo_mph / potential_exit_velo_mph) * 100
        pct_untapped = 100 - pct_achieved
        
        if pct_achieved >= 95:
            status = 'ELITE'
        elif pct_achieved >= 85:
            status = 'GOOD'
        elif pct_achieved >= 70:
            status = 'BELOW_POTENTIAL'
        else:
            status = 'UNDERTRAINED'
        
        return {
            'actual_mph': round(actual_exit_velo_mph, 1),
            'potential_mph': round(potential_exit_velo_mph, 1),
            'gap_mph': round(gap_mph, 1),
            'pct_achieved': round(pct_achieved, 1),
            'pct_untapped': round(pct_untapped, 1),
            'status': status
        }
    
    def identify_weakest_component(
        self,
        ground_score: float,
        engine_score: float,
        weapon_score: float
    ) -> Dict:
        """
        Identify which component is weakest and should be prioritized
        
        Args:
            ground_score: Ground (lower body) score 0-100
            engine_score: Engine (torso rotation) score 0-100
            weapon_score: Weapon (bat speed through zone) score 0-100
            
        Returns:
            Dictionary with weakest component analysis
        """
        components = {
            'GROUND': ground_score,
            'ENGINE': engine_score,
            'WEAPON': weapon_score
        }
        
        # Sort by score (lowest first)
        sorted_components = sorted(components.items(), key=lambda x: x[1])
        weakest_name, weakest_score = sorted_components[0]
        
        # Determine priority level
        if weakest_score < 50:
            priority = 'CRITICAL'
        elif weakest_score < 65:
            priority = 'HIGH'
        elif weakest_score < 80:
            priority = 'MEDIUM'
        else:
            priority = 'LOW'
        
        return {
            'weakest_component': weakest_name,
            'score': round(weakest_score, 1),
            'priority': priority,
            'components_ranked': [(name, round(score, 1)) for name, score in sorted_components]
        }
    
    def calculate_complete_gap_analysis(
        self,
        actual_metrics: Dict,
        potential_metrics: Dict,
        scores: Dict
    ) -> Dict:
        """
        Complete gap analysis combining all metrics
        
        Args:
            actual_metrics: {'bat_speed_mph': 57.9, 'exit_velocity_mph': 96.7}
            potential_metrics: {'bat_speed_mph': 76.0, 'exit_velocity_pitched_mph': 122.9}
            scores: {'ground': 72, 'engine': 85, 'weapon': 40}
            
        Returns:
            Complete gap analysis dictionary
        """
        # Calculate bat speed gap
        bat_speed_gap = self.calculate_bat_speed_gap(
            actual_metrics.get('bat_speed_mph', 0),
            potential_metrics.get('bat_speed_mph', 0)
        )
        
        # Calculate exit velocity gap (if available)
        exit_velo_gap = None
        if 'exit_velocity_mph' in actual_metrics and 'exit_velocity_pitched_mph' in potential_metrics:
            exit_velo_gap = self.calculate_exit_velocity_gap(
                actual_metrics['exit_velocity_mph'],
                potential_metrics['exit_velocity_pitched_mph']
            )
        
        # Identify weakest component
        weakest = self.identify_weakest_component(
            scores.get('ground', 0),
            scores.get('engine', 0),
            scores.get('weapon', 0)
        )
        
        # Calculate overall efficiency (average of G-E-W scores)
        overall_efficiency = (
            scores.get('ground', 0) + 
            scores.get('engine', 0) + 
            scores.get('weapon', 0)
        ) / 3
        
        # Generate summary
        summary = (
            f"Achieving {bat_speed_gap['pct_achieved']}% of bat speed potential "
            f"({bat_speed_gap['gap_mph']} mph gap). "
            f"Focus on {weakest['weakest_component']} (score: {weakest['score']}) "
            f"for improvement. Overall efficiency: {round(overall_efficiency, 1)}%"
        )
        
        result = {
            'bat_speed': bat_speed_gap,
            'weakest_component': weakest,
            'overall_efficiency': round(overall_efficiency, 1),
            'summary': summary
        }
        
        # Add exit velocity if available
        if exit_velo_gap:
            result['exit_velocity'] = exit_velo_gap
        
        return result


if __name__ == "__main__":
    # Test with Eric Williams data
    print("="*70)
    print("GAP ANALYZER TEST - ERIC WILLIAMS")
    print("="*70)
    
    analyzer = GapAnalyzer()
    
    # Test data
    actual = {
        'bat_speed_mph': 57.9,
        'exit_velocity_mph': 96.7
    }
    
    potential = {
        'bat_speed_mph': 76.0,
        'exit_velocity_pitched_mph': 122.9
    }
    
    scores = {
        'ground': 72,
        'engine': 85,
        'weapon': 40
    }
    
    # Run analysis
    gap_analysis = analyzer.calculate_complete_gap_analysis(actual, potential, scores)
    
    # Display results
    print("\nBat Speed Gap:")
    print(f"  Actual: {gap_analysis['bat_speed']['actual_mph']} mph")
    print(f"  Potential: {gap_analysis['bat_speed']['potential_mph']} mph")
    print(f"  Gap: {gap_analysis['bat_speed']['gap_mph']} mph")
    print(f"  % Achieved: {gap_analysis['bat_speed']['pct_achieved']}%")
    print(f"  Status: {gap_analysis['bat_speed']['status']}")
    
    print("\nWeakest Component:")
    print(f"  Component: {gap_analysis['weakest_component']['weakest_component']}")
    print(f"  Score: {gap_analysis['weakest_component']['score']}/100")
    print(f"  Priority: {gap_analysis['weakest_component']['priority']}")
    
    print(f"\nOverall Efficiency: {gap_analysis['overall_efficiency']}%")
    print(f"\nSummary: {gap_analysis['summary']}")
    print("\n" + "="*70)
