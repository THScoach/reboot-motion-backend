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
    raise ValueError("DATABASE_URL environment variable is not set!")

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
    Run database migrations to add missing columns
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
            
        logger.info("✅ Database migrations completed!")
        return True
    except Exception as e:
        logger.error(f"❌ Database migration failed: {e}")
        return False
