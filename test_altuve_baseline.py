"""Check what baseline the lookup table returns for Altuve"""
import sys
sys.path.append('/home/user/webapp')

from physics_engine.kinetic_capacity_calculator import _get_baseline_bat_speed

# Altuve specs
height = 66  # 5'6"
weight = 166
age = 34

baseline = _get_baseline_bat_speed(height, weight, age)
print(f"Altuve (5'6\", {weight} lbs, age {age}):")
print(f"Baseline from lookup: {baseline:.1f} mph")
print(f"\nWith +12% boost: {baseline * 1.12:.1f} mph")
print(f"\nWith +2\" wingspan (+3% boost): {baseline * 1.03:.1f} mph")
print(f"With 32oz bat (-2oz from 30oz = +1.4 mph): {baseline + 1.4:.1f} mph")
print(f"\nFinal (baseline × 1.03 + 1.4): {(baseline * 1.03) + 1.4:.1f} mph")
