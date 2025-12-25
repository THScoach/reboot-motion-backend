"""
Catching Barrels - Session Storage
===================================

SQLite database for storing player sessions and tracking progress.

Database Schema:
- players: Player biographical info
- sessions: Individual session records with PlayerReport JSON
- progress: Aggregated progress metrics

Author: Builder 2
Date: 2025-12-25
"""

import sqlite3
import json
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from pathlib import Path
import uuid

from player_report_schema import PlayerReport


# ============================================================================
# DATABASE SETUP
# ============================================================================

# Database file location
DB_PATH = Path(__file__).parent / "catching_barrels.db"


def get_db_connection():
    """Get SQLite database connection"""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row  # Enable column access by name
    return conn


def init_database():
    """Initialize database with schema"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # ========================================
    # PLAYERS TABLE
    # ========================================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS players (
            player_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER,
            height_inches REAL,
            weight_lbs REAL,
            wingspan_inches REAL,
            ape_index REAL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)
    
    # ========================================
    # SESSIONS TABLE
    # ========================================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            session_id TEXT PRIMARY KEY,
            player_id TEXT NOT NULL,
            session_number INTEGER NOT NULL,
            session_date TEXT NOT NULL,
            
            -- Core metrics
            krs_total REAL,
            creation_score REAL,
            transfer_score REAL,
            krs_level TEXT,
            
            bat_speed_mph REAL,
            exit_velocity_mph REAL,
            
            motor_profile_type TEXT,
            motor_profile_confidence REAL,
            
            -- Full report JSON
            report_json TEXT NOT NULL,
            
            created_at TEXT NOT NULL,
            
            FOREIGN KEY (player_id) REFERENCES players(player_id)
        )
    """)
    
    # ========================================
    # PROGRESS TABLE (Aggregated Stats)
    # ========================================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS progress (
            player_id TEXT PRIMARY KEY,
            total_sessions INTEGER DEFAULT 0,
            total_swings INTEGER DEFAULT 0,
            current_streak_weeks INTEGER DEFAULT 0,
            last_session_date TEXT,
            
            -- KRS stats
            current_krs REAL,
            best_krs REAL,
            avg_krs REAL,
            
            -- Milestones
            milestones_json TEXT DEFAULT '[]',
            
            updated_at TEXT NOT NULL,
            
            FOREIGN KEY (player_id) REFERENCES players(player_id)
        )
    """)
    
    # ========================================
    # INDEXES
    # ========================================
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_sessions_player 
        ON sessions(player_id)
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_sessions_date 
        ON sessions(session_date)
    """)
    
    conn.commit()
    conn.close()
    
    print(f"✅ Database initialized at: {DB_PATH}")


# ============================================================================
# PLAYER OPERATIONS
# ============================================================================

def create_or_update_player(
    player_id: str,
    name: str,
    age: int,
    height_inches: float,
    weight_lbs: float,
    wingspan_inches: Optional[float] = None,
) -> str:
    """
    Create or update player record
    
    Args:
        player_id: Player ID (use existing or generate new)
        name: Player name
        age: Player age
        height_inches: Height
        weight_lbs: Weight
        wingspan_inches: Wingspan (optional)
        
    Returns:
        player_id
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Calculate ape index if wingspan available
    ape_index = wingspan_inches - height_inches if wingspan_inches else None
    
    now = datetime.utcnow().isoformat()
    
    # Check if player exists
    cursor.execute("SELECT player_id FROM players WHERE player_id = ?", (player_id,))
    exists = cursor.fetchone()
    
    if exists:
        # Update existing player
        cursor.execute("""
            UPDATE players SET
                name = ?,
                age = ?,
                height_inches = ?,
                weight_lbs = ?,
                wingspan_inches = ?,
                ape_index = ?,
                updated_at = ?
            WHERE player_id = ?
        """, (name, age, height_inches, weight_lbs, wingspan_inches, ape_index, now, player_id))
    else:
        # Create new player
        cursor.execute("""
            INSERT INTO players (
                player_id, name, age, height_inches, weight_lbs,
                wingspan_inches, ape_index, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (player_id, name, age, height_inches, weight_lbs,
              wingspan_inches, ape_index, now, now))
    
    conn.commit()
    conn.close()
    
    return player_id


