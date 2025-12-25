"""
Ball Outcome Predictor for Swing DNA Analysis
=============================================

Predicts current and future ball outcomes based on biomechanical metrics:
- Exit velocity
- Launch angle
- Batted ball distribution (GB%, LD%, FB%)
- Spray chart (pull%, center%, oppo%)
- Breaking ball performance
"""

from typing import Dict
from dataclasses import dataclass
from .csv_parser import SwingMetrics
from .efficiency_calculator import EfficiencyScores


@dataclass
class BallOutcomes:
    """Container for ball outcome predictions"""
    current: Dict
    predicted: Dict
    improvement: Dict


class BallOutcomePredictor:
    """Predict ball outcomes from biomechanical metrics"""
    
    def predict(
        self, 
        metrics: SwingMetrics, 
        efficiency: EfficiencyScores
    ) -> BallOutcomes:
        """
        Predict current and future ball outcomes
        
        Args:
            metrics: SwingMetrics from CSV parser
            efficiency: EfficiencyScores from efficiency calculator
            
        Returns:
            BallOutcomes object with current, predicted, and improvement
        """
        # Calculate current outcomes
        current = self._calculate_current_outcomes(metrics, efficiency)
        
        # Calculate predicted outcomes (after training)
        predicted = self._calculate_predicted_outcomes(metrics, efficiency)
        
        # Calculate improvement
        improvement = self._calculate_improvement(current, predicted)
        
        return BallOutcomes(
            current=current,
            predicted=predicted,
            improvement=improvement
        )
    
    def _calculate_current_outcomes(
        self, 
        metrics: SwingMetrics, 
        efficiency: EfficiencyScores
    ) -> Dict:
        """Calculate current ball outcomes"""
        
        # Exit velocity based on bat speed and efficiency
        bat_speed = metrics.bat_speed
        total_eff = efficiency.total_efficiency / 100.0
        exit_velo = bat_speed * total_eff
        
        # Launch angle based on lead arm extension
        arm_ext = metrics.lead_arm_extension
        if arm_ext < 5:
            launch_angle = 2  # Severe ground ball tendency
            gb_rate = 65
            ld_rate = 25
            fb_rate = 10
            breaking_ball_avg = 0.180
            opposite_field_avg = 0.150
            pull_pct = 60
            center_pct = 25
            oppo_pct = 15
        elif arm_ext < 10:
            launch_angle = 8  # Ground ball tendency
            gb_rate = 55
            ld_rate = 35
            fb_rate = 10
            breaking_ball_avg = 0.220
            opposite_field_avg = 0.190
            pull_pct = 50
            center_pct = 30
            oppo_pct = 20
        elif arm_ext < 15:
            launch_angle = 12  # Balanced
            gb_rate = 40
            ld_rate = 45
            fb_rate = 15
            breaking_ball_avg = 0.260
            opposite_field_avg = 0.230
            pull_pct = 45
            center_pct = 35
            oppo_pct = 20
        else:
            launch_angle = 15  # Optimal line drive
            gb_rate = 35
            ld_rate = 55
            fb_rate = 10
            breaking_ball_avg = 0.280
            opposite_field_avg = 0.250
            pull_pct = 40
            center_pct = 35
            oppo_pct = 25
        
        # Spin rate and type
        if arm_ext < 10:
            spin_rate = 2800  # Topspin
            spin_type = "topspin"
        else:
            spin_rate = -1200  # Backspin (negative indicates direction)
            spin_type = "backspin"
        
        return {
            'exit_velo': round(exit_velo, 1),
            'launch_angle': launch_angle,
            'gb_rate': gb_rate,
            'ld_rate': ld_rate,
            'fb_rate': fb_rate,
            'breaking_ball_avg': breaking_ball_avg,
            'opposite_field_avg': opposite_field_avg,
            'spray_chart': {
                'pull_pct': pull_pct,
                'center_pct': center_pct,
                'oppo_pct': oppo_pct
            },
            'spin_rate': spin_rate,
            'spin_type': spin_type
        }
    
    def _calculate_predicted_outcomes(
        self, 
        metrics: SwingMetrics, 
        efficiency: EfficiencyScores
    ) -> Dict:
        """Calculate predicted outcomes after training"""
        
        bat_speed = metrics.bat_speed
        
        # Target efficiency after training (80-90%)
        target_efficiency = 0.85
        
        # Predicted exit velocity
        predicted_exit_velo = bat_speed * target_efficiency
        
        # Predicted optimal outcomes
        predicted_la = 15  # Optimal line drive angle
        predicted_gb_rate = 35  # Reduced ground balls
        predicted_ld_rate = 55  # Increased line drives
        predicted_fb_rate = 10  # Maintained fly balls
        
        # Improved contact quality
        predicted_bb_avg = 0.280 if efficiency.total_efficiency < 50 else 0.300
        predicted_oppo_avg = 0.240 if efficiency.total_efficiency < 50 else 0.270
        
        # More balanced spray chart
        predicted_pull = 40
        predicted_center = 35
        predicted_oppo = 25
        
        # Backspin for better carry
        predicted_spin_rate = -1200
        predicted_spin_type = "backspin"
        
        return {
            'exit_velo': round(predicted_exit_velo, 1),
            'launch_angle': predicted_la,
            'gb_rate': predicted_gb_rate,
            'ld_rate': predicted_ld_rate,
            'fb_rate': predicted_fb_rate,
            'breaking_ball_avg': predicted_bb_avg,
            'opposite_field_avg': predicted_oppo_avg,
            'spray_chart': {
                'pull_pct': predicted_pull,
                'center_pct': predicted_center,
                'oppo_pct': predicted_oppo
            },
            'spin_rate': predicted_spin_rate,
            'spin_type': predicted_spin_type
        }
    
    def _calculate_improvement(self, current: Dict, predicted: Dict) -> Dict:
        """Calculate improvement between current and predicted"""
        return {
            'exit_velo_gain': round(predicted['exit_velo'] - current['exit_velo'], 1),
            'launch_angle_gain': predicted['launch_angle'] - current['launch_angle'],
            'gb_rate_change': predicted['gb_rate'] - current['gb_rate'],
            'ld_rate_change': predicted['ld_rate'] - current['ld_rate'],
            'fb_rate_change': predicted['fb_rate'] - current['fb_rate'],
            'breaking_ball_avg_gain': round(predicted['breaking_ball_avg'] - current['breaking_ball_avg'], 3),
            'opposite_field_avg_gain': round(predicted['opposite_field_avg'] - current['opposite_field_avg'], 3)
        }
    
    def to_dict(self, outcomes: BallOutcomes) -> Dict:
        """Convert BallOutcomes to dictionary"""
        return {
            'current': outcomes.current,
            'predicted': outcomes.predicted,
            'improvement': outcomes.improvement
        }


