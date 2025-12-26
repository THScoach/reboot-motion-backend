#!/usr/bin/env python3
"""
Test Exit Velocity Predictor with Real Player Data

Validates that exit velocity predictions are realistic and size-appropriate.
Eric Williams (5'8", 190 lbs) should max at ~112 mph like Jose Altuve, NOT 127 mph.
"""

import sys
from physics_engine.exit_velocity_predictor import ExitVelocityPredictor


def test_eric_williams():
    """
    Test Eric Williams (5'8", 190 lbs)
    Should cap at ~112 mph max (similar to Altuve)
    NOT 127 mph (unrealistic)
    """
    print("=" * 80)
    print("TEST 1: ERIC WILLIAMS (5'8\", 190 lbs)")
    print("=" * 80)
    
    predictor = ExitVelocityPredictor()
    
    result = predictor.predict_current_vs_potential(
        bat_speed_actual=74.0,
        bat_speed_potential=76.5,
        height_inches=68,
        weight_lbs=190,
        timing_gap_current=1.5,
        timing_gap_potential=0.2,
        weapon_score_current=40,
        weapon_score_potential=60
    )
    
    print(f"\n📊 CURRENT STATE:")
    print(f"   Bat Speed: {result['current']['bat_speed_mph']} mph")
    print(f"   Contact Quality: {result['current']['contact_quality']}")
    print(f"   Exit Velo (Avg): {result['current']['exit_velocity_avg_mph']} mph")
    print(f"   Exit Velo (90th): {result['current']['exit_velocity_90th_mph']} mph")
    print(f"   Exit Velo (Max): {result['current']['exit_velocity_max_mph']} mph")
    print(f"   Reference Players: {result['current']['reference_players']}")
    
    print(f"\n🎯 POTENTIAL STATE:")
    print(f"   Bat Speed: {result['potential']['bat_speed_mph']} mph")
    print(f"   Contact Quality: {result['potential']['contact_quality']}")
    print(f"   Exit Velo (Avg): {result['potential']['exit_velocity_avg_mph']} mph")
    print(f"   Exit Velo (90th): {result['potential']['exit_velocity_90th_mph']} mph")
    print(f"   Exit Velo (Max): {result['potential']['exit_velocity_max_mph']} mph")
    
    print(f"\n📈 GAPS:")
    print(f"   Bat Speed Gain: {result['gaps']['bat_speed_gain_mph']:+.1f} mph")
    print(f"   Exit Velo Avg Gain: {result['gaps']['exit_velo_avg_gain_mph']:+.1f} mph")
    print(f"   Exit Velo 90th Gain: {result['gaps']['exit_velo_90th_gain_mph']:+.1f} mph")
    
    print(f"\n👤 PLAYER INFO:")
    print(f"   Size: {result['player_info']['size_description']}")
    
    # Validate
    errors = []
    
    if result['current']['exit_velocity_max_mph'] > 114:
        errors.append(f"❌ Current max too high: {result['current']['exit_velocity_max_mph']} mph (should be ≤114)")
    else:
        print(f"\n✅ Current max realistic: {result['current']['exit_velocity_max_mph']} mph ≤ 114 mph")
    
    if result['potential']['exit_velocity_max_mph'] > 114:
        errors.append(f"❌ Potential max too high: {result['potential']['exit_velocity_max_mph']} mph (should be ≤114)")
    else:
        print(f"✅ Potential max realistic: {result['potential']['exit_velocity_max_mph']} mph ≤ 114 mph")
    
    if result['potential']['exit_velocity_90th_mph'] > 114:
        errors.append(f"❌ 90th percentile too high: {result['potential']['exit_velocity_90th_mph']} mph")
    else:
        print(f"✅ 90th percentile realistic: {result['potential']['exit_velocity_90th_mph']} mph")
    
    # Check for reference to small players
    ref_str = str(result['current']['reference_players'])
    if 'Altuve' in ref_str or 'Pedroia' in ref_str:
        print(f"✅ References small players: {result['current']['reference_players']}")
    else:
        errors.append(f"❌ Should reference Altuve or Pedroia, got: {result['current']['reference_players']}")
    
    # Contact quality checks
    if result['current']['contact_quality'] == 'poor':
        print(f"✅ Current contact quality correct: {result['current']['contact_quality']}")
    else:
        errors.append(f"❌ Current contact should be 'poor', got: {result['current']['contact_quality']}")
    
    if result['potential']['contact_quality'] in ['good', 'average']:
        print(f"✅ Potential contact quality improved: {result['potential']['contact_quality']}")
    else:
        errors.append(f"❌ Potential contact should improve, got: {result['potential']['contact_quality']}")
    
    if errors:
        print(f"\n❌ ERIC WILLIAMS TEST FAILED:")
        for error in errors:
            print(f"   {error}")
        return False
    else:
        print(f"\n✅ ERIC WILLIAMS TEST PASSED")
        return True


