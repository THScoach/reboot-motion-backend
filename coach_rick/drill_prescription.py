"""
Drill Prescription Engine
=========================

Maps diagnosed mechanical issues to specific training drills.

Takes pattern recognition results and prescribes:
- Primary drills (most important)
- Secondary drills (supplementary)
- Weekly training schedule
- Expected gains & timeline

Author: Builder 2
Date: 2024-12-24
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta

try:
    from .knowledge_base import DRILL_LIBRARY, PRESCRIPTION_RULES
    from .pattern_recognition import PatternMatch
except ImportError:
    from knowledge_base import DRILL_LIBRARY, PRESCRIPTION_RULES
    from pattern_recognition import PatternMatch


@dataclass
class DrillPrescription:
    """Complete drill prescription for a player"""
    diagnosed_issue: str
    pattern_id: str
    drills: List[Dict]
    duration_weeks: int
    expected_gains: str
    weekly_schedule: Dict[str, List[Dict]]
    created_at: datetime


class DrillPrescriptionEngine:
    """
    Drill Prescription Engine for mapping issues to training plans.
    
    Takes pattern recognition results and creates actionable training plans
    with specific drills, schedules, and expected outcomes.
    """
    
    def __init__(self):
        """Initialize drill prescription engine"""
        self.drill_library = DRILL_LIBRARY
        self.prescription_rules = PRESCRIPTION_RULES
    
    def prescribe(self, primary_pattern: PatternMatch) -> DrillPrescription:
        """
        Create drill prescription from primary pattern.
        
        Args:
            primary_pattern: Primary mechanical issue identified
        
        Returns:
            DrillPrescription with complete training plan
        """
        pattern_id = primary_pattern.pattern_id
        
        # Get prescription rule for this pattern
        if pattern_id not in self.prescription_rules:
            return self._default_prescription(primary_pattern)
        
        rule = self.prescription_rules[pattern_id]
        
        # Build drill list
        prescribed_drills = []
        
        # Add primary drills
        for drill_id in rule['primary_drills']:
            if drill_id in self.drill_library:
                drill = self.drill_library[drill_id].copy()
                drill['drill_id'] = drill_id
                drill['priority'] = 'PRIMARY'
                prescribed_drills.append(drill)
        
        # Add secondary drills
        for drill_id in rule.get('secondary_drills', []):
            if drill_id in self.drill_library:
                drill = self.drill_library[drill_id].copy()
                drill['drill_id'] = drill_id
                drill['priority'] = 'SECONDARY'
                prescribed_drills.append(drill)
        
        # Generate weekly schedule
        weekly_schedule = self._generate_weekly_schedule(prescribed_drills)
        
        return DrillPrescription(
            diagnosed_issue=primary_pattern.diagnosis,
            pattern_id=pattern_id,
            drills=prescribed_drills,
            duration_weeks=rule['duration_weeks'],
            expected_gains=rule['expected_gains'],
            weekly_schedule=weekly_schedule,
            created_at=datetime.utcnow()
        )
    
    def prescribe_multi(self, patterns: List[PatternMatch]) -> List[DrillPrescription]:
        """
        Create prescriptions for multiple patterns.
        
        Args:
            patterns: List of patterns (sorted by priority)
        
        Returns:
            List of DrillPrescription objects
        """
        prescriptions = []
        
        for pattern in patterns[:3]:  # Top 3 issues max
            prescription = self.prescribe(pattern)
            prescriptions.append(prescription)
        
        return prescriptions
    
    def _generate_weekly_schedule(self, drills: List[Dict]) -> Dict[str, List[Dict]]:
        """
        Generate weekly training schedule from drill list.
        
        Args:
            drills: List of prescribed drills
        
        Returns:
            Dictionary mapping day name to list of drills
        """
        schedule = {
            "Monday": [],
            "Tuesday": [],
            "Wednesday": [],
            "Thursday": [],
            "Friday": [],
            "Saturday": [],
            "Sunday": []
        }
        
        for drill in drills:
            frequency = drill.get('frequency', '').lower()
            
            if 'daily' in frequency or 'always' in frequency:
                # Add to every day
                for day in schedule.keys():
                    schedule[day].append({
                        "drill_id": drill.get('drill_id'),
                        "drill_name": drill['drill_name'],
                        "volume": drill['volume'],
                        "priority": drill.get('priority', 'PRIMARY')
                    })
            
            elif '3x' in frequency or '3 times' in frequency:
                # Monday, Wednesday, Friday
                for day in ["Monday", "Wednesday", "Friday"]:
                    schedule[day].append({
                        "drill_id": drill.get('drill_id'),
                        "drill_name": drill['drill_name'],
                        "volume": drill['volume'],
                        "priority": drill.get('priority', 'PRIMARY')
                    })
            
            elif '2x' in frequency or '2 times' in frequency:
                # Tuesday, Thursday
                for day in ["Tuesday", "Thursday"]:
                    schedule[day].append({
                        "drill_id": drill.get('drill_id'),
                        "drill_name": drill['drill_name'],
                        "volume": drill['volume'],
                        "priority": drill.get('priority', 'PRIMARY')
                    })
            
            elif 'weekly' in frequency or 'week' in frequency:
                # Saturday only
                schedule["Saturday"].append({
                    "drill_id": drill.get('drill_id'),
                    "drill_name": drill['drill_name'],
                    "volume": drill['volume'],
                    "priority": drill.get('priority', 'PRIMARY')
                })
        
        return schedule
    
    def _default_prescription(self, pattern: PatternMatch) -> DrillPrescription:
        """
        Create default prescription when no specific rule exists.
        
        Args:
            pattern: Pattern to create prescription for
        
        Returns:
            Default DrillPrescription
        """
        # Use general drills
        default_drill = self.drill_library.get('no_stride_tee', {})
        default_drill['drill_id'] = 'no_stride_tee'
        default_drill['priority'] = 'PRIMARY'
        
        return DrillPrescription(
            diagnosed_issue=pattern.diagnosis,
            pattern_id=pattern.pattern_id,
            drills=[default_drill],
            duration_weeks=2,
            expected_gains="Improved swing consistency and mechanics",
            weekly_schedule=self._generate_weekly_schedule([default_drill]),
            created_at=datetime.utcnow()
        )
    
    def format_prescription_summary(self, prescription: DrillPrescription) -> str:
        """
        Format prescription as readable summary.
        
        Args:
            prescription: DrillPrescription to format
        
        Returns:
            Formatted string summary
        """
        lines = []
        lines.append("=" * 70)
        lines.append("DRILL PRESCRIPTION")
        lines.append("=" * 70)
        lines.append("")
        
        lines.append(f"ISSUE: {prescription.diagnosed_issue}")
        lines.append(f"DURATION: {prescription.duration_weeks} weeks")
        lines.append(f"EXPECTED GAINS: {prescription.expected_gains}")
        lines.append("")
        
        lines.append("PRESCRIBED DRILLS:")
        for i, drill in enumerate(prescription.drills, 1):
            priority_marker = "🔴" if drill['priority'] == 'PRIMARY' else "🔵"
            lines.append(f"{i}. {priority_marker} {drill['drill_name']}")
            lines.append(f"   Category: {drill['category']}")
            lines.append(f"   Volume: {drill['volume']}")
            lines.append(f"   Frequency: {drill['frequency']}")
            if drill.get('coaching_cues'):
                lines.append(f"   Key Cues:")
                for cue in drill['coaching_cues'][:2]:
                    lines.append(f"     • {cue}")
            lines.append("")
        
        lines.append("WEEKLY SCHEDULE:")
        for day, drills in prescription.weekly_schedule.items():
            if drills:
                lines.append(f"  {day}:")
                for drill in drills:
                    lines.append(f"    • {drill['drill_name']} - {drill['volume']}")
        
        lines.append("")
        lines.append("=" * 70)
        
        return "\n".join(lines)


# Example usage and testing
if __name__ == "__main__":
    import sys
    sys.path.insert(0, '/home/user/webapp')
    
    from coach_rick.motor_profile_classifier import classify_motor_profile
    from coach_rick.pattern_recognition import PatternRecognitionEngine
    
    # Test case: Spinner with lead arm bent
    spinner_data = {
        "kinematic_sequence": {
            "torso_peak_ms": 145,
            "arms_peak_ms": 160,
            "bat_peak_ms": 173,
            "grade": "B"
        },
        "tempo": {"ratio": 2.1},
        "stability": {"score": 92},
        "bat_speed": 82
    }
    
    # Step 1: Classify motor profile
    motor_profile_result = classify_motor_profile(spinner_data)
    
    # Step 2: Identify patterns
    pattern_engine = PatternRecognitionEngine()
    patterns = pattern_engine.analyze(spinner_data, motor_profile_result.profile)
    
    # Step 3: Prescribe drills
    prescription_engine = DrillPrescriptionEngine()
    
    if patterns:
        primary_pattern = patterns[0]
        prescription = prescription_engine.prescribe(primary_pattern)
        
        print("\n" + "=" * 70)
        print("DRILL PRESCRIPTION ENGINE TEST")
        print("=" * 70)
        print(f"\nMotor Profile: {motor_profile_result.profile}")
        print(f"Primary Issue: {primary_pattern.diagnosis}")
        print()
        
        print(prescription_engine.format_prescription_summary(prescription))
        
        # Test multiple prescriptions
        all_prescriptions = prescription_engine.prescribe_multi(patterns)
        print(f"\nTotal Prescriptions: {len(all_prescriptions)}")
        for i, p in enumerate(all_prescriptions, 1):
            print(f"  {i}. {p.diagnosed_issue} → {len(p.drills)} drills for {p.duration_weeks} weeks")
    else:
        print("No patterns detected")
