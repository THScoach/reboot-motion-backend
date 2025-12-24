"""
Knowledge Base
==============

Central repository for:
- Drill library (all training drills)
- Pattern recognition rules (mechanical issues)
- Drill prescription rules (issue → drill mapping)

Author: Builder 2
Date: 2024-12-24
"""

from typing import Dict, List

# ============================================================
# DRILL LIBRARY
# ============================================================

DRILL_LIBRARY = {
    "rope_swings": {
        "drill_name": "Rope Swings",
        "category": "Extension",
        "targets": ["Lead arm extension", "Preventing over-rotation"],
        "description": "Swing a heavy rope (or towel) to force arm extension. Can't compensate with body rotation.",
        "volume": "20 swings",
        "frequency": "Daily",
        "duration_weeks": 2,
        "video_demo_url": "/drills/rope-swings.mp4",
        "coaching_cues": [
            "Focus on extending through the 'contact' point",
            "Feel the rope pulling your arms long",
            "Don't let shoulders over-rotate to compensate"
        ],
        "progression": [
            {"week": 1, "volume": "15 swings daily", "focus": "Learn movement pattern"},
            {"week": 2, "volume": "20 swings daily", "focus": "Add intent/speed"},
            {"week": 3, "volume": "20 swings + tee work", "focus": "Transfer to bat"}
        ]
    },
    
    "one_arm_swings": {
        "drill_name": "Lead-Arm One-Hand Swings",
        "category": "Extension",
        "targets": ["Lead arm extension", "Driving through pitch plane"],
        "description": "Take swings with only lead arm. Forces arm to extend to make contact.",
        "volume": "30 reps",
        "frequency": "3x per week",
        "duration_weeks": 3,
        "video_demo_url": "/drills/one-arm-swings.mp4",
        "coaching_cues": [
            "Grip bat at balance point",
            "Extend arm through contact zone",
            "Feel lat engage as arm extends"
        ]
    },
    
    "resistance_band_extension": {
        "drill_name": "Resistance Band Extension Drills",
        "category": "Extension",
        "targets": ["Lead arm extension", "Lat activation"],
        "description": "Band around lead wrist, anchor behind. Swing against resistance.",
        "volume": "3 sets of 10 reps",
        "frequency": "Daily",
        "duration_weeks": 2,
        "video_demo_url": "/drills/band-extension.mp4",
        "coaching_cues": [
            "Band pulls you back, fight to extend forward",
            "Feel the stretch in lead lat",
            "Keep shoulders from over-rotating"
        ]
    },
    
    "no_stride_tee": {
        "drill_name": "No-Stride Tee Work",
        "category": "Connection",
        "targets": ["Staying connected", "Feeling load-to-launch"],
        "description": "Hit off tee with zero stride. Forces feel of quick, connected load-to-launch.",
        "volume": "50 swings",
        "frequency": "3x per week",
        "duration_weeks": 2,
        "video_demo_url": "/drills/no-stride-tee.mp4",
        "coaching_cues": [
            "No stride, just rotate",
            "Feel connected turn",
            "Quick load-to-launch"
        ]
    },
    
    "constraint_timing": {
        "drill_name": "Timing Constraint Soft Toss",
        "category": "Connection",
        "targets": ["Load speed", "Preventing over-separation"],
        "description": "Soft toss with 0.5 second load limit.",
        "volume": "40 swings",
        "frequency": "2x per week",
        "duration_weeks": 3,
        "video_demo_url": "/drills/constraint-timing.mp4",
        "coaching_cues": [
            "Quick trigger",
            "Don't get stuck in load",
            "Trust your hands"
        ]
    },
    
    "front_foot_elevated": {
        "drill_name": "Front Foot Elevated Tee",
        "category": "Separation",
        "targets": ["Hip-shoulder separation", "Ground force generation"],
        "description": "Front foot on 2-4 inch platform. Forces downward drive.",
        "volume": "30 swings",
        "frequency": "Daily",
        "duration_weeks": 3,
        "video_demo_url": "/drills/elevated-front-foot.mp4",
        "coaching_cues": [
            "Push down into elevated foot",
            "Feel hips fire first",
            "Delay shoulder opening"
        ]
    },
    
    "resistance_band_hips": {
        "drill_name": "Resistance Band Hip Lock",
        "category": "Separation",
        "targets": ["Hip-shoulder separation", "Elastic tension"],
        "description": "Band around hips, anchored behind. Push hips forward while delaying shoulders.",
        "volume": "3 sets of 10 dry swings",
        "frequency": "Daily",
        "duration_weeks": 2,
        "video_demo_url": "/drills/band-hip-lock.mp4",
        "coaching_cues": [
            "Drive hips against band",
            "Keep shoulders closed 0.5 seconds",
            "Feel stretch in front of spine"
        ]
    },
    
    "eyes_closed_tee": {
        "drill_name": "Eyes Closed Tee Work",
        "category": "Stability",
        "targets": ["Head stability", "Proprioception"],
        "description": "Hit off tee with eyes closed. Forces body awareness.",
        "volume": "20 swings",
        "frequency": "3x per week",
        "duration_weeks": 2,
        "video_demo_url": "/drills/eyes-closed.mp4",
        "coaching_cues": [
            "Feel your head stay quiet",
            "Balance through contact",
            "Trust your body"
        ]
    },
    
    "balance_finish": {
        "drill_name": "Balance Finish Drill",
        "category": "Stability",
        "targets": ["Head stability", "Posture control"],
        "description": "Every swing must finish in balanced position (hold 3 seconds).",
        "volume": "Every swing",
        "frequency": "Always",
        "duration_weeks": "Ongoing",
        "video_demo_url": "/drills/balance-finish.mp4",
        "coaching_cues": [
            "Hold finish 3 seconds",
            "Check head position",
            "Feel stable base"
        ]
    },
    
    "separation_drill": {
        "drill_name": "Hip-Shoulder Separation Drill",
        "category": "Separation",
        "targets": ["Hip-shoulder separation", "Elastic load"],
        "description": "Practice creating separation between hips and shoulders during load phase.",
        "volume": "3 sets of 10 reps",
        "frequency": "Daily",
        "duration_weeks": 3,
        "video_demo_url": "/drills/separation-drill.mp4",
        "coaching_cues": [
            "Load hips first",
            "Keep shoulders back",
            "Feel the stretch"
        ]
    }
}