def test_interpolation_skinny_tall():
    """
    Test interpolation for 6'0", 160 lbs (NOT in MLB database)
    Should interpolate between nearby players
    """
    print("\n" + "=" * 80)
    print("TEST 2: INTERPOLATION - 6'0\", 160 lbs (NOT IN DATABASE)")
    print("=" * 80)
    
    predictor = ExitVelocityPredictor()
    
    result = predictor.predict_from_bat_speed(
        bat_speed=72.0,
        height_inches=72,
        weight_lbs=160,
        contact_quality='average'
    )
    
    print(f"\n📊 PREDICTION:")
    print(f"   Player Size: {result['player_size']}")
    print(f"   Bat Speed: {result['bat_speed_mph']} mph")
    print(f"   Contact Quality: {result['contact_quality']}")
    print(f"   Exit Velo (Avg): {result['exit_velocity_avg_mph']} mph")
    print(f"   Exit Velo (90th): {result['exit_velocity_90th_mph']} mph")
    print(f"   Exit Velo (Max): {result['exit_velocity_max_mph']} mph")
    print(f"   Size-Adjusted Max: {result['size_adjusted_max']} mph")
    print(f"   Reference Players: {result['reference_players']}")
    
    # Validate interpolation
    errors = []
    
    if 110 <= result['exit_velocity_max_mph'] <= 118:
        print(f"\n✅ Interpolated max reasonable: {result['exit_velocity_max_mph']} mph (110-118 range)")
    else:
        errors.append(f"❌ Interpolated max out of range: {result['exit_velocity_max_mph']} mph (expected 110-118)")
    
    if len(result['reference_players']) >= 2:
        print(f"✅ Shows reference players: {len(result['reference_players'])} players")
    else:
        errors.append(f"❌ Should show ≥2 reference players, got: {len(result['reference_players'])}")
    
    # Check that it's interpolated (not an exact match)
    if result['exit_velocity_max_mph'] not in [112.3, 111.8, 113.2, 114.5, 116.8, 117.5]:
        print(f"✅ Value is interpolated (not exact match): {result['exit_velocity_max_mph']} mph")
    else:
        print(f"⚠️  Value matches exact benchmark (may be coincidental)")
    
    if errors:
        print(f"\n❌ INTERPOLATION TEST FAILED:")
        for error in errors:
            print(f"   {error}")
        return False
    else:
        print(f"\n✅ INTERPOLATION TEST PASSED")
        return True


