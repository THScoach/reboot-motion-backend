"""
PRIORITY 12: API ENHANCEMENT
Adds Priority 10 (Recommendation Engine) + Priority 11 (BioSwing Motor Preference)
to the existing /analyze endpoint
"""

import sys
from pathlib import Path

# Add physics_engine to path
sys.path.insert(0, str(Path(__file__).parent / "physics_engine"))

from kinetic_capacity_calculator import calculate_energy_capacity
from efficiency_analyzer import calculate_efficiency, predict_current_performance
from gap_analyzer import analyze_gaps
from motor_aware_efficiency_analyzer import calculate_motor_aware_efficiency
from swing_rehab_recommendation_engine import SwingRehabRecommendationEngine


def enhance_analysis_with_priority_10_11(
    # Existing analysis data
    ground_score: int,
    engine_score: int,
    weapon_score: int,
    
    # Athlete data
    height_inches: float,
    wingspan_inches: float,
    weight_lbs: float,
    age: int,
    bat_weight_oz: int = 30,
    
    # Optional actual bat speed from sensor
    actual_bat_speed_mph: float = None,
    
    # Optional energy data from video analysis
    rotation_ke_joules: float = None,
    translation_ke_joules: float = None
):
    """
    Enhance existing analysis with Priority 10 + 11 features
    
    Returns complete analysis dict with:
    - Motor preference detection (Priority 11)
    - Adjusted scores (Priority 11)
    - Kinetic capacity (Priority 9)
    - Gap analysis (Priority 9)
    - Personalized recommendations (Priority 10)
    """
    
    # ===== STEP 1: KINETIC CAPACITY (Priority 9) =====
    capacity = calculate_energy_capacity(
        height_inches=height_inches,
        wingspan_inches=wingspan_inches or height_inches,  # Default to height if not provided
        weight_lbs=weight_lbs,
        age=age,
        bat_weight_oz=bat_weight_oz
    )
    
    
    # ===== STEP 2: MOTOR PREFERENCE DETECTION (Priority 11) =====
    motor_aware_result = calculate_motor_aware_efficiency(
        ground_score=ground_score,
        engine_score=engine_score,
        weapon_score=weapon_score,
        height_inches=height_inches,
        wingspan_inches=wingspan_inches or height_inches,
        weight_lbs=weight_lbs,
        age=age,
        rotation_ke_joules=rotation_ke_joules,
        translation_ke_joules=translation_ke_joules
    )
    
    
    # ===== STEP 3: ADJUSTED EFFICIENCY & PERFORMANCE (Priority 9 + 11) =====
    efficiency = calculate_efficiency(
        motor_aware_result['ground_score_adjusted'],
        motor_aware_result['engine_score_adjusted'],
        motor_aware_result['weapon_score_adjusted']
    )
    
    predicted = predict_current_performance(capacity, efficiency)
    
    
    # ===== STEP 4: GAP ANALYSIS (Priority 9) =====
    gap_result = analyze_gaps(
        capacity_data=capacity,
        current_performance=predicted,
        blast_actual_mph=actual_bat_speed_mph,
        ground_score=motor_aware_result['ground_score_adjusted'],
        engine_score=motor_aware_result['engine_score_adjusted'],
        weapon_score=motor_aware_result['weapon_score_adjusted']
    )
    
    
    # ===== STEP 5: GENERATE RECOMMENDATIONS (Priority 10) =====
    recommendation_engine = SwingRehabRecommendationEngine()
    
    leak_breakdown = gap_result['leak_breakdown']
    
    # Convert leak format for recommendation engine
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
    
    
    # ===== STEP 6: BUILD ENHANCED RESPONSE =====
    return {
        # Priority 9: Kinetic Capacity
        'capacity': {
            'bat_speed_range': {
                'min_mph': capacity['bat_speed_capacity_min_mph'],
                'max_mph': capacity['bat_speed_capacity_max_mph'],
                'midpoint_mph': capacity['bat_speed_capacity_midpoint_mph']
            },
            'exit_velo_range': {
                'min_mph': capacity['exit_velo_capacity_min_mph'],
                'max_mph': capacity['exit_velo_capacity_max_mph']
            },
            'wingspan_advantage_mph': capacity.get('wingspan_advantage_mph', 0),
            'wingspan_advantage_pct': capacity.get('wingspan_advantage_percent', 0)
        },
        
        # Priority 11: Motor Preference
        'motor_preference': {
            'preference': motor_aware_result['motor_preference'],
            'post_bias': motor_aware_result['post_bias'],
            'primary_force': motor_aware_result['primary_force'],
            'confidence': motor_aware_result['preference_confidence'],
            'expected_rotation_ratio': motor_aware_result['expected_rotation_ratio'],
            'actual_rotation_ratio': motor_aware_result.get('actual_rotation_ratio'),
            'rotation_ratio_match': motor_aware_result.get('rotation_ratio_match'),
            'description': motor_aware_result['description'],
            'coaching_focus': motor_aware_result['coaching_focus'],
            'avoid_coaching': motor_aware_result['avoid_coaching']
        },
        
        # Priority 11: Adjusted Scores
        'scores_adjusted': {
            'ground': {
                'raw': motor_aware_result['ground_score_raw'],
                'adjusted': motor_aware_result['ground_score_adjusted'],
                'adjustment': motor_aware_result['ground_score_adjusted'] - motor_aware_result['ground_score_raw']
            },
            'engine': {
                'raw': motor_aware_result['engine_score_raw'],
                'adjusted': motor_aware_result['engine_score_adjusted'],
                'adjustment': motor_aware_result['engine_score_adjusted'] - motor_aware_result['engine_score_raw']
            },
            'weapon': {
                'raw': motor_aware_result['weapon_score_raw'],
                'adjusted': motor_aware_result['weapon_score_adjusted'],
                'adjustment': motor_aware_result['weapon_score_adjusted'] - motor_aware_result['weapon_score_raw']
            },
            'overall_efficiency': motor_aware_result['overall_efficiency']
        },
        
        # Priority 9: Performance & Gap Analysis
        'performance': {
            'predicted_bat_speed_mph': predicted['predicted_bat_speed_mph'],
            'predicted_exit_velo_mph': predicted['predicted_exit_velo_mph'],
            'actual_bat_speed_mph': actual_bat_speed_mph,
            'gap_to_capacity_max_mph': gap_result['gap_to_capacity_max_mph'],
            'alignment_status': gap_result['alignment_status'],
            'percent_capacity_used': gap_result.get('percent_capacity_used_actual') or gap_result.get('percent_capacity_used_predicted')
        },
        
        # Priority 9: Energy Leaks
        'energy_leaks': {
            'ground': {
                'leak_percent': leak_breakdown.get('ground', {}).get('leak_percent', 0),
                'potential_gain_mph': leak_breakdown.get('ground', {}).get('potential_gain_mph', 0),
                'priority': leak_breakdown.get('ground', {}).get('priority', 'LOW')
            },
            'engine': {
                'leak_percent': leak_breakdown.get('engine', {}).get('leak_percent', 0),
                'potential_gain_mph': leak_breakdown.get('engine', {}).get('potential_gain_mph', 0),
                'priority': leak_breakdown.get('engine', {}).get('priority', 'LOW')
            },
            'weapon': {
                'leak_percent': leak_breakdown.get('weapon', {}).get('leak_percent', 0),
                'potential_gain_mph': leak_breakdown.get('weapon', {}).get('potential_gain_mph', 0),
                'priority': leak_breakdown.get('weapon', {}).get('priority', 'LOW')
            },
            'prescription': gap_result.get('prescription', '')
        },
        
        # Priority 10: Correction Plan
        'correction_plan': {
            'issues': [
                {
                    'name': issue.name,
                    'category': issue.category.value,
                    'severity': issue.severity,
                    'priority': issue.priority.value,
                    'root_cause': issue.root_cause,
                    'potential_gain_mph': issue.data_evidence.get('expected_gain_mph', 0)
                }
                for issue in correction_plan.issues
            ],
            'drills': [
                {
                    'drill_id': drill.drill_id,
                    'drill_name': drill.drill_name,
                    'stage': drill.stage.value,
                    'description': drill.description,
                    'how_it_works': drill.how_it_works,
                    'sets_reps': drill.sets_reps,
                    'coaching_cues': drill.coaching_cues,
                    'equipment': drill.equipment_needed,
                    'integration_with_tools': drill.integration_with_tools,
                    'expected_outcome': drill.expected_outcome,
                    'addresses': [cat.value for cat in drill.addresses]
                }
                for drill in correction_plan.drill_progression
            ],
            'strength_work': correction_plan.strength_work,
            'timeline': correction_plan.timeline,
            'success_metrics': correction_plan.success_metrics,
            'motor_preference_notes': correction_plan.motor_preference_notes
        }
    }


