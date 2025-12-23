"""
BIOSWING DYNAMICS PREFERENCE DETECTOR
Based on Mike Adams/Terry Rowles force plate research

Determines optimal force preference (SPINNER/GLIDER/LAUNCHER) from body structure
and adjusts scoring to reward athletes for executing THEIR pattern well.

Research Foundation:
- BioSwing Dynamics structural screens
- Force plate COP/COM trace analysis
- Wingspan-to-height ratios predict force patterns
- Arm length ratios predict connection vs arc patterns
"""

from typing import Dict, Optional
from dataclasses import dataclass
from enum import Enum


class ForcePreference(Enum):
    """BioSwing force preference types"""
    SPINNER = "spinner"      # Center-post, rotational torque
    GLIDER = "glider"        # Rear-post, horizontal frontal
    LAUNCHER = "launcher"    # Front-post, vertical
    BALANCED = "balanced"    # No strong structural bias


class PostBias(Enum):
    """Post bias during swing"""
    CENTER_POST = "center-post"
    REAR_POST = "rear-post"
    FRONT_POST = "front-post"
    MIXED = "mixed"


@dataclass
class ForcePreferenceProfile:
    """Complete force preference profile based on body structure"""
    preference: ForcePreference
    post_bias: PostBias
    primary_force: str
    description: str
    
    # Expected biomechanical signatures
    expected_cop_pattern: str
    expected_com_pattern: str
    expected_grf_peak: str
    expected_rotation_ratio: float  # % of energy from rotation vs translation
    
    # Coaching guidance
    coaching_focus: str
    avoid_coaching: str
    
    # Scoring adjustments
    ground_score_weights: Dict[str, float]
    engine_score_weights: Dict[str, float]
    
    # Supporting data
    structural_indicators: Dict[str, any]
    confidence: float


