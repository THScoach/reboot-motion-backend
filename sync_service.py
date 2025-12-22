"""
Reboot Motion API Sync Service
Syncs players, sessions, and biomechanics data from Reboot Motion API
"""

import os
import requests
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Player, Session as SessionModel, BiomechanicsData, SyncLog

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
REBOOT_USERNAME = os.environ.get('REBOOT_USERNAME')
REBOOT_PASSWORD = os.environ.get('REBOOT_PASSWORD')
REBOOT_BASE_URL = 'https://api.rebootmotion.com'


class RebootMotionSync:
    """Service to sync data from Reboot Motion API using OAuth 2.0 authentication"""
    
    def __init__(self, username: Optional[str] = None, password: Optional[str] = None, db_session: Optional[Session] = None):
        """
        Initialize the sync service with OAuth credentials.
        
        Args:
            username: Reboot Motion username (or uses REBOOT_USERNAME env var)
            password: Reboot Motion password (or uses REBOOT_PASSWORD env var)
            db_session: Optional SQLAlchemy database session
        """
        # Use provided credentials or fall back to environment variables
        self.username = username or REBOOT_USERNAME
        self.password = password or REBOOT_PASSWORD
        
        if not self.username or not self.password:
            raise ValueError("REBOOT_USERNAME and REBOOT_PASSWORD must be provided or set as environment variables!")
        
        self.base_url = REBOOT_BASE_URL
        self.db_session = db_session
        self.access_token = None
        self.refresh_token = None
        self.token_expires_at = None
    
    def _get_access_token(self) -> str:
        """
        Get OAuth access token using Resource Owner Password flow.
        Caches the token and refreshes when needed.
        
        Returns:
            str: Valid access token
        """
        # Check if we have a valid cached token
        if self.access_token and self.token_expires_at:
            if datetime.utcnow() < self.token_expires_at - timedelta(minutes=5):
                return self.access_token
        
        # Request new token
        logger.info("🔑 Requesting OAuth access token...")
        
        try:
            response = requests.post(
                f"{self.base_url}/oauth/token",
                headers={
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                json={
                    'username': self.username,
                    'password': self.password
                },
                timeout=30
            )
            response.raise_for_status()
            
            token_data = response.json()
            self.access_token = token_data['access_token']
            self.refresh_token = token_data.get('refresh_token')
            
            # Access tokens expire after 24 hours
            self.token_expires_at = datetime.utcnow() + timedelta(hours=23, minutes=55)
            
            logger.info("✅ OAuth token obtained successfully")
            return self.access_token
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Failed to obtain OAuth token: {e}")
            raise
    
    def _make_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None, method: str = 'GET') -> Any:
        """
        Make authenticated HTTP request to Reboot Motion API.
        
        Args:
            endpoint: API endpoint (e.g., '/players')
            params: Optional query parameters
            method: HTTP method (GET, POST, etc.)
        
        Returns:
            JSON response data
        """
        url = f"{self.base_url}{endpoint}"
        token = self._get_access_token()
        
        headers = {
            'Authorization': f'Bearer {token}',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, params=params, timeout=30)
            elif method == 'POST':
                response = requests.post(url, headers=headers, json=params, timeout=30)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ API request failed for {endpoint}: {e}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Response: {e.response.text}")
            raise
    
    def sync_players(self, db: Session) -> int:
        """
        Sync all players from Reboot Motion API.
        
        Args:
            db: SQLAlchemy database session
        
        Returns:
            int: Number of players synced
        """
        logger.info("🔄 Syncing players...")
        
        try:
            # Get players from API
            players_data = self._make_request('/players')
            
            if not isinstance(players_data, list):
                logger.error(f"Expected list of players, got: {type(players_data)}")
                return 0
            
            synced_count = 0
            
            for player_data in players_data:
                org_player_id = player_data.get('org_player_id')
                if not org_player_id:
                    continue
                
                # Check if player exists
                player = db.query(Player).filter(Player.org_player_id == org_player_id).first()
                
                if player:
                    # Update existing player
                    player.reboot_player_id = player_data.get('reboot_player_id', player.reboot_player_id)
                    player.first_name = player_data.get('first_name', player.first_name)
                    player.last_name = player_data.get('last_name', player.last_name)
                    player.date_of_birth = player_data.get('date_of_birth', player.date_of_birth)
                    player.height_ft = player_data.get('height_ft', player.height_ft)
                    player.weight_lbs = player_data.get('weight_lbs', player.weight_lbs)
                    player.dominant_hand_hitting = player_data.get('dominant_hand_hitting', player.dominant_hand_hitting)
                    player.dominant_hand_throwing = player_data.get('dominant_hand_throwing', player.dominant_hand_throwing)
                    player.updated_at = datetime.utcnow()
                else:
                    # Create new player
                    player = Player(
                        org_player_id=org_player_id,
                        reboot_player_id=player_data.get('reboot_player_id'),
                        first_name=player_data.get('first_name'),
                        last_name=player_data.get('last_name'),
                        date_of_birth=player_data.get('date_of_birth'),
                        height_ft=player_data.get('height_ft'),
                        weight_lbs=player_data.get('weight_lbs'),
                        dominant_hand_hitting=player_data.get('dominant_hand_hitting'),
                        dominant_hand_throwing=player_data.get('dominant_hand_throwing')
                    )
                    db.add(player)
                
                synced_count += 1
            
            db.commit()
            logger.info(f"✅ Synced {synced_count} players")
            return synced_count
            
        except Exception as e:
            db.rollback()
            logger.error(f"❌ Error syncing players: {e}")
            raise
    
    def sync_sessions(self, db: Session, days_back: int = 30, limit: int = 200) -> int:
        """
        Sync HITTING sessions and determine actual participants using /processed_data endpoint.
        Only creates session records for players who actually have data.
        
        Args:
            db: SQLAlchemy database session
            days_back: How many days back to sync (default: 30)
            limit: Max sessions to fetch per request (default: 200)
        
        Returns:
            int: Number of session records created
        """
        logger.info(f"🔄 Syncing HITTING sessions (last {days_back} days)...")
        
        try:
            # Get all sessions from the API
            sessions_data = self._make_request('/sessions', params={'limit': limit})
            
            if not isinstance(sessions_data, list):
                logger.error(f"Expected list of sessions, got: {type(sessions_data)}")
                return 0
            
            logger.info(f"📊 API returned {len(sessions_data)} total sessions")
            
            # Log first session for debugging
            if sessions_data:
                logger.info(f"🔍 Sample session data: {sessions_data[0]}")
            
            # Filter for hitting sessions - includes both single camera and Hawkeye
            # Session types: "hitting-lite-processed-metrics" (single camera) and "hitting-processed-metrics" (Hawkeye)
            cutoff_date = datetime.utcnow() - timedelta(days=days_back)
            hitting_sessions = []
            
            # Define hitting session identifiers
            hitting_type_ids = [1]  # movement_type_id for hitting
            hitting_session_types = [
                'hitting-lite-processed-metrics',  # Single camera
                'hitting-processed-metrics',        # Hawkeye
                'hitting'                           # Generic hitting
            ]
            
            for session in sessions_data:
                # Extract session identifiers
                session_id = session.get('id', 'unknown')
                session_type_id = session.get('session_type_id')
                movement_type_id = session.get('movement_type_id')
                
                # Handle session_type and session_type_slug - they might be strings or dicts
                session_type_raw = session.get('session_type', '')
                session_type_slug_raw = session.get('session_type_slug', '')
                
                # Convert to string if needed
                if isinstance(session_type_raw, dict):
                    session_type = str(session_type_raw.get('name', '') or session_type_raw.get('slug', '')).lower()
                else:
                    session_type = str(session_type_raw).lower() if session_type_raw else ''
                
                if isinstance(session_type_slug_raw, dict):
                    session_type_slug = str(session_type_slug_raw.get('slug', '') or session_type_slug_raw.get('name', '')).lower()
                else:
                    session_type_slug = str(session_type_slug_raw).lower() if session_type_slug_raw else ''
                
                logger.info(f"🔍 Checking session {session_id[:8] if isinstance(session_id, str) else session_id}: "
                           f"session_type_id={session_type_id}, movement_type_id={movement_type_id}, "
                           f"session_type='{session_type}', session_type_slug='{session_type_slug}'")
                
                # Check if it's a hitting session by ID, type name, or slug
                is_hitting = (
                    session_type_id in hitting_type_ids or
                    movement_type_id in hitting_type_ids or
                    session_type in hitting_session_types or
                    session_type_slug in hitting_session_types or
                    'hitting' in session_type or
                    'hitting' in session_type_slug
                )
                
                if is_hitting:
                    # Check date if available
                    session_date_str = session.get('session_date')
                    if session_date_str:
                        try:
                            session_date = datetime.fromisoformat(session_date_str.replace('Z', '+00:00'))
                            if session_date >= cutoff_date:
                                hitting_sessions.append(session)
                        except ValueError:
                            # If date parsing fails, include it anyway
                            hitting_sessions.append(session)
                    else:
                        # No date info, include it
                        hitting_sessions.append(session)
            
            logger.info(f"🏏 Filtered to {len(hitting_sessions)} HITTING sessions in date range")
            
            # Get all players
            players = db.query(Player).all()
            logger.info(f"📊 Found {len(players)} players in database")
            
            total_sessions_created = 0
            total_skipped_exists = 0
            total_skipped_no_data = 0
            
            # Process each HITTING session
            for session_data in hitting_sessions:
                session_id = session_data.get('id')
                if not session_id:
                    continue
                
                session_date = None
                if session_data.get('session_date'):
                    try:
                        session_date = datetime.fromisoformat(session_data['session_date'].replace('Z', '+00:00'))
                    except ValueError:
                        pass
                
                # For Pipeline v2 (single camera), /processed_data doesn't work
                # Instead, we'll use /reports to find which sessions have data
                # Query reports for this session
                logger.info(f"📋 Checking reports for session {session_id[:8]}...")
                
                try:
                    # Get reports that might be associated with this session
                    # We'll check by date range around the session date
                    reports_params = {
                        'movement_types': [1],  # HITTING (must be a list)
                        'limit': 100
                    }
                    
                    # If we have a session date, filter reports by date
                    if session_date:
                        # Format date as YYYY-MM-DD
                        date_str = session_date.strftime('%Y-%m-%d')
                        reports_params['created_at_from'] = date_str
                        reports_params['created_at_to'] = date_str
                    
                    reports = self._make_request('/reports', params=reports_params)
                    
                    # Check if any reports match this session
                    # Reports should have player info we can match
                    session_has_data = False
                    session_player_ids = set()
                    
                    if isinstance(reports, list):
                        for report in reports:
                            # Check if this report belongs to this session
                            # The report might have session_id or we match by date/player
                            report_session_id = report.get('session_id') or report.get('mocap_session_id')
                            
                            if report_session_id == session_id:
                                session_has_data = True
                                # Extract player identifiers from report
                                org_player_id = report.get('org_player_id')
                                if org_player_id:
                                    session_player_ids.add(org_player_id)
                    
                    # Create session records for players found in reports
                    if session_has_data and session_player_ids:
                        logger.info(f"📊 Found {len(session_player_ids)} players with reports for session {session_id[:8]}")
                        
                        for player in players:
                            if player.org_player_id not in session_player_ids:
                                continue
                            
                            # Check if session record already exists
                            existing_session = db.query(SessionModel).filter(
                                SessionModel.session_id == session_id,
                                SessionModel.player_id == player.id
                            ).first()
                            
                            if existing_session:
                                total_skipped_exists += 1
                                continue
                            
                            # Create session record
                            new_session = SessionModel(
                                session_id=session_id,
                                player_id=player.id,
                                session_date=session_date,
                                movement_type_id=1,  # Hitting
                                movement_type_name='Hitting',
                                data_synced=False
                            )
                            db.add(new_session)
                            total_sessions_created += 1
                            logger.info(f"✅ Created session record: {player.first_name} {player.last_name} - {session_id[:8]}")
                    else:
                        logger.info(f"ℹ️ No reports found for session {session_id[:8]}, skipping...")
                        total_skipped_no_data += 1
                
                except requests.exceptions.HTTPError as e:
                    logger.warning(f"⚠️ Error checking reports for session {session_id}: {e}")
                    total_skipped_no_data += 1
                except Exception as e:
                    logger.error(f"❌ Error processing session {session_id}: {e}")
                    total_skipped_no_data += 1
            
            db.commit()
            logger.info(f"✅ Created {total_sessions_created} session records")
            logger.info(f"📊 Skipped: {total_skipped_exists} (already exist), {total_skipped_no_data} (no data)")
            return total_sessions_created
            
        except Exception as e:
            db.rollback()
            logger.error(f"❌ Error syncing sessions: {e}")
            raise
    
    def sync_biomechanics_data(self, db: Session, limit: int = 50) -> int:
        """
        Sync biomechanics data for sessions that don't have data yet.
        Uses /processed_data endpoint to fetch detailed movement data.
        
        Args:
            db: SQLAlchemy database session
            limit: Max number of sessions to process in this run
        
        Returns:
            int: Number of biomechanics records created
        """
        logger.info("🔄 Syncing biomechanics data...")
        
        try:
            # Find sessions that need data synced
            sessions_to_sync = db.query(SessionModel).filter(
                SessionModel.data_synced == False
            ).limit(limit).all()
            
            if not sessions_to_sync:
                logger.info("✅ No sessions need biomechanics data sync")
                return 0
            
            logger.info(f"📊 Found {len(sessions_to_sync)} sessions to sync")
            
            total_records_created = 0
            
            for session in sessions_to_sync:
                try:
                    player = session.player
                    
                    # Fetch processed data for this session and player
                    processed_data = self._make_request('/processed_data', params={
                        'session_id': session.session_id,
                        'movement_type_id': session.movement_type_id,
                        'org_player_id': player.org_player_id
                    })
                    
                    if not processed_data:
                        logger.warning(f"⚠️ No processed data for session {session.session_id}, player {player.org_player_id}")
                        session.data_synced = True  # Mark as synced even if no data
                        continue
                    
                    # Process the biomechanics data
                    # The structure varies, but typically contains movements or frames
                    records_created = self._process_biomechanics_data(db, session, processed_data)
                    total_records_created += records_created
                    
                    # Mark session as synced
                    session.data_synced = True
                    logger.info(f"✅ Synced {records_created} records for {player.first_name} {player.last_name} - {session.session_id[:8]}")
                
                except requests.exceptions.HTTPError as e:
                    if hasattr(e, 'response') and e.response is not None and e.response.status_code == 404:
                        # No data available, mark as synced
                        session.data_synced = True
                        logger.info(f"ℹ️ No data available for session {session.session_id}")
                    else:
                        logger.error(f"❌ Error syncing biomechanics for session {session.session_id}: {e}")
                        continue
                
                except Exception as e:
                    logger.error(f"❌ Error processing biomechanics for session {session.session_id}: {e}")
                    continue
            
            db.commit()
            logger.info(f"✅ Created {total_records_created} biomechanics records")
            return total_records_created
            
        except Exception as e:
            db.rollback()
            logger.error(f"❌ Error syncing biomechanics data: {e}")
            raise
    
    def _process_biomechanics_data(self, db: Session, session: SessionModel, data: Any) -> int:
        """
        Process and store biomechanics data from API response.
        
        Args:
            db: Database session
            session: Session model instance
            data: Raw data from /processed_data endpoint
        
        Returns:
            int: Number of records created
        """
        records_created = 0
        
        try:
            # Handle different response structures
            if isinstance(data, dict):
                # Single movement or summary data
                if 'movements' in data:
                    movements = data['movements']
                elif 'data' in data:
                    movements = data['data']
                else:
                    # Treat the whole dict as a single movement
                    movements = [data]
            elif isinstance(data, list):
                movements = data
            else:
                logger.warning(f"⚠️ Unexpected data type: {type(data)}")
                return 0
            
            # Process each movement
            for idx, movement in enumerate(movements):
                if not isinstance(movement, dict):
                    continue
                
                # Extract relevant biomechanics data
                # This structure depends on the actual API response
                biomech_record = BiomechanicsData(
                    session_id=session.id,
                    frame_number=idx,
                    timestamp=datetime.utcnow(),  # Use current time if not provided
                    joint_angles=movement.get('joint_angles', {}),
                    joint_positions=movement.get('joint_positions', {}),
                    joint_velocities=movement.get('joint_velocities', {})
                )
                
                # If the API provides more structured data, extract it
                if 'kinematic_sequence' in movement:
                    biomech_record.joint_angles['kinematic_sequence'] = movement['kinematic_sequence']
                
                if 'metrics' in movement:
                    biomech_record.joint_angles['metrics'] = movement['metrics']
                
                # Store the entire movement data for reference
                if not biomech_record.joint_angles:
                    biomech_record.joint_angles = movement
                
                db.add(biomech_record)
                records_created += 1
            
            return records_created
            
        except Exception as e:
            logger.error(f"❌ Error processing biomechanics data: {e}")
            return records_created
    
    async def sync_all_data(self) -> Dict[str, Any]:
        """
        Run full sync: players, sessions, and biomechanics data (async version for FastAPI).
        
        Returns:
            dict: Sync results
        """
        # Use provided db_session or create new one
        db = self.db_session if self.db_session else SessionLocal()
        
        try:
            logger.info("🚀 Starting full sync...")
            
            # Sync players
            players_synced = self.sync_players(db)
            
            # Sync sessions (with correct participant detection)
            sessions_synced = self.sync_sessions(db)
            
            # Sync biomechanics data
            biomechanics_synced = self.sync_biomechanics_data(db)
            
            logger.info(f"✅ Full sync completed: {players_synced} players, {sessions_synced} sessions, {biomechanics_synced} biomechanics records")
            
            return {
                'players_synced': players_synced,
                'sessions_synced': sessions_synced,
                'biomechanics_synced': biomechanics_synced,
                'status': 'success'
            }
            
        except Exception as e:
            logger.error(f"❌ Full sync failed: {e}")
            raise
        finally:
            # Only close if we created the session
            if not self.db_session:
                db.close()
    
    def full_sync(self) -> Dict[str, Any]:
        """
        Run full sync: players, sessions, and biomechanics data.
        
        Returns:
            dict: Sync results
        """
        db = SessionLocal()
        
        # Create sync log entry
        sync_log = SyncLog(
            sync_type='full_sync',
            status='in_progress',
            started_at=datetime.utcnow()
        )
        db.add(sync_log)
        db.commit()
        
        try:
            logger.info("🚀 Starting full sync...")
            
            # Sync players
            players_synced = self.sync_players(db)
            
            # Sync sessions
            sessions_synced = self.sync_sessions(db)
            
            # Sync biomechanics data
            biomechanics_synced = self.sync_biomechanics_data(db)
            
            # Update sync log
            sync_log.status = 'success'
            sync_log.records_synced = players_synced + sessions_synced + biomechanics_synced
            sync_log.players_synced = players_synced
            sync_log.sessions_synced = sessions_synced
            sync_log.biomechanics_synced = biomechanics_synced
            sync_log.completed_at = datetime.utcnow()
            db.commit()
            
            logger.info(f"✅ Full sync completed: {players_synced} players, {sessions_synced} sessions, {biomechanics_synced} biomechanics records")
            
            return {
                'players_synced': players_synced,
                'sessions_synced': sessions_synced,
                'biomechanics_synced': biomechanics_synced,
                'status': 'success'
            }
            
        except Exception as e:
            sync_log.status = 'failed'
            sync_log.error_message = str(e)
            sync_log.completed_at = datetime.utcnow()
            db.commit()
            logger.error(f"❌ Full sync failed: {e}")
            raise
        finally:
            db.close()


def run_sync():
    """Run sync from command line"""
    sync = RebootMotionSync()  # Will use env variables
    result = sync.full_sync()
    print(f"✅ Sync complete: {result}")


if __name__ == "__main__":
    run_sync()