# ============================================================
# PATTERN RECOGNITION RULES
# ============================================================

PATTERN_RULES = {
    # ========================================
    # SPINNER PATTERNS
    # ========================================
    "spinner_lead_arm_bent": {
        "conditions": {
            "motor_profile": "Spinner",
            "hip_shoulder_gap_ms": {"min": 10, "max": 20},
            "hands_bat_gap_ms": {"max": 15}
        },
        "diagnosis": "Lead arm not extending through pitch plane",
        "symptoms": [
            "Ground ball tendency",
            "Weak contact on away pitches",
            "Miss breaking balls away",
            "Top hand pronates early"
        ],
        "root_cause": "Lead arm stays bent through contact, causing rotation across pitch plane instead of through it",
        "priority": "HIGH"
    },
    
    "spinner_over_rotation": {
        "conditions": {
            "motor_profile": "Spinner",
            "hip_shoulder_gap_ms": {"max": 18},
            "stability_score": {"min": 85}
        },
        "diagnosis": "Shoulders over-compensating for lack of arm extension",
        "symptoms": [
            "Barrel sweeps instead of snaps",
            "Long swing path",
            "Pull-side dominant"
        ],
        "root_cause": "Arms not creating momentum on pitch plane, shoulders rotate excessively to compensate",
        "priority": "HIGH"
    },
    
    # ========================================
    # WHIPPER PATTERNS
    # ========================================
    "whipper_disconnection": {
        "conditions": {
            "motor_profile": "Whipper",
            "hip_shoulder_gap_ms": {"min": 30},
            "tempo_ratio": {"min": 3.0}
        },
        "diagnosis": "Loading too long, swing getting disconnected",
        "symptoms": [
            "Late on fastballs",
            "Swing feels long",
            "Inconsistent contact"
        ],
        "root_cause": "Excessive load phase breaks kinetic chain timing",
        "priority": "MEDIUM"
    },
    
    "whipper_early_rotation": {
        "conditions": {
            "motor_profile": "Whipper",
            "hip_shoulder_gap_ms": {"min": 25},
            "tempo_ratio": {"max": 2.0}
        },
        "diagnosis": "Not utilizing separation, rotating too early",
        "symptoms": [
            "Power inconsistency",
            "Fly outs to pull side"
        ],
        "root_cause": "Creating separation but not holding it long enough",
        "priority": "MEDIUM"
    },
    
    # ========================================
    # TORQUER PATTERNS
    # ========================================
    "torquer_rushing": {
        "conditions": {
            "motor_profile": "Torquer",
            "tempo_ratio": {"max": 1.5},
            "hip_shoulder_gap_ms": {"max": 15}
        },
        "diagnosis": "Rushing through swing, not building tension",
        "symptoms": [
            "Weak contact despite good ground forces",
            "Swing feels quick but lacks power"
        ],
        "root_cause": "Moving too fast to build elastic tension in torso",
        "priority": "MEDIUM"
    },
    
    "torquer_no_separation": {
        "conditions": {
            "motor_profile": "Torquer",
            "hip_shoulder_gap_ms": {"max": 12},
            "stability_score": {"min": 85}
        },
        "diagnosis": "Not creating any hip-shoulder separation",
        "symptoms": [
            "Limited power ceiling",
            "All arms swing"
        ],
        "root_cause": "Ground force not translating to rotational separation",
        "priority": "HIGH"
    },
    
    # ========================================
    # UNIVERSAL PATTERNS
    # ========================================
    "poor_kinematic_sequence": {
        "conditions": {
            "sequence_grade": ["C", "D", "F"]
        },
        "diagnosis": "Kinetic chain breakdown",
        "symptoms": [
            "Inconsistent power",
            "Effort doesn't match results"
        ],
        "root_cause": "Body segments not firing in optimal sequence",
        "priority": "HIGH"
    },
    
    "stability_issues": {
        "conditions": {
            "stability_score": {"max": 75}
        },
        "diagnosis": "Excessive head/spine movement",
        "symptoms": [
            "Inconsistent barrel contact",
            "Struggles with breaking balls"
        ],
        "root_cause": "Head moving during swing disrupts visual tracking",
        "priority": "HIGH"
    },
    
    "tempo_too_slow": {
        "conditions": {
            "tempo_ratio": {"min": 3.5}
        },
        "diagnosis": "Loading too long, losing momentum",
        "symptoms": [
            "Late on fastballs",
            "Timing issues"
        ],
        "root_cause": "Excessive load phase disrupts timing",
        "priority": "MEDIUM"
    },
    
    "tempo_too_fast": {
        "conditions": {
            "tempo_ratio": {"max": 1.2}
        },
        "diagnosis": "Not enough load, no elastic energy",
        "symptoms": [
            "Weak contact",
            "No power despite good mechanics"
        ],
        "root_cause": "No time to build elastic tension",
        "priority": "MEDIUM"
    }
}


