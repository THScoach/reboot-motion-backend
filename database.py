"""
Database Configuration and Connection
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import QueuePool
import logging

logger = logging.getLogger(__name__)

# Get DATABASE_URL from environment (Railway provides this automatically)
DATABASE_URL = os.environ.get('DATABASE_URL')

if not DATABASE_URL:
    # Fallback to SQLite for local development or when DATABASE_URL is not set
    logger.warning("⚠️ DATABASE_URL not set, using SQLite fallback")
    DATABASE_URL = "sqlite:///./catching_barrels.db"

# Create engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,  # Verify connections before using
    echo=False  # Set to True for SQL debugging
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Thread-safe session
db_session = scoped_session(SessionLocal)


def get_db():
    """
    Dependency for FastAPI routes
    Usage: db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initialize database - create all tables
    """
    from models import Base
    
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully!")


def check_db_connection():
    """
    Check if database connection is working
    """
    try:
        from sqlalchemy import text
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("✅ Database connection successful!")
        return True
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}")
        return False


def migrate_db():
    """
    Run database migrations to add missing columns and fix constraints
    """
    try:
        from sqlalchemy import text
        logger.info("🔄 Running database migrations...")
        
        with engine.connect() as conn:
            # Add new columns to sync_log table if they don't exist
            migrations = [
                "ALTER TABLE sync_log ADD COLUMN IF NOT EXISTS players_synced INTEGER DEFAULT 0",
                "ALTER TABLE sync_log ADD COLUMN IF NOT EXISTS sessions_synced INTEGER DEFAULT 0",
                "ALTER TABLE sync_log ADD COLUMN IF NOT EXISTS biomechanics_synced INTEGER DEFAULT 0",
            ]
            
            for migration in migrations:
                try:
                    conn.execute(text(migration))
                    conn.commit()
                    logger.info(f"✅ Migration executed: {migration[:50]}...")
                except Exception as e:
                    logger.warning(f"⚠️ Migration warning: {e}")
            
            # Fix session unique constraint to allow multiple players per session
            logger.info("🔄 Fixing session unique constraint...")
            
            # Drop old unique constraint on session_id
            try:
                conn.execute(text("ALTER TABLE sessions DROP CONSTRAINT IF EXISTS sessions_session_id_key CASCADE"))
                conn.commit()
                logger.info("✅ Dropped old session_id unique constraint")
            except Exception as e:
                logger.warning(f"⚠️ Drop constraint warning: {e}")
            
            # Drop old index
            try:
                conn.execute(text("DROP INDEX IF EXISTS ix_sessions_session_id CASCADE"))
                conn.commit()
                logger.info("✅ Dropped old session_id index")
            except Exception as e:
                logger.warning(f"⚠️ Drop index warning: {e}")
            
            # Add composite unique constraint (check if exists first)
            try:
                # Check if constraint already exists
                result = conn.execute(text(
                    "SELECT 1 FROM pg_constraint WHERE conname = 'uq_session_player'"
                )).fetchone()
                
                if not result:
                    conn.execute(text(
                        "ALTER TABLE sessions ADD CONSTRAINT uq_session_player UNIQUE (session_id, player_id)"
                    ))
                    conn.commit()
                    logger.info("✅ Added composite unique constraint (session_id, player_id)")
                else:
                    logger.info("✅ Composite unique constraint already exists")
            except Exception as e:
                logger.warning(f"⚠️ Add constraint warning: {e}")
            
            # Recreate non-unique index on session_id
            try:
                conn.execute(text("CREATE INDEX IF NOT EXISTS ix_sessions_session_id ON sessions(session_id)"))
                conn.commit()
                logger.info("✅ Created non-unique index on session_id")
            except Exception as e:
                logger.warning(f"⚠️ Create index warning: {e}")
            
        logger.info("✅ Database migrations completed!")
        return True
    except Exception as e:
        logger.error(f"❌ Database migration failed: {e}")
        return False
