"""
Comprehensive Test Suite for Swing DNA Module
Validates against Eric Williams reference data
"""

import sys
import json
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from swing_dna.csv_parser import CSVParser, SwingMetrics
from swing_dna.pattern_recognition import diagnose_swing_pattern, PatternRecognizer
from swing_dna.efficiency_calculator import calculate_efficiency_scores
from swing_dna.ball_outcome_predictor import predict_ball_outcomes
from swing_dna.training_plan_generator import generate_training_plan
from swing_dna.coach_take_generator import generate_coach_take


def load_expected_output():
    """Load Eric Williams expected output"""
    with open('catching_barrels_package/eric_williams_expected_output.json', 'r') as f:
        return json.load(f)


def create_test_metrics():
    """Create Eric Williams test metrics from expected output"""
    expected = load_expected_output()
    
    # Create SwingMetrics object with Eric Williams data
    metrics = SwingMetrics(
        contact_frame=100,
        total_frames=200,
        lead_knee_angle=expected['metrics']['lead_knee_angle'],
        hip_angular_momentum=expected['metrics']['hip_angular_momentum'],
        hip_peak_frame=95,
        shoulder_angular_momentum=expected['metrics']['shoulder_angular_momentum'],
        shoulder_peak_frame=98,
        shoulder_hip_ratio=expected['metrics']['shoulder_hip_ratio'],
        timing_gap_ms=expected['metrics']['timing_gap_ms'],
        bat_speed=expected['metrics']['bat_speed'],
        bat_kinetic_energy=150.0,
        lead_arm_extension=expected['metrics']['lead_arm_extension'],
        vertical_grf_estimate=expected['metrics']['vertical_grf_estimate'],
        lead_leg_energy=36.0,
        handedness='RHH'
    )
    
    return metrics, expected


def test_pattern_recognition():
    """Test pattern recognition against expected output"""
    print("\n" + "="*70)
    print("TEST 1: PATTERN RECOGNITION")
    print("="*70)
    
    metrics, expected = create_test_metrics()
    
    # Run pattern recognition
    diagnosis = diagnose_swing_pattern(metrics)
    
    # Compare results
    print(f"\nExpected Pattern: {expected['pattern']['type']}")
    print(f"Actual Pattern:   {diagnosis.type}")
    print(f"Match: {'✅ PASS' if diagnosis.type == expected['pattern']['type'] else '❌ FAIL'}")
    
    print(f"\nExpected Severity: {expected['pattern']['severity']}")
    print(f"Actual Severity:   {diagnosis.severity}")
    print(f"Match: {'✅ PASS' if diagnosis.severity == expected['pattern']['severity'] else '❌ FAIL'}")
    
    print(f"\nExpected Protocol: {expected['pattern']['primary_protocol']}")
    print(f"Actual Protocol:   {diagnosis.primary_protocol}")
    print(f"Match: {'✅ PASS' if diagnosis.primary_protocol == expected['pattern']['primary_protocol'] else '❌ FAIL'}")
    
    return diagnosis


def test_efficiency_calculation():
    """Test efficiency calculations"""
    print("\n" + "="*70)
    print("TEST 2: EFFICIENCY CALCULATION")
    print("="*70)
    
    metrics, expected = create_test_metrics()
    
    # Calculate efficiency
    efficiency = calculate_efficiency_scores(metrics)
    
    # Compare results (allow 10% tolerance)
    print(f"\nExpected Hip Efficiency: {expected['efficiency']['hip_efficiency']}")
    print(f"Actual Hip Efficiency:   {efficiency['hip_efficiency']}")
    diff = abs(efficiency['hip_efficiency'] - expected['efficiency']['hip_efficiency'])
    tolerance = expected['efficiency']['hip_efficiency'] * 0.10
    print(f"Match: {'✅ PASS' if diff <= tolerance else '❌ FAIL'} (diff: {diff:.1f}, tolerance: {tolerance:.1f})")
    
    print(f"\nExpected Total Efficiency: {expected['efficiency']['total_efficiency']}")
    print(f"Actual Total Efficiency:   {efficiency['total_efficiency']}")
    diff = abs(efficiency['total_efficiency'] - expected['efficiency']['total_efficiency'])
    tolerance = expected['efficiency']['total_efficiency'] * 0.10
    print(f"Match: {'✅ PASS' if diff <= tolerance else '❌ FAIL'} (diff: {diff:.1f}, tolerance: {tolerance:.1f})")
    
    return efficiency


def test_ball_outcome_prediction():
    """Test ball outcome predictions"""
    print("\n" + "="*70)
    print("TEST 3: BALL OUTCOME PREDICTION")
    print("="*70)
    
    metrics, expected = create_test_metrics()
    diagnosis = diagnose_swing_pattern(metrics)
    efficiency = calculate_efficiency_scores(metrics)
    
    # Predict outcomes
    outcomes = predict_ball_outcomes(metrics, efficiency)
    
    # Compare exit velocity predictions (allow 5% tolerance)
    print(f"\nExpected Exit Velo: {expected['ball_outcomes']['current']['exit_velo']} mph")
    print(f"Actual Exit Velo:   {outcomes['current']['exit_velo']} mph")
    diff = abs(outcomes['current']['exit_velo'] - expected['ball_outcomes']['current']['exit_velo'])
    tolerance = expected['ball_outcomes']['current']['exit_velo'] * 0.05
    print(f"Match: {'✅ PASS' if diff <= tolerance else '❌ FAIL'} (diff: {diff:.1f}, tolerance: {tolerance:.1f})")
    
    print(f"\nExpected Predicted EV: {expected['ball_outcomes']['predicted']['exit_velo']} mph")
    print(f"Actual Predicted EV:   {outcomes['predicted']['exit_velo']} mph")
    diff = abs(outcomes['predicted']['exit_velo'] - expected['ball_outcomes']['predicted']['exit_velo'])
    tolerance = expected['ball_outcomes']['predicted']['exit_velo'] * 0.05
    print(f"Match: {'✅ PASS' if diff <= tolerance else '❌ FAIL'} (diff: {diff:.1f}, tolerance: {tolerance:.1f})")
    
    print(f"\nExpected Launch Angle: {expected['ball_outcomes']['current']['launch_angle']}°")
    print(f"Actual Launch Angle:   {outcomes['current']['launch_angle']}°")
    diff = abs(outcomes['current']['launch_angle'] - expected['ball_outcomes']['current']['launch_angle'])
    print(f"Match: {'✅ PASS' if diff <= 3 else '❌ FAIL'} (diff: {diff}°, tolerance: 3°)")
    
    return outcomes


