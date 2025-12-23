"""
Priority 3 Test Suite: Gap Analysis & Recommendations
Tests both GapAnalyzer and RecommendationEngine with Eric Williams data
"""

import sys
sys.path.insert(0, '/home/user/webapp')

from physics_engine.gap_analyzer import GapAnalyzer
from physics_engine.recommendation_engine import RecommendationEngine


def test_gap_analyzer():
    """Test GapAnalyzer with Eric Williams data"""
    print("="*70)
    print("TEST 1: GAP ANALYZER - ERIC WILLIAMS")
    print("="*70)
    
    analyzer = GapAnalyzer()
    
    # Eric Williams test data
    actual_metrics = {
        'bat_speed_mph': 57.9,
        'exit_velocity_mph': 96.7
    }
    
    potential_metrics = {
        'bat_speed_mph': 76.0,
        'exit_velocity_pitched_mph': 122.9
    }
    
    scores = {
        'ground': 72,
        'engine': 85,
        'weapon': 40
    }
    
    # Run analysis
    gap_analysis = analyzer.calculate_complete_gap_analysis(
        actual_metrics,
        potential_metrics,
        scores
    )
    
    # Display results
    print("\n✅ Bat Speed Gap Analysis:")
    print(f"   Actual: {gap_analysis['bat_speed']['actual_mph']} mph")
    print(f"   Potential: {gap_analysis['bat_speed']['potential_mph']} mph")
    print(f"   Gap: {gap_analysis['bat_speed']['gap_mph']} mph")
    print(f"   % Achieved: {gap_analysis['bat_speed']['pct_achieved']}%")
    print(f"   % Untapped: {gap_analysis['bat_speed']['pct_untapped']}%")
    print(f"   Status: {gap_analysis['bat_speed']['status']}")
    
    print("\n✅ Exit Velocity Gap Analysis:")
    if 'exit_velocity' in gap_analysis:
        print(f"   Actual: {gap_analysis['exit_velocity']['actual_mph']} mph")
        print(f"   Potential: {gap_analysis['exit_velocity']['potential_mph']} mph")
        print(f"   Gap: {gap_analysis['exit_velocity']['gap_mph']} mph")
        print(f"   % Achieved: {gap_analysis['exit_velocity']['pct_achieved']}%")
    
    print("\n✅ Weakest Component:")
    print(f"   Component: {gap_analysis['weakest_component']['weakest_component']}")
    print(f"   Score: {gap_analysis['weakest_component']['score']}/100")
    print(f"   Priority: {gap_analysis['weakest_component']['priority']}")
    print(f"   Ranking: {gap_analysis['weakest_component']['components_ranked']}")
    
    print(f"\n✅ Overall Efficiency: {gap_analysis['overall_efficiency']}%")
    print(f"\n✅ Summary:")
    print(f"   {gap_analysis['summary']}")
    
    # Validation checks
    print("\n📋 VALIDATION CHECKS:")
    
    checks_passed = 0
    total_checks = 5
    
    # Check 1: Gap calculation
    if abs(gap_analysis['bat_speed']['gap_mph'] - 18.1) < 0.2:
        print("   ✅ Gap calculation correct (18.1 mph)")
        checks_passed += 1
    else:
        print(f"   ❌ Gap calculation incorrect (expected 18.1, got {gap_analysis['bat_speed']['gap_mph']})")
    
    # Check 2: Percentage achieved
    if abs(gap_analysis['bat_speed']['pct_achieved'] - 76.2) < 0.5:
        print("   ✅ Percentage achieved correct (~76.2%)")
        checks_passed += 1
    else:
        print(f"   ❌ Percentage achieved incorrect (expected 76.2%, got {gap_analysis['bat_speed']['pct_achieved']}%)")
    
    # Check 3: Weakest component identification
    if gap_analysis['weakest_component']['weakest_component'] == 'WEAPON':
        print("   ✅ Weakest component correctly identified (WEAPON)")
        checks_passed += 1
    else:
        print(f"   ❌ Weakest component incorrect (expected WEAPON, got {gap_analysis['weakest_component']['weakest_component']})")
    
    # Check 4: Priority level
    if gap_analysis['weakest_component']['priority'] == 'CRITICAL':
        print("   ✅ Priority level correct (CRITICAL for score 40)")
        checks_passed += 1
    else:
        print(f"   ❌ Priority level incorrect (expected CRITICAL, got {gap_analysis['weakest_component']['priority']})")
    
    # Check 5: Overall efficiency
    expected_efficiency = (72 + 85 + 40) / 3
    if abs(gap_analysis['overall_efficiency'] - expected_efficiency) < 0.5:
        print(f"   ✅ Overall efficiency correct (~{expected_efficiency:.1f}%)")
        checks_passed += 1
    else:
        print(f"   ❌ Overall efficiency incorrect (expected {expected_efficiency:.1f}, got {gap_analysis['overall_efficiency']})")
    
    print(f"\n   Result: {checks_passed}/{total_checks} checks passed")
    
    return gap_analysis, checks_passed == total_checks


