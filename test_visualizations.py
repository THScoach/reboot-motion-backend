"""
Priority 5 Test Suite: Visualization System
Tests BiomechanicsVisualizer chart generation
"""

import sys
sys.path.insert(0, '/home/user/webapp')

import os
from physics_engine.visualizations import BiomechanicsVisualizer


def test_chart_generation():
    """Test all chart generation functions"""
    print("="*70)
    print("TEST 1: CHART GENERATION")
    print("="*70)
    
    viz = BiomechanicsVisualizer()
    tests_passed = 0
    total_tests = 5
    
    # Create output directory
    output_dir = '/home/user/webapp/test_output/charts'
    os.makedirs(output_dir, exist_ok=True)
    
    # Test 1.1: Gap Chart
    print("\n✅ Test 1.1: Gap Chart Generation")
    try:
        path = viz.generate_gap_chart(57.9, 76.0, f'{output_dir}/gap_test.png')
        if os.path.exists(path):
            size_kb = os.path.getsize(path) / 1024
            print(f"   ✅ PASS: Gap chart created ({size_kb:.1f} KB)")
            tests_passed += 1
        else:
            print(f"   ❌ FAIL: File not created")
    except Exception as e:
        print(f"   ❌ FAIL: {e}")
    
    # Test 1.2: Radar Chart
    print("\n✅ Test 1.2: Radar Chart Generation")
    try:
        path = viz.generate_gew_radar_chart(72, 85, 40, f'{output_dir}/radar_test.png')
        if os.path.exists(path):
            size_kb = os.path.getsize(path) / 1024
            print(f"   ✅ PASS: Radar chart created ({size_kb:.1f} KB)")
            tests_passed += 1
        else:
            print(f"   ❌ FAIL: File not created")
    except Exception as e:
        print(f"   ❌ FAIL: {e}")
    
    # Test 1.3: Kinematic Sequence
    print("\n✅ Test 1.3: Kinematic Sequence Chart")
    try:
        sequence_data = {
            'pelvis_ms': 150,
            'torso_ms': 100,
            'arm_ms': 50,
            'hand_ms': 10,
            'contact_ms': 0
        }
        path = viz.generate_kinematic_sequence_waterfall(sequence_data, f'{output_dir}/sequence_test.png')
        if os.path.exists(path):
            size_kb = os.path.getsize(path) / 1024
            print(f"   ✅ PASS: Sequence chart created ({size_kb:.1f} KB)")
            tests_passed += 1
        else:
            print(f"   ❌ FAIL: File not created")
    except Exception as e:
        print(f"   ❌ FAIL: {e}")
    
    # Test 1.4: Energy Distribution
    print("\n✅ Test 1.4: Energy Distribution Pie Chart")
    try:
        path = viz.generate_energy_distribution_pie(61, 29, 10, f'{output_dir}/energy_test.png')
        if os.path.exists(path):
            size_kb = os.path.getsize(path) / 1024
            print(f"   ✅ PASS: Energy chart created ({size_kb:.1f} KB)")
            tests_passed += 1
        else:
            print(f"   ❌ FAIL: File not created")
    except Exception as e:
        print(f"   ❌ FAIL: {e}")
    
    # Test 1.5: Composite Report
    print("\n✅ Test 1.5: Composite Report Generation")
    try:
        player_data = {
            'name': 'Eric Williams',
            'age': 33,
            'height_inches': 68,
            'weight_lbs': 190
        }
        
        analysis_data = {
            'actual_bat_speed': 57.9,
            'potential_bat_speed': 76.0,
            'ground_score': 72,
            'engine_score': 85,
            'weapon_score': 40,
            'sequence': {
                'pelvis_ms': 150,
                'torso_ms': 100,
                'arm_ms': 50,
                'hand_ms': 10,
                'contact_ms': 0
            },
            'energy': {
                'lowerhalf_pct': 61,
                'torso_pct': 29,
                'arms_pct': 10
            },
            'recommendations': {
                'primary_component': 'WEAPON',
                'estimated_gain_mph': 7.2,
                'priority': 'CRITICAL',
                'training_frequency': '5-6 days/week'
            }
        }
        
        path = viz.generate_composite_report(player_data, analysis_data, f'{output_dir}/composite_test.png')
        if os.path.exists(path):
            size_kb = os.path.getsize(path) / 1024
            print(f"   ✅ PASS: Composite report created ({size_kb:.1f} KB)")
            tests_passed += 1
        else:
            print(f"   ❌ FAIL: File not created")
    except Exception as e:
        print(f"   ❌ FAIL: {e}")
    
    print(f"\n   Result: {tests_passed}/{total_tests} tests passed")
    return tests_passed == total_tests


def test_file_sizes():
    """Test that file sizes are reasonable (<1MB)"""
    print("\n" + "="*70)
    print("TEST 2: FILE SIZE VALIDATION")
    print("="*70)
    
    output_dir = '/home/user/webapp/test_output/charts'
    tests_passed = 0
    total_tests = 0
    
    if not os.path.exists(output_dir):
        print("\n   ❌ FAIL: Output directory not found")
        return False
    
    print("\n✅ Checking file sizes:")
    for filename in os.listdir(output_dir):
        if filename.endswith('.png'):
            total_tests += 1
            filepath = os.path.join(output_dir, filename)
            size_kb = os.path.getsize(filepath) / 1024
            size_mb = size_kb / 1024
            
            if size_mb < 1.0:
                print(f"   ✅ {filename}: {size_kb:.1f} KB (< 1 MB)")
                tests_passed += 1
            else:
                print(f"   ❌ {filename}: {size_mb:.2f} MB (TOO LARGE)")
    
    print(f"\n   Result: {tests_passed}/{total_tests} files within size limits")
    return tests_passed == total_tests


