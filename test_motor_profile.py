"""
Priority 4 Test Suite: Motor Profile Classification Refinement
Tests MotorProfileClassifier and ProfileComparison modules
"""

import sys
sys.path.insert(0, '/home/user/webapp')

from physics_engine.motor_profile_classifier import MotorProfileClassifier
from physics_engine.profile_comparisons import ProfileComparison


def test_motor_profile_classifier():
    """Test MotorProfileClassifier with multiple profile types"""
    print("="*70)
    print("TEST 1: MOTOR PROFILE CLASSIFIER")
    print("="*70)
    
    classifier = MotorProfileClassifier()
    tests_passed = 0
    total_tests = 5
    
    # Test 1.1: SPINNER (Eric Williams)
    print("\n✅ Test 1.1: SPINNER Profile (Eric Williams)")
    result = classifier.classify_with_confidence(
        ground_score=72,
        engine_score=85,
        weapon_score=40
    )
    print(f"   Profile: {result['profile']}")
    print(f"   Confidence: {result['confidence']}%")
    print(f"   Characteristics: {len(result['characteristics'])} traits identified")
    
    if result['profile'] == 'SPINNER' and result['confidence'] > 50:
        print("   ✅ PASS: Correctly identified SPINNER")
        tests_passed += 1
    else:
        print(f"   ❌ FAIL: Expected SPINNER, got {result['profile']}")
    
    # Test 1.2: TITAN (Elite player)
    print("\n✅ Test 1.2: TITAN Profile (Elite)")
    result = classifier.classify_with_confidence(
        ground_score=92,
        engine_score=90,
        weapon_score=88
    )
    print(f"   Profile: {result['profile']}")
    print(f"   Confidence: {result['confidence']}%")
    
    if result['profile'] == 'TITAN' and result['confidence'] > 80:
        print("   ✅ PASS: Correctly identified TITAN with high confidence")
        tests_passed += 1
    else:
        print(f"   ❌ FAIL: Expected TITAN with high confidence")
    
    # Test 1.3: WHIPPER (Upper body dominant)
    print("\n✅ Test 1.3: WHIPPER Profile (Upper body dominant)")
    result = classifier.classify_with_confidence(
        ground_score=45,
        engine_score=60,
        weapon_score=78
    )
    print(f"   Profile: {result['profile']}")
    print(f"   Confidence: {result['confidence']}%")
    
    if result['profile'] == 'WHIPPER' and result['confidence'] > 40:
        print("   ✅ PASS: Correctly identified WHIPPER")
        tests_passed += 1
    else:
        print(f"   ❌ FAIL: Expected WHIPPER, got {result['profile']}")
    
    # Test 1.4: BALANCED (Similar scores)
    print("\n✅ Test 1.4: BALANCED Profile (Similar scores)")
    result = classifier.classify_with_confidence(
        ground_score=68,
        engine_score=72,
        weapon_score=65
    )
    print(f"   Profile: {result['profile']}")
    print(f"   Confidence: {result['confidence']}%")
    print(f"   Profile Scores: {result['profile_scores']}")
    
    # BALANCED should have high score when all components are similar
    if result['profile_scores']['BALANCED'] > 80:
        print("   ✅ PASS: BALANCED score high for similar components")
        tests_passed += 1
    else:
        print(f"   ❌ FAIL: BALANCED score should be high")
    
    # Test 1.5: Edge case - All equal scores
    print("\n✅ Test 1.5: Edge Case (All equal scores)")
    result = classifier.classify_with_confidence(
        ground_score=70,
        engine_score=70,
        weapon_score=70
    )
    print(f"   Profile: {result['profile']}")
    print(f"   Confidence: {result['confidence']}%")
    
    # Should be BALANCED with very high confidence
    if result['profile'] == 'BALANCED' and result['confidence'] > 90:
        print("   ✅ PASS: Perfect BALANCED detection")
        tests_passed += 1
    else:
        print(f"   ❌ FAIL: Expected BALANCED with very high confidence")
    
    print(f"\n   Result: {tests_passed}/{total_tests} tests passed")
    return tests_passed == total_tests