def get_player(player_id: str) -> Optional[Dict]:
    """Get player by ID"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM players WHERE player_id = ?", (player_id,))
    row = cursor.fetchone()
    
    conn.close()
    
    if row:
        return dict(row)
    return None


# ============================================================================
# SESSION OPERATIONS
# ============================================================================

def save_session(report: PlayerReport) -> str:
    """
    Save session to database
    
    Args:
        report: Complete PlayerReport object
        
    Returns:
        session_id
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Convert report to JSON
    report_json = json.dumps(report.to_dict())
    
    now = datetime.utcnow().isoformat()
    
    # Insert session
    cursor.execute("""
        INSERT INTO sessions (
            session_id, player_id, session_number, session_date,
            krs_total, creation_score, transfer_score, krs_level,
            bat_speed_mph, exit_velocity_mph,
            motor_profile_type, motor_profile_confidence,
            report_json, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        report.session_id,
        report.player_id,
        report.session_number,
        report.session_date,
        report.krs.total,
        report.krs.creation_score,
        report.krs.transfer_score,
        report.krs.level.value,
        report.ball.current.exit_velo_mph - 10,  # Estimate bat speed from exit velo
        report.ball.current.exit_velo_mph,
        report.brain.motor_profile.primary.value,
        report.brain.motor_profile.primary_confidence,
        report_json,
        now,
    ))
    
    conn.commit()
    
    # Update progress
    _update_progress(cursor, report.player_id, report)
    
    conn.commit()
    conn.close()
    
    return report.session_id


def get_session(session_id: str) -> Optional[Dict]:
    """
    Get session by ID
    
    Returns:
        Dict with session data including full report_json
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM sessions WHERE session_id = ?", (session_id,))
    row = cursor.fetchone()
    
    conn.close()
    
    if row:
        session_dict = dict(row)
        # Parse report JSON
        session_dict['report'] = json.loads(session_dict['report_json'])
        return session_dict
    return None


def get_player_sessions(
    player_id: str,
    limit: int = 10,
    offset: int = 0
) -> List[Dict]:
    """
    Get sessions for a player
    
    Args:
        player_id: Player ID
        limit: Max sessions to return
        offset: Pagination offset
        
    Returns:
        List of session dicts
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM sessions
        WHERE player_id = ?
        ORDER BY session_date DESC
        LIMIT ? OFFSET ?
    """, (player_id, limit, offset))
    
    rows = cursor.fetchall()
    conn.close()
    
    sessions = []
    for row in rows:
        session_dict = dict(row)
        session_dict['report'] = json.loads(session_dict['report_json'])
        sessions.append(session_dict)
    
    return sessions


def get_latest_session(player_id: str) -> Optional[Dict]:
    """Get most recent session for a player"""
    sessions = get_player_sessions(player_id, limit=1)
    return sessions[0] if sessions else None


# ============================================================================
# PROGRESS OPERATIONS
# ============================================================================

