#!/usr/bin/env python3
"""
Reboot Motion Full Data Sync Script
====================================

Syncs all data from Reboot Motion API to PostgreSQL database:
- Players (100+)
- Sessions (all recent sessions)
- Biomechanics data (hitting data for each session)

Usage:
    python sync_reboot_data.py

Environment Variables Required:
    REBOOT_USERNAME - Reboot Motion username
    REBOOT_PASSWORD - Reboot Motion password
    DATABASE_URL - PostgreSQL connection string

Author: Builder 2
Date: 2025-12-26
"""

import os
import sys
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Run full Reboot Motion data sync"""
    
    print("=" * 70)
    print("🚀 REBOOT MOTION FULL DATA SYNC")
    print("=" * 70)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Check environment variables
    reboot_username = os.environ.get('REBOOT_USERNAME')
    reboot_password = os.environ.get('REBOOT_PASSWORD')
    database_url = os.environ.get('DATABASE_URL')
    
    if not reboot_username or not reboot_password:
        print("❌ ERROR: Reboot Motion credentials not set!")
        print("   Please set REBOOT_USERNAME and REBOOT_PASSWORD environment variables")
        sys.exit(1)
    
    if not database_url:
        print("⚠️  WARNING: DATABASE_URL not set, using SQLite fallback")
        print("   For production, set DATABASE_URL to PostgreSQL connection string")
        print()
    
    print(f"✅ Reboot Username: {reboot_username}")
    print(f"✅ Database: {'PostgreSQL' if database_url else 'SQLite (fallback)'}")
    print()
    
    try:
        from sync_service import RebootMotionSync
        
        # Initialize sync service
        print("🔄 Initializing Reboot Motion sync service...")
        sync = RebootMotionSync()
        
        print()
        print("=" * 70)
        print("PHASE 1: SYNC PLAYERS")
        print("=" * 70)
        
        # Run full sync
        result = sync.full_sync()
        
        print()
        print("=" * 70)
        print("✅ SYNC COMPLETE!")
        print("=" * 70)
        print(f"Players synced:      {result.get('players_synced', 0)}")
        print(f"Sessions synced:     {result.get('sessions_synced', 0)}")
        print(f"Biomechanics synced: {result.get('biomechanics_synced', 0)}")
        print(f"Status:              {result.get('status', 'unknown')}")
        print()
        print(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
        return 0
        
    except Exception as e:
        print()
        print("=" * 70)
        print("❌ SYNC FAILED!")
        print("=" * 70)
        print(f"Error: {e}")
        print()
        
        import traceback
        traceback.print_exc()
        
        return 1

if __name__ == "__main__":
    sys.exit(main())
