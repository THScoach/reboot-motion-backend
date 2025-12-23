"""
Efficiency Analyzer
===================

Calculates current efficiency from Ground/Engine/Weapon scores
and predicts actual bat speed (capacity × efficiency).

Philosophy: "You have X capacity. You're using Y% of it."
"""


def calculate_efficiency(ground_score, engine_score, weapon_score):
    """
    Convert raw scores (0-100) to efficiency multipliers (0.5-1.0).
    
    Mapping:
    - Score 100 → 1.0 efficiency (100% of capacity)
    - Score 50  → 0.75 efficiency (75% of capacity)
    - Score 0   → 0.5 efficiency (50% of capacity, floor)
    
    Formula: efficiency = 0.5 + (score / 100) * 0.5
    
    Args:
        ground_score: 0-100
        engine_score: 0-100
        weapon_score: 0-100
    
    Returns:
        dict with efficiency metrics:
        - ground_efficiency: 0.0-1.0
        - engine_efficiency: 0.0-1.0
        - weapon_efficiency: 0.0-1.0
        - overall_efficiency: Weighted average (25% G, 50% E, 25% W)
        - efficiency_percent: Overall as % (e.g., 76.1)
    """
    ground_efficiency = 0.5 + (ground_score / 100) * 0.5
    engine_efficiency = 0.5 + (engine_score / 100) * 0.5
    weapon_efficiency = 0.5 + (weapon_score / 100) * 0.5
    
    # Weighted average: Ground 25%, Engine 50%, Weapon 25%
    overall_efficiency = (
        ground_efficiency * 0.25 +
        engine_efficiency * 0.50 +
        weapon_efficiency * 0.25
    )
    
    return {
        'ground_efficiency': ground_efficiency,
        'engine_efficiency': engine_efficiency,
        'weapon_efficiency': weapon_efficiency,
        'overall_efficiency': overall_efficiency,
        'efficiency_percent': overall_efficiency * 100
    }


def predict_current_performance(capacity_data, efficiency_data, bat_weight_oz=30):
    """
    Apply efficiency multiplier to capacity to predict current bat speed.
    
    Args:
        capacity_data: Output from calculate_energy_capacity()
        efficiency_data: Output from calculate_efficiency()
        bat_weight_oz: Bat weight in ounces (default 30)
    
    Returns:
        dict with current performance:
        - predicted_bat_speed_mph: Capacity midpoint × efficiency
        - predicted_exit_velo_mph: vs 80mph pitch
        - percent_of_capacity_used: Efficiency %
        - energy_actual_joules: Actual energy delivered
        - energy_leaked_joules: Energy lost to inefficiency
    """
    capacity_midpoint = capacity_data['bat_speed_capacity_midpoint_mph']
    overall_efficiency = efficiency_data['overall_efficiency']
    
    predicted_bat_speed = capacity_midpoint * overall_efficiency
    
    # Calculate exit velocity (OFF TEE for capacity comparison)
    from physics_engine.kinetic_capacity_calculator import _calculate_exit_velo
    predicted_exit_velo = _calculate_exit_velo(
        predicted_bat_speed, 
        pitch_speed_mph=0,  # Off tee for realistic capacity numbers
        bat_weight_oz=bat_weight_oz
    )
    
    # Energy calculations
    energy_capacity = capacity_data['energy_capacity_joules']
    energy_actual = energy_capacity * overall_efficiency
    energy_leaked = energy_capacity - energy_actual
    
    return {
        'predicted_bat_speed_mph': predicted_bat_speed,
        'predicted_exit_velo_mph': predicted_exit_velo,
        'percent_of_capacity_used': efficiency_data['efficiency_percent'],
        'energy_actual_joules': energy_actual,
        'energy_leaked_joules': energy_leaked
    }


# Test function
if __name__ == "__main__":
    from physics_engine.kinetic_capacity_calculator import calculate_energy_capacity
    
    print("Testing Eric Williams efficiency (Ground 38, Engine 58, Weapon 55)...")
    
    # Calculate capacity first
    capacity = calculate_energy_capacity(68, 69, 190, 33, 30)
    
    # Calculate efficiency
    efficiency = calculate_efficiency(
        ground_score=38,
        engine_score=58,
        weapon_score=55
    )
    
    print(f"\n✅ EFFICIENCY RESULTS:")
    print(f"   Ground Efficiency: {efficiency['ground_efficiency']:.3f} ({38}/100)")
    print(f"   Engine Efficiency: {efficiency['engine_efficiency']:.3f} ({58}/100)")
    print(f"   Weapon Efficiency: {efficiency['weapon_efficiency']:.3f} ({55}/100)")
    print(f"   Overall Efficiency: {efficiency['efficiency_percent']:.1f}%")
    
    # Predict current performance
    current = predict_current_performance(capacity, efficiency)
    
    print(f"\n✅ CURRENT PERFORMANCE:")
    print(f"   Predicted Bat Speed: {current['predicted_bat_speed_mph']:.1f} mph")
    print(f"   Predicted Exit Velo: {current['predicted_exit_velo_mph']:.1f} mph")
    print(f"   % Capacity Used: {current['percent_of_capacity_used']:.1f}%")
    print(f"   Energy Actual: {current['energy_actual_joules']:.1f} J")
    print(f"   Energy Leaked: {current['energy_leaked_joules']:.1f} J")
    
    # Expected: 76.1% efficiency, 57-59 mph predicted
    assert 75 <= efficiency['efficiency_percent'] <= 77, \
        f"❌ Expected ~76% efficiency, got {efficiency['efficiency_percent']}"
    assert 57 <= current['predicted_bat_speed_mph'] <= 59, \
        f"❌ Expected ~58 mph, got {current['predicted_bat_speed_mph']}"
    
    print(f"\n✅ Eric Williams efficiency validated!")
