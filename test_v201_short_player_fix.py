"""
V2.0.1 Short Player Fix - Validation Test Suite
================================================

Tests the short player baseline boost fix for Jose Altuve underestimation.

Target: Improve Altuve prediction from 58.0 mph (error -11 mph) to 65-68 mph (error ±4 mph)
Constraint: No regressions on other 5 players (must remain within ±4 mph)

Author: Reboot Motion Development Team
Date: 2024-12-24
"""

import sys
sys.path.append('/home/user/webapp')

from physics_engine.kinetic_capacity_calculator import (
    calculate_energy_capacity,
    _apply_short_player_baseline_boost
)


# ============================================================================
# UNIT TESTS
# ============================================================================

def test_short_player_boost_altuve():
    """Test that Altuve gets proper +12% boost"""
    print("\n" + "="*80)
    print("TEST 1: Short Player Boost - Altuve")
    print("="*80)
    
    baseline = 58.0  # Original Altuve prediction
    height = 66  # 5'6"
    
    result = _apply_short_player_baseline_boost(baseline, height)
    
    expected = 58.0 * 1.12  # +12% boost
    error = abs(result - expected)
    
    print(f"Input: {baseline} mph (baseline for 5'6\" player)")
    print(f"Expected: {expected:.2f} mph (+12% boost)")
    print(f"Actual: {result:.2f} mph")
    print(f"Error: {error:.4f} mph")
    
    passed = error < 0.01
    print(f"Status: {'✅ PASS' if passed else '❌ FAIL'}")
    
    assert passed, f"Expected {expected:.2f}, got {result:.2f}"
    return passed


def test_short_player_boost_threshold():
    """Test that 5'8" (68") is the cutoff"""
    print("\n" + "="*80)
    print("TEST 2: Short Player Boost - Threshold Testing")
    print("="*80)
    
    baseline = 70.0
    
    # Test 5'7" (67") - SHOULD get boost
    result_67 = _apply_short_player_baseline_boost(baseline, 67)
    print(f"5'7\" (67\"): {baseline} → {result_67:.2f} mph")
    test1 = result_67 > baseline
    print(f"  Boost applied: {'✅ YES' if test1 else '❌ NO'}")
    
    # Test 5'8" (68") - Should NOT get boost
    result_68 = _apply_short_player_baseline_boost(baseline, 68)
    print(f"5'8\" (68\"): {baseline} → {result_68:.2f} mph")
    test2 = result_68 == baseline
    print(f"  No boost: {'✅ CORRECT' if test2 else '❌ INCORRECT'}")
    
    # Test 6'0" (72") - Should NOT get boost
    result_72 = _apply_short_player_baseline_boost(baseline, 72)
    print(f"6'0\" (72\"): {baseline} → {result_72:.2f} mph")
    test3 = result_72 == baseline
    print(f"  No boost: {'✅ CORRECT' if test3 else '❌ INCORRECT'}")
    
    passed = test1 and test2 and test3
    print(f"\nStatus: {'✅ PASS' if passed else '❌ FAIL'}")
    
    assert passed, "Threshold tests failed"
    return passed


def test_no_regression_average_height():
    """Ensure average height players are unaffected"""
    print("\n" + "="*80)
    print("TEST 3: No Regression - Average Height Players")
    print("="*80)
    
    test_heights = [
        (69, "5'9\""),
        (72, "6'0\""),
        (75, "6'3\""),
        (79, "6'7\"")
    ]
    
    baseline = 75.0
    all_passed = True
    
    for height, height_str in test_heights:
        result = _apply_short_player_baseline_boost(baseline, height)
        unchanged = (result == baseline)
        
        print(f"{height_str} ({height}\"): {baseline} → {result:.2f} mph - "
              f"{'✅ UNCHANGED' if unchanged else '❌ CHANGED'}")
        
        if not unchanged:
            all_passed = False
    
    print(f"\nStatus: {'✅ PASS' if all_passed else '❌ FAIL'}")
    
    assert all_passed, "Some average height players were affected"
    return all_passed


