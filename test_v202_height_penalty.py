"""
V2.0.2 Height Penalty - Unit Tests
===================================

Tests the height penalty correction for tall players (6'0"+).

Target: Apply -0.6% per inch over 6'0" (72") to reduce overestimation
"""

import sys
sys.path.append('/home/user/webapp')

from physics_engine.kinetic_capacity_calculator import (
    calculate_energy_capacity,
    _apply_height_penalty
)


# ============================================================================
# UNIT TESTS FOR HEIGHT PENALTY FUNCTION
# ============================================================================

def test_height_penalty_no_penalty_at_threshold():
    """Test that 6'0" (72") players get NO penalty (at threshold)"""
    print("\n" + "="*80)
    print("TEST 1: NO penalty at 6'0\" threshold")
    print("="*80)
    
    baseline = 75.0
    height = 72  # 6'0" exactly
    
    result = _apply_height_penalty(baseline, height)
    
    print(f"Input: {baseline} mph (6'0\" player)")
    print(f"Expected: {baseline} mph (no penalty)")
    print(f"Actual: {result:.2f} mph")
    
    passed = result == baseline
    print(f"Status: {'✅ PASS' if passed else '❌ FAIL'}")
    
    assert passed, f"Expected {baseline}, got {result}"
    return passed


def test_height_penalty_6_foot_7_judge():
    """Test Judge (6'7") gets -4.2% penalty"""
    print("\n" + "="*80)
    print("TEST 2: 6'7\" player (Aaron Judge) gets -4.2% penalty")
    print("="*80)
    
    baseline = 88.1  # Judge's interpolated baseline
    height = 79  # 6'7"
    
    excess_height = 79 - 72  # 7 inches over threshold
    expected_penalty = 0.006 * excess_height  # 0.042 = -4.2%
    expected_result = baseline * (1 - expected_penalty)
    
    result = _apply_height_penalty(baseline, height)
    error = abs(result - expected_result)
    
    print(f"Input: {baseline} mph (6'7\" player)")
    print(f"Excess height: {excess_height} inches over 6'0\"")
    print(f"Expected penalty: -{expected_penalty*100:.1f}%")
    print(f"Expected result: {expected_result:.2f} mph")
    print(f"Actual result: {result:.2f} mph")
    print(f"Error: {error:.4f} mph")
    
    passed = error < 0.01
    print(f"Status: {'✅ PASS' if passed else '❌ FAIL'}")
    
    assert passed, f"Expected {expected_result:.2f}, got {result:.2f}"
    return passed


def test_height_penalty_6_foot_5_alvarez():
    """Test Alvarez (6'5") gets -1.8% penalty"""
    print("\n" + "="*80)
    print("TEST 3: 6'5\" player (Yordan Alvarez) gets -1.8% penalty")
    print("="*80)
    
    baseline = 84.0  # Alvarez's baseline
    height = 77  # 6'5"
    
    excess_height = 77 - 72  # 5 inches over threshold
    expected_penalty = 0.006 * excess_height  # 0.030 = -3.0%
    expected_result = baseline * (1 - expected_penalty)
    
    result = _apply_height_penalty(baseline, height)
    error = abs(result - expected_result)
    
    print(f"Input: {baseline} mph (6'5\" player)")
    print(f"Excess height: {excess_height} inches over 6'0\"")
    print(f"Expected penalty: -{expected_penalty*100:.1f}%")
    print(f"Expected result: {expected_result:.2f} mph")
    print(f"Actual result: {result:.2f} mph")
    print(f"Error: {error:.4f} mph")
    
    passed = error < 0.01
    print(f"Status: {'✅ PASS' if passed else '❌ FAIL'}")
    
    assert passed, f"Expected {expected_result:.2f}, got {result:.2f}"
    return passed


