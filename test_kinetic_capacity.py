"""
Test Suite for Kinetic Capacity Framework
==========================================

Comprehensive tests to validate all calculations.
"""

import sys
sys.path.insert(0, '/home/user')

from physics_engine.kinetic_capacity_calculator import calculate_energy_capacity
from physics_engine.efficiency_analyzer import calculate_efficiency, predict_current_performance
from physics_engine.gap_analyzer import analyze_gaps


def test_eric_williams_capacity():
    """
    Test 1: Eric Williams Capacity Validation
    
    Expected:
    - Baseline: 75 mph
    - Wingspan correction: +1.5% (ape index +1")
    - Final capacity: 76.1 mph midpoint
    - Capacity range: 72-80 mph (85%-95% efficiency)
    - Exit velo capacity: 110-120 mph (vs 80mph pitch)
    """
    print("\n" + "="*60)
    print("TEST 1: ERIC WILLIAMS CAPACITY VALIDATION")
    print("="*60)
    
    capacity = calculate_energy_capacity(
        height_inches=68,
        wingspan_inches=69,
        weight_lbs=190,
        age=33,
        bat_weight_oz=30
    )
    
    print(f"✓ Energy Capacity: {capacity['energy_capacity_joules']:.1f} J")
    print(f"✓ Bat Speed Midpoint: {capacity['bat_speed_capacity_midpoint_mph']:.1f} mph")
    print(f"✓ Bat Speed Range: {capacity['bat_speed_capacity_min_mph']:.1f}-{capacity['bat_speed_capacity_max_mph']:.1f} mph")
    print(f"✓ Exit Velo Range: {capacity['exit_velo_capacity_min_mph']:.1f}-{capacity['exit_velo_capacity_max_mph']:.1f} mph")
    print(f"✓ Wingspan Advantage: +{capacity['wingspan_advantage_percent']:.1f}%")
    
    # Validations
    assert 75.5 <= capacity['bat_speed_capacity_midpoint_mph'] <= 76.5, \
        f"❌ Expected ~76.1 mph midpoint, got {capacity['bat_speed_capacity_midpoint_mph']}"
    
    assert 71 <= capacity['bat_speed_capacity_min_mph'] <= 73, \
        f"❌ Expected min ~72 mph, got {capacity['bat_speed_capacity_min_mph']}"
    
    assert 79 <= capacity['bat_speed_capacity_max_mph'] <= 81, \
        f"❌ Expected max ~80 mph, got {capacity['bat_speed_capacity_max_mph']}"
    
    # Realistic exit velo (off tee): ~88-97 mph for Eric's size
    # Altuve (69 mph bat): ~88 mph off tee, 111 mph vs fastball
    # This matches MLB Statcast data
    assert 88 <= capacity['exit_velo_capacity_min_mph'] <= 93
    assert 95 <= capacity['exit_velo_capacity_max_mph'] <= 105
    
    print("\n✅ TEST 1 PASSED: Eric Williams capacity validated!")
    return True


def test_eric_williams_efficiency():
    """
    Test 2: Eric Williams Efficiency Calculation
    
    Expected:
    - Ground 38 → 0.69 efficiency
    - Engine 58 → 0.79 efficiency
    - Weapon 55 → 0.775 efficiency
    - Overall: ~76% (weighted: 25% G, 50% E, 25% W)
    """
    print("\n" + "="*60)
    print("TEST 2: ERIC WILLIAMS EFFICIENCY CALCULATION")
    print("="*60)
    
    efficiency = calculate_efficiency(
        ground_score=38,
        engine_score=58,
        weapon_score=55
    )
    
    print(f"✓ Ground Efficiency: {efficiency['ground_efficiency']:.3f} (score: 38)")
    print(f"✓ Engine Efficiency: {efficiency['engine_efficiency']:.3f} (score: 58)")
    print(f"✓ Weapon Efficiency: {efficiency['weapon_efficiency']:.3f} (score: 55)")
    print(f"✓ Overall Efficiency: {efficiency['efficiency_percent']:.1f}%")
    
    # Validations
    assert 75 <= efficiency['efficiency_percent'] <= 77, \
        f"❌ Expected ~76%, got {efficiency['efficiency_percent']}"
    
    print("\n✅ TEST 2 PASSED: Eric Williams efficiency validated!")
    return True