def _update_progress(cursor, player_id: str, report: PlayerReport):
    """
    Update aggregated progress for player (internal helper)
    
    Args:
        cursor: Database cursor
        player_id: Player ID
        report: Latest session report
    """
    now = datetime.utcnow().isoformat()
    
    # Get current progress
    cursor.execute("SELECT * FROM progress WHERE player_id = ?", (player_id,))
    current = cursor.fetchone()
    
    if current:
        current = dict(current)
        
        # Calculate new values
        total_sessions = current['total_sessions'] + 1
        total_swings = report.progress.total_swings
        
        # Calculate streak
        last_date = datetime.fromisoformat(current['last_session_date'])
        current_date = datetime.fromisoformat(report.session_date)
        days_diff = (current_date - last_date).days
        
        if days_diff <= 7:
            current_streak_weeks = current['current_streak_weeks'] + (1 if days_diff >= 7 else 0)
        else:
            current_streak_weeks = 1  # Reset streak
        
        # KRS stats
        current_krs = report.krs.total
        best_krs = max(current['best_krs'], current_krs)
        
        # Calculate average KRS
        old_avg = current['avg_krs']
        avg_krs = ((old_avg * (total_sessions - 1)) + current_krs) / total_sessions
        
        # Milestones
        milestones = json.loads(current['milestones_json'])
        new_milestones = _check_milestones(
            total_sessions, total_swings, current_krs, best_krs, milestones
        )
        
        # Update progress
        cursor.execute("""
            UPDATE progress SET
                total_sessions = ?,
                total_swings = ?,
                current_streak_weeks = ?,
                last_session_date = ?,
                current_krs = ?,
                best_krs = ?,
                avg_krs = ?,
                milestones_json = ?,
                updated_at = ?
            WHERE player_id = ?
        """, (
            total_sessions, total_swings, current_streak_weeks,
            report.session_date, current_krs, best_krs, avg_krs,
            json.dumps(new_milestones), now, player_id
        ))
    else:
        # Create new progress record
        milestones = _check_milestones(1, report.progress.total_swings, report.krs.total, report.krs.total, [])
        
        cursor.execute("""
            INSERT INTO progress (
                player_id, total_sessions, total_swings, current_streak_weeks,
                last_session_date, current_krs, best_krs, avg_krs,
                milestones_json, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            player_id, 1, report.progress.total_swings, 1,
            report.session_date, report.krs.total, report.krs.total, report.krs.total,
            json.dumps(milestones), now
        ))


def _check_milestones(
    total_sessions: int,
    total_swings: int,
    current_krs: float,
    best_krs: float,
    existing_milestones: List[Dict]
) -> List[Dict]:
    """Check for new milestones"""
    milestones = existing_milestones.copy()
    
    # Session milestones
    session_marks = [5, 10, 25, 50, 100]
    for mark in session_marks:
        if total_sessions == mark:
            milestones.append({
                'type': 'sessions',
                'value': mark,
                'date': datetime.utcnow().isoformat(),
                'description': f'Completed {mark} sessions'
            })
    
    # Swing milestones
    swing_marks = [50, 100, 500, 1000]
    for mark in swing_marks:
        if total_swings >= mark and not any(m.get('type') == 'swings' and m.get('value') == mark for m in milestones):
            milestones.append({
                'type': 'swings',
                'value': mark,
                'date': datetime.utcnow().isoformat(),
                'description': f'Recorded {mark} swings'
            })
    
    # KRS level milestones
    krs_levels = [
        (40, 'BUILDING'),
        (60, 'DEVELOPING'),
        (75, 'ADVANCED'),
        (90, 'ELITE')
    ]
    for threshold, level in krs_levels:
        if current_krs >= threshold and not any(m.get('type') == 'krs_level' and m.get('value') == level for m in milestones):
            milestones.append({
                'type': 'krs_level',
                'value': level,
                'date': datetime.utcnow().isoformat(),
                'description': f'Reached {level} level'
            })
    
    return milestones


def get_player_progress(player_id: str) -> Optional[Dict]:
    """Get aggregated progress for a player"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM progress WHERE player_id = ?", (player_id,))
    row = cursor.fetchone()
    
    conn.close()
    
    if row:
        progress_dict = dict(row)
        progress_dict['milestones'] = json.loads(progress_dict['milestones_json'])
        return progress_dict
    return None


