"""
BAT MODULE - Reboot Motion Bat Optimization System
====================================================

Calculates bat specifications, Moment of Inertia (MOI), kinetic energy transfer,
and provides personalized bat weight recommendations.

Features:
- MOI calculation (from balance point or estimation)
- Bat kinetic energy calculation
- Body-to-bat energy transfer efficiency
- Optimal bat weight recommendations
- Exit velocity prediction with different bat weights

Author: Builder 2
Date: 2024-12-24
Version: 1.0.0
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import math


@dataclass
class BatSpecifications:
    """Bat physical specifications"""
    weight_oz: float
    length_inches: float
    model: Optional[str] = None
    balance_point_inches: Optional[float] = None  # From knob
    moi: Optional[float] = None  # kg·m² (calculated or provided)


@dataclass
class BatOptimizationResult:
    """Bat optimization analysis results"""
    current_bat: Dict
    bat_kinetic_energy_joules: float
    body_kinetic_energy_joules: float
    transfer_efficiency_percent: float
    optimal_weight_range_oz: Tuple[float, float]
    recommended_weights: List[Dict]
    exit_velo_predictions: List[Dict]
    optimization_notes: List[str]


class BatModule:
    """
    Bat Module for calculating MOI, energy transfer, and optimization recommendations.
    
    Key Equations:
    1. MOI (Moment of Inertia):
       - From balance point: MOI ≈ m * L² * k (k = 0.24-0.26 for baseball bats)
       - Estimation: MOI ≈ (weight_kg) * (length_m)² * 0.25
    
    2. Bat Kinetic Energy:
       KE_bat = 0.5 * MOI * (angular_velocity)²
       where angular_velocity = bat_speed / (2/3 * length)
    
    3. Transfer Efficiency:
       efficiency = (KE_bat / KE_body) * 100%
    """
    
    # Constants
    OZ_TO_KG = 0.0283495  # 1 oz = 0.0283495 kg
    INCHES_TO_M = 0.0254  # 1 inch = 0.0254 m
    MPH_TO_MS = 0.44704   # 1 mph = 0.44704 m/s
    
    # Bat MOI coefficient (dimensionless)
    MOI_COEFFICIENT_BALANCED = 0.25  # For balanced bats
    MOI_COEFFICIENT_END_LOADED = 0.27  # For end-loaded bats
    MOI_COEFFICIENT_LIGHT = 0.23  # For light/whippy bats
    
    # Exit velocity model coefficients (empirical)
    EXIT_VELO_MOI_FACTOR = 15.0  # mph per 0.01 kg·m² MOI
    EXIT_VELO_BAT_SPEED_FACTOR = 0.65  # Exit velo gain per bat speed mph
    
    def __init__(self):
        """Initialize Bat Module"""
        pass
    
    def calculate_moi(
        self,
        bat_weight_oz: float,
        bat_length_inches: float,
        balance_point_inches: Optional[float] = None,
        bat_type: str = "balanced"
    ) -> float:
        """
        Calculate bat Moment of Inertia (MOI).
        
        Args:
            bat_weight_oz: Bat weight in ounces
            bat_length_inches: Bat length in inches
            balance_point_inches: Balance point from knob (optional)
            bat_type: "balanced", "end_loaded", or "light"
        
        Returns:
            MOI in kg·m²
        
        Method 1 (if balance point known):
            MOI = m * L_balance² * k
            where L_balance is distance from knob to balance point
        
        Method 2 (estimation):
            MOI = m * L² * k
            k = 0.23-0.27 depending on bat type
        """
        # Convert to SI units
        mass_kg = bat_weight_oz * self.OZ_TO_KG
        length_m = bat_length_inches * self.INCHES_TO_M
        
        # Select MOI coefficient based on bat type
        if bat_type == "end_loaded":
            k = self.MOI_COEFFICIENT_END_LOADED
        elif bat_type == "light":
            k = self.MOI_COEFFICIENT_LIGHT
        else:
            k = self.MOI_COEFFICIENT_BALANCED
        
        if balance_point_inches:
            # Method 1: Use balance point (more accurate)
            balance_point_m = balance_point_inches * self.INCHES_TO_M
            moi = mass_kg * (balance_point_m ** 2) * k
        else:
            # Method 2: Estimate from total length
            moi = mass_kg * (length_m ** 2) * k
        
        return round(moi, 4)
    
    def calculate_bat_kinetic_energy(
        self,
        bat_speed_mph: float,
        bat_moi: float,
        bat_length_inches: float
    ) -> float:
        """
        Calculate bat kinetic energy at impact.
        
        Args:
            bat_speed_mph: Bat speed in mph
            bat_moi: Bat MOI in kg·m²
            bat_length_inches: Bat length in inches
        
        Returns:
            Kinetic energy in joules
        
        Equation:
            KE_bat = 0.5 * MOI * ω²
            where ω = v / r
            r ≈ (2/3) * bat_length (sweet spot distance)
        """
        # Convert bat speed to m/s
        bat_speed_ms = bat_speed_mph * self.MPH_TO_MS
        
        # Calculate rotation radius (sweet spot at ~2/3 of bat length)
        length_m = bat_length_inches * self.INCHES_TO_M
        rotation_radius_m = (2.0 / 3.0) * length_m
        
        # Calculate angular velocity (rad/s)
        angular_velocity = bat_speed_ms / rotation_radius_m
        
        # Calculate rotational kinetic energy
        bat_ke = 0.5 * bat_moi * (angular_velocity ** 2)
        
        return round(bat_ke, 1)
    
    def calculate_transfer_efficiency(
        self,
        bat_kinetic_energy: float,
        body_kinetic_energy: float
    ) -> float:
        """
        Calculate body-to-bat energy transfer efficiency.
        
        Args:
            bat_kinetic_energy: Bat KE in joules
            body_kinetic_energy: Body rotational KE in joules
        
        Returns:
            Transfer efficiency as percentage
        
        Elite players: 100-120% (can exceed 100% due to elastic energy storage)
        Good players: 80-100%
        Average players: 60-80%
        """
        if body_kinetic_energy == 0:
            return 0.0
        
        efficiency = (bat_kinetic_energy / body_kinetic_energy) * 100.0
        return round(efficiency, 1)
    
    def predict_exit_velocity(
        self,
        bat_speed_mph: float,
        bat_moi: float,
        pitch_speed_mph: float = 85.0,
        contact_quality: float = 1.0
    ) -> float:
        """
        Predict exit velocity based on bat speed and MOI.
        
        Args:
            bat_speed_mph: Bat speed in mph
            bat_moi: Bat MOI in kg·m²
            pitch_speed_mph: Pitch speed in mph (default 85)
            contact_quality: Contact quality factor 0.0-1.0 (default 1.0 = perfect)
        
        Returns:
            Predicted exit velocity in mph
        
        Empirical Model:
            Exit Velo = 0.65 * bat_speed + 0.15 * pitch_speed + MOI_factor
            MOI_factor = 15 * (MOI - 0.17)  # Bonus/penalty from MOI
        """
        # Base exit velocity (bat speed + pitch speed contribution)
        base_exit_velo = (self.EXIT_VELO_BAT_SPEED_FACTOR * bat_speed_mph +
                          0.15 * pitch_speed_mph)
        
        # MOI adjustment (relative to reference MOI of 0.17 kg·m²)
        moi_reference = 0.17
        moi_adjustment = self.EXIT_VELO_MOI_FACTOR * (bat_moi - moi_reference)
        
        # Total exit velocity
        exit_velo = base_exit_velo + moi_adjustment
        
        # Apply contact quality factor
        exit_velo *= contact_quality
        
        return round(exit_velo, 1)
    
    def recommend_bat_weights(
        self,
        current_bat_weight_oz: float,
        bat_length_inches: float,
        bat_speed_mph: float,
        body_kinetic_energy: float,
        transfer_efficiency: float,
        player_height_inches: float,
        player_weight_lbs: float
    ) -> List[Dict]:
        """
        Recommend optimal bat weights to test based on player profile.
        
        Args:
            current_bat_weight_oz: Current bat weight
            bat_length_inches: Bat length
            bat_speed_mph: Current bat speed
            body_kinetic_energy: Body KE in joules
            transfer_efficiency: Current transfer efficiency %
            player_height_inches: Player height
            player_weight_lbs: Player weight
        
        Returns:
            List of recommended bat weights with predictions
        
        Strategy:
        - Elite efficiency (>100%): Test heavier bats (+1-2 oz)
        - Good efficiency (80-100%): Test current ±1 oz
        - Low efficiency (<80%): Test lighter bats (-1-2 oz)
        """
        recommendations = []
        
        # Determine weight range based on transfer efficiency
        if transfer_efficiency >= 100:
            # Elite - can handle heavier bats
            weight_range = [
                current_bat_weight_oz - 1,
                current_bat_weight_oz,
                current_bat_weight_oz + 1,
                current_bat_weight_oz + 2
            ]
            optimization_strategy = "Elite efficiency - test heavier bats for more exit velo"
        elif transfer_efficiency >= 80:
            # Good - test moderate adjustments
            weight_range = [
                current_bat_weight_oz - 1,
                current_bat_weight_oz,
                current_bat_weight_oz + 1
            ]
            optimization_strategy = "Good efficiency - fine-tune with ±1 oz"
        else:
            # Needs improvement - try lighter bats
            weight_range = [
                current_bat_weight_oz - 2,
                current_bat_weight_oz - 1,
                current_bat_weight_oz
            ]
            optimization_strategy = "Try lighter bats to improve bat speed"
        
        # Calculate predictions for each weight
        for test_weight_oz in weight_range:
            if test_weight_oz < 26 or test_weight_oz > 36:
                continue  # Skip unrealistic weights
            
            # Estimate bat speed change (heavier = slower)
            # Rule of thumb: -0.5 mph per oz increase
            weight_diff = test_weight_oz - current_bat_weight_oz
            predicted_bat_speed = bat_speed_mph - (0.5 * weight_diff)
            
            # Calculate new MOI
            test_moi = self.calculate_moi(test_weight_oz, bat_length_inches)
            
            # Calculate new bat KE
            test_bat_ke = self.calculate_bat_kinetic_energy(
                predicted_bat_speed, test_moi, bat_length_inches
            )
            
            # Predict exit velocity
            test_exit_velo = self.predict_exit_velocity(
                predicted_bat_speed, test_moi
            )
            
            # Calculate new transfer efficiency
            test_efficiency = self.calculate_transfer_efficiency(
                test_bat_ke, body_kinetic_energy
            )
            
            recommendations.append({
                "bat_weight_oz": test_weight_oz,
                "predicted_bat_speed_mph": round(predicted_bat_speed, 1),
                "predicted_moi_kgm2": test_moi,
                "predicted_bat_ke_joules": test_bat_ke,
                "predicted_exit_velo_mph": test_exit_velo,
                "predicted_efficiency_percent": test_efficiency,
                "weight_change_oz": round(weight_diff, 1),
                "is_current": (test_weight_oz == current_bat_weight_oz)
            })
        
        return recommendations
    
    def analyze_bat_optimization(
        self,
        bat_weight_oz: float,
        bat_length_inches: float,
        bat_speed_mph: float,
        body_kinetic_energy: float,
        player_height_inches: float,
        player_weight_lbs: float,
        bat_model: Optional[str] = None,
        balance_point_inches: Optional[float] = None,
        bat_type: str = "balanced"
    ) -> BatOptimizationResult:
        """
        Complete bat optimization analysis.
        
        Args:
            bat_weight_oz: Current bat weight in oz
            bat_length_inches: Bat length in inches
            bat_speed_mph: Measured bat speed in mph
            body_kinetic_energy: Body rotational KE in joules
            player_height_inches: Player height
            player_weight_lbs: Player weight
            bat_model: Bat model name (optional)
            balance_point_inches: Balance point from knob (optional)
            bat_type: "balanced", "end_loaded", or "light"
        
        Returns:
            BatOptimizationResult with complete analysis
        """
        # Calculate current bat MOI
        current_moi = self.calculate_moi(
            bat_weight_oz, bat_length_inches, balance_point_inches, bat_type
        )
        
        # Calculate current bat kinetic energy
        bat_ke = self.calculate_bat_kinetic_energy(
            bat_speed_mph, current_moi, bat_length_inches
        )
        
        # Calculate transfer efficiency
        efficiency = self.calculate_transfer_efficiency(bat_ke, body_kinetic_energy)
        
        # Predict current exit velocity
        current_exit_velo = self.predict_exit_velocity(bat_speed_mph, current_moi)
        
        # Get bat weight recommendations
        recommendations = self.recommend_bat_weights(
            bat_weight_oz, bat_length_inches, bat_speed_mph,
            body_kinetic_energy, efficiency,
            player_height_inches, player_weight_lbs
        )
        
        # Determine optimal weight range
        if efficiency >= 100:
            optimal_range = (bat_weight_oz, bat_weight_oz + 2)
        elif efficiency >= 80:
            optimal_range = (bat_weight_oz - 1, bat_weight_oz + 1)
        else:
            optimal_range = (bat_weight_oz - 2, bat_weight_oz)
        
        # Generate optimization notes
        notes = []
        
        if efficiency >= 110:
            notes.append("🔥 Elite transfer efficiency (>110%) - you can handle heavier bats!")
        elif efficiency >= 100:
            notes.append("✅ Excellent transfer efficiency (100-110%) - test slightly heavier bats")
        elif efficiency >= 80:
            notes.append("👍 Good transfer efficiency (80-100%) - minor adjustments recommended")
        else:
            notes.append("⚠️ Low transfer efficiency (<80%) - consider lighter bat to improve speed")
        
        if bat_weight_oz > 32 and efficiency >= 100:
            notes.append("💪 Strong enough for heavy bat - could try 33-34 oz for more power")
        elif bat_weight_oz < 30 and efficiency < 80:
            notes.append("🏃 Already using lighter bat - focus on mechanics to improve efficiency")
        
        # MOI optimization notes
        if current_moi > 0.19:
            notes.append("📊 High MOI (>0.19) - good for power, but requires elite bat speed")
        elif current_moi < 0.15:
            notes.append("📊 Low MOI (<0.15) - fast bat speed, but less power transfer")
        else:
            notes.append("📊 Optimal MOI range (0.15-0.19) - balanced power and speed")
        
        # Current bat summary
        current_bat_summary = {
            "weight_oz": bat_weight_oz,
            "length_inches": bat_length_inches,
            "model": bat_model,
            "moi_kgm2": current_moi,
            "bat_type": bat_type,
            "balance_point_inches": balance_point_inches,
            "bat_speed_mph": bat_speed_mph,
            "predicted_exit_velo_mph": current_exit_velo
        }
        
        # Exit velocity predictions for all recommended weights
        exit_velo_predictions = [
            {
                "bat_weight_oz": rec["bat_weight_oz"],
                "exit_velo_mph": rec["predicted_exit_velo_mph"],
                "exit_velo_gain_mph": round(
                    rec["predicted_exit_velo_mph"] - current_exit_velo, 1
                )
            }
            for rec in recommendations
        ]
        
        return BatOptimizationResult(
            current_bat=current_bat_summary,
            bat_kinetic_energy_joules=bat_ke,
            body_kinetic_energy_joules=body_kinetic_energy,
            transfer_efficiency_percent=efficiency,
            optimal_weight_range_oz=optimal_range,
            recommended_weights=recommendations,
            exit_velo_predictions=exit_velo_predictions,
            optimization_notes=notes
        )


def format_bat_optimization_summary(result: BatOptimizationResult) -> str:
    """
    Format bat optimization result as readable summary.
    
    Args:
        result: BatOptimizationResult
    
    Returns:
        Formatted string summary
    """
    summary = []
    summary.append("=" * 60)
    summary.append("BAT OPTIMIZATION ANALYSIS")
    summary.append("=" * 60)
    summary.append("")
    
    # Current bat
    bat = result.current_bat
    summary.append("CURRENT BAT:")
    summary.append(f"  Weight: {bat['weight_oz']} oz")
    summary.append(f"  Length: {bat['length_inches']} inches")
    if bat.get('model'):
        summary.append(f"  Model: {bat['model']}")
    summary.append(f"  MOI: {bat['moi_kgm2']:.4f} kg·m²")
    summary.append(f"  Bat Speed: {bat['bat_speed_mph']} mph")
    summary.append(f"  Predicted Exit Velo: {bat['predicted_exit_velo_mph']} mph")
    summary.append("")
    
    # Energy transfer
    summary.append("ENERGY TRANSFER:")
    summary.append(f"  Body KE: {result.body_kinetic_energy_joules:.0f} joules")
    summary.append(f"  Bat KE: {result.bat_kinetic_energy_joules:.0f} joules")
    summary.append(f"  Transfer Efficiency: {result.transfer_efficiency_percent}%")
    summary.append("")
    
    # Recommendations
    summary.append("RECOMMENDED BAT WEIGHTS TO TEST:")
    summary.append(f"  Optimal Range: {result.optimal_weight_range_oz[0]}-{result.optimal_weight_range_oz[1]} oz")
    summary.append("")
    
    for rec in result.recommended_weights:
        marker = "→" if rec['is_current'] else " "
        summary.append(
            f"  {marker} {rec['bat_weight_oz']} oz: "
            f"Bat Speed {rec['predicted_bat_speed_mph']} mph, "
            f"Exit Velo {rec['predicted_exit_velo_mph']} mph "
            f"({rec['predicted_exit_velo_mph'] - bat['predicted_exit_velo_mph']:+.1f} mph)"
        )
    summary.append("")
    
    # Notes
    summary.append("OPTIMIZATION NOTES:")
    for note in result.optimization_notes:
        summary.append(f"  • {note}")
    summary.append("")
    summary.append("=" * 60)
    
    return "\n".join(summary)


# Example usage and testing
if __name__ == "__main__":
    # Example: Eric Williams analysis
    bat_module = BatModule()
    
    print("EXAMPLE: Eric Williams Bat Optimization")
    print()
    
    # Eric's data
    eric_bat_weight = 30.0  # oz
    eric_bat_length = 33.0  # inches
    eric_bat_speed = 82.0   # mph
    eric_body_ke = 514.0    # joules (from body rotation)
    eric_height = 70.0      # inches
    eric_weight = 185.0     # lbs
    
    # Analyze
    result = bat_module.analyze_bat_optimization(
        bat_weight_oz=eric_bat_weight,
        bat_length_inches=eric_bat_length,
        bat_speed_mph=eric_bat_speed,
        body_kinetic_energy=eric_body_ke,
        player_height_inches=eric_height,
        player_weight_lbs=eric_weight,
        bat_model="Louisville Slugger Prime",
        bat_type="balanced"
    )
    
    # Print summary
    print(format_bat_optimization_summary(result))