def test_recommendation_engine(gap_analysis):
    """Test RecommendationEngine with Eric Williams data"""
    print("\n" + "="*70)
    print("TEST 2: RECOMMENDATION ENGINE - ERIC WILLIAMS (SPINNER)")
    print("="*70)
    
    engine = RecommendationEngine()
    motor_profile = 'SPINNER'
    
    # Generate recommendations
    recommendations = engine.generate_complete_recommendations(
        gap_analysis,
        motor_profile
    )
    
    # Display results
    print("\n✅ Primary Focus:")
    print(f"   Component: {recommendations['primary_focus']['component']}")
    print(f"   Current Score: {recommendations['primary_focus']['current_score']}/100")
    print(f"   Priority: {recommendations['primary_focus']['priority']}")
    print(f"   Estimated Gain: +{recommendations['primary_focus']['estimated_gain_mph']} mph")
    print(f"   Focus Area: {recommendations['primary_focus']['focus_area']}")
    print(f"   Training Frequency: {recommendations['primary_focus']['training_frequency']}")
    print(f"   Drills: {len(recommendations['primary_focus']['recommended_drills'])} drills provided")
    
    print("\n✅ Motor Profile Guidance:")
    print(f"   Profile: {recommendations['motor_profile_guidance']['motor_profile']}")
    print(f"   Issue: {recommendations['motor_profile_guidance']['issue']}")
    print(f"   Primary Fix: {recommendations['motor_profile_guidance']['primary_fix']}")
    print(f"   Guidance: {recommendations['motor_profile_guidance']['guidance'][:80]}...")
    print(f"   Key Drills: {recommendations['motor_profile_guidance']['key_drills']}")
    
    if recommendations['secondary_focus']:
        print("\n✅ Secondary Focus Areas:")
        for rec in recommendations['secondary_focus']:
            print(f"   - {rec['component']}: Score {rec['current_score']}, +{rec['estimated_gain_mph']} mph potential")
    
    print(f"\n✅ Total Estimated Gain: +{recommendations['total_estimated_gain_mph']} mph")
    print(f"   (Would improve from 57.9 mph to ~{57.9 + recommendations['total_estimated_gain_mph']:.1f} mph)")
    
    print("\n✅ Action Plan:")
    for line in recommendations['action_plan'].split('\n'):
        print(f"   {line}")
    
    # Validation checks
    print("\n📋 VALIDATION CHECKS:")
    
    checks_passed = 0
    total_checks = 5
    
    # Check 1: Primary component correct
    if recommendations['primary_focus']['component'] == 'WEAPON':
        print("   ✅ Primary focus correct (WEAPON)")
        checks_passed += 1
    else:
        print(f"   ❌ Primary focus incorrect (expected WEAPON, got {recommendations['primary_focus']['component']})")
    
    # Check 2: Motor profile match
    if recommendations['motor_profile_guidance']['motor_profile'] == 'SPINNER':
        print("   ✅ Motor profile matched (SPINNER)")
        checks_passed += 1
    else:
        print(f"   ❌ Motor profile mismatch")
    
    # Check 3: Estimated gain reasonable (should be ~40-50% of 18.1 mph = 7-9 mph for score 40)
    primary_gain = recommendations['primary_focus']['estimated_gain_mph']
    if 6.0 <= primary_gain <= 10.0:
        print(f"   ✅ Estimated gain reasonable ({primary_gain} mph for CRITICAL weakness)")
        checks_passed += 1
    else:
        print(f"   ❌ Estimated gain unreasonable (expected 6-10 mph, got {primary_gain})")
    
    # Check 4: Training frequency appropriate for CRITICAL priority
    if '5-6 days' in recommendations['primary_focus']['training_frequency']:
        print("   ✅ Training frequency appropriate (5-6 days for CRITICAL)")
        checks_passed += 1
    else:
        print(f"   ❌ Training frequency inappropriate (got {recommendations['primary_focus']['training_frequency']})")
    
    # Check 5: Has recommended drills
    if len(recommendations['primary_focus']['recommended_drills']) >= 3:
        print(f"   ✅ Sufficient drills provided ({len(recommendations['primary_focus']['recommended_drills'])} drills)")
        checks_passed += 1
    else:
        print(f"   ❌ Insufficient drills (got {len(recommendations['primary_focus']['recommended_drills'])})")
    
    print(f"\n   Result: {checks_passed}/{total_checks} checks passed")
    
    return recommendations, checks_passed == total_checks


