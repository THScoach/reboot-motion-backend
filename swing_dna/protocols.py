"""
Training Protocols Library for Swing DNA
========================================

5 Evidence-Based Training Protocols:
1. PROTOCOL_1: Fix Lead Knee Energy Leak
2. PROTOCOL_2: Develop Vertical Ground Force
3. PROTOCOL_3: Train Hip Lock
4. PROTOCOL_4: Restore Kinetic Sequence
5. PROTOCOL_5: Integration to Live Swings

Based on Randy Sullivan, Frans Bosch, and Dr. Kwon research.
"""

from typing import Dict, List

# Protocol 1: Fix Lead Knee Energy Leak
PROTOCOL_1 = {
    'id': 'PROTOCOL_1',
    'name': 'Fix Lead Knee Energy Leak',
    'duration_weeks': 2,
    'focus': 'Lead knee extension (0-140° → 160-180°)',
    'indication': 'Lead knee < 140° at contact, energy leak pattern',
    'weeks': [
        {
            'week': '1-2',
            'focus': 'Fix Lead Knee Leak',
            'frequency': 'Daily',
            'session_duration': '20-30 minutes',
            'drills': [
                {
                    'name': 'Single-Leg Isometric Holds',
                    'sets': 3,
                    'reps': '20s',
                    'rest': '60s',
                    'intensity': 'Moderate',
                    'cue': 'Steel rod, not shock absorber',
                    'description': 'Stand on lead leg, knee at 160-170°. Push through ball of foot, engage quad + glute.',
                    'equipment': ['None'],
                    'progression': 'Increase hold time to 30s by Week 2'
                },
                {
                    'name': 'Single-Leg Vertical Jumps',
                    'sets': 3,
                    'reps': 5,
                    'rest': '90s',
                    'intensity': 'High',
                    'cue': 'Lock it on landing, don\'t collapse',
                    'description': 'Jump vertically off lead leg only. Land with knee 160-180° (stiff landing). Stick landing 2 seconds.',
                    'equipment': ['None'],
                    'progression': 'Increase jump height and landing control'
                },
                {
                    'name': 'Wall Knee Extension Drill',
                    'sets': 3,
                    'reps': 10,
                    'rest': '60s',
                    'intensity': 'Moderate',
                    'cue': 'Push down, knee locks',
                    'description': 'Back against wall, lead foot 12" forward. Push through ball of foot → extend knee. Feel quad + glute activate simultaneously.',
                    'equipment': ['Wall'],
                    'progression': 'Add resistance band around thigh'
                }
            ],
            'expected_change': 'Lead knee 0-140° → 160-180° at contact',
            'downstream_effect': 'Hip angmom ↑ by 2-3x',
            'validation_test': 'Video swing analysis - measure lead knee angle at contact'
        }
    ]
}

# Protocol 2: Develop Vertical Ground Force
PROTOCOL_2 = {
    'id': 'PROTOCOL_2',
    'name': 'Develop Vertical Ground Force',
    'duration_weeks': 4,
    'focus': 'vGRF 0.8-1.0x → 1.5-2.0x bodyweight',
    'indication': 'vGRF < 1.2x bodyweight, fast foot roll pattern',
    'weeks': [
        {
            'week': '1-2',
            'focus': 'Foundation - Soft Pedal',
            'frequency': '5 days/week',
            'session_duration': '20-30 minutes',
            'drills': [
                {
                    'name': 'Force Pedals (Soft)',
                    'sets': 3,
                    'reps': '10 swings',
                    'rest': '120s',
                    'intensity': 'Moderate',
                    'cue': 'Feel the bounce, push through it',
                    'description': 'Soft hexagonal foam platform under ball of lead foot. Start with dry swings only.',
                    'equipment': ['Force Pedals (soft)'],
                    'progression': 'Week 1: Dry swings, Week 2: Add tee work'
                },
                {
                    'name': 'Single-Leg Calf Raises',
                    'sets': 3,
                    'reps': 15,
                    'rest': '60s',
                    'intensity': 'Moderate',
                    'cue': 'Push through the ball of your foot',
                    'description': 'Stand on lead leg, ball of foot on edge. Rise to toes (plantarflexion), hold 2s, lower slowly.',
                    'equipment': ['Step or platform'],
                    'progression': 'Add weight (hold dumbbell)'
                },
                {
                    'name': 'Lead Leg Slam → Swing',
                    'sets': 3,
                    'reps': 10,
                    'rest': '90s',
                    'intensity': 'High',
                    'cue': 'Slam, brake hip, whip bat',
                    'description': 'Stand on lead leg. SLAM foot down (vertical push). Immediately load and swing. Feel hip decelerate after slam.',
                    'equipment': ['Bat'],
                    'progression': 'Add resistance band for added force'
                }
            ],
            'expected_change': 'vGRF 0.8-1.0x → 1.2-1.5x bodyweight',
            'downstream_effect': 'Hip deceleration capability ↑',
            'validation_test': 'Force plate measurement (if available)'
        },
        {
            'week': '3-4',
            'focus': 'Progression - Firm Pedal + Integration',
            'frequency': '5 days/week',
            'session_duration': '30-40 minutes',
            'drills': [
                {
                    'name': 'Force Pedals (Firm)',
                    'sets': 3,
                    'reps': '10 swings',
                    'rest': '120s',
                    'intensity': 'High',
                    'cue': 'Bounce off the ground',
                    'description': 'Firm pedal under lead foot. Progress from dry swings to tee work.',
                    'equipment': ['Force Pedals (firm)'],
                    'progression': 'Week 3: Tee, Week 4: Soft toss'
                },
                {
                    'name': 'Lead Leg Slam → Swing',
                    'sets': 3,
                    'reps': 10,
                    'rest': '90s',
                    'intensity': 'High',
                    'cue': 'Slam, brake hip, whip bat',
                    'description': 'Stand on lead leg. SLAM foot down. Immediately swing. Feel hip brake.',
                    'equipment': ['Bat'],
                    'progression': 'Increase force of slam'
                },
                {
                    'name': 'Medicine Ball Rotational Throws',
                    'sets': 3,
                    'reps': 8,
                    'rest': '120s',
                    'intensity': 'High',
                    'cue': 'Hip brake, torso GO',
                    'description': 'Simulate swing motion with 8-10lb med ball. Focus: Hip stops → Torso continues → Ball releases.',
                    'equipment': ['Medicine ball (8-10 lbs)'],
                    'progression': 'Increase ball weight to 12 lbs'
                }
            ],
            'expected_change': 'vGRF 1.2-1.5x → 1.5-2.0x bodyweight, Hip angmom 4-5 → 6-8',
            'downstream_effect': 'Shoulder/Hip ratio 8x → 3-4x',
            'validation_test': 'Force plate + video analysis'
        }
    ]
}