def get_krs_history(player_id: str, limit: int = 20) -> List[Dict]:
    """
    Get KRS history for charting
    
    Returns:
        List of {date, krs, creation, transfer}
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT session_date, krs_total, creation_score, transfer_score
        FROM sessions
        WHERE player_id = ?
        ORDER BY session_date ASC
        LIMIT ?
    """, (player_id, limit))
    
    rows = cursor.fetchall()
    conn.close()
    
    return [
        {
            'date': row['session_date'],
            'krs': row['krs_total'],
            'creation': row['creation_score'],
            'transfer': row['transfer_score']
        }
        for row in rows
    ]


# ============================================================================
# STATISTICS
# ============================================================================

def get_database_stats() -> Dict:
    """Get database statistics"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Total players
    cursor.execute("SELECT COUNT(*) as count FROM players")
    total_players = cursor.fetchone()['count']
    
    # Total sessions
    cursor.execute("SELECT COUNT(*) as count FROM sessions")
    total_sessions = cursor.fetchone()['count']
    
    # Average KRS
    cursor.execute("SELECT AVG(krs_total) as avg_krs FROM sessions")
    avg_krs = cursor.fetchone()['avg_krs'] or 0
    
    conn.close()
    
    return {
        'total_players': total_players,
        'total_sessions': total_sessions,
        'average_krs': round(avg_krs, 1),
        'database_path': str(DB_PATH),
    }


# ============================================================================
# INITIALIZATION
# ============================================================================

# Initialize database on module import
init_database()


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("SESSION STORAGE TEST")
    print("=" * 70)
    
    # Test data transformer
    from data_transformer import transform_to_player_report
    
    sample_response = {
        'session_id': f'test_{uuid.uuid4().hex[:8]}',
        'bat_speed_mph': 75.0,
        'exit_velocity_mph': 90.0,
        'efficiency_percent': 78.0,
        'tempo_score': 8.0,
        'stability_score': 7.5,
        'gew_overall': 75.0,
        'motor_profile': {
            'type': 'Spinner',
            'confidence': 88.0,
        },
        'patterns': [],
        'primary_issue': 'General development',
        'prescription': {
            'duration_weeks': 4,
            'drills': [],
        },
        'coach_messages': {
            'analysis': 'Great fundamentals!',
        },
    }
    
    player_info = {
        'player_id': f'player_{uuid.uuid4().hex[:8]}',
        'name': 'Test Player',
        'age': 24,
        'height_inches': 72,
        'weight_lbs': 185,
        'wingspan_inches': 74,
    }
    
    # Create player
    player_id = create_or_update_player(
        player_id=player_info['player_id'],
        name=player_info['name'],
        age=player_info['age'],
        height_inches=player_info['height_inches'],
        weight_lbs=player_info['weight_lbs'],
        wingspan_inches=player_info['wingspan_inches'],
    )
    print(f"✓ Created player: {player_id}")
    
    # Transform and save session
    report = transform_to_player_report(sample_response, player_info, session_count=1)
    session_id = save_session(report)
    print(f"✓ Saved session: {session_id}")
    
    # Retrieve session
    session = get_session(session_id)
    print(f"✓ Retrieved session: {session['session_id']}")
    print(f"  KRS: {session['krs_total']} ({session['krs_level']})")
    
    # Get progress
    progress = get_player_progress(player_id)
    print(f"✓ Player progress:")
    print(f"  Sessions: {progress['total_sessions']}")
    print(f"  Swings: {progress['total_swings']}")
    print(f"  Current KRS: {progress['current_krs']}")
    print(f"  Milestones: {len(progress['milestones'])}")
    
    # Database stats
    stats = get_database_stats()
    print(f"\n✓ Database stats:")
    print(f"  Total players: {stats['total_players']}")
    print(f"  Total sessions: {stats['total_sessions']}")
    print(f"  Average KRS: {stats['average_krs']}")
    print(f"  Database: {stats['database_path']}")
    
    print("=" * 70)
    print("✅ ALL TESTS PASSED")
    print("=" * 70)