def test_edge_cases():
    """Test edge cases and extreme values"""
    print("\n" + "="*80)
    print("TEST 4: Edge Cases")
    print("="*80)
    
    baseline = 60.0
    
    # Very short player (5'3" - 63")
    result_63 = _apply_short_player_baseline_boost(baseline, 63)
    boost_applied_63 = result_63 > baseline
    print(f"5'3\" (63\"): {baseline} → {result_63:.2f} mph - "
          f"{'✅ BOOST APPLIED' if boost_applied_63 else '❌ NO BOOST'}")
    
    # Exactly at threshold (5'8" - 68")
    result_68 = _apply_short_player_baseline_boost(baseline, 68)
    no_boost_68 = result_68 == baseline
    print(f"5'8\" (68\"): {baseline} → {result_68:.2f} mph - "
          f"{'✅ NO BOOST (correct)' if no_boost_68 else '❌ BOOST APPLIED (incorrect)'}")
    
    # Just below threshold (5'7.5" would be 67.5", but using 67 for int)
    result_67 = _apply_short_player_baseline_boost(baseline, 67)
    boost_applied_67 = result_67 > baseline
    print(f"5'7\" (67\"): {baseline} → {result_67:.2f} mph - "
          f"{'✅ BOOST APPLIED' if boost_applied_67 else '❌ NO BOOST'}")
    
    passed = boost_applied_63 and no_boost_68 and boost_applied_67
    print(f"\nStatus: {'✅ PASS' if passed else '❌ FAIL'}")
    
    assert passed, "Edge case tests failed"
    return passed


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

def test_altuve_full_pipeline():
    """Test complete pipeline with Altuve data"""
    print("\n" + "="*80)
    print("INTEGRATION TEST: Altuve Full Pipeline")
    print("="*80)
    
    # Altuve data
    height = 66  # 5'6"
    wingspan = 68  # Estimated (+2" ape index, typical)
    weight = 166
    age = 34
    bat_weight = 32
    
    statcast_actual = 69.0  # mph
    target_min = 65.0  # Within ±4 mph
    target_max = 73.0  # Within ±4 mph
    
    result = calculate_energy_capacity(
        height_inches=height,
        wingspan_inches=wingspan,
        weight_lbs=weight,
        age=age,
        bat_weight_oz=bat_weight
    )
    
    predicted = result['bat_speed_capacity_midpoint_mph']
    error = predicted - statcast_actual
    within_target = target_min <= predicted <= target_max
    
    print(f"Player: Jose Altuve")
    print(f"  Height: 5'6\" ({height}\")")
    print(f"  Weight: {weight} lbs")
    print(f"  Wingspan: {wingspan}\" (+{wingspan-height}\" ape index)")
    print(f"  Age: {age}")
    print(f"  Bat Weight: {bat_weight} oz")
    print(f"\n📊 RESULTS:")
    print(f"  Predicted: {predicted:.1f} mph")
    print(f"  Statcast Actual: {statcast_actual:.1f} mph")
    print(f"  Error: {error:+.1f} mph")
    print(f"  Target Range: {target_min:.1f}-{target_max:.1f} mph (±4 mph from actual)")
    print(f"  Within Target: {'✅ YES' if within_target else '❌ NO'}")
    
    # V2.0 comparison
    v20_predicted = 58.0
    v20_error = v20_predicted - statcast_actual
    improvement = abs(v20_error) - abs(error)
    
    print(f"\n📈 IMPROVEMENT vs V2.0:")
    print(f"  V2.0 Prediction: {v20_predicted:.1f} mph (error: {v20_error:+.1f} mph)")
    print(f"  V2.0.1 Prediction: {predicted:.1f} mph (error: {error:+.1f} mph)")
    print(f"  Improvement: {improvement:+.1f} mph {'✅' if improvement > 0 else '❌'}")
    
    passed = within_target and improvement > 0
    print(f"\nStatus: {'✅ PASS' if passed else '❌ FAIL'}")
    
    assert passed, f"Altuve prediction not within ±4 mph: {predicted:.1f} mph"
    return passed