# Protocol 3: Train Hip Lock
PROTOCOL_3 = {
    'id': 'PROTOCOL_3',
    'name': 'Train Hip Lock',
    'duration_weeks': 2,
    'focus': 'Pelvic stability and deceleration',
    'indication': 'Weak hip deceleration, early pelvis rotation',
    'weeks': [
        {
            'week': '1-2',
            'focus': 'Hip Lock Training',
            'frequency': '4-5 days/week',
            'session_duration': '25-35 minutes',
            'drills': [
                {
                    'name': 'Pallof Press (Anti-Rotation)',
                    'sets': 3,
                    'reps': 10,
                    'rest': '60s',
                    'intensity': 'Moderate',
                    'cue': 'Resist the pull, hips stay square',
                    'description': 'Band at chest height. Press forward, resist rotation. Hold 3s.',
                    'equipment': ['Resistance band', 'Anchor point'],
                    'progression': 'Increase band resistance'
                },
                {
                    'name': 'Hip Bridge Holds',
                    'sets': 3,
                    'reps': '30s',
                    'rest': '60s',
                    'intensity': 'Moderate',
                    'cue': 'Squeeze glutes, stable pelvis',
                    'description': 'Lie on back, feet flat. Lift hips, hold position. Feel glute activation.',
                    'equipment': ['None'],
                    'progression': 'Single-leg hip bridges'
                },
                {
                    'name': 'Rotational Med Ball Slams',
                    'sets': 3,
                    'reps': 8,
                    'rest': '90s',
                    'intensity': 'High',
                    'cue': 'Hip stops, torso accelerates',
                    'description': 'Hold med ball. Rotate and slam to ground. Focus on hip deceleration.',
                    'equipment': ['Medicine ball (10 lbs)'],
                    'progression': 'Increase slam speed'
                }
            ],
            'expected_change': 'Improved hip stability, delayed pelvis rotation',
            'downstream_effect': 'Increased hip-shoulder separation',
            'validation_test': 'Video analysis - measure hip-shoulder separation'
        }
    ]
}