def test_contact_quality_determination():
    """
    Test contact quality logic
    Poor timing OR poor weapon = poor overall (takes worst)
    """
    print("\n" + "=" * 80)
    print("TEST 3: CONTACT QUALITY DETERMINATION")
    print("=" * 80)
    
    predictor = ExitVelocityPredictor()
    
    test_cases = [
        # (timing_gap, weapon_score, expected_quality, description)
        (1.5, 40, 'poor', 'Poor timing (1.5s) + Poor weapon (40)'),
        (0.2, 65, 'good', 'Good timing (0.2s) + Good weapon (65)'),
        (0.2, 35, 'poor', 'Good timing (0.2s) BUT Poor weapon (35) → Takes worse'),
        (1.5, 80, 'poor', 'Poor timing (1.5s) BUT Elite weapon (80) → Takes worse'),
        (0.5, 50, 'average', 'Average timing (0.5s) + Average weapon (50)'),
        (0.25, 78, 'good', 'Good timing (0.25s) + Elite weapon (78) → Takes worse'),
        (1.0, 42, 'below_avg', 'Below-avg timing (1.0s) + Average weapon (42)'),
    ]
    
    errors = []
    passed = 0
    
    print()
    for timing, weapon, expected, description in test_cases:
        result = predictor._determine_contact_quality(timing, weapon)
        
        if result == expected:
            print(f"✅ {description}")
            print(f"   → Got: {result} (correct)")
            passed += 1
        else:
            print(f"❌ {description}")
            print(f"   → Expected: {expected}, Got: {result}")
            errors.append(f"Failed: {description}")
    
    print(f"\n📊 RESULTS: {passed}/{len(test_cases)} test cases passed")
    
    if errors:
        print(f"\n❌ CONTACT QUALITY TEST FAILED:")
        for error in errors:
            print(f"   {error}")
        return False
    else:
        print(f"\n✅ CONTACT QUALITY TEST PASSED")
        return True


def test_benchmark_lookup():
    """
    Test finding nearest benchmarks
    """
    print("\n" + "=" * 80)
    print("TEST 4: BENCHMARK LOOKUP")
    print("=" * 80)
    
    predictor = ExitVelocityPredictor()
    
    # Test for Eric Williams (68", 190 lbs)
    print(f"\n🔍 Finding nearest benchmarks for 5'8\", 190 lbs:")
    neighbors = predictor.find_nearest_benchmarks(68, 190, num_neighbors=4)
    
    print(f"\n📋 Top 4 nearest MLB players:")
    for i, (h, w, max_ev, avg_ev, name, distance) in enumerate(neighbors, 1):
        feet = h // 12
        inches = h % 12
        print(f"   {i}. {name} ({feet}'{inches}\", {w} lbs) - Max: {max_ev} mph, Distance: {distance:.1f}")
    
    # Validate
    errors = []
    
    # First neighbor should be close
    if neighbors[0][5] < 15:  # distance < 15
        print(f"\n✅ Closest player is very similar (distance: {neighbors[0][5]:.1f})")
    else:
        errors.append(f"❌ Closest player too far (distance: {neighbors[0][5]:.1f})")
    
    # Should return 4 neighbors
    if len(neighbors) == 4:
        print(f"✅ Returned 4 neighbors as requested")
    else:
        errors.append(f"❌ Expected 4 neighbors, got {len(neighbors)}")
    
    if errors:
        print(f"\n❌ BENCHMARK LOOKUP TEST FAILED:")
        for error in errors:
            print(f"   {error}")
        return False
    else:
        print(f"\n✅ BENCHMARK LOOKUP TEST PASSED")
        return True


def run_all_tests():
    """
    Run all tests and report results
    """
    print("\n" + "=" * 80)
    print("🧪 EXIT VELOCITY PREDICTOR TEST SUITE")
    print("=" * 80)
    print()
    
    tests = [
        ("Eric Williams (5'8\", 190 lbs)", test_eric_williams),
        ("Interpolation (6'0\", 160 lbs)", test_interpolation_skinny_tall),
        ("Contact Quality Logic", test_contact_quality_determination),
        ("Benchmark Lookup", test_benchmark_lookup),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ {name} FAILED with exception: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")
    
    print(f"\n{'=' * 80}")
    print(f"TOTAL: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED - PRIORITY 8 COMPLETE!")
        print("\n✅ Exit velocity predictions are REALISTIC and SIZE-APPROPRIATE")
        print("✅ Eric Williams (5'8\") maxes at ~112 mph, NOT 127 mph")
        print("✅ Interpolation works for sizes not in MLB database")
        print("✅ Contact quality correctly determined from timing + weapon score")
    else:
        print(f"⚠️  {total - passed} test(s) failed")
    
    print("=" * 80)
    
    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