def test_no_regressions():
    """Test that other 5 players remain accurate"""
    print("\n" + "="*80)
    print("REGRESSION TEST: Other 5 Players")
    print("="*80)
    
    test_players = [
        {
            'name': 'Mookie Betts',
            'height': 69, 'weight': 180, 'wingspan': 71, 'age': 31, 'bat_weight': 32,
            'statcast_actual': 72.0,  # Midpoint of 71-73
            'v20_prediction': 69.7
        },
        {
            'name': 'Ronald Acuña Jr',
            'height': 72, 'weight': 205, 'wingspan': 74, 'age': 26, 'bat_weight': 33,
            'statcast_actual': 73.0,  # Midpoint of 72-74
            'v20_prediction': 75.1
        },
        {
            'name': 'Aaron Judge',
            'height': 79, 'weight': 282, 'wingspan': 83, 'age': 33, 'bat_weight': 34,
            'statcast_actual': 77.0,  # Midpoint of 76-78
            'v20_prediction': 80.2
        },
        {
            'name': 'Giancarlo Stanton',
            'height': 78, 'weight': 245, 'wingspan': 81, 'age': 34, 'bat_weight': 34,
            'statcast_actual': 78.0,  # Midpoint of 77-79
            'v20_prediction': 78.9
        },
        {
            'name': 'Yordan Alvarez',
            'height': 77, 'weight': 225, 'wingspan': 79, 'age': 27, 'bat_weight': 33,
            'statcast_actual': 79.0,  # Midpoint of 78-80
            'v20_prediction': 82.0
        }
    ]
    
    all_passed = True
    regressions = []
    
    for player in test_players:
        result = calculate_energy_capacity(
            height_inches=player['height'],
            wingspan_inches=player['wingspan'],
            weight_lbs=player['weight'],
            age=player['age'],
            bat_weight_oz=player['bat_weight']
        )
        
        new_pred = result['bat_speed_capacity_midpoint_mph']
        old_pred = player['v20_prediction']
        statcast = player['statcast_actual']
        
        change = abs(new_pred - old_pred)
        error_new = new_pred - statcast
        within_4mph = abs(error_new) <= 4.0
        
        # Should be NO CHANGE (short player boost only applies to <5'8")
        no_change = change < 0.1
        
        status = "✅ PASS" if (no_change and within_4mph) else "❌ FAIL"
        if not (no_change and within_4mph):
            all_passed = False
            regressions.append(player['name'])
        
        print(f"\n{player['name']}:")
        print(f"  Height: {player['height']//12}'{player['height']%12}\"")
        print(f"  V2.0: {old_pred:.1f} mph")
        print(f"  V2.0.1: {new_pred:.1f} mph")
        print(f"  Change: {change:.1f} mph {'(no change ✅)' if no_change else '(CHANGED ❌)'}")
        print(f"  Statcast: {statcast:.1f} mph")
        print(f"  Error: {error_new:+.1f} mph {'(within ±4 ✅)' if within_4mph else '(outside ±4 ❌)'}")
        print(f"  Status: {status}")
    
    print(f"\n{'='*80}")
    print(f"REGRESSION TEST SUMMARY:")
    print(f"  Passed: {5 - len(regressions)}/5")
    print(f"  Failed: {len(regressions)}/5")
    if regressions:
        print(f"  Regressions: {', '.join(regressions)}")
    print(f"\nStatus: {'✅ PASS' if all_passed else '❌ FAIL'}")
    
    assert all_passed, f"Regressions detected: {regressions}"
    return all_passed


# ============================================================================
# MAIN TEST RUNNER
# ============================================================================

def run_all_tests():
    """Run all tests and report results"""
    print("="*80)
    print("V2.0.1 SHORT PLAYER FIX - VALIDATION TEST SUITE")
    print("="*80)
    print()
    
    tests = [
        ("Unit Test 1: Short Player Boost - Altuve", test_short_player_boost_altuve),
        ("Unit Test 2: Short Player Boost - Threshold", test_short_player_boost_threshold),
        ("Unit Test 3: No Regression - Average Height", test_no_regression_average_height),
        ("Unit Test 4: Edge Cases", test_edge_cases),
        ("Integration Test 1: Altuve Full Pipeline", test_altuve_full_pipeline),
        ("Integration Test 2: No Regressions (5 players)", test_no_regressions),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            passed = test_func()
            results.append((test_name, "✅ PASS"))
        except AssertionError as e:
            results.append((test_name, f"❌ FAIL: {str(e)}"))
        except Exception as e:
            results.append((test_name, f"❌ ERROR: {str(e)}"))
    
    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    
    for test_name, result in results:
        print(f"{test_name}: {result}")
    
    passed_count = sum(1 for _, r in results if r.startswith("✅"))
    total_count = len(results)
    
    print(f"\n{'='*80}")
    print(f"TOTAL: {passed_count}/{total_count} tests passed")
    
    if passed_count == total_count:
        print("✅ ALL TESTS PASSED - V2.0.1 READY FOR PRODUCTION")
    else:
        print("❌ SOME TESTS FAILED - NEEDS FIXES")
    
    print("="*80)
    
    return passed_count == total_count


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
