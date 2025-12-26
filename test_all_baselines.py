"""Check baselines for all 6 test players"""
import sys
sys.path.append('/home/user/webapp')

from physics_engine.kinetic_capacity_calculator import _get_baseline_bat_speed

test_players = [
    {'name': 'Jose Altuve', 'height': 66, 'weight': 166, 'age': 34, 'actual': 69.0},
    {'name': 'Mookie Betts', 'height': 69, 'weight': 180, 'age': 31, 'actual': 72.0},
    {'name': 'Ronald Acuña Jr', 'height': 72, 'weight': 205, 'age': 26, 'actual': 73.0},
    {'name': 'Aaron Judge', 'height': 79, 'weight': 282, 'age': 33, 'actual': 77.0},
    {'name': 'Giancarlo Stanton', 'height': 78, 'weight': 245, 'age': 34, 'actual': 78.0},
    {'name': 'Yordan Alvarez', 'height': 77, 'weight': 225, 'age': 27, 'actual': 79.0}
]

print("="*80)
print("BASELINE LOOKUP TABLE VALUES")
print("="*80)

for p in test_players:
    baseline = _get_baseline_bat_speed(p['height'], p['weight'], p['age'])
    error = baseline - p['actual']
    
    print(f"\n{p['name']} ({p['height']//12}'{p['height']%12}\", {p['weight']} lbs, age {p['age']}):")
    print(f"  Baseline: {baseline:.1f} mph")
    print(f"  Statcast Actual: {p['actual']:.1f} mph")
    print(f"  Baseline Error: {error:+.1f} mph {'✅' if abs(error) <= 5 else '❌'}")
    
print("\n" + "="*80)
print("CONCLUSION: The baseline table is INFLATED for tall players (6'5\"+)")
print("="*80)
