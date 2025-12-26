"""
PRIORITY 14: PROGRESS TRACKING SYSTEM
======================================

Track athlete improvement over time with session history, metrics comparison,
trend analysis, and achievement milestones.

Features:
- Session history with complete analysis results
- Metrics comparison (before/after, trends)
- Goal setting and tracking
- Milestone detection
- Achievement system
- Progress visualization data
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from enum import Enum
import json
import statistics


class MetricType(Enum):
    """Types of trackable metrics"""
    GROUND_SCORE = "ground_score"
    ENGINE_SCORE = "engine_score"
    WEAPON_SCORE = "weapon_score"
    OVERALL_EFFICIENCY = "overall_efficiency"
    BAT_SPEED_PREDICTED = "bat_speed_predicted"
    BAT_SPEED_ACTUAL = "bat_speed_actual"
    GAP_TO_CAPACITY = "gap_to_capacity"
    MOTOR_PREFERENCE_CONFIDENCE = "motor_preference_confidence"


class GoalStatus(Enum):
    """Goal achievement status"""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    ACHIEVED = "achieved"
    EXCEEDED = "exceeded"


class MilestoneType(Enum):
    """Types of achievement milestones"""
    FIRST_ANALYSIS = "first_analysis"
    MOTOR_PREFERENCE_IDENTIFIED = "motor_preference_identified"
    SCORE_IMPROVEMENT_10 = "score_improvement_10"
    SCORE_IMPROVEMENT_20 = "score_improvement_20"
    BAT_SPEED_GAIN_5 = "bat_speed_gain_5"
    BAT_SPEED_GAIN_10 = "bat_speed_gain_10"
    CONSISTENCY_STREAK_5 = "consistency_streak_5"
    CONSISTENCY_STREAK_10 = "consistency_streak_10"
    ALL_SCORES_ABOVE_70 = "all_scores_above_70"
    ALL_SCORES_ABOVE_80 = "all_scores_above_80"
    CAPACITY_80_PERCENT = "capacity_80_percent"
    CAPACITY_90_PERCENT = "capacity_90_percent"


@dataclass
class TrainingSession:
    """Complete training session with analysis results"""
    session_id: str
    athlete_id: str
    athlete_name: str
    session_date: datetime
    
    # Input data
    ground_score: int
    engine_score: int
    weapon_score: int
    height_inches: float
    wingspan_inches: Optional[float]
    weight_lbs: float
    age: int
    bat_weight_oz: int
    actual_bat_speed_mph: Optional[float]
    
    # Analysis results (from Priority 9+10+11)
    motor_preference: str
    motor_preference_confidence: float
    ground_score_adjusted: int
    engine_score_adjusted: int
    weapon_score_adjusted: int
    overall_efficiency: float
    bat_speed_capacity_midpoint: float
    predicted_bat_speed: float
    gap_to_capacity_max: float
    
    # Correction plan summary
    issues_count: int
    drills_count: int
    timeline_weeks: int
    expected_gain_mph: float
    
    # Notes and tags
    notes: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        data = asdict(self)
        data['session_date'] = self.session_date.isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'TrainingSession':
        """Create from dictionary"""
        data['session_date'] = datetime.fromisoformat(data['session_date'])
        return cls(**data)


@dataclass
class Goal:
    """Training goal with target metrics"""
    goal_id: str
    athlete_id: str
    created_date: datetime
    target_date: Optional[datetime]
    
    # Goal details
    metric_type: MetricType
    current_value: float
    target_value: float
    
    # Progress tracking
    status: GoalStatus
    progress_percent: float
    achieved_date: Optional[datetime] = None
    
    # Description
    title: str = ""
    description: str = ""
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        data = asdict(self)
        data['created_date'] = self.created_date.isoformat()
        data['target_date'] = self.target_date.isoformat() if self.target_date else None
        data['achieved_date'] = self.achieved_date.isoformat() if self.achieved_date else None
        data['metric_type'] = self.metric_type.value
        data['status'] = self.status.value
        return data


@dataclass
class Milestone:
    """Achievement milestone"""
    milestone_id: str
    athlete_id: str
    milestone_type: MilestoneType
    achieved_date: datetime
    session_id: str
    
    # Details
    title: str
    description: str
    icon: str
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        data = asdict(self)
        data['achieved_date'] = self.achieved_date.isoformat()
        data['milestone_type'] = self.milestone_type.value
        return data


class ProgressTracker:
    """
    Main progress tracking system
    Manages session history, goals, and milestones
    """
    
    def __init__(self):
        """Initialize progress tracker"""
        self.sessions: Dict[str, List[TrainingSession]] = {}  # athlete_id -> sessions
        self.goals: Dict[str, List[Goal]] = {}  # athlete_id -> goals
        self.milestones: Dict[str, List[Milestone]] = {}  # athlete_id -> milestones
    
    
    # ========================================
    # SESSION MANAGEMENT
    # ========================================
    
    def add_session(self, session: TrainingSession) -> None:
        """Add a training session"""
        if session.athlete_id not in self.sessions:
            self.sessions[session.athlete_id] = []
        
        self.sessions[session.athlete_id].append(session)
        
        # Sort by date (most recent first)
        self.sessions[session.athlete_id].sort(
            key=lambda s: s.session_date,
            reverse=True
        )
        
        # Check for milestones
        self._check_milestones(session)
        
        # Update goal progress
        self._update_goal_progress(session.athlete_id)
    
    
    def get_session(self, athlete_id: str, session_id: str) -> Optional[TrainingSession]:
        """Get specific session"""
        sessions = self.sessions.get(athlete_id, [])
        for session in sessions:
            if session.session_id == session_id:
                return session
        return None
    
    
    def get_sessions(
        self,
        athlete_id: str,
        limit: int = 50,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[TrainingSession]:
        """Get session history for athlete"""
        sessions = self.sessions.get(athlete_id, [])
        
        # Filter by date range
        if start_date:
            sessions = [s for s in sessions if s.session_date >= start_date]
        if end_date:
            sessions = [s for s in sessions if s.session_date <= end_date]
        
        return sessions[:limit]
    
    
    def get_latest_session(self, athlete_id: str) -> Optional[TrainingSession]:
        """Get most recent session"""
        sessions = self.sessions.get(athlete_id, [])
        return sessions[0] if sessions else None
    
    
    # ========================================
    # METRICS COMPARISON
    # ========================================
    
    def compare_sessions(
        self,
        athlete_id: str,
        session_id_1: str,
        session_id_2: str
    ) -> Dict:
        """Compare two sessions"""
        session1 = self.get_session(athlete_id, session_id_1)
        session2 = self.get_session(athlete_id, session_id_2)
        
        if not session1 or not session2:
            return {}
        
        return {
            'session_1': {
                'session_id': session1.session_id,
                'date': session1.session_date.isoformat(),
                'ground_score': session1.ground_score_adjusted,
                'engine_score': session1.engine_score_adjusted,
                'weapon_score': session1.weapon_score_adjusted,
                'overall_efficiency': session1.overall_efficiency,
                'predicted_bat_speed': session1.predicted_bat_speed,
                'actual_bat_speed': session1.actual_bat_speed_mph,
                'gap_to_capacity': session1.gap_to_capacity_max,
            },
            'session_2': {
                'session_id': session2.session_id,
                'date': session2.session_date.isoformat(),
                'ground_score': session2.ground_score_adjusted,
                'engine_score': session2.engine_score_adjusted,
                'weapon_score': session2.weapon_score_adjusted,
                'overall_efficiency': session2.overall_efficiency,
                'predicted_bat_speed': session2.predicted_bat_speed,
                'actual_bat_speed': session2.actual_bat_speed_mph,
                'gap_to_capacity': session2.gap_to_capacity_max,
            },
            'changes': {
                'ground_score': session2.ground_score_adjusted - session1.ground_score_adjusted,
                'engine_score': session2.engine_score_adjusted - session1.engine_score_adjusted,
                'weapon_score': session2.weapon_score_adjusted - session1.weapon_score_adjusted,
                'overall_efficiency': session2.overall_efficiency - session1.overall_efficiency,
                'predicted_bat_speed': session2.predicted_bat_speed - session1.predicted_bat_speed,
                'gap_to_capacity': session2.gap_to_capacity_max - session1.gap_to_capacity_max,
            },
            'improvements': self._calculate_improvements(session1, session2)
        }
    
    
    def get_progress_summary(self, athlete_id: str) -> Dict:
        """Get overall progress summary"""
        sessions = self.get_sessions(athlete_id)
        
        if not sessions:
            return {'error': 'No sessions found'}
        
        if len(sessions) == 1:
            return {
                'total_sessions': 1,
                'first_session_date': sessions[0].session_date.isoformat(),
                'latest_session_date': sessions[0].session_date.isoformat(),
                'message': 'Need at least 2 sessions to track progress'
            }
        
        first_session = sessions[-1]  # Oldest (last in reversed list)
        latest_session = sessions[0]  # Most recent (first in reversed list)
        
        return {
            'total_sessions': len(sessions),
            'first_session_date': first_session.session_date.isoformat(),
            'latest_session_date': latest_session.session_date.isoformat(),
            'days_tracked': (latest_session.session_date - first_session.session_date).days,
            
            'current_metrics': {
                'ground_score': latest_session.ground_score_adjusted,
                'engine_score': latest_session.engine_score_adjusted,
                'weapon_score': latest_session.weapon_score_adjusted,
                'overall_efficiency': latest_session.overall_efficiency,
                'predicted_bat_speed': latest_session.predicted_bat_speed,
                'motor_preference': latest_session.motor_preference,
            },
            
            'improvements_from_start': {
                'ground_score': latest_session.ground_score_adjusted - first_session.ground_score_adjusted,
                'engine_score': latest_session.engine_score_adjusted - first_session.engine_score_adjusted,
                'weapon_score': latest_session.weapon_score_adjusted - first_session.weapon_score_adjusted,
                'overall_efficiency': latest_session.overall_efficiency - first_session.overall_efficiency,
                'predicted_bat_speed': latest_session.predicted_bat_speed - first_session.predicted_bat_speed,
            },
            
            'trends': self._calculate_trends(sessions),
            'consistency_score': self._calculate_consistency(sessions),
        }
    
    
    def get_metric_history(
        self,
        athlete_id: str,
        metric_type: MetricType
    ) -> List[Dict]:
        """Get history of a specific metric"""
        sessions = self.get_sessions(athlete_id)
        
        history = []
        for session in reversed(sessions):  # Chronological order
            value = self._get_metric_value(session, metric_type)
            history.append({
                'date': session.session_date.isoformat(),
                'session_id': session.session_id,
                'value': value
            })
        
        return history
    
    
    # ========================================
    # GOAL MANAGEMENT
    # ========================================
    
    def add_goal(self, goal: Goal) -> None:
        """Add a training goal"""
        if goal.athlete_id not in self.goals:
            self.goals[goal.athlete_id] = []
        
        self.goals[goal.athlete_id].append(goal)
    
    
    def get_goals(self, athlete_id: str, active_only: bool = False) -> List[Goal]:
        """Get athlete's goals"""
        goals = self.goals.get(athlete_id, [])
        
        if active_only:
            goals = [g for g in goals if g.status in [GoalStatus.NOT_STARTED, GoalStatus.IN_PROGRESS]]
        
        return goals
    
    
    def _update_goal_progress(self, athlete_id: str) -> None:
        """Update progress on all active goals"""
        latest_session = self.get_latest_session(athlete_id)
        if not latest_session:
            return
        
        goals = self.get_goals(athlete_id, active_only=True)
        
        for goal in goals:
            # Get current value from latest session
            current_value = self._get_metric_value(latest_session, goal.metric_type)
            
            # Calculate progress
            if goal.current_value == goal.target_value:
                progress = 100.0
            else:
                progress = min(100.0, max(0.0,
                    (current_value - goal.current_value) / 
                    (goal.target_value - goal.current_value) * 100
                ))
            
            goal.progress_percent = progress
            
            # Update status
            if current_value >= goal.target_value:
                if current_value > goal.target_value:
                    goal.status = GoalStatus.EXCEEDED
                else:
                    goal.status = GoalStatus.ACHIEVED
                goal.achieved_date = latest_session.session_date
            elif progress > 0:
                goal.status = GoalStatus.IN_PROGRESS
    
    
    # ========================================
    # MILESTONE MANAGEMENT
    # ========================================
    
    def _check_milestones(self, session: TrainingSession) -> None:
        """Check for achieved milestones"""
        athlete_id = session.athlete_id
        
        if athlete_id not in self.milestones:
            self.milestones[athlete_id] = []
        
        achieved_types = {m.milestone_type for m in self.milestones[athlete_id]}
        
        # Check each milestone type
        milestones_to_add = []
        
        # First analysis
        if MilestoneType.FIRST_ANALYSIS not in achieved_types:
            if len(self.sessions.get(athlete_id, [])) == 1:
                milestones_to_add.append(self._create_milestone(
                    athlete_id, session, MilestoneType.FIRST_ANALYSIS,
                    "First Analysis Complete!",
                    "Started your journey to better swing mechanics",
                    "🎯"
                ))
        
        # Motor preference identified
        if MilestoneType.MOTOR_PREFERENCE_IDENTIFIED not in achieved_types:
            if session.motor_preference_confidence >= 0.8:
                milestones_to_add.append(self._create_milestone(
                    athlete_id, session, MilestoneType.MOTOR_PREFERENCE_IDENTIFIED,
                    "Motor Preference Identified!",
                    f"Confirmed as a {session.motor_preference.upper()}",
                    "🧬"
                ))
        
        # Score improvements
        sessions = self.get_sessions(athlete_id)
        if len(sessions) >= 2:
            first = sessions[-1]
            latest = sessions[0]
            
            avg_improvement = (
                (latest.ground_score_adjusted - first.ground_score_adjusted) +
                (latest.engine_score_adjusted - first.engine_score_adjusted) +
                (latest.weapon_score_adjusted - first.weapon_score_adjusted)
            ) / 3
            
            if avg_improvement >= 20 and MilestoneType.SCORE_IMPROVEMENT_20 not in achieved_types:
                milestones_to_add.append(self._create_milestone(
                    athlete_id, session, MilestoneType.SCORE_IMPROVEMENT_20,
                    "Major Improvement!",
                    "Average score increased by 20+ points",
                    "📈"
                ))
            elif avg_improvement >= 10 and MilestoneType.SCORE_IMPROVEMENT_10 not in achieved_types:
                milestones_to_add.append(self._create_milestone(
                    athlete_id, session, MilestoneType.SCORE_IMPROVEMENT_10,
                    "Solid Progress!",
                    "Average score increased by 10+ points",
                    "📊"
                ))
        
        # All scores above thresholds
        if (session.ground_score_adjusted >= 80 and 
            session.engine_score_adjusted >= 80 and 
            session.weapon_score_adjusted >= 80):
            if MilestoneType.ALL_SCORES_ABOVE_80 not in achieved_types:
                milestones_to_add.append(self._create_milestone(
                    athlete_id, session, MilestoneType.ALL_SCORES_ABOVE_80,
                    "Excellence Achieved!",
                    "All scores above 80!",
                    "⭐"
                ))
        elif (session.ground_score_adjusted >= 70 and 
              session.engine_score_adjusted >= 70 and 
              session.weapon_score_adjusted >= 70):
            if MilestoneType.ALL_SCORES_ABOVE_70 not in achieved_types:
                milestones_to_add.append(self._create_milestone(
                    athlete_id, session, MilestoneType.ALL_SCORES_ABOVE_70,
                    "Solid Mechanics!",
                    "All scores above 70!",
                    "✨"
                ))
        
        # Add new milestones
        self.milestones[athlete_id].extend(milestones_to_add)
    
    
    def get_milestones(self, athlete_id: str) -> List[Milestone]:
        """Get athlete's milestones"""
        return self.milestones.get(athlete_id, [])
    
    
    def _create_milestone(
        self,
        athlete_id: str,
        session: TrainingSession,
        milestone_type: MilestoneType,
        title: str,
        description: str,
        icon: str
    ) -> Milestone:
        """Create a milestone"""
        import uuid
        return Milestone(
            milestone_id=str(uuid.uuid4()),
            athlete_id=athlete_id,
            milestone_type=milestone_type,
            achieved_date=session.session_date,
            session_id=session.session_id,
            title=title,
            description=description,
            icon=icon
        )
    
    
    # ========================================
    # HELPER METHODS
    # ========================================
    
    def _get_metric_value(self, session: TrainingSession, metric_type: MetricType) -> float:
        """Extract metric value from session"""
        metric_map = {
            MetricType.GROUND_SCORE: session.ground_score_adjusted,
            MetricType.ENGINE_SCORE: session.engine_score_adjusted,
            MetricType.WEAPON_SCORE: session.weapon_score_adjusted,
            MetricType.OVERALL_EFFICIENCY: session.overall_efficiency,
            MetricType.BAT_SPEED_PREDICTED: session.predicted_bat_speed,
            MetricType.BAT_SPEED_ACTUAL: session.actual_bat_speed_mph or 0,
            MetricType.GAP_TO_CAPACITY: session.gap_to_capacity_max,
            MetricType.MOTOR_PREFERENCE_CONFIDENCE: session.motor_preference_confidence,
        }
        return metric_map.get(metric_type, 0)
    
    
    def _calculate_improvements(self, session1: TrainingSession, session2: TrainingSession) -> List[str]:
        """Calculate improvement messages"""
        improvements = []
        
        # Score improvements
        ground_delta = session2.ground_score_adjusted - session1.ground_score_adjusted
        if ground_delta > 0:
            improvements.append(f"Ground score improved by {ground_delta} points")
        
        engine_delta = session2.engine_score_adjusted - session1.engine_score_adjusted
        if engine_delta > 0:
            improvements.append(f"Engine score improved by {engine_delta} points")
        
        weapon_delta = session2.weapon_score_adjusted - session1.weapon_score_adjusted
        if weapon_delta > 0:
            improvements.append(f"Weapon score improved by {weapon_delta} points")
        
        # Bat speed
        speed_delta = session2.predicted_bat_speed - session1.predicted_bat_speed
        if speed_delta > 0:
            improvements.append(f"Predicted bat speed increased by {speed_delta:.1f} mph")
        
        # Gap reduction
        gap_delta = session1.gap_to_capacity_max - session2.gap_to_capacity_max
        if gap_delta > 0:
            improvements.append(f"Gap to capacity reduced by {gap_delta:.1f} mph")
        
        return improvements if improvements else ["No improvements detected"]
    
    
    def _calculate_trends(self, sessions: List[TrainingSession]) -> Dict:
        """Calculate metric trends"""
        if len(sessions) < 3:
            return {}
        
        # Get values in chronological order
        sessions_chrono = list(reversed(sessions))
        
        ground_scores = [s.ground_score_adjusted for s in sessions_chrono]
        engine_scores = [s.engine_score_adjusted for s in sessions_chrono]
        weapon_scores = [s.weapon_score_adjusted for s in sessions_chrono]
        
        return {
            'ground_score_trend': self._calculate_trend(ground_scores),
            'engine_score_trend': self._calculate_trend(engine_scores),
            'weapon_score_trend': self._calculate_trend(weapon_scores),
        }
    
    
    def _calculate_trend(self, values: List[float]) -> str:
        """Calculate trend direction"""
        if len(values) < 2:
            return 'insufficient_data'
        
        # Simple linear trend
        first_half_avg = statistics.mean(values[:len(values)//2])
        second_half_avg = statistics.mean(values[len(values)//2:])
        
        diff = second_half_avg - first_half_avg
        
        if diff > 5:
            return 'improving'
        elif diff < -5:
            return 'declining'
        else:
            return 'stable'
    
    
    def _calculate_consistency(self, sessions: List[TrainingSession]) -> float:
        """Calculate consistency score (0-100)"""
        if len(sessions) < 3:
            return 0.0
        
        # Calculate standard deviation of overall efficiency
        efficiencies = [s.overall_efficiency for s in sessions]
        
        if len(efficiencies) < 2:
            return 0.0
        
        std_dev = statistics.stdev(efficiencies)
        
        # Lower std_dev = higher consistency
        # Convert to 0-100 scale (lower std_dev is better)
        consistency = max(0, 100 - (std_dev * 10))
        
        return round(consistency, 1)


# Global progress tracker instance
_progress_tracker_instance = None

def get_progress_tracker() -> ProgressTracker:
    """Get or create global progress tracker instance"""
    global _progress_tracker_instance
    if _progress_tracker_instance is None:
        _progress_tracker_instance = ProgressTracker()
    return _progress_tracker_instance


# ========================================
# TESTING & EXAMPLES
# ========================================

if __name__ == "__main__":
    from datetime import datetime, timedelta
    import uuid
    
    tracker = ProgressTracker()
    
    print("=" * 80)
    print("PROGRESS TRACKING SYSTEM - PRIORITY 14")
    print("=" * 80)
    
    # Simulate Eric Williams progress over 8 weeks
    athlete_id = "eric_williams_001"
    athlete_name = "Eric Williams"
    
    base_date = datetime.now() - timedelta(weeks=8)
    
    # Session 1 (Week 0 - Initial)
    session1 = TrainingSession(
        session_id=str(uuid.uuid4()),
        athlete_id=athlete_id,
        athlete_name=athlete_name,
        session_date=base_date,
        ground_score=38, engine_score=58, weapon_score=55,
        height_inches=68, wingspan_inches=69, weight_lbs=190, age=33, bat_weight_oz=30,
        actual_bat_speed_mph=67.0,
        motor_preference="spinner", motor_preference_confidence=0.857,
        ground_score_adjusted=72, engine_score_adjusted=58, weapon_score_adjusted=55,
        overall_efficiency=60.7, bat_speed_capacity_midpoint=76.1,
        predicted_bat_speed=61.2, gap_to_capacity_max=13.4,
        issues_count=2, drills_count=4, timeline_weeks=6, expected_gain_mph=11.0
    )
    tracker.add_session(session1)
    
    # Session 2 (Week 2 - Some improvement)
    session2 = TrainingSession(
        session_id=str(uuid.uuid4()),
        athlete_id=athlete_id,
        athlete_name=athlete_name,
        session_date=base_date + timedelta(weeks=2),
        ground_score=45, engine_score=62, weapon_score=58,
        height_inches=68, wingspan_inches=69, weight_lbs=190, age=33, bat_weight_oz=30,
        actual_bat_speed_mph=69.0,
        motor_preference="spinner", motor_preference_confidence=0.890,
        ground_score_adjusted=78, engine_score_adjusted=62, weapon_score_adjusted=58,
        overall_efficiency=65.3, bat_speed_capacity_midpoint=76.1,
        predicted_bat_speed=64.8, gap_to_capacity_max=9.9,
        issues_count=1, drills_count=3, timeline_weeks=4, expected_gain_mph=7.2
    )
    tracker.add_session(session2)
    
    # Session 3 (Week 4 - Continued progress)
    session3 = TrainingSession(
        session_id=str(uuid.uuid4()),
        athlete_id=athlete_id,
        athlete_name=athlete_name,
        session_date=base_date + timedelta(weeks=4),
        ground_score=52, engine_score=68, weapon_score=63,
        height_inches=68, wingspan_inches=69, weight_lbs=190, age=33, bat_weight_oz=30,
        actual_bat_speed_mph=72.0,
        motor_preference="spinner", motor_preference_confidence=0.920,
        ground_score_adjusted=84, engine_score_adjusted=68, weapon_score_adjusted=63,
        overall_efficiency=71.7, bat_speed_capacity_midpoint=76.1,
        predicted_bat_speed=69.1, gap_to_capacity_max=5.8,
        issues_count=0, drills_count=2, timeline_weeks=2, expected_gain_mph=3.5
    )
    tracker.add_session(session3)
    
    # Get progress summary
    summary = tracker.get_progress_summary(athlete_id)
    
    print(f"\n📊 Progress Summary for {athlete_name}")
    print(f"   Total Sessions: {summary['total_sessions']}")
    print(f"   Days Tracked: {summary['days_tracked']}")
    print(f"   Consistency Score: {summary['consistency_score']:.1f}/100")
    
    print(f"\n📈 Current Metrics:")
    current = summary['current_metrics']
    print(f"   Ground: {current['ground_score']}")
    print(f"   Engine: {current['engine_score']}")
    print(f"   Weapon: {current['weapon_score']}")
    print(f"   Efficiency: {current['overall_efficiency']:.1f}%")
    print(f"   Predicted Bat Speed: {current['predicted_bat_speed']:.1f} mph")
    
    print(f"\n🎯 Improvements from Start:")
    improvements = summary['improvements_from_start']
    print(f"   Ground: +{improvements['ground_score']}")
    print(f"   Engine: +{improvements['engine_score']}")
    print(f"   Weapon: +{improvements['weapon_score']}")
    print(f"   Bat Speed: +{improvements['predicted_bat_speed']:.1f} mph")
    
    print(f"\n🏆 Milestones Achieved: {len(tracker.get_milestones(athlete_id))}")
    for milestone in tracker.get_milestones(athlete_id):
        print(f"   {milestone.icon} {milestone.title}")
    
    print("\n✅ Progress Tracking System Ready!")
