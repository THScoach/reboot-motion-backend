#!/usr/bin/env python3
"""
Test bat speed potential calculation against ground truth
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "physics_engine"))

from anthropometry import AnthropometricModel

print("=" * 70)
print("BAT SPEED POTENTIAL VALIDATION")
print("=" * 70)

# Test Case 1: Eric Williams
print("\n" + "=" * 70)
print("TEST 1: ERIC WILLIAMS")
print("=" * 70)
print("Profile: 5'8\", 190 lbs, 5'9\" wingspan, age 33, 30oz bat")
print("EXPECTED: ~76 mph bat speed potential")

eric = AnthropometricModel(
    height_inches=68,  # 5'8"
    weight_lbs=190,
    age=33,
    wingspan_inches=69  # 5'9"
)

eric_potential = eric.estimate_bat_speed_potential(
    bat_length_inches=33,
    bat_weight_oz=30
)

print(f"\nRESULTS:")
print(f"  Bat Speed Potential: {eric_potential['bat_speed_mph']} mph")
print(f"  Exit Velo (tee): {eric_potential['exit_velocity_tee_mph']} mph")
print(f"  Exit Velo (85 mph pitch): {eric_potential['exit_velocity_pitched_mph']} mph")
print(f"\nFactors:")
for factor, value in eric_potential['factors'].items():
    print(f"  {factor}: {value}")

error_eric = abs(eric_potential['bat_speed_mph'] - 76.0)
print(f"\nError: {error_eric:.1f} mph")
print(f"Status: {'✅ PASS' if error_eric < 5.0 else '❌ FAIL'} (within 5 mph)")

# Test Case 2: Connor Gray
print("\n" + "=" * 70)
print("TEST 2: CONNOR GRAY")
print("=" * 70)
print("Profile: 6'0\", 160 lbs, 6'4\" wingspan, age 16, 30oz bat")
print("EXPECTED: ~57.5 mph bat speed (from Reboot Motion data)")

connor = AnthropometricModel(
    height_inches=72,  # 6'0"
    weight_lbs=160,
    age=16,
    wingspan_inches=76  # 6'4"
)

connor_potential = connor.estimate_bat_speed_potential(
    bat_length_inches=33,
    bat_weight_oz=30
)

print(f"\nRESULTS:")
print(f"  Bat Speed Potential: {connor_potential['bat_speed_mph']} mph")
print(f"  Exit Velo (tee): {connor_potential['exit_velocity_tee_mph']} mph")
print(f"  Exit Velo (85 mph pitch): {connor_potential['exit_velocity_pitched_mph']} mph")
print(f"\nFactors:")
for factor, value in connor_potential['factors'].items():
    print(f"  {factor}: {value}")

error_connor = abs(connor_potential['bat_speed_mph'] - 57.5)
print(f"\nError: {error_connor:.1f} mph")
print(f"Status: {'✅ PASS' if error_connor < 5.0 else '❌ FAIL'} (within 5 mph)")

# Test Case 3: Shohei Ohtani (MLB elite)
print("\n" + "=" * 70)
print("TEST 3: SHOHEI OHTANI (MLB)")
print("=" * 70)
print("Profile: 6'4\", 210 lbs, ~6'7\" wingspan, age 29, 34oz bat")
print("EXPECTED: ~75-80 mph bat speed (MLB elite)")

shohei = AnthropometricModel(
    height_inches=76,  # 6'4"
    weight_lbs=210,
    age=29,
    wingspan_inches=79  # ~6'7"
)

shohei_potential = shohei.estimate_bat_speed_potential(
    bat_length_inches=34,
    bat_weight_oz=34
)

print(f"\nRESULTS:")
print(f"  Bat Speed Potential: {shohei_potential['bat_speed_mph']} mph")
print(f"  Exit Velo (tee): {shohei_potential['exit_velocity_tee_mph']} mph")
print(f"  Exit Velo (95 mph pitch): {shohei_potential['exit_velocity_pitched_mph']} mph")
print(f"\nFactors:")
for factor, value in shohei_potential['factors'].items():
    print(f"  {factor}: {value}")

in_range = 75 <= shohei_potential['bat_speed_mph'] <= 80
print(f"\nStatus: {'✅ PASS' if in_range else '❌ FAIL'} (75-80 mph range)")

# Summary
print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

tests_passed = sum([
    error_eric < 5.0,
    error_connor < 5.0,
    in_range
])

print(f"\nTests Passed: {tests_passed}/3")
print(f"Overall Status: {'✅ ALL TESTS PASSED' if tests_passed == 3 else '⚠️ SOME TESTS FAILED'}")