# Protocol 4: Restore Kinetic Sequence
PROTOCOL_4 = {
    'id': 'PROTOCOL_4',
    'name': 'Restore Kinetic Sequence',
    'duration_weeks': 2,
    'focus': 'Proper timing: Hips → Torso → Arms → Bat',
    'indication': 'Simultaneous rotation, poor separation',
    'weeks': [
        {
            'week': '1-2',
            'focus': 'Sequential Activation',
            'frequency': '4-5 days/week',
            'session_duration': '30-40 minutes',
            'drills': [
                {
                    'name': 'Step Back → Load → Explode',
                    'sets': 3,
                    'reps': 10,
                    'rest': '60s',
                    'intensity': 'Moderate',
                    'cue': '1-2-3 rhythm: Step, load, GO',
                    'description': 'Step back with back foot. Load. EXPLODE forward with hips leading.',
                    'equipment': ['Bat'],
                    'progression': 'Increase load speed'
                },
                {
                    'name': 'Hip Turn → Freeze',
                    'sets': 3,
                    'reps': 8,
                    'rest': '60s',
                    'intensity': 'Moderate',
                    'cue': 'Hips GO, shoulders stay',
                    'description': 'Initiate hip rotation. Hold shoulders back. Feel stretch. Then release.',
                    'equipment': ['Bat'],
                    'progression': 'Increase hold time'
                },
                {
                    'name': 'Med Ball Sequential Throw',
                    'sets': 3,
                    'reps': 8,
                    'rest': '90s',
                    'intensity': 'High',
                    'cue': 'Hips, torso, arms, BALL',
                    'description': 'Throw med ball. Focus on sequential firing: hips first, then torso, then arms.',
                    'equipment': ['Medicine ball (8 lbs)'],
                    'progression': 'Increase throw distance'
                }
            ],
            'expected_change': 'Hip-shoulder timing gap 5-10ms → 15-25ms',
            'downstream_effect': 'Reduced shoulder compensation, improved bat whip',
            'validation_test': 'Motion capture - timing analysis'
        }
    ]
}

# Protocol 5: Integration to Live Swings
PROTOCOL_5 = {
    'id': 'PROTOCOL_5',
    'name': 'Integration to Live Swings',
    'duration_weeks': 2,
    'focus': 'Transfer training to game swings',
    'indication': 'Final phase for all patterns',
    'weeks': [
        {
            'week': '5-6',
            'focus': 'Live Integration',
            'frequency': '5 days/week',
            'session_duration': '45-60 minutes',
            'drills': [
                {
                    'name': 'Force Pedals + Soft Toss (Firm)',
                    'sets': 3,
                    'reps': '15 swings',
                    'rest': '180s',
                    'intensity': 'Game-speed',
                    'cue': 'Push, extend, whip',
                    'description': 'Firm pedal under lead foot. Live ball contact (soft toss from front). Focus: Vertical push → Extension → Whip.',
                    'equipment': ['Force Pedals (firm)', 'Balls'],
                    'progression': 'Increase pitch velocity'
                },
                {
                    'name': 'Dr. Kwon Rope Swings',
                    'sets': 3,
                    'reps': 20,
                    'rest': '90s',
                    'intensity': 'Moderate',
                    'cue': 'Hips, torso, arms, THEN rope',
                    'description': 'Rope attached to bat handle (3-4 feet). Swing rope → forces sequential acceleration. Feel "lag" (rope lags behind body rotation).',
                    'equipment': ['Rope', 'Bat'],
                    'progression': 'Add weighted rope'
                },
                {
                    'name': 'Constraint Soft Toss',
                    'sets': 3,
                    'reps': 20,
                    'rest': '120s',
                    'intensity': 'Game-speed',
                    'cue': 'Lead arm stretches to ball',
                    'description': 'Ball placed at contact point on tee. Must extend lead arm to reach ball. Can\'t pull across (ball will be missed).',
                    'equipment': ['Tee', 'Balls'],
                    'progression': 'Move to front toss, then live BP'
                }
            ],
            'expected_change': 'Pattern transfers to live swings, ball outcomes improve',
            'downstream_effect': 'Exit velo ↑ 5-9 mph, Launch angle ↑ 10-15°, GB% ↓ 20-30%',
            'validation_test': 'Game stats - exit velo, launch angle, batted ball distribution'
        }
    ]
}

# Combined protocols dictionary
PROTOCOLS = {
    'PROTOCOL_1': PROTOCOL_1,
    'PROTOCOL_2': PROTOCOL_2,
    'PROTOCOL_3': PROTOCOL_3,
    'PROTOCOL_4': PROTOCOL_4,
    'PROTOCOL_5': PROTOCOL_5
}

# Protocol selection based on pattern
PROTOCOL_MAPPING = {
    'PATTERN_1_KNEE_LEAK': {
        'primary': 'PROTOCOL_1',
        'secondary': 'PROTOCOL_2',
        'integration': 'PROTOCOL_5'
    },
    'PATTERN_2_WEAK_HIP': {
        'primary': 'PROTOCOL_2',
        'secondary': 'PROTOCOL_3',
        'integration': 'PROTOCOL_5'
    },
    'PATTERN_3_SPINNER': {
        'primary': 'PROTOCOL_2',
        'secondary': 'PROTOCOL_1',
        'integration': 'PROTOCOL_5'
    },
    'PATTERN_4_SHOULDER_COMP': {
        'primary': 'PROTOCOL_3',
        'secondary': 'PROTOCOL_4',
        'integration': 'PROTOCOL_5'
    }
}