def test_edge_cases():
    """Test edge cases and error handling"""
    print("\n" + "="*70)
    print("TEST 3: EDGE CASES & ERROR HANDLING")
    print("="*70)
    
    analyzer = GapAnalyzer()
    engine = RecommendationEngine()
    
    checks_passed = 0
    total_checks = 3
    
    # Test 1: Zero potential (division by zero protection)
    print("\n✅ Test: Zero potential handling")
    try:
        result = analyzer.calculate_bat_speed_gap(50.0, 0.0)
        if result['status'] == 'UNKNOWN' and result['gap_mph'] == 0.0:
            print("   ✅ Zero potential handled correctly")
            checks_passed += 1
        else:
            print("   ❌ Zero potential not handled properly")
    except Exception as e:
        print(f"   ❌ Exception with zero potential: {e}")
    
    # Test 2: TITAN profile (elite across all components)
    print("\n✅ Test: TITAN profile (elite player)")
    try:
        titan_gap = {
            'bat_speed': {'gap_mph': 2.0, 'pct_achieved': 97.4},
            'weakest_component': {
                'weakest_component': 'GROUND',
                'score': 92,
                'priority': 'LOW',
                'components_ranked': [('GROUND', 92), ('ENGINE', 95), ('WEAPON', 94)]
            },
            'overall_efficiency': 93.7,
            'summary': 'Elite performance'
        }
        titan_rec = engine.generate_complete_recommendations(titan_gap, 'TITAN')
        if titan_rec['primary_focus']['priority'] == 'LOW':
            print("   ✅ TITAN profile handled correctly (low priority improvement)")
            checks_passed += 1
        else:
            print("   ❌ TITAN profile not handled correctly")
    except Exception as e:
        print(f"   ❌ Exception with TITAN profile: {e}")
    
    # Test 3: Multiple low scores
    print("\n✅ Test: Multiple low scores (balanced weakness)")
    try:
        balanced_gap = {
            'bat_speed': {'gap_mph': 15.0, 'pct_achieved': 70.0},
            'weakest_component': {
                'weakest_component': 'GROUND',
                'score': 55,
                'priority': 'HIGH',
                'components_ranked': [('GROUND', 55), ('ENGINE', 58), ('WEAPON', 62)]
            },
            'overall_efficiency': 58.3,
            'summary': 'Multiple weak areas'
        }
        balanced_rec = engine.generate_complete_recommendations(balanced_gap, 'BALANCED')
        if len(balanced_rec['secondary_focus']) == 2:  # Should have 2 secondary areas
            print("   ✅ Multiple weak areas handled (2 secondary focus areas)")
            checks_passed += 1
        else:
            print(f"   ❌ Multiple weak areas not handled properly (got {len(balanced_rec['secondary_focus'])} secondary)")
    except Exception as e:
        print(f"   ❌ Exception with balanced weakness: {e}")
    
    print(f"\n   Result: {checks_passed}/{total_checks} checks passed")
    
    return checks_passed == total_checks


def main():
    """Run all tests"""
    print("\n" + "🎯"*35)
    print("PRIORITY 3: GAP ANALYSIS & RECOMMENDATIONS - TEST SUITE")
    print("🎯"*35 + "\n")
    
    # Test 1: Gap Analyzer
    gap_analysis, test1_passed = test_gap_analyzer()
    
    # Test 2: Recommendation Engine
    recommendations, test2_passed = test_recommendation_engine(gap_analysis)
    
    # Test 3: Edge Cases
    test3_passed = test_edge_cases()
    
    # Final summary
    print("\n" + "="*70)
    print("FINAL SUMMARY")
    print("="*70)
    
    tests_passed = sum([test1_passed, test2_passed, test3_passed])
    total_tests = 3
    
    print(f"\n   Test 1 - Gap Analyzer: {'✅ PASS' if test1_passed else '❌ FAIL'}")
    print(f"   Test 2 - Recommendation Engine: {'✅ PASS' if test2_passed else '❌ FAIL'}")
    print(f"   Test 3 - Edge Cases: {'✅ PASS' if test3_passed else '❌ FAIL'}")
    
    print(f"\n   Overall: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("\n   🎉 ALL TESTS PASSED - PRIORITY 3 COMPLETE!")
        print("="*70 + "\n")
        return 0
    else:
        print("\n   ⚠️  SOME TESTS FAILED - REVIEW NEEDED")
        print("="*70 + "\n")
        return 1


if __name__ == "__main__":
    exit(main())
