"""
Simple V2.0.1 Test: What does the ACTUAL current code predict?
"""

import sys
sys.path.append('/home/user/webapp')

from physics_engine.kinetic_capacity_calculator import calculate_energy_capacity

# Test the 6 key players
test_players = [
    {
        'name': 'Jose Altuve',
        'height': 66, 'weight': 166, 'wingspan': 68, 'age': 34, 'bat_weight': 32,
        'statcast_actual': 69.0
    },
    {
        'name': 'Mookie Betts',
        'height': 69, 'weight': 180, 'wingspan': 71, 'age': 31, 'bat_weight': 32,
        'statcast_actual': 72.0
    },
    {
        'name': 'Ronald Acuña Jr',
        'height': 72, 'weight': 205, 'wingspan': 74, 'age': 26, 'bat_weight': 33,
        'statcast_actual': 73.0
    },
    {
        'name': 'Aaron Judge',
        'height': 79, 'weight': 282, 'wingspan': 83, 'age': 33, 'bat_weight': 34,
        'statcast_actual': 77.0
    },
    {
        'name': 'Giancarlo Stanton',
        'height': 78, 'weight': 245, 'wingspan': 81, 'age': 34, 'bat_weight': 34,
        'statcast_actual': 78.0
    },
    {
        'name': 'Yordan Alvarez',
        'height': 77, 'weight': 225, 'wingspan': 79, 'age': 27, 'bat_weight': 33,
        'statcast_actual': 79.0
    }
]

print("="*80)
print("CURRENT V2.0.1 PREDICTIONS (with short player boost)")
print("="*80)

within_4mph_count = 0

for player in test_players:
    result = calculate_energy_capacity(
        height_inches=player['height'],
        wingspan_inches=player['wingspan'],
        weight_lbs=player['weight'],
        age=player['age'],
        bat_weight_oz=player['bat_weight']
    )
    
    predicted = result['bat_speed_capacity_midpoint_mph']
    actual = player['statcast_actual']
    error = predicted - actual
    within_target = abs(error) <= 4.0
    
    if within_target:
        within_4mph_count += 1
    
    print(f"\n{player['name']} ({player['height']//12}'{player['height']%12}\", {player['weight']} lbs):")
    print(f"  Predicted: {predicted:.1f} mph")
    print(f"  Actual: {actual:.1f} mph")
    print(f"  Error: {error:+.1f} mph {'✅' if within_target else '❌'}")

print(f"\n{'='*80}")
print(f"ACCURACY: {within_4mph_count}/6 players within ±4 mph ({within_4mph_count/6*100:.1f}%)")
print(f"TARGET: ≥83% (5/6 players)")
print(f"STATUS: {'✅ PASS' if within_4mph_count >= 5 else '❌ FAIL'}")
print("="*80)
