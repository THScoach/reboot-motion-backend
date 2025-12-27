#!/usr/bin/env python3
"""
Check what data is actually available for analysis
"""

import sys
from database import SessionLocal
from models import Player, Session
from sync_service import RebootMotionSync
import json

def main():
    print("=" * 70)
    print("🔍 CHECKING AVAILABLE DATA FOR ANALYSIS")
    print("=" * 70)
    
    # Initialize
    sync = RebootMotionSync(
        username='coachrickpd@gmail.com',
        password='Train@2025'
    )
    
    db = SessionLocal()
    
    try:
        # Check local database
        print("\n📊 LOCAL DATABASE STATUS:")
        player_count = db.query(Player).count()
        session_count = db.query(Session).count()
        print(f"   Players: {player_count}")
        print(f"   Sessions: {session_count}")
        
        # Get Connor Gray
        connor = db.query(Player).filter(
            Player.first_name == 'Connor',
            Player.last_name == 'Gray'
        ).first()
        
        if connor:
            print(f"\n✅ Found Connor Gray:")
            print(f"   Player ID: {connor.id}")
            print(f"   Org Player ID: {connor.org_player_id}")
            
            # Get his sessions
            sessions = db.query(Session).filter(Session.player_id == connor.id).all()
            print(f"\n📋 Connor's Sessions ({len(sessions)} total):")
            
            for i, session in enumerate(sessions, 1):
                print(f"\n   Session {i}:")
                print(f"      ID: {session.session_id}")
                print(f"      Date: {session.session_date}")
                print(f"      Movement: {session.movement_type_name}")
                print(f"      Data Synced: {session.data_synced}")
                
                # Try to get session details from API
                print(f"\n      🔍 Checking API for session details...")
                try:
                    session_detail = sync._make_request(f'/sessions/{session.session_id}')
                    
                    # Check what data is available
                    print(f"      ✅ Session details available:")
                    print(f"         Status: {session_detail.get('status')}")
                    print(f"         Num movements: {session_detail.get('num_movements', 0)}")
                    print(f"         Total movements: {session_detail.get('total_movements', {})}")
                    
                    # Check for movements/swings
                    if 'movements' in session_detail:
                        movements = session_detail.get('movements', [])
                        print(f"         Available movements: {len(movements)}")
                        if movements and len(movements) > 0:
                            print(f"\n         Sample movement data:")
                            print(f"         {json.dumps(movements[0], indent=10)[:500]}...")
                    
                except Exception as e:
                    print(f"      ❌ Error: {e}")
                
                # Try to get processed data
                print(f"\n      🔍 Checking for processed/biomechanics data...")
                try:
                    processed = sync._make_request(
                        f'/processed_data',
                        params={
                            'session_id': session.session_id,
                            'movement_type_id': 1,
                            'org_player_id': connor.org_player_id
                        }
                    )
                    print(f"      ✅ Processed data available!")
                    print(f"         Keys: {list(processed.keys())[:10]}")
                except Exception as e:
                    print(f"      ❌ Processed data not available: {str(e)[:100]}")
        
        print("\n" + "=" * 70)
        print("✅ DATA CHECK COMPLETE")
        print("=" * 70)
        
    finally:
        db.close()

if __name__ == "__main__":
    main()