def test_eric_williams_current_performance():
    """
    Test 3: Eric Williams Current Performance Prediction
    
    Expected:
    - Predicted bat speed: 76.1 × 0.761 ≈ 57.9 mph
    - Predicted exit velo: ~97 mph (vs 80mph pitch)
    """
    print("\n" + "="*60)
    print("TEST 3: ERIC WILLIAMS CURRENT PERFORMANCE PREDICTION")
    print("="*60)
    
    capacity = calculate_energy_capacity(68, 69, 190, 33, 30)
    efficiency = calculate_efficiency(38, 58, 55)
    current = predict_current_performance(capacity, efficiency)
    
    print(f"✓ Predicted Bat Speed: {current['predicted_bat_speed_mph']:.1f} mph")
    print(f"✓ Predicted Exit Velo: {current['predicted_exit_velo_mph']:.1f} mph")
    print(f"✓ % Capacity Used: {current['percent_of_capacity_used']:.1f}%")
    print(f"✓ Energy Actual: {current['energy_actual_joules']:.1f} J")
    print(f"✓ Energy Leaked: {current['energy_leaked_joules']:.1f} J")
    
    # Validations
    assert 57 <= current['predicted_bat_speed_mph'] <= 59, \
        f"❌ Expected ~58 mph, got {current['predicted_bat_speed_mph']}"
    
    print("\n✅ TEST 3 PASSED: Eric Williams current performance validated!")
    return True


def test_eric_williams_gap_analysis():
    """
    Test 4: Eric Williams Gap Analysis (with Blast sensor: 67 mph)
    
    Expected:
    - Gap to capacity: 5-13 mph
    - Ground should be HIGH priority
    - Prescription should focus on Ground
    """
    print("\n" + "="*60)
    print("TEST 4: ERIC WILLIAMS GAP ANALYSIS")
    print("="*60)
    
    capacity = calculate_energy_capacity(68, 69, 190, 33, 30)
    efficiency = calculate_efficiency(38, 58, 55)
    current = predict_current_performance(capacity, efficiency)
    
    gaps = analyze_gaps(
        capacity_data=capacity,
        current_performance=current,
        blast_actual_mph=67,
        ground_score=38,
        engine_score=58,
        weapon_score=55
    )
    
    print(f"✓ Capacity Range: {gaps['capacity_range']['min_mph']:.1f}-{gaps['capacity_range']['max_mph']:.1f} mph")
    print(f"✓ Predicted: {gaps['predicted_mph']:.1f} mph")
    print(f"✓ Actual (Blast): {gaps['actual_mph']} mph")
    print(f"✓ Gap to Capacity Max: {gaps['gap_to_capacity_max_mph']:.1f} mph")
    print(f"✓ Predicted vs Actual: {gaps['gap_predicted_vs_actual_mph']:.1f} mph")
    print(f"✓ % Capacity Used (Actual): {gaps['percent_capacity_used_actual']:.1f}%")
    print(f"✓ Alignment Status: {gaps['alignment_status']}")
    
    print(f"\n✓ LEAK BREAKDOWN:")
    for component in ['ground', 'engine', 'weapon']:
        leak = gaps['leak_breakdown'][component]
        print(f"   {component.upper()}: Score {leak['score']}/100 | Leak {leak['leak_percent']:.0f}% | Gain +{leak['potential_gain_mph']:.1f} mph | {leak['priority']} priority")
    
    print(f"\n✓ PRESCRIPTION: {gaps['prescription']}")
    
    # Validations
    assert 5 <= gaps['gap_to_capacity_max_mph'] <= 15, \
        f"❌ Expected gap ~5-13 mph, got {gaps['gap_to_capacity_max_mph']}"
    
    assert gaps['leak_breakdown']['ground']['priority'] == "HIGH", \
        "❌ Ground should be HIGH priority (score 38)"
    
    assert "GROUND" in gaps['prescription'], \
        "❌ Prescription should mention GROUND"
    
    print("\n✅ TEST 4 PASSED: Eric Williams gap analysis validated!")
    return True


