"""
Production FastAPI Backend - Reboot Motion Athlete App
With PostgreSQL Database Integration
"""

from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime
import os
import logging

# Import database and models
from database import get_db, init_db, check_db_connection
from models import Player, Session as SessionModel, BiomechanicsData, SyncLog
from sync_service import RebootMotionSync

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Reboot Motion Athlete API - Production",
    description="REST API for athlete biomechanics data with PostgreSQL",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your Netlify domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database on app startup"""
    logger.info("🚀 Starting Reboot Motion API...")
    
    # Check database connection
    if check_db_connection():
        logger.info("✅ Database connected")
        # Create tables if they don't exist
        try:
            init_db()
            logger.info("✅ Database tables ready")
        except Exception as e:
            logger.error(f"❌ Error initializing database: {e}")
    else:
        logger.error("❌ Database connection failed - API will use limited functionality")


# Root endpoint
@app.get("/")
def read_root():
    """API information"""
    return {
        "message": "Reboot Motion Athlete API - Production",
        "version": "2.0.0",
        "status": "running",
        "database": "PostgreSQL",
        "endpoints": {
            "health": "/health",
            "players": "/players",
            "player_detail": "/players/{id}",
            "player_sessions": "/players/{id}/sessions",
            "session_data": "/sessions/{id}/data",
            "sync_status": "/sync/status",
            "docs": "/docs"
        }
    }


# Health check
@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    """Health check with database status"""
    try:
        # Test database connection
        db.execute("SELECT 1")
        db_status = "connected"
    except:
        db_status = "disconnected"
    
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "database": db_status
    }


# Get all players
@app.get("/players")
def get_players(
    skip: int = Query(0, description="Number of records to skip"),
    limit: int = Query(100, description="Maximum number of records to return"),
    search: Optional[str] = Query(None, description="Search by player name"),
    db: Session = Depends(get_db)
):
    """Get list of all players from database"""
    try:
        query = db.query(Player)
        
        # Search filter
        if search:
            search_filter = f"%{search}%"
            query = query.filter(
                (Player.first_name.ilike(search_filter)) |
                (Player.last_name.ilike(search_filter))
            )
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        players = query.order_by(Player.last_name, Player.first_name)\
                      .offset(skip)\
                      .limit(limit)\
                      .all()
        
        return {
            "total": total,
            "players": [player.to_dict() for player in players],
            "page": skip // limit + 1,
            "limit": limit
        }
    except Exception as e:
        logger.error(f"Error getting players: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Get specific player
@app.get("/players/{player_id}")
def get_player(player_id: int, db: Session = Depends(get_db)):
    """Get specific player details"""
    player = db.query(Player).filter(Player.id == player_id).first()
    
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    
    return player.to_dict()


# Get player's sessions
@app.get("/players/{player_id}/sessions")
def get_player_sessions(
    player_id: int,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    limit: int = Query(50, description="Maximum number of sessions to return"),
    db: Session = Depends(get_db)
):
    """Get all sessions for a specific player"""
    # Verify player exists
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    
    # Query sessions
    query = db.query(SessionModel).filter(SessionModel.player_id == player_id)
    
    # Date filters
    if start_date:
        query = query.filter(SessionModel.session_date >= start_date)
    if end_date:
        query = query.filter(SessionModel.session_date <= end_date)
    
    # Get sessions ordered by date
    sessions = query.order_by(SessionModel.session_date.desc())\
                   .limit(limit)\
                   .all()
    
    return {
        "sessions": [session.to_dict(include_player=True) for session in sessions],
        "total": len(sessions),
        "player_id": player_id
    }


# Get session details
@app.get("/sessions/{session_id}")
def get_session(session_id: int, db: Session = Depends(get_db)):
    """Get specific session details"""
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return session.to_dict(include_player=True)


# Get session biomechanics data
@app.get("/sessions/{session_id}/data")
def get_session_data(
    session_id: int,
    limit: int = Query(1000, description="Maximum number of data points to return"),
    db: Session = Depends(get_db)
):
    """Get biomechanics data for a session"""
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Get biomechanics data
    data_points = db.query(BiomechanicsData)\
                   .filter(BiomechanicsData.session_id == session_id)\
                   .order_by(BiomechanicsData.frame_number)\
                   .limit(limit)\
                   .all()
    
    return {
        "session": session.to_dict(include_player=True),
        "data_points": [dp.to_dict() for dp in data_points],
        "total_points": len(data_points)
    }


# Get session metrics
@app.get("/sessions/{session_id}/metrics")
def get_session_metrics(session_id: int, db: Session = Depends(get_db)):
    """Get aggregated metrics for a session"""
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Get biomechanics data count
    frame_count = db.query(BiomechanicsData)\
                   .filter(BiomechanicsData.session_id == session_id)\
                   .count()
    
    # Get first and last timestamps
    data_points = db.query(BiomechanicsData)\
                   .filter(BiomechanicsData.session_id == session_id)\
                   .order_by(BiomechanicsData.timestamp)\
                   .all()
    
    start_time = data_points[0].timestamp if data_points else None
    end_time = data_points[-1].timestamp if data_points else None
    
    return {
        "session_id": session_id,
        "total_frames": frame_count,
        "start_time": start_time.isoformat() if start_time else None,
        "end_time": end_time.isoformat() if end_time else None,
        "movement_type": session.movement_type_name
    }


# Get sync status
@app.get("/sync/status")
def get_sync_status(db: Session = Depends(get_db)):
    """Get status of last data sync"""
    last_sync = db.query(SyncLog)\
                 .order_by(SyncLog.started_at.desc())\
                 .first()
    
    if not last_sync:
        return {
            "message": "No sync operations recorded yet",
            "status": "never_synced"
        }
    
    return last_sync.to_dict()


# Trigger manual sync
@app.post("/sync/trigger")
async def trigger_sync(db: Session = Depends(get_db)):
    """Trigger manual data sync from Reboot Motion API"""
    try:
        # Check if OAuth credentials are configured
        username = os.environ.get("REBOOT_USERNAME")
        password = os.environ.get("REBOOT_PASSWORD")
        
        if not username or not password:
            raise HTTPException(
                status_code=500,
                detail="REBOOT_USERNAME and REBOOT_PASSWORD environment variables must be set"
            )
        
        # Initialize sync service with OAuth credentials
        sync_service = RebootMotionSync(username=username, password=password, db_session=db)
        
        logger.info("🔄 Starting data sync from Reboot Motion API...")
        
        # Create sync log entry
        sync_log = SyncLog(
            started_at=datetime.now(),
            status="in_progress"
        )
        db.add(sync_log)
        db.commit()
        
        try:
            # Perform sync
            result = await sync_service.sync_all_data()
            
            # Update sync log
            sync_log.completed_at = datetime.now()
            sync_log.status = "completed"
            sync_log.players_synced = result.get("players_synced", 0)
            sync_log.sessions_synced = result.get("sessions_synced", 0)
            sync_log.biomechanics_synced = result.get("biomechanics_synced", 0)
            sync_log.error_message = None
            db.commit()
            
            logger.info(f"✅ Sync completed: {result['players_synced']} players, {result['sessions_synced']} sessions")
            
            return {
                "status": "success",
                "message": "Data sync completed successfully",
                **result
            }
            
        except Exception as sync_error:
            # Update sync log with error
            sync_log.completed_at = datetime.now()
            sync_log.status = "failed"
            sync_log.error_message = str(sync_error)
            db.commit()
            
            logger.error(f"❌ Sync failed: {sync_error}")
            raise HTTPException(status_code=500, detail=f"Sync failed: {str(sync_error)}")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error triggering sync: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Get database stats
@app.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    """Get database statistics"""
    try:
        player_count = db.query(Player).count()
        session_count = db.query(SessionModel).count()
        biomech_count = db.query(BiomechanicsData).count()
        synced_sessions = db.query(SessionModel).filter(SessionModel.data_synced == True).count()
        
        return {
            "total_players": player_count,
            "total_sessions": session_count,
            "synced_sessions": synced_sessions,
            "pending_sessions": session_count - synced_sessions,
            "biomechanics_records": biomech_count
        }
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
