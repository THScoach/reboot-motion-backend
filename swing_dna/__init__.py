"""
Swing DNA Analysis Module
=========================

Advanced biomechanics analysis for baseball swing optimization.
Processes CSV data (momentum-energy.csv + inverse-kinematics.csv) to:
- Diagnose swing patterns (4 types)
- Calculate efficiency metrics
- Predict ball outcomes
- Generate 6-week training plans

Author: Builder 2
Date: 2024-12-25
Version: 1.0.0
"""

from .csv_parser import CSVParser
from .pattern_recognition import PatternRecognizer
from .efficiency_calculator import EfficiencyCalculator
from .ball_outcome_predictor import BallOutcomePredictor
from .training_plan_generator import TrainingPlanGenerator
from .protocols import PROTOCOLS

__version__ = "1.0.0"
__all__ = [
    "CSVParser",
    "PatternRecognizer",
    "EfficiencyCalculator",
    "BallOutcomePredictor",
    "TrainingPlanGenerator",
    "PROTOCOLS"
]
