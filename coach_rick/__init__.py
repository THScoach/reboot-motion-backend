"""
Coach Rick AI Engine
====================

AI-powered coaching system that generates personalized training feedback.

Components:
- Motor Profile Classifier (Spinner, Whipper, Torquer)
- Pattern Recognition Engine (diagnose mechanical issues)
- Drill Prescription System (map issues to drills)
- Conversational AI (GPT-4 integration for Coach Rick's voice)

Author: Builder 2
Date: 2024-12-24
Deadline: 2025-01-07
"""

__version__ = "1.0.0"
__author__ = "Builder 2"

from .motor_profile_classifier import MotorProfileClassifier, classify_motor_profile
from .pattern_recognition import PatternRecognitionEngine
from .knowledge_base import DRILL_LIBRARY, PRESCRIPTION_RULES, PATTERN_RULES
from .drill_prescription import DrillPrescriptionEngine
from .conversational_ai import ConversationalAI

__all__ = [
    'MotorProfileClassifier',
    'classify_motor_profile',
    'PatternRecognitionEngine',
    'DrillPrescriptionEngine',
    'ConversationalAI',
    'DRILL_LIBRARY',
    'PRESCRIPTION_RULES',
    'PATTERN_RULES'
]
