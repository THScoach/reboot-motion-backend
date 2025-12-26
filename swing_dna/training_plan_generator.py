"""
Training Plan Generator for Swing DNA Analysis
Generates personalized 6-week training plans based on swing pattern diagnosis

Author: Coach Rick AI
Date: 2025-12-25
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from .pattern_recognition import PatternDiagnosis
from .protocols import PROTOCOLS, PROTOCOL_MAPPING


@dataclass
class WeeklyPhase:
    """Weekly training phase"""
    week_number: int
    focus: str
    drills: List[Dict[str, Any]]
    expected_change: str
    downstream_effect: str
    validation_test: str
    duration_minutes: int = 45
    frequency_per_week: int = 4


@dataclass
class TrainingPlan:
    """Complete 6-week training plan"""
    athlete_name: str
    pattern: str
    severity: str
    primary_issue: str
    protocols_used: List[str]
    weeks: List[WeeklyPhase]
    total_weeks: int = 6
    created_at: str = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "athlete_name": self.athlete_name,
            "pattern": self.pattern,
            "severity": self.severity,
            "primary_issue": self.primary_issue,
            "protocols_used": self.protocols_used,
            "total_weeks": self.total_weeks,
            "created_at": self.created_at,
            "weeks": [
                {
                    "week_number": week.week_number,
                    "focus": week.focus,
                    "drills": week.drills,
                    "expected_change": week.expected_change,
                    "downstream_effect": week.downstream_effect,
                    "validation_test": week.validation_test,
                    "duration_minutes": week.duration_minutes,
                    "frequency_per_week": week.frequency_per_week
                }
                for week in self.weeks
            ]
        }


class TrainingPlanGenerator:
    """Generates 6-week training plans based on swing pattern diagnosis"""
    
    def __init__(self):
        self.protocols = PROTOCOLS
        self.protocol_mapping = PROTOCOL_MAPPING
    
    def generate_plan(
        self,
        athlete_name: str,
        pattern: PatternDiagnosis,
        metrics: Dict[str, float]
    ) -> TrainingPlan:
        """
        Generate complete 6-week training plan
        
        Args:
            athlete_name: Athlete's name
            pattern: Diagnosed swing pattern
            metrics: Biomechanical metrics
            
        Returns:
            Complete training plan with weekly phases
        """
        # Get protocols for this pattern
        primary_protocol_key = pattern.primary_protocol
        secondary_protocol_key = pattern.secondary_protocol
        
        primary_protocol = self.protocols.get(primary_protocol_key)
        secondary_protocol = self.protocols.get(secondary_protocol_key)
        
        if not primary_protocol:
            raise ValueError(f"Protocol {primary_protocol_key} not found")
        
        # Build weekly phases
        weeks = []
        
        # Weeks 1-2: Primary protocol focus (weeks 1-2 from primary)
        for week_data in primary_protocol["weeks"][:2]:
            weeks.append(WeeklyPhase(
                week_number=len(weeks) + 1,
                focus=week_data["focus"],
                drills=week_data["drills"],
                expected_change=week_data["expected_change"],
                downstream_effect=week_data["downstream_effect"],
                validation_test=week_data["validation_test"]
            ))
        
        # Weeks 3-4: Layer in secondary protocol (weeks 3-4 from primary + secondary)
        if secondary_protocol:
            for i, week_data in enumerate(primary_protocol["weeks"][2:4]):
                # Combine primary and secondary drills
                combined_drills = week_data["drills"].copy()
                if i < len(secondary_protocol["weeks"]):
                    # Add 1-2 drills from secondary protocol
                    secondary_drills = secondary_protocol["weeks"][i]["drills"][:2]
                    combined_drills.extend(secondary_drills)
                
                weeks.append(WeeklyPhase(
                    week_number=len(weeks) + 1,
                    focus=f"{week_data['focus']} + {secondary_protocol['weeks'][i]['focus'] if i < len(secondary_protocol['weeks']) else 'Integration'}",
                    drills=combined_drills,
                    expected_change=week_data["expected_change"],
                    downstream_effect=week_data["downstream_effect"],
                    validation_test=week_data["validation_test"]
                ))
        else:
            # No secondary protocol - just continue primary
            for week_data in primary_protocol["weeks"][2:4]:
                weeks.append(WeeklyPhase(
                    week_number=len(weeks) + 1,
                    focus=week_data["focus"],
                    drills=week_data["drills"],
                    expected_change=week_data["expected_change"],
                    downstream_effect=week_data["downstream_effect"],
                    validation_test=week_data["validation_test"]
                ))
        
        # Weeks 5-6: Integration and live swings (always from PROTOCOL_5)
        integration_protocol = self.protocols.get("PROTOCOL_5")
        if integration_protocol and len(integration_protocol["weeks"]) >= 2:
            for week_data in integration_protocol["weeks"][:2]:
                weeks.append(WeeklyPhase(
                    week_number=len(weeks) + 1,
                    focus=week_data["focus"],
                    drills=week_data["drills"],
                    expected_change=week_data["expected_change"],
                    downstream_effect=week_data["downstream_effect"],
                    validation_test=week_data["validation_test"]
                ))
        
        # Ensure we have exactly 6 weeks
        while len(weeks) < 6:
            # Add maintenance week
            weeks.append(WeeklyPhase(
                week_number=len(weeks) + 1,
                focus="Maintain Gains",
                drills=[
                    {
                        "name": "Full Warm-up",
                        "sets": "1x",
                        "reps": "10 min",
                        "cue": "Review all previous drills"
                    },
                    {
                        "name": "Live Swings",
                        "sets": "3x",
                        "reps": "10 swings",
                        "cue": "Focus on quality over quantity"
                    }
                ],
                expected_change="Solidify movement patterns",
                downstream_effect="Maintain all previous gains",
                validation_test="Re-test all metrics"
            ))
        
        # Create training plan
        return TrainingPlan(
            athlete_name=athlete_name,
            pattern=pattern.type,
            severity=pattern.severity,
            primary_issue=pattern.root_cause,
            protocols_used=[primary_protocol_key] + ([secondary_protocol_key] if secondary_protocol_key else []),
            weeks=weeks[:6]  # Ensure exactly 6 weeks
        )
    
    def get_drill_summary(self, plan: TrainingPlan) -> Dict[str, Any]:
        """Get summary of all drills in the plan"""
        all_drills = []
        drill_names = set()
        
        for week in plan.weeks:
            for drill in week.drills:
                drill_name = drill.get("name", "")
                if drill_name and drill_name not in drill_names:
                    all_drills.append(drill)
                    drill_names.add(drill_name)
        
        return {
            "total_drills": len(all_drills),
            "drill_list": all_drills,
            "total_duration_hours": sum(w.duration_minutes for w in plan.weeks) / 60,
            "sessions_per_week": plan.weeks[0].frequency_per_week if plan.weeks else 4
        }
    
    def get_timeline(self, plan: TrainingPlan, start_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """Generate timeline with dates"""
        if start_date is None:
            start_date = datetime.now()
        
        timeline = []
        current_date = start_date
        
        for week in plan.weeks:
            week_end = current_date + timedelta(days=7)
            timeline.append({
                "week_number": week.week_number,
                "start_date": current_date.strftime("%Y-%m-%d"),
                "end_date": week_end.strftime("%Y-%m-%d"),
                "focus": week.focus,
                "sessions": week.frequency_per_week,
                "total_minutes": week.duration_minutes * week.frequency_per_week
            })
            current_date = week_end
        
        return timeline


def generate_training_plan(
    athlete_name: str,
    pattern: PatternDiagnosis,
    metrics: Dict[str, float]
) -> Dict[str, Any]:
    """
    Convenience function to generate training plan
    
    Args:
        athlete_name: Athlete's name
        pattern: Diagnosed swing pattern
        metrics: Biomechanical metrics
        
    Returns:
        Training plan as dictionary
    """
    generator = TrainingPlanGenerator()
    plan = generator.generate_plan(athlete_name, pattern, metrics)
    
    return {
        "training_plan": plan.to_dict(),
        "drill_summary": generator.get_drill_summary(plan),
        "timeline": generator.get_timeline(plan)
    }


# Testing
if __name__ == "__main__":
    print("\n" + "="*70)
    print("TRAINING PLAN GENERATOR - TEST")
    print("="*70 + "\n")
    
    # Mock swing pattern for testing
    from .pattern_recognition import PatternDiagnosis
    
    test_pattern = PatternDiagnosis(
        pattern="PATTERN_1_KNEE_LEAK",
        severity="CRITICAL",
        confidence=0.95,
        root_cause="Energy Leak at Lead Knee",
        primary_protocol="PROTOCOL_1",
        secondary_protocol="PROTOCOL_2",
        key_metrics={
            "lead_knee_angle": 30.5,
            "hip_angular_momentum": 2.10,
            "shoulder_hip_ratio": 8.68
        }
    )
    
    test_metrics = {
        "lead_knee_angle": 30.5,
        "hip_angular_momentum": 2.10,
        "shoulder_angular_momentum": 18.25,
        "bat_speed": 82.0
    }
    
    # Generate plan
    result = generate_training_plan("Eric Williams", test_pattern, test_metrics)
    
    print("✅ Training Plan Generated")
    print(f"   Pattern: {result['training_plan']['pattern']}")
    print(f"   Severity: {result['training_plan']['severity']}")
    print(f"   Protocols: {', '.join(result['training_plan']['protocols_used'])}")
    print(f"\n📋 Plan Overview:")
    print(f"   Total Weeks: {result['training_plan']['total_weeks']}")
    print(f"   Total Drills: {result['drill_summary']['total_drills']}")
    print(f"   Total Hours: {result['drill_summary']['total_duration_hours']:.1f}")
    print(f"   Sessions/Week: {result['drill_summary']['sessions_per_week']}")
    
    print(f"\n📅 Weekly Breakdown:")
    for week in result['training_plan']['weeks']:
        print(f"\n   Week {week['week_number']}: {week['focus']}")
        print(f"   • {len(week['drills'])} drills")
        print(f"   • Expected: {week['expected_change']}")
    
    print("\n" + "="*70)
    print("✅ TRAINING PLAN GENERATOR READY")
    print("="*70 + "\n")
