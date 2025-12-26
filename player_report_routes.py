"""
Player Report API Routes
Phase 1 Week 3-4: Priority 3
Endpoints for KRS scoring and 4B Framework metrics
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from database import get_db
from models import PlayerReport, Player, Session as DBSession
from krs_calculator import calculate_krs, calculate_on_table_gain
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["Player Reports"])


@router.get("/sessions/{session_id}/report")
async def get_session_report(
    session_id: str,
    db: Session = Depends(get_db)
):
    """
    Get full player report for a session.
    
    Returns:
    - KRS Hero data (total, level, subscores, on-table gain)
    - 4B Framework data (Brain, Body, Bat, Ball)
    - Session metadata
    
    Example response matches /docs/API_REFERENCE.md spec
    """
    try:
        # Query player report
        report = db.query(PlayerReport).filter(
            PlayerReport.session_id == session_id
        ).first()
        
        if not report:
            raise HTTPException(
                status_code=404,
                detail=f"No report found for session {session_id}"
            )
        
        # Return report with player info
        return report.to_dict(include_player=True)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching session report: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/sessions/latest")
async def get_latest_session(
    player_id: int = Query(..., description="Player ID"),
    db: Session = Depends(get_db)
):
    """
    Get most recent session for player.
    Used by Home Dashboard KRS Display Card.
    
    Returns:
    - Latest session report
    - KRS summary
    - 4B Framework preview
    """
    try:
        # Query latest report for player
        report = db.query(PlayerReport).filter(
            PlayerReport.player_id == player_id
        ).order_by(
            PlayerReport.analyzed_at.desc()
        ).first()
        
        if not report:
            # Return empty state for new players
            player = db.query(Player).filter(Player.id == player_id).first()
            if not player:
                raise HTTPException(
                    status_code=404,
                    detail=f"Player {player_id} not found"
                )
            
            return {
                "player_id": player_id,
                "has_data": False,
                "message": "No sessions yet. Upload your first swing!",
                "player": player.to_dict()
            }
        
        # Return latest report
        return {
            "player_id": player_id,
            "has_data": True,
            "latest_report": report.to_dict(include_player=True)
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching latest session: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/players/{player_id}/progress")
async def get_player_progress(
    player_id: int,
    days: int = Query(30, description="Number of days to look back"),
    db: Session = Depends(get_db)
):
    """
    Get KRS history for 30-day progress chart.
    
    Response:
    {
        "krs_history": [
            {"date": "2025-11-26", "krs": 70, "creation": 72, "transfer": 68},
            {"date": "2025-12-03", "krs": 71, "creation": 73, "transfer": 69},
            ...
        ],
        "trend": {
            "start_krs": 70,
            "end_krs": 75,
            "change": 5,
            "weekly_average": 0.5,
            "direction": "up"
        },
        "stats": {
            "total_swings": 150,
            "week_streak": 12,
            "days_since_last_swing": 1,
            "average_krs": 72.5
        }
    }
    """
    try:
        # Validate player exists
        player = db.query(Player).filter(Player.id == player_id).first()
        if not player:
            raise HTTPException(
                status_code=404,
                detail=f"Player {player_id} not found"
            )
        
        # Calculate date range
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        # Query reports in date range
        reports = db.query(PlayerReport).filter(
            PlayerReport.player_id == player_id,
            PlayerReport.analyzed_at >= start_date,
            PlayerReport.analyzed_at <= end_date
        ).order_by(
            PlayerReport.analyzed_at.asc()
        ).all()
        
        if not reports:
            return {
                "player_id": player_id,
                "krs_history": [],
                "trend": None,
                "stats": {
                    "total_swings": 0,
                    "week_streak": 0,
                    "days_since_last_swing": None,
                    "average_krs": None
                },
                "message": "No data available for the selected period"
            }
        
        # Build KRS history
        krs_history = []
        for report in reports:
            krs_history.append({
                "date": report.analyzed_at.strftime("%Y-%m-%d"),
                "krs": round(report.krs_total, 1),
                "creation": round(report.creation_score, 1),
                "transfer": round(report.transfer_score, 1)
            })
        
        # Calculate trend
        start_krs = reports[0].krs_total
        end_krs = reports[-1].krs_total
        change = round(end_krs - start_krs, 1)
        weeks = days / 7
        weekly_average = round(change / weeks, 1) if weeks > 0 else 0
        direction = "up" if change > 0 else "down" if change < 0 else "stable"
        
        # Calculate stats
        total_swings = sum(r.swing_count for r in reports if r.swing_count)
        average_krs = round(sum(r.krs_total for r in reports) / len(reports), 1)
        
        # Calculate streak (consecutive weeks with at least 1 session)
        week_streak = 0
        current_date = datetime.utcnow()
        for i in range(52):  # Check up to 52 weeks
            week_start = current_date - timedelta(days=(i+1)*7)
            week_end = current_date - timedelta(days=i*7)
            has_session = any(
                week_start <= r.analyzed_at <= week_end
                for r in reports
            )
            if has_session:
                week_streak += 1
            else:
                break
        
        # Days since last swing
        last_session = reports[-1]
        days_since = (datetime.utcnow() - last_session.analyzed_at).days
        
        return {
            "player_id": player_id,
            "krs_history": krs_history,
            "trend": {
                "start_krs": round(start_krs, 1),
                "end_krs": round(end_krs, 1),
                "change": change,
                "weekly_average": weekly_average,
                "direction": direction
            },
            "stats": {
                "total_swings": total_swings,
                "week_streak": week_streak,
                "days_since_last_swing": days_since,
                "average_krs": average_krs
            }
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching player progress: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/players/{player_id}/recommended-drills")
async def get_recommended_drills(
    player_id: int,
    db: Session = Depends(get_db)
):
    """
    Get personalized drill recommendations.
    Based on Creation/Transfer gaps and motor profile.
    
    Returns 10-15 drills prioritized by:
    1. Weakest 4B area (Brain/Body/Bat/Ball)
    2. Motor profile match
    3. KRS level appropriate
    """
    try:
        # Get latest report
        report = db.query(PlayerReport).filter(
            PlayerReport.player_id == player_id
        ).order_by(
            PlayerReport.analyzed_at.desc()
        ).first()
        
        if not report:
            player = db.query(Player).filter(Player.id == player_id).first()
            if not player:
                raise HTTPException(
                    status_code=404,
                    detail=f"Player {player_id} not found"
                )
            
            return {
                "player_id": player_id,
                "motor_profile": None,
                "drills": [],
                "message": "Complete a swing assessment to get personalized drills"
            }
        
        # Identify weakness areas
        creation_gap = 100 - report.creation_score
        transfer_gap = 100 - report.transfer_score
        
        # Determine focus area
        if creation_gap > transfer_gap:
            focus_area = "Creation"
            primary_category = "4B-Body"
        else:
            focus_area = "Transfer"
            primary_category = "4B-Bat"
        
        # Mock drill recommendations (in production, query from drills table)
        drills = [
            {
                "drill_id": "drill_001",
                "name": "Hip Rotation Drill",
                "category": "4B-Body",
                "focus_area": "Creation",
                "prescription": "Develop rotational power through progressive hip activation sequences",
                "duration": 5,
                "difficulty": "Intermediate",
                "thumbnail_url": "/drills/hip-rotation-thumb.jpg",
                "video_url": "/drills/hip-rotation-video.mp4",
                "reason": f"Enhance {focus_area.lower()} score (current: {report.creation_score if focus_area == 'Creation' else report.transfer_score:.1f})",
                "expected_gain": f"Improve {focus_area} score by 2-3 points"
            },
            {
                "drill_id": "drill_002",
                "name": "Weight Transfer Drill",
                "category": "4B-Bat",
                "focus_area": "Transfer",
                "prescription": "Optimize energy transfer from lower body to bat through proper sequencing",
                "duration": 7,
                "difficulty": "Intermediate",
                "thumbnail_url": "/drills/weight-transfer-thumb.jpg",
                "video_url": "/drills/weight-transfer-video.mp4",
                "reason": f"Improve transfer efficiency (current: {report.bat_transfer_efficiency:.0f}%)",
                "expected_gain": "Increase exit velocity by 2-4 mph"
            },
            {
                "drill_id": "drill_003",
                "name": f"{report.brain_motor_profile} Motor Pattern Drill",
                "category": "4B-Brain",
                "focus_area": "Motor Profile",
                "prescription": f"Reinforce {report.brain_motor_profile} movement patterns",
                "duration": 10,
                "difficulty": "Advanced",
                "thumbnail_url": f"/drills/{report.brain_motor_profile.lower()}-thumb.jpg",
                "video_url": f"/drills/{report.brain_motor_profile.lower()}-video.mp4",
                "reason": f"Optimize {report.brain_motor_profile} profile strengths",
                "expected_gain": "Increase consistency and timing"
            }
        ]
        
        return {
            "player_id": player_id,
            "motor_profile": report.brain_motor_profile,
            "focus_area": focus_area,
            "drills": drills,
            "generated_at": datetime.utcnow().isoformat()
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching recommended drills: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.post("/reports/create")
async def create_player_report(
    session_id: str,
    player_id: int,
    creation_score: float,
    transfer_score: float,
    exit_velocity: float,
    physical_capacity: float,
    motor_profile: str,
    db: Session = Depends(get_db)
):
    """
    Create a new player report (for testing/development).
    
    In production, this would be called by the analysis pipeline after Coach Rick processes a video.
    """
    try:
        # Validate player exists
        player = db.query(Player).filter(Player.id == player_id).first()
        if not player:
            raise HTTPException(
                status_code=404,
                detail=f"Player {player_id} not found"
            )
        
        # Calculate KRS
        krs_data = calculate_krs(creation_score, transfer_score)
        
        # Calculate on-table gain
        gain_data = calculate_on_table_gain(
            exit_velocity,
            physical_capacity,
            transfer_score
        )
        
        # Create report
        report = PlayerReport(
            session_id=session_id,
            player_id=player_id,
            krs_total=krs_data['krs_total'],
            krs_level=krs_data['krs_level'],
            creation_score=creation_score,
            transfer_score=transfer_score,
            on_table_gain_value=gain_data['value'] if gain_data else None,
            on_table_gain_metric=gain_data['metric'] if gain_data else 'mph',
            on_table_gain_description=gain_data['description'] if gain_data else None,
            brain_motor_profile=motor_profile,
            brain_confidence=92.0,
            brain_timing=0.24,
            body_creation_score=creation_score,
            body_physical_capacity_mph=physical_capacity,
            body_peak_force_n=723.0,
            bat_transfer_score=transfer_score,
            bat_transfer_efficiency=82.0,
            bat_attack_angle_deg=12.0,
            ball_exit_velocity_mph=exit_velocity,
            ball_capacity_mph=physical_capacity,
            ball_launch_angle_deg=18.0,
            ball_contact_quality="SOLID",
            swing_count=12,
            duration_minutes=45
        )
        
        db.add(report)
        db.commit()
        db.refresh(report)
        
        logger.info(f"Created report for session {session_id}, player {player_id}")
        
        return {
            "message": "Report created successfully",
            "report": report.to_dict(include_player=True)
        }
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating report: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )
