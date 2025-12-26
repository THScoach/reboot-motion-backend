"""
Recommendation Engine Module
Generates actionable improvement recommendations based on gap analysis

Part of Priority 3: Gap Analysis & Recommendations
"""

from typing import Dict, List
import logging

logger = logging.getLogger(__name__)


class RecommendationEngine:
    """
    Generates personalized improvement recommendations based on:
    - Gap analysis (actual vs potential)
    - Component scores (Ground, Engine, Weapon)
    - Motor profile classification
    """
    
    # Component-specific training drills
    COMPONENT_DRILLS = {
        'GROUND': {
            'drills': [
                'Med ball rotational throws (3 sets x 10 reps)',
                'Hip turn exercises with resistance bands',
                'Stride mechanics work with markers',
                'Lower half explosive drills (box jumps, broad jumps)',
                'Weight transfer exercises on balance board'
            ],
            'focus': 'Lower body power generation and connection to ground'
        },
        'ENGINE': {
            'drills': [
                'Separation drills (hips lead, shoulders follow)',
                'Torso rotation exercises with medicine ball',
                'Core strengthening (planks, Russian twists, wood chops)',
                'Timing sequencing work (slow motion swings)',
                'X-factor stretch exercises'
            ],
            'focus': 'Core rotation and energy transfer from lower to upper body'
        },
        'WEAPON': {
            'drills': [
                'Tee work focusing on hand path',
                'Inside-out swing path drills',
                'Barrel control exercises (hit specific zones)',
                'One-handed swings (lead arm extension)',
                'Contact point timing drills'
            ],
            'focus': 'Hand path efficiency and barrel control through contact'
        }
    }
    
    # Motor profile-specific guidance
    MOTOR_PROFILE_GUIDANCE = {
        'SPINNER': {
            'issue': 'Spinning off ball - hands not engaged',
            'primary_fix': 'WEAPON',
            'guidance': 'You rotate well but need to connect hands to body rotation. Focus on keeping hands inside the ball and extending through contact.',
            'key_drills': ['Tee work with inside-out path', 'Lead arm extension drills']
        },
        'SLINGSHOTTER': {
            'issue': 'Good body rotation but poor energy transfer to bat',
            'primary_fix': 'WEAPON',
            'guidance': 'Your body generates good rotation but energy is not transferring efficiently to the bat. Work on connecting core rotation to hand path.',
            'key_drills': ['Timing sequencing drills', 'One-handed swings']
        },
        'WHIPPER': {
            'issue': 'All hands, no body support',
            'primary_fix': 'GROUND',
            'guidance': 'You rely too much on upper body. Build lower half engagement and let the body drive the swing, not just the hands.',
            'key_drills': ['Hip rotation drills', 'Weight transfer exercises', 'Med ball throws']
        },
        'TITAN': {
            'issue': 'Elite mechanics - minor refinements',
            'primary_fix': None,
            'guidance': 'Excellent mechanics across all components. Focus on maintaining consistency and fine-tuning timing.',
            'key_drills': ['Maintain current training', 'Game-speed repetitions']
        },
        'BALANCED': {
            'issue': 'Balanced profile - no major weakness',
            'primary_fix': None,
            'guidance': 'Solid mechanics across the board. Focus on the weakest scoring component for incremental gains.',
            'key_drills': ['Component-specific based on scores']
        }
    }
    
    def __init__(self):
        pass
    
    def estimate_potential_gain(
        self,
        component_score: float,
        total_gap_mph: float
    ) -> float:
        """
        Estimate potential bat speed gain from improving a component
        
        Args:
            component_score: Current score (0-100) for the component
            total_gap_mph: Total bat speed gap between actual and potential
            
        Returns:
            Estimated gain in mph from improving this component
        """
        # Lower scores = more potential for improvement
        if component_score < 40:
            gain_percentage = 0.50  # 50% of total gap
        elif component_score < 55:
            gain_percentage = 0.40  # 40% of total gap
        elif component_score < 70:
            gain_percentage = 0.30  # 30% of total gap
        elif component_score < 85:
            gain_percentage = 0.20  # 20% of total gap
        else:
            gain_percentage = 0.10  # 10% of total gap
        
        return total_gap_mph * gain_percentage
    
    def generate_component_recommendation(
        self,
        component: str,
        score: float,
        priority: str,
        potential_gain_mph: float
    ) -> Dict:
        """
        Generate recommendation for a specific component
        
        Args:
            component: 'GROUND', 'ENGINE', or 'WEAPON'
            score: Current score (0-100)
            priority: 'CRITICAL', 'HIGH', 'MEDIUM', or 'LOW'
            potential_gain_mph: Estimated gain in bat speed
            
        Returns:
            Component recommendation dictionary
        """
        component_info = self.COMPONENT_DRILLS.get(component, {})
        
        # Determine training frequency based on priority
        if priority == 'CRITICAL':
            training_frequency = '5-6 days per week'
        elif priority == 'HIGH':
            training_frequency = '4-5 days per week'
        elif priority == 'MEDIUM':
            training_frequency = '3-4 days per week'
        else:
            training_frequency = '2-3 days per week'
        
        return {
            'component': component,
            'current_score': round(score, 1),
            'priority': priority,
            'estimated_gain_mph': round(potential_gain_mph, 1),
            'focus_area': component_info.get('focus', 'General mechanics'),
            'recommended_drills': component_info.get('drills', []),
            'training_frequency': training_frequency
        }
    
    def generate_motor_profile_recommendation(
        self,
        motor_profile: str,
        weakest_component: str
    ) -> Dict:
        """
        Generate motor profile-specific recommendation
        
        Args:
            motor_profile: 'SPINNER', 'SLINGSHOTTER', 'WHIPPER', 'TITAN', 'BALANCED'
            weakest_component: Weakest component from gap analysis
            
        Returns:
            Motor profile guidance dictionary
        """
        # Get profile-specific guidance (fallback to BALANCED if unknown)
        profile_info = self.MOTOR_PROFILE_GUIDANCE.get(
            motor_profile,
            self.MOTOR_PROFILE_GUIDANCE['BALANCED']
        )
        
        # Use profile's recommended fix, or fallback to weakest component
        primary_fix = profile_info['primary_fix'] or weakest_component
        
        return {
            'motor_profile': motor_profile,
            'issue': profile_info['issue'],
            'primary_fix': primary_fix,
            'guidance': profile_info['guidance'],
            'key_drills': profile_info['key_drills']
        }
    
    def generate_complete_recommendations(
        self,
        gap_analysis: Dict,
        motor_profile: str
    ) -> Dict:
        """
        Generate complete recommendation package
        
        Args:
            gap_analysis: Output from GapAnalyzer.calculate_complete_gap_analysis()
            motor_profile: Motor profile classification
            
        Returns:
            Complete recommendations dictionary with:
            - Primary focus (weakest component)
            - Motor profile guidance
            - Secondary focus areas
            - Action plan
            - Total estimated gain
        """
        # Extract key metrics
        bat_speed_gap_mph = gap_analysis['bat_speed']['gap_mph']
        weakest = gap_analysis['weakest_component']
        
        # Generate primary recommendation (weakest component)
        primary_gain = self.estimate_potential_gain(
            weakest['score'],
            bat_speed_gap_mph
        )
        
        primary_recommendation = self.generate_component_recommendation(
            weakest['weakest_component'],
            weakest['score'],
            weakest['priority'],
            primary_gain
        )
        
        # Generate motor profile-specific recommendation
        profile_recommendation = self.generate_motor_profile_recommendation(
            motor_profile,
            weakest['weakest_component']
        )
        
        # Generate secondary recommendations for other low-scoring components
        secondary_recommendations = []
        for component, score in weakest['components_ranked'][1:]:  # Skip the weakest (already primary)
            if score < 80:  # Only recommend if below 80
                gain = self.estimate_potential_gain(score, bat_speed_gap_mph)
                
                # Determine priority
                if score < 65:
                    priority = 'HIGH'
                elif score < 80:
                    priority = 'MEDIUM'
                else:
                    priority = 'LOW'
                
                secondary_recommendations.append(
                    self.generate_component_recommendation(component, score, priority, gain)
                )
        
        # Generate action plan
        action_plan = self._generate_action_plan(
            primary_recommendation,
            profile_recommendation,
            secondary_recommendations
        )
        
        # Calculate total estimated gain
        total_gain = primary_gain + sum(r['estimated_gain_mph'] for r in secondary_recommendations)
        
        return {
            'summary': gap_analysis['summary'],
            'primary_focus': primary_recommendation,
            'motor_profile_guidance': profile_recommendation,
            'secondary_focus': secondary_recommendations,
            'action_plan': action_plan,
            'total_estimated_gain_mph': round(total_gain, 1)
        }
    
    def _generate_action_plan(
        self,
        primary: Dict,
        profile: Dict,
        secondary: List[Dict]
    ) -> str:
        """
        Generate formatted action plan text
        """
        plan = f"""1. PRIMARY FOCUS: {primary['component']} (current score: {primary['current_score']}, potential gain: +{primary['estimated_gain_mph']} mph)
   - {profile['guidance']}
   - Train {primary['training_frequency']}
   - Key drills: {', '.join(profile['key_drills'][:2])}

"""
        
        if secondary:
            plan += f"2. SECONDARY FOCUS: {', '.join([r['component'] for r in secondary])}\n"
            for rec in secondary:
                plan += f"   - {rec['component']}: +{rec['estimated_gain_mph']} mph potential gain\n"
            plan += "\n"
        
        plan += "3. REASSESS: Test again in 4-6 weeks to measure progress"
        
        return plan


if __name__ == "__main__":
    # Test with Eric Williams data
    print("="*70)
    print("RECOMMENDATION ENGINE TEST - ERIC WILLIAMS")
    print("="*70)
    
    # Mock gap analysis (output from GapAnalyzer)
    gap_analysis = {
        'bat_speed': {
            'actual_mph': 57.9,
            'potential_mph': 76.0,
            'gap_mph': 18.1,
            'pct_achieved': 76.2,
            'pct_untapped': 23.8,
            'status': 'BELOW_POTENTIAL'
        },
        'weakest_component': {
            'weakest_component': 'WEAPON',
            'score': 40,
            'priority': 'CRITICAL',
            'components_ranked': [('WEAPON', 40), ('GROUND', 72), ('ENGINE', 85)]
        },
        'overall_efficiency': 65.7,
        'summary': 'Achieving 76.2% of bat speed potential (18.1 mph gap). Focus on WEAPON (score: 40) for improvement. Overall efficiency: 65.7%'
    }
    
    motor_profile = 'SPINNER'
    
    # Generate recommendations
    engine = RecommendationEngine()
    recommendations = engine.generate_complete_recommendations(gap_analysis, motor_profile)
    
    # Display results
    print("\nPrimary Focus:")
    print(f"  Component: {recommendations['primary_focus']['component']}")
    print(f"  Current Score: {recommendations['primary_focus']['current_score']}/100")
    print(f"  Priority: {recommendations['primary_focus']['priority']}")
    print(f"  Estimated Gain: +{recommendations['primary_focus']['estimated_gain_mph']} mph")
    print(f"  Training: {recommendations['primary_focus']['training_frequency']}")
    
    print("\nMotor Profile Guidance:")
    print(f"  Profile: {recommendations['motor_profile_guidance']['motor_profile']}")
    print(f"  Issue: {recommendations['motor_profile_guidance']['issue']}")
    print(f"  Fix: {recommendations['motor_profile_guidance']['primary_fix']}")
    print(f"  Guidance: {recommendations['motor_profile_guidance']['guidance']}")
    
    if recommendations['secondary_focus']:
        print("\nSecondary Focus:")
        for rec in recommendations['secondary_focus']:
            print(f"  - {rec['component']}: +{rec['estimated_gain_mph']} mph potential")
    
    print(f"\nTotal Estimated Gain: +{recommendations['total_estimated_gain_mph']} mph")
    
    print("\nAction Plan:")
    print(recommendations['action_plan'])
    
    print("\n" + "="*70)
