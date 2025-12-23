"""
Gap Analyzer
============

Compares capacity vs predicted vs actual (Blast/DK sensor) and localizes energy leaks.

Philosophy: "You have X capacity, using Y%, here's where the Z% is leaking."
"""


def analyze_gaps(capacity_data, current_performance, blast_actual_mph, 
                 ground_score, engine_score, weapon_score):
    """
    Compare capacity → predicted → actual and localize leaks.
    
    Args:
        capacity_data: From calculate_energy_capacity()
        current_performance: From predict_current_performance()
        blast_actual_mph: Actual bat speed from Blast/DK sensor (or None)
        ground_score, engine_score, weapon_score: Raw scores
    
    Returns:
        dict with gap analysis:
        - capacity_range: {min, max, midpoint} mph
        - predicted_mph: Predicted bat speed
        - actual_mph: Actual sensor bat speed (or None)
        - gap_to_capacity_min_mph: Gap to min capacity
        - gap_to_capacity_max_mph: Gap to max capacity
        - gap_predicted_vs_actual_mph: Predicted - actual (or None)
        - percent_capacity_used_predicted: % based on predicted
        - percent_capacity_used_actual: % based on actual (or None)
        - alignment_status: "good", "warning", "poor", "no_sensor_data"
        - leak_breakdown: {ground, engine, weapon} with scores, leak %, gains, priority
        - prescription: Human-readable action plan
    """
    capacity_min = capacity_data['bat_speed_capacity_min_mph']
    capacity_max = capacity_data['bat_speed_capacity_max_mph']
    capacity_midpoint = capacity_data['bat_speed_capacity_midpoint_mph']
    predicted_mph = current_performance['predicted_bat_speed_mph']
    
    # Gaps
    gap_to_capacity_min = capacity_min - (blast_actual_mph or predicted_mph)
    gap_to_capacity_max = capacity_max - (blast_actual_mph or predicted_mph)
    gap_predicted_vs_actual = (predicted_mph - blast_actual_mph) if blast_actual_mph else None
    
    # % of capacity used
    percent_capacity_predicted = (predicted_mph / capacity_midpoint) * 100
    percent_capacity_actual = ((blast_actual_mph / capacity_midpoint) * 100) if blast_actual_mph else None
    
    # Alignment check (predicted vs actual should be within ±8 mph)
    if gap_predicted_vs_actual is not None:
        if abs(gap_predicted_vs_actual) <= 5:
            alignment = "good"
        elif abs(gap_predicted_vs_actual) <= 8:
            alignment = "warning"
        else:
            alignment = "poor"
    else:
        alignment = "no_sensor_data"
    
    # Leak breakdown
    leak_breakdown = _calculate_leak_breakdown(
        ground_score, engine_score, weapon_score,
        gap_to_capacity_max  # Use max gap for potential gain calculations
    )
    
    # Generate prescription
    prescription = _generate_prescription(leak_breakdown)
    
    return {
        'capacity_range': {
            'min_mph': capacity_min,
            'max_mph': capacity_max,
            'midpoint_mph': capacity_midpoint
        },
        'predicted_mph': predicted_mph,
        'actual_mph': blast_actual_mph,
        
        'gap_to_capacity_min_mph': gap_to_capacity_min,
        'gap_to_capacity_max_mph': gap_to_capacity_max,
        'gap_predicted_vs_actual_mph': gap_predicted_vs_actual,
        
        'percent_capacity_used_predicted': percent_capacity_predicted,
        'percent_capacity_used_actual': percent_capacity_actual,
        
        'alignment_status': alignment,
        
        'leak_breakdown': leak_breakdown,
        'prescription': prescription
    }