# Example usage
if __name__ == "__main__":
    from .csv_parser import SwingMetrics
    from .efficiency_calculator import EfficiencyScores
    
    # Eric Williams example
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
    
    efficiency = EfficiencyScores(
        hip_efficiency=21.0,
        knee_efficiency=0.2,
        contact_efficiency=7.5,
        total_efficiency=11.2
    )
    
    predictor = BallOutcomePredictor()
    outcomes = predictor.predict(metrics, efficiency)
    
    print("⚾ Ball Outcome Predictions:")
    print(f"\nCurrent:")
    print(f"  Exit Velo: {outcomes.current['exit_velo']} mph")
    print(f"  Launch Angle: {outcomes.current['launch_angle']}°")
    print(f"  Ground Ball Rate: {outcomes.current['gb_rate']}%")
    
    print(f"\nPredicted:")
    print(f"  Exit Velo: {outcomes.predicted['exit_velo']} mph")
    print(f"  Launch Angle: {outcomes.predicted['launch_angle']}°")
    print(f"  Ground Ball Rate: {outcomes.predicted['gb_rate']}%")
    
    print(f"\nImprovement:")
    print(f"  Exit Velo Gain: +{outcomes.improvement['exit_velo_gain']} mph")
    print(f"  Launch Angle Gain: +{outcomes.improvement['launch_angle_gain']}°")
    print(f"  GB Rate Change: {outcomes.improvement['gb_rate_change']}%")
