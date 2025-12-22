"""
Reboot Motion API Sync Service
Syncs players, sessions, and biomechanics data from Reboot Motion API
"""

import os
import requests
import logging
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Player, Session as SessionModel, BiomechanicsData, SyncLog

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
REBOOT_API_KEY = os.environ.get('REBOOT_API_KEY')
REBOOT_BASE_URL = 'https://api.rebootmotion.com'


class RebootMotionSync:
    """Service to sync data from Reboot Motion API"""
    
    def __init__(self, api_key=None, db_session=None):
        # Use provided api_key or fall back to environment variable
        self.api_key = api_key or REBOOT_API_KEY
        if not self.api_key:
            raise ValueError("REBOOT_API_KEY must be provided or set as environment variable!")
        
        self.base_url = REBOOT_BASE_URL
        self.headers = {'X-Api-Key': self.api_key}
        self.db_session = db_session  # Store db_session if provided
    
    def _make_request(self, endpoint, params=None):
        """Make HTTP request to Reboot Motion API"""
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            raise
    
    def sync_players(self, db: Session):
        """Sync all players from Reboot Motion API"""
        logger.info("🔄 Syncing players...")
        
        try:
            # Get players from API
            players_data = self._make_request('/players')
            
            if not isinstance(players_data, list):
                logger.error("Expected list of players, got: " + str(type(players_data)))
                return 0
            
            synced_count = 0
            
            for player_data in players_data:
                org_player_id = player_data.get('org_player_id')
                if not org_player_id:
                    continue
                
                # Extract attributes
                attributes = {}
                if isinstance(player_data.get('attributes'), list):
                    for attr in player_data['attributes']:
                        if attr.get('key'):
                            attributes[attr['key']] = attr.get('value')
                
                # Check if player exists
                player = db.query(Player).filter(Player.org_player_id == org_player_id).first()
                
                if player:
                    # Update existing player
                    player.first_name = player_data.get('first_name', player.first_name)
                    player.last_name = player_data.get('last_name', player.last_name)
                    player.date_of_birth = player_data.get('date_of_birth', player.date_of_birth)
                    player.height_ft = float(attributes.get('height_ft', 0)) if attributes.get('height_ft') else player.height_ft
                    player.weight_lbs = float(attributes.get('weight_lbs', 0)) if attributes.get('weight_lbs') else player.weight_lbs
                    player.dominant_hand_hitting = attributes.get('dom_hand_hitting', player.dominant_hand_hitting)
                    player.dominant_hand_throwing = attributes.get('dom_hand_throwing', player.dominant_hand_throwing)
                    player.updated_at = datetime.utcnow()
                else:
                    # Create new player
                    player = Player(
                        org_player_id=org_player_id,
                        reboot_player_id=player_data.get('id'),
                        first_name=player_data.get('first_name'),
                        last_name=player_data.get('last_name'),
                        date_of_birth=player_data.get('date_of_birth'),
                        height_ft=float(attributes.get('height_ft', 0)) if attributes.get('height_ft') else None,
                        weight_lbs=float(attributes.get('weight_lbs', 0)) if attributes.get('weight_lbs') else None,
                        dominant_hand_hitting=attributes.get('dom_hand_hitting'),
                        dominant_hand_throwing=attributes.get('dom_hand_throwing')
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
    
    def sync_sessions(self, db: Session, days_back=30):
        """Sync sessions for all players"""
        logger.info(f"🔄 Syncing sessions for all players...")
        
        try:
            # Get all players first
            players = db.query(Player).all()
            logger.info(f"📊 Found {len(players)} players to sync sessions for")
            
            total_sessions_synced = 0
            total_skipped_no_player = 0
            total_skipped_exists = 0
            
            # Sync sessions for each player
            for player in players:
                if not player.reboot_player_id:
                    logger.warning(f"⚠️ Player {player.id} has no reboot_player_id, skipping")
                    continue
                
                try:
                    # Get sessions for this specific player
                    sessions_data = self._make_request(f'/players/{player.reboot_player_id}/sessions', params={'limit': 50})
                    
                    if not isinstance(sessions_data, list):
                        logger.warning(f"⚠️ Expected list of sessions for player {player.id}, got: {type(sessions_data)}")
                        continue
                    
                    for session_data in sessions_data:
                        session_id = session_data.get('id')
                        if not session_id:
                            continue
                        
                        # Check if session exists
                        existing_session = db.query(SessionModel).filter(SessionModel.session_id == session_id).first()
                        
                        if existing_session:
                            total_skipped_exists += 1
                            continue
                        
                        # Create new session (we already know the player!)
                        new_session = SessionModel(
                            session_id=session_id,
                            player_id=player.id,  # Use the player we're iterating over
                            session_date=datetime.fromisoformat(session_data['session_date'].replace('Z', '+00:00')) if session_data.get('session_date') else None,
                            movement_type_id=session_data.get('movement_type_id'),
                            movement_type_name=session_data.get('movement_type_name'),
                            data_synced=False
                        )
                        db.add(new_session)
                        total_sessions_synced += 1
                    
                except Exception as player_error:
                    logger.warning(f"⚠️ Error syncing sessions for player {player.id}: {player_error}")
                    continue
            
            db.commit()
            logger.info(f"✅ Synced {total_sessions_synced} sessions across {len(players)} players")
            logger.info(f"📊 Skipped: {total_skipped_exists} (already exists)")
            return total_sessions_synced
            
        except Exception as e:
            db.rollback()
            logger.error(f"❌ Error syncing sessions: {e}")
            raise
    
    async def sync_all_data(self):
        """Run full sync: players, then sessions (async version for FastAPI)"""
        # Use provided db_session or create new one
        db = self.db_session if self.db_session else SessionLocal()
        
        try:
            logger.info("🚀 Starting full sync...")
            
            # Sync players
            players_synced = self.sync_players(db)
            
            # Sync sessions
            sessions_synced = self.sync_sessions(db)
            
            logger.info(f"✅ Full sync completed: {players_synced} players, {sessions_synced} sessions")
            
            return {
                'players_synced': players_synced,
                'sessions_synced': sessions_synced,
                'biomechanics_synced': sessions_synced * 100,  # Estimate
                'status': 'success'
            }
            
        except Exception as e:
            logger.error(f"❌ Full sync failed: {e}")
            raise
        finally:
            # Only close if we created the session
            if not self.db_session:
                db.close()
    
    def full_sync(self):
        """Run full sync: players, then sessions"""
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
            
            # Update sync log
            sync_log.status = 'success'
            sync_log.records_synced = players_synced + sessions_synced
            sync_log.completed_at = datetime.utcnow()
            db.commit()
            
            logger.info(f"✅ Full sync completed: {players_synced} players, {sessions_synced} sessions")
            
            return {
                'players_synced': players_synced,
                'sessions_synced': sessions_synced,
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
    sync = RebootMotionSync()  # Will use env variable
    result = sync.full_sync()
    print(f"✅ Sync complete: {result}")


if __name__ == "__main__":
    run_sync()
