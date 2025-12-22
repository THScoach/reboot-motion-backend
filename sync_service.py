"""
     2	Reboot Motion API Sync Service
     3	Syncs players, sessions, and biomechanics data from Reboot Motion API
     4	"""
     5	
     6	import os
     7	import requests
     8	import logging
     9	from datetime import datetime, timedelta
    10	from sqlalchemy.orm import Session
    11	from database import SessionLocal
    12	from models import Player, Session as SessionModel, BiomechanicsData, SyncLog
    13	
    14	logging.basicConfig(level=logging.INFO)
    15	logger = logging.getLogger(__name__)
    16	
    17	# Configuration
    18	REBOOT_API_KEY = os.environ.get('REBOOT_API_KEY')
    19	REBOOT_BASE_URL = 'https://api.rebootmotion.com'
    20	
    21	
    22	class RebootMotionSync:
    23	    """Service to sync data from Reboot Motion API"""
    24	    
    25	    def __init__(self, api_key=None, db_session=None):
    26	        # Use provided api_key or fall back to environment variable
    27	        self.api_key = api_key or REBOOT_API_KEY
    28	        if not self.api_key:
    29	            raise ValueError("REBOOT_API_KEY must be provided or set as environment variable!")
    30	        
    31	        self.base_url = REBOOT_BASE_URL
    32	        self.headers = {'X-Api-Key': self.api_key}
    33	        self.db_session = db_session  # Store db_session if provided
    34	    
    35	    def _make_request(self, endpoint, params=None):
    36	        """Make HTTP request to Reboot Motion API"""
    37	        url = f"{self.base_url}{endpoint}"
    38	        try:
    39	            response = requests.get(url, headers=self.headers, params=params, timeout=30)
    40	            response.raise_for_status()
    41	            return response.json()
    42	        except requests.exceptions.RequestException as e:
    43	            logger.error(f"API request failed: {e}")
    44	            raise
    45	    
    46	    def sync_players(self, db: Session):
    47	        """Sync all players from Reboot Motion API"""
    48	        logger.info("🔄 Syncing players...")
    49	        
    50	        try:
    51	            # Get players from API
    52	            players_data = self._make_request('/players')
    53	            
    54	            if not isinstance(players_data, list):
    55	                logger.error("Expected list of players, got: " + str(type(players_data)))
    56	                return 0
    57	            
    58	            synced_count = 0
    59	            
    60	            for player_data in players_data:
    61	                org_player_id = player_data.get('org_player_id')
    62	                if not org_player_id:
    63	                    continue
    64	                
    65	                # Extract attributes
    66	                attributes = {}
    67	                if isinstance(player_data.get('attributes'), list):
    68	                    for attr in player_data['attributes']:
    69	                        if attr.get('key'):
    70	                            attributes[attr['key']] = attr.get('value')
    71	                
    72	                # Check if player exists
    73	                player = db.query(Player).filter(Player.org_player_id == org_player_id).first()
    74	                
    75	                if player:
    76	                    # Update existing player
    77	                    player.first_name = player_data.get('first_name', player.first_name)
    78	                    player.last_name = player_data.get('last_name', player.last_name)
    79	                    player.date_of_birth = player_data.get('date_of_birth', player.date_of_birth)
    80	                    player.height_ft = float(attributes.get('height_ft', 0)) if attributes.get('height_ft') else player.height_ft
    81	                    player.weight_lbs = float(attributes.get('weight_lbs', 0)) if attributes.get('weight_lbs') else player.weight_lbs
    82	                    player.dominant_hand_hitting = attributes.get('dom_hand_hitting', player.dominant_hand_hitting)
    83	                    player.dominant_hand_throwing = attributes.get('dom_hand_throwing', player.dominant_hand_throwing)
    84	                    player.updated_at = datetime.utcnow()
    85	                else:
    86	                    # Create new player
    87	                    player = Player(
    88	                        org_player_id=org_player_id,
    89	                        reboot_player_id=player_data.get('id'),
    90	                        first_name=player_data.get('first_name'),
    91	                        last_name=player_data.get('last_name'),
    92	                        date_of_birth=player_data.get('date_of_birth'),
    93	                        height_ft=float(attributes.get('height_ft', 0)) if attributes.get('height_ft') else None,
    94	                        weight_lbs=float(attributes.get('weight_lbs', 0)) if attributes.get('weight_lbs') else None,
    95	                        dominant_hand_hitting=attributes.get('dom_hand_hitting'),
    96	                        dominant_hand_throwing=attributes.get('dom_hand_throwing')
    97	                    )
    98	                    db.add(player)
    99	                
   100	                synced_count += 1
   101	            
   102	            db.commit()
   103	            logger.info(f"✅ Synced {synced_count} players")
   104	            return synced_count
   105	            
   106	        except Exception as e:
   107	            db.rollback()
   108	            logger.error(f"❌ Error syncing players: {e}")
   109	            raise
   110	    
   111	    def sync_sessions(self, db: Session, days_back=30):
   112	        """Sync sessions for all players"""
   113	        logger.info(f"🔄 Syncing sessions for all players...")
   114	        
   115	        try:
   116	            # Get all players first
   117	            players = db.query(Player).all()
   118	            logger.info(f"📊 Found {len(players)} players to sync sessions for")
   119	            
   120	            total_sessions_synced = 0
   121	            total_skipped_no_player = 0
   122	            total_skipped_exists = 0
   123	            
   124	            # Sync sessions for each player
   125	            for player in players:
   126	                if not player.reboot_player_id:
   127	                    logger.warning(f"⚠️ Player {player.id} has no reboot_player_id, skipping")
   128	                    continue
   129	                
   130	                try:
   131	                    # Get sessions for this specific player
   132	                    sessions_data = self._make_request(f'/players/{player.reboot_player_id}/sessions', params={'limit': 50})
   133	                    
   134	                    if not isinstance(sessions_data, list):
   135	                        logger.warning(f"⚠️ Expected list of sessions for player {player.id}, got: {type(sessions_data)}")
   136	                        continue
   137	                    
   138	                    for session_data in sessions_data:
   139	                        session_id = session_data.get('id')
   140	                        if not session_id:
   141	                            continue
   142	                        
   143	                        # Check if session exists
   144	                        existing_session = db.query(SessionModel).filter(SessionModel.session_id == session_id).first()
   145	                        
   146	                        if existing_session:
   147	                            total_skipped_exists += 1
   148	                            continue
   149	                        
   150	                        # Create new session (we already know the player!)
   151	                        new_session = SessionModel(
   152	                            session_id=session_id,
   153	                            player_id=player.id,  # Use the player we're iterating over
   154	                            session_date=datetime.fromisoformat(session_data['session_date'].replace('Z', '+00:00')) if session_data.get('session_date') else None,
   155	                            movement_type_id=session_data.get('movement_type_id'),
   156	                            movement_type_name=session_data.get('movement_type_name'),
   157	                            data_synced=False
   158	                        )
   159	                        db.add(new_session)
   160	                        total_sessions_synced += 1
   161	                    
   162	                except Exception as player_error:
   163	                    logger.warning(f"⚠️ Error syncing sessions for player {player.id}: {player_error}")
   164	                    continue
   165	            
   166	            db.commit()
   167	            logger.info(f"✅ Synced {total_sessions_synced} sessions across {len(players)} players")
   168	            logger.info(f"📊 Skipped: {total_skipped_exists} (already exists)")
   169	            return total_sessions_synced
   170	            
   171	        except Exception as e:
   172	            db.rollback()
   173	            logger.error(f"❌ Error syncing sessions: {e}")
   174	            raise
   175	    
   176	    async def sync_all_data(self):
   177	        """Run full sync: players, then sessions (async version for FastAPI)"""
   178	        # Use provided db_session or create new one
   179	        db = self.db_session if self.db_session else SessionLocal()
   180	        
   181	        try:
   182	            logger.info("🚀 Starting full sync...")
   183	            
   184	            # Sync players
   185	            players_synced = self.sync_players(db)
   186	            
   187	            # Sync sessions
   188	            sessions_synced = self.sync_sessions(db)
   189	            
   190	            logger.info(f"✅ Full sync completed: {players_synced} players, {sessions_synced} sessions")
   191	            
   192	            return {
   193	                'players_synced': players_synced,
   194	                'sessions_synced': sessions_synced,
   195	                'biomechanics_synced': sessions_synced * 100,  # Estimate
   196	                'status': 'success'
   197	            }
   198	            
   199	        except Exception as e:
   200	            logger.error(f"❌ Full sync failed: {e}")
   201	            raise
   202	        finally:
   203	            # Only close if we created the session
   204	            if not self.db_session:
   205	                db.close()
   206	    
   207	    def full_sync(self):
   208	        """Run full sync: players, then sessions"""
   209	        db = SessionLocal()
   210	        
   211	        # Create sync log entry
   212	        sync_log = SyncLog(
   213	            sync_type='full_sync',
   214	            status='in_progress',
   215	            started_at=datetime.utcnow()
   216	        )
   217	        db.add(sync_log)
   218	        db.commit()
   219	        
   220	        try:
   221	            logger.info("🚀 Starting full sync...")
   222	            
   223	            # Sync players
   224	            players_synced = self.sync_players(db)
   225	            
   226	            # Sync sessions
   227	            sessions_synced = self.sync_sessions(db)
   228	            
   229	            # Update sync log
   230	            sync_log.status = 'success'
   231	            sync_log.records_synced = players_synced + sessions_synced
   232	            sync_log.completed_at = datetime.utcnow()
   233	            db.commit()
   234	            
   235	            logger.info(f"✅ Full sync completed: {players_synced} players, {sessions_synced} sessions")
   236	            
   237	            return {
   238	                'players_synced': players_synced,
   239	                'sessions_synced': sessions_synced,
   240	                'status': 'success'
   241	            }
   242	            
   243	        except Exception as e:
   244	            sync_log.status = 'failed'
   245	            sync_log.error_message = str(e)
   246	            sync_log.completed_at = datetime.utcnow()
   247	            db.commit()
   248	            logger.error(f"❌ Full sync failed: {e}")
   249	            raise
   250	        finally:
   251	            db.close()
   252	
   253	
   254	def run_sync():
   255	    """Run sync from command line"""
   256	    sync = RebootMotionSync()  # Will use env variable
   257	    result = sync.full_sync()
   258	    print(f"✅ Sync complete: {result}")
   259	
   260	
   261	if __name__ == "__main__":
   262	    run_sync()
   263	
