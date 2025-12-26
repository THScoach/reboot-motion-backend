"""
Enhanced Motor Profile Classification Module
Classifies swing mechanics into motor profiles with confidence scoring

Part of Priority 4: Motor Profile Classification Refinement
"""

from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class MotorProfileClassifier:
    """
    Enhanced motor profile classification with confidence scoring
    
    Profiles:
    - TITAN: Elite across all components (G/E/W all >80)
    - SPINNER: High rotation, low transfer (G>75, E>75, W<60)
    - SLINGSHOTTER: Good body, poor hands (G>75, W<60)
    - WHIPPER: All hands, no body (G<60, W>75)
    - BALANCED: Mixed scores, no clear pattern
    """
    
    # Profile definitions with scoring rules
    PROFILE_RULES = {
        'TITAN': {
            'description': 'Elite mechanics across all components',
            'conditions': {
                'ground_min': 80,
                'engine_min': 80,
                'weapon_min': 80
            },
            'weight': 1.0
        },
        'SPINNER': {
            'description': 'High rotation mechanics with lower transfer efficiency',
            'conditions': {
                'ground_min': 70,
                'engine_min': 70,
                'weapon_max': 65
            },
            'weight': 1.0
        },
        'SLINGSHOTTER': {
            'description': 'Good lower body and core rotation, poor bat control',
            'conditions': {
                'ground_min': 70,
                'engine_range': (60, 85),
                'weapon_max': 65
            },
            'weight': 1.0
        },
        'WHIPPER': {
            'description': 'Upper body dominant, lacks lower body engagement',
            'conditions': {
                'ground_max': 65,
                'weapon_min': 70
            },
            'weight': 1.0
        },
        'BALANCED': {
            'description': 'Balanced mechanics, no major strength or weakness',
            'conditions': {
                'score_variance_max': 20  # All scores within 20 points
            },
            'weight': 0.8
        }
    }
    
    # Detailed profile insights
    PROFILE_INSIGHTS = {
        'TITAN': {
            'famous_examples': ['Mike Trout', 'Aaron Judge', 'Mookie Betts (peak)'],
            'typical_body_type': 'Athletic, well-proportioned, explosive',
            'advantages': [
                'Elite power generation from ground',
                'Excellent energy transfer through kinetic chain',
                'Consistent barrel control',
                'High exit velocities',
                'Can handle all pitch types and locations'
            ],
            'disadvantages': [
                'High expectations to maintain',
                'Minor mechanical flaws can have major impact',
                'Requires consistent training to maintain elite status'
            ],
            'optimal_pitch_zones': ['All zones'],
            'struggle_zones': ['None - well-rounded'],
            'improvement_priority': 'Maintain consistency, fine-tune timing'
        },
        'SPINNER': {
            'famous_examples': ['Jose Altuve', 'Dustin Pedroia', 'David Eckstein'],
            'typical_body_type': 'Compact, lower center of gravity, strong legs',
            'advantages': [
                'Excellent lower body mechanics',
                'Good timing and rhythm',
                'Strong ground connection',
                'Quick to ball',
                'Good vs inside pitches'
            ],
            'disadvantages': [
                'Energy loss at contact point',
                'Hands disconnect from body rotation',
                'Inconsistent barrel control',
                'Vulnerable to outside pitches',
                'Can "spin off" the ball'
            ],
            'optimal_pitch_zones': ['Inside', 'Low', 'Middle-in'],
            'struggle_zones': ['Away', 'Up and away', 'Off-speed away'],
            'improvement_priority': 'WEAPON - Connect hands to rotation'
        },
        'SLINGSHOTTER': {
            'famous_examples': ['Early-career Giancarlo Stanton', 'Adam Dunn'],
            'typical_body_type': 'Strong, powerful, sometimes rigid upper body',
            'advantages': [
                'Powerful lower body drive',
                'Good hip-shoulder separation potential',
                'High peak exit velocities when connected',
                'Raw power generation'
            ],
            'disadvantages': [
                'Inconsistent bat path',
                'Energy leaks in kinetic chain',
                'Struggles with pitch recognition',
                'Long swing can be exploited',
                'Vulnerable to quality breaking balls'
            ],
            'optimal_pitch_zones': ['Middle', 'Up', 'Elevated fastballs'],
            'struggle_zones': ['Low', 'Away', 'Breaking balls down'],
            'improvement_priority': 'WEAPON - Improve hand path and bat control'
        },
        'WHIPPER': {
            'famous_examples': ['Ichiro Suzuki (contact mode)', 'Tony Gwynn (early)'],
            'typical_body_type': 'Lean, quick hands, sometimes smaller frame',
            'advantages': [
                'Quick bat speed through zone',
                'Good bat-to-ball skills',
                'Can handle high velocity',
                'Short, direct swing',
                'Good vs fastballs'
            ],
            'disadvantages': [
                'Limited power generation',
                'Poor lower body engagement',
                'Arm-dominant swing',
                'Lower exit velocities',
                'Struggles vs off-speed',
                'Minimal use of lower half'
            ],
            'optimal_pitch_zones': ['Up', 'Middle-up', 'Fastball zones'],
            'struggle_zones': ['Low', 'Off-speed', 'Breaking balls'],
            'improvement_priority': 'GROUND - Develop lower body connection'
        },
        'BALANCED': {
            'famous_examples': ['Most developing players', 'Solid average hitters'],
            'typical_body_type': 'Variable - depends on specific weaknesses',
            'advantages': [
                'No major mechanical flaw',
                'Well-rounded skillset',
                'Consistent performance',
                'Room for improvement in all areas'
            ],
            'disadvantages': [
                'No standout strength',
                'May lack elite tools',
                'Needs specific development path',
                'Can plateau without focused work'
            ],
            'optimal_pitch_zones': ['Middle', 'Depends on specific swing'],
            'struggle_zones': ['Varies by individual weaknesses'],
            'improvement_priority': 'Focus on lowest scoring component'
        }
    }
    
    def __init__(self):
        pass
    
    def _calculate_profile_score(
        self,
        profile: str,
        ground: float,
        engine: float,
        weapon: float
    ) -> float:
        """
        Calculate how well a player matches a specific profile
        Returns confidence score 0-100
        """
        rules = self.PROFILE_RULES[profile]['conditions']
        score = 0.0
        max_score = 0.0
        
        if profile == 'TITAN':
            # All scores must be high
            max_score = 300
            score = min(ground, 100) + min(engine, 100) + min(weapon, 100)
            # Bonus for exceeding 80 threshold
            if ground >= 80:
                score += (ground - 80) * 0.5
            if engine >= 80:
                score += (engine - 80) * 0.5
            if weapon >= 80:
                score += (weapon - 80) * 0.5
            return min(score / max_score * 100, 100)
        
        elif profile == 'SPINNER':
            # High ground and HIGH engine, low weapon
            # Key: Engine must be VERY HIGH (distinguishes from SLINGSHOTTER)
            max_score = 100
            ground_score = min(ground, 100) * 0.30
            # Engine is the key differentiator - must be high
            engine_score = min(engine, 100) * 0.40 if engine >= 75 else min(engine, 100) * 0.20
            # Weapon should be low - inverse scoring
            weapon_score = (100 - weapon) * 0.30 if weapon < 70 else 0
            score = ground_score + engine_score + weapon_score
            return min(score, 100)
        
        elif profile == 'SLINGSHOTTER':
            # High ground, medium engine, low weapon
            max_score = 100
            ground_score = min(ground, 100) * 0.40
            # Engine should be moderate
            engine_score = (100 - abs(engine - 72.5)) * 0.30
            # Weapon should be low
            weapon_score = (100 - weapon) * 0.30 if weapon < 70 else 0
            score = ground_score + engine_score + weapon_score
            return min(score, 100)
        
        elif profile == 'WHIPPER':
            # Low ground, high weapon
            max_score = 100
            # Ground should be low - inverse scoring
            ground_score = (100 - ground) * 0.40 if ground < 70 else 0
            weapon_score = min(weapon, 100) * 0.40
            # Engine can be moderate
            engine_score = min(engine, 100) * 0.20
            score = ground_score + weapon_score + engine_score
            return min(score, 100)
        
        elif profile == 'BALANCED':
            # All scores should be similar (low variance)
            scores = [ground, engine, weapon]
            avg_score = sum(scores) / len(scores)
            variance = sum((s - avg_score) ** 2 for s in scores) / len(scores)
            std_dev = variance ** 0.5
            
            # Lower variance = higher balanced score
            # Std dev of 0 = 100%, std dev of 30+ = 0%
            balanced_score = max(0, 100 - (std_dev * 3.33))
            return balanced_score
        
        return 0.0
    
    def classify_with_confidence(
        self,
        ground_score: float,
        engine_score: float,
        weapon_score: float,
        tempo_ratio: Optional[float] = None,
        kinematic_sequence_quality: Optional[float] = None
    ) -> Dict:
        """
        Classify motor profile with confidence scoring
        
        Args:
            ground_score: Ground (lower body) score 0-100
            engine_score: Engine (torso rotation) score 0-100
            weapon_score: Weapon (bat speed) score 0-100
            tempo_ratio: Optional tempo ratio for additional context
            kinematic_sequence_quality: Optional sequence quality score
            
        Returns:
            Dictionary with profile, confidence, and characteristics
        """
        # Calculate scores for all profiles
        profile_scores = {}
        for profile in self.PROFILE_RULES.keys():
            profile_scores[profile] = self._calculate_profile_score(
                profile, ground_score, engine_score, weapon_score
            )
        
        # Find primary profile (highest score)
        sorted_profiles = sorted(
            profile_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        primary_profile = sorted_profiles[0][0]
        primary_confidence = sorted_profiles[0][1]
        
        # Find secondary profile if confidence is low
        secondary_profile = None
        if primary_confidence < 80 and len(sorted_profiles) > 1:
            secondary_profile = sorted_profiles[1][0]
        
        # Generate characteristics based on scores
        characteristics = self._generate_characteristics(
            ground_score, engine_score, weapon_score
        )
        
        return {
            'profile': primary_profile,
            'confidence': round(primary_confidence, 1),
            'profile_scores': {k: round(v, 1) for k, v in profile_scores.items()},
            'secondary_profile': secondary_profile,
            'characteristics': characteristics
        }
    
    def _generate_characteristics(
        self,
        ground: float,
        engine: float,
        weapon: float
    ) -> List[str]:
        """
        Generate characteristic descriptions based on scores
        """
        chars = []
        
        # Ground characteristics
        if ground >= 85:
            chars.append('Excellent lower body power generation')
        elif ground >= 70:
            chars.append('Good lower body mechanics')
        elif ground >= 55:
            chars.append('Moderate lower body engagement')
        else:
            chars.append('Limited lower body contribution')
        
        # Engine characteristics
        if engine >= 85:
            chars.append('Elite core rotation and energy transfer')
        elif engine >= 70:
            chars.append('Good torso rotation velocity')
        elif engine >= 55:
            chars.append('Average core engagement')
        else:
            chars.append('Weak torso rotation')
        
        # Weapon characteristics
        if weapon >= 85:
            chars.append('Excellent bat speed and barrel control')
        elif weapon >= 70:
            chars.append('Good hand path efficiency')
        elif weapon >= 55:
            chars.append('Average bat-to-ball ability')
        else:
            chars.append('Poor energy transfer to bat')
        
        # Relationship characteristics
        if ground > 75 and engine > 75 and weapon < 60:
            chars.append('Body rotates well but hands disconnect')
        elif ground > 75 and weapon < 60:
            chars.append('Strong foundation but weak transfer to contact')
        elif weapon > 75 and ground < 60:
            chars.append('Hand-dominated swing lacking body support')
        
        return chars
    
    def get_profile_insights(self, profile: str) -> Dict:
        """
        Get detailed insights for a specific motor profile
        
        Args:
            profile: Profile name (TITAN, SPINNER, etc.)
            
        Returns:
            Dictionary with detailed profile information
        """
        if profile not in self.PROFILE_INSIGHTS:
            profile = 'BALANCED'  # Fallback
        
        insights = self.PROFILE_INSIGHTS[profile].copy()
        insights['name'] = profile
        insights['description'] = self.PROFILE_RULES[profile]['description']
        
        return insights
    
    def get_all_profiles_info(self) -> List[Dict]:
        """
        Get information about all motor profiles
        
        Returns:
            List of profile information dictionaries
        """
        profiles = []
        for profile_name in self.PROFILE_RULES.keys():
            info = self.get_profile_insights(profile_name)
            profiles.append(info)
        
        return profiles


if __name__ == "__main__":
    # Test the classifier
    print("="*70)
    print("MOTOR PROFILE CLASSIFIER TEST")
    print("="*70)
    
    classifier = MotorProfileClassifier()
    
    # Test Case 1: Eric Williams (SPINNER)
    print("\nTest 1: Eric Williams (Expected: SPINNER)")
    print("-" * 70)
    result = classifier.classify_with_confidence(
        ground_score=72,
        engine_score=85,
        weapon_score=40
    )
    print(f"Profile: {result['profile']}")
    print(f"Confidence: {result['confidence']}%")
    print(f"Profile Scores: {result['profile_scores']}")
    print(f"Secondary: {result['secondary_profile']}")
    print("Characteristics:")
    for char in result['characteristics']:
        print(f"  - {char}")
    
    # Test Case 2: Elite player (TITAN)
    print("\n\nTest 2: Elite Player (Expected: TITAN)")
    print("-" * 70)
    result = classifier.classify_with_confidence(
        ground_score=92,
        engine_score=90,
        weapon_score=88
    )
    print(f"Profile: {result['profile']}")
    print(f"Confidence: {result['confidence']}%")
    print(f"Profile Scores: {result['profile_scores']}")
    
    # Test Case 3: Upper body dominant (WHIPPER)
    print("\n\nTest 3: Upper Body Dominant (Expected: WHIPPER)")
    print("-" * 70)
    result = classifier.classify_with_confidence(
        ground_score=45,
        engine_score=60,
        weapon_score=78
    )
    print(f"Profile: {result['profile']}")
    print(f"Confidence: {result['confidence']}%")
    print(f"Profile Scores: {result['profile_scores']}")
    
    # Test Case 4: Balanced
    print("\n\nTest 4: Balanced Player (Expected: BALANCED)")
    print("-" * 70)
    result = classifier.classify_with_confidence(
        ground_score=68,
        engine_score=72,
        weapon_score=65
    )
    print(f"Profile: {result['profile']}")
    print(f"Confidence: {result['confidence']}%")
    print(f"Profile Scores: {result['profile_scores']}")
    
    # Get profile insights
    print("\n\nSPINNER Profile Insights:")
    print("-" * 70)
    insights = classifier.get_profile_insights('SPINNER')
    print(f"Description: {insights['description']}")
    print(f"Famous Examples: {', '.join(insights['famous_examples'])}")
    print(f"Advantages: {insights['advantages'][0]}")
    print(f"Improvement Priority: {insights['improvement_priority']}")
    
    print("\n" + "="*70)