# ============================================================
# PRESCRIPTION RULES
# ============================================================

PRESCRIPTION_RULES = {
    "spinner_lead_arm_bent": {
        "primary_drills": ["rope_swings", "one_arm_swings"],
        "secondary_drills": ["resistance_band_extension"],
        "duration_weeks": 3,
        "expected_gains": "+3-5 mph exit velocity, better away contact, less ground balls"
    },
    
    "spinner_over_rotation": {
        "primary_drills": ["rope_swings", "resistance_band_extension"],
        "secondary_drills": ["one_arm_swings"],
        "duration_weeks": 2,
        "expected_gains": "+2-4 mph bat speed, tighter swing path"
    },
    
    "whipper_disconnection": {
        "primary_drills": ["no_stride_tee", "constraint_timing"],
        "secondary_drills": [],
        "duration_weeks": 2,
        "expected_gains": "Better fastball timing, more consistent contact"
    },
    
    "whipper_early_rotation": {
        "primary_drills": ["resistance_band_hips", "separation_drill"],
        "secondary_drills": [],
        "duration_weeks": 3,
        "expected_gains": "+3-5 mph bat speed from better separation utilization"
    },
    
    "torquer_rushing": {
        "primary_drills": ["resistance_band_hips", "no_stride_tee"],
        "secondary_drills": [],
        "duration_weeks": 2,
        "expected_gains": "+3-5 mph bat speed, better power transfer"
    },
    
    "torquer_no_separation": {
        "primary_drills": ["front_foot_elevated", "separation_drill"],
        "secondary_drills": ["resistance_band_hips"],
        "duration_weeks": 4,
        "expected_gains": "+5-8 mph bat speed from creating separation"
    },
    
    "poor_kinematic_sequence": {
        "primary_drills": ["front_foot_elevated", "resistance_band_hips"],
        "secondary_drills": [],
        "duration_weeks": 4,
        "expected_gains": "+5-8 mph bat speed, consistent power"
    },
    
    "stability_issues": {
        "primary_drills": ["eyes_closed_tee", "balance_finish"],
        "secondary_drills": [],
        "duration_weeks": 3,
        "expected_gains": "Better contact consistency, improved breaking ball recognition"
    },
    
    "tempo_too_slow": {
        "primary_drills": ["constraint_timing", "no_stride_tee"],
        "secondary_drills": [],
        "duration_weeks": 2,
        "expected_gains": "Better timing on fastballs, quicker trigger"
    },
    
    "tempo_too_fast": {
        "primary_drills": ["resistance_band_hips", "front_foot_elevated"],
        "secondary_drills": [],
        "duration_weeks": 3,
        "expected_gains": "+3-5 mph bat speed from elastic loading"
    }
}


# Utility functions
def get_drill(drill_id: str) -> Dict:
    """Get drill details by ID"""
    return DRILL_LIBRARY.get(drill_id, {})


def get_pattern_rule(pattern_id: str) -> Dict:
    """Get pattern rule by ID"""
    return PATTERN_RULES.get(pattern_id, {})


def get_prescription_rule(pattern_id: str) -> Dict:
    """Get prescription rule by pattern ID"""
    return PRESCRIPTION_RULES.get(pattern_id, {})
