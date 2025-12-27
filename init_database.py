#!/usr/bin/env python3
"""
Initialize Database Tables
Creates all required tables for Reboot Motion data sync
"""

import sys
import os
from pathlib import Path

# Add parent directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from database import engine, SessionLocal
from models import Base, Player, Session, BiomechanicsData, SyncLog, PlayerReport

def init_database():
    """
    Initialize all database tables
    """
    print("=" * 70)
    print("🚀 DATABASE INITIALIZATION")
    print("=" * 70)
    
    try:
        # Create all tables
        print("\n📊 Creating database tables...")
        Base.metadata.create_all(bind=engine)
        
        # Verify tables exist
        db = SessionLocal()
        try:
            # Test queries
            player_count = db.query(Player).count()
            session_count = db.query(Session).count()
            sync_log_count = db.query(SyncLog).count()
            
            print(f"\n✅ Database initialized successfully!")
            print(f"   - Players table: {player_count} records")
            print(f"   - Sessions table: {session_count} records")
            print(f"   - Sync logs: {sync_log_count} records")
            
        finally:
            db.close()
        
        print("\n" + "=" * 70)
        print("✅ INITIALIZATION COMPLETE")
        print("=" * 70)
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = init_database()
    sys.exit(0 if success else 1)