def test_eric_williams_charts():
    """Generate complete chart set for Eric Williams"""
    print("\n" + "="*70)
    print("TEST 3: ERIC WILLIAMS COMPLETE CHART SET")
    print("="*70)
    
    viz = BiomechanicsVisualizer()
    
    # Output directory
    output_dir = '/home/user/webapp/charts/eric_williams'
    os.makedirs(output_dir, exist_ok=True)
    
    # Eric Williams data
    player_data = {
        'name': 'Eric Williams',
        'age': 33,
        'height_inches': 68,
        'weight_lbs': 190
    }
    
    analysis_data = {
        'actual_bat_speed': 57.9,
        'potential_bat_speed': 76.0,
        'ground_score': 72,
        'engine_score': 85,
        'weapon_score': 40,
        'sequence': {
            'pelvis_ms': 150,
            'torso_ms': 100,
            'arm_ms': 50,
            'hand_ms': 10,
            'contact_ms': 0
        },
        'energy': {
            'lowerhalf_pct': 61,
            'torso_pct': 29,
            'arms_pct': 10
        },
        'recommendations': {
            'primary_component': 'WEAPON',
            'estimated_gain_mph': 7.2,
            'priority': 'CRITICAL',
            'training_frequency': '5-6 days/week'
        }
    }
    
    tests_passed = 0
    total_tests = 5
    
    print("\n✅ Generating charts:")
    
    # 1. Gap chart
    try:
        viz.generate_gap_chart(
            analysis_data['actual_bat_speed'],
            analysis_data['potential_bat_speed'],
            f'{output_dir}/gap.png'
        )
        print(f"   ✅ Gap chart: {output_dir}/gap.png")
        tests_passed += 1
    except Exception as e:
        print(f"   ❌ Gap chart failed: {e}")
    
    # 2. Radar chart
    try:
        viz.generate_gew_radar_chart(
            analysis_data['ground_score'],
            analysis_data['engine_score'],
            analysis_data['weapon_score'],
            f'{output_dir}/radar.png'
        )
        print(f"   ✅ Radar chart: {output_dir}/radar.png")
        tests_passed += 1
    except Exception as e:
        print(f"   ❌ Radar chart failed: {e}")
    
    # 3. Kinematic sequence
    try:
        viz.generate_kinematic_sequence_waterfall(
            analysis_data['sequence'],
            f'{output_dir}/sequence.png'
        )
        print(f"   ✅ Sequence chart: {output_dir}/sequence.png")
        tests_passed += 1
    except Exception as e:
        print(f"   ❌ Sequence chart failed: {e}")
    
    # 4. Energy distribution
    try:
        viz.generate_energy_distribution_pie(
            analysis_data['energy']['lowerhalf_pct'],
            analysis_data['energy']['torso_pct'],
            analysis_data['energy']['arms_pct'],
            f'{output_dir}/energy.png'
        )
        print(f"   ✅ Energy chart: {output_dir}/energy.png")
        tests_passed += 1
    except Exception as e:
        print(f"   ❌ Energy chart failed: {e}")
    
    # 5. Composite report
    try:
        viz.generate_composite_report(
            player_data,
            analysis_data,
            f'{output_dir}/composite_report.png'
        )
        print(f"   ✅ Composite report: {output_dir}/composite_report.png")
        tests_passed += 1
    except Exception as e:
        print(f"   ❌ Composite report failed: {e}")
    
    print(f"\n   Result: {tests_passed}/{total_tests} charts generated")
    print(f"\n   📁 All charts saved to: {output_dir}/")
    
    return tests_passed == total_tests


def main():
    """Run all tests"""
    print("\n" + "🎯"*35)
    print("PRIORITY 5: VISUALIZATION SYSTEM - TEST SUITE")
    print("🎯"*35 + "\n")
    
    # Run all test suites
    test1_passed = test_chart_generation()
    test2_passed = test_file_sizes()
    test3_passed = test_eric_williams_charts()
    
    # Final summary
    print("\n" + "="*70)
    print("FINAL SUMMARY")
    print("="*70)
    
    tests_passed = sum([test1_passed, test2_passed, test3_passed])
    total_tests = 3
    
    print(f"\n   Test 1 - Chart Generation: {'✅ PASS' if test1_passed else '❌ FAIL'}")
    print(f"   Test 2 - File Size Validation: {'✅ PASS' if test2_passed else '❌ FAIL'}")
    print(f"   Test 3 - Eric Williams Charts: {'✅ PASS' if test3_passed else '❌ FAIL'}")
    
    print(f"\n   Overall: {tests_passed}/{total_tests} test suites passed")
    
    if tests_passed == total_tests:
        print("\n   🎉 ALL TESTS PASSED - PRIORITY 5 VISUALIZATION COMPLETE!")
        print("\n   📁 Sample charts: /home/user/webapp/charts/eric_williams/")
        print("="*70 + "\n")
        return 0
    else:
        print("\n   ⚠️  SOME TESTS FAILED - REVIEW NEEDED")
        print("="*70 + "\n")
        return 1


if __name__ == "__main__":
    exit(main())