def test_profile_insights():
    """Test profile insights retrieval"""
    print("\n" + "="*70)
    print("TEST 2: PROFILE INSIGHTS")
    print("="*70)
    
    classifier = MotorProfileClassifier()
    tests_passed = 0
    total_tests = 3
    
    # Test 2.1: Get SPINNER insights
    print("\n✅ Test 2.1: SPINNER Insights")
    insights = classifier.get_profile_insights('SPINNER')
    print(f"   Name: {insights['name']}")
    print(f"   Description: {insights['description'][:50]}...")
    print(f"   Famous Examples: {len(insights['famous_examples'])} players")
    print(f"   Advantages: {len(insights['advantages'])} listed")
    print(f"   Improvement Priority: {insights['improvement_priority']}")
    
    if (insights['name'] == 'SPINNER' and 
        len(insights['famous_examples']) > 0 and
        insights['improvement_priority'] == 'WEAPON - Connect hands to rotation'):
        print("   ✅ PASS: SPINNER insights complete")
        tests_passed += 1
    else:
        print("   ❌ FAIL: SPINNER insights incomplete")
    
    # Test 2.2: Get all profiles info
    print("\n✅ Test 2.2: All Profiles Info")
    all_profiles = classifier.get_all_profiles_info()
    print(f"   Total Profiles: {len(all_profiles)}")
    
    if len(all_profiles) == 5:  # Should have 5 profiles
        print("   ✅ PASS: All 5 profiles returned")
        tests_passed += 1
    else:
        print(f"   ❌ FAIL: Expected 5 profiles, got {len(all_profiles)}")
    
    # Test 2.3: Verify each profile has complete info
    print("\n✅ Test 2.3: Profile Completeness Check")
    required_keys = ['name', 'description', 'famous_examples', 'advantages', 
                     'disadvantages', 'improvement_priority']
    all_complete = True
    
    for profile_info in all_profiles:
        missing = [key for key in required_keys if key not in profile_info]
        if missing:
            print(f"   ❌ {profile_info.get('name', 'Unknown')} missing: {missing}")
            all_complete = False
    
    if all_complete:
        print("   ✅ PASS: All profiles have complete information")
        tests_passed += 1
    else:
        print("   ❌ FAIL: Some profiles incomplete")
    
    print(f"\n   Result: {tests_passed}/{total_tests} tests passed")
    return tests_passed == total_tests


