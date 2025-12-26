"""
PRIORITY 16: TEAM MANAGEMENT API ROUTES
========================================

FastAPI routes for Coach Dashboard and Team Management

Endpoints:
- POST /coaches - Create coach profile
- GET /coaches/{coach_id} - Get coach details
- POST /teams - Create team
- GET /teams/{team_id} - Get team details
- GET /coaches/{coach_id}/teams - Get coach's teams
- POST /athletes - Add athlete to team
- GET /athletes/{athlete_id} - Get athlete details
- GET /teams/{team_id}/roster - Get team roster
- GET /teams/{team_id}/analytics - Get team analytics
- POST /notes - Add coach note
- GET /athletes/{athlete_id}/notes - Get athlete notes
- POST /assignments - Assign drill to athlete
- GET /athletes/{athlete_id}/assignments - Get athlete assignments
- PUT /assignments/{assignment_id} - Update assignment progress
- POST /athletes/compare - Compare multiple athletes

Author: Reboot Motion Development Team
Date: 2025-12-24
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, EmailStr
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta

from physics_engine.team_management import (
    TeamManagementSystem,
    CoachRole,
    TeamType,
    AthleteStatus,
    AssignmentStatus
)

# Initialize router and system
router = APIRouter(prefix="/api/teams", tags=["Team Management"])
team_system = TeamManagementSystem()


# ============================================================================
# REQUEST MODELS
# ============================================================================

class CoachCreate(BaseModel):
    name: str
    email: EmailStr
    role: str = "head_coach"
    organization: str
    phone: Optional[str] = None
    bio: Optional[str] = None
    certifications: List[str] = []


class TeamCreate(BaseModel):
    name: str
    team_type: str = "high_school"
    coach_id: str
    season: str
    description: Optional[str] = None


class AthleteCreate(BaseModel):
    name: str
    email: EmailStr
    team_id: str
    date_of_birth: str  # ISO format: "2006-03-15"
    height_inches: int
    wingspan_inches: int
    weight_lbs: int
    bat_weight_oz: int
    status: str = "active"
    position: Optional[str] = None
    jersey_number: Optional[int] = None
    grad_year: Optional[int] = None
    parent_email: Optional[EmailStr] = None
    phone: Optional[str] = None


class NoteCreate(BaseModel):
    coach_id: str
    athlete_id: str
    content: str
    category: str = "observation"
    is_private: bool = True
    tags: List[str] = []


class AssignmentCreate(BaseModel):
    coach_id: str
    athlete_id: str
    drill_id: str
    drill_name: str
    due_days: int = 7  # Days from now
    priority: str = "MEDIUM"
    sets_required: int = 3
    notes: Optional[str] = None


class AssignmentUpdate(BaseModel):
    sets_completed: int


class AthleteCompare(BaseModel):
    athlete_ids: List[str]
    metric: str = "bat_speed"


# ============================================================================
# COACH ENDPOINTS
# ============================================================================

@router.post("/coaches")
def create_coach(coach: CoachCreate) -> Dict[str, Any]:
    """Create new coach profile"""
    try:
        coach_id = team_system.create_coach(coach.dict())
        coach_obj = team_system.get_coach(coach_id)
        
        return {
            'success': True,
            'coach_id': coach_id,
            'coach': coach_obj.to_dict()
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/coaches/{coach_id}")
def get_coach(coach_id: str) -> Dict[str, Any]:
    """Get coach details"""
    coach = team_system.get_coach(coach_id)
    
    if not coach:
        raise HTTPException(status_code=404, detail="Coach not found")
    
    return {
        'success': True,
        'coach': coach.to_dict()
    }


@router.get("/coaches/{coach_id}/teams")
def get_coach_teams(coach_id: str) -> Dict[str, Any]:
    """Get all teams for a coach"""
    teams = team_system.get_coach_teams(coach_id)
    
    return {
        'success': True,
        'total_teams': len(teams),
        'teams': [team.to_dict() for team in teams]
    }


# ============================================================================
# TEAM ENDPOINTS
# ============================================================================

@router.post("/teams")
def create_team(team: TeamCreate) -> Dict[str, Any]:
    """Create new team"""
    try:
        team_id = team_system.create_team(team.dict())
        team_obj = team_system.get_team(team_id)
        
        return {
            'success': True,
            'team_id': team_id,
            'team': team_obj.to_dict()
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/teams/{team_id}")
def get_team(team_id: str) -> Dict[str, Any]:
    """Get team details"""
    team = team_system.get_team(team_id)
    
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    return {
        'success': True,
        'team': team.to_dict()
    }


@router.get("/teams/{team_id}/roster")
def get_team_roster(
    team_id: str,
    status: Optional[str] = Query(None, description="Filter by status: active, injured, inactive"),
    search: Optional[str] = Query(None, description="Search by name, position, or jersey")
) -> Dict[str, Any]:
    """Get team roster with optional filters"""
    team = team_system.get_team(team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    if search:
        roster = team_system.search_athletes(team_id, search)
    else:
        roster = team_system.get_team_roster(team_id, status)
    
    return {
        'success': True,
        'team_id': team_id,
        'team_name': team.name,
        'total_athletes': len(roster),
        'roster': [athlete.to_dict() for athlete in roster]
    }


@router.get("/teams/{team_id}/analytics")
def get_team_analytics(team_id: str) -> Dict[str, Any]:
    """Get team analytics and aggregate stats"""
    team = team_system.get_team(team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    analytics = team_system.get_team_analytics(team_id)
    
    return {
        'success': True,
        'team_name': team.name,
        'analytics': analytics
    }


# ============================================================================
# ATHLETE ENDPOINTS
# ============================================================================

@router.post("/athletes")
def add_athlete(athlete: AthleteCreate) -> Dict[str, Any]:
    """Add athlete to team"""
    try:
        athlete_data = athlete.dict()
        # Convert date string to datetime
        athlete_data['date_of_birth'] = datetime.fromisoformat(athlete.date_of_birth)
        
        athlete_id = team_system.add_athlete(athlete_data)
        athlete_obj = team_system.get_athlete(athlete_id)
        
        return {
            'success': True,
            'athlete_id': athlete_id,
            'athlete': athlete_obj.to_dict()
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/athletes/{athlete_id}")
def get_athlete(athlete_id: str) -> Dict[str, Any]:
    """Get athlete details"""
    athlete = team_system.get_athlete(athlete_id)
    
    if not athlete:
        raise HTTPException(status_code=404, detail="Athlete not found")
    
    return {
        'success': True,
        'athlete': athlete.to_dict()
    }


# ============================================================================
# NOTES ENDPOINTS
# ============================================================================

@router.post("/notes")
def add_note(note: NoteCreate) -> Dict[str, Any]:
    """Add coach note for athlete"""
    try:
        note_id = team_system.add_note(note.dict())
        
        return {
            'success': True,
            'note_id': note_id,
            'message': 'Note added successfully'
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/athletes/{athlete_id}/notes")
def get_athlete_notes(
    athlete_id: str,
    days_back: int = Query(30, description="Number of days to look back")
) -> Dict[str, Any]:
    """Get notes for athlete"""
    athlete = team_system.get_athlete(athlete_id)
    if not athlete:
        raise HTTPException(status_code=404, detail="Athlete not found")
    
    notes = team_system.get_athlete_notes(athlete_id, days_back)
    
    return {
        'success': True,
        'athlete_id': athlete_id,
        'athlete_name': athlete.name,
        'total_notes': len(notes),
        'notes': [note.to_dict() for note in notes]
    }


# ============================================================================
# ASSIGNMENT ENDPOINTS
# ============================================================================

@router.post("/assignments")
def assign_drill(assignment: AssignmentCreate) -> Dict[str, Any]:
    """Assign drill to athlete"""
    try:
        assignment_data = assignment.dict()
        # Calculate due date
        assignment_data['due_date'] = datetime.now() + timedelta(days=assignment.due_days)
        del assignment_data['due_days']
        
        assignment_id = team_system.assign_drill(assignment_data)
        
        return {
            'success': True,
            'assignment_id': assignment_id,
            'message': 'Drill assigned successfully'
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/athletes/{athlete_id}/assignments")
def get_athlete_assignments(
    athlete_id: str,
    status: Optional[str] = Query(None, description="Filter by status: assigned, in_progress, completed, overdue")
) -> Dict[str, Any]:
    """Get assignments for athlete"""
    athlete = team_system.get_athlete(athlete_id)
    if not athlete:
        raise HTTPException(status_code=404, detail="Athlete not found")
    
    assignments = team_system.get_athlete_assignments(athlete_id, status)
    
    return {
        'success': True,
        'athlete_id': athlete_id,
        'athlete_name': athlete.name,
        'total_assignments': len(assignments),
        'assignments': [assignment.to_dict() for assignment in assignments]
    }


@router.put("/assignments/{assignment_id}")
def update_assignment(assignment_id: str, update: AssignmentUpdate) -> Dict[str, Any]:
    """Update assignment progress"""
    success = team_system.update_assignment_progress(
        assignment_id, 
        update.sets_completed
    )
    
    if not success:
        raise HTTPException(status_code=404, detail="Assignment not found")
    
    return {
        'success': True,
        'message': 'Assignment updated successfully'
    }


# ============================================================================
# COMPARISON ENDPOINTS
# ============================================================================

@router.post("/athletes/compare")
def compare_athletes(comparison: AthleteCompare) -> Dict[str, Any]:
    """Compare multiple athletes"""
    try:
        comparison_data = team_system.compare_athletes(
            comparison.athlete_ids,
            comparison.metric
        )
        
        return {
            'success': True,
            'metric': comparison.metric,
            'total_athletes': len(comparison_data),
            'comparison': comparison_data
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================================
# DASHBOARD SUMMARY
# ============================================================================

@router.get("/dashboard/{coach_id}")
def get_coach_dashboard(coach_id: str) -> Dict[str, Any]:
    """Get comprehensive dashboard for coach"""
    coach = team_system.get_coach(coach_id)
    if not coach:
        raise HTTPException(status_code=404, detail="Coach not found")
    
    teams = team_system.get_coach_teams(coach_id)
    
    dashboard = {
        'coach': coach.to_dict(),
        'total_teams': len(teams),
        'teams': []
    }
    
    for team in teams:
        team_data = team.to_dict()
        team_data['analytics'] = team_system.get_team_analytics(team.team_id)
        dashboard['teams'].append(team_data)
    
    return {
        'success': True,
        'dashboard': dashboard
    }
