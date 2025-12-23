"""
MOTOR-PREFERENCE-AWARE EFFICIENCY ANALYZER
Integrates BioSwing Dynamics preference detection with efficiency scoring

Instead of generic scoring, this scores athletes based on how well they
EXECUTE their body's optimal force pattern (SPINNER/GLIDER/LAUNCHER).
"""

from typing import Dict, Optional
from bioswing_preference_detector import BioSwingPreferenceDetector, ForcePreference


def calculate_motor_aware_efficiency(
    ground_score: int,
    engine_score: int,
    weapon_score: int,
    height_inches: float,
    wingspan_inches: float,
    weight_lbs: float,
    age: int,
    rotation_ke_joules: Optional[float] = None,
    translation_ke_joules: Optional[float] = None
) -> Dict:
    """
    Calculate efficiency scores adjusted for motor preference
    
    Args:
        ground_score: Raw ground score (0-100)
        engine_score: Raw engine score (0-100)
        weapon_score: Raw weapon score (0-100)
        height_inches: Height
        wingspan_inches: Wingspan
        weight_lbs: Weight
        age: Age
        rotation_ke_joules: Optional rotational kinetic energy
        translation_ke_joules: Optional translational kinetic energy
        
    Returns:
        Dict with adjusted scores and preference information
    """
    
    # Detect motor preference
    detector = BioSwingPreferenceDetector()
    preference_profile = detector.determine_preference(
        height_inches=height_inches,
        wingspan_inches=wingspan_inches,
        weight_lbs=weight_lbs,
        age=age
    )
    
    # Calculate actual rotation ratio (if energy data available)
    actual_rotation_ratio = None
    rotation_ratio_match = None
    
    if rotation_ke_joules is not None and translation_ke_joules is not None:
        total_ke = rotation_ke_joules + translation_ke_joules
        if total_ke > 0:
            actual_rotation_ratio = rotation_ke_joules / total_ke
            expected_ratio = preference_profile.expected_rotation_ratio
            rotation_ratio_match = abs(actual_rotation_ratio - expected_ratio) < 0.10
    
    
    # ADJUST GROUND SCORE BASED ON PREFERENCE
    adjusted_ground_score = adjust_ground_score_for_preference(
        ground_score,
        preference_profile,
        actual_rotation_ratio
    )
    
    # ADJUST ENGINE SCORE BASED ON PREFERENCE  
    adjusted_engine_score = adjust_engine_score_for_preference(
        engine_score,
        preference_profile
    )
    
    # Weapon score is generally preference-neutral
    adjusted_weapon_score = weapon_score
    
    
    # Calculate efficiencies
    ground_efficiency = adjusted_ground_score / 100.0
    engine_efficiency = adjusted_engine_score / 100.0
    weapon_efficiency = adjusted_weapon_score / 100.0
    
    # Overall efficiency (weighted)
    overall_efficiency = (
        ground_efficiency * 0.25 +
        engine_efficiency * 0.50 +
        weapon_efficiency * 0.25
    )
    
    return {
        # Original scores
        'ground_score_raw': ground_score,
        'engine_score_raw': engine_score,
        'weapon_score_raw': weapon_score,
        
        # Adjusted scores
        'ground_score_adjusted': adjusted_ground_score,
        'engine_score_adjusted': adjusted_engine_score,
        'weapon_score_adjusted': adjusted_weapon_score,
        
        # Efficiencies
        'ground_efficiency': ground_efficiency,
        'engine_efficiency': engine_efficiency,
        'weapon_efficiency': weapon_efficiency,
        'overall_efficiency': overall_efficiency,
        
        # Preference information
        'motor_preference': preference_profile.preference.value,
        'post_bias': preference_profile.post_bias.value,
        'primary_force': preference_profile.primary_force,
        'preference_confidence': preference_profile.confidence,
        'expected_rotation_ratio': preference_profile.expected_rotation_ratio,
        'actual_rotation_ratio': actual_rotation_ratio,
        'rotation_ratio_match': rotation_ratio_match,
        
        # Coaching insights
        'coaching_focus': preference_profile.coaching_focus,
        'avoid_coaching': preference_profile.avoid_coaching,
        'description': preference_profile.description
    }


