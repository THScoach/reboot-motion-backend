"""
Catching Barrels - Session API Endpoints
=========================================

RESTful API endpoints for session management and player progress.

Endpoints:
- GET /api/sessions/{session_id}/report
- GET /api/players/{player_id}/progress

Author: Builder 2
Date: 2025-12-25
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import json
import logging

from session_storage import (
    get_session,
    get_player_progress,
    get_player_sessions,
    get_krs_history,
)

# Setup logger
logger = logging.getLogger(__name__)

# ============================================================================
# ROUTER
# ============================================================================

router = APIRouter(prefix="/api", tags=["Sessions & Progress"])


# ============================================================================
# ENDPOINTS
# ============================================================================

# Health check endpoint - using _health to avoid conflicts with {session_id}
@router.get("/storage/health")
async def storage_health() -> Dict[str, Any]:
    """Health check for session storage"""
    from session_storage import get_database_stats
    
    stats = get_database_stats()
    
    return {
        'status': 'healthy',
        'service': 'Session Storage API',
        'database': stats,
    }


@router.get("/sessions/{session_id}/report")
async def get_session_report(session_id: str) -> Dict[str, Any]:
    """
    Get complete player report for a session
    
    Args:
        session_id: Session ID from Coach Rick analysis
        
    Returns:
        Complete PlayerReport JSON
        
    Example:
        GET /api/sessions/coach_rick_abc123/report
    """
    session = get_session(session_id)
    
    if not session:
        raise HTTPException(
            status_code=404,
            detail=f"Session not found: {session_id}"
        )
    
    # Return the complete report
    return session['report']


@router.get("/players/{player_id}/progress")
async def get_player_progress_endpoint(player_id: str) -> Dict[str, Any]:
    """
    Get aggregated progress for a player
    
    Args:
        player_id: Player ID
        
    Returns:
        {
            total_sessions: int,
            total_swings: int,
            current_krs: float,
            best_krs: float,
            avg_krs: float,
            current_streak_weeks: int,
            last_session_date: str,
            krs_history: [{date, krs, creation, transfer}],
            recent_sessions: [session summaries],
            milestones: [milestone objects]
        }
        
    Example:
        GET /api/players/player_123/progress
    """
    progress = get_player_progress(player_id)
    
    if not progress:
        raise HTTPException(
            status_code=404,
            detail=f"Player not found: {player_id}"
        )
    
    # Get KRS history for charting
    krs_history = get_krs_history(player_id, limit=20)
    
    # Get recent sessions (last 5)
    recent_sessions = get_player_sessions(player_id, limit=5)
    recent_summary = [
        {
            'session_id': s['session_id'],
            'session_number': s['session_number'],
            'session_date': s['session_date'],
            'krs_total': s['krs_total'],
            'krs_level': s['krs_level'],
            'motor_profile_type': s['motor_profile_type'],
        }
        for s in recent_sessions
    ]
    
    # Combine everything
    return {
        'player_id': player_id,
        'total_sessions': progress['total_sessions'],
        'total_swings': progress['total_swings'],
        'current_krs': progress['current_krs'],
        'best_krs': progress['best_krs'],
        'avg_krs': progress['avg_krs'],
        'current_streak_weeks': progress['current_streak_weeks'],
        'last_session_date': progress['last_session_date'],
        'krs_history': krs_history,
        'recent_sessions': recent_summary,
        'milestones': progress['milestones'],
    }


@router.get("/sessions/{session_id}")
async def get_session_summary(session_id: str) -> Dict[str, Any]:
    """
    Get session summary (without full report)
    
    Args:
        session_id: Session ID
        
    Returns:
        Session summary with key metrics
    """
    session = get_session(session_id)
    
    if not session:
        raise HTTPException(
            status_code=404,
            detail=f"Session not found: {session_id}"
        )
    
    # Return summary without full report
    return {
        'session_id': session['session_id'],
        'player_id': session['player_id'],
        'session_number': session['session_number'],
        'session_date': session['session_date'],
        'krs_total': session['krs_total'],
        'creation_score': session['creation_score'],
        'transfer_score': session['transfer_score'],
        'krs_level': session['krs_level'],
        'bat_speed_mph': session['bat_speed_mph'],
        'exit_velocity_mph': session['exit_velocity_mph'],
        'motor_profile_type': session['motor_profile_type'],
        'motor_profile_confidence': session['motor_profile_confidence'],
        'created_at': session['created_at'],
    }


@router.get("/players/{player_id}/sessions")
async def get_player_sessions_endpoint(
    player_id: str,
    limit: int = 10,
    offset: int = 0
) -> Dict[str, Any]:
    """
    Get sessions for a player (paginated)
    
    Args:
        player_id: Player ID
        limit: Max sessions to return (default 10)
        offset: Pagination offset (default 0)
        
    Returns:
        List of session summaries
    """
    sessions = get_player_sessions(player_id, limit=limit, offset=offset)
    
    if not sessions:
        return {
            'player_id': player_id,
            'sessions': [],
            'count': 0,
        }
    
    # Return summaries
    summaries = [
        {
            'session_id': s['session_id'],
            'session_number': s['session_number'],
            'session_date': s['session_date'],
            'krs_total': s['krs_total'],
            'krs_level': s['krs_level'],
            'motor_profile_type': s['motor_profile_type'],
        }
        for s in sessions
    ]
    
    return {
        'player_id': player_id,
        'sessions': summaries,
        'count': len(summaries),
        'limit': limit,
        'offset': offset,
    }


@router.get("/reboot/players/search")
async def search_reboot_players(query: str) -> Dict[str, Any]:
    """
    Search for players in Reboot Motion database
    
    Args:
        query: Search string (player name)
        
    Returns:
        List of matching players (top 10)
        
    Example:
        GET /api/reboot/players/search?query=Eric+Williams
    """
    from sync_service import RebootMotionSync
    
    try:
        # Initialize Reboot Motion sync
        sync = RebootMotionSync()
        
        # Get all players from Reboot Motion
        players = sync.get_players()
        
        # Filter by name (case-insensitive)
        query_lower = query.lower()
        filtered = [
            p for p in players
            if query_lower in f"{p.get('first_name', '')} {p.get('last_name', '')}".lower()
        ]
        
        # Return top 10 matches
        return {
            'query': query,
            'count': len(filtered),
            'players': filtered[:10]
        }
        
    except Exception as e:
        # If Reboot Motion API fails, return empty results
        logger.error(f"Reboot Motion search failed: {e}")
        return {
            'query': query,
            'count': 0,
            'players': [],
            'error': str(e)
        }


@router.get("/reboot/players/{player_id}/sessions")
async def get_reboot_player_sessions(
    player_id: str,
    limit: int = 10
) -> Dict[str, Any]:
    """
    Get sessions for a player from Reboot Motion API
    
    Args:
        player_id: Reboot Motion player ID
        limit: Max sessions to return (default 10)
        
    Returns:
        List of session dictionaries with biomechanics data
        
    Example:
        GET /api/reboot/players/0068edb2-6243-4a48-8d9b-da6be14c4e69/sessions?limit=5
    """
    import os
    import logging
    
    logger = logging.getLogger(__name__)
    
    # Check if Reboot credentials are available
    has_credentials = os.environ.get('REBOOT_USERNAME') and os.environ.get('REBOOT_PASSWORD')
    
    if not has_credentials:
        logger.warning("⚠️ Reboot Motion credentials not configured")
        return {
            'player_id': player_id,
            'sessions': [],
            'count': 0,
            'error': 'Reboot Motion credentials not configured'
        }
    
    try:
        from sync_service import RebootMotionSync
        
        # Initialize Reboot Motion sync
        logger.info(f"🔄 Fetching sessions for player {player_id}...")
        sync = RebootMotionSync()
        
        # Get sessions from Reboot Motion API
        sessions = sync.get_player_sessions(player_id, limit=limit)
        
        if not sessions:
            logger.warning(f"⚠️ No sessions found for player {player_id}")
            return {
                'player_id': player_id,
                'sessions': [],
                'count': 0,
                'message': 'No sessions found for this player'
            }
        
        logger.info(f"✅ Found {len(sessions)} sessions for player {player_id}")
        
        # Return sessions with metadata
        return {
            'player_id': player_id,
            'sessions': sessions,
            'count': len(sessions),
            'limit': limit,
            'source': 'reboot_motion_api'
        }
        
    except ValueError as e:
        logger.error(f"❌ Credential error: {e}")
        return {
            'player_id': player_id,
            'sessions': [],
            'count': 0,
            'error': f'Reboot Motion credentials error: {str(e)}'
        }
    except Exception as e:
        logger.error(f"❌ Failed to fetch sessions for player {player_id}: {e}")
        return {
            'player_id': player_id,
            'sessions': [],
            'count': 0,
            'error': f'Failed to fetch sessions: {str(e)}'
        }


@router.post("/reboot/sync")
async def trigger_reboot_sync() -> Dict[str, Any]:
    """
    Trigger full sync of Reboot Motion data to database
    
    Syncs:
    - All players
    - All sessions  
    - All biomechanics data
    
    This can take several minutes for large datasets.
    
    Returns:
        Sync results with counts
        
    Example:
        POST /api/reboot/sync
    """
    import os
    import logging
    
    logger = logging.getLogger(__name__)
    
    # Check if Reboot credentials are available
    has_credentials = os.environ.get('REBOOT_USERNAME') and os.environ.get('REBOOT_PASSWORD')
    
    if not has_credentials:
        logger.warning("⚠️ Reboot Motion credentials not configured")
        return {
            'status': 'error',
            'error': 'Reboot Motion credentials not configured. Please set REBOOT_USERNAME and REBOOT_PASSWORD environment variables.'
        }
    
    try:
        from sync_service import RebootMotionSync
        
        logger.info("🚀 Starting full Reboot Motion sync...")
        sync = RebootMotionSync()
        
        # Run the async sync
        result = await sync.sync_all_data()
        
        logger.info(f"✅ Sync completed: {result}")
        return result
        
    except ValueError as e:
        logger.error(f"❌ Credential error: {e}")
        return {
            'status': 'error',
            'error': f'Reboot Motion credentials error: {str(e)}'
        }
    except Exception as e:
        logger.error(f"❌ Sync failed: {e}")
        import traceback
        traceback.print_exc()
        return {
            'status': 'error',
            'error': f'Sync failed: {str(e)}'
        }


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    print("Session API Router ready!")
    print("Endpoints:")
    print("  GET /api/sessions/{session_id}/report")
    print("  GET /api/players/{player_id}/progress")
    print("  GET /api/sessions/{session_id}")
    print("  GET /api/players/{player_id}/sessions")
    print("  GET /api/sessions/health")
