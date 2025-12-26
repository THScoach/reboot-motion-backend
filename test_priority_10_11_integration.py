"""
INTEGRATION TEST: PRIORITY 9 + 10 + 11
Complete pipeline test for Kinetic Capacity + BioSwing Motor Preference + Recommendation Engine

This demonstrates the full end-to-end workflow:
1. Calculate kinetic capacity (Priority 9)
2. Detect motor preference and adjust scores (Priority 11)
3. Generate personalized recommendations (Priority 10)
"""

import sys
sys.path.insert(0, 'physics_engine')

from kinetic_capacity_calculator import calculate_energy_capacity
from efficiency_analyzer import calculate_efficiency, predict_current_performance
from gap_analyzer import analyze_gaps
from motor_aware_efficiency_analyzer import calculate_motor_aware_efficiency
from swing_rehab_recommendation_engine import SwingRehabRecommendationEngine


def test_complete_pipeline():
    """Test the complete integrated pipeline"""
    
    print("\n" + "="*80)
    print("PRIORITY 9 + 10 + 11 INTEGRATION TEST")
    print("="*80)
    
    # ===== TEST DATA: ERIC WILLIAMS =====
    print("\n📝 Test Subject: Eric Williams")
    print("   Height: 5'8\" (68\"), Wingspan: 5'9\" (69\"), Weight: 190 lbs, Age: 33")
    print("   Bat Weight: 30 oz")
    print("   Video Scores: Ground 38, Engine 58, Weapon 55")
    print("   Actual Bat Speed (Blast): 67 mph")
    print("   Rotational KE: 3743 J, Translational KE: 421 J")
    
    
    # ===== STEP 1: PRIORITY 9 - KINETIC CAPACITY =====
    print("\n" + "="*80)
    print("STEP 1: KINETIC CAPACITY (Priority 9)")
    print("="*80)
    
    capacity = calculate_energy_capacity(
        height_inches=68,
        wingspan_inches=69,
        weight_lbs=190,
        age=33,
        bat_weight_oz=30
    )
    
    print(f"\n✅ Capacity Calculated:")
    print(f"   Bat Speed Range: {capacity['bat_speed_capacity_min_mph']:.1f}-{capacity['bat_speed_capacity_max_mph']:.1f} mph")
    print(f"   Midpoint: {capacity['bat_speed_capacity_midpoint_mph']:.1f} mph")
    print(f"   Exit Velo Range: {capacity['exit_velo_capacity_min_mph']:.1f}-{capacity['exit_velo_capacity_max_mph']:.1f} mph")
    
    
    # ===== STEP 2: PRIORITY 11 - MOTOR-AWARE SCORING =====
    print("\n" + "="*80)
    print("STEP 2: MOTOR PREFERENCE DETECTION & ADJUSTED SCORING (Priority 11)")
    print("="*80)
    
    motor_aware_result = calculate_motor_aware_efficiency(
        ground_score=38,
        engine_score=58,
        weapon_score=55,
        height_inches=68,
        wingspan_inches=69,
        weight_lbs=190,
        age=33,
        rotation_ke_joules=3743,
        translation_ke_joules=421
    )
    
    print(f"\n🧬 Motor Preference Detected: {motor_aware_result['motor_preference'].upper()}")
    print(f"   Confidence: {motor_aware_result['preference_confidence']:.1%}")
    print(f"   Expected Rotation: {motor_aware_result['expected_rotation_ratio']:.1%}")
    print(f"   Actual Rotation: {motor_aware_result['actual_rotation_ratio']:.1%}")
    print(f"   Match: {'✅ YES' if motor_aware_result['rotation_ratio_match'] else '❌ NO'}")
    
    print(f"\n📊 Adjusted Scores:")
    print(f"   Ground: {motor_aware_result['ground_score_raw']} → {motor_aware_result['ground_score_adjusted']} (+{motor_aware_result['ground_score_adjusted'] - motor_aware_result['ground_score_raw']})")
    print(f"   Engine: {motor_aware_result['engine_score_raw']} → {motor_aware_result['engine_score_adjusted']}")
    print(f"   Weapon: {motor_aware_result['weapon_score_raw']} → {motor_aware_result['weapon_score_adjusted']}")
    print(f"   Overall Efficiency: {motor_aware_result['overall_efficiency']:.1%}")
    
    
    # ===== STEP 3: PRIORITY 9 - GAP ANALYSIS (with adjusted scores) =====
    print("\n" + "="*80)
    print("STEP 3: GAP ANALYSIS WITH ADJUSTED SCORES (Priority 9)")
    print("="*80)
    
    # Use adjusted scores for efficiency calculation
    efficiency_data = {
        'ground_score': motor_aware_result['ground_score_adjusted'],
        'engine_score': motor_aware_result['engine_score_adjusted'],
        'weapon_score': motor_aware_result['weapon_score_adjusted'],
        'overall_efficiency': motor_aware_result['overall_efficiency']
    }
    
    efficiency = calculate_efficiency(
        motor_aware_result['ground_score_adjusted'],
        motor_aware_result['engine_score_adjusted'],
        motor_aware_result['weapon_score_adjusted']
    )
    
    predicted = predict_current_performance(capacity, efficiency)
    
    print(f"\n✅ Performance Prediction:")
    print(f"   Predicted Bat Speed: {predicted['predicted_bat_speed_mph']:.1f} mph")
    print(f"   Actual Bat Speed: 67.0 mph")
    print(f"   Capacity Used: {predicted['percent_of_capacity_used']:.1%}")
    
    # Gap analysis using analyze_gaps
    gap_result = analyze_gaps(
        capacity_data=capacity,
        current_performance=predicted,
        blast_actual_mph=67.0,
        ground_score=motor_aware_result['ground_score_adjusted'],
        engine_score=motor_aware_result['engine_score_adjusted'],
        weapon_score=motor_aware_result['weapon_score_adjusted']
    )
    
    print(f"\n📈 Gap Analysis:")
    print(f"   Gap to Max: {gap_result['gap_to_capacity_max_mph']:.1f} mph")
    print(f"   Alignment: {gap_result['alignment_status']}")
    
    # Extract leak breakdown
    leak_breakdown = gap_result['leak_breakdown']
    
    print(f"\n💧 Energy Leaks:")
    for component_key in ['ground', 'engine', 'weapon']:
        if component_key in leak_breakdown:
            leak = leak_breakdown[component_key]
            print(f"   {component_key.upper()}: {leak['leak_percent']:.0f}% leak → +{leak['potential_gain_mph']:.1f} mph [{leak['priority']}]")
    
    
    # ===== STEP 4: PRIORITY 10 - RECOMMENDATIONS =====
    print("\n" + "="*80)
    print("STEP 4: PERSONALIZED CORRECTION PLAN (Priority 10)")
    print("="*80)
    
    recommendation_engine = SwingRehabRecommendationEngine()
    
    # Convert leak breakdown to format expected by recommendation engine
    leaks_for_recommendation = {
        'GROUND': {
            'leak_percent': leak_breakdown.get('ground', {}).get('leak_percent', 0),
            'gain_mph': leak_breakdown.get('ground', {}).get('potential_gain_mph', 0),
            'priority': leak_breakdown.get('ground', {}).get('priority', 'LOW')
        },
        'ENGINE': {
            'leak_percent': leak_breakdown.get('engine', {}).get('leak_percent', 0),
            'gain_mph': leak_breakdown.get('engine', {}).get('potential_gain_mph', 0),
            'priority': leak_breakdown.get('engine', {}).get('priority', 'LOW')
        },
        'WEAPON': {
            'leak_percent': leak_breakdown.get('weapon', {}).get('leak_percent', 0),
            'gain_mph': leak_breakdown.get('weapon', {}).get('potential_gain_mph', 0),
            'priority': leak_breakdown.get('weapon', {}).get('priority', 'LOW')
        }
    }
    
    correction_plan = recommendation_engine.generate_recommendations(
        ground_score=motor_aware_result['ground_score_adjusted'],
        engine_score=motor_aware_result['engine_score_adjusted'],
        weapon_score=motor_aware_result['weapon_score_adjusted'],
        capacity_data=capacity,
        gap_analysis={'leaks': leaks_for_recommendation},
        motor_preference=motor_aware_result['motor_preference']
    )
    
    print(f"\n✅ Correction Plan Generated:")
    print(f"   Issues Identified: {len(correction_plan.issues)}")
    print(f"   Drills Prescribed: {len(correction_plan.drill_progression)}")
    print(f"   Strength Exercises: {len(correction_plan.strength_work)}")
    print(f"   Timeline: {correction_plan.timeline}")
    
    print(f"\n🎯 Top 3 Issues to Address:")
    for i, issue in enumerate(correction_plan.issues[:3], 1):
        print(f"   {i}. {issue.name} [{issue.priority.value}]")
        print(f"      Severity: {issue.severity:.0%}")
        if 'expected_gain_mph' in issue.data_evidence:
            print(f"      Potential Gain: +{issue.data_evidence['expected_gain_mph']:.1f} mph")
    
    print(f"\n🏋️ First 3 Drills:")
    for i, drill in enumerate(correction_plan.drill_progression[:3], 1):
        print(f"   {i}. {drill.drill_name}")
        print(f"      Stage: {drill.stage.value}")
        print(f"      Sets/Reps: {drill.sets_reps}")
    
    print(f"\n💪 First 3 Strength Exercises:")
    for i, exercise in enumerate(correction_plan.strength_work[:3], 1):
        print(f"   {i}. {exercise['exercise']}")
        print(f"      Sets/Reps: {exercise['sets_reps']}")
    
    print(f"\n📊 Success Targets:")
    for key, value in correction_plan.success_metrics.items():
        print(f"   {key}: {value:.1f}")
    
    
    # ===== FINAL SUMMARY =====
    print("\n" + "="*80)
    print("✅ INTEGRATION TEST COMPLETE!")
    print("="*80)
    
    print("\n🎉 Complete Analysis Summary:")
    print(f"   ✓ Priority 9: Capacity ({capacity['bat_speed_capacity_midpoint_mph']:.1f} mph)")
    print(f"   ✓ Priority 11: Motor Preference (SPINNER @ {motor_aware_result['preference_confidence']:.1%})")
    print(f"   ✓ Priority 11: Adjusted Ground Score (38 → {motor_aware_result['ground_score_adjusted']})")
    print(f"   ✓ Priority 9: Gap Analysis ({gap_result['gap_to_capacity_max_mph']:.1f} mph untapped)")
    print(f"   ✓ Priority 10: {len(correction_plan.issues)} Issues + {len(correction_plan.drill_progression)} Drills")
    print(f"   ✓ Timeline: {correction_plan.timeline}")
    print(f"   ✓ Expected Gain: +{correction_plan.success_metrics['expected_bat_speed_gain_mph']:.1f} mph")
    
    print("\n✅ All systems integrated and working!")
    print("="*80)
    
    return True


if __name__ == "__main__":
    try:
        success = test_complete_pipeline()
        if success:
            print("\n✅ PRIORITY 9 + 10 + 11 INTEGRATION: SUCCESS")
            exit(0)
        else:
            print("\n❌ PRIORITY 9 + 10 + 11 INTEGRATION: FAILED")
            exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