def adjust_ground_score_for_preference(
    raw_ground_score: int,
    preference_profile,
    actual_rotation_ratio: Optional[float]
) -> int:
    """
    Adjust ground score based on motor preference
    
    Key insight: If athlete is executing their PREFERRED pattern,
    boost the score. If fighting their preference, don't penalize.
    """
    
    adjusted_score = raw_ground_score
    
    if preference_profile.preference == ForcePreference.SPINNER:
        # SPINNERS: Reward rotational execution, don't penalize lack of translation
        
        # If we have energy data, check rotation ratio match
        if actual_rotation_ratio is not None:
            expected = preference_profile.expected_rotation_ratio
            
            if actual_rotation_ratio >= expected:
                # Executing spinner pattern WELL or EXCELLENTLY - REWARD SIGNIFICANTLY
                
                # Base boost: They're a spinner executing spinner mechanics
                base_boost = 25  # Spinner doing spinner things gets 25 points
                
                # Bonus for exceeding expected
                excellence_bonus = (actual_rotation_ratio - expected) * 200  # Scale up
                
                # Total boost
                total_boost = base_boost + excellence_bonus
                adjusted_score = min(100, raw_ground_score + total_boost)
                
            elif actual_rotation_ratio < 0.70:
                # Too much translation for a spinner - might be fighting preference
                # But don't penalize too harshly - might be learning
                adjusted_score = raw_ground_score  # Keep raw score
        
        else:
            # No energy data - use heuristic
            # If ground score is low, it might be because they're being
            # penalized for not moving forward (spinner trait)
            # Give significant boost if very low
            if raw_ground_score < 50:
                adjusted_score = min(75, raw_ground_score + 25)  # Significant boost
            elif raw_ground_score < 70:
                adjusted_score = min(85, raw_ground_score + 15)  # Moderate boost
    
    elif preference_profile.preference == ForcePreference.GLIDER:
        # GLIDERS: Reward lateral movement, don't penalize lack of rotation
        
        if actual_rotation_ratio is not None:
            expected = preference_profile.expected_rotation_ratio
            
            if actual_rotation_ratio <= expected:
                # Executing glider pattern well (more translation) - REWARD
                boost = min(20, (expected - actual_rotation_ratio) * 100)
                adjusted_score = min(100, raw_ground_score + boost)
            elif actual_rotation_ratio > 0.80:
                # Too much rotation for a glider - might be fighting preference
                pass  # Keep raw score
        
        else:
            # No energy data - use heuristic
            # Gliders might be penalized for not staying centered
            # Give modest boost if low
            if raw_ground_score < 50:
                adjusted_score = raw_ground_score + 10  # Modest boost
    
    elif preference_profile.preference == ForcePreference.LAUNCHER:
        # LAUNCHERS: Reward vertical execution
        # Hard to detect without force plate data
        # Use conservative adjustment
        if raw_ground_score < 50:
            adjusted_score = raw_ground_score + 10
    
    return int(adjusted_score)


def adjust_engine_score_for_preference(
    raw_engine_score: int,
    preference_profile
) -> int:
    """
    Adjust engine score based on motor preference
    
    Engine (kinetic chain) execution varies by preference:
    - Spinners: Hip-shoulder separation critical
    - Gliders: Weight shift timing critical
    - Launchers: Vertical timing critical
    """
    
    # Engine adjustments are generally smaller than ground
    # because kinetic chain principles are more universal
    
    adjusted_score = raw_engine_score
    
    if preference_profile.preference == ForcePreference.SPINNER:
        # Spinners with good engine should score high on separation
        # If engine score is moderate, might be separation issue
        # (common for spinners to spin hips+chest together)
        pass  # Keep raw score for now
    
    elif preference_profile.preference == ForcePreference.GLIDER:
        # Gliders with good engine should score high on timing
        # If engine score is moderate, might be timing issue
        pass  # Keep raw score for now
    
    return int(adjusted_score)


# ===== TESTING =====
if __name__ == "__main__":
    print("=" * 80)
    print("MOTOR-AWARE EFFICIENCY TEST - ERIC WILLIAMS")
    print("=" * 80)
    
    # Eric's data
    result = calculate_motor_aware_efficiency(
        ground_score=38,  # Original "bad" score
        engine_score=58,
        weapon_score=55,
        height_inches=68,
        wingspan_inches=69,
        weight_lbs=190,
        age=33,
        rotation_ke_joules=3743,  # From RebootMotion
        translation_ke_joules=421  # From RebootMotion
    )
    
    print(f"\n📊 MOTOR PREFERENCE:")
    print(f"   Preference: {result['motor_preference'].upper()}")
    print(f"   Post Bias: {result['post_bias']}")
    print(f"   Primary Force: {result['primary_force']}")
    print(f"   Confidence: {result['preference_confidence']:.1%}")
    
    print(f"\n🔄 ROTATION ANALYSIS:")
    print(f"   Expected Rotation Ratio: {result['expected_rotation_ratio']:.1%}")
    print(f"   Actual Rotation Ratio: {result['actual_rotation_ratio']:.1%}")
    print(f"   Match: {'✅ YES' if result['rotation_ratio_match'] else '❌ NO'}")
    
    print(f"\n📈 SCORES (RAW → ADJUSTED):")
    print(f"   Ground: {result['ground_score_raw']} → {result['ground_score_adjusted']} (+{result['ground_score_adjusted'] - result['ground_score_raw']})")
    print(f"   Engine: {result['engine_score_raw']} → {result['engine_score_adjusted']} (+{result['engine_score_adjusted'] - result['engine_score_raw']})")
    print(f"   Weapon: {result['weapon_score_raw']} → {result['weapon_score_adjusted']} (+{result['weapon_score_adjusted'] - result['weapon_score_raw']})")
    
    print(f"\n✅ EFFICIENCIES:")
    print(f"   Ground: {result['ground_efficiency']:.1%}")
    print(f"   Engine: {result['engine_efficiency']:.1%}")
    print(f"   Weapon: {result['weapon_efficiency']:.1%}")
    print(f"   Overall: {result['overall_efficiency']:.1%}")
    
    print(f"\n🎯 COACHING:")
    print(f"   FOCUS: {result['coaching_focus']}")
    print(f"   AVOID: {result['avoid_coaching']}")
    
    print("\n" + "=" * 80)