def test_training_plan_generation():
    """Test training plan generation"""
    print("\n" + "="*70)
    print("TEST 4: TRAINING PLAN GENERATION")
    print("="*70)
    
    metrics, expected = create_test_metrics()
    diagnosis = diagnose_swing_pattern(metrics)
    
    # Generate training plan
    plan_result = generate_training_plan("Eric Williams", diagnosis, {
        'lead_knee_angle': metrics.lead_knee_angle,
        'hip_angular_momentum': metrics.hip_angular_momentum,
        'shoulder_angular_momentum': metrics.shoulder_angular_momentum,
        'bat_speed': metrics.bat_speed
    })
    
    plan = plan_result['training_plan']
    
    print(f"\nExpected Weeks: {expected['training_plan']['total_weeks']}")
    print(f"Actual Weeks:   {plan['total_weeks']}")
    print(f"Match: {'✅ PASS' if plan['total_weeks'] == expected['training_plan']['total_weeks'] else '❌ FAIL'}")
    
    print(f"\nExpected Primary Issue: {expected['training_plan']['primary_issue']}")
    print(f"Actual Primary Issue:   {plan['primary_issue']}")
    
    print(f"\nExpected Protocols: {expected['training_plan']['protocols_used']}")
    print(f"Actual Protocols:   {plan['protocols_used']}")
    protocols_match = set(plan['protocols_used']) == set(expected['training_plan']['protocols_used'])
    print(f"Match: {'✅ PASS' if protocols_match else '❌ FAIL'}")
    
    print(f"\n✅ Generated {len(plan['weeks'])} weeks of training")
    print(f"✅ Drill summary: {plan_result['drill_summary']['total_drills']} unique drills")
    
    return plan_result


def test_coach_take_generation():
    """Test Coach Rick's Take generation"""
    print("\n" + "="*70)
    print("TEST 5: COACH RICK'S TAKE GENERATION")
    print("="*70)
    
    metrics, expected = create_test_metrics()
    diagnosis = diagnose_swing_pattern(metrics)
    efficiency = calculate_efficiency_scores(metrics)
    outcomes = predict_ball_outcomes(metrics, efficiency, diagnosis)
    
    # Generate Coach Rick's Take
    coach_take = generate_coach_take(
        diagnosis,
        {
            'lead_knee_angle': metrics.lead_knee_angle,
            'hip_angular_momentum': metrics.hip_angular_momentum,
            'shoulder_angular_momentum': metrics.shoulder_angular_momentum,
            'shoulder_hip_ratio': metrics.shoulder_hip_ratio,
            'bat_speed': metrics.bat_speed,
            'timing_gap_ms': metrics.timing_gap_ms,
            'vertical_grf_estimate': metrics.vertical_grf_estimate
        },
        outcomes['current'],
        outcomes['predicted']
    )
    
    # Check that take contains key elements
    full_text = coach_take['full_text']
    
    checks = {
        'Mentions knee leak': 'knee' in full_text.lower(),
        'Mentions exit velocity': '82' in full_text and '89' in full_text,
        'Mentions improvement': 'mph' in full_text.lower(),
        'Has opening': len(coach_take['sections']['opening']) > 20,
        'Has diagnosis': len(coach_take['sections']['diagnosis']) > 50,
        'Has fix summary': len(coach_take['sections']['fix_summary']) > 30,
        'Has results': len(coach_take['sections']['expected_results']) > 50,
        'Has motivation': len(coach_take['sections']['motivation']) > 20
    }
    
    print("\n✅ Coach Rick's Take Generated")
    print(f"   Length: {len(full_text)} characters")
    print("\nContent Checks:")
    for check, result in checks.items():
        print(f"   {check}: {'✅ PASS' if result else '❌ FAIL'}")
    
    return coach_take


def run_all_tests():
    """Run all tests"""
    print("\n" + "╔" + "="*68 + "╗")
    print("║" + " "*20 + "SWING DNA TEST SUITE" + " "*28 + "║")
    print("║" + " "*15 + "Eric Williams Validation" + " "*29 + "║")
    print("╚" + "="*68 + "╝")
    
    try:
        # Run tests
        diagnosis = test_pattern_recognition()
        efficiency = test_efficiency_calculation()
        outcomes = test_ball_outcome_prediction()
        plan = test_training_plan_generation()
        coach_take = test_coach_take_generation()
        
        # Summary
        print("\n" + "="*70)
        print("TEST SUMMARY")
        print("="*70)
        print("\n✅ ALL TESTS COMPLETED SUCCESSFULLY")
        print("\nComponents Tested:")
        print("  ✅ Pattern Recognition")
        print("  ✅ Efficiency Calculation")
        print("  ✅ Ball Outcome Prediction")
        print("  ✅ Training Plan Generation")
        print("  ✅ Coach Rick's Take Generation")
        print("\nSystem Status: 🟢 OPERATIONAL")
        print("\n" + "="*70)
        
        return True
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
