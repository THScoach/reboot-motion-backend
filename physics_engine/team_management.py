"""
PRIORITY 16: COACH DASHBOARD & TEAM MANAGEMENT
================================================

A comprehensive team management system for baseball coaches to:
- Manage multiple athletes and teams
- Compare athlete performance across the roster
- Assign training plans and drills
- Track team-wide progress and analytics
- Communicate with athletes

Data Models:
- Coach: Coach profile with credentials
- Team: Teams/groups of athletes
- Athlete: Individual athlete profile
- CoachNote: Communication and observations
- TrainingAssignment: Assigned drills and plans

Author: Reboot Motion Development Team
Date: 2025-12-24
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
from enum import Enum
import uuid


# ============================================================================
# ENUMERATIONS
# ============================================================================

class CoachRole(Enum):
    """Coach role levels"""
    HEAD_COACH = "head_coach"
    ASSISTANT_COACH = "assistant_coach"
    HITTING_COORDINATOR = "hitting_coordinator"
    STRENGTH_COACH = "strength_coach"


class TeamType(Enum):
    """Types of teams"""
    HIGH_SCHOOL = "high_school"
    COLLEGE = "college"
    PROFESSIONAL = "professional"
    TRAVEL = "travel"
    CLUB = "club"
    PRIVATE_TRAINING = "private_training"


class AthleteStatus(Enum):
    """Athlete status in team"""
    ACTIVE = "active"
    INJURED = "injured"
    INACTIVE = "inactive"
    GRADUATED = "graduated"


class AssignmentStatus(Enum):
    """Training assignment status"""
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    OVERDUE = "overdue"


# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class Coach:
    """Coach profile and credentials"""
    coach_id: str
    name: str
    email: str
    role: CoachRole
    organization: str
    created_date: datetime
    phone: Optional[str] = None
    bio: Optional[str] = None
    certifications: List[str] = field(default_factory=list)
    teams: List[str] = field(default_factory=list)  # team_ids
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'coach_id': self.coach_id,
            'name': self.name,
            'email': self.email,
            'role': self.role.value,
            'organization': self.organization,
            'created_date': self.created_date.isoformat(),
            'phone': self.phone,
            'bio': self.bio,
            'certifications': self.certifications,
            'teams': self.teams
        }


@dataclass
class Team:
    """Team/Group of athletes"""
    team_id: str
    name: str
    team_type: TeamType
    coach_id: str
    created_date: datetime
    season: str  # e.g., "2024 Spring", "2024-2025"
    description: Optional[str] = None
    athlete_ids: List[str] = field(default_factory=list)
    assistant_coach_ids: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'team_id': self.team_id,
            'name': self.name,
            'team_type': self.team_type.value,
            'coach_id': self.coach_id,
            'created_date': self.created_date.isoformat(),
            'season': self.season,
            'description': self.description,
            'athlete_ids': self.athlete_ids,
            'assistant_coach_ids': self.assistant_coach_ids,
            'total_athletes': len(self.athlete_ids)
        }


@dataclass
class Athlete:
    """Individual athlete profile"""
    athlete_id: str
    name: str
    email: str
    team_id: str
    date_of_birth: datetime
    height_inches: int
    wingspan_inches: int
    weight_lbs: int
    bat_weight_oz: int
    status: AthleteStatus
    created_date: datetime
    position: Optional[str] = None
    jersey_number: Optional[int] = None
    grad_year: Optional[int] = None
    parent_email: Optional[str] = None
    phone: Optional[str] = None
    notes: Optional[str] = None
    
    @property
    def age(self) -> int:
        """Calculate current age"""
        today = datetime.now()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'athlete_id': self.athlete_id,
            'name': self.name,
            'email': self.email,
            'team_id': self.team_id,
            'age': self.age,
            'height_inches': self.height_inches,
            'wingspan_inches': self.wingspan_inches,
            'weight_lbs': self.weight_lbs,
            'bat_weight_oz': self.bat_weight_oz,
            'status': self.status.value,
            'position': self.position,
            'jersey_number': self.jersey_number,
            'grad_year': self.grad_year,
            'created_date': self.created_date.isoformat()
        }


@dataclass
class CoachNote:
    """Coach notes and observations"""
    note_id: str
    coach_id: str
    athlete_id: str
    timestamp: datetime
    content: str
    category: str  # e.g., "observation", "concern", "praise", "injury"
    is_private: bool = True
    tags: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'note_id': self.note_id,
            'coach_id': self.coach_id,
            'athlete_id': self.athlete_id,
            'timestamp': self.timestamp.isoformat(),
            'content': self.content,
            'category': self.category,
            'is_private': self.is_private,
            'tags': self.tags
        }


@dataclass
class TrainingAssignment:
    """Assigned training plan/drill"""
    assignment_id: str
    coach_id: str
    athlete_id: str
    drill_id: str
    drill_name: str
    assigned_date: datetime
    due_date: datetime
    status: AssignmentStatus
    priority: str  # HIGH, MEDIUM, LOW
    sets_required: int
    sets_completed: int
    notes: Optional[str] = None
    completed_date: Optional[datetime] = None
    
    @property
    def is_overdue(self) -> bool:
        """Check if assignment is overdue"""
        return datetime.now() > self.due_date and self.status != AssignmentStatus.COMPLETED
    
    @property
    def completion_percentage(self) -> float:
        """Calculate completion percentage"""
        if self.sets_required == 0:
            return 0.0
        return (self.sets_completed / self.sets_required) * 100
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'assignment_id': self.assignment_id,
            'coach_id': self.coach_id,
            'athlete_id': self.athlete_id,
            'drill_id': self.drill_id,
            'drill_name': self.drill_name,
            'assigned_date': self.assigned_date.isoformat(),
            'due_date': self.due_date.isoformat(),
            'status': self.status.value,
            'priority': self.priority,
            'sets_required': self.sets_required,
            'sets_completed': self.sets_completed,
            'completion_percentage': self.completion_percentage,
            'is_overdue': self.is_overdue,
            'notes': self.notes,
            'completed_date': self.completed_date.isoformat() if self.completed_date else None
        }


# ============================================================================
# TEAM MANAGEMENT SYSTEM
# ============================================================================

class TeamManagementSystem:
    """
    Comprehensive team management system for coaches
    
    Features:
    - Coach and team management
    - Athlete roster management
    - Multi-athlete comparison
    - Training assignment tracking
    - Coach notes and communication
    """
    
    def __init__(self):
        self.coaches: Dict[str, Coach] = {}
        self.teams: Dict[str, Team] = {}
        self.athletes: Dict[str, Athlete] = {}
        self.notes: Dict[str, List[CoachNote]] = {}  # athlete_id -> notes
        self.assignments: Dict[str, List[TrainingAssignment]] = {}  # athlete_id -> assignments
    
    # ========================================================================
    # COACH MANAGEMENT
    # ========================================================================
    
    def create_coach(self, coach_data: Dict[str, Any]) -> str:
        """Create new coach profile"""
        coach_id = str(uuid.uuid4())
        
        coach = Coach(
            coach_id=coach_id,
            name=coach_data['name'],
            email=coach_data['email'],
            role=CoachRole(coach_data.get('role', 'head_coach')),
            organization=coach_data['organization'],
            created_date=datetime.now(),
            phone=coach_data.get('phone'),
            bio=coach_data.get('bio'),
            certifications=coach_data.get('certifications', [])
        )
        
        self.coaches[coach_id] = coach
        return coach_id
    
    def get_coach(self, coach_id: str) -> Optional[Coach]:
        """Get coach by ID"""
        return self.coaches.get(coach_id)
    
    # ========================================================================
    # TEAM MANAGEMENT
    # ========================================================================
    
    def create_team(self, team_data: Dict[str, Any]) -> str:
        """Create new team"""
        team_id = str(uuid.uuid4())
        
        team = Team(
            team_id=team_id,
            name=team_data['name'],
            team_type=TeamType(team_data.get('team_type', 'high_school')),
            coach_id=team_data['coach_id'],
            created_date=datetime.now(),
            season=team_data['season'],
            description=team_data.get('description')
        )
        
        self.teams[team_id] = team
        
        # Add team to coach's team list
        coach = self.coaches.get(team_data['coach_id'])
        if coach:
            coach.teams.append(team_id)
        
        return team_id
    
    def get_team(self, team_id: str) -> Optional[Team]:
        """Get team by ID"""
        return self.teams.get(team_id)
    
    def get_coach_teams(self, coach_id: str) -> List[Team]:
        """Get all teams for a coach"""
        return [team for team in self.teams.values() if team.coach_id == coach_id]
    
    # ========================================================================
    # ATHLETE MANAGEMENT
    # ========================================================================
    
    def add_athlete(self, athlete_data: Dict[str, Any]) -> str:
        """Add athlete to team"""
        athlete_id = str(uuid.uuid4())
        
        athlete = Athlete(
            athlete_id=athlete_id,
            name=athlete_data['name'],
            email=athlete_data['email'],
            team_id=athlete_data['team_id'],
            date_of_birth=athlete_data['date_of_birth'],
            height_inches=athlete_data['height_inches'],
            wingspan_inches=athlete_data['wingspan_inches'],
            weight_lbs=athlete_data['weight_lbs'],
            bat_weight_oz=athlete_data['bat_weight_oz'],
            status=AthleteStatus(athlete_data.get('status', 'active')),
            created_date=datetime.now(),
            position=athlete_data.get('position'),
            jersey_number=athlete_data.get('jersey_number'),
            grad_year=athlete_data.get('grad_year'),
            parent_email=athlete_data.get('parent_email'),
            phone=athlete_data.get('phone')
        )
        
        self.athletes[athlete_id] = athlete
        
        # Add athlete to team
        team = self.teams.get(athlete_data['team_id'])
        if team:
            team.athlete_ids.append(athlete_id)
        
        # Initialize notes and assignments
        self.notes[athlete_id] = []
        self.assignments[athlete_id] = []
        
        return athlete_id
    
    def get_athlete(self, athlete_id: str) -> Optional[Athlete]:
        """Get athlete by ID"""
        return self.athletes.get(athlete_id)
    
    def get_team_roster(self, team_id: str, status_filter: Optional[str] = None) -> List[Athlete]:
        """Get all athletes in a team with optional status filter"""
        team = self.teams.get(team_id)
        if not team:
            return []
        
        roster = [self.athletes[aid] for aid in team.athlete_ids if aid in self.athletes]
        
        if status_filter:
            status_enum = AthleteStatus(status_filter)
            roster = [a for a in roster if a.status == status_enum]
        
        return roster
    
    def search_athletes(self, team_id: str, query: str) -> List[Athlete]:
        """Search athletes by name, position, or jersey number"""
        roster = self.get_team_roster(team_id)
        query_lower = query.lower()
        
        return [
            athlete for athlete in roster
            if query_lower in athlete.name.lower()
            or (athlete.position and query_lower in athlete.position.lower())
            or (athlete.jersey_number and str(athlete.jersey_number) == query)
        ]
    
    # ========================================================================
    # COACH NOTES
    # ========================================================================
    
    def add_note(self, note_data: Dict[str, Any]) -> str:
        """Add coach note for athlete"""
        note_id = str(uuid.uuid4())
        
        note = CoachNote(
            note_id=note_id,
            coach_id=note_data['coach_id'],
            athlete_id=note_data['athlete_id'],
            timestamp=datetime.now(),
            content=note_data['content'],
            category=note_data.get('category', 'observation'),
            is_private=note_data.get('is_private', True),
            tags=note_data.get('tags', [])
        )
        
        athlete_id = note_data['athlete_id']
        if athlete_id not in self.notes:
            self.notes[athlete_id] = []
        
        self.notes[athlete_id].append(note)
        return note_id
    
    def get_athlete_notes(self, athlete_id: str, days_back: int = 30) -> List[CoachNote]:
        """Get notes for athlete within time period"""
        if athlete_id not in self.notes:
            return []
        
        cutoff_date = datetime.now() - timedelta(days=days_back)
        return [
            note for note in self.notes[athlete_id]
            if note.timestamp >= cutoff_date
        ]
    
    # ========================================================================
    # TRAINING ASSIGNMENTS
    # ========================================================================
    
    def assign_drill(self, assignment_data: Dict[str, Any]) -> str:
        """Assign drill to athlete"""
        assignment_id = str(uuid.uuid4())
        
        assignment = TrainingAssignment(
            assignment_id=assignment_id,
            coach_id=assignment_data['coach_id'],
            athlete_id=assignment_data['athlete_id'],
            drill_id=assignment_data['drill_id'],
            drill_name=assignment_data['drill_name'],
            assigned_date=datetime.now(),
            due_date=assignment_data['due_date'],
            status=AssignmentStatus.ASSIGNED,
            priority=assignment_data.get('priority', 'MEDIUM'),
            sets_required=assignment_data.get('sets_required', 3),
            sets_completed=0,
            notes=assignment_data.get('notes')
        )
        
        athlete_id = assignment_data['athlete_id']
        if athlete_id not in self.assignments:
            self.assignments[athlete_id] = []
        
        self.assignments[athlete_id].append(assignment)
        return assignment_id
    
    def get_athlete_assignments(self, athlete_id: str, 
                                 status_filter: Optional[str] = None) -> List[TrainingAssignment]:
        """Get assignments for athlete"""
        if athlete_id not in self.assignments:
            return []
        
        assignments = self.assignments[athlete_id]
        
        # Update overdue status
        for assignment in assignments:
            if assignment.is_overdue and assignment.status != AssignmentStatus.COMPLETED:
                assignment.status = AssignmentStatus.OVERDUE
        
        if status_filter:
            status_enum = AssignmentStatus(status_filter)
            assignments = [a for a in assignments if a.status == status_enum]
        
        return assignments
    
    def update_assignment_progress(self, assignment_id: str, sets_completed: int) -> bool:
        """Update assignment progress"""
        for athlete_assignments in self.assignments.values():
            for assignment in athlete_assignments:
                if assignment.assignment_id == assignment_id:
                    assignment.sets_completed = sets_completed
                    
                    if sets_completed >= assignment.sets_required:
                        assignment.status = AssignmentStatus.COMPLETED
                        assignment.completed_date = datetime.now()
                    elif sets_completed > 0:
                        assignment.status = AssignmentStatus.IN_PROGRESS
                    
                    return True
        return False
    
    # ========================================================================
    # TEAM ANALYTICS
    # ========================================================================
    
    def get_team_analytics(self, team_id: str) -> Dict[str, Any]:
        """Get aggregate team analytics"""
        roster = self.get_team_roster(team_id)
        
        if not roster:
            return {
                'total_athletes': 0,
                'active_athletes': 0,
                'error': 'No athletes in team'
            }
        
        active_athletes = [a for a in roster if a.status == AthleteStatus.ACTIVE]
        
        # Calculate average biometrics
        avg_height = sum(a.height_inches for a in active_athletes) / len(active_athletes)
        avg_wingspan = sum(a.wingspan_inches for a in active_athletes) / len(active_athletes)
        avg_weight = sum(a.weight_lbs for a in active_athletes) / len(active_athletes)
        avg_age = sum(a.age for a in active_athletes) / len(active_athletes)
        
        # Count assignments
        total_assignments = sum(len(self.assignments.get(a.athlete_id, [])) for a in active_athletes)
        completed_assignments = sum(
            len([asn for asn in self.assignments.get(a.athlete_id, []) 
                 if asn.status == AssignmentStatus.COMPLETED])
            for a in active_athletes
        )
        
        completion_rate = (completed_assignments / total_assignments * 100) if total_assignments > 0 else 0
        
        return {
            'team_id': team_id,
            'total_athletes': len(roster),
            'active_athletes': len(active_athletes),
            'injured_athletes': len([a for a in roster if a.status == AthleteStatus.INJURED]),
            'avg_height_inches': round(avg_height, 1),
            'avg_wingspan_inches': round(avg_wingspan, 1),
            'avg_weight_lbs': round(avg_weight, 1),
            'avg_age': round(avg_age, 1),
            'total_assignments': total_assignments,
            'completed_assignments': completed_assignments,
            'completion_rate': round(completion_rate, 1),
            'positions': self._count_positions(active_athletes)
        }
    
    def _count_positions(self, athletes: List[Athlete]) -> Dict[str, int]:
        """Count athletes by position"""
        positions = {}
        for athlete in athletes:
            if athlete.position:
                positions[athlete.position] = positions.get(athlete.position, 0) + 1
        return positions
    
    # ========================================================================
    # MULTI-ATHLETE COMPARISON
    # ========================================================================
    
    def compare_athletes(self, athlete_ids: List[str], 
                         metric: str = 'bat_speed') -> List[Dict[str, Any]]:
        """
        Compare multiple athletes on a specific metric
        
        Requires integration with Priority 14 (Progress Tracking)
        to get latest metrics
        """
        comparison = []
        
        for athlete_id in athlete_ids:
            athlete = self.athletes.get(athlete_id)
            if not athlete:
                continue
            
            # This would integrate with Priority 14's ProgressTracker
            # For now, return athlete profile data
            comparison.append({
                'athlete_id': athlete_id,
                'name': athlete.name,
                'age': athlete.age,
                'height': athlete.height_inches,
                'wingspan': athlete.wingspan_inches,
                'position': athlete.position,
                'status': athlete.status.value,
                # Future: Add latest metrics from Progress Tracker
                # 'latest_bat_speed': progress_tracker.get_latest_metric(athlete_id, 'bat_speed'),
                # 'ground_score': progress_tracker.get_latest_metric(athlete_id, 'ground_score'),
                # etc.
            })
        
        return comparison


# ============================================================================
# TEST & DEMONSTRATION
# ============================================================================

def test_team_management():
    """Test the team management system"""
    print("=" * 70)
    print("TEAM MANAGEMENT SYSTEM - PRIORITY 16")
    print("=" * 70)
    print()
    
    system = TeamManagementSystem()
    
    # Create coach
    print("1. CREATING COACH")
    print("-" * 70)
    coach_id = system.create_coach({
        'name': 'Coach Mike Johnson',
        'email': 'mike.johnson@thsbaseball.com',
        'role': 'head_coach',
        'organization': 'Tomball High School Baseball',
        'phone': '(281) 555-1234',
        'certifications': ['USA Baseball', 'ABCA Level 3']
    })
    coach = system.get_coach(coach_id)
    print(f"✅ Coach Created: {coach.name}")
    print(f"   Role: {coach.role.value}")
    print(f"   Organization: {coach.organization}")
    print()
    
    # Create team
    print("2. CREATING TEAM")
    print("-" * 70)
    team_id = system.create_team({
        'name': 'Varsity Baseball 2024',
        'team_type': 'high_school',
        'coach_id': coach_id,
        'season': '2024 Spring',
        'description': 'Varsity team for Spring 2024 season'
    })
    team = system.get_team(team_id)
    print(f"✅ Team Created: {team.name}")
    print(f"   Season: {team.season}")
    print(f"   Type: {team.team_type.value}")
    print()
    
    # Add athletes
    print("3. ADDING ATHLETES TO ROSTER")
    print("-" * 70)
    athletes_data = [
        {
            'name': 'Eric Williams',
            'email': 'ewilliams@student.thsbaseball.com',
            'team_id': team_id,
            'date_of_birth': datetime(2006, 3, 15),
            'height_inches': 68,
            'wingspan_inches': 69,
            'weight_lbs': 190,
            'bat_weight_oz': 30,
            'position': 'OF',
            'jersey_number': 24,
            'grad_year': 2024,
            'status': 'active'
        },
        {
            'name': 'Jake Martinez',
            'email': 'jmartinez@student.thsbaseball.com',
            'team_id': team_id,
            'date_of_birth': datetime(2006, 7, 22),
            'height_inches': 72,
            'wingspan_inches': 74,
            'weight_lbs': 205,
            'bat_weight_oz': 32,
            'position': '1B',
            'jersey_number': 15,
            'grad_year': 2024,
            'status': 'active'
        },
        {
            'name': 'Tommy Chen',
            'email': 'tchen@student.thsbaseball.com',
            'team_id': team_id,
            'date_of_birth': datetime(2007, 1, 8),
            'height_inches': 70,
            'wingspan_inches': 71,
            'weight_lbs': 180,
            'bat_weight_oz': 31,
            'position': 'SS',
            'jersey_number': 7,
            'grad_year': 2025,
            'status': 'active'
        }
    ]
    
    athlete_ids = []
    for athlete_data in athletes_data:
        athlete_id = system.add_athlete(athlete_data)
        athlete_ids.append(athlete_id)
        athlete = system.get_athlete(athlete_id)
        print(f"✅ {athlete.name} (#{athlete.jersey_number}) - {athlete.position}")
        print(f"   Age: {athlete.age}, Height: {athlete.height_inches}\", Bat: {athlete.bat_weight_oz}oz")
    print()
    
    # Add coach notes
    print("4. ADDING COACH NOTES")
    print("-" * 70)
    system.add_note({
        'coach_id': coach_id,
        'athlete_id': athlete_ids[0],
        'content': 'Eric showed great improvement in hip rotation today. Continue focusing on connection drills.',
        'category': 'observation',
        'tags': ['hip_rotation', 'improvement']
    })
    system.add_note({
        'coach_id': coach_id,
        'athlete_id': athlete_ids[1],
        'content': 'Jake needs to work on front leg stability. Assign barrier drills.',
        'category': 'concern',
        'tags': ['ground_mechanics', 'stability']
    })
    
    for athlete_id in athlete_ids[:2]:
        notes = system.get_athlete_notes(athlete_id)
        athlete = system.get_athlete(athlete_id)
        print(f"✅ Note added for {athlete.name}")
        if notes:
            print(f"   \"{notes[0].content[:60]}...\"")
    print()
    
    # Assign drills
    print("5. ASSIGNING TRAINING DRILLS")
    print("-" * 70)
    assignments_data = [
        {
            'coach_id': coach_id,
            'athlete_id': athlete_ids[0],
            'drill_id': 'step_drill_stage1',
            'drill_name': 'Step Through Drill (Stage 1)',
            'due_date': datetime.now() + timedelta(days=7),
            'priority': 'HIGH',
            'sets_required': 5,
            'notes': 'Focus on rhythm and timing'
        },
        {
            'coach_id': coach_id,
            'athlete_id': athlete_ids[0],
            'drill_id': 'hip_rotation_drill',
            'drill_name': 'Hip-Only Rotation Drill',
            'due_date': datetime.now() + timedelta(days=7),
            'priority': 'HIGH',
            'sets_required': 4
        },
        {
            'coach_id': coach_id,
            'athlete_id': athlete_ids[1],
            'drill_id': 'barrier_drill',
            'drill_name': 'Backside Barrier Drill',
            'due_date': datetime.now() + timedelta(days=7),
            'priority': 'HIGH',
            'sets_required': 5,
            'notes': 'Work on front leg stability'
        }
    ]
    
    for assignment_data in assignments_data:
        assignment_id = system.assign_drill(assignment_data)
        athlete = system.get_athlete(assignment_data['athlete_id'])
        print(f"✅ Assigned to {athlete.name}: {assignment_data['drill_name']}")
        print(f"   Priority: {assignment_data['priority']}, Sets: {assignment_data['sets_required']}")
    print()
    
    # Update assignment progress
    print("6. UPDATING ASSIGNMENT PROGRESS")
    print("-" * 70)
    eric_assignments = system.get_athlete_assignments(athlete_ids[0])
    if eric_assignments:
        system.update_assignment_progress(eric_assignments[0].assignment_id, 3)
        print(f"✅ Eric Williams completed 3/5 sets of Step Through Drill")
        print(f"   Status: {eric_assignments[0].status.value}")
        print(f"   Completion: {eric_assignments[0].completion_percentage:.1f}%")
    print()
    
    # Team analytics
    print("7. TEAM ANALYTICS")
    print("-" * 70)
    analytics = system.get_team_analytics(team_id)
    print(f"✅ Team Overview:")
    print(f"   Total Athletes: {analytics['total_athletes']}")
    print(f"   Active: {analytics['active_athletes']}")
    print(f"   Avg Height: {analytics['avg_height_inches']}\"")
    print(f"   Avg Age: {analytics['avg_age']} years")
    print(f"   Total Assignments: {analytics['total_assignments']}")
    print(f"   Completion Rate: {analytics['completion_rate']}%")
    print(f"   Positions: {analytics['positions']}")
    print()
    
    # Multi-athlete comparison
    print("8. ATHLETE COMPARISON")
    print("-" * 70)
    comparison = system.compare_athletes(athlete_ids)
    print("✅ Roster Comparison:")
    print(f"   {'Name':<20} {'Pos':<5} {'Age':<5} {'Height':<7} {'Wingspan':<9}")
    print("   " + "-" * 50)
    for athlete_data in comparison:
        print(f"   {athlete_data['name']:<20} {athlete_data['position']:<5} "
              f"{athlete_data['age']:<5} {athlete_data['height']:<7} "
              f"{athlete_data['wingspan']:<9}")
    print()
    
    print("=" * 70)
    print("✅ TEAM MANAGEMENT SYSTEM READY!")
    print("=" * 70)
    print()
    print("FEATURES AVAILABLE:")
    print("  ✅ Coach profile management")
    print("  ✅ Team creation and organization")
    print("  ✅ Athlete roster management")
    print("  ✅ Coach notes and observations")
    print("  ✅ Training drill assignments")
    print("  ✅ Progress tracking on assignments")
    print("  ✅ Team analytics dashboard")
    print("  ✅ Multi-athlete comparison")
    print()


if __name__ == '__main__':
    test_team_management()