def test_profile_comparisons():
    """Test ProfileComparison with different age groups"""
    print("\n" + "="*70)
    print("TEST 3: PROFILE COMPARISONS")
    print("="*70)
    
    comparison = ProfileComparison()
    tests_passed = 0
    total_tests = 5
    
    # Test 3.1: Eric Williams (adult, 33 years old)
    print("\n✅ Test 3.1: Eric Williams (Adult, 33 years)")
    eric_metrics = {
        'bat_speed_mph': 76.0,
        'exit_velocity_mph': 100.0,
        'ground_score': 72,
        'engine_score': 85,
        'weapon_score': 40
    }
    result = comparison.compare_to_benchmarks(eric_metrics, 33)
    
    print(f"   Age Group: {result['age_group']}")
    print(f"   Bat Speed Rating: {result['bat_speed_mph']['rating']}")
    print(f"   Bat Speed Percentile: {result['bat_speed_mph']['percentile']}th")
    print(f"   Overall Rating: {result['overall_rating']}")
    
    if (result['age_group'] == 'adult' and 
        result['bat_speed_mph']['rating'] == 'ABOVE_AVERAGE'):
        print("   ✅ PASS: Eric Williams correctly rated")
        tests_passed += 1
    else:
        print("   ❌ FAIL: Incorrect rating for Eric Williams")
    
    # Test 3.2: Connor Gray (high school, 16 years old)
    print("\n✅ Test 3.2: Connor Gray (High School, 16 years)")
    connor_metrics = {
        'bat_speed_mph': 57.5,
        'ground_score': 65,
        'engine_score': 70,
        'weapon_score': 55
    }
    result = comparison.compare_to_benchmarks(connor_metrics, 16)
    
    print(f"   Age Group: {result['age_group']}")
    print(f"   Bat Speed Rating: {result['bat_speed_mph']['rating']}")
    print(f"   Overall Rating: {result['overall_rating']}")
    
    if result['age_group'] == 'high_school':
        print("   ✅ PASS: Connor Gray in correct age group")
        tests_passed += 1
    else:
        print(f"   ❌ FAIL: Wrong age group for Connor Gray")
    
    # Test 3.3: Elite MLB player
    print("\n✅ Test 3.3: Elite MLB Player (28 years)")
    elite_metrics = {
        'bat_speed_mph': 82.0,
        'exit_velocity_mph': 110.0,
        'ground_score': 91,
        'engine_score': 93,
        'weapon_score': 89
    }
    result = comparison.compare_to_benchmarks(elite_metrics, 28)
    
    print(f"   Bat Speed Rating: {result['bat_speed_mph']['rating']}")
    print(f"   Bat Speed Percentile: {result['bat_speed_mph']['percentile']}th")
    print(f"   Overall Rating: {result['overall_rating']}")
    
    if result['overall_rating'] == 'ELITE':
        print("   ✅ PASS: Elite player correctly identified")
        tests_passed += 1
    else:
        print(f"   ❌ FAIL: Elite player should have ELITE rating")
    
    # Test 3.4: Youth player
    print("\n✅ Test 3.4: Youth Player (12 years)")
    youth_metrics = {
        'bat_speed_mph': 48.0,
        'ground_score': 65,
        'engine_score': 68,
        'weapon_score': 60
    }
    result = comparison.compare_to_benchmarks(youth_metrics, 12)
    
    print(f"   Age Group: {result['age_group']}")
    print(f"   Bat Speed Rating: {result['bat_speed_mph']['rating']}")
    
    if result['age_group'] == 'youth':
        print("   ✅ PASS: Youth player in correct age group")
        tests_passed += 1
    else:
        print(f"   ❌ FAIL: Wrong age group for youth player")
    
    # Test 3.5: Percentile calculation
    print("\n✅ Test 3.5: Percentile Calculations")
    # Elite performance should be 90+ percentile
    elite_bat_speed = comparison.compare_metric('bat_speed_mph', 82.0, 'adult')
    # Average performance should be ~50 percentile
    avg_bat_speed = comparison.compare_metric('bat_speed_mph', 70.0, 'adult')
    
    print(f"   Elite (82 mph): {elite_bat_speed['percentile']}th percentile")
    print(f"   Average (70 mph): {avg_bat_speed['percentile']}th percentile")
    
    if elite_bat_speed['percentile'] >= 85 and 40 <= avg_bat_speed['percentile'] <= 60:
        print("   ✅ PASS: Percentile calculations reasonable")
        tests_passed += 1
    else:
        print("   ❌ FAIL: Percentile calculations off")
    
    print(f"\n   Result: {tests_passed}/{total_tests} tests passed")
    return tests_passed == total_tests