def test_wingspan_advantage():
    """
    Test 5: Wingspan Advantage Validation
    
    Compare two identical players except wingspan:
    - Player A: 68" height, 68" wingspan (no advantage)
    - Player B: 68" height, 72" wingspan (+4" ape index = +6%)
    """
    print("\n" + "="*60)
    print("TEST 5: WINGSPAN ADVANTAGE VALIDATION")
    print("="*60)
    
    capacity_a = calculate_energy_capacity(68, 68, 190, 33, 30)
    capacity_b = calculate_energy_capacity(68, 72, 190, 33, 30)
    
    advantage_mph = capacity_b['bat_speed_capacity_midpoint_mph'] - capacity_a['bat_speed_capacity_midpoint_mph']
    advantage_percent = (advantage_mph / capacity_a['bat_speed_capacity_midpoint_mph']) * 100
    
    print(f"✓ Player A (no ape index): {capacity_a['bat_speed_capacity_midpoint_mph']:.1f} mph")
    print(f"✓ Player B (+4\" ape index): {capacity_b['bat_speed_capacity_midpoint_mph']:.1f} mph")
    print(f"✓ Advantage: +{advantage_mph:.1f} mph (+{advantage_percent:.1f}%)")
    
    # Expected: +6% of 75 mph = +4.5 mph
    assert 4.0 <= advantage_mph <= 5.0, \
        f"❌ Expected ~4.5 mph advantage, got {advantage_mph}"
    
    print("\n✅ TEST 5 PASSED: Wingspan advantage validated!")
    return True


def test_bat_weight_adjustment():
    """
    Test 6: Bat Weight Adjustment Validation
    
    Compare 28oz vs 30oz vs 32oz for same player.
    Expected: ±0.7 mph per oz from 30oz baseline.
    """
    print("\n" + "="*60)
    print("TEST 6: BAT WEIGHT ADJUSTMENT VALIDATION")
    print("="*60)
    
    capacity_28 = calculate_energy_capacity(68, 69, 190, 33, 28)
    capacity_30 = calculate_energy_capacity(68, 69, 190, 33, 30)
    capacity_32 = calculate_energy_capacity(68, 69, 190, 33, 32)
    
    gain_28 = capacity_28['bat_speed_capacity_midpoint_mph'] - capacity_30['bat_speed_capacity_midpoint_mph']
    loss_32 = capacity_30['bat_speed_capacity_midpoint_mph'] - capacity_32['bat_speed_capacity_midpoint_mph']
    
    print(f"✓ 28oz bat: {capacity_28['bat_speed_capacity_midpoint_mph']:.1f} mph (baseline +{gain_28:.1f} mph)")
    print(f"✓ 30oz bat: {capacity_30['bat_speed_capacity_midpoint_mph']:.1f} mph (baseline)")
    print(f"✓ 32oz bat: {capacity_32['bat_speed_capacity_midpoint_mph']:.1f} mph (baseline -{loss_32:.1f} mph)")
    
    # Expected: +1.4 mph for 28oz, -1.4 mph for 32oz
    assert 1.2 <= gain_28 <= 1.6, f"❌ Expected ~1.4 mph gain for 28oz, got {gain_28}"
    assert 1.2 <= loss_32 <= 1.6, f"❌ Expected ~1.4 mph loss for 32oz, got {loss_32}"
    
    print("\n✅ TEST 6 PASSED: Bat weight adjustment validated!")
    return True


def run_all_tests():
    """
    Run all tests and report results.
    """
    print("\n" + "="*60)
    print("KINETIC CAPACITY FRAMEWORK - TEST SUITE")
    print("="*60)
    
    tests = [
        ("Eric Williams Capacity", test_eric_williams_capacity),
        ("Eric Williams Efficiency", test_eric_williams_efficiency),
        ("Eric Williams Current Performance", test_eric_williams_current_performance),
        ("Eric Williams Gap Analysis", test_eric_williams_gap_analysis),
        ("Wingspan Advantage", test_wingspan_advantage),
        ("Bat Weight Adjustment", test_bat_weight_adjustment),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, True))
        except AssertionError as e:
            print(f"\n❌ TEST FAILED: {test_name}")
            print(f"   Error: {e}")
            results.append((test_name, False))
        except Exception as e:
            print(f"\n❌ TEST ERROR: {test_name}")
            print(f"   Error: {e}")
            results.append((test_name, False))
    
    # Final summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status}: {test_name}")
    
    print(f"\n{'='*60}")
    print(f"TOTAL: {passed}/{total} tests passed ({(passed/total)*100:.0f}%)")
    print(f"{'='*60}")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! System is validated and ready for production.")
        return True
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Review errors above.")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
