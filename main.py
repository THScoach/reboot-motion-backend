"""
FastAPI Backend for Reboot Motion Athlete App
Main API endpoints for serving data to frontend
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
from datetime import datetime
import os

# Initialize FastAPI app
app = FastAPI(
    title="Reboot Motion Athlete API",
    description="REST API for athlete biomechanics data",
    version="1.0.0"
)

# CORS middleware - allows frontend to access API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your Netlify domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock data for initial testing (before database is connected)
MOCK_PLAYERS = [
    {
        "id": 1,
        "first_name": "Connor",
        "last_name": "Gray",
        "height_ft": 6.0,
        "weight_lbs": 160,
        "dominant_hand_hitting": "LHA",
        "dominant_hand_throwing": "RHA",
        "date_of_birth": "2010-11-24"
    },
    {
        "id": 2,
        "first_name": "John",
        "last_name": "Smith",
        "height_ft": 5.11,
        "weight_lbs": 185,
        "dominant_hand_hitting": "RHA",
        "dominant_hand_throwing": "RHA",
        "date_of_birth": "2009-05-15"
    },
    {
        "id": 3,
        "first_name": "Mike",
        "last_name": "Johnson",
        "height_ft": 6.2,
        "weight_lbs": 195,
        "dominant_hand_hitting": "RHA",
        "dominant_hand_throwing": "RHA",
        "date_of_birth": "2008-09-20"
    }
]

MOCK_SESSIONS = [
    {
        "id": 1,
        "session_id": "527e68db-34e9-4daf-a123",
        "player_id": 1,
        "session_date": "2024-12-20T10:30:00",
        "movement_type_name": "Pitching",
        "data_synced": True,
        "player": MOCK_PLAYERS[0]
    },
    {
        "id": 2,
        "session_id": "627e68db-34e9-4daf-b234",
        "player_id": 1,
        "session_date": "2024-12-18T14:15:00",
        "movement_type_name": "Hitting",
        "data_synced": True,
        "player": MOCK_PLAYERS[0]
    },
    {
        "id": 3,
        "session_id": "727e68db-34e9-4daf-c345",
        "player_id": 2,
        "session_date": "2024-12-19T09:00:00",
        "movement_type_name": "Pitching",
        "data_synced": False,
        "player": MOCK_PLAYERS[1]
    }
]

# Root endpoint
@app.get("/")
def read_root():
    """API information"""
    return {
        "message": "Reboot Motion Athlete API",
        "version": "1.0.0",
        "status": "running",
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
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "database": "connected"  # Will update when real DB is connected
    }

# Get all players
@app.get("/players")
def get_players(
    skip: int = Query(0, description="Number of records to skip"),
    limit: int = Query(100, description="Maximum number of records to return"),
    search: Optional[str] = Query(None, description="Search by player name")
):
    """Get list of all players"""
    players = MOCK_PLAYERS
    
    # Search filter
    if search:
        search_lower = search.lower()
        players = [
            p for p in players 
            if search_lower in p["first_name"].lower() or search_lower in p["last_name"].lower()
        ]
    
    # Pagination
    total = len(players)
    players = players[skip:skip + limit]
    
    return {
        "total": total,
        "players": players,
        "page": skip // limit + 1,
        "limit": limit
    }

# Get specific player
@app.get("/players/{player_id}")
def get_player(player_id: int):
    """Get specific player details"""
    player = next((p for p in MOCK_PLAYERS if p["id"] == player_id), None)
    
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    
    return player

# Get player's sessions
@app.get("/players/{player_id}/sessions")
def get_player_sessions(
    player_id: int,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    limit: int = Query(50, description="Maximum number of sessions to return")
):
    """Get all sessions for a specific player"""
    sessions = [s for s in MOCK_SESSIONS if s["player_id"] == player_id]
    
    if not sessions:
        return {
            "sessions": [],
            "total": 0,
            "player_id": player_id
        }
    
    return {
        "sessions": sessions[:limit],
        "total": len(sessions),
        "player_id": player_id
    }

# Get session details
@app.get("/sessions/{session_id}")
def get_session(session_id: int):
    """Get specific session details"""
    session = next((s for s in MOCK_SESSIONS if s["id"] == session_id), None)
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return session

# Get session biomechanics data
@app.get("/sessions/{session_id}/data")
def get_session_data(
    session_id: int,
    limit: int = Query(1000, description="Maximum number of data points to return")
):
    """Get biomechanics data for a session"""
    session = next((s for s in MOCK_SESSIONS if s["id"] == session_id), None)
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Generate mock biomechanics data
    data_points = []
    for i in range(min(100, limit)):  # Generate 100 sample frames
        data_points.append({
            "frame_number": i + 1,
            "timestamp": f"2024-12-20T10:30:{i:02d}",
            "joint_angles": {
                "shoulder": 45.5 + (i * 0.5),
                "elbow": 90.0 + (i * 0.3),
                "hip": 120.0 - (i * 0.2),
                "knee": 150.0 + (i * 0.1)
            },
            "joint_positions": {
                "shoulder_x": 1.2 + (i * 0.01),
                "shoulder_y": 0.8 + (i * 0.02),
                "elbow_x": 1.5 + (i * 0.015),
                "elbow_y": 0.6 + (i * 0.01)
            },
            "joint_velocities": {
                "shoulder": 2.5 + (i * 0.05),
                "elbow": 3.2 + (i * 0.03),
                "hip": 1.8 + (i * 0.02)
            }
        })
    
    return {
        "session": session,
        "data_points": data_points,
        "total_points": len(data_points)
    }

# Get session metrics
@app.get("/sessions/{session_id}/metrics")
def get_session_metrics(session_id: int):
    """Get aggregated metrics for a session"""
    session = next((s for s in MOCK_SESSIONS if s["id"] == session_id), None)
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return {
        "session_id": session_id,
        "total_frames": 100,
        "start_time": "2024-12-20T10:30:00",
        "end_time": "2024-12-20T10:35:00",
        "duration_seconds": 300,
        "max_velocity": 95.5,
        "avg_velocity": 87.3,
        "max_shoulder_angle": 145.2,
        "avg_shoulder_angle": 98.7
    }

# Get sync status
@app.get("/sync/status")
def get_sync_status():
    """Get status of last data sync"""
    return {
        "last_sync": "2024-12-20T08:00:00",
        "status": "success",
        "records_synced": 150,
        "next_sync": "2024-12-21T08:00:00"
    }

# Trigger manual sync
@app.post("/sync/trigger")
def trigger_sync():
    """Trigger manual data sync (placeholder)"""
    return {
        "status": "sync_triggered",
        "message": "Data sync started in background",
        "estimated_completion": "2 minutes"
    }

# Error handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    return {
        "error": str(exc),
        "message": "An error occurred processing your request"
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