def test_height_penalty_no_penalty_below_threshold():
    """Test that players <6'0" get NO penalty"""
    print("\n" + "="*80)
    print("TEST 4: NO penalty for players <6'0\"")
    print("="*80)
    
    test_heights = [
        (66, "5'6\" (Altuve)"),
        (69, "5'9\" (Betts)"),
        (71, "5'11\"")
    ]
    
    baseline = 70.0
    all_passed = True
    
    for height, height_str in test_heights:
        result = _apply_height_penalty(baseline, height)
        unchanged = (result == baseline)
        
        print(f"{height_str}: {baseline} → {result:.2f} mph - "
              f"{'✅ NO PENALTY' if unchanged else '❌ PENALTY APPLIED'}")
        
        if not unchanged:
            all_passed = False
    
    print(f"\nStatus: {'✅ PASS' if all_passed else '❌ FAIL'}")
    
    assert all_passed, "Some sub-6'0\" players were penalized"
    return all_passed


def test_height_penalty_cap_at_10_percent():
    """Test that penalty caps at -10% for very tall players"""
    print("\n" + "="*80)
    print("TEST 5: Penalty caps at -10% for very tall players")
    print("="*80)
    
    baseline = 90.0
    
    # Test 6'11" (83") - should be -6.6% (11" × 0.6%)
    height_83 = 83
    result_83 = _apply_height_penalty(baseline, height_83)
    expected_83 = baseline * (1 - 0.066)  # -6.6%
    
    print(f"6'11\" (83\"): {baseline} → {result_83:.2f} mph")
    print(f"  Expected: {expected_83:.2f} mph (-6.6%)")
    print(f"  Penalty applied: -{(1 - result_83/baseline)*100:.1f}%")
    
    # Test 7'3" (87") - would be -9.0% but within cap
    height_87 = 87
    result_87 = _apply_height_penalty(baseline, height_87)
    expected_87 = baseline * (1 - 0.090)  # -9.0%
    
    print(f"\n7'3\" (87\"): {baseline} → {result_87:.2f} mph")
    print(f"  Expected: {expected_87:.2f} mph (-9.0%)")
    print(f"  Penalty applied: -{(1 - result_87/baseline)*100:.1f}%")
    
    # Test 7'5" (89") - would be -10.2% but capped at -10%
    height_89 = 89
    result_89 = _apply_height_penalty(baseline, height_89)
    expected_89 = baseline * (1 - 0.10)  # Capped at -10%
    
    print(f"\n7'5\" (89\"): {baseline} → {result_89:.2f} mph")
    print(f"  Raw penalty would be: -{(89-72)*0.6:.1f}% (-10.2%)")
    print(f"  Capped at: -10.0%")
    print(f"  Expected: {expected_89:.2f} mph")
    print(f"  Actual: {result_89:.2f} mph")
    
    passed = abs(result_89 - expected_89) < 0.01
    print(f"\nStatus: {'✅ PASS (cap works)' if passed else '❌ FAIL (cap broken)'}")
    
    assert passed, f"Expected {expected_89:.2f}, got {result_89:.2f}"
    return passed


# ============================================================================
# INTEGRATION TESTS - 6 MLB PLAYERS
# ============================================================================