# Test function
if __name__ == "__main__":
    # Test with Eric Williams data
    result = enhance_analysis_with_priority_10_11(
        ground_score=38,
        engine_score=58,
        weapon_score=55,
        height_inches=68,
        wingspan_inches=69,
        weight_lbs=190,
        age=33,
        bat_weight_oz=30,
        actual_bat_speed_mph=67.0,
        rotation_ke_joules=3743,
        translation_ke_joules=421
    )
    
    print("=" * 80)
    print("PRIORITY 12 API ENHANCEMENT TEST")
    print("=" * 80)
    
    print(f"\n🧬 Motor Preference: {result['motor_preference']['preference'].upper()}")
    print(f"   Confidence: {result['motor_preference']['confidence']:.1%}")
    
    print(f"\n📊 Scores (Raw → Adjusted):")
    print(f"   Ground: {result['scores_adjusted']['ground']['raw']} → {result['scores_adjusted']['ground']['adjusted']} ({result['scores_adjusted']['ground']['adjustment']:+d})")
    print(f"   Engine: {result['scores_adjusted']['engine']['raw']} → {result['scores_adjusted']['engine']['adjusted']}")
    print(f"   Weapon: {result['scores_adjusted']['weapon']['raw']} → {result['scores_adjusted']['weapon']['adjusted']}")
    
    print(f"\n🎯 Correction Plan:")
    print(f"   Issues: {len(result['correction_plan']['issues'])}")
    print(f"   Drills: {len(result['correction_plan']['drills'])}")
    print(f"   Timeline: {result['correction_plan']['timeline']}")
    
    print("\n✅ API Enhancement Working!")