def _calculate_leak_breakdown(ground_score, engine_score, weapon_score, total_gap_mph):
    """
    Quantify how much each component is leaking.
    
    Logic:
    - Each score (0-100) represents efficiency in that component
    - Lower score = more leakage
    - Distribute total gap proportionally to inefficiency
    """
    # Inefficiency = (100 - score)
    ground_inefficiency = 100 - ground_score
    engine_inefficiency = 100 - engine_score
    weapon_inefficiency = 100 - weapon_score
    
    # Weighted inefficiency (Ground 25%, Engine 50%, Weapon 25%)
    weighted_ground = ground_inefficiency * 0.25
    weighted_engine = engine_inefficiency * 0.50
    weighted_weapon = weapon_inefficiency * 0.25
    total_weighted = weighted_ground + weighted_engine + weighted_weapon
    
    # Calculate leak % and potential gain
    ground_leak_percent = (weighted_ground / total_weighted) * 100 if total_weighted > 0 else 0
    engine_leak_percent = (weighted_engine / total_weighted) * 100 if total_weighted > 0 else 0
    weapon_leak_percent = (weighted_weapon / total_weighted) * 100 if total_weighted > 0 else 0
    
    ground_gain = (ground_leak_percent / 100) * total_gap_mph
    engine_gain = (engine_leak_percent / 100) * total_gap_mph
    weapon_gain = (weapon_leak_percent / 100) * total_gap_mph
    
    # Priority (HIGH if leak > 30%, MEDIUM if 20-30%, LOW if < 20%)
    def get_priority(leak_percent):
        if leak_percent > 30:
            return "HIGH"
        elif leak_percent > 20:
            return "MEDIUM"
        else:
            return "LOW"
    
    return {
        'ground': {
            'score': ground_score,
            'leak_percent': ground_leak_percent,
            'potential_gain_mph': ground_gain,
            'priority': get_priority(ground_leak_percent)
        },
        'engine': {
            'score': engine_score,
            'leak_percent': engine_leak_percent,
            'potential_gain_mph': engine_gain,
            'priority': get_priority(engine_leak_percent)
        },
        'weapon': {
            'score': weapon_score,
            'leak_percent': weapon_leak_percent,
            'potential_gain_mph': weapon_gain,
            'priority': get_priority(weapon_leak_percent)
        }
    }


def _generate_prescription(leak_breakdown):
    """
    Generate human-readable prescription based on leak priorities.
    """
    components = ['ground', 'engine', 'weapon']
    sorted_components = sorted(
        components,
        key=lambda c: leak_breakdown[c]['potential_gain_mph'],
        reverse=True
    )
    
    top_component = sorted_components[0]
    top_gain = leak_breakdown[top_component]['potential_gain_mph']
    top_score = leak_breakdown[top_component]['score']
    
    prescription = f"Focus on {top_component.upper()} (score: {top_score}) "
    prescription += f"for +{top_gain:.1f} mph gain. "
    
    if len(sorted_components) > 1:
        second_component = sorted_components[1]
        second_gain = leak_breakdown[second_component]['potential_gain_mph']
        if second_gain > 3:  # Only mention if meaningful
            prescription += f"Then address {second_component.upper()} for +{second_gain:.1f} mph."
    
    return prescription


# Test function
if __name__ == "__main__":
    from physics_engine.kinetic_capacity_calculator import calculate_energy_capacity
    from physics_engine.efficiency_analyzer import calculate_efficiency, predict_current_performance
    
    print("Testing Eric Williams gap analysis (Blast actual: 67 mph)...")
    
    # Calculate capacity
    capacity = calculate_energy_capacity(68, 69, 190, 33, 30)
    
    # Calculate efficiency and current performance
    efficiency = calculate_efficiency(38, 58, 55)
    current = predict_current_performance(capacity, efficiency)
    
    # Analyze gaps
    gaps = analyze_gaps(
        capacity_data=capacity,
        current_performance=current,
        blast_actual_mph=67,
        ground_score=38,
        engine_score=58,
        weapon_score=55
    )
    
    print(f"\n✅ GAP ANALYSIS RESULTS:")
    print(f"   Capacity Range: {gaps['capacity_range']['min_mph']:.1f}-{gaps['capacity_range']['max_mph']:.1f} mph")
    print(f"   Predicted: {gaps['predicted_mph']:.1f} mph")
    print(f"   Actual (Blast): {gaps['actual_mph']} mph")
    print(f"   Gap to Capacity Max: {gaps['gap_to_capacity_max_mph']:.1f} mph")
    print(f"   Predicted vs Actual: {gaps['gap_predicted_vs_actual_mph']:.1f} mph")
    print(f"   % Capacity Used (Actual): {gaps['percent_capacity_used_actual']:.1f}%")
    print(f"   Alignment Status: {gaps['alignment_status']}")
    
    print(f"\n✅ LEAK BREAKDOWN:")
    for component in ['ground', 'engine', 'weapon']:
        leak = gaps['leak_breakdown'][component]
        print(f"   {component.upper()}: {leak['score']}/100 | Leak: {leak['leak_percent']:.0f}% | Gain: +{leak['potential_gain_mph']:.1f} mph | Priority: {leak['priority']}")
    
    print(f"\n✅ PRESCRIPTION:")
    print(f"   {gaps['prescription']}")
    
    # Validations
    assert 5 <= gaps['gap_to_capacity_max_mph'] <= 15, \
        f"❌ Expected gap ~5-13 mph, got {gaps['gap_to_capacity_max_mph']}"
    assert gaps['leak_breakdown']['ground']['priority'] == "HIGH", \
        "❌ Ground should be HIGH priority"
    
    print(f"\n✅ Eric Williams gap analysis validated!")