class BioSwingPreferenceDetector:
    """
    Detects optimal force preference from body structure using BioSwing Dynamics principles
    """
    
    def __init__(self):
        """Initialize detector"""
        pass
    
    def determine_preference(
        self,
        height_inches: float,
        wingspan_inches: float,
        weight_lbs: float,
        age: int,
        upper_arm_length_inches: Optional[float] = None,
        forearm_length_inches: Optional[float] = None
    ) -> ForcePreferenceProfile:
        """
        Determine force preference from structural screens
        
        Args:
            height_inches: Height in inches
            wingspan_inches: Wingspan in inches
            weight_lbs: Body weight in pounds
            age: Age in years
            upper_arm_length_inches: Optional upper arm length
            forearm_length_inches: Optional forearm length
            
        Returns:
            ForcePreferenceProfile with complete preference assessment
        """
        
        # SCREEN 1: WINGSPAN VS HEIGHT (Primary)
        ape_index = wingspan_inches - height_inches
        
        # SCREEN 2: BODY COMPOSITION
        bmi = (weight_lbs / (height_inches ** 2)) * 703
        stocky = bmi > 26  # More muscular/compact build
        lean = bmi < 24    # Leaner, easier to translate
        
        # SCREEN 3: ARM RATIO (if available)
        arm_connection_score = 0
        arm_ratio = None
        if upper_arm_length_inches and forearm_length_inches:
            arm_ratio = upper_arm_length_inches / forearm_length_inches
            if arm_ratio > 1.0:  # Upper arm longer = hands closer, more connected
                arm_connection_score = 2
            elif arm_ratio < 0.95:  # Forearm longer = hands farther, more arc
                arm_connection_score = -2
        
        # SCREEN 4: AGE FACTOR
        # Older athletes have established patterns, harder to change
        age_factor = 1.0 if age < 25 else 0.8 if age < 35 else 0.6
        
        
        # =================================================================
        # CLASSIFICATION LOGIC (BioSwing Framework)
        # =================================================================
        
        # Count indicators for each preference
        spinner_indicators = 0
        glider_indicators = 0
        launcher_indicators = 0
        
        # SPINNER INDICATORS (Center-Post, Rotational)
        if -1 <= ape_index <= 2:  # Wingspan ≈ Height
            spinner_indicators += 3
        if stocky:  # Heavier/more muscular
            spinner_indicators += 2
        if arm_connection_score > 0:  # Shorter arms, more connected
            spinner_indicators += 2
        if height_inches < 70:  # Shorter stature
            spinner_indicators += 1
        
        # GLIDER INDICATORS (Rear-Post, Horizontal)
        if ape_index > 2:  # Wingspan > Height (longer arms)
            glider_indicators += 3
        if lean:  # Leaner build
            glider_indicators += 2
        if arm_connection_score < 0:  # Longer forearms, more arc
            glider_indicators += 2
        if height_inches > 72:  # Taller stature
            glider_indicators += 1
        
        # LAUNCHER INDICATORS (Front-Post, Vertical)
        if ape_index < -1:  # Wingspan < Height (shorter arms)
            launcher_indicators += 3
        if stocky:  # More mass to drive vertically
            launcher_indicators += 1
        if height_inches < 68:  # Shorter stature
            launcher_indicators += 1
        
        
        # Determine primary preference
        max_indicators = max(spinner_indicators, glider_indicators, launcher_indicators)
        
        # Calculate confidence (0-1)
        total_indicators = spinner_indicators + glider_indicators + launcher_indicators
        confidence = max_indicators / total_indicators if total_indicators > 0 else 0.5
        
        
        # =================================================================
        # BUILD PREFERENCE PROFILE
        # =================================================================
        
        if spinner_indicators >= max_indicators and spinner_indicators > 3:
            return self._build_spinner_profile(
                ape_index, bmi, arm_ratio, age, confidence,
                {'ape_index': ape_index, 'bmi': bmi, 'arm_ratio': arm_ratio,
                 'spinner_score': spinner_indicators}
            )
        
        elif glider_indicators >= max_indicators and glider_indicators > 3:
            return self._build_glider_profile(
                ape_index, bmi, arm_ratio, age, confidence,
                {'ape_index': ape_index, 'bmi': bmi, 'arm_ratio': arm_ratio,
                 'glider_score': glider_indicators}
            )
        
        elif launcher_indicators >= max_indicators and launcher_indicators > 3:
            return self._build_launcher_profile(
                ape_index, bmi, arm_ratio, age, confidence,
                {'ape_index': ape_index, 'bmi': bmi, 'arm_ratio': arm_ratio,
                 'launcher_score': launcher_indicators}
            )
        
        else:
            return self._build_balanced_profile(
                ape_index, bmi, arm_ratio, age, confidence,
                {'ape_index': ape_index, 'bmi': bmi, 'arm_ratio': arm_ratio,
                 'all_scores': (spinner_indicators, glider_indicators, launcher_indicators)}
            )
    
    
    def _build_spinner_profile(
        self, ape_index, bmi, arm_ratio, age, confidence, indicators
    ) -> ForcePreferenceProfile:
        """Build profile for SPINNER (center-post, rotational torque)"""
        
        return ForcePreferenceProfile(
            preference=ForcePreference.SPINNER,
            post_bias=PostBias.CENTER_POST,
            primary_force="rotational_torque",
            description="Short-lever, torso-connected athlete. Rotates hard over stable base with minimal lateral drift.",
            
            # Expected biomechanical signatures
            expected_cop_pattern="COP stays centered between feet with small lateral excursions. Trail-to-lead shift happens but inside the feet.",
            expected_com_pattern="COM 'turns in a barrel' - modest down-up, modest lateral, high rotation over stable base.",
            expected_grf_peak="Rotational torque peak is dominant, typically mid-downswing (P4→P5). Horizontal and vertical present but secondary.",
            expected_rotation_ratio=0.85,  # 85% rotational, 15% translational
            
            # Coaching guidance
            coaching_focus="Preserve connection and rotation. Focus on: (1) Back-leg stability as rotation axis, (2) Deep back-hip coil before spin, (3) Rotational power, (4) Connected arm action (hands close to body).",
            avoid_coaching="DON'T force big lateral drift, forward weight shift, or front-leg drive. These fight the spinner's natural pattern and reduce efficiency.",
            
            # Scoring adjustments
            ground_score_weights={
                'rotational_execution': 0.30,    # Is torque peak dominant?
                'back_leg_stability': 0.30,      # Stable post for rotation?
                'load_depth': 0.30,              # Deep coil before spin?
                'front_foot_timing': 0.10        # Less critical for spinners
            },
            engine_score_weights={
                'hip_shoulder_separation': 0.40,  # Critical for spinners
                'rotational_sequence': 0.30,      # Hip-chest timing
                'connection_quality': 0.20,       # Arms stay connected
                'tempo': 0.10
            },
            
            # Supporting data
            structural_indicators=indicators,
            confidence=confidence
        )
    
    
    def _build_glider_profile(
        self, ape_index, bmi, arm_ratio, age, confidence, indicators
    ) -> ForcePreferenceProfile:
        """Build profile for GLIDER (rear-post, horizontal frontal force)"""
        
        return ForcePreferenceProfile(
            preference=ForcePreference.GLIDER,
            post_bias=PostBias.REAR_POST,
            primary_force="horizontal_frontal",
            description="Long-lever athlete. Uses lateral motion and trail-to-lead weight shift. More 'reach and drift' than pure rotation.",
            
            # Expected biomechanical signatures
            expected_cop_pattern="COP shows big lateral excursion from trail to lead foot. Clear trail-to-lead shift pattern.",
            expected_com_pattern="COM moves side-to-side as primary motion. Lateral displacement more pronounced than vertical or rotational.",
            expected_grf_peak="Horizontal/frontal force peak is dominant. Torque present but secondary to lateral drive.",
            expected_rotation_ratio=0.60,  # 60% rotational, 40% translational
            
            # Coaching guidance
            coaching_focus="Allow and enhance lateral drift. Focus on: (1) Trail-leg deep load with lateral push, (2) Forward weight shift timing, (3) Lead-leg stable post to receive momentum, (4) Extended reach through ball.",
            avoid_coaching="DON'T force tight rotation or keep weight centered. Gliders NEED lateral movement - fighting it reduces their natural power source.",
            
            # Scoring adjustments
            ground_score_weights={
                'horizontal_execution': 0.35,    # Is horizontal GRF peak?
                'lateral_cop_shift': 0.25,       # Big trail→lead movement?
                'trail_leg_load': 0.25,          # Deep load before drift?
                'lead_leg_stability': 0.15       # Stable post to receive?
            },
            engine_score_weights={
                'weight_shift_timing': 0.35,     # Critical for gliders
                'lateral_sequence': 0.25,        # Trail→lead coordination
                'rotational_blend': 0.25,        # Still need some rotation
                'tempo': 0.15
            },
            
            # Supporting data
            structural_indicators=indicators,
            confidence=confidence
        )
    
    
    def _build_launcher_profile(
        self, ape_index, bmi, arm_ratio, age, confidence, indicators
    ) -> ForcePreferenceProfile:
        """Build profile for LAUNCHER (front-post, vertical force)"""
        
        return ForcePreferenceProfile(
            preference=ForcePreference.LAUNCHER,
            post_bias=PostBias.FRONT_POST,
            primary_force="vertical",
            description="Compact, powerful athlete. Uses vertical ground forces with front-leg pivot. Down-then-up motion pattern.",
            
            # Expected biomechanical signatures
            expected_cop_pattern="COP forward-biased. Clear vertical component with front-foot pressure emphasis.",
            expected_com_pattern="COM shows pronounced down-then-up pattern. Front-leg serves as pivot point for vertical drive.",
            expected_grf_peak="Vertical force peak is dominant. Front leg generates explosive upward drive.",
            expected_rotation_ratio=0.70,  # 70% rotational, 30% translational (mix)
            
            # Coaching guidance
            coaching_focus="Leverage vertical ground forces. Focus on: (1) Front-leg stability and explosive drive, (2) Down-load before up-drive, (3) Vertical power generation, (4) Front-post pivot mechanics.",
            avoid_coaching="DON'T force big lateral drift or pure rear-leg rotation. Launchers are front-leg dominant - use their vertical power.",
            
            # Scoring adjustments
            ground_score_weights={
                'vertical_execution': 0.35,      # Is vertical GRF peak?
                'front_leg_stability': 0.30,     # Strong front-post?
                'down_up_pattern': 0.20,         # COM drops then rises?
                'load_quality': 0.15             # Initial load before drive?
            },
            engine_score_weights={
                'vertical_timing': 0.35,         # Down→up timing critical
                'front_leg_drive': 0.30,         # Explosive push-up
                'rotational_blend': 0.20,        # Still need rotation
                'tempo': 0.15
            },
            
            # Supporting data
            structural_indicators=indicators,
            confidence=confidence
        )
    
    
    def _build_balanced_profile(
        self, ape_index, bmi, arm_ratio, age, confidence, indicators
    ) -> ForcePreferenceProfile:
        """Build profile for BALANCED (no strong structural bias)"""
        
        return ForcePreferenceProfile(
            preference=ForcePreference.BALANCED,
            post_bias=PostBias.MIXED,
            primary_force="mixed",
            description="No strong structural bias. Can adapt multiple force patterns based on training and preference.",
            
            # Expected biomechanical signatures
            expected_cop_pattern="Variable based on learned pattern. Could be centered, lateral, or forward-biased.",
            expected_com_pattern="Moderate in all directions - no dominant movement signature.",
            expected_grf_peak="Balanced horizontal/torque/vertical. No clear dominant force type.",
            expected_rotation_ratio=0.70,  # 70% rotational, 30% translational (neutral)
            
            # Coaching guidance
            coaching_focus="Build to athlete's strength or situational needs. Can develop as spinner, glider, or launcher based on training emphasis.",
            avoid_coaching="No specific patterns to avoid - balanced structure allows flexibility. Watch for athlete's natural tendencies and build those.",
            
            # Scoring adjustments
            ground_score_weights={
                'overall_force_quality': 0.40,
                'balance': 0.30,
                'adaptability': 0.30
            },
            engine_score_weights={
                'general_sequence': 0.40,
                'coordination': 0.30,
                'tempo': 0.30
            },
            
            # Supporting data
            structural_indicators=indicators,
            confidence=confidence
        )