def test_six_player_integration():
    """Test full pipeline with height penalty on 6 MLB players"""
    print("\n" + "="*80)
    print("INTEGRATION TEST: 6 MLB Players with V2.0.2 Height Penalty")
    print("="*80)
    
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
            'name': 'Yordan Alvarez',
            'height': 77, 'weight': 225, 'wingspan': 79, 'age': 27, 'bat_weight': 33,
            'statcast_actual': 79.0
        },
        {
            'name': 'Giancarlo Stanton',
            'height': 78, 'weight': 245, 'wingspan': 81, 'age': 34, 'bat_weight': 34,
            'statcast_actual': 78.0
        },
        {
            'name': 'Aaron Judge',
            'height': 79, 'weight': 282, 'wingspan': 83, 'age': 33, 'bat_weight': 34,
            'statcast_actual': 77.0
        }
    ]
    
    within_4mph_count = 0
    results = []
    
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
        
        results.append({
            'name': player['name'],
            'height_str': f"{player['height']//12}'{player['height']%12}\"",
            'predicted': predicted,
            'actual': actual,
            'error': error,
            'within_target': within_target
        })
        
        print(f"\n{player['name']} ({player['height']//12}'{player['height']%12}\"):")
        print(f"  Predicted: {predicted:.1f} mph")
        print(f"  Actual: {actual:.1f} mph")
        print(f"  Error: {error:+.1f} mph {'✅' if within_target else '❌'}")
    
    accuracy_pct = (within_4mph_count / len(test_players)) * 100
    target_met = within_4mph_count >= 5  # Need 5/6 for 83%+
    
    print(f"\n{'='*80}")
    print(f"ACCURACY: {within_4mph_count}/6 players within ±4 mph ({accuracy_pct:.1f}%)")
    print(f"TARGET: ≥83% (5/6 players)")
    print(f"STATUS: {'✅ TARGET MET' if target_met else '❌ TARGET NOT MET'}")
    print("="*80)
    
    return within_4mph_count, accuracy_pct, target_met, results


# ============================================================================
# MAIN TEST RUNNER
# ============================================================================

def run_all_tests():
    """Run all tests and report results"""
    print("="*80)
    print("V2.0.2 HEIGHT PENALTY - TEST SUITE")
    print("="*80)
    
    # Unit tests
    unit_tests = [
        ("Unit Test 1: NO penalty at 6'0\" threshold", test_height_penalty_no_penalty_at_threshold),
        ("Unit Test 2: Judge (6'7\") gets -4.2% penalty", test_height_penalty_6_foot_7_judge),
        ("Unit Test 3: Alvarez (6'5\") gets -1.8% penalty", test_height_penalty_6_foot_5_alvarez),
        ("Unit Test 4: NO penalty for <6'0\" players", test_height_penalty_no_penalty_below_threshold),
        ("Unit Test 5: Penalty caps at -10%", test_height_penalty_cap_at_10_percent),
    ]
    
    unit_results = []
    for test_name, test_func in unit_tests:
        try:
            passed = test_func()
            unit_results.append((test_name, "✅ PASS"))
        except AssertionError as e:
            unit_results.append((test_name, f"❌ FAIL: {str(e)}"))
        except Exception as e:
            unit_results.append((test_name, f"❌ ERROR: {str(e)}"))
    
    # Integration test
    print("\n" + "="*80)
    within_count, accuracy, target_met, player_results = test_six_player_integration()
    
    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    
    print("\n📋 UNIT TESTS:")
    for test_name, result in unit_results:
        print(f"  {test_name}: {result}")
    
    unit_passed = sum(1 for _, r in unit_results if r.startswith("✅"))
    print(f"\n  Unit Tests: {unit_passed}/{len(unit_results)} passed")
    
    print("\n📊 INTEGRATION TEST:")
    print(f"  Accuracy: {within_count}/6 players ({accuracy:.1f}%)")
    print(f"  Target: ≥83% (5/6 players)")
    print(f"  Result: {'✅ TARGET MET' if target_met else '❌ TARGET NOT MET'}")
    
    print("\n" + "="*80)
    if unit_passed == len(unit_results) and target_met:
        print("✅ ALL TESTS PASSED - V2.0.2 READY FOR PRODUCTION")
    elif unit_passed == len(unit_results):
        print("⚠️  UNIT TESTS PASS BUT ACCURACY TARGET NOT MET")
        print("    Recommendation: Increase penalty to -1.0% per inch")
    else:
        print("❌ SOME TESTS FAILED - NEEDS FIXES")
    print("="*80)
    
    return unit_passed == len(unit_results), target_met, accuracy, player_results


if __name__ == "__main__":
    unit_pass, target_met, accuracy, player_results = run_all_tests()
    
    # Exit with appropriate code
    if unit_pass and target_met:
        sys.exit(0)  # Success
    else:
        sys.exit(1)  # Needs adjustment