def test_integration():
    """Test integration of both modules together"""
    print("\n" + "="*70)
    print("TEST 4: INTEGRATION TEST")
    print("="*70)
    
    classifier = MotorProfileClassifier()
    comparison = ProfileComparison()
    tests_passed = 0
    total_tests = 2
    
    # Test 4.1: Complete analysis for Eric Williams
    print("\n✅ Test 4.1: Complete Analysis (Eric Williams)")
    
    # Classification
    profile_result = classifier.classify_with_confidence(
        ground_score=72,
        engine_score=85,
        weapon_score=40
    )
    
    # Comparison
    metrics = {
        'bat_speed_mph': 76.0,
        'ground_score': 72,
        'engine_score': 85,
        'weapon_score': 40
    }
    benchmark_result = comparison.compare_to_benchmarks(metrics, 33)
    
    # Insights
    insights = classifier.get_profile_insights(profile_result['profile'])
    
    print(f"   Motor Profile: {profile_result['profile']} ({profile_result['confidence']}% confidence)")
    print(f"   Age Group: {benchmark_result['age_group']}")
    print(f"   Bat Speed: {benchmark_result['bat_speed_mph']['rating']} ({benchmark_result['bat_speed_mph']['percentile']}th percentile)")
    print(f"   Improvement Priority: {insights['improvement_priority']}")
    
    if (profile_result['profile'] == 'SPINNER' and
        benchmark_result['bat_speed_mph']['rating'] == 'ABOVE_AVERAGE' and
        'WEAPON' in insights['improvement_priority']):
        print("   ✅ PASS: Complete analysis coherent")
        tests_passed += 1
    else:
        print("   ❌ FAIL: Analysis results don't align")
    
    # Test 4.2: Verify consistency across modules
    print("\n✅ Test 4.2: Cross-Module Consistency")
    
    # Profile says WEAPON needs work
    weakest_from_profile = profile_result['characteristics']
    weapon_issue = any('Poor energy transfer' in char or 'hands' in char.lower() 
                      for char in weakest_from_profile)
    
    # Benchmarks show WEAPON is below average
    weapon_below_avg = benchmark_result['weapon_score']['rating'] in ['BELOW_AVERAGE', 'AVERAGE']
    
    # Insights say improve WEAPON
    insights_weapon = 'WEAPON' in insights['improvement_priority']
    
    print(f"   Profile identifies hand/weapon issue: {weapon_issue}")
    print(f"   Benchmark shows weapon below average: {weapon_below_avg}")
    print(f"   Insights recommend weapon improvement: {insights_weapon}")
    
    if weapon_issue and weapon_below_avg and insights_weapon:
        print("   ✅ PASS: All modules agree on weakness")
        tests_passed += 1
    else:
        print("   ❌ FAIL: Modules not consistent")
    
    print(f"\n   Result: {tests_passed}/{total_tests} tests passed")
    return tests_passed == total_tests


def main():
    """Run all tests"""
    print("\n" + "🎯"*35)
    print("PRIORITY 4: MOTOR PROFILE CLASSIFICATION - TEST SUITE")
    print("🎯"*35 + "\n")
    
    # Run all test suites
    test1_passed = test_motor_profile_classifier()
    test2_passed = test_profile_insights()
    test3_passed = test_profile_comparisons()
    test4_passed = test_integration()
    
    # Final summary
    print("\n" + "="*70)
    print("FINAL SUMMARY")
    print("="*70)
    
    tests_passed = sum([test1_passed, test2_passed, test3_passed, test4_passed])
    total_tests = 4
    
    print(f"\n   Test 1 - Motor Profile Classifier: {'✅ PASS' if test1_passed else '❌ FAIL'}")
    print(f"   Test 2 - Profile Insights: {'✅ PASS' if test2_passed else '❌ FAIL'}")
    print(f"   Test 3 - Profile Comparisons: {'✅ PASS' if test3_passed else '❌ FAIL'}")
    print(f"   Test 4 - Integration: {'✅ PASS' if test4_passed else '❌ FAIL'}")
    
    print(f"\n   Overall: {tests_passed}/{total_tests} test suites passed")
    
    if tests_passed == total_tests:
        print("\n   🎉 ALL TESTS PASSED - PRIORITY 4 COMPLETE!")
        print("="*70 + "\n")
        return 0
    else:
        print("\n   ⚠️  SOME TESTS FAILED - REVIEW NEEDED")
        print("="*70 + "\n")
        return 1


if __name__ == "__main__":
    exit(main())