# ===== USAGE EXAMPLE =====
if __name__ == "__main__":
    # Test with Eric Williams
    detector = BioSwingPreferenceDetector()
    
    profile = detector.determine_preference(
        height_inches=68,      # 5'8"
        wingspan_inches=69,    # 5'9" (ape +1")
        weight_lbs=190,
        age=33
    )
    
    print("=" * 80)
    print("BIOSWING PREFERENCE DETECTION - ERIC WILLIAMS")
    print("=" * 80)
    print(f"\n🧬 PREFERENCE: {profile.preference.value.upper()}")
    print(f"📍 POST BIAS: {profile.post_bias.value}")
    print(f"⚡ PRIMARY FORCE: {profile.primary_force}")
    print(f"📊 CONFIDENCE: {profile.confidence:.1%}")
    
    print(f"\n📝 DESCRIPTION:")
    print(f"   {profile.description}")
    
    print(f"\n🎯 EXPECTED BIOMECHANICS:")
    print(f"   COP Pattern: {profile.expected_cop_pattern}")
    print(f"   COM Pattern: {profile.expected_com_pattern}")
    print(f"   GRF Peak: {profile.expected_grf_peak}")
    print(f"   Rotation Ratio: {profile.expected_rotation_ratio:.0%} rotational")
    
    print(f"\n✅ COACHING FOCUS:")
    print(f"   {profile.coaching_focus}")
    
    print(f"\n❌ AVOID:")
    print(f"   {profile.avoid_coaching}")
    
    print(f"\n⚖️ GROUND SCORE WEIGHTS:")
    for component, weight in profile.ground_score_weights.items():
        print(f"   • {component}: {weight:.0%}")
    
    print(f"\n⚖️ ENGINE SCORE WEIGHTS:")
    for component, weight in profile.engine_score_weights.items():
        print(f"   • {component}: {weight:.0%}")
    
    print("\n" + "=" * 80)
